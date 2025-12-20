from typing import Optional
from datetime import datetime
import uuid
from fastapi import Depends, HTTPException, status

from models.user import User, UserCreate, UserInDB


class AbstractAuthService:
    def register_user(self, username: str, password: str) -> User:
        raise NotImplementedError

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        raise NotImplementedError

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    def get_current_user(self, token: str) -> User:
        raise NotImplementedError

    def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> bool:
        raise NotImplementedError
