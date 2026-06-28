from app.models.agent_models import ModelConfig

from app.services.providers.openai_provider import (
    OpenAIProvider,
)

from app.services.providers.azure_provider import (
    AzureProvider,
)

from app.services.providers.ollama_provider import (
    OllamaProvider,
)


class ProviderFactory:
    """
    Factory used to create the correct LLM provider.
    """

    @staticmethod
    def create(
        config: ModelConfig
    ):

        provider = config.provider.lower()

        if provider == "openai":
            return OpenAIProvider()

        if provider == "azure":
            return AzureProvider()

        if provider == "ollama":
            return OllamaProvider()

        raise ValueError(
            f"Unsupported provider: {config.provider}"
        )