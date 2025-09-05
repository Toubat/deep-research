from __future__ import annotations

from typing import Annotated, List

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


def merge_search_results(curr_results: list[str], new_results: list[str]) -> list[str]:
    """
    Merge the search results
    """

    return curr_results + new_results


def merge_research_results(
    curr_results: dict[str, str], new_results: dict[str, str]
) -> dict[str, str]:
    """
    Merge the research results
    """
    return {**curr_results, **new_results}


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

    intro_section: str | None = Field(default=None)

    conclusion_section: str | None = Field(default=None)

    report_sections: list[ReportSection] = Field(default_factory=list)

    research_results: Annotated[dict[str, str], merge_research_results] = Field(
        default_factory=dict
    )

    section_results: list[SectionResult] = Field(default_factory=list)


class ResearchAgentState(BaseModel):
    research_context: str
    topic: str
    description: str
    goal: str = Field(default="", description="Measurable objective for this section")
    has_knowledge_gap: bool = Field(default=False)
    draft_content: str = Field(default="test content")
    research_results: dict[str, str] = Field(default_factory=dict)


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
    goal: str = Field(default="", description="Measurable objective for the section")
    
class SectionResult(BaseModel):
    title: str
    description: str
    content: str


class ReportSectionSchema(BaseModel):
    sections: List[ReportSection]
