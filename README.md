# Remind Link

인스타그램과 쓰레드에 저장한 게시물을 자동으로 수집하고 분류하는 서비스

## 🚀 빠른 시작

### 로컬 개발

#### 백엔드
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python init_db.py
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

#### 프론트엔드
```bash
cd frontend
npm install
npm run dev
```

### 서버 재기동
```powershell
.\restart_all.ps1
```

### 서버 종료
```powershell
.\stop_all.ps1
```

## 📦 배포

자세한 배포 가이드는 [DEPLOYMENT.md](./DEPLOYMENT.md)를 참고하세요.

### 빠른 배포

1. **GitHub에 푸시**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/remind-link.git
git push -u origin main
```

2. **Vercel에 프론트엔드 배포**
   - [Vercel](https://vercel.com) 접속
   - GitHub 레포지토리 연결
   - Root Directory: `frontend`
   - 환경 변수: `NEXT_PUBLIC_API_URL=https://your-backend-url.com`

3. **Railway에 백엔드 배포**
   - [Railway](https://railway.app) 접속
   - New Project → Deploy from GitHub
   - Root Directory: `backend`
   - 환경 변수 설정 (DEPLOYMENT.md 참고)

## 🛠️ 기술 스택

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy, SQLite/PostgreSQL
- **Auth**: JWT
- **Integration**: instagrapi (Instagram)

## 📝 주요 기능

- ✅ 사용자 인증 (회원가입/로그인)
- ✅ 인스타그램 저장 게시물 수집
- ✅ 콘텐츠 자동 분류
- ✅ 카테고리 관리
- ✅ 검색 및 필터링

## 📄 API 문서

로컬 개발 시: http://localhost:8000/docs

## 🔧 환경 변수

### Backend (.env)
```env
DATABASE_URL=sqlite:///./remindlink.db
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=http://localhost:3000
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 문서

- [프로젝트 기획](./docs/01_PROJECT_PLANNING.md)
- [아키텍처](./docs/02_ARCHITECTURE.md)
- [API 명세](./docs/03_API_SPEC.md)
- [배포 가이드](./DEPLOYMENT.md)

## 📄 라이선스

MIT
