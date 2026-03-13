from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
import json


def run_test_lead(strategy):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Test Lead.

Generate System Test Execution Plan.

Return JSON:

{{
 "test_phases": [],
 "timeline": "",
 "resources": []
}}

Strategy: {strategy}
""")

    chain = prompt | llm

    result = chain.invoke({"strategy": str(strategy)})

    try:
        return json.loads(result.content)
    except:
        return {"raw": result.content}