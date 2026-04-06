"""
DebateSphere AI
================
A structured AI debate simulator built with LangGraph, Gemini API, and Streamlit.

How it works:
  A single Gemini model is invoked across 13 sequential LangGraph workflow
  stages. Each stage sends a role-specific prompt (moderator, PRO debater,
  CON debater, fact-check reviewer, judge) and writes the output into a
  shared state dictionary. Streamlit renders the results live.

Run with:
    streamlit run app.py
"""

import streamlit as st

# ── Page config MUST be the very first Streamlit call ──
st.set_page_config(
    page_title="DebateSphere AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ──
from ui.styles import MAIN_CSS
from ui.components import (
    render_header,
    render_progress,
    render_speaker_card,
    render_score_radar,
    render_score_bars,
    render_winner_banner,
    render_verdict_highlights,
    render_transcript,
    render_qa_block,
    render_divider,
)
from src.config import (
    DEBATE_MODES, DEBATE_STYLES, DEBATE_TONES,
    DEBATE_DOMAINS, PRO_PERSONAS, CON_PERSONAS,
)
from src.graph import debate_graph
from src.nodes import answer_audience_question   # standalone Q&A call (not in graph)
from src.scoring import parse_scores_from_verdict
from src.utils import (
    load_sample_topics, transcript_to_text,
    generate_debate_id,
)

# ── Inject premium CSS ──
st.markdown(MAIN_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
if "debate_state" not in st.session_state:
    st.session_state.debate_state = None
if "debate_running" not in st.session_state:
    st.session_state.debate_running = False
if "debate_done" not in st.session_state:
    st.session_state.debate_done = False
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "debate_id" not in st.session_state:
    st.session_state.debate_id = None

sample_topics = load_sample_topics()


# ─────────────────────────────────────────────
#  SIDEBAR — CONFIGURATION PANEL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size:1.8rem;">⚖️</div>
        <div style="font-size:1rem; font-weight:700; color:#f1f5f9; letter-spacing:0.03em;">
            DebateSphere AI
        </div>
        <div style="font-size:0.7rem; color:#64748b; margin-top:0.2rem;">
            Structured Debate Simulator
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Debate Topic</div>', unsafe_allow_html=True)

    # Topic suggestion picker
    domain_pick = st.selectbox(
        "Browse topics by domain",
        ["— pick a domain —"] + list(sample_topics.keys()),
        key="domain_picker",
    )
    suggested_topic = ""
    if domain_pick != "— pick a domain —" and domain_pick in sample_topics:
        suggested_topic = st.selectbox(
            "Suggested topics",
            ["— custom —"] + sample_topics[domain_pick],
            key="topic_picker",
        )

    motion_default = (
        suggested_topic
        if suggested_topic and suggested_topic != "— custom —"
        else ""
    )
    motion_input = st.text_area(
        "Motion / Topic",
        value=motion_default,
        placeholder="e.g. Should AI replace first-round job interviews?",
        height=90,
        key="motion_input",
    )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Debate Configuration</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        debate_mode  = st.selectbox("Mode",         DEBATE_MODES,   key="debate_mode")
        debate_style = st.selectbox("Style",        DEBATE_STYLES,  key="debate_style")
        tone         = st.selectbox("Tone",         DEBATE_TONES,   key="tone")
    with col_b:
        domain       = st.selectbox("Domain",       DEBATE_DOMAINS, key="domain")
        pro_persona  = st.selectbox("PRO Persona",  PRO_PERSONAS,   key="pro_persona")
        con_persona  = st.selectbox("CON Persona",  CON_PERSONAS,   key="con_persona")

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    start_btn = st.button("🚀 Start Debate",  type="primary", use_container_width=True)
    clear_btn = st.button("🗑️ Clear Session", use_container_width=True)

    if clear_btn:
        for key in ["debate_state", "debate_running", "debate_done", "qa_history", "debate_id"]:
            if key == "debate_state":
                st.session_state[key] = None
            elif key in ("debate_running", "debate_done"):
                st.session_state[key] = False
            elif key == "qa_history":
                st.session_state[key] = []
            else:
                st.session_state[key] = None
        st.rerun()

    # Transcript download (available once debate is complete)
    if st.session_state.debate_done and st.session_state.debate_state:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        transcript_txt = transcript_to_text(
            st.session_state.debate_state.get("transcript", [])
        )
        st.download_button(
            label="📥 Download Transcript",
            data=transcript_txt,
            file_name=f"debate_{st.session_state.debate_id}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("""
    <div style="text-align:center; margin-top:2rem; font-size:0.65rem; color:#334155;">
        Powered by LangGraph · Gemini AI · Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TRIGGER: START DEBATE
# ─────────────────────────────────────────────
if start_btn:
    if not motion_input.strip():
        st.error("Please enter a debate motion or topic.")
        st.stop()

    from src.config import GOOGLE_API_KEY
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
        st.error("⚠️ Google API key not set. Add your key to the `.env` file.")
        st.stop()

    st.session_state.debate_running = True
    st.session_state.debate_done    = False
    st.session_state.qa_history     = []
    st.session_state.debate_id      = generate_debate_id()

    # ── Initial state passed into the LangGraph workflow ──
    initial_state = {
        "topic":        motion_input.strip(),
        "motion":       motion_input.strip(),
        "debate_mode":  debate_mode,
        "debate_style": debate_style,
        "tone":         tone,
        "domain":       domain,
        "pro_persona":  pro_persona,
        "con_persona":  con_persona,
        # All output fields start empty
        "moderator_intro":    "",
        "pro_opening":        "",
        "con_opening":        "",
        "pro_rebuttal":       "",
        "con_rebuttal":       "",
        "cross_question":     "",
        "pro_cross_response": "",
        "con_cross_response": "",
        "pro_closing":        "",
        "con_closing":        "",
        "fact_review_notes":  "",
        "judge_round_scores": {},
        "final_verdict":      "",
        "winner":             "",
        "transcript":         [],
        "audience_questions": [],
        "followup_answers":   [],
        "current_step":       "setup",
        "error":              None,
    }

    # ── Live progress display during workflow execution ──
    render_header()
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <span class="status-pill status-running">
            ⚡ Debate in Progress — ID: {st.session_state.debate_id}
        </span>
    </div>
    """, unsafe_allow_html=True)

    progress_placeholder = st.empty()
    status_placeholder   = st.empty()
    cards_container      = st.container()

    # Human-readable label for each workflow stage
    step_messages = {
        "setup":               "Initialising workflow...",
        "moderator_intro":     "🎙️ Moderator stage — setting the scene...",
        "pro_opening":         "🔵 PRO stage — crafting opening statement...",
        "con_opening":         "🔴 CON stage — crafting opening statement...",
        "pro_rebuttal":        "🔵 PRO stage — formulating rebuttal...",
        "con_rebuttal":        "🔴 CON stage — formulating rebuttal...",
        "fact_review":         "🟣 Fact-check stage — reviewing claims...",
        "cross_question":      "⚪ Moderator stage — forming cross-question...",
        "pro_cross_response":  "🔵 PRO stage — answering cross-question...",
        "con_cross_response":  "🔴 CON stage — answering cross-question...",
        "pro_closing":         "🔵 PRO stage — preparing closing statement...",
        "con_closing":         "🔴 CON stage — preparing closing statement...",
        "final_judge":         "🟡 Judge stage — analysing full debate...",
    }

    rendered_steps = set()
    final_state    = None

    # ── Stream the graph node by node ──
    with st.spinner(""):
        for step_output in debate_graph.stream(initial_state):
            for node_name, state in step_output.items():
                final_state = state
                current     = state.get("current_step", node_name)

                with progress_placeholder.container():
                    render_progress(current)

                with status_placeholder.container():
                    msg = step_messages.get(current, f"Running stage: {current}...")
                    st.markdown(f"""
                    <div style="text-align:center; margin-bottom:1rem;
                                color:#94a3b8; font-size:0.85rem;">
                        {msg}
                    </div>
                    """, unsafe_allow_html=True)

                # Render new transcript entries as they arrive
                transcript = state.get("transcript", [])
                for entry in transcript:
                    entry_key = f"{entry['speaker']}_{entry['round']}"
                    if entry_key not in rendered_steps:
                        rendered_steps.add(entry_key)
                        with cards_container:
                            # Judge verdict is rendered in the Verdict tab, not here
                            if entry["round"] != "final_verdict":
                                render_speaker_card(
                                    entry["speaker"],
                                    entry["round"],
                                    entry["content"],
                                )

    # ── Store completed state and trigger re-render ──
    if final_state:
        st.session_state.debate_state   = final_state
        st.session_state.debate_done    = True
        st.session_state.debate_running = False

        status_placeholder.empty()
        with progress_placeholder.container():
            render_progress("final_judge")
            st.markdown("""
            <div style="text-align:center; margin-top:0.5rem;">
                <span class="status-pill status-done">✅ Debate Complete</span>
            </div>
            """, unsafe_allow_html=True)

    st.rerun()


# ─────────────────────────────────────────────
#  MAIN DISPLAY (renders after debate completes)
# ─────────────────────────────────────────────
render_header()

state = st.session_state.debate_state

# ── Empty / welcome state ──
if not state:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚖️</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: #64748b; margin-bottom: 0.6rem;">
            No debate running yet
        </div>
        <div style="font-size: 0.9rem; color: #475569; max-width:500px; margin:0 auto;">
            Configure your debate settings in the sidebar and click
            <strong style="color:#3b82f6;">🚀 Start Debate</strong> to begin.
        </div>
        <div style="margin-top:2rem; display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;
                        padding:1rem 1.5rem;min-width:150px;">
                <div style="font-size:1.5rem;">🔗</div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:0.3rem;font-weight:600;">
                    LangGraph Workflow
                </div>
            </div>
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;
                        padding:1rem 1.5rem;min-width:150px;">
                <div style="font-size:1.5rem;">📋</div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:0.3rem;font-weight:600;">
                    13-Stage Workflow
                </div>
            </div>
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;
                        padding:1rem 1.5rem;min-width:150px;">
                <div style="font-size:1.5rem;">🏆</div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:0.3rem;font-weight:600;">
                    Judge & Scoring Stage
                </div>
            </div>
            <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;
                        padding:1rem 1.5rem;min-width:150px;">
                <div style="font-size:1.5rem;">🎯</div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:0.3rem;font-weight:600;">
                    Fact-Check Stage
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Full results display (debate complete) ──
if st.session_state.debate_done:
    motion     = state.get("motion", "")
    winner     = state.get("winner", "DRAW")
    verdict    = state.get("final_verdict", "")
    transcript = state.get("transcript", [])

    # Top status bar
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between;
                margin-bottom:1.2rem; flex-wrap:wrap; gap:0.5rem;">
        <div>
            <span style="font-size:0.65rem; color:#64748b; font-weight:700;
                         letter-spacing:0.1em; text-transform:uppercase;">
                Debate ID: {st.session_state.debate_id}
            </span>
            <div style="font-size:1rem; color:#f1f5f9; font-weight:600; margin-top:0.2rem;">
                {motion}
            </div>
        </div>
        <span class="status-pill status-done">✅ Complete</span>
    </div>
    """, unsafe_allow_html=True)

    render_progress("final_judge")

    # ── Five-tab result layout ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏟️ Debate Arena",
        "🏆 Verdict & Scores",
        "🟣 Fact-Check",
        "💬 Audience Q&A",
        "📜 Full Transcript",
    ])

    # ──────────────── TAB 1: DEBATE ARENA ────────────────
    with tab1:
        st.markdown('<div class="section-heading">Debate Arena</div>', unsafe_allow_html=True)

        if state.get("moderator_intro"):
            render_speaker_card("Moderator", "intro", state["moderator_intro"])
        render_divider()

        st.markdown('<div class="section-heading">Opening Statements</div>', unsafe_allow_html=True)
        col_pro, col_con = st.columns(2)
        with col_pro:
            if state.get("pro_opening"):
                render_speaker_card("Pro", "opening", state["pro_opening"])
        with col_con:
            if state.get("con_opening"):
                render_speaker_card("Con", "opening", state["con_opening"])

        render_divider()

        st.markdown('<div class="section-heading">Rebuttals</div>', unsafe_allow_html=True)
        col_pro2, col_con2 = st.columns(2)
        with col_pro2:
            if state.get("pro_rebuttal"):
                render_speaker_card("Pro", "rebuttal", state["pro_rebuttal"])
        with col_con2:
            if state.get("con_rebuttal"):
                render_speaker_card("Con", "rebuttal", state["con_rebuttal"])

        render_divider()

        if state.get("cross_question"):
            st.markdown('<div class="section-heading">Cross-Examination</div>', unsafe_allow_html=True)
            render_speaker_card("Moderator", "cross_question", state["cross_question"])
            col_p3, col_c3 = st.columns(2)
            with col_p3:
                if state.get("pro_cross_response"):
                    render_speaker_card("Pro", "cross_response", state["pro_cross_response"])
            with col_c3:
                if state.get("con_cross_response"):
                    render_speaker_card("Con", "cross_response", state["con_cross_response"])

        render_divider()

        st.markdown('<div class="section-heading">Closing Statements</div>', unsafe_allow_html=True)
        col_pro4, col_con4 = st.columns(2)
        with col_pro4:
            if state.get("pro_closing"):
                render_speaker_card("Pro", "closing", state["pro_closing"])
        with col_con4:
            if state.get("con_closing"):
                render_speaker_card("Con", "closing", state["con_closing"])

    # ──────────────── TAB 2: VERDICT & SCORES ────────────────
    with tab2:
        st.markdown('<div class="section-heading">Final Verdict</div>', unsafe_allow_html=True)
        render_winner_banner(winner)

        if verdict:
            render_divider()
            scores    = parse_scores_from_verdict(verdict)
            has_scores = bool(scores["pro"] and scores["con"])

            if has_scores:
                st.markdown('<div class="section-heading">Score Breakdown</div>', unsafe_allow_html=True)
                sc1, sc2 = st.columns(2)
                with sc1:
                    render_score_bars(scores, "pro")
                with sc2:
                    render_score_bars(scores, "con")

                render_divider()
                st.markdown('<div class="section-heading">Performance Radar</div>', unsafe_allow_html=True)
                render_score_radar(scores)

            render_divider()
            st.markdown('<div class="section-heading">Verdict Analysis</div>', unsafe_allow_html=True)
            render_verdict_highlights(verdict)

            render_divider()
            with st.expander("📄 Full Judge Verdict (Raw)"):
                st.markdown(f"""
                <div class="debate-card card-judge">
                    <div class="card-content">{verdict}</div>
                </div>
                """, unsafe_allow_html=True)

    # ──────────────── TAB 3: FACT-CHECK ────────────────
    with tab3:
        st.markdown('<div class="section-heading">Fact-Check & Claim Analysis</div>', unsafe_allow_html=True)
        fact_notes = state.get("fact_review_notes", "")
        if fact_notes:
            render_speaker_card("Fact-Check Analyst", "fact_review", fact_notes)
        else:
            st.info("No fact-check data available.")

    # ──────────────── TAB 4: AUDIENCE Q&A ────────────────
    with tab4:
        st.markdown('<div class="section-heading">Audience Q&A</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="color:#64748b; font-size:0.85rem; margin-bottom:1rem;">
            Ask follow-up questions and direct them to any debate participant.
        </div>
        """, unsafe_allow_html=True)

        qa_col1, qa_col2 = st.columns([3, 1])
        with qa_col1:
            qa_question = st.text_input(
                "Your Question",
                placeholder="e.g. What would be the biggest risk if this motion passed?",
                key="qa_input",
            )
        with qa_col2:
            qa_target = st.selectbox(
                "Direct to",
                ["Pro", "Con", "Judge", "Neutral Summary"],
                key="qa_target",
            )

        ask_btn = st.button("💬 Ask Question", type="primary")

        if ask_btn and qa_question.strip():
            with st.spinner("Generating response..."):
                answer = answer_audience_question(state, qa_question.strip(), qa_target)
            st.session_state.qa_history.append({
                "question": qa_question.strip(),
                "target":   qa_target,
                "answer":   answer,
            })

        if st.session_state.qa_history:
            render_divider()
            st.markdown('<div class="section-heading">Q&A History</div>', unsafe_allow_html=True)
            for qa in reversed(st.session_state.qa_history):
                render_qa_block(qa["question"], qa["target"], qa["answer"])

    # ──────────────── TAB 5: FULL TRANSCRIPT ────────────────
    with tab5:
        st.markdown('<div class="section-heading">Full Debate Transcript</div>', unsafe_allow_html=True)
        render_transcript(transcript)

        if transcript:
            render_divider()
            transcript_txt = transcript_to_text(transcript)
            st.download_button(
                "📥 Download Full Transcript (.txt)",
                data=transcript_txt,
                file_name=f"debate_{st.session_state.debate_id}.txt",
                mime="text/plain",
            )
