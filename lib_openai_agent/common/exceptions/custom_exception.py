from typing import Any
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from libs.utils.u_logger import Logger


class CustomHttpException(Exception):
    def __init__(self, status_code: int, detail: str, data: Any = None):
        self.status_code = status_code
        self.detail = detail
        if data is not None:
            self.data = data

    def set_request_path(self, path: str):
        self.path = path

    def to_response(self):
        content = {
            "statusCode": self.status_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": self.path,
            "errorMessage": f"{self.detail}",
            "reasons": self.data if hasattr(self, 'data') else {},
        }
        result = JSONResponse(
            status_code=self.status_code,
            content=content)

        Logger.log(content, 40, 'CustomHttpException')
        return result
