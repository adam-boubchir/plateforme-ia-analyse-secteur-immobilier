from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

class ModelConfig(BaseModel):
    """
    Configuration of an AI model.

    One instance corresponds to one configured
    model in the database.
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
# AGENT EXECUTION RESULT
# ==========================================================

class AgentExecutionResult(BaseModel):
    """
    Generic execution result returned by every AI Agent.
    """

    success: bool

    result: Any = None

    error: str | None = None

    execution_time_ms: float = 0


# ==========================================================
# LLM METADATA
# ==========================================================

class LLMMetadata(BaseModel):
    """
    Metadata returned by the provider.
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

class LLMResponse(BaseModel):
    """
    Generic response returned by an LLM provider.
    """

    content: str

    metadata: LLMMetadata | None = None


# ==========================================================
# AGENT METADATA
# ==========================================================

class AgentMetadata(BaseModel):
    """
    Metadata common to every AI agent.
    """

    agent_name: str

    started_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    finished_at: datetime | None = None

    execution_time_ms: float | None = None

    success: bool = True

    error: str | None = None