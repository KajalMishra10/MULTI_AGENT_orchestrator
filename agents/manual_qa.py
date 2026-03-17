from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
from utils.parse_and_validate import parse_and_validate
from models.schemas import ManualTests


def run_manual_qa(plan):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Manual QA Engineer.

Generate manual test cases.

Return ONLY valid JSON (no extra text):

{{
 "manual_tests": [
   {{
     "test_id": "",
     "title": "",
     "steps": [],
     "expected_result": ""
   }}
 ]
}}

Plan: {plan}
""")

    chain = prompt | llm

    result = chain.invoke({"plan": str(plan)})

    return parse_and_validate(result.content, ManualTests)