from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


def merge_search_results(curr_results: list[str], new_results: list[str]) -> list[str]:
    """
    Merge the search results
    """

    return curr_results + new_results


class AgentState(BaseModel):
    """
    State for Deep Researcher Agent
    """

    ask_clarification: bool = Field(
        default=True, description="Whether the agent should ask for clarification"
    )

    clarify_search_queries: list[str] = Field(
        default_factory=list,
        description="The search queries to clarify the user's query",
    )

    clarify_search_results: Annotated[list[str], merge_search_results] = Field(
        default_factory=list,
        description="The search results for the clarify search queries",
    )

    # https://langchain-ai.github.io/langgraph/concepts/low_level/?h=message#why-use-messages
    clarify_messages: Annotated[list[AnyMessage], add_messages] = Field(
        default_factory=list, description="The messages for the clarify search queries"
    )


class WebSearchInput(BaseModel):
    """
    Input for the web search
    """

    query_idx: int = Field(description="The index of the search query")
    search_query: str = Field(description="The search query to search the web for")
