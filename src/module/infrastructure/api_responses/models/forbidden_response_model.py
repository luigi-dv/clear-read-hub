from pydantic import BaseModel


class ForbiddenResponse(BaseModel):
    status: str = "forbidden"
    message: str = "Forbidden"
    errors: dict = None
