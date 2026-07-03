from pydantic import BaseModel, Field


class EligibilityState(BaseModel):
    combined_input: str = Field(default="")
    student_profile: str = Field(default="")
    opportunity_text: str = Field(default="")
    is_eligible: bool = Field(default=False)
    reasoning: str = Field(default="")
    deadline: str = Field(default="")
    deadline_status: str = Field(default="")