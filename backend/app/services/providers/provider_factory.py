from __future__ import annotations

from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.azure_provider import (
    AzureProvider,
)
from app.services.providers.base_provider import (
    BaseProvider,
)
from app.services.providers.ollama_provider import (
    OllamaProvider,
)
from app.services.providers.openai_provider import (
    OpenAIProvider,
)

__all__ = (
    "ProviderFactory",
)


class ProviderFactory:
    """
    Factory responsible for resolving LLM providers.

    Supported providers can be extended dynamically
    through provider registration.
    """

    _PROVIDERS: dict[str, type[BaseProvider]] = {
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
        *,
        config: ModelConfig,
    ) -> BaseProvider:
        """
        Create the provider associated with a model configuration.

        Args:
            config:
                Model configuration.

        Returns:
            Instantiated provider.

        Raises:
            ValueError:
                If the provider is not supported.
        """

        provider_name = cls._normalize_provider_name(
            name=config.provider,
        )

        provider_class = cls._PROVIDERS.get(
            provider_name,
        )

        if provider_class is None:
            supported = ", ".join(
                cls.supported_providers(),
            )

            raise ValueError(
                f"Unsupported provider '{config.provider}'. "
                f"Supported providers: {supported}.",
            )

        provider = provider_class()

        return provider

    @classmethod
    def register_provider(
        cls,
        *,
        name: str,
        provider_class: type[BaseProvider],
    ) -> None:
        """
        Register a new provider implementation.

        Args:
            name:
                Provider name.

            provider_class:
                Provider implementation.

        Raises:
            ValueError:
                If the provider already exists.
        """

        normalized_name = cls._normalize_provider_name(
            name=name,
        )

        if normalized_name in cls._PROVIDERS:
            raise ValueError(
                f"Provider '{normalized_name}' is already registered.",
            )

        cls._PROVIDERS[normalized_name] = provider_class

    @classmethod
    def supported_providers(
        cls,
    ) -> list[str]:
        """
        Return the list of supported providers.

        Returns:
            Sorted provider names.
        """

        providers = sorted(
            cls._PROVIDERS.keys(),
        )

        return providers

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _normalize_provider_name(
        *,
        name: str,
    ) -> str:
        """
        Normalize a provider name.

        Args:
            name:
                Raw provider name.

        Returns:
            Normalized provider name.
        """

        normalized_name = name.strip().lower()

        return normalized_name