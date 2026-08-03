from __future__ import annotations

import os

from openai import AzureOpenAI
from openai import OpenAIError

from app.database.config import settings
from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.base_provider import (
    BaseProvider,
)

__all__ = (
    "AzureProvider",
)


class AzureProvider(BaseProvider):
    """
    Azure OpenAI provider implementation.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        *,
        config: ModelConfig,
        prompt: str,
    ) -> str:
        """
        Generate a response using Azure OpenAI.

        Args:
            config:
                Model configuration.

            prompt:
                Prompt sent to the language model.

        Returns:
            Generated response.

        Raises:
            RuntimeError:
                If Azure OpenAI returns an error.
        """

        self.validate_config(
            config=config,
        )

        self.before_generate(
            config=config,
            prompt=prompt,
        )

        client = self._create_client(
            config=config,
        )

        messages = self._build_messages(
            config=config,
            prompt=prompt,
        )

        try:
            response = client.chat.completions.create(
                model=config.deployment_name,
                messages=messages,
                temperature=config.temperature,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty,
                max_completion_tokens=config.max_tokens,
            )
            print("=" * 80)
            print("AZURE RAW RESPONSE")
            print(response)
            print("=" * 80)

            print("FINISH REASON:", response.choices[0].finish_reason)
            print("MESSAGE:", repr(response.choices[0].message.content))

        except OpenAIError as ex:
            raise RuntimeError(
                f"Azure OpenAI error: {ex}",
            ) from ex

        content = (
            response.choices[0].message.content
            or ""
        )

        generated_response = self.after_generate(
            response=content,
        )

        return generated_response

    # ==========================================================
    # OVERRIDES
    # ==========================================================

    def validate_config(
        self,
        *,
        config: ModelConfig,
    ) -> None:
        """
        Validate the Azure OpenAI configuration.

        Args:
            config:
                Model configuration.

        Raises:
            ValueError:
                If the configuration is incomplete.
        """

        if not config.api_base_url:
            raise ValueError(
                "Azure endpoint is missing.",
            )

        if not config.deployment_name:
            raise ValueError(
                "Deployment name is missing.",
            )

        if not config.api_key_alias:
            raise ValueError(
                "API key alias is missing.",
            )

        api_key = os.getenv(
            config.api_key_alias,
        )

        if not api_key:
            raise ValueError(
                f"Environment variable '{config.api_key_alias}' was not found.",
            )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_client(
        self,
        *,
        config: ModelConfig,
    ) -> AzureOpenAI:
        """
        Create an Azure OpenAI client.

        Args:
            config:
                Model configuration.

        Returns:
            Configured Azure OpenAI client.
        """

        api_key = os.getenv(
            config.api_key_alias,
        )

        client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=config.api_base_url,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            timeout=config.timeout_seconds,
        )

        return client

    @staticmethod
    def _build_messages(
        *,
        config: ModelConfig,
        prompt: str,
    ) -> list[dict[str, str]]:
        """
        Build the chat messages.

        Args:
            config:
                Model configuration.

            prompt:
                User prompt.

        Returns:
            Chat messages formatted for Azure OpenAI.
        """

        messages = [
            {
                "role": "system",
                "content": config.system_prompt or "",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        return messages