from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from datetime import datetime, timedelta

from app.models.user import (
    AuthRequest,
    TokenResponse,
    RefreshTokenRequest,
    SuccessResponse,
    ChangePasswordRequest,
    Token,
    User
)
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.core.config import settings
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registrate", response_model=TokenResponse)
async def register(
    auth_data: AuthRequest,
    auth_service: AuthService = Depends()
) -> Any:
    """Регистрация нового пользователя"""
    user = await auth_service.register_user(
        username=auth_data.username,
        password=auth_data.password
    )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.user_id, "username": user.username}
    )
    
    return TokenResponse(
        access_token=Token(
            token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        refresh_token=Token(
            token=refresh_token,
            expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        ),
        user=user
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    auth_data: AuthRequest,
    auth_service: AuthService = Depends()
) -> Any:
    """Вход в систему"""
    user = await auth_service.authenticate_user(
        username=auth_data.username,
        password=auth_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.user_id, "username": user.username}
    )
    
    return TokenResponse(
        access_token=Token(
            token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        refresh_token=Token(
            token=refresh_token,
            expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        ),
        user=user
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends()
) -> Any:
    """Обновление токена доступа"""
    payload = verify_token(refresh_data.refresh_token.token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен"
        )
    
    user_id = payload.get("sub")
    user = await auth_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.user_id, "username": user.username}
    )
    
    return TokenResponse(
        access_token=Token(
            token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        refresh_token=Token(
            token=refresh_token,
            expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        ),
        user=user
    )


@router.post("/logout", response_model=SuccessResponse)
async def logout(
    current_user: User = Depends(auth_service.get_current_user)
) -> Any:
    """Выход из системы"""
    # В реальном приложении здесь можно добавить токен в blacklist
    return SuccessResponse(message="Успешный выход из системы")


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(auth_service.get_current_user)
) -> Any:
    """Получение информации о текущем пользователе"""
    return current_user


@router.post("/verify-token", response_model=SuccessResponse)
async def verify_user_token(
    current_user: User = Depends(auth_service.get_current_user)
) -> Any:
    """Проверка валидности токена"""
    return SuccessResponse(message="Токен валиден")


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(auth_service.get_current_user),
    auth_service: AuthService = Depends()
) -> Any:
    """Изменение пароля пользователя"""
    await auth_service.change_password(
        user_id=current_user.user_id,
        current_password=password_data.current_password,
        new_password=password_data.new_password
    )
    
    return SuccessResponse(message="Пароль успешно изменен")