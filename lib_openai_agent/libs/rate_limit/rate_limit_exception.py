from typing import Any
from datetime import datetime, timezone
from fastapi.responses import JSONResponse


class CustomRateLimitHttpException(Exception):
    def __init__(self, status_code: int, detail: str, data: Any = None):
        self.status_code = status_code
        self.detail = detail
        if data is not None:
            self.data = data

    def set_request_path(self, path: str):
        self.path = path

    def to_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "statusCode": self.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": self.path,
                "errorMessage": f"{self.detail}",
                "reasons": self.data if hasattr(self, 'data') else {},
            }
        )
