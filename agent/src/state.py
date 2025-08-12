from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing import List


def merge_search_results(curr_results: list[str], new_results: list[str]) -> list[str]:
    """
    Merge the search results
    """

    return curr_results + new_results


class AgentState(BaseModel):
    """
    State for Deep Researcher Agent
    """

    user_input: str = Field(description="The original user question")

    background_search_queries: list[str] = Field(
        default_factory=list,
        description="The search queries to search background of the user's query",
    )

    background_search_results: Annotated[list[str], merge_search_results] = Field(
        default_factory=list,
        description="The search results for the background search queries",
    )

    # https://langchain-ai.github.io/langgraph/concepts/low_level/?h=message#why-use-messages
    background_messages: Annotated[list[AnyMessage], add_messages] = Field(
        default_factory=list,
        description="The messages for the background search queries",
    )

    clarification_question: str | None = Field(default=None)

    clarification_result: str | None = Field(default=None)


class WebSearchInput(BaseModel):
    """
    Input for the web search
    """

    query_idx: int = Field(description="The index of the search query")
    search_query: str = Field(description="The search query to search the web for")


class ClarifyQuerySchema(BaseModel):
    clarify_search_queries: list[str] = Field(
        ..., description="List of 2-3 relevant search queries"
    )

class ReportSection(BaseModel):
    title: str
    description: str

class ReportSectionSchema(BaseModel):
    sections: List[ReportSection]
