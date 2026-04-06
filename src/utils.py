"""
DebateSphere AI - Utilities
Helper functions for transcript management, export, and text processing.
"""

import json
import re
import uuid
from datetime import datetime
from typing import List, Dict


def generate_debate_id() -> str:
    return str(uuid.uuid4())[:8].upper()


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_markdown(text: str) -> str:
    """Strip markdown bold/italic markers for plain text export."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    return text.strip()


def transcript_to_text(transcript: List[Dict[str, str]]) -> str:
    """Convert transcript list to formatted plain text."""
    lines = ["=" * 60, "DEBATESPHERE AI — DEBATE TRANSCRIPT", "=" * 60, ""]
    for entry in transcript:
        speaker = entry.get("speaker", "Unknown")
        round_name = entry.get("round", "").upper().replace("_", " ")
        content = clean_markdown(entry.get("content", ""))
        lines.append(f"[{round_name}] — {speaker}")
        lines.append("-" * 40)
        lines.append(content)
        lines.append("")
    return "\n".join(lines)


def save_transcript(transcript: List[Dict[str, str]], debate_id: str, folder: str = "exports/transcripts") -> str:
    """Save transcript to a .txt file and return the file path."""
    import os
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/debate_{debate_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript_to_text(transcript))
    return filename


def load_sample_topics(path: str = "data/sample_topics.json") -> Dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}
