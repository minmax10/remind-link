"""
인증 API 라우터 (한글 버전)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.user import User
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings
from pydantic import BaseModel, EmailStr

router = APIRouter()

# OAuth2 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="비밀번호_인증",
    description="사용자명(이메일)과 비밀번호로 로그인하여 토큰을 받습니다"
)


class UserRegister(BaseModel):
    """회원가입 요청 모델"""
    email: EmailStr
    password: str
    name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123",
                "name": "홍길동"
            }
        }


class UserResponse(BaseModel):
    """사용자 응답 모델"""
    id: str
    email: str
    name: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid",
                "email": "user@example.com",
                "name": "홍길동"
            }
        }


class Token(BaseModel):
    """토큰 응답 모델"""
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="새로운 사용자를 등록합니다. 이메일, 비밀번호, 이름을 입력하세요."
)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """회원가입"""
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    # 사용자 생성
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="로그인",
    description="이메일과 비밀번호로 로그인합니다. 성공하면 access_token을 받습니다."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    로그인
    
    **사용 방법:**
    1. 위의 "Authorize" 버튼을 클릭하세요
    2. 사용자명에 이메일을 입력하세요
    3. 비밀번호를 입력하세요
    4. "Authorize" 버튼을 클릭하세요
    5. 받은 토큰을 복사하여 다른 API 호출 시 사용하세요
    """
    # 사용자 조회 (OAuth2PasswordRequestForm은 username 필드를 사용)
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰 생성
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/refresh",
    response_model=Token,
    summary="토큰 갱신",
    description="만료된 토큰을 새로 갱신합니다."
)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """토큰 갱신 (현재는 구현되지 않음)"""
    # TODO: Refresh token 구현
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="토큰 갱신 기능은 아직 구현되지 않았습니다"
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """현재 로그인한 사용자 조회"""
    from app.utils.security import decode_access_token
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 유효하지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 유효하지 않습니다",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
        )
    
    return user
