"""
인증 API 라우터
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

# OAuth2 스키마 설정 (한글 설명 추가)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="비밀번호_인증",
    description="사용자명과 비밀번호로 로그인하여 토큰을 받습니다"
)


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="새로운 사용자를 등록합니다"
)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """회원가입 - 이메일, 비밀번호, 이름으로 새 계정을 만듭니다"""
    try:
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
        
        return {
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"회원가입 중 오류가 발생했습니다: {str(e)}"
        )


@router.post(
    "/login",
    response_model=Token,
    summary="로그인",
    description="""
    이메일과 비밀번호로 로그인합니다.
    
    **Swagger UI에서 사용하는 방법:**
    1. 페이지 상단의 "Authorize" 버튼을 클릭하세요
    2. "사용자명" 필드에 이메일 주소를 입력하세요
    3. "비밀번호" 필드에 비밀번호를 입력하세요
    4. "Authorize" 버튼을 클릭하세요
    5. 토큰이 자동으로 저장되어 이후 API 호출에 사용됩니다
    
    **직접 호출하는 방법:**
    - form-data 형식으로 username(이메일)과 password를 전송하세요
    """
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """로그인 - 이메일과 비밀번호로 인증하고 토큰을 받습니다"""
    # 사용자 조회
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
