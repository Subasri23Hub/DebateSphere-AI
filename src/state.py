"""
DebateSphere AI - State Schema
Defines the full debate state using TypedDict for LangGraph.
"""

from typing import TypedDict, List, Dict, Optional, Any


class DebateState(TypedDict):
    # Setup
    topic: str
    motion: str
    debate_mode: str
    debate_style: str
    tone: str
    domain: str
    pro_persona: str
    con_persona: str

    # Agent outputs
    moderator_intro: str
    pro_opening: str
    con_opening: str
    pro_rebuttal: str
    con_rebuttal: str
    cross_question: str
    pro_cross_response: str
    con_cross_response: str
    pro_closing: str
    con_closing: str

    # Analysis
    fact_review_notes: str
    judge_round_scores: Dict[str, Any]
    final_verdict: str
    winner: str

    # Transcript
    transcript: List[Dict[str, str]]

    # Q&A
    audience_questions: List[str]
    followup_answers: List[Dict[str, str]]

    # Flow control
    current_step: str
    error: Optional[str]
