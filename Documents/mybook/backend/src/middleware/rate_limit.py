"""
Rate limiting middleware for authentication endpoints.
"""
import time
from collections import defaultdict
from typing import Dict, Tuple, Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitExceeded(HTTPException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, detail: str, retry_after: int):
        super().__init__(
            status_code=429,
            detail=detail,
            headers={"Retry-After": str(retry_after)},
        )


class RateLimiter:
    """
    In-memory rate limiter using sliding window algorithm.
    """

    def __init__(
        self,
        requests_per_minute: int = 100,
        block_duration_seconds: int = 60,
    ):
        self.requests_per_minute = requests_per_minute
        self.block_duration_seconds = block_duration_seconds
        self.requests: defaultdict = defaultdict(list)
        self.blocked: defaultdict = defaultdict(float)

    def _get_key(self, request: Request) -> str:
        """Get rate limit key for request."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _cleanup(self, key: str, current_time: float):
        """Remove old requests outside the window."""
        window_start = current_time - 60
        self.requests[key] = [
            ts for ts in self.requests[key] if ts > window_start
        ]

    def is_blocked(self, key: str) -> bool:
        """Check if a key is currently blocked."""
        return self.blocked.get(key, 0) > time.time()

    def check_rate_limit(
        self,
        request: Request,
        max_requests: Optional[int] = None,
    ) -> Tuple[bool, int]:
        """
        Check rate limit for a request.
        """
        key = self._get_key(request)
        current_time = time.time()

        if self.is_blocked(key):
            retry_after = int(self.blocked[key] - current_time)
            return False, max(0, retry_after)

        self._cleanup(key, current_time)

        max_req = max_requests or self.requests_per_minute
        if len(self.requests[key]) >= max_req:
            self.blocked[key] = current_time + self.block_duration_seconds
            return False, self.block_duration_seconds

        self.requests[key].append(current_time)
        return True, 0

    def get_remaining(self, request: Request) -> int:
        """Get remaining requests for this window."""
        key = self._get_key(request)
        self._cleanup(key, time.time())
        remaining = self.requests_per_minute - len(self.requests[key])
        return max(0, remaining)


auth_rate_limiter = RateLimiter(
    requests_per_minute=10,
    block_duration_seconds=60,
)

general_rate_limiter = RateLimiter(
    requests_per_minute=100,
    block_duration_seconds=60,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for applying rate limits."""

    def __init__(
        self,
        app,
        rate_limiter: RateLimiter,
        paths: tuple = ("/auth/",),
        exclude_paths: tuple = (),
    ):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.paths = paths
        self.exclude_paths = exclude_paths

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(excl) for excl in self.exclude_paths):
            return await call_next(request)

        should_limit = any(path.startswith(p) for p in self.paths)

        if should_limit:
            is_allowed, retry_after = self.rate_limiter.check_rate_limit(request)

            if not is_allowed:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "rate_limit_exceeded",
                        "message": "Too many requests. Please try again later.",
                        "retry_after": retry_after,
                    },
                    headers={"Retry-After": str(retry_after)},
                )

        response = await call_next(request)

        if should_limit:
            remaining = self.rate_limiter.get_remaining(request)
            response.headers["X-RateLimit-Limit"] = str(
                self.rate_limiter.requests_per_minute
            )
            response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response


def create_rate_limit_middleware(
    app,
    auth_limit: int = 10,
    general_limit: int = 100,
):
    """Create and configure rate limit middleware."""
    auth_limiter = RateLimiter(
        requests_per_minute=auth_limit,
        block_duration_seconds=60,
    )

    app.add_middleware(
        RateLimitMiddleware,
        rate_limiter=auth_limiter,
        paths=("/auth/signup", "/auth/signin"),
        exclude_paths=("/auth/signout",),
    )

    general_limiter = RateLimiter(
        requests_per_minute=general_limit,
        block_duration_seconds=60,
    )

    app.add_middleware(
        RateLimitMiddleware,
        rate_limiter=general_limiter,
        paths=("/api/",),
        exclude_paths=(),
    )
