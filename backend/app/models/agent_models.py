from pydantic import BaseModel
from typing import Optional


class ModelConfig(BaseModel):

    agent_name: str

    provider: str

    model_name: str

    api_key_alias: Optional[str] = None

    temperature: float

    max_tokens: int

    is_active: bool

    api_base_url: Optional[str] = None

    deployment_name: Optional[str] = None

    system_prompt: Optional[str] = None

    timeout_seconds: int = 60

    top_p: float = 1.0

    frequency_penalty: float = 0.0

    presence_penalty: float = 0.0

from typing import Any


class AgentExecutionResult(BaseModel):

    success: bool

    result: Any = None

    error: str | None = None

    execution_time_ms: float