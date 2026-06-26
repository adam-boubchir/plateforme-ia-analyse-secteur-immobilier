from sqlalchemy.orm import Session

from app.services.model_manager import (
    ModelManager
)

from app.services.providers.provider_factory import (
    ProviderFactory
)

from app.database.config import settings


class LLMService:

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

        config = self.model_manager.get(
            agent_name
        )

        api_key = settings.OPENAI_API_KEY

        provider = ProviderFactory.create(
            config.provider,
            api_key
        )

        return provider.generate(
            config=config,
            prompt=prompt
        )