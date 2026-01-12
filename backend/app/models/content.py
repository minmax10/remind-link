"""
콘텐츠 모델
"""
from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime, UniqueConstraint, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import GUID
import uuid
from app.database import Base


class Content(Base):
    __tablename__ = "contents"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(Text, nullable=False)
    title = Column(String(500))
    description = Column(Text)
    image_url = Column(Text)
    category_id = Column(GUID(), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    source = Column(String(50), nullable=False)  # 'instagram', 'threads', 'manual'
    content_metadata = Column(JSON)  # SQLite는 JSON, PostgreSQL은 JSONB (metadata는 SQLAlchemy 예약어)
    summary = Column(Text)
    reading_time = Column(Integer)  # 분 단위
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    user = relationship("User", backref="contents")
    category = relationship("Category", backref="contents")
    
    # 제약조건
    __table_args__ = (
        UniqueConstraint('user_id', 'url', name='uq_user_url'),
    )
