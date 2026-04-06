"""
DebateSphere AI - LangGraph Workflow
======================================
Builds and compiles the structured debate workflow using LangGraph.

Architecture:
  - One StateGraph with a single DebateState schema
  - 13 sequential nodes, each a plain Python function
  - Linear edges: every node connects to the next one in order
  - No conditional branching, no routing, no agent frameworks

Flow:
  START
    → setup
    → moderator_intro
    → pro_opening
    → con_opening
    → pro_rebuttal
    → con_rebuttal
    → fact_review
    → cross_question
    → pro_cross_response
    → con_cross_response
    → pro_closing
    → con_closing
    → judge_verdict
  END
"""

from langgraph.graph import StateGraph, END

from src.state import DebateState
from src.nodes import (
    setup_node,
    moderator_intro_node,
    pro_opening_node,
    con_opening_node,
    pro_rebuttal_node,
    con_rebuttal_node,
    fact_review_node,
    cross_question_node,
    pro_cross_response_node,
    con_cross_response_node,
    pro_closing_node,
    con_closing_node,
    judge_verdict_node,
)


def build_debate_graph():
    """
    Construct the LangGraph StateGraph for the debate workflow.

    Steps:
      1. Create a StateGraph with the DebateState schema
      2. Register each workflow stage as a named node
      3. Connect nodes with directed edges (linear sequence)
      4. Set the entry point and compile

    Returns:
      A compiled LangGraph graph ready to be streamed or invoked.
    """
    graph = StateGraph(DebateState)

    # ── Register all workflow stage nodes ──
    graph.add_node("setup",               setup_node)
    graph.add_node("moderator_intro",     moderator_intro_node)
    graph.add_node("pro_opening",         pro_opening_node)
    graph.add_node("con_opening",         con_opening_node)
    graph.add_node("pro_rebuttal",        pro_rebuttal_node)
    graph.add_node("con_rebuttal",        con_rebuttal_node)
    graph.add_node("fact_review",         fact_review_node)
    graph.add_node("cross_question",      cross_question_node)
    graph.add_node("pro_cross_response",  pro_cross_response_node)
    graph.add_node("con_cross_response",  con_cross_response_node)
    graph.add_node("pro_closing",         pro_closing_node)
    graph.add_node("con_closing",         con_closing_node)
    graph.add_node("judge_verdict",       judge_verdict_node)

    # ── Set the entry point ──
    graph.set_entry_point("setup")

    # ── Define the linear debate flow (edge by edge) ──
    graph.add_edge("setup",               "moderator_intro")
    graph.add_edge("moderator_intro",     "pro_opening")
    graph.add_edge("pro_opening",         "con_opening")
    graph.add_edge("con_opening",         "pro_rebuttal")
    graph.add_edge("pro_rebuttal",        "con_rebuttal")
    graph.add_edge("con_rebuttal",        "fact_review")
    graph.add_edge("fact_review",         "cross_question")
    graph.add_edge("cross_question",      "pro_cross_response")
    graph.add_edge("pro_cross_response",  "con_cross_response")
    graph.add_edge("con_cross_response",  "pro_closing")
    graph.add_edge("pro_closing",         "con_closing")
    graph.add_edge("con_closing",         "judge_verdict")
    graph.add_edge("judge_verdict",       END)

    return graph.compile()


# ── Module-level compiled graph instance ──
# Imported directly by app.py
debate_graph = build_debate_graph()
