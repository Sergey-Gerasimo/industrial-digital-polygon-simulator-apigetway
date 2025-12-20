from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get(f"{settings.API_PREFIX}/")
async def root():
    return {
        "message": "Industrial Digital Polygon Simulator API Gateway",
        "version": settings.VERSION,
        "docs": f"{settings.API_PREFIX}/docs",
        "redoc": f"{settings.API_PREFIX}/redoc",
    }


@app.get(f"{settings.API_PREFIX}/health")
async def health_check():
    return {"status": "healthy"}
