# Remind Link - API 명세서

## 1. 기본 정보

- **Base URL**: `https://api.remindlink.com/v1`
- **인증**: JWT Bearer Token
- **Content-Type**: `application/json`

## 2. 인증 API

### 2.1 회원가입
```http
POST /auth/register
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "홍길동"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "홍길동"
    },
    "tokens": {
      "accessToken": "jwt_token",
      "refreshToken": "refresh_token"
    }
  }
}
```

### 2.2 로그인
```http
POST /auth/login
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "홍길동"
    },
    "tokens": {
      "accessToken": "jwt_token",
      "refreshToken": "refresh_token"
    }
  }
}
```

### 2.3 토큰 갱신
```http
POST /auth/refresh
```

**Request Body**:
```json
{
  "refreshToken": "refresh_token"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "accessToken": "new_jwt_token",
    "refreshToken": "new_refresh_token"
  }
}
```

### 2.4 로그아웃
```http
POST /auth/logout
```

**Headers**:
```
Authorization: Bearer {accessToken}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## 3. 콘텐츠 API

### 3.1 콘텐츠 목록 조회
```http
GET /contents
```

**Query Parameters**:
- `page` (number, default: 1): 페이지 번호
- `limit` (number, default: 20): 페이지당 항목 수
- `category` (string, optional): 카테고리 필터
- `tag` (string, optional): 태그 필터
- `source` (string, optional): 출처 필터 (instagram, threads, clipboard, manual)
- `search` (string, optional): 검색어
- `sort` (string, default: "created_at"): 정렬 기준 (created_at, updated_at, view_count)
- `order` (string, default: "desc"): 정렬 순서 (asc, desc)
- `fromDate` (string, optional): 시작 날짜 (ISO 8601)
- `toDate` (string, optional): 종료 날짜 (ISO 8601)

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "contents": [
      {
        "id": "uuid",
        "url": "https://example.com/article",
        "title": "Article Title",
        "description": "Article description",
        "imageUrl": "https://example.com/image.jpg",
        "category": {
          "id": "uuid",
          "name": "기술/개발",
          "slug": "technology",
          "icon": "code",
          "color": "#3B82F6"
        },
        "tags": [
          {"id": "uuid", "name": "React"},
          {"id": "uuid", "name": "TypeScript"}
        ],
        "source": "clipboard",
        "summary": "이 글은 React와 TypeScript를 사용한...",
        "readingTime": 5,
        "viewCount": 10,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

### 3.2 콘텐츠 상세 조회
```http
GET /contents/:id
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "url": "https://example.com/article",
    "title": "Article Title",
    "description": "Article description",
    "imageUrl": "https://example.com/image.jpg",
    "category": {
      "id": "uuid",
      "name": "기술/개발",
      "slug": "technology"
    },
    "tags": [
      {"id": "uuid", "name": "React"},
      {"id": "uuid", "name": "TypeScript"}
    ],
    "source": "clipboard",
    "metadata": {
      "author": "John Doe",
      "publishedAt": "2024-01-01"
    },
    "summary": "이 글은 React와 TypeScript를 사용한...",
    "readingTime": 5,
    "viewCount": 10,
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

### 3.3 콘텐츠 추가
```http
POST /contents
```

**Request Body**:
```json
{
  "url": "https://example.com/article",
  "categoryId": "uuid", // optional, AI가 자동 분류
  "tags": ["React", "TypeScript"], // optional
  "source": "manual" // manual, clipboard, instagram, threads
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "url": "https://example.com/article",
    "title": "Article Title",
    "description": "Article description",
    "imageUrl": "https://example.com/image.jpg",
    "category": {
      "id": "uuid",
      "name": "기술/개발",
      "slug": "technology"
    },
    "tags": [
      {"id": "uuid", "name": "React"},
      {"id": "uuid", "name": "TypeScript"}
    ],
    "source": "manual",
    "summary": "이 글은 React와 TypeScript를 사용한...",
    "readingTime": 5,
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

**처리 흐름**:
1. URL 유효성 검증
2. 중복 체크 (동일 URL이 이미 저장되어 있는지)
3. 메타데이터 추출 (Scraper Service)
4. AI 분류 (카테고리, 태그, 요약 생성)
5. 데이터베이스 저장

### 3.4 콘텐츠 수정
```http
PATCH /contents/:id
```

**Request Body**:
```json
{
  "title": "Updated Title", // optional
  "description": "Updated description", // optional
  "categoryId": "uuid", // optional
  "tags": ["React", "Vue"], // optional
  "notes": "Personal notes" // optional
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Updated Title",
    "description": "Updated description",
    "category": {
      "id": "uuid",
      "name": "기술/개발"
    },
    "tags": [
      {"id": "uuid", "name": "React"},
      {"id": "uuid", "name": "Vue"}
    ],
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

### 3.5 콘텐츠 삭제
```http
DELETE /contents/:id
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Content deleted successfully"
}
```

### 3.6 콘텐츠 조회수 증가
```http
POST /contents/:id/view
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "viewCount": 11
  }
}
```

## 4. 카테고리 API

### 4.1 카테고리 목록 조회
```http
GET /categories
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "기술/개발",
      "slug": "technology",
      "icon": "code",
      "color": "#3B82F6",
      "contentCount": 25
    },
    {
      "id": "uuid",
      "name": "디자인/아트",
      "slug": "design",
      "icon": "palette",
      "color": "#EC4899",
      "contentCount": 15
    }
  ]
}
```

### 4.2 사용자별 카테고리 통계
```http
GET /categories/stats
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "category": {
        "id": "uuid",
        "name": "기술/개발",
        "slug": "technology"
      },
      "count": 25,
      "percentage": 35.7
    }
  ]
}
```

## 5. 태그 API

### 5.1 태그 목록 조회
```http
GET /tags
```

**Query Parameters**:
- `search` (string, optional): 태그 검색
- `limit` (number, default: 50): 최대 개수

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "React",
      "contentCount": 10
    },
    {
      "id": "uuid",
      "name": "TypeScript",
      "contentCount": 8
    }
  ]
}
```

### 5.2 태그 자동완성
```http
GET /tags/autocomplete
```

**Query Parameters**:
- `q` (string, required): 검색어

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {"id": "uuid", "name": "React"},
    {"id": "uuid", "name": "React Native"}
  ]
}
```

## 6. 검색 API

### 6.1 통합 검색
```http
GET /search
```

**Query Parameters**:
- `q` (string, required): 검색어
- `page` (number, default: 1)
- `limit` (number, default: 20)
- `category` (string, optional): 카테고리 필터
- `tag` (string, optional): 태그 필터

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "contents": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 50,
      "totalPages": 3
    }
  }
}
```

## 7. 통합 연동 API

### 7.1 연동 목록 조회
```http
GET /integrations
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "platform": "instagram",
      "isActive": true,
      "lastSyncAt": "2024-01-01T00:00:00Z",
      "syncStatus": "success"
    },
    {
      "id": "uuid",
      "platform": "threads",
      "isActive": false,
      "lastSyncAt": null,
      "syncStatus": null
    }
  ]
}
```

### 7.2 인스타그램 연동 시작
```http
POST /integrations/instagram/connect
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "authUrl": "https://api.instagram.com/oauth/authorize?..."
  }
```

### 7.3 인스타그램 연동 콜백
```http
GET /integrations/instagram/callback
```

**Query Parameters**:
- `code` (string): OAuth 인증 코드

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "integration": {
      "id": "uuid",
      "platform": "instagram",
      "isActive": true
    }
  }
}
```

### 7.4 수동 동기화
```http
POST /integrations/:id/sync
```

**Response** (202 Accepted):
```json
{
  "success": true,
  "message": "Sync started",
  "data": {
    "jobId": "uuid"
  }
}
```

### 7.5 연동 해제
```http
DELETE /integrations/:id
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Integration disconnected"
}
```

## 8. 통계 API

### 8.1 대시보드 통계
```http
GET /stats/dashboard
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "totalContents": 150,
    "totalCategories": 8,
    "totalTags": 45,
    "contentsThisMonth": 25,
    "mostUsedCategory": {
      "id": "uuid",
      "name": "기술/개발",
      "count": 50
    },
    "recentActivity": [
      {
        "date": "2024-01-01",
        "count": 5
      }
    ]
  }
}
```

## 9. 에러 응답

### 에러 코드
- `VALIDATION_ERROR`: 입력 데이터 검증 실패
- `UNAUTHORIZED`: 인증 실패
- `FORBIDDEN`: 권한 없음
- `NOT_FOUND`: 리소스를 찾을 수 없음
- `DUPLICATE_CONTENT`: 중복 콘텐츠
- `RATE_LIMIT_EXCEEDED`: 요청 한도 초과
- `INTERNAL_ERROR`: 서버 내부 오류

### 에러 응답 예시
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid URL format",
    "details": {
      "field": "url",
      "message": "URL must be a valid HTTP/HTTPS URL"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 10. Rate Limiting

- **일반 API**: 100 requests/minute
- **인증 API**: 10 requests/minute
- **검색 API**: 30 requests/minute

Rate limit 초과 시:
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1609459200
```
