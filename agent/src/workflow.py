from typing import cast

from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import AIMessage
from langchain_core.messages.tool import tool_call
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from langgraph.config import get_config
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send, interrupt
from src.configuration import Configuration
from src.mocks import MOCK_STATE_PATCH
from src.prompts import (
    ASK_CLARIFICATION_PROMPT,
    BACKGROUND_QUERY_GEN_PROMPT,
    CONCAT_SINGLE_SEARCH_RESULT,
    FORMAT_SEARCH_RESULTS,
)
from src.state import AgentState, ClarifyQuerySchema, WebSearchInput
from src.utils import random_id
from tavily import TavilyClient

load_dotenv(find_dotenv(), override=True)

tavily_client = TavilyClient()


# Graph Nodes
def init(state: AgentState):
    config = Configuration.from_configurable(get_config())

    if config.is_mock:
        return {"user_input": state.user_input, **MOCK_STATE_PATCH}

    return {}


def generate_background_search_query(state: AgentState):
    config = Configuration.from_configurable(get_config())
    llm = ChatOpenAI(model=config.reasoning_model)
    structured_llm = llm.with_structured_output(ClarifyQuerySchema)

    prompt_tpl = PromptTemplate.from_template(BACKGROUND_QUERY_GEN_PROMPT)
    chain = prompt_tpl | structured_llm

    result = cast(ClarifyQuerySchema, chain.invoke({"user_input": state.user_input}))
    return {"background_search_queries": result.clarify_search_queries}


def web_search(state: WebSearchInput):
    response = tavily_client.search(state.search_query, search_depth="basic")

    concat_search_result_prompt = PromptTemplate.from_template(
        template=CONCAT_SINGLE_SEARCH_RESULT,
        template_format="jinja2",
    )

    concat_search_result = concat_search_result_prompt.format(
        search_results=response["results"]
    )

    return {"background_search_results": [concat_search_result]}


def append_search_results(state: AgentState):
    tool_call_id = random_id()

    tool_call_dict = tool_call(
        id=tool_call_id,
        name="web_search",
        args={"query": state.background_search_queries},
    )

    search_result_prompt = PromptTemplate.from_template(
        template=FORMAT_SEARCH_RESULTS,
        template_format="jinja2",
    )

    tool_call_message = AIMessage(content=str(tool_call_dict))  # type: ignore

    tool_output = AIMessage(
        content=search_result_prompt.format(
            search_results=state.background_search_results
        ),
    )

    return {"background_messages": [tool_call_message, tool_output]}


async def ask_clarify_from_user(state: AgentState):
    config = Configuration.from_configurable(get_config())
    llm = ChatOpenAI(model=config.reasoning_model)

    background_messages = state.background_messages

    clarify_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                template=ASK_CLARIFICATION_PROMPT
            ),
            MessagesPlaceholder(variable_name="background_messages"),
            AIMessage(
                content="Now I have finished background queries, I will generate a clarification to user"
            ),
        ]
    )

    chain = clarify_prompt | llm
    clarification_question = await chain.ainvoke(
        {"user_input": state.user_input, "background_messages": background_messages}
    )

    clarification_result = interrupt({"questions": clarification_question})

    return {
        "clarification_result": clarification_result,
        "clarification_question": clarification_question,
    }


async def formulate_report_sections(state: AgentState):
    # take user_input, clarification_question, clarification_result, background_search_queries, background_search_results
    # ask LLM design report sections (title, description as detailed as possible)
    # sections = [
    #    {
    #       "title": string.
    #       "description": string
    #    } // use pydantic structured output
    # ]
    pass


# Graph Edges
def continue_search_background_info(state: AgentState):
    return [
        Send("web_search", WebSearchInput(query_idx=idx, search_query=query))
        for idx, query in enumerate(state.background_search_queries)
    ]


def decide_enterance(state: AgentState):
    config = Configuration.from_configurable(get_config())

    if config.is_mock:
        return END
    else:
        return "background_search"


graph_builder = StateGraph(AgentState, Configuration)

graph_builder.add_node("init", init)
graph_builder.add_node("background_search", generate_background_search_query)
graph_builder.add_node("web_search", web_search)
graph_builder.add_node("append_search_results", append_search_results)
graph_builder.add_node("ask_clarify_from_user", ask_clarify_from_user)

graph_builder.add_edge(START, "init")
graph_builder.add_conditional_edges(
    "init",
    decide_enterance,  # type: ignore
    ["background_search", END],
)
graph_builder.add_conditional_edges(
    "background_search",
    continue_search_background_info,  # type: ignore
    ["web_search"],
)
graph_builder.add_edge("web_search", "append_search_results")
graph_builder.add_edge("append_search_results", "ask_clarify_from_user")
graph_builder.add_edge("ask_clarify_from_user", END)


graph = graph_builder.compile()
