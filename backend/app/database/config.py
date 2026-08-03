from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

__all__ = (
    "Settings",
    "settings",
)


# ==========================================================
# ENVIRONMENT
# ==========================================================

_BASE_DIR = Path(__file__).resolve().parents[2]

_ENV_FILE = _BASE_DIR / ".env"

load_dotenv(
    dotenv_path=_ENV_FILE,
)


class Settings:
    """
    Central application configuration.

    Environment variables are loaded from the project's `.env` file
    and exposed as strongly-typed attributes.
    """

    def __init__(
        self,
    ) -> None:
        # ======================================================
        # APPLICATION DATABASE
        # ======================================================

        self.IMMO_AI_SERVER = self._get_env(
            key="IMMO_AI_SERVER",
        )

        self.IMMO_AI_DATABASE = self._get_env(
            key="IMMO_AI_DATABASE",
        )

        # ======================================================
        # MINISTRY DATABASE
        # ======================================================

        self.MINISTRY_SERVER = self._get_env(
            key="MINISTRY_SERVER",
        )

        self.MINISTRY_DATABASE = self._get_env(
            key="MINISTRY_DATABASE",
        )

        # ======================================================
        # SQL SERVER
        # ======================================================

        self.SQL_USERNAME = self._require_env(
            key="SQL_USERNAME",
        )

        self.SQL_PASSWORD = self._require_env(
            key="SQL_PASSWORD",
        )

        # ======================================================
        # AZURE OPENAI
        # ======================================================

        self.AZURE_OPENAI_API_VERSION = self._require_env(
            key="AZURE_OPENAI_API_VERSION",
        )

    # ======================================================
    # PRIVATE
    # ======================================================

    @staticmethod
    def _get_env(
        *,
        key: str,
    ) -> str | None:
        """
        Return an optional environment variable.

        Args:
            key: Environment variable name.

        Returns:
            The environment variable value, or None if not defined.
        """

        return os.getenv(key)

    @staticmethod
    def _require_env(
        *,
        key: str,
    ) -> str:
        """
        Return a required environment variable.

        Args:
            key: Environment variable name.

        Returns:
            The environment variable value.

        Raises:
            RuntimeError:
                If the variable is missing or empty.
        """

        value = os.getenv(key)

        if not value:
            raise RuntimeError(
                f"Missing required environment variable '{key}'."
            )

        return value


settings = Settings()