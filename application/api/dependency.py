from config.logger_config import logger
from logging import Logger

from services.auth_service import AbstractAuthService


def get_logger() -> Logger:
    return logger


def get_auth_service() -> AbstractAuthService:
    """Пока не нужен. Не надо его использовать."""
    return AbstractAuthService()
