from pydantic import BaseModel


class SuccessResponseModel(BaseModel):
    status: str = "success"
    message: str = "Success"
    data: dict = None
