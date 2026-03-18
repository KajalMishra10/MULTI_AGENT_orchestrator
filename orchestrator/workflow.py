import logging
from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.pm_agent import run_pm_agent
from agents.test_manager import run_test_manager
from agents.test_lead import run_test_lead
from agents.manual_qa import run_manual_qa
from agents.automation_qa import run_automation_qa
from agents.reviewer import run_reviewer
from rag.retriever import get_retriever
from utils.save_output import save_agent_output

logger = logging.getLogger(__name__)

MAX_REVISIONS = 2


# STATE SCHEMA
class AgentState(TypedDict, total=False):
    idea: str
    srs: dict
    strategy: dict
    plan: dict
    manual_tests: dict
    automation_tests: dict
    run_dir: str
    # Review tracking
    srs_feedback: str
    srs_revisions: int
    strategy_feedback: str
    strategy_revisions: int


# NODES

def pm_node(state: AgentState):
    idea = state["idea"]
    feedback = state.get("srs_feedback", "")
    revisions = state.get("srs_revisions", 0)

    if feedback:
        logger.info(f"[PM Agent] Revision {revisions} - addressing feedback")

    srs = run_pm_agent(idea, feedback=feedback)
    save_agent_output(state["run_dir"], f"1_srs_v{revisions + 1}", srs)
    return {"srs": srs, "srs_revisions": revisions + 1}


def review_srs_node(state: AgentState):
    logger.info("[Reviewer] Reviewing SRS...")

    review = run_reviewer(
        agent_name="Product Manager",
        output=state["srs"],
        criteria="""
- product_overview should be detailed (at least 2-3 sentences)
- target_users should have at least 2 user types
- features should have at least 3 features
- No empty or placeholder values
"""
    )

    save_agent_output(state["run_dir"], f"1_srs_review_v{state.get('srs_revisions', 1)}", review)
    logger.info(f"[Reviewer] SRS score: {review.get('score', '?')}/10 - {'APPROVED' if review.get('approved') else 'NEEDS REVISION'}")

    return {"srs_feedback": review.get("feedback", "")}


def srs_decision(state: AgentState) -> str:
    """Decide: approve SRS or send back to PM for revision."""
    revisions = state.get("srs_revisions", 1)
    feedback = state.get("srs_feedback", "")

    # If no feedback or max revisions reached, move forward
    if not feedback or revisions >= MAX_REVISIONS:
        if revisions >= MAX_REVISIONS:
            logger.info(f"[Reviewer] Max revisions ({MAX_REVISIONS}) reached for SRS, moving forward")
        return "approved"

    # Check if the review was actually approved (no real issues)
    srs = state.get("srs", {})
    if not srs.get("validation_error") and len(srs.get("features", [])) >= 3:
        return "approved"

    return "needs_revision"


def tm_node(state: AgentState):
    retriever = get_retriever()
    docs = retriever.invoke(str(state["srs"]))
    context = "\n".join([d.page_content for d in docs])
    feedback = state.get("strategy_feedback", "")
    revisions = state.get("strategy_revisions", 0)

    if feedback:
        logger.info(f"[Test Manager] Revision {revisions} - addressing feedback")

    srs_input = f"""
       Use these testing guidelines:

       {context}
       Create testing strategy for this SRS:
       {state["srs"]}
    """

    strategy = run_test_manager(srs_input, feedback=feedback)
    save_agent_output(state["run_dir"], f"2_test_strategy_v{revisions + 1}", strategy)
    return {"strategy": strategy, "strategy_revisions": revisions + 1}


def review_strategy_node(state: AgentState):
    logger.info("[Reviewer] Reviewing Test Strategy...")

    review = run_reviewer(
        agent_name="Test Manager",
        output=state["strategy"],
        criteria="""
- scope should clearly define what is being tested
- test_types should include at least 3 types (e.g., functional, performance, security)
- environment should specify test environment details
- risks should identify at least 2 risks
- No empty or placeholder values
"""
    )

    save_agent_output(state["run_dir"], f"2_strategy_review_v{state.get('strategy_revisions', 1)}", review)
    logger.info(f"[Reviewer] Strategy score: {review.get('score', '?')}/10 - {'APPROVED' if review.get('approved') else 'NEEDS REVISION'}")

    return {"strategy_feedback": review.get("feedback", "")}


def strategy_decision(state: AgentState) -> str:
    """Decide: approve strategy or send back to TM for revision."""
    revisions = state.get("strategy_revisions", 1)
    feedback = state.get("strategy_feedback", "")

    if not feedback or revisions >= MAX_REVISIONS:
        if revisions >= MAX_REVISIONS:
            logger.info(f"[Reviewer] Max revisions ({MAX_REVISIONS}) reached for Strategy, moving forward")
        return "approved"

    strategy = state.get("strategy", {})
    if not strategy.get("validation_error") and len(strategy.get("test_types", [])) >= 3:
        return "approved"

    return "needs_revision"


def tl_node(state: AgentState):
    plan = run_test_lead(state["strategy"])
    save_agent_output(state["run_dir"], "3_execution_plan", plan)
    return {"plan": plan}


def manual_node(state: AgentState):
    tests = run_manual_qa(state["plan"])
    save_agent_output(state["run_dir"], "4_manual_tests", tests)
    return {"manual_tests": tests}


def automation_node(state: AgentState):
    scripts = run_automation_qa(state["plan"])
    save_agent_output(state["run_dir"], "5_automation_tests", scripts)
    return {"automation_tests": scripts}


# GRAPH

def build_graph():

    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("pm", pm_node)
    builder.add_node("review_srs", review_srs_node)
    builder.add_node("tm", tm_node)
    builder.add_node("review_strategy", review_strategy_node)
    builder.add_node("tl", tl_node)
    builder.add_node("manual", manual_node)
    builder.add_node("automation", automation_node)

    # Flow: PM → Review SRS → (decision) → TM → Review Strategy → (decision) → TL → QA
    builder.set_entry_point("pm")

    builder.add_edge("pm", "review_srs")

    builder.add_conditional_edges("review_srs", srs_decision, {
        "approved": "tm",
        "needs_revision": "pm",
    })

    builder.add_edge("tm", "review_strategy")

    builder.add_conditional_edges("review_strategy", strategy_decision, {
        "approved": "tl",
        "needs_revision": "tm",
    })

    builder.add_edge("tl", "manual")
    builder.add_edge("tl", "automation")

    builder.add_edge("manual", END)
    builder.add_edge("automation", END)

    return builder.compile()
