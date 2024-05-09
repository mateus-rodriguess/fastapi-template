from uuid import UUID

from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.user import Message, User, UserPublic, UserUpdate
from app.utils.custom_pagination import PageParams


class UserRepository:

    @classmethod
    async def get_all_users(
        cls, session: Session, sort_by: str = "created_at", filters: dict = ""
    ) -> PageParams[UserPublic]:
        return await paginate(
            session, select(User).filter_by(**filters).order_by(sort_by)
        )

    @classmethod
    async def create_user(cls, session: Session, user_create: dict):
        db_obj = User.model_validate(
            user_create,
            update={"password": get_password_hash(user_create.password)},
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @classmethod
    async def update_user_me(
        cls, session: Session, current_user: User, user_in: UserUpdate
    ) -> UserPublic:

        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["password"] = hashed_password

        current_user.sqlmodel_update(user_data, update=extra_data)
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)
        return current_user

    @classmethod
    async def get_user_by_email(
        cls, session: Session, email: str
    ) -> UserPublic | None:
        session_user = await session.exec(
            select(User).where(User.email == email)
        )
        return session_user.first()

    @classmethod
    async def get_user_by_uuid(
        cls, session: Session, uuid: UUID
    ) -> UserPublic | None:
        session_user = await session.exec(
            select(User).where(User.uuid == uuid)
        )
        return session_user.first()

    @classmethod
    async def update_password_me(
        cls, session: Session, current_user: User, password: str
    ) -> Message:
        hashed_password = get_password_hash(password)
        current_user.password = hashed_password
        session.add(current_user)
        await session.commit()
        return Message(detail="Password updated successfully.")

    @classmethod
    async def authenticate(
        cls, session: Session, email: str, password: str
    ) -> UserPublic | None:
        db_user = await cls.get_user_by_email(session=session, email=email)

        if not db_user:
            return None
        if not verify_password(password, db_user.password):
            return None
        return db_user

    @classmethod
    async def delete_user(cls, session: Session, uuid: UUID) -> Message:
        user = await session.get(User, uuid)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        await session.delete(user)
        await session.commit()
        return Message(detail="User deleted successfully.")
