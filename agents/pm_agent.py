from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm
from utils.parse_and_validate import parse_and_validate
from models.schemas import SRS


def run_pm_agent(requirement):

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Product Manager.

Create an SRS.

Return ONLY valid JSON (no extra text):

{{
 "product_overview": "",
 "target_users": [],
 "features": []
}}

Idea: {idea}
""")

    chain = prompt | llm

    result = chain.invoke({"idea": requirement})

    return parse_and_validate(result.content, SRS)