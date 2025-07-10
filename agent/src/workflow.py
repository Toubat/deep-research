from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import tool_call
from langchain_core.prompts import PromptTemplate
from langgraph.config import get_config
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from src.configuration import Configuration
from src.prompts import FORMAT_SEARCH_RESULTS
from src.state import AgentState, WebSearchInput
from src.utils import random_id


# Graph Nodes
def generate_clarification_search_query(state: AgentState):
    config = Configuration.from_configurable(get_config())

    # TODO: Implement the logic to generate the clarification search query
    """
    1. Define a pydantic schema and use llm.with_structured_output to generate the schema
    https://python.langchain.com/docs/concepts/structured_outputs/
    """

    return {"clarify_search_queries": ["Search query 1", "Search query 2"]}


def web_search(state: WebSearchInput):
    query = state.search_query

    # TODO: Invoke the web search API
    # https://docs.firecrawl.dev/features/search#performing-a-search-with-firecrawl

    # Playground: https://www.firecrawl.dev/app/playground?mode=search&searchQuery=MCP&searchLimit=5&searchScrapeContent=true&formats=markdown&parsePDF=true&maxAge=14400000

    return {"clarify_search_results": [f"Search result of query: {query}"]}


def append_search_results(state: AgentState):
    tool_call_id = random_id()

    tool_call_dict = tool_call(
        id=tool_call_id,
        name="web_search",
        args={"query": state.clarify_search_queries},
    )

    search_result_prompt = PromptTemplate.from_template(
        template=FORMAT_SEARCH_RESULTS,
        template_format="jinja2",
    )

    tool_call_message = AIMessage(content=[tool_call_dict])  # type: ignore

    tool_output = ToolMessage(
        tool_call_id=tool_call_id,
        content=search_result_prompt.format(
            search_results=state.clarify_search_results
        ),
    )

    return {"clarify_messages": [tool_call_message, tool_output]}


# Graph Edges
def continue_search_background_info(state: AgentState):
    return [
        Send("web_search", WebSearchInput(query_idx=idx, search_query=query))
        for idx, query in enumerate(state.clarify_search_queries)
    ]


graph_builder = StateGraph(AgentState, Configuration)

graph_builder.add_node(
    "generate_clarification_search_query", generate_clarification_search_query
)
graph_builder.add_node("web_search", web_search)
graph_builder.add_node("append_search_results", append_search_results)

graph_builder.add_edge(START, "generate_clarification_search_query")
graph_builder.add_conditional_edges(
    "generate_clarification_search_query",
    continue_search_background_info,  # type: ignore
    ["web_search"],
)
graph_builder.add_edge("web_search", "append_search_results")
graph_builder.add_edge("append_search_results", END)


graph = graph_builder.compile()
