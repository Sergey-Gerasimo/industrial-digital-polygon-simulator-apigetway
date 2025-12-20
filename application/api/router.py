from fastapi import APIRouter

from app.api.auth.endpoints import router as auth_router
# Импортируем другие роутеры, когда они будут созданы
# from app.api.users.endpoints import router as users_router
# from app.api.rooms.endpoints import router as rooms_router
# from app.api.invites.endpoints import router as invites_router

api_router = APIRouter()

api_router.include_router(auth_router)

# Другие роутеры будут добавлены позже
# api_router.include_router(users_router)
# api_router.include_router(rooms_router)
# api_router.include_router(invites_router)