import os

import requests
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import tool_call
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.config import get_config
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from src.configuration import Configuration
from src.prompts import FORMAT_SEARCH_RESULTS
from src.state import AgentState, WebSearchInput
from src.utils import random_id


# Graph Nodes
def generate_clarification_search_query(state: AgentState):
    from pydantic import BaseModel, Field

    class ClarifyQuerySchema(BaseModel):
        clarify_search_queries: list[str] = Field(
            ..., description="List of 2-3 relevant search queries"
        )

    config = Configuration.from_configurable(get_config())
    llm = ChatOpenAI(model=config.model, temperature=0.7)
    structured_llm = llm.with_structured_output(ClarifyQuerySchema)

    prompt = f"""
    You are a helpful research assistant. Based on the user's question: "{state.user_input}",
    generate 2 or 3 search queries that would help clarify or expand on the topic.
    """

    result = structured_llm.invoke(prompt)
    return result.dict()
    # TODO: Implement the logic to generate the clarification search query
    """
    1. Define a pydantic schema and use llm.with_structured_output to generate the schema
    https://python.langchain.com/docs/concepts/structured_outputs/
    """


def web_search(state: WebSearchInput):
    query = state.search_query
    api_key = os.getenv("TAVILY_API_KEY")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"query": query, "search_depth": "basic", "include_answer": False}

    response = requests.post(
        "https://api.tavily.com/search", json=payload, headers=headers
    )

    if response.status_code != 200:
        return {
            "clarify_search_results": [f"Error: {response.text}"],
            "clarify_messages": [],
        }
    data = response.json()
    results = []

    for result in data.get("results", []):
        title = result.get("title", "No Title")
        url = result.get("url", "No URL")
        results.append(f"{title} - {url}")

    return {"clarify_search_results": results, "clarify_messages": []}
    # TODO: Invoke the web search API
    # https://docs.firecrawl.dev/features/search#performing-a-search-with-firecrawl

    # Playground: https://www.firecrawl.dev/app/playground?mode=search&searchQuery=MCP&searchLimit=5&searchScrapeContent=true&formats=markdown&parsePDF=true&maxAge=14400000


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
