from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
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

    result = chain.invoke({"strategy": str(strategy)})

    return parse_and_validate(result.content, ExecutionPlan)