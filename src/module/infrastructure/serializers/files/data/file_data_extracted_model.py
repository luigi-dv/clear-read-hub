from pydantic import BaseModel
from datetime import datetime


class FileDataExtractedModel(BaseModel):
    name: str
    metadata: dict
    file_type: str
    size: int
    creation_time: datetime
    extracted_text: list[str]
