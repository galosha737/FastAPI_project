import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.logging_config import request_id_var


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логгирования времени выполнения запроса,
    метода, пути, кода состояния и других деталей.
    Также генерирует id запросу.
    """
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())

        token = request_id_var.set(req_id)

        start_time = time.time()
        logging.info({
            "event": "Request started",
            "method": request.method,
            "path": request.url.path,
            "client_host": request.client.host if request.client else "-",
            "user_agent": request.headers.get("user-agent", "-"),
        })

        try:
            response: Response = await call_next(request)
        except Exception as e:
            logging.error({
                "event": "Unhandled exception during request processing",
                "method": request.method,
                "path": request.url.path,
                "exception": str(e),
                "traceback": str(e.__traceback__)
            })
            raise
        finally:
            request_id_var.reset(token)

            process_time = time.time() - start_time

            logging.info({
                "event": "Request handled",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": f"{process_time:.4f}s",
                "content_length": response.headers.get("content-length", "-"),
                "user_agent": request.headers.get("user-agent", "-"),
                "client_host": request.client.host if request.client else "-",
                "query_params": dict(request.query_params),
            })

        return response
