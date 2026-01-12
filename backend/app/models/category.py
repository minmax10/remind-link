"""
카테고리 모델
"""
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.models.user import GUID
import uuid
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    icon = Column(String(50))
    color = Column(String(7))  # HEX color
    is_default = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
