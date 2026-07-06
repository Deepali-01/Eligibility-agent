🎓 Opportunity Eligibility Agent

An AI agent that tells students instantly whether they qualify for an opportunity — and whether they've already missed the deadline.

Built for Google & Kaggle's AI Agents: Intensive Vibe Coding Capstone Project (Freestyle Track), using Google's Agent Development Kit (ADK) and Antigravity IDE.
📌 The Problem
As a student, I constantly come across internships, hackathons, and scholarships — but figuring out whether I'm actually eligible takes real time. Many listings are written for B.Tech/B.E. students only, and that detail is often buried deep in the fine print. This agent solves that — paste your profile and an opportunity's description together, and it tells you instantly, with reasoning, whether you qualify and whether the deadline has passed.
🤖 Why an Agent (not just a script)?
Eligibility criteria are written in free-form natural language, needing real reasoning to interpret correctly — not fixed keyword matching. This agent uses an LLM to read and judge the match, and to reason about deadlines from unstructured text.
🏗️ Architecture
START → evaluate_node → recommend_node (eligible + deadline valid) OR reject_node (ineligible OR deadline passed OR failed security check)
Flow: input arrives as one combined message → security validation (length + prompt-injection check) before any model call → structured Gemini evaluation returning JSON (is_eligible, reasoning, deadline, deadline_status) → routing to recommend or reject.
State is managed via ADK's EligibilityState schema. Profile data lives only in in-memory session state — never logged, never written to disk.
✅ Concepts Demonstrated

Multi-node agent workflow (ADK) — conditional routing via Workflow edges in app/agent.py
Structured LLM output — EligibilityExtraction schema forces machine-actionable JSON
Security features — input length limits + prompt-injection detection before any model call
Antigravity — entire agent built and debugged using Antigravity IDE's natural-language prompting

🎥 Demo Examples
Eligible case: BCA student + "CodeForGood Hackathon, open to all UG students" → recommend
Ineligible case: BCA student + "TechCorp Internship, B.Tech/B.E. only" → reject
📁 Project Structure
eligibility-agent/
├── app/
│   ├── agent.py
│   ├── schema.py
│   ├── fast_api_app.py
│   └── app_utils/
├── tests/
├── GEMINI.md
└── pyproject.toml
🚀 Running Locally
Requirements: uv, agents-cli (uv tool install google-agents-cli), a Gemini API key from Google AI Studio.
bashgit clone https://github.com/Deepali-01/Eligibility-agent.git
cd Eligibility-agent/eligibility-agent
uvx google-agents-cli setup
agents-cli install
Add your key to a local .env file, then:
bashagents-cli playground
🛠️ Commands
CommandDescriptionagents-cli installInstall dependenciesagents-cli playgroundLaunch local dev environmentagents-cli lintRun code quality checksagents-cli evalEvaluate agent behavioruv run pytest tests/unit tests/integrationRun tests
⚠️ Known Limitation
Deadline "urgent" vs "time_left" classification isn't always precisely date-calculated — a refinement opportunity for future iterations.
🙋 About
Built by Deepali Sharma, BCA student, as part of Google & Kaggle's capstone (Freestyle Track).