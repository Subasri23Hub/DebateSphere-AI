"""
DebateSphere AI - UI Styles
Premium CSS for the Streamlit interface.
"""

MAIN_CSS = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

/* ── Root Variables ── */
:root {
    --pro-color: #3b82f6;
    --pro-light: #dbeafe;
    --pro-dark: #1d4ed8;
    --con-color: #ef4444;
    --con-light: #fee2e2;
    --con-dark: #b91c1c;
    --judge-color: #f59e0b;
    --judge-light: #fef3c7;
    --mod-color: #6b7280;
    --mod-light: #f3f4f6;
    --fact-color: #8b5cf6;
    --fact-light: #ede9fe;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --bg-card2: #243044;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --radius: 12px;
    --shadow: 0 4px 24px rgba(0,0,0,0.35);
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1a2540 50%, #0f172a 100%) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer { visibility: hidden; }
/* Do NOT hide header, because sidebar toggle is there */
header {
    visibility: visible !important;
    background: transparent !important;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 40%, #2d1b4e 100%);
    border-radius: var(--radius);
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
}
.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 400;
    letter-spacing: 0.03em;
}
.hero-badges {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.72rem;
    color: var(--text-secondary);
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Section Heading ── */
.section-heading {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* ── Debate Card (generic) ── */
.debate-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    border: 1px solid var(--border);
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    transition: transform 0.15s;
}
.debate-card:hover { transform: translateY(-1px); }

/* ── Speaker Cards ── */
.card-moderator {
    border-left: 4px solid var(--mod-color);
    background: linear-gradient(135deg, #1e293b 0%, #243044 100%);
}
.card-pro {
    border-left: 4px solid var(--pro-color);
    background: linear-gradient(135deg, #1e2d45 0%, #1e293b 100%);
}
.card-con {
    border-left: 4px solid var(--con-color);
    background: linear-gradient(135deg, #2d1e1e 0%, #1e293b 100%);
}
.card-judge {
    border-left: 4px solid var(--judge-color);
    background: linear-gradient(135deg, #2d2310 0%, #1e293b 100%);
}
.card-fact {
    border-left: 4px solid var(--fact-color);
    background: linear-gradient(135deg, #221e2d 0%, #1e293b 100%);
}

.card-speaker-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.label-moderator { color: var(--mod-color); }
.label-pro { color: var(--pro-color); }
.label-con { color: var(--con-color); }
.label-judge { color: var(--judge-color); }
.label-fact { color: var(--fact-color); }

.card-round-tag {
    font-size: 0.6rem;
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 0.15rem 0.5rem;
    color: var(--text-secondary);
    font-weight: 500;
    letter-spacing: 0.07em;
    margin-left: auto;
}

.card-content {
    color: var(--text-primary);
    font-size: 0.92rem;
    line-height: 1.75;
    white-space: pre-wrap;
}

/* ── Score Card ── */
.score-block {
    background: var(--bg-card2);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    border: 1px solid var(--border);
    margin-bottom: 0.75rem;
}
.score-title {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.score-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
}
.score-label { color: var(--text-secondary); font-weight: 500; }
.score-bar-container {
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.08);
    border-radius: 3px;
    margin: 0 0.75rem;
    overflow: hidden;
}
.score-bar {
    height: 100%;
    border-radius: 3px;
    transition: width 0.6s ease;
}
.score-number {
    font-weight: 700;
    font-size: 0.85rem;
    min-width: 32px;
    text-align: right;
}
.score-total-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--border);
    font-size: 0.9rem;
    font-weight: 700;
}

/* ── Winner Banner ── */
.winner-banner {
    text-align: center;
    padding: 1.8rem 1rem;
    border-radius: var(--radius);
    margin: 1rem 0;
    border: 1px solid;
}
.winner-banner.pro {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e2d45 100%);
    border-color: var(--pro-color);
}
.winner-banner.con {
    background: linear-gradient(135deg, #3b1f1f 0%, #2d1e1e 100%);
    border-color: var(--con-color);
}
.winner-banner.draw {
    background: linear-gradient(135deg, #2d2310 0%, #1e293b 100%);
    border-color: var(--judge-color);
}
.winner-label {
    font-size: 2rem;
    margin-bottom: 0.3rem;
}
.winner-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
}
.winner-sub {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* ── Step Progress Bar ── */
.step-progress {
    display: flex;
    gap: 0.3rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.step-dot {
    flex: 1;
    min-width: 30px;
    height: 4px;
    border-radius: 2px;
    background: rgba(255,255,255,0.08);
}
.step-dot.done { background: var(--pro-color); }
.step-dot.active {
    background: var(--judge-color);
    box-shadow: 0 0 8px var(--judge-color);
    animation: pulse 1.2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #121e32 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stTextArea label {
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}

/* ── Streamlit inputs dark override ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #1e293b !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}

/* ── Q&A ── */
.qa-block {
    background: var(--bg-card);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    border: 1px solid var(--border);
    margin-bottom: 0.75rem;
}
.qa-question {
    font-size: 0.82rem;
    color: var(--text-secondary);
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.qa-answer {
    font-size: 0.9rem;
    color: var(--text-primary);
    line-height: 1.65;
    white-space: pre-wrap;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Verdict Highlights ── */
.verdict-highlight {
    background: var(--bg-card2);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    border: 1px solid var(--border);
    font-size: 0.88rem;
    color: var(--text-primary);
    line-height: 1.6;
}
.verdict-highlight-title {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.35rem;
}

/* ── Status pill ── */
.status-pill {
    display: inline-block;
    border-radius: 12px;
    padding: 0.2rem 0.7rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}
.status-running { background: rgba(245,158,11,0.15); color: var(--judge-color); border: 1px solid var(--judge-color); }
.status-done { background: rgba(34,197,94,0.12); color: #22c55e; border: 1px solid #22c55e; }
</style>
"""
