from agents.llm_client import call_llm


def run_test_lead(strategy):
    """
    Test Lead agent
    
    Input:
        Test Strategy
    
    Output:
        System Test Execution Plan
    """

    system_prompt = """
You are a Test Lead.

Based on the test strategy generate a System Test Execution Plan.

Include:

- Test Phases
- Execution Timeline
- Resource Allocation
"""

    result = call_llm(system_prompt, strategy)

    return result