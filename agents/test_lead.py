from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm, call_llm_with_retry
from utils.parse_and_validate import parse_and_validate
from models.schemas import ExecutionPlan


def run_test_lead(strategy):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Test Lead.

Generate System Test Execution Plan.

Return ONLY valid JSON (no extra text):

{{
 "test_phases": [],
 "timeline": "",
 "resources": []
}}

Strategy: {strategy}
""")

    chain = prompt | llm

    content = call_llm_with_retry(chain, {"strategy": str(strategy)})

    return parse_and_validate(content, ExecutionPlan)
