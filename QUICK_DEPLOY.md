# 🚀 빠른 배포 가이드 (5분 완성)

## 1단계: GitHub에 코드 업로드

### 1-1. GitHub 레포지토리 생성
1. [GitHub](https://github.com) 접속
2. 우측 상단 "+" → "New repository" 클릭
3. 레포지토리 이름: `remind-link`
4. Public 또는 Private 선택
5. "Create repository" 클릭

### 1-2. 로컬에서 푸시
```bash
cd C:\Users\john\Desktop\re-light\remind-link

# 커밋 (아직 안 했다면)
git add .
git commit -m "Initial commit"

# GitHub 레포지토리 연결 (본인의 레포지토리 URL로 변경)
git remote add origin https://github.com/your-username/remind-link.git

# 브랜치 이름 확인/변경
git branch -M main

# 푸시
git push -u origin main
```

---

## 2단계: 백엔드 배포 (Railway)

### 2-1. Railway 가입 및 프로젝트 생성
1. [Railway](https://railway.app) 접속
2. "Login" → GitHub 계정으로 로그인
3. "New Project" 클릭
4. "Deploy from GitHub repo" 선택
5. `remind-link` 레포지토리 선택

### 2-2. 설정
1. **Root Directory**: `backend` 설정
2. **Start Command**: 자동 감지됨 (없으면 `uvicorn app.main:app --host 0.0.0.0 --port $PORT`)

### 2-3. PostgreSQL 데이터베이스 추가
1. "New" → "Database" → "Add PostgreSQL"
2. 생성 완료 후 "Connect" 탭에서 `DATABASE_URL` 복사

### 2-4. 환경 변수 설정
Railway 프로젝트 → "Variables" 탭에서 추가:

```
DATABASE_URL=<Railway가 제공한 PostgreSQL URL>
SECRET_KEY=<랜덤 문자열, 예: python -c "import secrets; print(secrets.token_urlsafe(32))">
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
```

### 2-5. 배포 URL 확인
Railway 대시보드에서 배포된 서비스 URL 확인 (예: `https://remind-link-api.railway.app`)
이 URL을 복사해두세요!

---

## 3단계: 프론트엔드 배포 (Vercel)

### 3-1. Vercel 가입 및 프로젝트 생성
1. [Vercel](https://vercel.com) 접속
2. "Sign Up" → GitHub 계정으로 로그인
3. "Add New Project" 클릭
4. `remind-link` 레포지토리 선택
5. "Import" 클릭

### 3-2. 설정
- **Framework Preset**: Next.js (자동 감지)
- **Root Directory**: `frontend` 설정
- **Build Command**: `npm run build` (자동)
- **Output Directory**: `.next` (자동)

### 3-3. 환경 변수 추가
"Environment Variables" 섹션에서:
```
NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
```
(위에서 복사한 Railway 백엔드 URL 사용)

### 3-4. 배포
"Deploy" 버튼 클릭 → 자동 배포 시작 (1-2분 소요)

### 3-5. 배포 URL 확인
배포 완료 후 Vercel이 제공하는 URL 확인 (예: `https://remind-link.vercel.app`)

---

## 4단계: CORS 설정 업데이트

Railway 백엔드 환경 변수에서 `ALLOWED_ORIGINS` 업데이트:

```
ALLOWED_ORIGINS=https://remind-link.vercel.app,http://localhost:3000
```

Railway에서 "Redeploy" 실행 (환경 변수 변경 후)

---

## 5단계: 데이터베이스 초기화

### 방법 1: Railway 터미널 사용
1. Railway 프로젝트 → "Deployments" → 최신 배포 클릭
2. "View Logs" 옆 "Shell" 클릭
3. 터미널에서:
```bash
cd /app
python init_db.py
```

### 방법 2: 로컬에서 원격 DB 사용 (임시)
```bash
cd backend
# Railway PostgreSQL URL을 DATABASE_URL로 설정
export DATABASE_URL="postgresql://..."
python init_db.py
```

---

## ✅ 완료!

이제 다음 URL에서 서비스 사용:
- **프론트엔드**: https://remind-link.vercel.app
- **백엔드 API**: https://remind-link-api.railway.app/docs

---

## 🔧 문제 해결

### CORS 오류
- Railway 환경 변수 `ALLOWED_ORIGINS`에 프론트엔드 URL 추가 후 재배포

### 데이터베이스 연결 오류
- Railway PostgreSQL이 생성되었는지 확인
- `DATABASE_URL` 환경 변수 확인

### 빌드 실패
- Vercel 빌드 로그 확인
- `frontend/package.json` 확인
- Root Directory가 `frontend`로 설정되었는지 확인

---

## 📝 추가 설정

### 커스텀 도메인
- Vercel: 프로젝트 → Settings → Domains
- Railway: 프로젝트 → Settings → Domains

### 자동 배포
- GitHub에 푸시하면 자동 재배포됩니다!
