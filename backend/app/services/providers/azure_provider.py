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
    Azure OpenAI Provider.

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

        client = self._create_client(
            config
        )

        self._print_configuration(
            config
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

                max_completion_tokens=config.max_tokens,

            )

            return (
                response
                .choices[0]
                .message.content
                .strip()
            )

        except OpenAIError as ex:

            raise RuntimeError(
                f"Azure OpenAI error: {str(ex)}"
            ) from ex

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_client(
        self,
        config: ModelConfig,
    ) -> AzureOpenAI:
        """
        Create Azure OpenAI client.
        """

        api_key = os.getenv(
            config.api_key_alias
        )

        if not api_key:

            raise ValueError(

                f"Environment variable '{config.api_key_alias}' was not found."

            )

        return AzureOpenAI(

            api_key=api_key,

            azure_endpoint=config.api_base_url,

            api_version=settings.AZURE_OPENAI_API_VERSION,

        )

    def _print_configuration(
        self,
        config: ModelConfig,
    ) -> None:
        """
        Print Azure configuration.
        """

        print()

        print("=" * 100)

        print("AZURE OPENAI CONFIGURATION")

        print("=" * 100)

        print(
            f"Provider      : {config.provider}"
        )

        print(
            f"Model         : {config.model_name}"
        )

        print(
            f"Deployment    : {config.deployment_name}"
        )

        print(
            f"Endpoint      : {config.api_base_url}"
        )

        print(
            f"API Key Alias : {config.api_key_alias}"
        )

        print(
            f"Temperature   : {config.temperature}"
        )

        print(
            f"Top P         : {config.top_p}"
        )

        print(
            f"Max Tokens    : {config.max_tokens}"
        )

        print("=" * 100)

        print()