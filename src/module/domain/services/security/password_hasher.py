# In your domain layer
from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """
    Password Hasher Interface
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass
