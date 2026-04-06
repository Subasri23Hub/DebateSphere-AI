"""
DebateSphere AI - Workflow Nodes
=================================
Each function in this file is a single LangGraph node.

How it works:
  - There is ONE Gemini model instance shared across all nodes.
  - Each node receives the current debate state, builds a role-specific
    prompt, calls Gemini, and writes its output back into the state.
  - There are NO agents, agent executors, or multi-agent frameworks.
  - This is a plain sequential LangGraph workflow:
        setup → moderator → pro_opening → con_opening → ... → judge → END

The "role simulation" happens entirely through prompt design — Gemini is
instructed to respond as a moderator, or a PRO debater, or a judge,
depending on which node is currently executing.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from src.config import GOOGLE_API_KEY, GEMINI_MODEL
from src.state import DebateState
from src.prompts import (
    MODERATOR_PROMPT,
    PRO_OPENING_PROMPT,
    CON_OPENING_PROMPT,
    PRO_REBUTTAL_PROMPT,
    CON_REBUTTAL_PROMPT,
    FACT_CHECK_PROMPT,
    CROSS_QUESTION_PROMPT,
    PRO_CROSS_RESPONSE_PROMPT,
    CON_CROSS_RESPONSE_PROMPT,
    PRO_CLOSING_PROMPT,
    CON_CLOSING_PROMPT,
    JUDGE_SCORING_PROMPT,
    AUDIENCE_QA_PROMPT,
)


# ─────────────────────────────────────────────
#  SHARED GEMINI MODEL
#  One model, used by every node in the graph.
# ─────────────────────────────────────────────
def _get_model() -> ChatGoogleGenerativeAI:
    """
    Create and return the Gemini model instance.
    Called fresh each time to avoid stale state across workflow runs.
    """
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.85,
    )


def _call_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.
    This is the single point of LLM invocation used by every node.
    """
    model = _get_model()
    response = model.invoke([HumanMessage(content=prompt)])
    return response.content.strip()


# ─────────────────────────────────────────────
#  TRANSCRIPT HELPER
# ─────────────────────────────────────────────
def _add_to_transcript(
    state: DebateState,
    speaker: str,
    stage: str,
    content: str,
) -> list:
    """
    Append a new entry to the running debate transcript.
    Returns the updated transcript list.
    """
    transcript = list(state.get("transcript", []))
    transcript.append({
        "speaker": speaker,
        "round": stage,
        "content": content,
    })
    return transcript


# ═════════════════════════════════════════════
#  LANGGRAPH NODE FUNCTIONS
#  Each function below = one node in the graph.
#  Signature: (state: DebateState) -> DebateState
# ═════════════════════════════════════════════

# ── Node 1: Setup ────────────────────────────
def setup_node(state: DebateState) -> DebateState:
    """
    Initialise all output fields to empty before the workflow begins.
    No LLM call is made here — this is purely a state reset step.
    """
    state["current_step"] = "setup"
    state["transcript"] = []
    state["audience_questions"] = []
    state["followup_answers"] = []
    state["error"] = None
    return state


# ── Node 2: Moderator Introduction ───────────
def moderator_intro_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted to respond as a neutral debate moderator.
    Introduces the motion, participants, and structure.
    """
    state["current_step"] = "moderator_intro"

    prompt = MODERATOR_PROMPT.format(
        style=state["debate_style"],
        tone=state["tone"],
        domain=state["domain"],
        pro_persona=state["pro_persona"],
        con_persona=state["con_persona"],
        motion=state["motion"],
    )
    output = _call_gemini(prompt)

    state["moderator_intro"] = output
    state["transcript"] = _add_to_transcript(state, "Moderator", "intro", output)
    return state


# ── Node 3: PRO Opening Statement ────────────
def pro_opening_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted to respond as the PRO debater.
    Delivers a structured opening statement in favour of the motion.
    """
    state["current_step"] = "pro_opening"

    prompt = PRO_OPENING_PROMPT.format(
        pro_persona=state["pro_persona"],
        style=state["debate_style"],
        tone=state["tone"],
        domain=state["domain"],
        motion=state["motion"],
    )
    output = _call_gemini(prompt)

    state["pro_opening"] = output
    state["transcript"] = _add_to_transcript(state, "Pro", "opening", output)
    return state


# ── Node 4: CON Opening Statement ────────────
def con_opening_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted to respond as the CON debater.
    Delivers a structured opening statement against the motion.
    """
    state["current_step"] = "con_opening"

    prompt = CON_OPENING_PROMPT.format(
        con_persona=state["con_persona"],
        style=state["debate_style"],
        tone=state["tone"],
        domain=state["domain"],
        motion=state["motion"],
    )
    output = _call_gemini(prompt)

    state["con_opening"] = output
    state["transcript"] = _add_to_transcript(state, "Con", "opening", output)
    return state


# ── Node 5: PRO Rebuttal ──────────────────────
def pro_rebuttal_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted as the PRO debater responding to CON's opening.
    Counters weaknesses and reinforces PRO's own position.
    """
    state["current_step"] = "pro_rebuttal"

    prompt = PRO_REBUTTAL_PROMPT.format(
        pro_persona=state["pro_persona"],
        style=state["debate_style"],
        tone=state["tone"],
        motion=state["motion"],
        con_opening=state.get("con_opening", ""),
    )
    output = _call_gemini(prompt)

    state["pro_rebuttal"] = output
    state["transcript"] = _add_to_transcript(state, "Pro", "rebuttal", output)
    return state


# ── Node 6: CON Rebuttal ──────────────────────
def con_rebuttal_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted as the CON debater responding to PRO's opening.
    Challenges assumptions and exposes weaknesses in PRO's arguments.
    """
    state["current_step"] = "con_rebuttal"

    prompt = CON_REBUTTAL_PROMPT.format(
        con_persona=state["con_persona"],
        style=state["debate_style"],
        tone=state["tone"],
        motion=state["motion"],
        pro_opening=state.get("pro_opening", ""),
    )
    output = _call_gemini(prompt)

    state["con_rebuttal"] = output
    state["transcript"] = _add_to_transcript(state, "Con", "rebuttal", output)
    return state


# ── Node 7: Fact-Check Stage ─────────────────
def fact_review_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted as a neutral fact-check reviewer.
    Classifies claims from both sides as factual, opinion, prediction, etc.
    This is still a simple Gemini call — no external tools or web search.
    """
    state["current_step"] = "fact_review"

    prompt = FACT_CHECK_PROMPT.format(
        motion=state["motion"],
        pro_opening=state.get("pro_opening", ""),
        con_opening=state.get("con_opening", ""),
        pro_rebuttal=state.get("pro_rebuttal", ""),
        con_rebuttal=state.get("con_rebuttal", ""),
    )
    output = _call_gemini(prompt)

    state["fact_review_notes"] = output
    state["transcript"] = _add_to_transcript(state, "Fact-Check Analyst", "fact_review", output)
    return state


# ── Node 8: Cross-Examination Question ───────
def cross_question_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted as the moderator to generate one sharp
    cross-examination question that challenges both sides equally.
    """
    state["current_step"] = "cross_question"

    prompt = CROSS_QUESTION_PROMPT.format(
        motion=state["motion"],
        pro_opening=state.get("pro_opening", ""),
        con_opening=state.get("con_opening", ""),
    )
    output = _call_gemini(prompt)

    state["cross_question"] = output
    state["transcript"] = _add_to_transcript(state, "Moderator", "cross_question", output)
    return state


# ── Node 9: PRO Cross-Examination Response ───
def pro_cross_response_node(state: DebateState) -> DebateState:
    """
    Gemini responds as the PRO debater answering the cross-question.
    """
    state["current_step"] = "pro_cross_response"

    prompt = PRO_CROSS_RESPONSE_PROMPT.format(
        pro_persona=state["pro_persona"],
        motion=state["motion"],
        cross_question=state.get("cross_question", ""),
    )
    output = _call_gemini(prompt)

    state["pro_cross_response"] = output
    state["transcript"] = _add_to_transcript(state, "Pro", "cross_response", output)
    return state


# ── Node 10: CON Cross-Examination Response ──
def con_cross_response_node(state: DebateState) -> DebateState:
    """
    Gemini responds as the CON debater answering the cross-question.
    """
    state["current_step"] = "con_cross_response"

    prompt = CON_CROSS_RESPONSE_PROMPT.format(
        con_persona=state["con_persona"],
        motion=state["motion"],
        cross_question=state.get("cross_question", ""),
    )
    output = _call_gemini(prompt)

    state["con_cross_response"] = output
    state["transcript"] = _add_to_transcript(state, "Con", "cross_response", output)
    return state


# ── Node 11: PRO Closing Statement ───────────
def pro_closing_node(state: DebateState) -> DebateState:
    """
    Gemini responds as the PRO debater delivering a closing statement.
    Summarises key points and makes a final persuasive appeal.
    """
    state["current_step"] = "pro_closing"

    prompt = PRO_CLOSING_PROMPT.format(
        pro_persona=state["pro_persona"],
        style=state["debate_style"],
        tone=state["tone"],
        motion=state["motion"],
    )
    output = _call_gemini(prompt)

    state["pro_closing"] = output
    state["transcript"] = _add_to_transcript(state, "Pro", "closing", output)
    return state


# ── Node 12: CON Closing Statement ───────────
def con_closing_node(state: DebateState) -> DebateState:
    """
    Gemini responds as the CON debater delivering a closing statement.
    Summarises counter-points and leaves a strong final impression.
    """
    state["current_step"] = "con_closing"

    prompt = CON_CLOSING_PROMPT.format(
        con_persona=state["con_persona"],
        style=state["debate_style"],
        tone=state["tone"],
        motion=state["motion"],
    )
    output = _call_gemini(prompt)

    state["con_closing"] = output
    state["transcript"] = _add_to_transcript(state, "Con", "closing", output)
    return state


# ── Node 13: Judge Verdict ────────────────────
def judge_verdict_node(state: DebateState) -> DebateState:
    """
    Gemini is prompted as an impartial judge.
    Reads the entire debate transcript from state and produces:
      - Scores per dimension (Logic, Clarity, Evidence, Persuasion, Rebuttal)
      - A declared winner
      - Analysis of strongest/weakest points and logical issues
    """
    state["current_step"] = "final_judge"

    prompt = JUDGE_SCORING_PROMPT.format(
        motion=state["motion"],
        style=state["debate_style"],
        domain=state["domain"],
        moderator_intro=state.get("moderator_intro", ""),
        pro_opening=state.get("pro_opening", ""),
        con_opening=state.get("con_opening", ""),
        pro_rebuttal=state.get("pro_rebuttal", ""),
        con_rebuttal=state.get("con_rebuttal", ""),
        cross_question=state.get("cross_question", ""),
        pro_cross_response=state.get("pro_cross_response", ""),
        con_cross_response=state.get("con_cross_response", ""),
        pro_closing=state.get("pro_closing", ""),
        con_closing=state.get("con_closing", ""),
        fact_review_notes=state.get("fact_review_notes", ""),
    )
    output = _call_gemini(prompt)

    state["final_verdict"] = output

    # Determine winner from the verdict text
    winner = "DRAW"
    upper = output.upper()
    if "WINNER: PRO" in upper:
        winner = "PRO"
    elif "WINNER: CON" in upper:
        winner = "CON"
    state["winner"] = winner

    state["transcript"] = _add_to_transcript(state, "Judge", "final_verdict", output)
    return state


# ═════════════════════════════════════════════
#  AUDIENCE Q&A  (called directly, not via graph)
#  This is a standalone Gemini call triggered by
#  user interaction after the debate finishes.
# ═════════════════════════════════════════════
def answer_audience_question(
    state: DebateState,
    question: str,
    target: str,
) -> str:
    """
    Takes a post-debate audience question and generates a response
    from the perspective of the chosen target (Pro / Con / Judge / Neutral).
    Called directly from app.py — not part of the LangGraph workflow.
    """
    prompt = AUDIENCE_QA_PROMPT.format(
        motion=state["motion"],
        target=target,
        pro_opening=state.get("pro_opening", ""),
        con_opening=state.get("con_opening", ""),
        winner=state.get("winner", "DRAW"),
        question=question,
    )
    return _call_gemini(prompt)
