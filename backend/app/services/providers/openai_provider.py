from __future__ import annotations

import os

from openai import OpenAI
from openai import OpenAIError

from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.base_provider import (
    BaseProvider,
)

__all__ = (
    "OpenAIProvider",
)


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider implementation.
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
        Generate a response using OpenAI.

        Args:
            config:
                Model configuration.

            prompt:
                Prompt sent to the language model.

        Returns:
            Generated response.

        Raises:
            RuntimeError:
                If the OpenAI API returns an error.
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
                model=config.model_name,
                messages=messages,
                temperature=config.temperature,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty,
                max_tokens=config.max_tokens,
            )

        except OpenAIError as ex:
            raise RuntimeError(
                f"OpenAI error: {ex}",
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
        Validate the OpenAI configuration.

        Args:
            config:
                Model configuration.

        Raises:
            ValueError:
                If the configuration is incomplete.
        """

        if not config.model_name:
            raise ValueError(
                "OpenAI model name is missing.",
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
    ) -> OpenAI:
        """
        Create an OpenAI client.

        Args:
            config:
                Model configuration.

        Returns:
            Configured OpenAI client.
        """

        api_key = os.getenv(
            config.api_key_alias,
        )

        client = OpenAI(
            api_key=api_key,
            base_url=config.api_base_url or None,
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
            Chat messages formatted for OpenAI.
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