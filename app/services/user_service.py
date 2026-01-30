from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.user import User
from app.utils.exceptions import NotFoundException, ConflictException

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def create_user(self, user_create: UserCreate) -> UserResponse:
        # Check if user already exists
        if self.repository.get_by_email(user_create.email):
            raise ConflictException("Email already registered")
        
        if self.repository.get_by_username(user_create.username):
            raise ConflictException("Username already taken")
        
        user = self.repository.create(user_create)
        return UserResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_multi(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        updated_user = self.repository.update(user, user_update)
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        self.repository.delete(user)
