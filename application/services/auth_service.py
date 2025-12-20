from typing import Optional
from datetime import datetime
import uuid
from fastapi import Depends, HTTPException, status

from app.models.user import User, UserCreate, UserInDB
from app.core.security import verify_password, get_password_hash


class AuthService:
    def __init__(self):
        self.users = {}
        self._initialize_test_users()
    
    def _initialize_test_users(self):
        # Тестовые пользователи
        test_users = [
            UserCreate(
                username="admin",
                password="admin123",
                user_role="admin",
                is_active=True
            ),
            UserCreate(
                username="user1",
                password="user123",
                user_role="user",
                is_active=True
            ),
            UserCreate(
                username="user2",
                password="user123",
                user_role="user",
                is_active=True
            ),
        ]
        
        for user_data in test_users:
            user_id = str(uuid.uuid4())
            hashed_password = get_password_hash(user_data.password)
            
            user = UserInDB(
                user_id=user_id,
                username=user_data.username,
                user_role=user_data.user_role,
                is_active=user_data.is_active,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.users[user_id] = user
            self.users[user.username] = user  # Для поиска по username
    
    async def register_user(self, username: str, password: str) -> User:
        # Проверка существования пользователя
        if username in self.users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )
        
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(password)
        
        user = UserInDB(
            user_id=user_id,
            username=username,
            user_role="user",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.users[user_id] = user
        self.users[username] = user
        
        return user
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.users.get(username)
        if not user:
            return None
        
        # В реальном приложении здесь была бы проверка хеша пароля
        # Для демо просто проверяем, что пароль не пустой
        if not password:
            return None
        
        return user
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    async def get_current_user(self, token: str) -> User:
        # В реальном приложении здесь была бы проверка JWT токена
        # Пока испльзуеи заглушку для пробной версии
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Требуется аутентификация"
            )
        
        for user_id, user in self.users.items():
            if isinstance(user, UserInDB):
                return user
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    async def change_password(self, user_id: str, current_password: str, new_password: str):
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        if not current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный текущий пароль"
            )
        
        return True


def get_auth_service() -> AuthService:
    return AuthService()