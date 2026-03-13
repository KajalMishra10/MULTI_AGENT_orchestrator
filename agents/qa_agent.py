from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
import json


def run_qa_agent(plan):

    llm = get_llm()

    prompt = PromptTemplate(
        input_variables=["plan"],
        template="""
You are a QA Engineer.

Generate:

1. Manual Test Cases
2. Selenium Automation Scripts

Return JSON:

{{
 "manual_tests": [],
 "automation_scripts": []
}}

Execution Plan:
{plan}
"""
    )

    chain = prompt | llm

    result = chain.invoke({"plan": str(plan)})

    try:
        data = json.loads(result.content)
    except:
        data = {"raw_output": result.content}

    return data