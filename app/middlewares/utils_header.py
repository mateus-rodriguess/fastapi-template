import time

from fastapi import Request, Response


async def header_utils(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["user-agent"] = request.headers["user-agent"]
    
    return response
