"""
DebateSphere AI - Configuration
Loads environment variables and defines global settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Gemini model to use
GEMINI_MODEL = "gemini-2.5-flash"

# Debate configuration defaults
DEFAULT_ROUNDS = 1
MAX_TOKENS = 300

# Debate Modes
DEBATE_MODES = [
    "Classic Debate",
    "Expert Panel Debate",
    "Boardroom Mode",
    "Ethics Mode",
    "Investor Mode",
]

# Debate Styles
DEBATE_STYLES = [
    "Oxford Style",
    "Courtroom Style",
    "Policy Style",
    "Startup Pitch Battle",
    "Academic Discussion",
]

# Tones
DEBATE_TONES = [
    "Professional",
    "Formal",
    "Conversational",
    "Aggressive",
    "Socratic",
]

# Domains
DEBATE_DOMAINS = [
    "Technology",
    "Business",
    "Education",
    "Ethics",
    "Politics",
    "Healthcare",
    "Environment",
    "Product Management",
    "Finance",
    "Society",
]

# Personas
PRO_PERSONAS = [
    "AI Strategist",
    "Tech Entrepreneur",
    "Economist",
    "Policy Advocate",
    "Innovation Researcher",
    "Growth Hacker",
    "Futurist",
    "Business Consultant",
]

CON_PERSONAS = [
    "Labor Ethics Specialist",
    "Risk Analyst",
    "Environmental Ethicist",
    "Civil Rights Lawyer",
    "Traditional Economist",
    "Consumer Advocate",
    "Privacy Expert",
    "Social Scientist",
]
