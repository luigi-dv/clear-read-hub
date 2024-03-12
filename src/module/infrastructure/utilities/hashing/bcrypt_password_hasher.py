from src.module.domain.services.security.password_hasher import PasswordHasher
from src.module.infrastructure.utilities.hashing.password import get_password_hash


class BcryptPasswordHasher(PasswordHasher):
    """
    Bcrypt Password Hasher
    """

    def hash_password(self, password: str) -> str:
        """
        Hash the password

        :param password: The password
        :return: The hashed password
        """
        return get_password_hash(password)
