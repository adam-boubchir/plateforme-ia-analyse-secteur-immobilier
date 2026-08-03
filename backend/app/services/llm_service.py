from __future__ import annotations

from typing import Any

from app.services.model_manager import (
    ModelManager,
)
from app.services.providers.provider_factory import (
    ProviderFactory,
)

__all__ = (
    "LLMService",
)


class LLMService:
    """
    Central service responsible for interacting with
    Large Language Models.

    Responsibilities
    ----------------
    - Load the model configuration.
    - Resolve the appropriate provider.
    - Execute prompt generation.
    """

    def __init__(
        self,
        *,
        model_manager: ModelManager,
    ) -> None:
        self._model_manager = model_manager

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        *,
        agent_name: str,
        prompt: str,
    ) -> str:
        """
        Generate a response using the configured language model.

        Args:
            agent_name:
                Name of the AI agent requesting the generation.

            prompt:
                Prompt sent to the language model.

        Returns:
            Generated response.
        """

        config = self._load_configuration(
            agent_name=agent_name,
        )

        provider = self._create_provider(
            config=config,
        )

        response = provider.generate(
            config=config,
            prompt=prompt,
        )

        cleaned_response = response.strip()

        return cleaned_response

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_configuration(
        self,
        *,
        agent_name: str,
    ) -> Any:
        """
        Retrieve the model configuration associated
        with the specified agent.

        Args:
            agent_name:
                Name of the AI agent.

        Returns:
            Model configuration.

        Raises:
            ValueError:
                If no configuration exists for the agent.
        """

        config = self._model_manager.get(
            agent_name=agent_name,
        )

        if config is None:
            raise ValueError(
                f"No model configured for agent '{agent_name}'.",
            )

        return config

    def _create_provider(
        self,
        *,
        config: Any,
    ) -> Any:
        """
        Create the provider associated with the given model
        configuration.

        Args:
            config:
                Model configuration.

        Returns:
            Instantiated provider.
        """

        provider = ProviderFactory.create(
            config=config,
        )

        return provider