from src.module.domain.entities.files.data.file_data import FileData


class FileDataExtracted(FileData):
    """
    Represents the data and text extracted of a file as a domain entity.

      Attributes:
        - `extracted_text` (list[str]): The text extracted from the file.
    """

    def __init__(self, file_data: FileData, extracted_text: list[str]):
        super().__init__(
            name=file_data.name,
            data=file_data.data,
            metadata=file_data.metadata,
            file_type=file_data.file_type,
            size=file_data.size,
            creation_time=file_data.creation_time,
        )
        self._extracted_text = extracted_text

    @property
    def extracted_text(self) -> list[str]:
        """
        Get the file's extracted text.

        Returns:
            - list[str[: The file's extracted text.
        """
        return self._extracted_text
