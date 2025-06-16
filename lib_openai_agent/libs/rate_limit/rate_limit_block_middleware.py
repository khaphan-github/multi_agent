from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .rate_limit_exception import CustomRateLimitHttpException
from .provider import rate_limitter_handler


class RateLimitBlockMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Initialize RateLimiter with the provider
        self.rate_limiter = rate_limitter_handler

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        if self.rate_limiter.is_ip_blocked(ip):  # Use the RateLimiter instance
            res = CustomRateLimitHttpException(
                status_code=403,
                detail=f"IP {ip} is temporarily blocked. Try again later."
            )
            res.set_request_path(request.url.path)
            return res.to_response()
        response = await call_next(request)
        return response
