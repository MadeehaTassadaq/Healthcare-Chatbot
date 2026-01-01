"""
User model for authentication and profile storage.
"""
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from src.lib.database import Base


class User(Base):
    """
    User account with authentication credentials and profile data.

    Attributes:
        id: Unique user identifier (UUID)
        email: User's email address (immutable, unique)
        password_hash: bcrypt hash of password
        better_auth_id: Reference to Better-Auth user ID
        created_at: Account creation timestamp
        last_login_at: Last successful sign-in timestamp
        deleted_at: Soft delete timestamp (GDPR compliance)
        profile_data: Structured JSON profile (software/hardware background)
    """

    __tablename__ = "users"

    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    better_auth_id = Column(String(255), unique=True, nullable=True, index=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Profile data (JSONB for flexibility)
    profile_data = Column(JSONB, nullable=False, default=dict)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    chapter_preferences = relationship(
        "ChapterPreference",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_better_auth_id', 'better_auth_id'),
        Index('idx_user_deleted_at', 'deleted_at'),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    @property
    def is_deleted(self) -> bool:
        """Check if account is soft-deleted."""
        return self.deleted_at is not None

    @property
    def is_active(self) -> bool:
        """Check if account is active (not deleted)."""
        return self.deleted_at is None

    def get_profile(self) -> Dict[str, Any]:
        """Get user profile data."""
        return self.profile_data or {}

    def update_profile(self, profile_data: Dict[str, Any]) -> None:
        """Update user profile data."""
        self.profile_data = profile_data

    def soft_delete(self) -> None:
        """Mark account as deleted (soft delete for GDPR compliance)."""
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """Restore a soft-deleted account."""
        self.deleted_at = None

    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (excludes sensitive fields)."""
        return {
            "id": str(self.id),
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "profile": self.get_profile(),
        }
