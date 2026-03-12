from agents.pm_agent import run_pm_agent
from agents.test_manager import run_test_manager
from agents.test_lead import run_test_lead
from agents.qa_agent import run_qa_agent


def run_workflow(requirement):

    print("\nRunning Product Manager Agent...")
    srs = run_pm_agent(requirement)

    print("\nRunning Test Manager Agent...")
    strategy = run_test_manager(srs)

    print("\nRunning Test Lead Agent...")
    step = run_test_lead(strategy)

    print("\nRunning QA Agent...")
    qa_output = run_qa_agent(step)

    return {
        "SRS": srs,
        "Test Strategy": strategy,
        "STEP": step,
        "QA Output": qa_output
    }