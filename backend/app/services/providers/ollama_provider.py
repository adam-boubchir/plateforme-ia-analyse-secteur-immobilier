from __future__ import annotations

import requests

from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.base_provider import (
    BaseProvider,
)

__all__ = (
    "OllamaProvider",
)


class OllamaProvider(BaseProvider):
    """
    Ollama provider implementation.

    Responsible for communicating with a local or remote
    Ollama server.
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
        Generate a response using Ollama.

        Args:
            config:
                Model configuration.

            prompt:
                Prompt sent to the language model.

        Returns:
            Generated response.

        Raises:
            RuntimeError:
                If the Ollama server returns an error or
                an invalid response.
        """

        self.validate_config(
            config=config,
        )

        self.before_generate(
            config=config,
            prompt=prompt,
        )

        payload = self._build_payload(
            config=config,
            prompt=prompt,
        )

        try:
            response = requests.post(
                url=f"{config.api_base_url}/api/generate",
                json=payload,
                timeout=config.timeout_seconds,
            )

            response.raise_for_status()

            data: dict[str, object] = response.json()

        except requests.RequestException as ex:
            raise RuntimeError(
                f"Ollama error: {ex}",
            ) from ex

        except ValueError as ex:
            raise RuntimeError(
                "Invalid JSON returned by Ollama.",
            ) from ex

        content = str(
            data.get(
                "response",
                "",
            )
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
        Validate the Ollama configuration.

        Args:
            config:
                Model configuration.

        Raises:
            ValueError:
                If the configuration is incomplete.
        """

        if not config.api_base_url:
            raise ValueError(
                "Ollama server URL is missing.",
            )

        if not config.model_name:
            raise ValueError(
                "Ollama model name is missing.",
            )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _build_payload(
        *,
        config: ModelConfig,
        prompt: str,
    ) -> dict[str, object]:
        """
        Build the request payload sent to Ollama.

        Args:
            config:
                Model configuration.

            prompt:
                User prompt.

        Returns:
            HTTP payload compatible with the Ollama API.
        """

        payload = {
            "model": config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": config.temperature,
                "top_p": config.top_p,
            },
        }

        return payload