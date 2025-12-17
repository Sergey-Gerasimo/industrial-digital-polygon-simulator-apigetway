import uvicorn
from fastapi import FastAPI

from config import EnvConfig, LoggerConfig, logger

env = EnvConfig()
LoggerConfig(log_level=env.LOG_LEVEL, log_format=env.LOG_FORMAT).configure()

app = FastAPI(
    title=env.APP_NAME,
    debug=env.DEBUG,
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info(f"Starting {env.APP_NAME} on {env.HOST}:{env.PORT}")
    uvicorn.run(
        "application.main:app",
        host=env.HOST,
        port=env.PORT,
        reload=env.DEBUG,
    )
