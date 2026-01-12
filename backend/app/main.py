"""
FastAPI 애플리케이션 진입점
"""
import sys
import os

# UTF-8 인코딩 강제 설정
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["LC_ALL"] = "C.UTF-8"
    os.environ["LANG"] = "C.UTF-8"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db
from app.api import auth, contents, integrations, categories

# FastAPI 앱 생성
app = FastAPI(
    title="Remind Link API",
    description="인스타그램과 쓰레드 저장글을 자동으로 수집하고 분류하는 서비스",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
    default_response_class=JSONResponse
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    init_db()


# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["🔐 인증"])
app.include_router(contents.router, prefix="/api/contents", tags=["📄 콘텐츠"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["🔗 연동"])
app.include_router(categories.router, prefix="/api/categories", tags=["📁 카테고리"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Remind Link API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}
