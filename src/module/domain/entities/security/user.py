from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class User(BaseModel):
    """
    User entity represents the user of the application
    """

    id: Optional[UUID] = Field(default_factory=uuid4, alias="_id")
    email: str
    password: str
    disabled: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}
