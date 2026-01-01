"""
Session model for JWT session management.
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
from src.lib.database import Base


class Session(Base):
    """
    User session with JWT token tracking.

    Attributes:
        id: Unique session identifier (UUID)
        user_id: Foreign key to User
        access_token_hash: Hashed JWT access token
        refresh_token_hash: Hashed JWT refresh token
        created_at: Session creation timestamp
        expires_at: Access token expiration timestamp
        last_used_at: Last activity timestamp
        ip_address: Client IP address for audit
        user_agent: Client user agent string
    """

    __tablename__ = "sessions"

    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Token hashes (store hashed tokens, not raw)
    access_token_hash = Column(String(255), nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False, index=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_used_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Audit fields
    ip_address = Column(INET, nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")

    # Indexes for common queries
    __table_args__ = (
        Index('idx_session_user_id', 'user_id'),
        Index('idx_session_access_token', 'access_token_hash'),
        Index('idx_session_expires_at', 'expires_at'),
    )

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user_id={self.user_id})>"

    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if session is still valid."""
        return not self.is_expired

    def update_activity(self) -> None:
        """Update last used timestamp."""
        self.last_used_at = datetime.now(timezone.utc)

    def extend_expiration(self, minutes: int = 15) -> None:
        """Extend session expiration."""
        self.expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "ip_address": str(self.ip_address) if self.ip_address else None,
            "user_agent": self.user_agent,
        }
