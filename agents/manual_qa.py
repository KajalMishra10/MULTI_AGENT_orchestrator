from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
import json


def run_manual_qa(plan):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Manual QA Engineer.

Generate manual test cases.

Return JSON:

{{
 "manual_tests": []
}}

Plan: {plan}
""")

    chain = prompt | llm

    result = chain.invoke({"plan": str(plan)})

    try:
        return json.loads(result.content)
    except:
        return {"raw": result.content}
    