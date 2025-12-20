from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from datetime import datetime, timedelta

from models.user import (
    AuthRequest,
    TokenResponse,
    RefreshTokenRequest,
    SuccessResponse,
    ChangePasswordRequest,
    Token,
    User,
)

from api.dependency import get_logger, Logger, get_auth_service
from services.auth_service import AbstractAuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registrate", response_model=TokenResponse)
async def register(
    auth_data: AuthRequest,
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:
    """
    Регистрация нового пользователя
    """
    logger.info("Registrating new user")
    logger.warning("Not implemented registration. Just return test data.")

    return TokenResponse(
        access_token=Token(token="test_token", expires_in=1000),
        refresh_token=Token(
            token="test_refresh_token",
            expires_in=1000,
        ),
        user=User(
            username="test_username",
            user_role="test_user_role",
            user_id="test_user_id",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    auth_data: AuthRequest,
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:
    """Вход в систему"""
    logger.info("Logging in user")
    logger.warning("Not implemented login. Just return test data.")

    if auth_data.username == "exist_username":
        return SuccessResponse(success=False, message="User not found")

    return TokenResponse(
        access_token=Token(token="test_token", expires_in=1000),
        refresh_token=Token(
            token="test_refresh_token",
            expires_in=1000,
        ),
        user=User(
            username="test_username",
            user_role="test_user_role",
            user_id="test_user_id",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:
    """Обновление токена доступа"""
    logger.info("Refreshing token")
    logger.warning("Not implemented refresh token. Just return test data.")
    return TokenResponse(
        access_token=Token(token="test_token", expires_in=1000),
        refresh_token=Token(
            token="test_refresh_token",
            expires_in=1000,
        ),
        user=User(
            username="test_username",
            user_role="test_user_role",
            user_id="test_user_id",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    )


@router.post("/logout", response_model=SuccessResponse)
async def logout(
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:
    """Выход из системы"""
    logger.info("Logging out user")
    logger.warning("Not implemented logout. Just return test data.")
    # В реальном приложении здесь можно добавить токен в blacklist
    return SuccessResponse(message="Успешный выход из системы")


@router.get("/me", response_model=User)
async def get_current_user_info(
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:

    logger.info("Getting current user info")
    logger.warning("Not implemented get current user info. Just return test data.")
    return User(
        username="test_username",
        user_role="test_user_role",
        user_id="test_user_id",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.post("/verify-token", response_model=SuccessResponse)
async def verify_user_token(
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:
    """Проверка валидности токена"""
    logger.info("Verifying user token")
    logger.warning("Not implemented verify user token. Just return test data.")
    return SuccessResponse(message="Токен валиден")


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    auth_service: AbstractAuthService = Depends(get_auth_service),
    logger: Logger = Depends(get_logger),
) -> Any:
    logger.info("Changing password")
    logger.warning("Not implemented change password. Just return test data.")
    return SuccessResponse(message="Пароль успешно изменен")
