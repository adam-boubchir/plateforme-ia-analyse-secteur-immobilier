from openai import OpenAI

from app.services.providers.base_provider import (
    BaseProvider
)


class OpenAIProvider(BaseProvider):

    def __init__(
        self,
        api_key: str
    ):

        self.client = OpenAI(
            api_key=api_key
        )

    def generate(
        self,
        config: ModelConfig,
        prompt: str
    ) -> str:

        messages = []

        if config.system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": config.system_prompt
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = self.client.chat.completions.create(

            model=config.model_name,

            messages=messages,

            temperature=config.temperature,

            max_tokens=config.max_tokens,

            top_p=config.top_p,

            frequency_penalty=config.frequency_penalty,

            presence_penalty=config.presence_penalty
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )