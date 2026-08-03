from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.model_config import (
    ModelConfigEntity,
)
from app.models.agent_models import (
    ModelConfig,
)

__all__ = (
    "ModelManager",
)


class ModelManager:
    """
    Responsible for loading AI model configurations.

    Responsibilities
    ----------------
    - Load active model configurations from the database.
    - Cache configurations in memory.
    - Refresh cached configurations.
    """

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        self._db = db
        self._cache: dict[str, ModelConfig] = {}

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get(
        self,
        *,
        agent_name: str,
    ) -> ModelConfig:
        """
        Return the active configuration for an agent.

        Args:
            agent_name:
                Name of the AI agent.

        Returns:
            Active model configuration.

        Raises:
            ValueError:
                If no active configuration exists.
        """

        if agent_name not in self._cache:
            configuration = self._load_active_model(
                agent_name=agent_name,
            )

            self._cache[agent_name] = configuration

        configuration = self._cache[agent_name]

        return configuration

    def has_model(
        self,
        *,
        agent_name: str,
    ) -> bool:
        """
        Check whether an active model exists.

        Args:
            agent_name:
                Name of the AI agent.

        Returns:
            True if an active model exists, otherwise False.
        """

        try:
            self.get(
                agent_name=agent_name,
            )

            exists = True

        except ValueError:
            exists = False

        return exists

    def refresh(
        self,
        *,
        agent_name: str,
    ) -> ModelConfig:
        """
        Reload a cached model configuration.

        Args:
            agent_name:
                Name of the AI agent.

        Returns:
            Reloaded model configuration.
        """

        self._cache.pop(
            agent_name,
            None,
        )

        configuration = self.get(
            agent_name=agent_name,
        )

        return configuration

    def clear_cache(
        self,
    ) -> None:
        """
        Clear every cached model configuration.
        """

        self._cache.clear()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_active_model(
        self,
        *,
        agent_name: str,
    ) -> ModelConfig:
        """
        Load the active model configuration from the database.

        Args:
            agent_name:
                Name of the AI agent.

        Returns:
            Active model configuration.

        Raises:
            ValueError:
                If no active model exists.
        """

        statement = (
            select(
                ModelConfigEntity,
            )
            .where(
                ModelConfigEntity.agent_name == agent_name,
            )
            .where(
                ModelConfigEntity.is_active,
            )
        )

        entity = self._db.scalar(
            statement,
        )

        if entity is None:
            raise ValueError(
                f"No active model configured for agent '{agent_name}'.",
            )

        configuration = self._to_model(
            entity=entity,
        )

        return configuration

    @staticmethod
    def _to_model(
        *,
        entity: ModelConfigEntity,
    ) -> ModelConfig:
        """
        Convert a database entity into a domain model.

        Args:
            entity:
                ORM entity.

        Returns:
            Domain model configuration.
        """

        configuration = ModelConfig(
            agent_name=entity.agent_name,
            provider=entity.provider,
            model_name=entity.model_name,
            api_key_alias=entity.api_key_alias,
            api_base_url=entity.api_base_url,
            deployment_name=entity.deployment_name,
            system_prompt=entity.system_prompt,
            temperature=float(
                entity.temperature,
            ),
            top_p=float(
                entity.top_p,
            ),
            frequency_penalty=float(
                entity.frequency_penalty,
            ),
            presence_penalty=float(
                entity.presence_penalty,
            ),
            timeout_seconds=entity.timeout_seconds,
            max_tokens=entity.max_tokens,
            is_active=entity.is_active,
        )

        return configuration