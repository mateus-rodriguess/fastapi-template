from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class MensageHealth(BaseModel):
    message: dict = {"detail": "OK"}


@router.get(
    path="/health",
    status_code=status.HTTP_200_OK,
    response_model=MensageHealth,
)
async def health() -> dict:
    return MensageHealth
