import time

from fastapi import Request, Response


async def header_utils(request: Request, call_next):
    start_time = time.process_time()
    response: Response = await call_next(request)
    process_time = time.process_time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    response.headers["user-agent"] = request.headers["user-agent"]

    return response
