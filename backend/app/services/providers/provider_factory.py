from app.database.config import settings

from app.services.providers.openai_provider import (
    OpenAIProvider
)


class ProviderFactory:

    @staticmethod
    def create(
        provider_name: str,
        api_key: str
    ):

        provider = provider_name.lower()

        if provider == "openai":

            return OpenAIProvider(
                api_key
            )

        raise ValueError(
            f"Provider '{provider_name}' is not supported."
        )