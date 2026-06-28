from openai import OpenAI

from app.database.config import settings

from app.models.agent_models import ModelConfig

from app.services.providers.base_provider import (
    BaseProvider
)


class OpenAIProvider(BaseProvider):
    """
    OpenAI implementation.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate(
        self,
        config: ModelConfig,
        prompt: str
    ) -> str:

        response = self.client.chat.completions.create(

            model=config.model_name,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=config.temperature,

            max_tokens=config.max_tokens,
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )