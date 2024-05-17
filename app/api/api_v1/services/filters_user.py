from typing import Dict
from uuid import UUID

from fastapi import Query
from pydantic import EmailStr


def filters_query(
    uuid: UUID = Query(None, description="uuid"),
    email: EmailStr = Query(None, description="Email", alias="email"),
    full_name: str = Query(None, description="Full name", alias="fullName"),
    sort_by: str = Query(
        default="created_at", description="Sort by", alias="sortBy"
    ),
) -> Dict:

    return {
        "uuid": uuid,
        "email": email,
        "full_name": full_name,
        "sort_by": sort_by,
    }
