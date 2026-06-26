from abc import ABC, abstractmethod

from app.models.agent_models import (
    ModelConfig
)


class BaseProvider(ABC):

    @abstractmethod
    def generate(
        self,
        config: ModelConfig,
        prompt: str
    ) -> str:
        pass