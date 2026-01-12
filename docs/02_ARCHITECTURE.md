# Remind Link - 기술 아키텍처 설계

## 1. 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        사용자 인터페이스                        │
├──────────────┬──────────────┬──────────────┬──────────────┤
│  Web App     │ Desktop App  │  Extension   │  Mobile App  │
│  (React)     │  (Electron)  │  (Chrome)    │  (Future)    │
└──────┬───────┴──────┬────────┴──────┬───────┴──────┬───────┘
       │              │                │              │
       └──────────────┴────────────────┴──────────────┘
                         │
                    ┌────▼─────┐
                    │   API     │
                    │  Gateway  │
                    │ (Express) │
                    └────┬──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐    ┌──────▼──────┐  ┌─────▼─────┐
   │  Auth   │    │   Content   │  │  AI/ML    │
   │ Service │    │   Service   │  │  Service  │
   └─────────┘    └──────┬──────┘  └─────┬─────┘
                         │                │
                    ┌────▼────────────────▼────┐
                    │      Database Layer       │
                    │  ┌──────────┬──────────┐ │
                    │  │PostgreSQL│  Redis   │ │
                    │  └──────────┴──────────┘ │
                    └──────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐    ┌──────▼──────┐  ┌─────▼─────┐
   │External │    │   Scraper   │  │  Storage  │
   │  APIs   │    │   Service   │  │  (S3/CDN) │
   └─────────┘    └─────────────┘  └───────────┘
```

## 2. 기술 스택 상세

### 2.1 Frontend

#### Web Application
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: 
  - React Query (서버 상태)
  - Zustand (클라이언트 상태)
- **Animation**: Framer Motion
- **Form**: React Hook Form + Zod
- **Date**: date-fns

**선택 이유**:
- Next.js: SSR/SSG로 SEO 최적화, API Routes로 풀스택 개발 가능
- TypeScript: 타입 안정성으로 버그 감소
- Tailwind CSS: 빠른 개발, 일관된 디자인
- React Query: 서버 상태 관리 및 캐싱

#### Desktop Application
- **Framework**: Electron + React
- **Language**: TypeScript
- **클립보드 모니터링**: 
  - Windows: `electron-clipboard-watcher`
  - Mac: `clipboardy`
  - Linux: `xclip`

**선택 이유**:
- Electron: 크로스 플랫폼 데스크톱 앱 개발
- 기존 React 코드 재사용 가능

#### Browser Extension
- **Framework**: React + TypeScript
- **Manifest**: Manifest V3
- **Storage**: Chrome Storage API

**선택 이유**:
- 크로스 브라우저 호환성 (Chrome, Edge, Firefox)

### 2.2 Backend

#### API Server
- **Framework**: Node.js + Express 또는 Python + FastAPI
- **Language**: TypeScript 또는 Python
- **Validation**: Zod (Node.js) 또는 Pydantic (Python)
- **Authentication**: JWT + Refresh Token
- **Rate Limiting**: express-rate-limit

**Node.js 선택 시**:
- 프론트엔드와 같은 언어로 풀스택 개발
- npm 생태계 활용

**Python 선택 시**:
- AI/ML 라이브러리 통합 용이
- 웹 스크래핑 라이브러리 풍부 (BeautifulSoup, Scrapy)

#### Database
- **Primary DB**: PostgreSQL
  - 관계형 데이터 구조
  - JSONB 타입으로 유연한 메타데이터 저장
  - Full-text search 지원
- **Cache**: Redis
  - 세션 관리
  - API 응답 캐싱
  - 실시간 알림 큐

**선택 이유**:
- PostgreSQL: 안정적이고 확장 가능한 관계형 DB
- Redis: 빠른 캐싱 및 세션 관리

#### AI/ML Service
- **LLM**: OpenAI GPT-4 또는 Anthropic Claude
- **Framework**: LangChain
- **Vector DB**: (선택) Pinecone 또는 Weaviate (유사 콘텐츠 검색용)

**선택 이유**:
- GPT-4/Claude: 고품질 텍스트 분석 및 분류
- LangChain: LLM 통합 프레임워크

#### Web Scraping
- **Node.js**: Cheerio + Puppeteer
- **Python**: BeautifulSoup + Selenium

**선택 이유**:
- OG 태그 및 메타데이터 추출
- JavaScript 렌더링이 필요한 페이지 처리

### 2.3 Infrastructure

#### Hosting
- **Frontend**: Vercel (Next.js 최적화)
- **Backend**: AWS EC2 또는 Railway
- **Database**: AWS RDS (PostgreSQL) 또는 Supabase
- **Storage**: AWS S3 (이미지 저장)
- **CDN**: CloudFront 또는 Vercel Edge Network

#### DevOps
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry (에러 추적)
- **Analytics**: Google Analytics 또는 Plausible

## 3. 시스템 컴포넌트 상세

### 3.1 API Gateway
**역할**: 모든 클라이언트 요청의 진입점

**기능**:
- 인증/인가 처리
- 요청 라우팅
- Rate limiting
- 요청 로깅

**엔드포인트 구조**:
```
/api/v1/
  ├── auth/          # 인증
  ├── users/         # 사용자 관리
  ├── contents/      # 콘텐츠 CRUD
  ├── categories/    # 카테고리 관리
  ├── tags/          # 태그 관리
  ├── search/        # 검색
  └── integrations/  # 외부 연동
```

### 3.2 Content Service
**역할**: 콘텐츠의 CRUD 및 비즈니스 로직 처리

**주요 기능**:
- 콘텐츠 저장/수정/삭제
- 메타데이터 추출
- 중복 감지
- 통계 집계

### 3.3 AI/ML Service
**역할**: 콘텐츠 분석 및 분류

**주요 기능**:
- 카테고리 분류
- 태그 생성
- 요약 생성
- 유사 콘텐츠 검색

**처리 흐름**:
```
콘텐츠 저장 요청
  ↓
메타데이터 추출 (제목, 설명, 이미지)
  ↓
AI 서비스로 전송
  ↓
분류 + 태그 + 요약 생성
  ↓
결과 저장
```

### 3.4 Scraper Service
**역할**: 외부 링크의 메타데이터 추출

**주요 기능**:
- OG 태그 파싱
- 이미지 다운로드
- 콘텐츠 요약 (선택)
- Favicon 추출

**비동기 처리**:
- 큐 시스템 (Bull 또는 Celery) 사용
- 백그라운드 작업으로 처리

### 3.5 Integration Services
**역할**: 외부 플랫폼 연동

**주요 연동**:
- Instagram Graph API
- Twitter/X API v2
- 클립보드 모니터링 (Desktop App)

## 4. 데이터베이스 스키마 설계

### 4.1 주요 테이블

#### users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### contents
```sql
CREATE TABLE contents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  title VARCHAR(500),
  description TEXT,
  image_url TEXT,
  category_id UUID REFERENCES categories(id),
  source VARCHAR(50), -- 'instagram', 'threads', 'clipboard', 'manual'
  metadata JSONB, -- 플랫폼별 추가 메타데이터
  summary TEXT, -- AI 생성 요약
  reading_time INTEGER, -- 읽기 시간 (분)
  view_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, url) -- 중복 방지
);

CREATE INDEX idx_contents_user_id ON contents(user_id);
CREATE INDEX idx_contents_category_id ON contents(category_id);
CREATE INDEX idx_contents_created_at ON contents(created_at DESC);
CREATE INDEX idx_contents_url ON contents USING gin(url gin_trgm_ops); -- Full-text search
```

#### categories
```sql
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  icon VARCHAR(50),
  color VARCHAR(7), -- HEX color
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### tags
```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, name)
);

CREATE INDEX idx_tags_user_id ON tags(user_id);
```

#### content_tags (Many-to-Many)
```sql
CREATE TABLE content_tags (
  content_id UUID REFERENCES contents(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (content_id, tag_id)
);
```

#### integrations
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
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, platform)
);
```

## 5. API 설계 원칙

### 5.1 RESTful API
- 리소스 중심 설계
- HTTP 메서드 적절히 사용 (GET, POST, PUT, DELETE, PATCH)
- 상태 코드 명확히 사용

### 5.2 응답 형식
```json
{
  "success": true,
  "data": { ... },
  "message": "Success",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

에러 응답:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": { ... }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 5.3 인증
- JWT 토큰 기반 인증
- Access Token: 15분 만료
- Refresh Token: 7일 만료
- HTTP-only Cookie에 Refresh Token 저장

## 6. 보안 고려사항

### 6.1 데이터 보안
- 비밀번호: bcrypt 해싱
- API 키: 환경 변수로 관리
- SQL Injection 방지: ORM 또는 파라미터화된 쿼리 사용
- XSS 방지: 입력 데이터 검증 및 이스케이프

### 6.2 인증 보안
- HTTPS 필수
- CORS 설정
- Rate limiting
- CSRF 토큰 (필요시)

### 6.3 프라이버시
- 클립보드 데이터는 로컬에서만 처리
- 사용자 데이터 암호화 저장
- GDPR 준수 (유럽 사용자)

## 7. 성능 최적화

### 7.1 캐싱 전략
- Redis를 활용한 API 응답 캐싱
- 정적 콘텐츠 CDN 캐싱
- 브라우저 캐싱 (Cache-Control 헤더)

### 7.2 데이터베이스 최적화
- 인덱스 최적화
- 쿼리 최적화
- Connection pooling

### 7.3 프론트엔드 최적화
- 코드 스플리팅
- 이미지 최적화 (WebP, lazy loading)
- Virtual scrolling (대량 데이터)

## 8. 확장성 고려사항

### 8.1 수평 확장
- 로드 밸런서로 여러 서버 인스턴스 운영
- 데이터베이스 읽기 전용 복제본
- 마이크로서비스 아키텍처로 전환 가능

### 8.2 비동기 처리
- 큐 시스템으로 무거운 작업 처리
- 웹 스크래핑, AI 분석 등은 백그라운드 작업

### 8.3 모니터링
- 로그 집계 (ELK Stack 또는 CloudWatch)
- 메트릭 수집 (Prometheus + Grafana)
- 에러 추적 (Sentry)
