# Project: Opportunity Eligibility Agent

## Purpose
A multi-agent ADK workflow that helps a student determine if they are eligible for an opportunity (internship, hackathon, scholarship) and whether its deadline has passed. This is a Kaggle capstone submission for Google's "AI Agents: Intensive Vibe Coding" course, Freestyle track.

## Required behavior (do not skip any step)

1. **gather_node**: Conversational node. First asks the user for their student profile, saves it to `state.student_profile`. Then asks for the opportunity description, saves it to `state.opportunity_text`. Only proceeds to evaluation once BOTH are present. Must not loop or re-ask if a value is already correctly saved to state.

2. **evaluate_node**: Uses a Gemini model call with a structured JSON response schema (fields: `is_eligible: bool`, `reasoning: str`, `deadline: str`, `deadline_status: "passed"|"urgent"|"time_left"`). Compares `state.student_profile` against `state.opportunity_text`. Saves results to state. Routes to "recommend" if eligible and not passed, otherwise "reject".

3. **recommend_node** and **reject_node**: Print a clear final message to the user summarizing the verdict, reasoning, and deadline status.

4. **Security requirement**: The student's profile data must stay in-memory only (in `state`), never written to disk, never logged via `print` or `logger`, and never sent to any external URL/tool other than the Gemini model call itself for evaluation.

## Technical requirements
- Use `google.adk.workflow` with `START`, `Workflow`, `@node` exactly as ADK 2.0 expects.
- `app/schema.py` must define `EligibilityState` with fields: `student_profile: str = ""`, `opportunity_text: str = ""`, `is_eligible: bool = False`, `reasoning: str = ""`, `deadline: str = ""`, `deadline_status: str = ""`.
- `app/agent.py` must define `workflow` and export `app = App(root_agent=workflow, name="app")`. Do NOT include unrelated example code (no weather/time tools, no duplicate agent definitions).
- No syntax errors — the file must load cleanly under `agents-cli playground`.

## What NOT to do
- Do not add MCP servers or custom Agent Skills — out of scope for this pass.
- Do not modify files outside `app/agent.py` and `app/schema.py` unless strictly necessary to fix an import error.
- Do not leave any dead/unreachable code, duplicate function definitions, or duplicate keyword arguments.

## Task
Rewrite `app/agent.py` and `app/schema.py` from scratch according to the spec above, replacing all existing content. Verify the file has no syntax errors before finishing.