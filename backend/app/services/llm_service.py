from typing import Any

from app.services.model_manager import (
    ModelManager,
)
from app.services.providers.provider_factory import (
    ProviderFactory,
)


class LLMService:
    """
    Central service responsible for interacting with
    Large Language Models.

    Responsibilities
    ----------------
    • Retrieve the model configuration
    • Instantiate the correct provider
    • Send prompts
    • Return generated responses
    """

    def __init__(
        self,
        model_manager: ModelManager,
    ) -> None:

        self.model_manager: ModelManager = model_manager

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        agent_name: str,
        prompt: str,
    ) -> str:
        """
        Generate a response using the configured model.
        """

        config: Any = self._load_configuration(
            agent_name=agent_name,
        )

        provider = ProviderFactory.create(
            config=config,
        )

        response: str = provider.generate(
            config=config,
            prompt=prompt,
        )

        return response.strip()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_configuration(
        self,
        agent_name: str,
    ) -> Any:
        """
        Load the model configuration.
        """

        config = self.model_manager.get(
            agent_name=agent_name,
        )

        if config is None:
            raise ValueError(
                f"No model configured for agent '{agent_name}'."
            )

        return config