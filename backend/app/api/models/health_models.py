from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health endpoint response.
    """

    status: str