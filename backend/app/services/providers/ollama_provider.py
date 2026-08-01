import requests

from app.models.agent_models import (
    ModelConfig,
)
from app.services.providers.base_provider import (
    BaseProvider,
)


class OllamaProvider(BaseProvider):
    """
    Ollama provider.

    Responsible for communicating with a local
    Ollama server.

    Default endpoint:
        http://localhost:11434
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
        Generate a response using Ollama.
        """

        payload: dict = {
            "model": config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": config.temperature,
                "top_p": config.top_p,
            },
        }

        try:
            response = requests.post(
                url=f"{config.api_base_url}/api/generate",
                json=payload,
                timeout=config.timeout_seconds,
            )

            response.raise_for_status()

        except requests.RequestException as ex:
            raise RuntimeError(
                f"Ollama error: {ex}"
            ) from ex

        data: dict = response.json()

        return data.get(
            "response",
            "",
        ).strip()


__all__ = [
    "OllamaProvider",
]