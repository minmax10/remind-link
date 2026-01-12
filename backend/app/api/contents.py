"""
콘텐츠 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.content import Content
from app.models.user import User
from app.api.auth import get_current_user
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

router = APIRouter()


class ContentCreate(BaseModel):
    url: HttpUrl
    category_id: Optional[str] = None
    source: str = "manual"


class ContentResponse(BaseModel):
    id: str
    url: str
    title: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    category_id: Optional[str]
    source: str
    summary: Optional[str]
    reading_time: Optional[int]
    view_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("", response_model=List[ContentResponse])
async def get_contents(
    category: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """콘텐츠 목록 조회"""
    query = db.query(Content).filter(Content.user_id == current_user.id)
    
    # 필터 적용
    if category:
        query = query.filter(Content.category_id == category)
    if source:
        query = query.filter(Content.source == source)
    if search:
        query = query.filter(
            or_(
                Content.title.contains(search),
                Content.description.contains(search)
            )
        )
    
    # 정렬 및 페이지네이션
    contents = query.order_by(Content.created_at.desc()).offset(skip).limit(limit).all()
    
    # 응답 형식 변환
    result = []
    for content in contents:
        result.append({
            "id": str(content.id),
            "url": content.url,
            "title": content.title,
            "description": content.description,
            "image_url": content.image_url,
            "category_id": str(content.category_id) if content.category_id else None,
            "category": {
                "id": str(content.category.id),
                "name": content.category.name,
                "color": content.category.color
            } if content.category else None,
            "source": content.source,
            "summary": content.summary,
            "reading_time": content.reading_time,
            "view_count": content.view_count,
            "created_at": content.created_at
        })
    
    return result


@router.post("", response_model=ContentResponse, status_code=201)
async def create_content(
    content_data: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """콘텐츠 추가"""
    # 중복 체크
    existing = db.query(Content).filter(
        Content.user_id == current_user.id,
        Content.url == str(content_data.url)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="이미 저장된 URL입니다")
    
    # 콘텐츠 생성
    new_content = Content(
        user_id=current_user.id,
        url=str(content_data.url),
        source=content_data.source,
        category_id=content_data.category_id
    )
    
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    
    # TODO: 메타데이터 추출 및 AI 분류는 백그라운드 작업으로 처리
    
    return new_content


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """콘텐츠 상세 조회"""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
    
    # 조회수 증가
    content.view_count += 1
    db.commit()
    
    return content
