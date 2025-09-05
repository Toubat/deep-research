from langgraph.constants import END
from langgraph.graph import START, StateGraph
from src.configuration import Configuration
from src.state import ResearchAgentState
from src.configuration import Configuration
from langchain_openai import ChatOpenAI
from langgraph.config import get_config

# Graph Nodes
def generate_queries(state: ResearchAgentState):
    config = Configuration.from_configurable(get_config())
    model = config.reasoning_model
    llm = ChatOpenAI(model=model) if str(model).startswith("o4") else ChatOpenAI(model=model, temperature=0.3)
    prompt = f"""
    The research topic is: "{state.topic}".
    Background:
    ---
    {state.research_context}
    ---
    Generate 2–3 diverse and highly relevant search queries.
    Return each query on its own line.
    """
    resp = llm.invoke(prompt)
    queries = [q.strip(" -\t") for q in resp.content.strip().split("\n") if q.strip()]
    if not queries:
        queries = [f"{state.topic} overview"]
    return {"search_queries": queries}

def draft_report_section(state: ResearchAgentState):
    config = Configuration.from_configurable(get_config())
    model = config.reasoning_model
    llm = ChatOpenAI(model=model) if str(model).startswith("o4") else ChatOpenAI(model=model, temperature=0.4)
    prompt = f"""
    Research topic: "{state.topic}"
    Section description: {state.description}
    Section goal: {state.goal}
    Background:
    ---
    {state.research_context}
    ---
    Write a detailed draft report section (3–5 paragraphs) that directly meets the section goal.
    Be specific and informative; cite facts when appropriate.
    """
    resp = llm.invoke(prompt)
    draft = (resp.content or "").strip() or f"{state.topic}: (placeholder) No content generated."
    return {"draft_content": draft, "research_results": {state.topic: draft}}



def check_knowledge_gap(state: ResearchAgentState):
    # IMPORTANT: provide feedback if knowledge gap exists
    config = Configuration.from_configurable(get_config())
    model = config.reasoning_model
    llm = ChatOpenAI(model=model) if str(model).startswith("o4") else ChatOpenAI(model=model, temperature=0.3)

    prompt = f"""
    As an objective evaluator, determine whether the following DRAFT fully meets the SECTION GOAL.
    SECTION GOAL:
    {state.goal}
    DRAFT:
    ---
    {state.draft_content}
    ---
    Answer on the first line with exactly one word: "Yes" if the goal is fully met; otherwise "No".
    If "No", on the next lines list 2–4 specific, actionable gaps that must be addressed.
    """
    resp = llm.invoke(prompt)
    text = (resp.content or "").strip()
    first_line, *rest = text.splitlines()
    met = first_line.strip().upper().startswith("YES")

    if met:
        return {"has_knowledge_gap": False}

    gaps = "\n".join(rest).strip() or "Add concrete details, evidence, and citations aligned to the goal."
    feedback = f"\n\n[Goal check]\nGoal met: False\nGaps:\n{gaps}"
    return {"has_knowledge_gap": False, "draft_content": (state.draft_content or "").rstrip() + feedback}

def finalize_research_results(state: ResearchAgentState):
    return {"research_results": {state.topic: state.draft_content}}


# Graph Edges
def decide_finish_report_section(state: ResearchAgentState):
    if state.has_knowledge_gap:
        return "generate_queries"
    else:
        return "finalize_research_results"


def create_research_agent():
    graph_builder = StateGraph(ResearchAgentState, Configuration)

    graph_builder.add_node("generate_queries", generate_queries)
    graph_builder.add_node("draft_report_section", draft_report_section)
    graph_builder.add_node("check_knowledge_gap", check_knowledge_gap)
    graph_builder.add_node("finalize_research_results", finalize_research_results)

    graph_builder.add_edge(START, "generate_queries")
    graph_builder.add_edge("generate_queries", "draft_report_section")
    graph_builder.add_edge("draft_report_section", "check_knowledge_gap")
    graph_builder.add_conditional_edges(
        "check_knowledge_gap",
        decide_finish_report_section,
        ["generate_queries", "finalize_research_results"],
    )
    graph_builder.add_edge("finalize_research_results", END)

    return graph_builder.compile()
