from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.api_v1.deps import CurrentUser, get_session
from app.api.api_v1.service.filters_user import filters_query
from app.core.security import verify_password
from app.db.repositories.user import UserRepository
from app.models.user import (Message, UpdatePassword, UserAllowedFilters,
                             UserPublic, UserRegister, UserUpdate)
from app.utils.custom_pagination import PageParams

router = APIRouter()
router_unauthenticated = APIRouter()


@router_unauthenticated.post(
    path="/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
)
async def create_user(
    *, user_in: UserRegister, session: Session = Depends(get_session)
) -> dict:
    user = await UserRepository.get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    return await UserRepository.create_user(
        session=session, user_create=user_in
    )


@router.get(path="/users", status_code=status.HTTP_200_OK)
async def get_users(
    *,
    session: Session = Depends(get_session),
    filters: dict = Depends(filters_query)
) -> PageParams[UserPublic]:
    params = UserAllowedFilters(**filters).model_dump(exclude_none=True)
    return await UserRepository.get_all_users(
        session, sort_by=params.pop("sort_by"), filters=params
    )


@router.get(
    path="/users/{id:int}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
async def get_user(
    *, id: int, session: Session = Depends(get_session)
) -> dict:
    data = await UserRepository.get_user_by_id(session, id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found."
        )
    return data


@router.patch(
    path="/users",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
async def update_user_me(
    *,
    user_in: UserUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_session)
) -> dict:
    if user_in.email:
        existing_user = await UserRepository.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )
    return await UserRepository.update_user_me(session, current_user, user_in)


@router.patch("/users/me/password")
async def update_password_me(
    *,
    body: UpdatePassword,
    current_user: CurrentUser,
    session: Session = Depends(get_session)
) -> Message:
    if not verify_password(body.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password.",
        )
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current one.",
        )

    return await UserRepository.update_password_me(
        session, current_user, body.new_password
    )


@router.get("/users/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.delete(
    path="/users/{id:int}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def delete_user(
    *, id: int, session: Session = Depends(get_session)
) -> Message:
    return await UserRepository.delete_user(session, id)
