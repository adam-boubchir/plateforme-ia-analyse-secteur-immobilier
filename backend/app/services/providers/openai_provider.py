import os

from openai import (
    OpenAI,
    OpenAIError,
)

from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.base_provider import (
    BaseProvider,
)


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider.

    Responsible for communicating with the OpenAI API.
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
        Generate a response using OpenAI.
        """

        client: OpenAI = self._create_client(
            config=config,
        )

        try:
            response = client.chat.completions.create(
                model=config.model_name,
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
                max_tokens=config.max_tokens,
            )

        except OpenAIError as ex:
            raise RuntimeError(
                f"OpenAI error: {ex}"
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
    ) -> OpenAI:
        """
        Create an OpenAI client.
        """

        api_key: str | None = os.getenv(
            config.api_key_alias,
        )

        if api_key is None:
            raise ValueError(
                f"Environment variable '{config.api_key_alias}' was not found."
            )

        return OpenAI(
            api_key=api_key,
            base_url=config.api_base_url or None,
            timeout=config.timeout_seconds,
        )


__all__ = [
    "OpenAIProvider",
]