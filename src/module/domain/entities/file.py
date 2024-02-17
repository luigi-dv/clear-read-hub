from fastapi import UploadFile
from src.module.domain.value_objects.FileSize import FileSize
from src.module.domain.value_objects.FileType import FileType


class File:
    def __init__(self, upload_file: UploadFile):
        self.filename = upload_file.filename
        self.content_type = upload_file.content_type
        self.content = upload_file.file

    @property
    async def size(self) -> FileSize:
        self.content.seek(0, 2)  # Seek to the end of the file
        size = self.content.tell()  # Get the current position in the file
        self.content.seek(0)  # Seek back to the beginning of the file
        return FileSize(size)

    @property
    async def type(self) -> FileType:
        return FileType(self.content_type.split("/")[-1])

    async def validate(self):
        # Validate file size
        try:
            FileSize((await self.size).size)
        except ValueError as e:
            raise e

        # Validate file type
        try:
            FileType(self.content_type.split("/")[-1])
        except ValueError as e:
            raise e
