from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum


get_current_time = lambda: datetime.now(timezone.utc)


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    user_role: UserRole = UserRole.USER
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    user_role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class Token(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_in: int


class TokenResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    timestamp: datetime = Field(default_factory=get_current_time)
    access_token: Token
    refresh_token: Token
    user: User


class AuthRequest(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: Token


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    timestamp: datetime = Field(default_factory=get_current_time)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    user_role: UserRole = UserRole.USER
    is_active: bool = True


class GetAllUsersRequest(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)


class GetAllUsersResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=get_current_time)
    users: list[User]
    total_count: int


class ChangeUserRequest(BaseModel):
    user_id: str
    user_role: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
