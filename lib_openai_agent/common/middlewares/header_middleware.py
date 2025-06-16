from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ExtractHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('authorization')
        if auth_header:
            try:
                access_token = auth_header.split(' ')[1]
            except IndexError:
                access_token = None
        else:
            access_token = None

        is_user_logged_in = access_token is not None

        request.state.custom_request_state = {
            "access_token": access_token,
            "is_user_logged_in": is_user_logged_in
        }

        response = await call_next(request)
        return response
