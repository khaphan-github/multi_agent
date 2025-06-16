
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from libs.utils.u_logger import Logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        headers = dict(request.headers)
        Logger.log(f"Incoming Request: {request.method} {request.url}")
        Logger.log(f"Request Headers: {headers}")
        response = await call_next(request)
        Logger.log(f"Response Status: {response.status_code}")
        return response
