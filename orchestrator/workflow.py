from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.pm_agent import run_pm_agent
from agents.test_manager import run_test_manager
from agents.test_lead import run_test_lead
from agents.manual_qa import run_manual_qa
from agents.automation_qa import run_automation_qa
from rag.retriever import get_retriever


# STATE SCHEMA
class AgentState(TypedDict, total=False):
    idea: str
    srs: dict
    strategy: dict
    plan: dict
    manual_tests: dict
    automation_tests: dict


# NODES

def pm_node(state: AgentState):
    idea = state["idea"]
    srs = run_pm_agent(idea)
    return {"srs": srs}


def tm_node(state: AgentState):
    retriever = get_retriever()

    docs = retriever.invoke(str(state["srs"]))

    context = "\n".join([d.page_content for d in docs])

    strategy = run_test_manager(
       f"""
       Use these testing guidelines:

       {context}
       Create testing strategy for this SRS:
       {state["srs"]}
    """)
    return {"strategy": strategy}


def tl_node(state: AgentState):
    plan = run_test_lead(state["strategy"])
    return {"plan": plan}


def manual_node(state: AgentState):
    tests = run_manual_qa(state["plan"])
    return {"manual_tests": tests}


def automation_node(state: AgentState):
    scripts = run_automation_qa(state["plan"])
    return {"automation_tests": scripts}


# GRAPH

def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("pm", pm_node)
    builder.add_node("tm", tm_node)
    builder.add_node("tl", tl_node)
    builder.add_node("manual", manual_node)
    builder.add_node("automation", automation_node)

    builder.set_entry_point("pm")

    builder.add_edge("pm", "tm")
    builder.add_edge("tm", "tl")

    builder.add_edge("tl", "manual")
    builder.add_edge("tl", "automation")

    builder.add_edge("manual", END)
    builder.add_edge("automation", END)

    return builder.compile()