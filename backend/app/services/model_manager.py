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
    Responsible for loading AI model configurations
    from the database.

    Features
    --------
    • Cache configurations
    • Load active models
    • Support multiple AI agents
    • Ready for fallback strategies
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db: Session = db

        self._cache: dict[str, ModelConfig] = {}

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get(
        self,
        agent_name: str,
    ) -> ModelConfig:
        """
        Return the active configuration of an agent.
        """

        if agent_name in self._cache:
            return self._cache[agent_name]

        config: ModelConfig = self._load_active_model(
            agent_name=agent_name,
        )

        self._cache[agent_name] = config

        return config
    
    def has_model(
        self,
        agent_name: str,
    ) -> bool:
        """
        Return True if the agent has an active model.
        """

        try:

            self.get(
                agent_name=agent_name,
            )

            return True

        except ValueError:

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
            agent_name=agent_name,
        )

    def refresh_cache(
        self,
    ) -> None:
        """
        Clear every cached configuration.
        """

        self._cache.clear()

    def clear_cache(self) -> None:
        """
        Clear every cached configuration.
        """

        self._cache.clear()
    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_active_model(
        self,
        agent_name: str,
    ) -> ModelConfig:
        """
        Load the active model configuration
        from the database.
        """

        entity: ModelConfigEntity | None = self.db.scalar(
            select(ModelConfigEntity)
            .where(
                ModelConfigEntity.agent_name == agent_name,
            )
            .where(
                ModelConfigEntity.is_active,
            )
        )

        if entity is None:
            raise ValueError(
                f"No active model configured for '{agent_name}'."
            )

        return self._to_model(
            entity=entity,
        )

    @staticmethod
    def _to_model(
        entity: ModelConfigEntity,
    ) -> ModelConfig:
        """
        Convert an ORM entity into a ModelConfig.
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

    __all__ = [
        "ModelManager",
    ]