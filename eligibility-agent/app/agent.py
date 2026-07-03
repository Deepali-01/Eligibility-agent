# ruff: noqa
import logging

from pydantic import BaseModel
from google.adk.agents.context import Context
from google.adk.apps import App
from google import genai
from google.adk.workflow import START, Workflow, node
from google.genai import types

from app.schema import EligibilityState

logger = logging.getLogger(__name__)


class EligibilityExtraction(BaseModel):
    is_eligible: bool
    reasoning: str
    deadline: str
    deadline_status: str  # "passed", "urgent", "time_left"


@node
async def evaluate_node(ctx: Context, node_input: str) -> str:
    """Takes ONE combined message containing both the student profile and the
    opportunity description, and evaluates eligibility in a single pass."""
    state = ctx.state
    state.combined_input = node_input.strip()

    client = genai.Client(api_key=__import__("os").environ["GEMINI_API_KEY"], vertexai=False)

    prompt = f"""
    You are an Opportunity Eligibility Assistant.

    The user has provided their student profile AND an opportunity description
    together in one message below. Identify which parts are the profile and
    which are the opportunity, then determine if the student is eligible.

    TODAY'S DATE: 2026-07-03

    USER MESSAGE:
    {state.combined_input}

    Extract the application deadline from the text.
    Classify the deadline status as one of: "passed", "urgent" (within 3 days), or "time_left".
    If no deadline is found, use "time_left".
    """

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_schema=EligibilityExtraction,
                response_mime_type="application/json",
            )
        )
        parsed = response.parsed

        state.is_eligible = getattr(parsed, "is_eligible", False)
        state.reasoning = getattr(parsed, "reasoning", "")
        state.deadline = getattr(parsed, "deadline", "")
        state.deadline_status = getattr(parsed, "deadline_status", "")
    except Exception as e:
        logger.error(f"Error calling model: {e}")
        state.is_eligible = False
        state.reasoning = "Failed to evaluate eligibility."
        state.deadline_status = "passed"

    is_eligible = getattr(state, "is_eligible", False)
    deadline_status = getattr(state, "deadline_status", "")

    if is_eligible and deadline_status != "passed":
        return "recommend"
    else:
        return "reject"


@node
async def recommend_node(ctx: Context) -> None:
    state = ctx.state
    deadline = getattr(state, "deadline", "")
    deadline_status = getattr(state, "deadline_status", "")
    reasoning = getattr(state, "reasoning", "")

    print(f"\n RECOMMENDED: You are eligible! Deadline: {deadline} ({deadline_status})")
    print(f"Reasoning: {reasoning}\n")


@node
async def reject_node(ctx: Context) -> None:
    state = ctx.state
    deadline_status = getattr(state, "deadline_status", "")
    reasoning = getattr(state, "reasoning", "")

    print(f"\n REJECTED: Not a match or expired. Deadline status: {deadline_status}")
    print(f"Reasoning: {reasoning}\n")


workflow = Workflow(
    name="eligibility_workflow",
    state_schema=EligibilityState,
    edges=[
        (START, evaluate_node),
        (evaluate_node, {
            "recommend": recommend_node,
            "reject": reject_node,
        }),
    ],
)

app = App(
    root_agent=workflow,
    name="app",
)
