# Remind Link - 데이터 모델 상세 설계

## 1. ERD (Entity Relationship Diagram)

```
┌─────────────┐
│    users    │
├─────────────┤
│ id (PK)     │
│ email       │
│ password    │
│ name        │
│ avatar_url  │
│ created_at  │
│ updated_at  │
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼──────────┐      ┌──────────────┐
│   contents      │      │  categories  │
├─────────────────┤      ├──────────────┤
│ id (PK)         │      │ id (PK)      │
│ user_id (FK)    │──────│ name         │
│ url             │ N:1  │ slug         │
│ title           │      │ icon         │
│ description     │      │ color        │
│ image_url       │      │ is_default   │
│ category_id(FK) │      └──────────────┘
│ source          │
│ metadata        │
│ summary         │
│ reading_time    │
│ view_count      │
│ created_at      │
│ updated_at      │
└──────┬──────────┘
       │
       │ N:M
       │
┌──────▼──────────┐      ┌──────────────┐
│  content_tags   │      │     tags     │
├─────────────────┤      ├──────────────┤
│ content_id (FK) │──────│ id (PK)      │
│ tag_id (FK)     │ N:1  │ user_id (FK) │
└─────────────────┘      │ name         │
                          │ created_at   │
                          └──────────────┘

┌─────────────┐
│ integrations│
├─────────────┤
│ id (PK)     │
│ user_id(FK) │
│ platform    │
│ access_token│
│ refresh_token│
│ expires_at  │
│ last_sync_at│
│ is_active   │
└─────────────┘
```

## 2. 테이블 상세 설계

### 2.1 users 테이블

**목적**: 사용자 정보 저장

**스키마**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  avatar_url TEXT,
  email_verified BOOLEAN DEFAULT false,
  email_verification_token VARCHAR(255),
  reset_password_token VARCHAR(255),
  reset_password_expires TIMESTAMP,
  last_login_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_email_verification_token ON users(email_verification_token);
```

**필드 설명**:
- `id`: 사용자 고유 ID (UUID)
- `email`: 이메일 주소 (로그인 ID)
- `password_hash`: bcrypt로 해싱된 비밀번호
- `name`: 사용자 이름
- `avatar_url`: 프로필 이미지 URL
- `email_verified`: 이메일 인증 여부
- `email_verification_token`: 이메일 인증 토큰
- `reset_password_token`: 비밀번호 재설정 토큰
- `reset_password_expires`: 비밀번호 재설정 토큰 만료 시간
- `last_login_at`: 마지막 로그인 시간

### 2.2 categories 테이블

**목적**: 콘텐츠 카테고리 정의

**스키마**:
```sql
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  icon VARCHAR(50),
  color VARCHAR(7), -- HEX color code
  description TEXT,
  is_default BOOLEAN DEFAULT false,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_categories_slug ON categories(slug);
```

**기본 카테고리 데이터**:
```sql
INSERT INTO categories (name, slug, icon, color, is_default, sort_order) VALUES
('기술/개발', 'technology', 'code', '#3B82F6', true, 1),
('디자인/아트', 'design', 'palette', '#EC4899', true, 2),
('비즈니스/경제', 'business', 'briefcase', '#10B981', true, 3),
('뉴스/시사', 'news', 'newspaper', '#F59E0B', true, 4),
('엔터테인먼트', 'entertainment', 'film', '#8B5CF6', true, 5),
('교육/학습', 'education', 'book', '#06B6D4', true, 6),
('건강/라이프스타일', 'health', 'heart', '#EF4444', true, 7),
('여행/음식', 'travel', 'map', '#F97316', true, 8),
('기타', 'other', 'folder', '#6B7280', true, 9);
```

### 2.3 contents 테이블

**목적**: 사용자가 저장한 콘텐츠 정보

**스키마**:
```sql
CREATE TABLE contents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  title VARCHAR(500),
  description TEXT,
  image_url TEXT,
  favicon_url TEXT,
  category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  source VARCHAR(50) NOT NULL, -- 'instagram', 'threads', 'clipboard', 'manual', 'browser'
  metadata JSONB DEFAULT '{}', -- 플랫폼별 추가 메타데이터
  summary TEXT, -- AI 생성 요약
  reading_time INTEGER, -- 읽기 시간 (분)
  view_count INTEGER DEFAULT 0,
  is_archived BOOLEAN DEFAULT false,
  is_favorite BOOLEAN DEFAULT false,
  notes TEXT, -- 사용자 메모
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, url) -- 동일 사용자의 중복 URL 방지
);

CREATE INDEX idx_contents_user_id ON contents(user_id);
CREATE INDEX idx_contents_category_id ON contents(category_id);
CREATE INDEX idx_contents_source ON contents(source);
CREATE INDEX idx_contents_created_at ON contents(created_at DESC);
CREATE INDEX idx_contents_is_archived ON contents(is_archived);
CREATE INDEX idx_contents_is_favorite ON contents(is_favorite);
CREATE INDEX idx_contents_url_trgm ON contents USING gin(url gin_trgm_ops); -- Full-text search
CREATE INDEX idx_contents_title_trgm ON contents USING gin(title gin_trgm_ops);
CREATE INDEX idx_contents_description_trgm ON contents USING gin(description gin_trgm_ops);
```

**metadata JSONB 예시**:
```json
{
  "instagram": {
    "postId": "123456789",
    "author": "@username",
    "caption": "Post caption...",
    "imageUrls": ["url1", "url2"]
  },
  "threads": {
    "tweetId": "123456789",
    "author": "@username",
    "text": "Tweet text...",
    "mediaUrls": ["url1"]
  },
  "og": {
    "siteName": "Example Site",
    "type": "article",
    "author": "John Doe",
    "publishedTime": "2024-01-01T00:00:00Z"
  }
}
```

### 2.4 tags 테이블

**목적**: 콘텐츠 태그

**스키마**:
```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  color VARCHAR(7), -- HEX color (선택사항)
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, name) -- 사용자별 태그 이름 중복 방지
);

CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name_trgm ON tags USING gin(name gin_trgm_ops);
```

### 2.5 content_tags 테이블

**목적**: 콘텐츠와 태그의 다대다 관계

**스키마**:
```sql
CREATE TABLE content_tags (
  content_id UUID NOT NULL REFERENCES contents(id) ON DELETE CASCADE,
  tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (content_id, tag_id)
);

CREATE INDEX idx_content_tags_content_id ON content_tags(content_id);
CREATE INDEX idx_content_tags_tag_id ON content_tags(tag_id);
```

### 2.6 integrations 테이블

**목적**: 외부 플랫폼 연동 정보

**스키마**:
```sql
CREATE TABLE integrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  platform VARCHAR(50) NOT NULL, -- 'instagram', 'threads', 'pinterest', etc.
  access_token TEXT,
  refresh_token TEXT,
  token_expires_at TIMESTAMP,
  platform_user_id VARCHAR(255), -- 외부 플랫폼의 사용자 ID
  platform_username VARCHAR(255), -- 외부 플랫폼의 사용자명
  last_sync_at TIMESTAMP,
  sync_status VARCHAR(50), -- 'success', 'failed', 'pending'
  sync_error_message TEXT,
  is_active BOOLEAN DEFAULT true,
  settings JSONB DEFAULT '{}', -- 플랫폼별 설정
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, platform) -- 사용자별 플랫폼당 하나의 연동만 허용
);

CREATE INDEX idx_integrations_user_id ON integrations(user_id);
CREATE INDEX idx_integrations_platform ON integrations(platform);
CREATE INDEX idx_integrations_is_active ON integrations(is_active);
```

**settings JSONB 예시**:
```json
{
  "autoSync": true,
  "syncInterval": 3600, // seconds
  "syncOnlyNew": true
}
```

### 2.7 sync_jobs 테이블 (선택사항)

**목적**: 동기화 작업 추적

**스키마**:
```sql
CREATE TABLE sync_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  integration_id UUID NOT NULL REFERENCES integrations(id) ON DELETE CASCADE,
  status VARCHAR(50) NOT NULL, -- 'pending', 'running', 'completed', 'failed'
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  items_synced INTEGER DEFAULT 0,
  items_failed INTEGER DEFAULT 0,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sync_jobs_integration_id ON sync_jobs(integration_id);
CREATE INDEX idx_sync_jobs_status ON sync_jobs(status);
```

## 3. 데이터 관계

### 3.1 사용자와 콘텐츠
- **관계**: 1:N (한 사용자는 여러 콘텐츠 보유)
- **CASCADE**: 사용자 삭제 시 모든 콘텐츠 삭제

### 3.2 콘텐츠와 카테고리
- **관계**: N:1 (여러 콘텐츠가 하나의 카테고리)
- **NULL 허용**: 카테고리가 없을 수 있음
- **SET NULL**: 카테고리 삭제 시 콘텐츠의 카테고리는 NULL

### 3.3 콘텐츠와 태그
- **관계**: N:M (다대다)
- **중간 테이블**: content_tags
- **CASCADE**: 콘텐츠 또는 태그 삭제 시 관계 삭제

### 3.4 사용자와 태그
- **관계**: 1:N (한 사용자는 여러 태그 보유)
- **CASCADE**: 사용자 삭제 시 모든 태그 삭제

### 3.5 사용자와 연동
- **관계**: 1:N (한 사용자는 여러 플랫폼 연동 가능)
- **제약**: 사용자당 플랫폼당 하나의 연동만 허용 (UNIQUE)

## 4. 인덱스 전략

### 4.1 기본 인덱스
- 모든 외래키에 인덱스 생성
- 자주 조회되는 컬럼에 인덱스 (created_at, source 등)

### 4.2 Full-text Search 인덱스
- PostgreSQL의 GIN 인덱스 사용
- url, title, description에 트라이그램 인덱스

### 4.3 복합 인덱스
```sql
-- 사용자별 최신 콘텐츠 조회
CREATE INDEX idx_contents_user_created ON contents(user_id, created_at DESC);

-- 사용자별 카테고리별 콘텐츠 조회
CREATE INDEX idx_contents_user_category ON contents(user_id, category_id);

-- 아카이브되지 않은 최신 콘텐츠
CREATE INDEX idx_contents_active ON contents(user_id, is_archived, created_at DESC) 
WHERE is_archived = false;
```

## 5. 데이터 무결성 제약조건

### 5.1 UNIQUE 제약조건
- `users.email`: 이메일 중복 방지
- `users.email_verification_token`: 인증 토큰 고유성
- `categories.slug`: 카테고리 슬러그 고유성
- `contents(user_id, url)`: 사용자별 URL 중복 방지
- `tags(user_id, name)`: 사용자별 태그 이름 중복 방지
- `integrations(user_id, platform)`: 사용자별 플랫폼당 하나의 연동

### 5.2 CHECK 제약조건
```sql
-- URL 형식 검증
ALTER TABLE contents ADD CONSTRAINT check_url_format 
CHECK (url ~ '^https?://');

-- 읽기 시간은 0 이상
ALTER TABLE contents ADD CONSTRAINT check_reading_time 
CHECK (reading_time >= 0);

-- 조회수는 0 이상
ALTER TABLE contents ADD CONSTRAINT check_view_count 
CHECK (view_count >= 0);
```

### 5.3 외래키 제약조건
- 모든 외래키에 CASCADE 또는 SET NULL 설정
- 참조 무결성 보장

## 6. 데이터 마이그레이션 전략

### 6.1 초기 스키마 생성
- 모든 테이블 생성
- 기본 카테고리 데이터 삽입
- 인덱스 생성

### 6.2 스키마 변경
- 마이그레이션 파일로 관리
- 롤백 가능한 마이그레이션
- 데이터 손실 없는 변경

## 7. 데이터 백업 전략

### 7.1 정기 백업
- 일일 자동 백업
- 주간 전체 백업
- 월간 아카이브 백업

### 7.2 백업 저장소
- AWS S3 또는 Google Cloud Storage
- 암호화된 백업
- 여러 리전에 복제

## 8. 성능 최적화

### 8.1 파티셔닝 (대규모 데이터)
- 날짜별 파티셔닝 (contents 테이블)
- 사용자별 파티셔닝 (선택사항)

### 8.2 아카이빙
- 오래된 콘텐츠는 별도 테이블로 이동
- `is_archived` 플래그로 소프트 삭제

### 8.3 캐싱
- Redis에 자주 조회되는 데이터 캐싱
- 카테고리 목록
- 사용자별 통계
