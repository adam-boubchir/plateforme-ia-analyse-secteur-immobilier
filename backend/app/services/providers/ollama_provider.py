import requests

from app.models.agent_models import (
    ModelConfig,
)

from app.services.providers.base_provider import (
    BaseProvider,
)


class OllamaProvider(BaseProvider):
    """
    Ollama Provider.

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

        self._print_configuration(
            config
        )

        payload = {

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

            data = response.json()

            return data.get(
                "response",
                "",
            ).strip()

        except requests.RequestException as ex:

            raise RuntimeError(

                f"Ollama error: {str(ex)}"

            ) from ex

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _print_configuration(
        self,
        config: ModelConfig,
    ) -> None:

        print()

        print("=" * 100)

        print("OLLAMA CONFIGURATION")

        print("=" * 100)

        print(
            f"Provider    : {config.provider}"
        )

        print(
            f"Model       : {config.model_name}"
        )

        print(
            f"Endpoint    : {config.api_base_url}"
        )

        print(
            f"Temperature : {config.temperature}"
        )

        print(
            f"Top P       : {config.top_p}"
        )

        print(
            f"Timeout     : {config.timeout_seconds}"
        )

        print("=" * 100)

        print()