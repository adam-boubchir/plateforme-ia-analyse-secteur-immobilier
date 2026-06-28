from sqlalchemy.orm import Session

from app.services.model_manager import (
    ModelManager
)

from app.services.providers.provider_factory import (
    ProviderFactory
)


class LLMService:
    """
    Central service used to communicate with an LLM.
    """

    def __init__(
        self,
        db: Session
    ):

        self.model_manager = ModelManager(db)

    def generate(
        self,
        agent_name: str,
        prompt: str
    ) -> str:
        """
        Generate a response using the configured model.
        """

        config = self.model_manager.get(
            agent_name
        )

        provider = ProviderFactory.create(
            config
        )

        return provider.generate(
            config=config,
            prompt=prompt
        )