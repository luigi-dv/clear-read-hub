import io
from datetime import datetime


class FileData:
    """
    Represents the data of a file as a domain entity.

    Attributes:
        - `name` (str): The file name
        - `data` (io.BytesIO): The file content represented as a BytesIO object.
        - `metadata` (dict[str, str]): The file metadata
        - `file_type` (str): The file type/extension
        - `size` (int): The file size
        - `creation_time` (datetime): The file creation time
    """

    def __init__(
        self,
        name: str,
        data: list[io.BytesIO],
        metadata: dict[str, str],
        file_type: str,
        size: int,
        creation_time: datetime,
    ):
        """
        Initialize the FileData entity.

        Parameters:
            - `name` (str): The file name
            - `data` (io.BytesIO): The file content represented as a BytesIO object.
            - `metadata` (dict[str, str]): The file metadata
            - `file_type` (str): The file type/extension
            - `size` (int): The file size
            - `creation_time` (datetime): The file creation time
        """
        self._name = name
        self._data = data
        self._metadata = metadata
        self._file_type = file_type
        self._size = size
        self._creation_time = creation_time

    @property
    def name(self) -> str:
        """
        Get the file name.

        Returns:
            - str: The file name.
        """
        return self._name

    @property
    def data(self) -> list[io.BytesIO]:
        """
        Get the file content as a BytesIO object.

        Returns:
            - io.BytesIO: The file content.
        """
        return self._data

    @property
    def metadata(self) -> dict[str, str]:
        """
        Get the file metadata.

          Returns:
              - dict[str, str]: The file metadata.
        """
        return self._metadata

    @property
    def file_type(self) -> str:
        """
        Get the file type/extension.

          Returns:
              - str: The file type.
        """
        return self._file_type

    @property
    def size(self) -> int:
        """
        Get the file size.

          Returns:
              - int: The file size.
        """
        return self._size

    @property
    def creation_time(self) -> datetime:
        """
        Get the file creation time.

          Returns:
              - datetime: The file creation time.
        """
        return self._creation_time
