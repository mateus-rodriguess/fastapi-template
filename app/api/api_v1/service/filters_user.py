from typing import Dict

from fastapi import Query


def filters_query(
    id: int = Query(None, description="id"),
    full_name: str = Query(None, description="Full name", alias="fullName"),
    sort_by: str = Query(
        default="created_at", description="Sort by", alias="sortBy"
    ),
) -> Dict:

    return {"id": id, "full_name": full_name, "sort_by": sort_by}
