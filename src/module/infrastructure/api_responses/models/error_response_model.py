from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: str = "An error occurred"
    message: str = "Not Found"
    errors: dict = None
