"""
DebateSphere AI - Formatter
Converts raw agent outputs into clean, UI-ready structured text.
"""

import re
from typing import Dict, Any


def extract_section(text: str, header: str) -> str:
    """Extract a specific section from markdown-formatted text."""
    pattern = rf"\*\*{re.escape(header)}\*\*(.*?)(?=\*\*[A-Z]|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def format_speaker_label(speaker: str) -> str:
    labels = {
        "Pro": "🔵 PRO",
        "Con": "🔴 CON",
        "Moderator": "⚪ MODERATOR",
        "Judge": "🟡 JUDGE",
        "Fact-Check Analyst": "🟣 FACT-CHECK",
    }
    return labels.get(speaker, f"🎤 {speaker.upper()}")


def format_round_label(round_name: str) -> str:
    labels = {
        "intro": "Opening Introduction",
        "opening": "Opening Statement",
        "rebuttal": "Rebuttal",
        "fact_review": "Fact-Check Analysis",
        "cross_question": "Cross-Examination Question",
        "cross_response": "Cross-Examination Response",
        "closing": "Closing Statement",
        "final_verdict": "Final Verdict",
    }
    return labels.get(round_name, round_name.replace("_", " ").title())


def extract_winner_line(verdict_text: str) -> str:
    """Pull out the WINNER line from judge verdict."""
    for line in verdict_text.split("\n"):
        if "WINNER:" in line.upper():
            return line.strip().replace("**", "")
    return "WINNER: DRAW"


def extract_balanced_takeaway(verdict_text: str) -> str:
    """Extract the balanced takeaway from the judge's verdict."""
    return extract_section(verdict_text, "Balanced Takeaway:")


def extract_strongest_argument(verdict_text: str) -> str:
    return extract_section(verdict_text, "Strongest Argument Overall:")


def extract_weakest_points(verdict_text: str) -> Dict[str, str]:
    return {
        "pro": extract_section(verdict_text, "Weakest Point — PRO:"),
        "con": extract_section(verdict_text, "Weakest Point — CON:"),
    }


def extract_logical_issues(verdict_text: str) -> str:
    return extract_section(verdict_text, "Logical Issues Detected:")
