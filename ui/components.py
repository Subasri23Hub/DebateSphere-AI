"""
DebateSphere AI - UI Components
Reusable Streamlit rendering components.
"""

import streamlit as st
import plotly.graph_objects as go
from src.scoring import parse_scores_from_verdict, get_score_color, SCORE_DIMENSIONS
from src.formatter import (
    format_round_label,
    extract_winner_line,
    extract_balanced_takeaway,
    extract_strongest_argument,
    extract_weakest_points,
    extract_logical_issues,
)


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">⚖️ DebateSphere AI</div>
        <div class="hero-subtitle">
            Structured Debate Simulator · Role-Based Prompting · AI-Powered Verdicts
        </div>
        <div class="hero-badges">
            <span class="badge">🔗 LangGraph</span>
            <span class="badge">✨ Gemini AI</span>
            <span class="badge">🎯 13-Stage Workflow</span>
            <span class="badge">⚡ Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PROGRESS TRACKER
# ─────────────────────────────────────────────
STEPS = [
    "setup", "moderator_intro", "pro_opening", "con_opening",
    "pro_rebuttal", "con_rebuttal", "fact_review", "cross_question",
    "pro_cross_response", "con_cross_response", "pro_closing",
    "con_closing", "final_judge",
]

STEP_LABELS = [
    "Setup", "Intro", "PRO Open", "CON Open",
    "PRO Rebut", "CON Rebut", "Fact-Check", "Cross-Q",
    "PRO Ans", "CON Ans", "PRO Close", "CON Close", "Verdict",
]

def render_progress(current_step: str):
    try:
        current_idx = STEPS.index(current_step)
    except ValueError:
        current_idx = -1

    dots = ""
    for i, _ in enumerate(STEPS):
        if i < current_idx:
            dots += '<div class="step-dot done"></div>'
        elif i == current_idx:
            dots += '<div class="step-dot active"></div>'
        else:
            dots += '<div class="step-dot"></div>'

    label = STEP_LABELS[current_idx] if 0 <= current_idx < len(STEP_LABELS) else ""
    st.markdown(f"""
    <div style="margin-bottom:0.3rem">
        <span class="section-heading">Workflow Progress — {label}</span>
    </div>
    <div class="step-progress">{dots}</div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SPEAKER CARD
# ─────────────────────────────────────────────
def render_speaker_card(speaker: str, round_name: str, content: str):
    speaker_lower = speaker.lower()
    if "moderator" in speaker_lower:
        card_class, label_class, icon = "card-moderator", "label-moderator", "⚪"
        label = "MODERATOR"
    elif "pro" in speaker_lower:
        card_class, label_class, icon = "card-pro", "label-pro", "🔵"
        label = "PRO DEBATER"
    elif "con" in speaker_lower:
        card_class, label_class, icon = "card-con", "label-con", "🔴"
        label = "CON DEBATER"
    elif "judge" in speaker_lower:
        card_class, label_class, icon = "card-judge", "label-judge", "🟡"
        label = "JUDGE"
    elif "fact" in speaker_lower:
        card_class, label_class, icon = "card-fact", "label-fact", "🟣"
        label = "FACT-CHECK STAGE"
    else:
        card_class, label_class, icon = "debate-card", "label-moderator", "🎤"
        label = speaker.upper()

    round_display = format_round_label(round_name)

    st.markdown(f"""
    <div class="debate-card {card_class}">
        <div class="card-speaker-label">
            <span class="{label_class}">{icon} {label}</span>
            <span class="card-round-tag">{round_display}</span>
        </div>
        <div class="card-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SCORE CHART (Plotly radar)
# ─────────────────────────────────────────────
def render_score_radar(scores: dict):
    pro_scores = [scores["pro"].get(d, 0) for d in SCORE_DIMENSIONS]
    con_scores = [scores["con"].get(d, 0) for d in SCORE_DIMENSIONS]
    dims = SCORE_DIMENSIONS + [SCORE_DIMENSIONS[0]]  # close the radar
    pro_scores_c = pro_scores + [pro_scores[0]]
    con_scores_c = con_scores + [con_scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=pro_scores_c, theta=dims, fill='toself',
        name='PRO', line_color='#3b82f6',
        fillcolor='rgba(59,130,246,0.15)',
        line_width=2,
    ))
    fig.add_trace(go.Scatterpolar(
        r=con_scores_c, theta=dims, fill='toself',
        name='CON', line_color='#ef4444',
        fillcolor='rgba(239,68,68,0.15)',
        line_width=2,
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 10], color='#64748b',
                            gridcolor='rgba(255,255,255,0.08)', tickfont_size=10),
            angularaxis=dict(color='#94a3b8', gridcolor='rgba(255,255,255,0.08)'),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(font=dict(color='#94a3b8', size=11), bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=20, b=20, l=30, r=30),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
#  SCORE BAR CARD (HTML)
# ─────────────────────────────────────────────
def render_score_bars(scores: dict, side: str):
    color = "#3b82f6" if side == "pro" else "#ef4444"
    title = "🔵 PRO SCORES" if side == "pro" else "🔴 CON SCORES"
    total = scores.get(f"{side}_total", 0)
    rows_html = ""
    for dim in SCORE_DIMENSIONS:
        val = scores[side].get(dim, 0)
        pct = val * 10
        bar_color = get_score_color(val)
        rows_html += f"""
        <div class="score-row">
            <span class="score-label">{dim}</span>
            <div class="score-bar-container">
                <div class="score-bar" style="width:{pct}%;background:{bar_color};"></div>
            </div>
            <span class="score-number" style="color:{bar_color};">{val}/10</span>
        </div>"""

    st.markdown(f"""
    <div class="score-block">
        <div class="score-title" style="color:{color};">{title}</div>
        {rows_html}
        <div class="score-total-row">
            <span style="color:{color};">Total Score</span>
            <span style="color:{color};">{total} / 50</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  WINNER BANNER
# ─────────────────────────────────────────────
def render_winner_banner(winner: str):
    if winner == "PRO":
        css_class = "pro"
        emoji = "🏆"
        text = "PRO Wins the Debate!"
        sub = "The PRO side delivered the stronger case."
    elif winner == "CON":
        css_class = "con"
        emoji = "🏆"
        text = "CON Wins the Debate!"
        sub = "The CON side delivered the stronger case."
    else:
        css_class = "draw"
        emoji = "🤝"
        text = "The Debate Ends in a Draw"
        sub = "Both sides made equally compelling arguments."

    st.markdown(f"""
    <div class="winner-banner {css_class}">
        <div class="winner-label">{emoji}</div>
        <div class="winner-text">{text}</div>
        <div class="winner-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  VERDICT HIGHLIGHTS
# ─────────────────────────────────────────────
def render_verdict_highlights(verdict_text: str):
    strongest = extract_strongest_argument(verdict_text)
    weakest = extract_weakest_points(verdict_text)
    logical = extract_logical_issues(verdict_text)
    takeaway = extract_balanced_takeaway(verdict_text)

    if strongest:
        st.markdown(f"""
        <div class="verdict-highlight">
            <div class="verdict-highlight-title">⭐ Strongest Argument Overall</div>
            {strongest}
        </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if weakest["pro"]:
            st.markdown(f"""
            <div class="verdict-highlight">
                <div class="verdict-highlight-title" style="color:#3b82f6;">🔵 PRO Weakest Point</div>
                {weakest["pro"]}
            </div>""", unsafe_allow_html=True)
    with col2:
        if weakest["con"]:
            st.markdown(f"""
            <div class="verdict-highlight">
                <div class="verdict-highlight-title" style="color:#ef4444;">🔴 CON Weakest Point</div>
                {weakest["con"]}
            </div>""", unsafe_allow_html=True)

    if logical:
        st.markdown(f"""
        <div class="verdict-highlight">
            <div class="verdict-highlight-title">⚠️ Logical Issues Detected</div>
            {logical}
        </div>""", unsafe_allow_html=True)

    if takeaway:
        st.markdown(f"""
        <div class="verdict-highlight" style="border-color:#f59e0b;">
            <div class="verdict-highlight-title" style="color:#f59e0b;">🌐 Balanced Takeaway</div>
            {takeaway}
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TRANSCRIPT VIEWER
# ─────────────────────────────────────────────
def render_transcript(transcript: list):
    if not transcript:
        st.info("No transcript yet.")
        return
    for entry in transcript:
        render_speaker_card(
            entry.get("speaker", ""),
            entry.get("round", ""),
            entry.get("content", ""),
        )


# ─────────────────────────────────────────────
#  Q&A BLOCK
# ─────────────────────────────────────────────
def render_qa_block(question: str, target: str, answer: str):
    st.markdown(f"""
    <div class="qa-block">
        <div class="qa-question">❓ Question to {target}: {question}</div>
        <div class="qa-answer">{answer}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FANCY DIVIDER
# ─────────────────────────────────────────────
def render_divider():
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
