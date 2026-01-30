from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def create_user(self, user_create: UserCreate) -> UserResponse:
        # Check if user already exists
        if self.repository.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.repository.get_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        user = self.repository.create(user_create)
        return UserResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_multi(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        updated_user = self.repository.update(user, user_update)
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        self.repository.delete(user)
