"""Logging middleware with request_id and latency tracking.

Adds X-Request-ID to every response and logs structured JSON to file.
"""
from __future__ import annotations

import time
from urllib import request
import uuid

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from httpx import request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityCORSMiddleware(CORSMiddleware):
    """Reusable CORS policy for local frontend integration."""

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
            **kwargs,
        )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log each request: method, path, status, latency, request_id."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            logger.bind(request_id=request_id).exception(
                "Unhandled exception in request"
            )
            raise

        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        log_level = (
            "INFO" if status_code < 400
            else "WARNING" if status_code < 500
            else "ERROR"
        )

        logger.bind(request_id=request_id).log(
            log_level,
            "{timestamp} {method} {path} {status} {latency_ms}ms id={request_id}",
            timestamp=start,
            method=request.method,
            path=request.url.path,
            status=status_code,
            latency_ms=latency_ms,
            request_id=request_id,
        )

        response.headers["X-Request-ID"] = request_id
        return response

