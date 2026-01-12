# Remind Link - 빠른 시작 가이드

## 🚀 5분 안에 시작하기

### 1단계: 환경 설정
```powershell
# 프로젝트 폴더로 이동
cd C:\Users\john\Desktop\re-light\remind-link\backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 환경 변수 설정
```powershell
# .env 파일 생성
copy env.example .env
```

`.env` 파일을 열어서 최소한 다음 값만 설정:
```env
DATABASE_URL=sqlite:///./remindlink.db
SECRET_KEY=your-super-secret-key-min-32-characters-long
```

### 3단계: 데이터베이스 초기화
```powershell
python init_db.py
```

### 4단계: 서버 실행
```powershell
uvicorn app.main:app --reload
```

### 5단계: 테스트
브라우저에서 http://localhost:8000/docs 접속

## ✅ 확인 사항

서버가 정상 실행되면:
- ✅ http://localhost:8000 - 루트 엔드포인트
- ✅ http://localhost:8000/api/health - 헬스 체크
- ✅ http://localhost:8000/docs - Swagger UI

## 🧪 첫 API 테스트

### 1. 회원가입
```bash
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "test1234",
  "name": "테스트 사용자"
}
```

### 2. 로그인
```bash
POST http://localhost:8000/api/auth/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=test1234
```

응답에서 `access_token` 복사

### 3. 콘텐츠 추가
```bash
POST http://localhost:8000/api/contents
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://example.com/article",
  "source": "manual"
}
```

### 4. 콘텐츠 목록 조회
```bash
GET http://localhost:8000/api/contents
Authorization: Bearer {access_token}
```

## 📝 다음 단계

1. ✅ 기본 API 작동 확인
2. 🔄 인스타그램 연동 구현 (다음 세션)
3. 🔄 쓰레드 연동 구현 (다음 세션)
4. 🔄 AI 분류 기능 추가

## ❗ 문제 해결

### 포트가 이미 사용 중
```powershell
uvicorn app.main:app --reload --port 8001
```

### 모듈을 찾을 수 없음
```powershell
# 가상환경이 활성화되어 있는지 확인
# 터미널 앞에 (venv) 표시가 있어야 함
```

### 데이터베이스 오류
```powershell
# 데이터베이스 파일 삭제 후 재초기화
del remindlink.db
python init_db.py
```

---

**더 자세한 내용은 [SETUP.md](./SETUP.md) 참고**
