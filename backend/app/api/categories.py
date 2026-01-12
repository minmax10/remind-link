"""
카테고리 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.content import Content
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    icon: str | None
    color: str | None
    content_count: int = 0
    
    class Config:
        from_attributes = True


@router.get("", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """카테고리 목록 조회"""
    categories = db.query(Category).order_by(Category.sort_order).all()
    
    result = []
    for category in categories:
        # 각 카테고리의 콘텐츠 개수 계산
        content_count = db.query(Content).filter(Content.category_id == category.id).count()
        category_dict = {
            "id": str(category.id),
            "name": category.name,
            "slug": category.slug,
            "icon": category.icon,
            "color": category.color,
            "content_count": content_count
        }
        result.append(category_dict)
    
    return result


def init_default_categories(db: Session):
    """기본 카테고리 초기화"""
    default_categories = [
        {"name": "기술/개발", "slug": "technology", "icon": "code", "color": "#3B82F6", "sort_order": 1},
        {"name": "디자인/아트", "slug": "design", "icon": "palette", "color": "#EC4899", "sort_order": 2},
        {"name": "비즈니스/경제", "slug": "business", "icon": "briefcase", "color": "#10B981", "sort_order": 3},
        {"name": "뉴스/시사", "slug": "news", "icon": "newspaper", "color": "#F59E0B", "sort_order": 4},
        {"name": "엔터테인먼트", "slug": "entertainment", "icon": "film", "color": "#8B5CF6", "sort_order": 5},
        {"name": "교육/학습", "slug": "education", "icon": "book", "color": "#06B6D4", "sort_order": 6},
        {"name": "건강/라이프스타일", "slug": "health", "icon": "heart", "color": "#EF4444", "sort_order": 7},
        {"name": "여행/음식", "slug": "travel", "icon": "map", "color": "#F97316", "sort_order": 8},
        {"name": "기타", "slug": "other", "icon": "folder", "color": "#6B7280", "sort_order": 9},
    ]
    
    for cat_data in default_categories:
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
    
    db.commit()
