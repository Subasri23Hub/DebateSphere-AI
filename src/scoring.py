"""
DebateSphere AI - Scoring Utilities
Parses and structures judge scores for display.
"""

import re
from typing import Dict, Any


SCORE_DIMENSIONS = [
    "Logic & Reasoning",
    "Clarity & Structure",
    "Evidence Quality",
    "Persuasiveness",
    "Rebuttal Strength",
]


def parse_scores_from_verdict(verdict_text: str) -> Dict[str, Any]:
    """
    Parse score values from the judge's verdict text.
    Returns a dict with 'pro', 'con', and 'totals'.
    """
    scores = {
        "pro": {},
        "con": {},
        "pro_total": 0,
        "con_total": 0,
    }

    lines = verdict_text.split("\n")
    current_side = None

    for line in lines:
        line = line.strip()

        if "PRO:" in line and "WINNER" not in line.upper():
            current_side = "pro"
        elif "CON:" in line and "WINNER" not in line.upper():
            current_side = "con"

        if current_side and "Total:" in line:
            match = re.search(r"(\d+)/50", line)
            if match:
                scores[f"{current_side}_total"] = int(match.group(1))

        for dim in SCORE_DIMENSIONS:
            if dim in line and current_side:
                match = re.search(r"(\d+)/10", line)
                if match:
                    scores[current_side][dim] = int(match.group(1))

    return scores


def get_score_color(score: int) -> str:
    """Return a color hex based on score value."""
    if score >= 8:
        return "#22c55e"   # green
    elif score >= 6:
        return "#f59e0b"   # amber
    else:
        return "#ef4444"   # red


def format_winner_badge(winner: str) -> str:
    if winner == "PRO":
        return "🏆 PRO wins the debate!"
    elif winner == "CON":
        return "🏆 CON wins the debate!"
    else:
        return "🤝 The debate ends in a DRAW."
