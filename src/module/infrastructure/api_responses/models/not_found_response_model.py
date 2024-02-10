from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    status: str = "not_found"
    message: str = "Not Found"
    data: dict = None
