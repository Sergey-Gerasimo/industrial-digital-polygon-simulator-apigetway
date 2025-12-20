import sys
from loguru import logger


class LoggerConfig:
    """Logger configuration using loguru."""

    def __init__(
        self,
        log_level: str = "INFO",
        log_format: str | None = None,
    ) -> None:
        self.log_level = log_level
        self.log_format = log_format or (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    def configure(self) -> None:
        """Configure loguru logger."""
        logger.remove()

        logger.add(
            sys.stderr,
            format=self.log_format,
            level=self.log_level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

        logger.info(f"Logger configured with level: {self.log_level}")


__all__ = ["LoggerConfig", "logger"]
