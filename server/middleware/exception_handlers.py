from fastapi import Request
from fastapi.responses import JSONResponse
from logger import logger


async def catch_middleware_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("Unhandled Expceptions")
        return JSONResponse(status_code=500, content={'error': str(exc)})
