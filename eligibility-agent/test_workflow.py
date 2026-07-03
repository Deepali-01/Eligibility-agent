import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.agent import workflow
from app.schema import EligibilityState

async def run_workflow():
    student = "Computer Science Junior at Stanford, fluent in Python and AI, 3.8 GPA."
    
    # Test case 1: Eligible, future deadline
    print("--- Test Case 1: Eligible, time_left ---")
    opportunity1 = "Google Software Engineering Intern. Must be pursuing CS degree. Deadline: August 2027."
    state1 = EligibilityState(student_profile=student, opportunity_text=opportunity1)
    
    try:
        res = await workflow.run(node_input=state1)
        print(f"Workflow finished successfully.")
        
    except Exception as e:
        print(f"Error running workflow: {e}")

if __name__ == "__main__":
    asyncio.run(run_workflow())
