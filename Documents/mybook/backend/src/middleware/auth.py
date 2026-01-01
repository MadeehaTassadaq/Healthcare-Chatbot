"""
Authentication middleware for JWT validation.
"""
from typing import Optional, Callable
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.lib.database import get_async_session
from src.lib.jwt import validate_access_token
from src.models.user import User
from src.services.auth.user_service import get_user_by_id

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Dependency for getting the current authenticated user.
    """
    token = credentials.credentials
    payload = validate_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.deleted_at is not None:
        raise HTTPException(
            status_code=401,
            detail="Account has been deleted",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    session: AsyncSession = Depends(get_async_session),
) -> Optional[User]:
    """
    Dependency for optionally getting the current user.
    """
    if credentials is None:
        return None

    token = credentials.credentials
    payload = validate_access_token(token)

    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    user = await get_user_by_id(session, user_id)
    if user is None or user.deleted_at is not None:
        return None

    return user


class AuthenticatedUser:
    """Dependency class for injecting the current user."""

    def __init__(self, user: User):
        self.user = user
        self.id = user.id
        self.email = user.email

    def __repr__(self):
        return f"AuthenticatedUser(id={self.id}, email={self.email})"


async def require_auth(
    user: User = Depends(get_current_user),
) -> AuthenticatedUser:
    """
    Dependency that requires authentication.
    """
    return AuthenticatedUser(user)
