# ⚖️ DebateSphere AI

> A structured AI debate simulator built with **LangGraph**, **Gemini API**, and **Streamlit**.
> A single LLM is invoked across multiple workflow stages to simulate moderator, PRO, CON, fact-check, and judge roles.

---

## 🚀 What is DebateSphere AI?

DebateSphere AI is a **structured LangGraph workflow** that simulates a full professional debate. It uses a single Gemini model called sequentially across 13 workflow stages — each stage sends a different role-specific prompt (moderator, PRO debater, CON debater, fact-check reviewer, judge) and writes the output into a shared state.

There are **no agent frameworks, no multi-agent orchestration, and no tool-calling agents**. The system is built entirely with basic LangGraph concepts: a `StateGraph`, plain Python node functions, and linear edges.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔗 LangGraph Workflow | 13 sequential nodes with linear edges |
| ✨ Single Gemini Model | One LLM called with different role prompts at each stage |
| 🏆 Judge & Scoring Stage | 5-dimension scoring with radar chart visualization |
| 🟣 Fact-Check Stage | Claim classification: factual, opinion, assumption, prediction, weak |
| 💬 Audience Q&A | Post-debate follow-up Gemini calls |
| 📥 Transcript Export | Download the full debate as a .txt file |
| 🎨 Premium Dark UI | Custom CSS Streamlit interface |
| 🗂️ Sample Topics | Browse suggested topics by domain |

---

## 🏗️ How the Workflow Works

```
START
  ↓  setup             — initialise state
  ↓  moderator_intro   — Gemini prompted as neutral moderator
  ↓  pro_opening       — Gemini prompted as PRO debater
  ↓  con_opening       — Gemini prompted as CON debater
  ↓  pro_rebuttal      — Gemini prompted as PRO debater (rebuttal)
  ↓  con_rebuttal      — Gemini prompted as CON debater (rebuttal)
  ↓  fact_review       — Gemini prompted as claim reviewer
  ↓  cross_question    — Gemini prompted as moderator (cross-exam Q)
  ↓  pro_cross_response— Gemini prompted as PRO debater (answer)
  ↓  con_cross_response— Gemini prompted as CON debater (answer)
  ↓  pro_closing       — Gemini prompted as PRO debater (closing)
  ↓  con_closing       — Gemini prompted as CON debater (closing)
  ↓  judge_verdict     — Gemini prompted as impartial judge
END
  → Audience Q&A       — standalone Gemini call (not in graph)
```

**Key concept:** The same LLM produces completely different outputs at each stage because each node sends a different prompt. Role simulation is achieved through prompt engineering, not through agent frameworks.

---

## 📁 Project Structure

```
DebateSphereAI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── .env                    # API key (add yours here)
├── README.md
│
├── src/
│   ├── config.py           # Settings, modes, personas, styles
│   ├── state.py            # LangGraph TypedDict state schema
│   ├── graph.py            # LangGraph StateGraph builder
│   ├── nodes.py            # All 13 workflow node functions + Q&A
│   ├── prompts.py          # All role-specific prompt templates
│   ├── scoring.py          # Score parsing and chart helpers
│   ├── formatter.py        — Output extraction helpers
│   └── utils.py            # Transcript export and utilities
│
├── ui/
│   ├── styles.py           # Premium CSS theme
│   ├── components.py       # Reusable Streamlit UI components
│   └── layout.py           # Page layout helpers
│
├── data/
│   └── sample_topics.json  # Suggested debate topics by domain
│
└── exports/
    └── transcripts/        # Saved debate transcripts
```

---

## ⚙️ Setup & Installation

### 1. Navigate to the project folder

```bash
cd D:\Sourcesys\DebateSphereAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Google API key

Open `.env` and replace the placeholder:

```
GOOGLE_API_KEY=your_actual_google_api_key_here
```

Get a free key at: https://aistudio.google.com/app/apikey

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🎯 Usage

1. **Configure** in the sidebar: enter a topic, choose mode/style/tone/domain and personas
2. **Click "🚀 Start Debate"** — the 13-stage LangGraph workflow executes
3. **View results** across 5 tabs:
   - 🏟️ Debate Arena — all stages displayed side by side
   - 🏆 Verdict & Scores — winner, radar chart, verdict analysis
   - 🟣 Fact-Check — claim classification per side
   - 💬 Audience Q&A — post-debate interactive questions
   - 📜 Full Transcript — complete log with download

---

## 🗣️ How to Explain This to Faculty

> "This project uses LangGraph to build a structured 13-stage debate workflow.
> There is one `StateGraph` with one `DebateState` TypedDict.
> Each stage is a plain Python function (node) that calls the Gemini model
> with a role-specific prompt — for example, the `moderator_intro` node sends
> a moderator prompt, the `pro_opening` node sends a PRO debater prompt, and
> the `judge_verdict` node sends a judge prompt.
> All 13 nodes are connected with linear edges: `setup → moderator_intro → pro_opening → ... → judge_verdict → END`.
> The workflow is executed using `graph.stream()` in Streamlit so results appear
> progressively. No agent frameworks are used — role simulation is done through
> prompt engineering."

---

## 🛠️ Tech Stack

- **Python** — core language
- **LangGraph** — `StateGraph` workflow orchestration
- **Gemini 1.5 Flash** — LLM for all workflow stages
- **LangChain Google GenAI** — Gemini Python integration
- **Streamlit** — interactive web interface
- **Plotly** — radar chart score visualisation
- **python-dotenv** — environment variable management

---

## 📝 Resume Description

> Built **DebateSphere AI**, a structured AI debate simulator using LangGraph, Gemini API, and Streamlit — featuring a 13-stage sequential workflow where a single LLM is invoked with role-specific prompts (moderator, PRO, CON, fact-check reviewer, judge), structured scoring, claim analysis, and interactive verdict generation through a premium Streamlit dashboard.

---

## 🔮 Future Enhancements

- Real-time streaming of Gemini responses
- PDF transcript export
- Debate history and session storage
- Voice-based debate mode
- Web-grounded fact checking
- Score trend charts across multiple debates
- Topic recommendation engine

---

*Built with ❤️ using LangGraph + Gemini + Streamlit*
