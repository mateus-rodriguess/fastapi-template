from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class filtersQuery(BaseModel):
    uuid: UUID = None
    email: EmailStr = None
    # full_name: str | None = Field(None,  alias="fullName"),
    sort_by: Literal["created_at", "updated_at"] = "created_at"
    page: int = Field(1)
    page_size: int = Field(100, gt=0, le=100, alias="pageSize")
