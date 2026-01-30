from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.schemas.user import Token
from app.utils.exceptions import UnauthorizedException, BadRequestException

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login"""
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException("Incorrect username or password")
    
    if not user.is_active:
        raise BadRequestException("Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
