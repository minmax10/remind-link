# Remind Link 배포 가이드

## 배포 옵션

### 1. 프론트엔드 배포 (Next.js)

#### Vercel (권장) - Next.js에 최적화
1. GitHub에 코드 푸시
2. [Vercel](https://vercel.com) 접속
3. "Add New Project" 클릭
4. GitHub 레포지토리 선택
5. 프레임워크 자동 감지 (Next.js)
6. 환경 변수 추가:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```
7. Deploy 클릭

**장점:**
- Next.js에 최적화
- 자동 HTTPS
- 글로벌 CDN
- 무료 플랜 제공

#### Netlify
1. GitHub에 코드 푸시
2. [Netlify](https://netlify.com) 접속
3. "Add new site" → "Import an existing project"
4. GitHub 레포지토리 선택
5. 빌드 설정:
   - Build command: `npm run build`
   - Publish directory: `.next`
6. 환경 변수 추가

#### GitHub Pages
- Next.js는 정적 내보내기 필요
- API 서버가 필요하므로 권장하지 않음

---

### 2. 백엔드 배포 (FastAPI)

#### Railway (권장) - 간단하고 빠름
1. [Railway](https://railway.app) 접속
2. "New Project" → "Deploy from GitHub"
3. 백엔드 레포지토리 선택
4. 환경 변수 설정:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-secret-key
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```
5. 자동 배포 시작

**장점:**
- PostgreSQL 무료 제공
- 간단한 설정
- 자동 HTTPS
- 무료 플랜 제공 ($5 크레딧/월)

#### Render
1. [Render](https://render.com) 접속
2. "New" → "Web Service"
3. GitHub 레포지토리 연결
4. 빌드 명령: `pip install -r requirements.txt`
5. 시작 명령: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. 환경 변수 설정

#### Fly.io
1. [Fly.io](https://fly.io) CLI 설치
2. `fly launch` 실행
3. PostgreSQL 추가: `fly postgres create`
4. 환경 변수 연결

---

## 전체 배포 절차

### 1. GitHub에 코드 푸시
```bash
cd remind-link
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/remind-link.git
git push -u origin main
```

### 2. 백엔드 배포 (Railway 예시)
1. Railway에서 프로젝트 생성
2. PostgreSQL 데이터베이스 추가
3. 환경 변수 설정:
   ```
   DATABASE_URL=<Railway가 제공하는 PostgreSQL URL>
   SECRET_KEY=<랜덤 문자열 생성>
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   INSTAGRAM_USERNAME=
   INSTAGRAM_PASSWORD=
   ```
4. 배포 URL 확인 (예: https://remind-link-api.railway.app)

### 3. 프론트엔드 배포 (Vercel 예시)
1. Vercel에서 프로젝트 생성
2. 환경 변수 설정:
   ```
   NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
   ```
3. 배포 URL 확인 (예: https://remind-link.vercel.app)

### 4. CORS 설정 확인
백엔드의 `ALLOWED_ORIGINS`에 프론트엔드 URL 추가

---

## 환경 변수 목록

### 백엔드 (.env)
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
```

### 프론트엔드 (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

---

## 무료 플랜 한계

### Vercel
- 대역폭: 100GB/월
- 함수 실행 시간: 제한적
- **충분함**

### Railway
- 월 $5 크레딧
- 소규모 프로젝트에 충분
- **충분함**

### Render
- 무료 플랜은 15분 비활성화 시 슬리프
- **개인 프로젝트에는 적합**

---

## 로컬 성능 개선

### 현재 적용된 개선 사항:
1. ✅ 불필요한 console.log 제거
2. ✅ Next.js 최적화 설정 (swcMinify)
3. ✅ 프로덕션에서 console 제거
4. ✅ 환경 변수로 API URL 관리

### 추가 개선 방법:
1. **프로덕션 빌드 사용:**
   ```bash
   npm run build
   npm start
   ```

2. **개발 모드 최적화:**
   - 이미 적용됨 (swcMinify)

3. **이미지 최적화:**
   - Next.js Image 컴포넌트 사용 (필요 시)

---

## 문제 해결

### 로그인 화면이 느린 경우
1. 개발 모드 대신 프로덕션 빌드 사용
2. 브라우저 캐시 확인
3. 네트워크 탭에서 요청 시간 확인

### 배포 후 CORS 오류
- 백엔드 `ALLOWED_ORIGINS`에 프론트엔드 URL 추가

### 데이터베이스 연결 오류
- 배포 플랫폼의 환경 변수 확인
- DATABASE_URL 형식 확인
