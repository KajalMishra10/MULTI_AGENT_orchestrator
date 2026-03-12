from agents.llm_client import call_llm


def run_qa_agent(step):
    """
    QA agent
    
    Input:
        Execution Plan
    
    Output:
        Test Cases + Automation scripts
    """

    with open("prompts/qa_prompt.txt", "r") as f:
        system_prompt = f.read()

    result = call_llm(system_prompt, step)

    return result