import json
from langchain_core.prompts import PromptTemplate
from agents.llm_client import get_llm, call_llm_with_retry
from utils.parse_and_validate import parse_and_validate
from models.schemas import ReviewResult


def run_reviewer(agent_name: str, output: dict, criteria: str) -> dict:
    """Review an agent's output and decide if it needs revision.

    Returns: {"approved": bool, "score": int, "feedback": str}
    """

    llm = get_llm()

    prompt = PromptTemplate.from_template("""
You are a Senior QA Reviewer.

Review the output of the "{agent_name}" agent.

## Review Criteria
{criteria}

## Output to Review
{output}

## Instructions
- Score from 1-10 (1=terrible, 10=perfect)
- If score >= 7, set approved to true
- If score < 7, set approved to false and give specific feedback on what to improve

Return ONLY valid JSON (no extra text):

{{
  "approved": true,
  "score": 8,
  "feedback": "specific feedback here"
}}
""")

    chain = prompt | llm

    content = call_llm_with_retry(chain, {
        "agent_name": agent_name,
        "output": json.dumps(output, indent=2),
        "criteria": criteria,
    })

    return parse_and_validate(content, ReviewResult)
