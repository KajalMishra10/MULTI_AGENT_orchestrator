import json
from agents.llm_client import call_llm


def run_pm_agent(requirement):

    with open("prompts/pm_prompt.txt") as f:
        system_prompt = f.read()

    response = call_llm(system_prompt, requirement)

    try:
        data = json.loads(response)
    except:
        print(" JSON parsing failed, returning raw text")
        data = {"raw_output": response}

    return data