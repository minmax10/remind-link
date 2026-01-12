# 🤖 자동 배포 실행 가이드

## ✅ 완료된 작업

1. Git 저장소 초기화
2. 파일 커밋 준비
3. 배포 스크립트 생성

## 🚀 다음 단계

### Step 1: GitHub 레포지토리 생성

1. 브라우저에서 https://github.com/new 접속
2. Repository name: `remind-link` 입력
3. Description: `인스타그램 저장 게시물 자동 수집 및 분류 서비스`
4. Public 또는 Private 선택
5. **"Initialize this repository with a README" 체크 해제** (이미 코드가 있으므로)
6. "Create repository" 클릭

### Step 2: GitHub에 푸시

PowerShell에서 실행:

```powershell
cd C:\Users\john\Desktop\re-light\remind-link
.\push_to_github.ps1
```

또는 수동으로:

```powershell
# GitHub 레포지토리 URL을 확인한 후
git remote add origin https://github.com/your-username/remind-link.git
git branch -M main
git push -u origin main
```

**인증 필요 시:**
- Personal Access Token 생성: https://github.com/settings/tokens
- "repo" 권한 선택
- 토큰을 비밀번호처럼 사용

### Step 3: Railway 백엔드 배포

1. https://railway.app 접속
2. "Login" → GitHub 로그인
3. "New Project" → "Deploy from GitHub repo"
4. `remind-link` 선택
5. **중요:** Settings → Root Directory를 `backend`로 변경
6. "Variables" 탭:
   ```
   DATABASE_URL=<PostgreSQL URL>
   SECRET_KEY=<랜덤 문자열>
   ALLOWED_ORIGINS=http://localhost:3000
   ```
7. "New" → "Database" → "Add PostgreSQL"
8. PostgreSQL의 "Connect" 탭에서 DATABASE_URL 복사
9. Variables에 DATABASE_URL 추가
10. 배포 완료 후 URL 확인

### Step 4: Vercel 프론트엔드 배포

1. https://vercel.com 접속
2. "Sign Up" → GitHub 로그인
3. "Add New Project"
4. `remind-link` 선택
5. **중요:** Root Directory를 `frontend`로 변경
6. Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=<Railway에서 받은 백엔드 URL>
   ```
7. "Deploy" 클릭
8. 배포 완료 후 URL 확인

### Step 5: CORS 업데이트

Railway Variables에서:
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```
설정 후 Redeploy

### Step 6: 데이터베이스 초기화

Railway → Deployments → 최신 배포 → Shell:
```bash
cd /app
python init_db.py
```

## ✅ 완료!

이제 서비스 사용 가능:
- 프론트엔드: https://your-app.vercel.app
- 백엔드 API: https://your-api.railway.app/docs

## 🛠️ 문제 해결

### Git 인증 오류
- Personal Access Token 사용
- 또는 SSH 키 설정

### 배포 실패
- Root Directory 확인 (backend/frontend)
- 환경 변수 확인
- 빌드 로그 확인

### CORS 오류
- ALLOWED_ORIGINS에 프론트엔드 URL 추가
- Railway 재배포
