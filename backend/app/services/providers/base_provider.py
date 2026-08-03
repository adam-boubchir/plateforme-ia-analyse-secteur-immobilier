from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.models.agent_models import (
    ModelConfig,
)

__all__ = (
    "BaseProvider",
)


class BaseProvider(ABC):
    """
    Abstract base class implemented by every LLM provider.

    Providers encapsulate the communication with a specific
    Large Language Model service such as Azure OpenAI,
    OpenAI, Ollama, Gemini, Claude, or any future provider.

    The generation workflow can be customized by overriding
    the optional lifecycle hooks.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    @abstractmethod
    def generate(
        self,
        *,
        config: ModelConfig,
        prompt: str,
    ) -> str:
        """
        Generate a response using the configured provider.

        Args:
            config:
                Model configuration.

            prompt:
                Prompt sent to the language model.

        Returns:
            Generated response.

        Raises:
            NotImplementedError:
                Must be implemented by concrete providers.
        """

        raise NotImplementedError

    # ==========================================================
    # OPTIONAL HOOKS
    # ==========================================================

    def validate_config(
        self,
        *,
        config: ModelConfig,
    ) -> None:
        """
        Validate the provider configuration.

        Concrete providers may override this method to perform
        provider-specific validation before generation.

        Args:
            config:
                Model configuration.
        """

        return None

    def before_generate(
        self,
        *,
        config: ModelConfig,
        prompt: str,
    ) -> None:
        """
        Hook executed immediately before sending the request.

        Concrete providers may override this method for
        logging, telemetry, preprocessing or validation.

        Args:
            config:
                Model configuration.

            prompt:
                Prompt that will be sent.
        """

        return None

    def after_generate(
        self,
        *,
        response: str,
    ) -> str:
        """
        Hook executed immediately after generation.

        The default implementation removes surrounding
        whitespace.

        Args:
            response:
                Raw generated response.

        Returns:
            Processed response.
        """

        cleaned_response = response.strip()

        return cleaned_response