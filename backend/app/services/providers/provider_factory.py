from typing import Type

from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.azure_provider import (
    AzureProvider,
)
from app.services.providers.ollama_provider import (
    OllamaProvider,
)
from app.services.providers.openai_provider import (
    OpenAIProvider,
)


class ProviderFactory:
    """
    Factory responsible for instantiating
    the appropriate LLM provider.

    Supported providers
    -------------------
    • Azure OpenAI
    • OpenAI
    • Ollama

    New providers can be registered without
    modifying the rest of the project.
    """

    _PROVIDERS: dict[str, Type] = {
        "azure": AzureProvider,
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
    }

    # ==========================================================
    # PUBLIC
    # ==========================================================

    @classmethod
    def create(
        cls,
        config: ModelConfig,
    ):
        """
        Return an instance of the configured provider.
        """

        provider_name: str = (
            config.provider
            .strip()
            .lower()
        )

        provider_class: Type | None = cls._PROVIDERS.get(
            provider_name,
        )

        if provider_class is None:

            supported = ", ".join(
                cls.supported_providers()
            )

            raise ValueError(
                f"Unsupported provider '{config.provider}'. "
                f"Supported providers: {supported}"
            )

        return provider_class()

    @classmethod
    def register_provider(
        cls,
        name: str,
        provider_class: Type,
    ) -> None:
        """
        Register a new provider.
        """

        cls._PROVIDERS[
            name.strip().lower()
        ] = provider_class

    @classmethod
    def supported_providers(
        cls,
    ) -> list[str]:
        """
        Return the supported providers.
        """

        return sorted(
            cls._PROVIDERS.keys(),
        )


__all__ = [
    "ProviderFactory",
]