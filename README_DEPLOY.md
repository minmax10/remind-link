# 🚀 배포 최종 가이드

## ✅ 현재 상태

- ✅ Git 설치 완료
- ✅ Git 저장소 초기화 완료
- ✅ 파일 커밋 완료

## 📋 배포 단계

### Step 1: GitHub 레포지토리 생성

1. **브라우저에서 접속**: https://github.com/new

2. **레포지토리 설정**:
   - Repository name: `remind-link`
   - Description: `인스타그램 저장 게시물 자동 수집 및 분류 서비스`
   - Public 또는 Private 선택
   - ⚠️ **"Initialize this repository with a README" 체크 해제** (중요!)
   - ⚠️ **"Add .gitignore" 선택 안 함**
   - ⚠️ **"Choose a license" 선택 안 함**

3. **"Create repository" 클릭**

### Step 2: GitHub에 푸시

PowerShell에서:

```powershell
cd C:\Users\john\Desktop\re-light\remind-link
.\auto_push_github.ps1
```

스크립트가 다음을 요청합니다:
- GitHub 사용자명 입력

**인증이 필요한 경우:**
- Personal Access Token 사용
- 생성: https://github.com/settings/tokens
- 권한: `repo` 전체 권한
- 비밀번호 대신 토큰 사용

### Step 3: Railway 백엔드 배포

1. **접속**: https://railway.app
2. **로그인**: GitHub 계정으로 로그인
3. **New Project** → **Deploy from GitHub repo**
4. `remind-link` 레포지토리 선택
5. **Settings** → **Root Directory**: `backend`로 변경
6. **Variables** 탭에서 환경 변수 추가:

```
DATABASE_URL=<PostgreSQL URL - 나중에 추가>
SECRET_KEY=<랜덤 문자열 생성>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
```

7. **New** → **Database** → **Add PostgreSQL**
8. PostgreSQL 생성 후 **Connect** 탭에서 `DATABASE_URL` 복사
9. **Variables**에 `DATABASE_URL` 추가
10. 배포 완료 후 URL 확인 (예: `https://remind-link-api.railway.app`)

**SECRET_KEY 생성 방법:**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Vercel 프론트엔드 배포

1. **접속**: https://vercel.com
2. **로그인**: GitHub 계정으로 로그인
3. **Add New Project** 클릭
4. `remind-link` 레포지토리 선택
5. **Configure Project**:
   - **Framework Preset**: Next.js (자동 감지)
   - **Root Directory**: `frontend`로 변경 ⚠️ 중요!
   - **Build Command**: `npm run build` (자동)
   - **Output Directory**: `.next` (자동)

6. **Environment Variables** 섹션:
   ```
   NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
   ```
   (위에서 받은 Railway 백엔드 URL 입력)

7. **Deploy** 클릭
8. 배포 완료 후 URL 확인 (예: `https://remind-link.vercel.app`)

### Step 5: CORS 설정 업데이트

Railway의 **Variables** 탭에서:

```
ALLOWED_ORIGINS=https://remind-link.vercel.app,http://localhost:3000
```

(실제 Vercel 프론트엔드 URL로 변경)

설정 후 Railway에서 **Redeploy** 실행

### Step 6: 데이터베이스 초기화

1. Railway 프로젝트 → **Deployments** → 최신 배포 클릭
2. **View Logs** 옆 **Shell** 탭 클릭
3. 터미널에서:

```bash
cd /app
python init_db.py
```

또는 Railway **Settings** → **Service** → **Start Command** 추가:
```
python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## ✅ 완료!

이제 서비스 사용 가능:
- **프론트엔드**: https://remind-link.vercel.app
- **백엔드 API**: https://remind-link-api.railway.app/docs

## 🔧 문제 해결

### GitHub 푸시 실패
- Personal Access Token 확인
- 레포지토리 이름 확인
- 사용자명 확인

### Railway 배포 실패
- Root Directory가 `backend`인지 확인
- 환경 변수 확인
- 빌드 로그 확인

### Vercel 배포 실패
- Root Directory가 `frontend`인지 확인
- `NEXT_PUBLIC_API_URL` 환경 변수 확인
- 빌드 로그 확인

### CORS 오류
- Railway의 `ALLOWED_ORIGINS`에 프론트엔드 URL 추가
- Railway 재배포

### 데이터베이스 오류
- Railway PostgreSQL이 생성되었는지 확인
- `DATABASE_URL` 환경 변수 확인

## 📝 유용한 링크

- GitHub: https://github.com/your-username/remind-link
- Railway Dashboard: https://railway.app/dashboard
- Vercel Dashboard: https://vercel.com/dashboard

## 🎉 성공!

배포가 완료되면 자동으로 업데이트됩니다:
- GitHub에 푸시 → 자동 재배포
- 환경 변수 변경 → 수동 재배포 필요
