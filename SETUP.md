# Remind Link - 설치 가이드

## 📋 필수 설치 항목

### 1. Python 설치

#### Windows
1. [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.11 이상 다운로드
2. 설치 시 **"Add Python to PATH"** 체크 필수!
3. 설치 확인:
```powershell
python --version
# Python 3.11.x 이상이어야 함
```

### 2. PostgreSQL 설치 (선택사항)

#### 옵션 A: PostgreSQL 설치
1. [PostgreSQL 공식 사이트](https://www.postgresql.org/download/windows/)에서 다운로드
2. 설치 중 비밀번호 설정 (기억해두세요!)
3. 설치 확인:
```powershell
psql --version
```

#### 옵션 B: SQLite 사용 (간단하게 시작)
- Python에 기본 포함되어 있음
- 별도 설치 불필요

### 3. Git 설치
1. [Git 공식 사이트](https://git-scm.com/download/win)에서 다운로드
2. 설치 확인:
```powershell
git --version
```

## 🚀 프로젝트 설정

### 1. 프로젝트 폴더로 이동
```powershell
cd C:\Users\john\Desktop\re-light\remind-link
```

### 2. Python 가상환경 생성
```powershell
python -m venv venv
```

### 3. 가상환경 활성화
```powershell
.\venv\Scripts\Activate.ps1
```

만약 실행 정책 오류가 발생하면:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. 의존성 설치
```powershell
cd backend
pip install -r requirements.txt
```

### 5. 환경 변수 설정
```powershell
# .env 파일 생성 (backend 폴더에)
copy .env.example .env
```

`.env` 파일을 열어서 필요한 값들을 입력하세요:
```env
# 데이터베이스 (SQLite로 시작하는 경우)
DATABASE_URL=sqlite:///./remindlink.db

# 또는 PostgreSQL 사용하는 경우
# DATABASE_URL=postgresql://user:password@localhost:5432/remindlink

# JWT 시크릿 키 (랜덤 문자열 생성)
SECRET_KEY=your-super-secret-key-change-this-in-production

# OpenAI API 키 (선택사항, 나중에 추가 가능)
OPENAI_API_KEY=your-openai-api-key

# Twitter API (나중에 추가)
TWITTER_CLIENT_ID=
TWITTER_CLIENT_SECRET=
TWITTER_REDIRECT_URI=http://localhost:8000/api/integrations/threads/callback
```

### 6. 데이터베이스 초기화
```powershell
# 기본 카테고리 데이터 삽입
python init_db.py
```

### 7. 서버 실행
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면:
- API 문서: http://localhost:8000/docs
- 대체 문서: http://localhost:8000/redoc

## 🔑 API 키 발급 가이드

### OpenAI API 키 (AI 분류용)
1. [OpenAI Platform](https://platform.openai.com/) 접속
2. 계정 생성 또는 로그인
3. API Keys 메뉴에서 새 키 생성
4. `.env` 파일에 `OPENAI_API_KEY` 추가

### Twitter API 키 (쓰레드 연동용)
1. [Twitter Developer Portal](https://developer.twitter.com/) 접속
2. 개발자 계정 신청 (승인 필요, 시간 소요)
3. 새 앱 생성
4. OAuth 2.0 설정:
   - Callback URL: `http://localhost:8000/api/integrations/threads/callback`
   - App permissions: `bookmarks.read` 권한 필요
5. Client ID와 Client Secret 발급
6. `.env` 파일에 추가

### Instagram (선택사항)
- 공식 API는 저장된 게시물 접근 불가
- 웹 스크래핑 방식 사용 시 별도 API 키 불필요
- instagrapi 사용 시 계정 정보만 필요

## 🧪 테스트

### API 테스트
```powershell
# 서버 실행 후
curl http://localhost:8000/api/health
```

또는 브라우저에서:
- http://localhost:8000/docs 접속
- Swagger UI에서 직접 테스트 가능

## ❗ 문제 해결

### Python이 인식되지 않을 때
- PATH 환경 변수에 Python 추가
- 또는 전체 경로 사용: `C:\Python311\python.exe`

### 가상환경 활성화 오류
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 포트가 이미 사용 중일 때
```powershell
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

### 데이터베이스 연결 오류
- PostgreSQL 사용 시: 서비스가 실행 중인지 확인
- SQLite 사용 시: 파일 경로 확인

## 📚 다음 단계

1. 서버가 정상 실행되면 `/docs`에서 API 테스트
2. 회원가입/로그인 테스트
3. 인스타그램/쓰레드 연동 테스트

---

**문제가 발생하면**: 프로젝트 이슈에 등록하거나 문서를 확인하세요.
