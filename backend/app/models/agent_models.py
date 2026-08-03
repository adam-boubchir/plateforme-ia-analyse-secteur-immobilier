from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

__all__ = (
    "ModelConfig",
    "LLMMetadata",
    "LLMResponse",
    "AgentMetadata",
    "AgentResponse",
    "AgentExecutionResult",
)


class BaseAgentModel(BaseModel):
    """
    Base class shared by every domain model.
    """

    model_config = ConfigDict(
        frozen=False,
        extra="ignore",
    )


# ==========================================================
# MODEL CONFIGURATION
# ==========================================================


class ModelConfig(BaseAgentModel):
    """
    AI model configuration.
    """

    agent_name: str

    provider: str

    model_name: str

    api_key_alias: str | None = None

    api_base_url: str | None = None

    deployment_name: str | None = None

    system_prompt: str | None = None

    temperature: float = 0.0

    top_p: float = 1.0

    frequency_penalty: float = 0.0

    presence_penalty: float = 0.0

    timeout_seconds: int = 60

    max_tokens: int = 4096

    is_active: bool = True


# ==========================================================
# LLM METADATA
# ==========================================================


class LLMMetadata(BaseAgentModel):
    """
    Metadata returned by a language model.
    """

    provider: str

    model_name: str

    deployment_name: str | None = None

    input_tokens: int = 0

    output_tokens: int = 0

    total_tokens: int = 0

    finish_reason: str | None = None


# ==========================================================
# LLM RESPONSE
# ==========================================================


class LLMResponse(BaseAgentModel):
    """
    Generic response returned by a provider.
    """

    content: str

    metadata: LLMMetadata | None = None


# ==========================================================
# AGENT METADATA
# ==========================================================


class AgentMetadata(BaseAgentModel):
    """
    Execution metadata shared by every AI agent.
    """

    agent_name: str

    started_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    finished_at: datetime | None = None

    execution_time_ms: float | None = None

    success: bool = True

    error: str | None = None


# ==========================================================
# AGENT RESPONSE
# ==========================================================


class AgentResponse(BaseAgentModel):
    """
    Standard response returned by every AI agent.
    """

    success: bool = True

    content: str

    metadata: AgentMetadata | None = None

    llm: LLMMetadata | None = None

    data: Any = None

    error: str | None = None


# ==========================================================
# AGENT EXECUTION RESULT
# ==========================================================


class AgentExecutionResult(BaseAgentModel):
    """
    Internal execution result.
    """

    success: bool

    result: Any = None

    error: str | None = None

    execution_time_ms: float = 0