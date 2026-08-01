import os

from openai import (
    AzureOpenAI,
    OpenAIError,
)

from app.database.config import settings
from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.base_provider import (
    BaseProvider,
)


class AzureProvider(BaseProvider):
    """
    Azure OpenAI provider.

    Responsible for communicating with Azure OpenAI.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        config: ModelConfig,
        prompt: str,
    ) -> str:
        """
        Generate a response using Azure OpenAI.
        """

        client: AzureOpenAI = self._create_client(
            config=config,
        )

        try:
            response = client.chat.completions.create(
                model=config.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": config.system_prompt or "",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=config.temperature,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty,
                max_completion_tokens=config.max_tokens,
            )

        except OpenAIError as ex:
            raise RuntimeError(
                f"Azure OpenAI error: {ex}"
            ) from ex

        content: str | None = (
            response.choices[0].message.content
        )

        return content.strip() if content else ""

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_client(
        self,
        config: ModelConfig,
    ) -> AzureOpenAI:
        """
        Create an Azure OpenAI client.
        """

        api_key: str | None = os.getenv(
            config.api_key_alias,
        )

        if api_key is None:
            raise ValueError(
                f"Environment variable '{config.api_key_alias}' was not found."
            )

        return AzureOpenAI(
            api_key=api_key,
            azure_endpoint=config.api_base_url,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            timeout=config.timeout_seconds,
        )


__all__ = [
    "AzureProvider",
]