from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import ValidationError
from sqlmodel import Session

from app.api.api_v1.deps import CurrentUser, TokenDep, get_session
from app.core import security
from app.core.settings import get_settings
from app.db.repositories.user import UserRepository
from app.models.user import TokenResponse

router = APIRouter()
settings = get_settings()


@router.post("/login/access-token")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await UserRepository.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password.",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user."
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return TokenResponse(
        access_token=security.create_access_token(
            user.uuid, expires_delta=access_token_expires
        )
    )


@router.post(
    path="/login/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def refresh_access_token(
    current_user: CurrentUser, token: TokenDep
) -> TokenResponse:
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    try:
        payload: dict = security.verify_refresh_token(token)
        if payload.get("sub") is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials.",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate credentials.",
        )

    return TokenResponse(
        access_token=security.create_access_token(
            current_user.uuid, access_token_expires
        ),
        token_type="Bearer",
    )
