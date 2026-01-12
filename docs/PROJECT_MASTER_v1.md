# Remind Link - 통합 프로젝트 문서 v1.0

> **핵심 목표**: 인스타그램과 쓰레드 계정 연동 후 실제로 동작하는 MVP 구축

## 📋 프로젝트 개요

Remind Link는 사용자가 인스타그램과 쓰레드(X)에서 저장한 콘텐츠를 자동으로 수집하고, AI를 활용해 카테고리별로 분류하여 보기 좋게 정리해주는 서비스입니다.

### Phase 1 핵심 기능 (v1.0)
1. ✅ 인스타그램 저장글 자동 수집
2. ✅ 쓰레드(X) 저장글 자동 수집
3. ✅ 수동 링크 추가
4. ✅ 기본 카테고리 분류 (규칙 기반 → AI 기반)
5. ✅ 콘텐츠 목록 조회 및 필터링

## 🏗️ 기술 스택

### Backend
- **Python 3.11+**
- **FastAPI** - API 프레임워크
- **SQLAlchemy** - ORM
- **PostgreSQL** - 데이터베이스 (또는 SQLite로 시작)
- **Pydantic** - 데이터 검증
- **httpx** - HTTP 클라이언트
- **BeautifulSoup4** - 웹 스크래핑
- **python-dotenv** - 환경 변수 관리

### 인스타그램 연동
- **Instagram Basic Display API** 또는 **웹 스크래핑** (Puppeteer 대신 Selenium)
- **instagrapi** (비공식 라이브러리) - 선택사항

### 쓰레드(X) 연동
- **Twitter API v2** - 공식 API 사용
- **tweepy** - Twitter API 클라이언트

### AI 분류
- **OpenAI API** (GPT-4) 또는 **Anthropic Claude API**
- **langchain** - LLM 통합

## 📁 프로젝트 구조

```
remind-link/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 앱 진입점
│   │   ├── config.py            # 설정 관리
│   │   ├── database.py          # DB 연결
│   │   ├── models/              # SQLAlchemy 모델
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── content.py
│   │   │   ├── category.py
│   │   │   └── integration.py
│   │   ├── schemas/             # Pydantic 스키마
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── content.py
│   │   │   └── integration.py
│   │   ├── api/                 # API 라우터
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── contents.py
│   │   │   ├── integrations.py
│   │   │   └── categories.py
│   │   ├── services/            # 비즈니스 로직
│   │   │   ├── __init__.py
│   │   │   ├── instagram.py    # 인스타그램 연동
│   │   │   ├── twitter.py      # 쓰레드 연동
│   │   │   ├── scraper.py      # 메타데이터 추출
│   │   │   └── ai_classifier.py # AI 분류
│   │   └── utils/               # 유틸리티
│   │       ├── __init__.py
│   │       └── security.py     # 인증/암호화
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic/                # DB 마이그레이션 (선택)
├── frontend/                    # 나중에 구현
├── docs/
│   └── PROJECT_MASTER_v1.md    # 이 문서
├── README.md
└── SETUP.md                     # 설치 가이드
```

## 🔑 인스타그램 연동 전략

### 방법 1: Instagram Basic Display API (공식, 제한적)
- **장점**: 공식 API, 안정적
- **단점**: 저장된 게시물 API가 없음 (개인 미디어만 가능)

### 방법 2: 웹 스크래핑 (Selenium)
- **장점**: 저장된 게시물 접근 가능
- **단점**: ToS 위반 가능성, 불안정할 수 있음
- **구현**: Selenium으로 로그인 후 저장된 게시물 페이지 접근

### 방법 3: instagrapi (비공식 라이브러리)
- **장점**: 저장된 게시물 접근 가능, 비교적 안정적
- **단점**: 비공식, 언제든 막힐 수 있음

**v1.0에서는 방법 2 (웹 스크래핑) 또는 방법 3 (instagrapi) 사용**

## 🔑 쓰레드(X) 연동 전략

### Twitter API v2 사용
- **북마크 엔드포인트**: `GET /2/users/:id/bookmarks`
- **필요한 권한**: `bookmarks.read`
- **인증**: OAuth 2.0

**구현 단계**:
1. Twitter Developer Portal에서 앱 생성
2. OAuth 2.0 인증 플로우
3. 북마크 API 호출
4. 트윗 메타데이터 추출

## 📊 데이터베이스 스키마 (간소화)

### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### contents
```sql
CREATE TABLE contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(500),
    description TEXT,
    image_url TEXT,
    category_id UUID REFERENCES categories(id),
    source VARCHAR(50) NOT NULL, -- 'instagram', 'threads', 'manual'
    metadata JSONB DEFAULT '{}',
    summary TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, url)
);
```

### categories
```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50),
    color VARCHAR(7)
);

-- 기본 카테고리
INSERT INTO categories (name, slug, icon, color) VALUES
('기술/개발', 'technology', 'code', '#3B82F6'),
('디자인/아트', 'design', 'palette', '#EC4899'),
('비즈니스/경제', 'business', 'briefcase', '#10B981'),
('뉴스/시사', 'news', 'newspaper', '#F59E0B'),
('엔터테인먼트', 'entertainment', 'film', '#8B5CF6'),
('교육/학습', 'education', 'book', '#06B6D4'),
('건강/라이프스타일', 'health', 'heart', '#EF4444'),
('여행/음식', 'travel', 'map', '#F97316'),
('기타', 'other', 'folder', '#6B7280');
```

### integrations
```sql
CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'instagram', 'threads'
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    last_sync_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(user_id, platform)
);
```

## 🚀 개발 단계

### Step 1: 프로젝트 초기 설정
- [x] 폴더 구조 생성
- [ ] Python 가상환경 설정
- [ ] requirements.txt 작성
- [ ] .env.example 작성

### Step 2: FastAPI 기본 구조
- [ ] FastAPI 앱 초기화
- [ ] 데이터베이스 연결 설정
- [ ] 기본 모델 정의
- [ ] 인증 시스템 (JWT)

### Step 3: 기본 API
- [ ] 회원가입/로그인 API
- [ ] 콘텐츠 CRUD API
- [ ] 카테고리 조회 API

### Step 4: 인스타그램 연동
- [ ] 인스타그램 로그인 (웹 스크래핑 또는 instagrapi)
- [ ] 저장된 게시물 가져오기
- [ ] 메타데이터 추출
- [ ] 주기적 동기화

### Step 5: 쓰레드 연동
- [ ] Twitter OAuth 인증
- [ ] 북마크 API 연동
- [ ] 트윗 메타데이터 추출
- [ ] 주기적 동기화

### Step 6: AI 분류
- [ ] OpenAI/Claude API 연동
- [ ] 카테고리 분류 프롬프트
- [ ] 태그 생성
- [ ] 요약 생성

### Step 7: 메타데이터 추출
- [ ] OG 태그 파싱
- [ ] 이미지 추출
- [ ] 요약 생성

## 📝 API 엔드포인트 (핵심만)

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/refresh` - 토큰 갱신

### 콘텐츠
- `GET /api/contents` - 목록 조회 (필터, 검색)
- `POST /api/contents` - 수동 추가
- `GET /api/contents/{id}` - 상세 조회
- `PATCH /api/contents/{id}` - 수정
- `DELETE /api/contents/{id}` - 삭제

### 연동
- `GET /api/integrations` - 연동 목록
- `POST /api/integrations/instagram/connect` - 인스타그램 연동 시작
- `GET /api/integrations/instagram/callback` - 인스타그램 콜백
- `POST /api/integrations/threads/connect` - 쓰레드 연동 시작
- `GET /api/integrations/threads/callback` - 쓰레드 콜백
- `POST /api/integrations/{id}/sync` - 수동 동기화
- `DELETE /api/integrations/{id}` - 연동 해제

### 카테고리
- `GET /api/categories` - 카테고리 목록

## 🔐 환경 변수

```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost:5432/remindlink
# 또는 SQLite로 시작: sqlite:///./remindlink.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Instagram (선택)
INSTAGRAM_USERNAME=your-username
INSTAGRAM_PASSWORD=your-password

# Twitter API
TWITTER_CLIENT_ID=your-client-id
TWITTER_CLIENT_SECRET=your-client-secret
TWITTER_REDIRECT_URI=http://localhost:8000/api/integrations/threads/callback

# 서버
HOST=0.0.0.0
PORT=8000
```

## 📦 설치 필요 항목

1. **Python 3.11 이상**
2. **PostgreSQL** (또는 SQLite로 시작)
3. **Git**
4. **가상환경 도구** (venv)

## 🎯 다음 버전 계획

### v1.1
- 프론트엔드 추가 (React/Next.js)
- 고급 필터 및 검색
- 다양한 뷰 모드

### v1.2
- 클립보드 모니터링 (데스크톱 앱)
- 브라우저 확장 프로그램

### v2.0
- 고급 AI 기능
- 통계 및 인사이트
- 공유 기능

---

**문서 버전**: v1.0  
**최종 업데이트**: 2024-01-12  
**다음 업데이트 예정**: 개발 진행에 따라 v1.1로 업데이트
