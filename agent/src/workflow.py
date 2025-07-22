from typing import cast

from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import tool_call
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.config import get_config
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from src.configuration import Configuration
from src.prompts import (
    CLARIFY_QUERY_GEN_PROMPT,
    CONCAT_SINGLE_SEARCH_RESULT,
    FORMAT_SEARCH_RESULTS,
)
from src.state import AgentState, ClarifyQuerySchema, WebSearchInput
from src.utils import random_id
from tavily import TavilyClient

load_dotenv(find_dotenv(), override=True)

tavily_client = TavilyClient()


# Graph Nodes
def generate_clarification_search_query(state: AgentState):
    config = Configuration.from_configurable(get_config())
    llm = ChatOpenAI(model=config.model, temperature=0.2)
    structured_llm = llm.with_structured_output(ClarifyQuerySchema)

    prompt_tpl = PromptTemplate.from_template(CLARIFY_QUERY_GEN_PROMPT)
    chain = prompt_tpl | structured_llm

    result = cast(ClarifyQuerySchema, chain.invoke({"user_input": state.user_input}))
    return {"clarify_search_queries": result.clarify_search_queries}


def web_search(state: WebSearchInput):
    response = tavily_client.search("Who is Leo Messi?", search_depth="basic")

    concat_search_result_prompt = PromptTemplate.from_template(
        template=CONCAT_SINGLE_SEARCH_RESULT,
        template_format="jinja2",
    )

    concat_search_result = concat_search_result_prompt.format(
        search_results=response["results"]
    )

    return {"clarify_search_results": [concat_search_result]}


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
