from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm, call_llm_with_retry
from utils.parse_and_validate import parse_and_validate
from models.schemas import SRS


def run_pm_agent(requirement, feedback=""):

    llm = get_llm()

    feedback_block = ""
    if feedback:
        feedback_block = f"""

## Previous Review Feedback (MUST address these issues):
{feedback}
"""

    prompt = PromptTemplate.from_template("""
You are a Product Manager.

Create an SRS.
{feedback_block}
Return ONLY valid JSON (no extra text):

{{
 "product_overview": "",
 "target_users": [],
 "features": []
}}

Idea: {idea}
""")

    chain = prompt | llm

    content = call_llm_with_retry(chain, {
        "idea": requirement,
        "feedback_block": feedback_block,
    })

    return parse_and_validate(content, SRS)
