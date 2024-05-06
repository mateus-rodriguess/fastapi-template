from typing import Dict
from uuid import UUID

from fastapi import Query


def filters_query(
    uuid: UUID = Query(None, description="uuid"),
    full_name: str = Query(None, description="Full name", alias="fullName"),
    sort_by: str = Query(
        default="created_at", description="Sort by", alias="sortBy"
    ),
) -> Dict:

    return {"uuid": uuid, "full_name": full_name, "sort_by": sort_by}
