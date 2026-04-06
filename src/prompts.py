# src/prompts.py
# DebateSphere AI - Token-Optimized Prompt Templates

MODERATOR_PROMPT = """
You are a neutral debate moderator.

Motion: "{motion}"
Style: {style}
Tone: {tone}
Domain: {domain}
Pro persona: {pro_persona}
Con persona: {con_persona}

Write a crisp introduction to the debate.
- Introduce the motion clearly
- Mention both sides neutrally
- Keep it professional and engaging

Maximum 80 words.
"""

PRO_OPENING_PROMPT = """
You are debating in favor of the motion as a {pro_persona}.

Motion: "{motion}"
Style: {style}
Tone: {tone}
Domain: {domain}

Write:
1. A clear supporting position
2. Exactly 2 strong arguments
3. A short conclusion

Maximum 100 words.
"""

CON_OPENING_PROMPT = """
You are debating against the motion as a {con_persona}.

Motion: "{motion}"
Style: {style}
Tone: {tone}
Domain: {domain}

Write:
1. A clear opposing position
2. Exactly 2 strong counterarguments
3. A short conclusion

Maximum 100 words.
"""

PRO_REBUTTAL_PROMPT = """
You are arguing for the motion as a {pro_persona}.

Motion: "{motion}"
Opponent's opening:
{con_opening}

Write a concise rebuttal:
- Counter the 2 weakest opposing points
- Reinforce your strongest point

Maximum 80 words.
"""

CON_REBUTTAL_PROMPT = """
You are arguing against the motion as a {con_persona}.

Motion: "{motion}"
Opponent's opening:
{pro_opening}

Write a concise rebuttal:
- Counter the 2 weakest supporting points
- Reinforce your strongest counterpoint

Maximum 80 words.
"""

FACT_CHECK_PROMPT = """
You are a claim reviewer.

Motion: "{motion}"

PRO:
{pro_opening}

CON:
{con_opening}

Identify:
- 1 strong claim from PRO
- 1 strong claim from CON
- 1 weak or unsupported claim (from either side)

Keep it short and clear.

Maximum 80 words.
"""

CROSS_QUESTION_PROMPT = """
You are a neutral debate moderator.

Motion: "{motion}"

PRO side:
{pro_opening}

CON side:
{con_opening}

Generate exactly one short, neutral cross-question that challenges both sides fairly.

Maximum 30 words.
"""

PRO_CROSS_RESPONSE_PROMPT = """
You are speaking for the PRO side.

Motion: "{motion}"
Question: "{cross_question}"

Answer briefly in support of the motion.

Maximum 60 words.
"""

CON_CROSS_RESPONSE_PROMPT = """
You are speaking for the CON side.

Motion: "{motion}"
Question: "{cross_question}"

Answer briefly against the motion.

Maximum 60 words.
"""

PRO_CLOSING_PROMPT = """
You are giving the PRO closing statement.

Motion: "{motion}"

Summarize the strongest 2 PRO points and end confidently.

Maximum 60 words.
"""

CON_CLOSING_PROMPT = """
You are giving the CON closing statement.

Motion: "{motion}"

Summarize the strongest 2 CON points and end confidently.

Maximum 60 words.
"""

AUDIENCE_QA_PROMPT = """
You are answering a follow-up debate question.

Motion: "{motion}"
Target role: {target}
Question: "{question}"

PRO opening: {pro_opening}
CON opening: {con_opening}
Winner: {winner}

Respond from the perspective of {target}.
Keep it brief and relevant.

Maximum 80 words.
"""

JUDGE_SCORING_PROMPT = """
You are a neutral debate judge.

Motion: "{motion}"

PRO side:
{pro_opening}
{pro_rebuttal}

CON side:
{con_opening}
{con_rebuttal}

Evaluate both sides briefly.

Give:
- PRO score out of 10 for Logic, Clarity, Persuasiveness
- CON score out of 10 for Logic, Clarity, Persuasiveness
- Winner
- Strongest point overall
- Balanced takeaway

Maximum 180 words.
"""