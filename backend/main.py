from fastapi import FastAPI

app = FastAPI(
    title="IMMO AI API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "IMMO AI Backend is running"
    }
from app.database.config import settings

print(settings.IMMO_AI_DATABASE)