from langgraph.constants import END
from langgraph.graph import START, StateGraph
from src.configuration import Configuration
from src.state import ResearchAgentState


# Graph Nodes
def generate_queries(state: ResearchAgentState):
    pass


def draft_report_section(state: ResearchAgentState):
    pass


def check_knowledge_gap(state: ResearchAgentState):
    # IMPORTANT: provide feedback if knowledge gap exists
    pass


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
