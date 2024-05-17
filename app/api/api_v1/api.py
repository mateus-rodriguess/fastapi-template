from fastapi import APIRouter, Depends, Security
from fastapi_limiter.depends import RateLimiter

from app.api.api_v1.deps import reusable_oauth2
from app.api.api_v1.endpoints import auth, health, users

api_router = APIRouter()

api_router.prefix = "/api/v1"

time = 9_999_999  # Danger

api_router.include_router(
    router=auth.router,
    dependencies=[Depends(RateLimiter(times=time, seconds=5))],
    tags=["auth"],
)
api_router.include_router(
    users.router_unauthenticated,
    dependencies=[Depends(RateLimiter(times=time, seconds=5))],
    tags=["users"],
)

dependencies = [
    Depends(RateLimiter(times=time, seconds=5)),
    Security(dependency=reusable_oauth2, use_cache=True),
]

api_router.include_router(
    users.router, dependencies=dependencies, tags=["users"]
)
api_router.include_router(
    health.router, dependencies=dependencies, tags=["health"]
)
