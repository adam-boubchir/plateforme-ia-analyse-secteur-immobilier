from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.model_config import (
    ModelConfigEntity,
)

from app.models.agent_models import (
    ModelConfig,
)


class ModelManager:
    """
    Central manager responsible for retrieving AI model
    configurations from the database.

    Features
    --------
    • Cache model configurations
    • Load active models
    • Support multiple AI agents
    • Ready for fallback strategies
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self._cache: dict[
            str,
            ModelConfig,
        ] = {}

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get(
        self,
        agent_name: str,
    ) -> ModelConfig:
        """
        Return the active configuration for one agent.
        """

        if agent_name in self._cache:

            return self._cache[
                agent_name
            ]

        config = self._load_active_model(
            agent_name
        )

        self._cache[
            agent_name
        ] = config

        return config

    def has_model(
        self,
        agent_name: str,
    ) -> bool:
        """
        Check whether an active configuration exists.
        """

        try:

            self.get(
                agent_name
            )

            return True

        except Exception:

            return False

    def refresh(
        self,
        agent_name: str,
    ) -> ModelConfig:
        """
        Reload one configuration.
        """

        self._cache.pop(
            agent_name,
            None,
        )

        return self.get(
            agent_name
        )

    def refresh_cache(
        self,
    ) -> None:
        """
        Reload every configuration.
        """

        self._cache.clear()

    def clear_cache(
        self,
    ) -> None:
        """
        Alias.
        """

        self.refresh_cache()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_active_model(
        self,
        agent_name: str,
    ) -> ModelConfig:
        """
        Load the active model from the database.
        """

        entity = self.db.scalar(

            select(
                ModelConfigEntity
            )

            .where(
                ModelConfigEntity.agent_name
                == agent_name
            )

            .where(
                ModelConfigEntity.is_active
            )

        )

        if entity is None:

            raise ValueError(

                f"No active model configured for '{agent_name}'."

            )

        return self._to_model(
            entity
        )

    def _to_model(
        self,
        entity: ModelConfigEntity,
    ) -> ModelConfig:
        """
        Convert ORM entity into ModelConfig.
        """

        return ModelConfig(

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

            is_active=entity.is_active,

        )