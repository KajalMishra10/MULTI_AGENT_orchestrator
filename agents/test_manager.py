from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
from utils.parse_and_validate import parse_and_validate
from models.schemas import TestStrategy


def run_test_manager(srs):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Test Manager.

Create a Test Strategy.

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

    result = chain.invoke({"srs": str(srs)})

    return parse_and_validate(result.content, TestStrategy)