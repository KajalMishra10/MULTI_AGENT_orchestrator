from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm, call_llm_with_retry
from utils.parse_and_validate import parse_and_validate
from models.schemas import TestStrategy


def run_test_manager(srs, feedback=""):

    llm = get_llm()

    feedback_block = ""
    if feedback:
        feedback_block = f"""

## Previous Review Feedback (MUST address these issues):
{feedback}
"""

    prompt = PromptTemplate.from_template("""
You are a Test Manager.

Create a Test Strategy.
{feedback_block}
Return ONLY valid JSON (no extra text):

{{
 "scope": "",
 "test_types": [],
 "environment": "",
 "risks": []
}}

SRS: {srs}
""")

    chain = prompt | llm

    content = call_llm_with_retry(chain, {
        "srs": str(srs),
        "feedback_block": feedback_block,
    })

    return parse_and_validate(content, TestStrategy)
