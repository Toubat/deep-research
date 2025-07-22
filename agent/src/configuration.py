from __future__ import annotations

from typing import Literal

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

ModelType = Literal["gpt-4.1", "o4-mini"]


class Configuration(BaseModel):
    """
    Configuration for the Deep Researcher Agent
    """

    model: ModelType = Field(
        default="gpt-4.1", description="The model to use for the Deep Researcher Agent"
    )

    reasoning_model: ModelType = Field(
        default="o4-mini", description="The model to use for the Deep Researcher Agent"
    )

    is_mock: bool = Field(default=True)

    @classmethod
    def from_configurable(cls, config: RunnableConfig) -> Configuration:
        return cls.model_validate(config.get("configurable", {}))

    def to_configurable(self) -> RunnableConfig:
        return RunnableConfig(configurable={"model": self.model})
