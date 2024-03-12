from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from src.module.domain.entities.security.user import User
from src.module.infrastructure.persistence.db_context import DatabaseContext
from src.module.infrastructure.configuration.files_loader import load_responses
from src.module.domain.repositories.security.user_repository import IUserRepository


class UserRepository(IUserRepository):
    """
    User repository implementation
    """

    def __init__(self):
        self.context = DatabaseContext()
        self.database = self.context.get_database()
        self.collection = self.database.users
        # Create index for email field
        self.collection.create_index([("email", 1)], unique=True)
        self.responses = load_responses()

    async def find_by_id(self, user_id: str) -> User:
        document = self.collection.find_one({"_id": user_id})
        if document:
            return User(**document)
        else:
            raise HTTPException(
                status_code=404,
                detail=self.responses.module.domain.error.operation_failed,
            )

    async def find_by_email(self, email: str) -> User:
        try:
            document = self.collection.find_one({"email": email})
            if document:
                return User(**document)
            else:
                raise HTTPException(
                    status_code=404,
                    detail=self.responses.module.domain.error.operation_failed,
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=self.responses.module.domain.error.operation_failed,
            )

    async def create(self, user: User) -> User:
        try:
            result = self.collection.insert_one(user.dict(by_alias=True))
            if result.acknowledged:
                user.id = result.inserted_id
                return user
            else:
                raise HTTPException(
                    status_code=500,
                    detail=self.responses.module.domain.operation_failed,
                )
        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=400,
                detail="Duplicate key error creating user, email already exists",
            )

    async def update(self, user: User) -> User:
        try:
            result = self.collection.update_one(
                {"_id": user.id}, {"$set": user.dict(by_alias=True)}
            )
            if result.modified_count > 0:
                return user
            else:
                raise HTTPException(
                    status_code=404, detail="User not found or not modified"
                )
        except DuplicateKeyError:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=self.responses.module.domain.error.operation_failed,
            )

    async def delete(self, user_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": user_id})
            if result.deleted_count > 0:
                return True
            else:
                raise HTTPException(
                    status_code=404, detail="User not found or not deleted"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=self.responses.module.domain.error.operation_failed,
            )
