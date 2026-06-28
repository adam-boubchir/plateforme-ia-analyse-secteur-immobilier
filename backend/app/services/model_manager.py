from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.model_config import (
    ModelConfigEntity
)

from app.models.agent_models import (
    ModelConfig
)


class ModelManager:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

        self._cache: dict[
            str,
            ModelConfig
        ] = {}

    def get(
        self,
        agent_name: str
    ) -> ModelConfig:

        if agent_name in self._cache:

            return self._cache[agent_name]

        entity = self.db.scalar(

            select(ModelConfigEntity)

            .where(
                ModelConfigEntity.agent_name
                == agent_name
            )

            .where(ModelConfigEntity.is_active)

        )

        if entity is None:

            raise ValueError(
                f"No active model configured for "
                f"'{agent_name}'."
            )

        config = ModelConfig(

            agent_name=entity.agent_name,

            provider=entity.provider,

            model_name=entity.model_name,

            api_key_alias=entity.api_key_alias,

            api_base_url=entity.api_base_url,

            deployment_name=entity.deployment_name,

            system_prompt=entity.system_prompt,

            temperature=float(
                entity.temperature
            ),

            top_p=float(
                entity.top_p
            ),

            frequency_penalty=float(
                entity.frequency_penalty
            ),

            presence_penalty=float(
                entity.presence_penalty
            ),

            timeout_seconds=entity.timeout_seconds,

            max_tokens=entity.max_tokens,

            is_active=entity.is_active

        )

        self._cache[agent_name] = config

        return config

    def refresh_cache(self) -> None:

        self._cache.clear()

    def clear_cache(self) -> None:

        self._cache.clear()