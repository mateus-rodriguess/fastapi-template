from fastapi import APIRouter, Security

from app.api.api_v1.deps import reusable_oauth2
from app.api.api_v1.endpoints import auth, health, users

api_router = APIRouter()

api_router.prefix = "/api/v1"

api_router.include_router(router=auth.router, dependencies=None, tags=["auth"])
api_router.include_router(users.router_unauthenticated, tags=["users"])

api_router.dependencies = [
    Security(dependency=reusable_oauth2, use_cache=True)
]
api_router.include_router(users.router, tags=["users"])
api_router.include_router(health.router, tags=["health"])
