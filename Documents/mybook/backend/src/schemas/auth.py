"""
Pydantic schemas for authentication.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


# ============== Request Schemas ==============

class SignupRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (8+ characters, mixed case, numbers)"
    )
    confirm_password: str = Field(..., description="Password confirmation")
    profile: "ProfileData" = Field(..., description="User's background profile")
    consent: bool = Field(default=False, description="User consent to terms")

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Ensure passwords match."""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("consent")
    @classmethod
    def consent_required(cls, v: bool) -> bool:
        """Ensure user has given consent."""
        if not v:
            raise ValueError("User consent is required")
        return v


class SigninRequest(BaseModel):
    """Request schema for user sign-in."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class RefreshTokenRequest(BaseModel):
    """Request schema for token refresh."""

    refresh_token: str = Field(..., description="Refresh token")


class DeleteAccountRequest(BaseModel):
    """Request schema for account deletion."""

    password: str = Field(..., description="Current password for verification")
    confirm_delete: bool = Field(..., description="Confirmation to delete account")

    @field_validator("confirm_delete")
    @classmethod
    def confirm_delete_required(cls, v: bool) -> bool:
        """Ensure deletion is confirmed."""
        if not v:
            raise ValueError("Account deletion must be confirmed")
        return v


# ============== Response Schemas ==============

class UserInfo(BaseModel):
    """Public user information."""

    id: str = Field(..., description="User UUID")
    email: EmailStr = Field(..., description="User's email")
    created_at: datetime = Field(..., description="Account creation time")
    last_login_at: Optional[datetime] = Field(None, description="Last sign-in time")

    class Config:
        from_attributes = True


class SessionInfo(BaseModel):
    """Session information."""

    id: str = Field(..., description="Session UUID")
    created_at: datetime = Field(..., description="Session creation time")
    expires_at: datetime = Field(..., description="Session expiration time")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    ip_address: Optional[str] = Field(None, description="Client IP address")


class AuthResponse(BaseModel):
    """Authentication response with tokens and user info."""

    user: UserInfo = Field(..., description="User information")
    session: SessionInfo = Field(..., description="Session information")
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenRefreshResponse(BaseModel):
    """Token refresh response."""

    access_token: str = Field(..., description="New JWT access token")
    refresh_token: str = Field(..., description="New JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration in seconds")


class SessionResponse(BaseModel):
    """Current session response."""

    session: SessionInfo = Field(..., description="Session information")
    user: UserInfo = Field(..., description="User information")


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str = Field(..., description="Response message")


# ============== Profile Schemas ==============

class SoftwareBackground(BaseModel):
    """User's software development background."""

    languages: List[str] = Field(
        default=[],
        min_length=1,
        description="Programming languages (e.g., python, c++, rust)"
    )
    frameworks: List[str] = Field(
        default=[],
        min_length=1,
        description="Frameworks (e.g., pytorch, tensorflow, ros2)"
    )
    tools: List[str] = Field(
        default=[],
        min_length=1,
        description="Tools (e.g., docker, git, jupyter)"
    )
    experience_level: str = Field(
        ...,
        description="Experience level",
        pattern="^(beginner|intermediate|advanced)$"
    )


class HardwareBackground(BaseModel):
    """User's hardware/robotics background."""

    platforms: List[str] = Field(
        default=[],
        min_length=1,
        description="Robotics platforms (e.g., nvidia-jetson, raspberry-pi)"
    )
    sensors: List[str] = Field(
        default=[],
        min_length=1,
        description="Sensors (e.g., lidar, rgb-camera, imu)"
    )
    actuators: List[str] = Field(
        default=[],
        min_length=1,
        description="Actuators (e.g., servo-motors, brushless-dc)"
    )
    experience_level: str = Field(
        ...,
        description="Experience level",
        pattern="^(beginner|intermediate|advanced)$"
    )


class ProfileData(BaseModel):
    """Complete profile data for new users."""

    software: SoftwareBackground = Field(..., description="Software background")
    hardware: HardwareBackground = Field(..., description="Hardware background")


class ProfileDataPartial(BaseModel):
    """Partial profile data for updates."""

    software: Optional[SoftwareBackground] = None
    hardware: Optional[HardwareBackground] = None


class ProfileResponse(BaseModel):
    """Profile response for authenticated users."""

    email: EmailStr = Field(..., description="User's email")
    profile: ProfileData = Field(..., description="User's profile data")
    created_at: datetime = Field(..., description="Account creation time")
    last_login_at: Optional[datetime] = Field(None, description="Last sign-in time")


# ============== Error Schemas ==============

class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")


class ValidationErrorResponse(BaseModel):
    """Validation error response."""

    error: str = Field(default="validation_error")
    message: str = Field(..., description="Validation failed")
    details: List[dict] = Field(..., description="Validation errors")


# Rebuild models to handle forward references
SignupRequest.model_rebuild()
