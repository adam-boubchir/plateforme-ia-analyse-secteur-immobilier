import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

class Settings:

    IMMO_AI_SERVER = os.getenv("IMMO_AI_SERVER")
    IMMO_AI_DATABASE = os.getenv("IMMO_AI_DATABASE")

    MINISTRY_SERVER = os.getenv("MINISTRY_SERVER")
    MINISTRY_DATABASE = os.getenv("MINISTRY_DATABASE")

    SQL_USERNAME = os.getenv("SQL_USERNAME")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()