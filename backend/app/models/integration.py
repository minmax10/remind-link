"""
외부 플랫폼 연동 모델
"""
from sqlalchemy import Column, String, Boolean, DateTime, UniqueConstraint, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import GUID
import uuid
from app.database import Base


class Integration(Base):
    __tablename__ = "integrations"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False)  # 'instagram', 'threads'
    access_token = Column(Text)
    refresh_token = Column(Text)
    platform_username = Column(String(255))  # 외부 플랫폼 사용자명
    expires_at = Column(DateTime(timezone=True))
    last_sync_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    user = relationship("User", backref="integrations")
    
    # 제약조건
    __table_args__ = (
        UniqueConstraint('user_id', 'platform', name='uq_user_platform'),
    )
