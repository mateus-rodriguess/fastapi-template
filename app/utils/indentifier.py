from fastapi import Request
from fastapi.routing import APIRoute


async def ip_or_host_identifier(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host + ":" + request.scope["path"]


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"
