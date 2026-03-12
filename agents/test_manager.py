import json
from agents.llm_client import call_llm


def run_test_manager(srs_json):

    with open("prompts/test_strategy_prompt.txt") as f:
        system_prompt = f.read()

    response = call_llm(system_prompt, str(srs_json))

    try:
        data = json.loads(response)
    except:
        data = {"raw_output": response}

    return data