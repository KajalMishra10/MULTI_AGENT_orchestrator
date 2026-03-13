from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
import json


def run_automation_qa(plan):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are an Automation QA Engineer.

Generate Selenium automation scripts.

Return JSON:

{{
 "automation_scripts": []
}}

Plan: {plan}
""")

    chain = prompt | llm

    result = chain.invoke({"plan": str(plan)})

    try:
        return json.loads(result.content)
    except:
        return {"raw": result.content}