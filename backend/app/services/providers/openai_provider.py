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
    OpenAI Provider.

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

        client = self._create_client(
            config
        )

        self._print_configuration(
            config
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

            return (

                response

                .choices[0]

                .message

                .content

                .strip()

            )

        except OpenAIError as ex:

            raise RuntimeError(

                f"OpenAI error: {str(ex)}"

            ) from ex

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

        api_key = os.getenv(
            config.api_key_alias
        )

        if not api_key:

            raise ValueError(

                f"Environment variable '{config.api_key_alias}' was not found."

            )

        return OpenAI(

            api_key=api_key,

            base_url=config.api_base_url or None,

        )

    def _print_configuration(
        self,
        config: ModelConfig,
    ) -> None:
        """
        Display OpenAI configuration.
        """

        print()

        print("=" * 100)

        print("OPENAI CONFIGURATION")

        print("=" * 100)

        print(
            f"Provider      : {config.provider}"
        )

        print(
            f"Model         : {config.model_name}"
        )

        print(
            f"Base URL      : {config.api_base_url}"
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