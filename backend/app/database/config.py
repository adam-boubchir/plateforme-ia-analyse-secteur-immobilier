import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(
    dotenv_path=BASE_DIR / ".env",
)


class Settings:
    """
    Application configuration loaded from environment variables.
    """

    def __init__(self) -> None:

        # ==========================================================
        # APPLICATION DATABASE
        # ==========================================================

        self.IMMO_AI_SERVER: str | None = os.getenv(
            "IMMO_AI_SERVER",
        )

        self.IMMO_AI_DATABASE: str | None = os.getenv(
            "IMMO_AI_DATABASE",
        )

        # ==========================================================
        # MINISTRY DATABASE
        # ==========================================================

        self.MINISTRY_SERVER: str | None = os.getenv(
            "MINISTRY_SERVER",
        )

        self.MINISTRY_DATABASE: str | None = os.getenv(
            "MINISTRY_DATABASE",
        )

        # ==========================================================
        # SQL SERVER
        # ==========================================================

        self.SQL_USERNAME: str | None = os.getenv(
            "SQL_USERNAME",
        )

        self.SQL_PASSWORD: str | None = os.getenv(
            "SQL_PASSWORD",
        )

        # ==========================================================
        # AZURE OPENAI
        # ==========================================================

        self.AZURE_OPENAI_API_KEY: str | None = os.getenv(
            "AZURE_OPENAI_API_KEY",
        )

        self.AZURE_OPENAI_ENDPOINT: str | None = os.getenv(
            "AZURE_OPENAI_ENDPOINT",
        )

        self.AZURE_OPENAI_API_VERSION: str | None = os.getenv(
            "AZURE_OPENAI_API_VERSION",
        )

        self.AZURE_OPENAI_DEPLOYMENT: str | None = os.getenv(
            "AZURE_OPENAI_DEPLOYMENT",
        )


settings = Settings()


__all__ = [
    "Settings",
    "settings",
]