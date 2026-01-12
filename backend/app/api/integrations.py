"""
외부 플랫폼 연동 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.integration import Integration
from app.models.content import Content
from app.models.user import User
from app.api.auth import get_current_user
from app.services.instagram import InstagramService
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()


class IntegrationResponse(BaseModel):
    id: str
    platform: str
    is_active: bool
    last_sync_at: Optional[str]
    
    class Config:
        from_attributes = True


class InstagramConnectRequest(BaseModel):
    username: str
    password: str


@router.get("", response_model=List[IntegrationResponse])
async def get_integrations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """연동 목록 조회"""
    integrations = db.query(Integration).filter(
        Integration.user_id == current_user.id
    ).all()
    return integrations


@router.post("/instagram/connect")
async def connect_instagram(
    request: InstagramConnectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """인스타그램 연동 시작 (사용자명/비밀번호)"""
    try:
        # 기존 연동 확인
        existing = db.query(Integration).filter(
            Integration.user_id == current_user.id,
            Integration.platform == 'instagram'
        ).first()
        
        # 인스타그램 서비스로 로그인 테스트
        instagram_service = InstagramService(request.username, request.password)
        login_success = instagram_service.login()
        
        if not login_success:
            raise HTTPException(status_code=400, detail="인스타그램 로그인에 실패했습니다")
        
        # 연동 정보 저장 (비밀번호는 암호화해서 저장해야 하지만, 일단 평문으로)
        # TODO: 비밀번호 암호화 구현
        if existing:
            existing.access_token = request.password  # 임시로 비밀번호 저장
            existing.platform_username = request.username
            existing.is_active = True
            existing.updated_at = datetime.utcnow()
        else:
            integration = Integration(
                user_id=current_user.id,
                platform='instagram',
                access_token=request.password,  # 임시로 비밀번호 저장
                platform_username=request.username,
                is_active=True
            )
            db.add(integration)
        
        db.commit()
        
        return {
            "message": "인스타그램 연동이 완료되었습니다",
            "platform": "instagram"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"인스타그램 연동 실패: {str(e)}")


@router.post("/threads/connect")
async def connect_threads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """쓰레드(X) 연동 시작"""
    return {"message": "쓰레드 연동 기능은 구현 중입니다"}


@router.post("/{integration_id}/sync")
async def sync_integration(
    integration_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """수동 동기화"""
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id
    ).first()
    
    if not integration:
        raise HTTPException(status_code=404, detail="연동을 찾을 수 없습니다")
    
    if not integration.is_active:
        raise HTTPException(status_code=400, detail="비활성화된 연동입니다")
    
    try:
        if integration.platform == 'instagram':
            # 인스타그램 동기화
            if not integration.platform_username or not integration.access_token:
                raise HTTPException(status_code=400, detail="인스타그램 인증 정보가 없습니다")
            
            instagram_service = InstagramService(
                integration.platform_username,
                integration.access_token
            )
            instagram_service.login()
            
            # 저장된 게시물 가져오기
            saved_posts = instagram_service.get_saved_posts(limit=100)
            
            # 콘텐츠로 변환하여 저장
            synced_count = 0
            for post in saved_posts:
                # 중복 체크
                existing = db.query(Content).filter(
                    Content.user_id == current_user.id,
                    Content.url == post['url']
                ).first()
                
                if not existing:
                    content = Content(
                        user_id=current_user.id,
                        url=post['url'],
                        title=post.get('title', '')[:500],
                        description=post.get('description', ''),
                        image_url=post.get('image_url'),
                        source='instagram',
                        content_metadata=post.get('metadata', {})
                    )
                    db.add(content)
                    synced_count += 1
            
            # 동기화 시간 업데이트
            integration.last_sync_at = datetime.utcnow()
            db.commit()
            
            return {
                "message": f"{synced_count}개의 콘텐츠가 동기화되었습니다",
                "synced_count": synced_count
            }
        else:
            raise HTTPException(status_code=400, detail="지원하지 않는 플랫폼입니다")
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"동기화 실패: {str(e)}")


@router.delete("/{integration_id}")
async def disconnect_integration(
    integration_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """연동 해제"""
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id
    ).first()
    
    if not integration:
        raise HTTPException(status_code=404, detail="연동을 찾을 수 없습니다")
    
    db.delete(integration)
    db.commit()
    
    return {"message": "연동이 해제되었습니다"}
