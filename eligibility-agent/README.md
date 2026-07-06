# 🎓 Opportunity Eligibility Agent

> An AI agent that tells students instantly whether they qualify for an opportunity — and whether they've already missed the deadline.

Built for Google & Kaggle's **AI Agents: Intensive Vibe Coding Capstone Project** (Freestyle Track), using Google's Agent Development Kit (ADK) and Antigravity IDE.

---

## 📌 The Problem

As a student, I constantly come across internships, hackathons, and scholarships — but figuring out whether I'm actually eligible takes real time. Many listings are written for B.Tech/B.E. students only, and that detail is often buried deep in the fine print. I've personally lost time reading through eligibility criteria for opportunities I didn't even qualify for, and missed deadlines simply because I spent too long on the reading part.

**This agent solves that.** Paste your profile and an opportunity's description together, and it tells you — instantly and with reasoning — whether you qualify, and whether the deadline has already passed.

---

## 🤖 Why an Agent (not just a script)?

A simple keyword-matching script can't handle this problem, because eligibility criteria are written in free-form natural language — "open to engineering students," "B.Tech/B.E. only," "any UG stream welcome" all mean different things and need real reasoning to interpret correctly. This agent uses an LLM to *read and judge* the match between a profile and criteria, and to extract and reason about deadlines from unstructured text — not fixed pattern matching.

---

## 🏗️ Architecture

```
START → evaluate_node → ┬─ recommend_node (eligible + deadline valid)
                         └─ reject_node   (ineligible OR deadline passed OR failed security check)
```

**Flow:**
1. **Input arrives** — one message containing both the student's profile and the opportunity's description.
2. **Security validation** (inside `evaluate_node`, before any model call) — rejects inputs over 5,000 characters, and scans for prompt-injection phrases like "ignore previous instructions," blocking them without ever reaching the LLM.
3. **Structured evaluation** — a Gemini 2.5 Flash call returns a strict JSON schema:

```python
class EligibilityExtraction(BaseModel):
    is_eligible: bool
    reasoning: str
    deadline: str
    deadline_status: str  # "passed", "urgent", "time_left"
```

4. **Routing** — based on the result, goes to `recommend_node` (eligible message) or `reject_node` (rejection message).

State is managed via ADK's `EligibilityState` schema. Profile data lives only in in-memory session state — never logged, never written to disk.

---

## ✅ Concepts Demonstrated

| Concept | Where |
|---|---|
| Multi-node agent workflow (ADK) | `app/agent.py` — conditional routing via `Workflow` edges |
| Structured LLM output | `EligibilityExtraction` schema forces machine-actionable JSON |
| Security features | Input length limits + prompt-injection detection before any model call |
| Antigravity | Entire agent built and debugged using Antigravity IDE's natural-language prompting |

---

## 🎥 Demo Examples

**Eligible case:** BCA student + "CodeForGood Hackathon, open to all UG students" → Output: `recommend`

**Ineligible case:** BCA student + "TechCorp Internship, B.Tech/B.E. only" → Output: `reject`

---

## 📁 Project Structure

```
eligibility-agent/
├── app/                        # Core agent code
│   ├── agent.py                # Main agent logic (workflow, nodes, security validation)
│   ├── schema.py                # EligibilityState schema definition
│   ├── fast_api_app.py          # FastAPI backend server
│   └── app_utils/               # App utilities and helpers
├── tests/                      # Unit, integration, and load tests
├── GEMINI.md                    # AI-assisted development guide
└── pyproject.toml               # Project dependencies
```

---

## 🚀 Running Locally

**Requirements:**
- **uv**: Python package manager — [Install](https://docs.astral.sh/uv/getting-started/installation/)
- **agents-cli**: Install with `uv tool install google-agents-cli`
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

**Setup:**
```bash
git clone https://github.com/Deepali-01/Eligibility-agent.git
cd Eligibility-agent/eligibility-agent
uvx google-agents-cli setup
agents-cli install
```

Create a `.env` file (copy from `.env.example`) and add your key:
```
GEMINI_API_KEY=your-actual-key-here
```

**Test the agent:**
```bash
agents-cli playground
```

---

## 🛠️ Commands

| Command | Description |
|---|---|
| `agents-cli install` | Install dependencies using uv |
| `agents-cli playground` | Launch local development environment |
| `agents-cli lint` | Run code quality checks |
| `agents-cli eval` | Evaluate agent behavior |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests |

### Project Management

| Command | What It Does |
|---|---|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## ⚠️ Known Limitation

Deadline classification between "urgent" (within 3 days) and "time_left" isn't always precisely date-calculated by the model — a refinement opportunity for future iterations. Core eligibility judgment and expired-deadline detection are accurate and tested.

---

## 🙋 About

Built by Deepali Sharma, BCA student, as part of Google & Kaggle's 5-Day AI Agents Intensive Vibe Coding Course capstone (Freestyle Track).