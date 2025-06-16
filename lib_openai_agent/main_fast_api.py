"""
    The entry file for the FastAPI application.
"""

from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.router import router
import asyncio
from common.middlewares.header_middleware import ExtractHeaderMiddleware
from common.middlewares.logger_middleware import LoggerMiddleware
from common.exceptions.custom_exception import CustomHttpException
from libs.rate_limit.rate_limit_block_middleware import RateLimitBlockMiddleware
from libs.rate_limit.rate_limit_exception import CustomRateLimitHttpException
from libs.rate_limit.limiter import RateLimiter
from libs.rate_limit.provider import limiter
from config.startup_task import APP_START_UP_TASKS
from libs.rate_limit.provider import rate_limitter_handler


app = FastAPI(title="GPT Assistants", version="1.1.0",
              debug=False)


@app.on_event("startup")
async def startup_event():
    await asyncio.gather(*(task() for task in APP_START_UP_TASKS))

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ExtractHeaderMiddleware)
# app.add_middleware(RateLimitBlockMiddleware)
app.add_middleware(LoggerMiddleware)

app.include_router(router)
app.state.limiter = limiter


@app.exception_handler(CustomHttpException)
async def custom_exception_handler(request: Request, exc: CustomHttpException):
    exc.set_request_path(request.url.path)
    return exc.to_response()


# @app.exception_handler(RateLimitExceeded)
# async def rate_limit_exceptions(request: Request, exc: RateLimitExceeded):
#     _exc = CustomRateLimitHttpException(
#         status_code=429, detail="Rate limit exceeded")
#     _exc.set_request_path(request.url.path)
#     response = _exc.to_response()
#     response = request.app.state.limiter._inject_headers(
#         response, request.state.view_rate_limit
#     )
#     ip = request.client.host
#     try:
#         rate_limitter_handler.log_spam_ip(
#             ip=ip,
#         )
#     except Exception as e:
#         print(e)
#     return response
