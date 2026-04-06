"""
DebateSphere AI
---------------
This file is intentionally left as a compatibility stub.

The project was refactored to remove all agent-based terminology.
All workflow node functions now live in:

    src/nodes.py

Please import from src.nodes instead of src.agents.
"""

# Re-export everything from nodes.py so any stale import still works
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
    answer_audience_question,
)
