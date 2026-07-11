import os

from openai import AzureOpenAI

from app.database.config import settings

from app.models.agent_models import ModelConfig

from app.services.providers.base_provider import BaseProvider


class AzureProvider(BaseProvider):

    def generate(
        self,
        config: ModelConfig,
        prompt: str,
    ) -> str:

        api_key = os.getenv(config.api_key_alias)

        if not api_key:
            raise ValueError(
                f"Environment variable '{config.api_key_alias}' not found."
            )

        client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=config.api_base_url,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )
        print("===== AZURE CONFIG =====")
        print("Provider :", config.provider)
        print("Model :", config.model_name)
        print("Deployment :", config.deployment_name)
        print("Endpoint :", config.api_base_url)
        print("API Alias :", config.api_key_alias)
        print("========================")

        response = client.chat.completions.create(

            model=config.deployment_name,

            messages=[

                {
                    "role": "system",
                    "content": config.system_prompt or ""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],


            max_completion_tokens=config.max_tokens,


        )

        return response.choices[0].message.content.strip()