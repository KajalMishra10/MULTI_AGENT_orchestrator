from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
import json


def run_test_manager(srs):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Test Manager.

Create a Test Strategy.

Return JSON:

{{
 "scope": "",
 "test_types": [],
 "environment": "",
 "risks": []
}}

SRS: {srs}
""")

    chain = prompt | llm

    result = chain.invoke({"srs": str(srs)})

    try:
        return json.loads(result.content)
    except:
        return {"raw": result.content}