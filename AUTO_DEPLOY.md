# 🚀 자동 배포 가이드

## 현재 상태

✅ Git 저장소 초기화 완료
✅ 파일 커밋 완료

## 다음 단계 (수동 작업 필요)

### 1. GitHub 레포지토리 생성

1. https://github.com 접속
2. 우측 상단 "+" → "New repository" 클릭
3. Repository name: `remind-link`
4. Description: `인스타그램 저장 게시물 자동 수집 및 분류 서비스`
5. Public 또는 Private 선택
6. "Create repository" 클릭
7. 생성된 페이지에서 **HTTPS URL 복사** (예: `https://github.com/your-username/remind-link.git`)

### 2. GitHub에 코드 푸시

PowerShell에서 실행:

```powershell
cd C:\Users\john\Desktop\re-light\remind-link

# 원격 저장소 추가 (위에서 복사한 URL 사용)
git remote add origin https://github.com/your-username/remind-link.git

# 브랜치 이름을 main으로 설정
git branch -M main

# 푸시
git push -u origin main
```

### 3. Railway에 백엔드 배포

1. https://railway.app 접속
2. "Login" → GitHub 계정으로 로그인
3. "New Project" → "Deploy from GitHub repo"
4. `remind-link` 레포지토리 선택
5. **설정:**
   - Root Directory: `backend`
   - Start Command: 자동 감지됨
6. "Variables" 탭에서 환경 변수 추가:
   ```
   DATABASE_URL=<Railway PostgreSQL URL>
   SECRET_KEY=<랜덤 문자열>
   ALLOWED_ORIGINS=http://localhost:3000
   ```
7. "New" → "Database" → "Add PostgreSQL" 클릭
8. PostgreSQL 추가 후 "Connect" 탭에서 `DATABASE_URL` 복사
9. 환경 변수 `DATABASE_URL`에 붙여넣기
10. 배포 완료 후 URL 확인 (예: `https://remind-link-api.railway.app`)

### 4. Vercel에 프론트엔드 배포

1. https://vercel.com 접속
2. "Sign Up" → GitHub 계정으로 로그인
3. "Add New Project" 클릭
4. `remind-link` 레포지토리 선택
5. **설정:**
   - Framework Preset: Next.js (자동)
   - Root Directory: `frontend` 변경
   - Build Command: `npm run build` (자동)
6. "Environment Variables" 섹션에서:
   ```
   NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
   ```
   (위에서 복사한 Railway URL 사용)
7. "Deploy" 클릭
8. 배포 완료 후 URL 확인 (예: `https://remind-link.vercel.app`)

### 5. CORS 설정 업데이트

Railway 환경 변수에서:
```
ALLOWED_ORIGINS=https://remind-link.vercel.app,http://localhost:3000
```
설정 후 Railway에서 "Redeploy" 실행

### 6. 데이터베이스 초기화

Railway 프로젝트 → "Deployments" → 최신 배포 → "Shell" 탭:
```bash
cd /app
python init_db.py
```

## ✅ 완료!

이제 다음 URL에서 접속 가능:
- 프론트엔드: https://remind-link.vercel.app
- 백엔드 API: https://remind-link-api.railway.app/docs

## 🛠️ 빠른 명령어 모음

```powershell
# GitHub 푸시
cd C:\Users\john\Desktop\re-light\remind-link
git remote add origin https://github.com/your-username/remind-link.git
git branch -M main
git push -u origin main

# 이후 코드 변경 시
git add .
git commit -m "Update"
git push
```

## 📝 참고

- GitHub에 푸시하면 Vercel과 Railway가 자동으로 재배포됩니다
- 환경 변수는 각 플랫폼의 설정에서 관리하세요
- PostgreSQL은 Railway에서 무료로 제공됩니다
