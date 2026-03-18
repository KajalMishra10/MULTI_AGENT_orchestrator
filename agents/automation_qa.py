from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm, call_llm_with_retry
from utils.parse_and_validate import parse_and_validate
from models.schemas import AutomationTests


def run_automation_qa(plan):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are an Automation QA Engineer.

Generate Selenium automation scripts.

Return ONLY valid JSON (no extra text):

{{
 "automation_scripts": [
   {{
     "script_id": "",
     "title": "",
     "code": ""
   }}
 ]
}}

Plan: {plan}
""")

    chain = prompt | llm

    content = call_llm_with_retry(chain, {"plan": str(plan)})

    return parse_and_validate(content, AutomationTests)