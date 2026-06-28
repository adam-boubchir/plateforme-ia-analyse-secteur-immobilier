from app.models.agent_models import ModelConfig

from app.services.providers.base_provider import (
    BaseProvider
)


class OllamaProvider(BaseProvider):

    def generate(
        self,
        config: ModelConfig,
        prompt: str
    ) -> str:

        raise NotImplementedError(
            "Ollama provider is not implemented yet."
        )