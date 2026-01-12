# 🚀 프로덕션 배포 가이드

## 배포 상태

✅ GitHub 푸시 완료
✅ 레포지토리: https://github.com/minmax10/remind-link

## 배포 순서

### 1단계: Railway 백엔드 배포

1. **접속**: https://railway.app/new
2. **로그인**: "Login" 버튼 클릭 → GitHub 계정으로 로그인
3. **"GitHub Repository" 선택** (드롭다운 메뉴에서)
4. **레포지토리 검색 및 선택**: `minmax10/remind-link` 검색 후 선택
5. **"Deploy" 버튼 클릭**
6. **배포가 시작되면 → Settings 탭 클릭**
7. **Root Directory 설정**:

   - Settings 페이지에서 **"Root Directory"** 항목 찾기
   - 입력란에 `backend` 입력
   - **"Update" 또는 "Save" 버튼 클릭**
   - ⚠️ 중요: Root Directory를 `backend`로 설정하지 않으면 배포가 실패합니다!

8. **PostgreSQL 데이터베이스 추가**:

   - **New** → **Database** → **Add PostgreSQL**
   - 생성 완료 후 **Connect** 탭에서 `DATABASE_URL` 복사

9. **환경 변수 설정** (Variables 탭):

   ```
   DATABASE_URL=<PostgreSQL URL (위에서 복사)>
   SECRET_KEY=<랜덤 문자열 생성>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALLOWED_ORIGINS=http://localhost:3000
   PYTHONIOENCODING=utf-8
   LC_ALL=C.UTF-8
   LANG=C.UTF-8
   INSTAGRAM_USERNAME=
   INSTAGRAM_PASSWORD=
   ```
   
   ⚠️ **중요**: `PYTHONIOENCODING`, `LC_ALL`, `LANG` 환경 변수를 추가해야 한글이 깨지지 않습니다!

   **SECRET_KEY 생성 방법**:

   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

10. **배포 완료 후 URL 확인** (예: `https://remind-link-api.railway.app`)
    - 이 URL을 복사해두세요!

---

### 2단계: Vercel 프론트엔드 배포

1. **접속**: https://vercel.com
2. **로그인**: GitHub 계정으로 로그인
3. **Add New Project** 클릭
4. **레포지토리 선택**: `minmax10/remind-link`
5. **프로젝트 설정 화면**:

   - **"Configure Project"** 섹션에서
   - **"Root Directory"** 찾기 (기본값은 `.` 또는 비어있음)
   - **Root Directory에 `frontend` 입력** ⚠️ 중요!
   - **Framework Preset**: Next.js (자동 감지됨)
   - **Build Command**: `npm run build` (자동)
   - **Output Directory**: `.next` (자동)

6. **Environment Variables** 섹션:

   ```
   NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
   ```

   (위에서 복사한 Railway 백엔드 URL 사용)

7. **Deploy** 클릭
8. **배포 완료 후 URL 확인** (예: `https://remind-link.vercel.app`)
   - 이 URL을 복사해두세요!

---

### 3단계: CORS 설정 업데이트

Railway 백엔드의 **Variables** 탭에서:

```
ALLOWED_ORIGINS=https://remind-link.vercel.app,http://localhost:3000
```

(실제 Vercel 프론트엔드 URL로 변경)

설정 후 Railway에서 **Redeploy** 실행

---

### 4단계: 데이터베이스 초기화

1. Railway 프로젝트 → **Deployments** → 최신 배포 클릭
2. **View Logs** 옆 **Shell** 탭 클릭
3. 터미널에서:

```bash
cd /app
python init_db.py
```

또는 Railway **Settings** → **Service** → **Start Command** 수정:

```
python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## ✅ 배포 완료 확인

### 백엔드 확인

- API 문서: `https://remind-link-api.railway.app/docs`
- Health check: `https://remind-link-api.railway.app/api/health`

### 프론트엔드 확인

- 메인 페이지: `https://remind-link.vercel.app`

---

## 📱 인스타그램 연동 사용 방법

### 1. 회원가입/로그인

1. 프론트엔드 URL 접속: `https://remind-link.vercel.app`
2. "회원가입" 탭 클릭
3. 이름, 이메일, 비밀번호 입력
4. "회원가입" 버튼 클릭
5. 자동으로 로그인되어 메인 페이지로 이동

### 2. 인스타그램 연동

1. 메인 페이지에서 **"인스타그램 연동"** 버튼 클릭
2. 인스타그램 사용자명과 비밀번호 입력
   - ⚠️ **2단계 인증이 활성화된 경우 앱 비밀번호 사용 필요**
3. **"연동하기"** 버튼 클릭
4. 연동 완료 확인

### 3. 저장된 게시물 동기화

1. 메인 페이지에서 **"동기화"** 버튼 클릭
2. 저장된 게시물 자동 수집
3. 게시물 목록 표시

---

## 🔐 인스타그램 앱 비밀번호 생성 (2단계 인증 활성화 시)

1. 인스타그램 앱에서 **프로필** → **설정**
2. **보안** → **2단계 인증**
3. **앱 비밀번호**
4. **새 앱 비밀번호 만들기**
5. 앱 이름 입력 (예: "Remind Link")
6. 생성된 비밀번호 복사 (연동 시 사용)

---

## 🔧 문제 해결

### CORS 오류

- Railway `ALLOWED_ORIGINS`에 프론트엔드 URL 추가
- Railway 재배포

### 데이터베이스 연결 오류

- Railway PostgreSQL이 생성되었는지 확인
- `DATABASE_URL` 환경 변수 확인

### 빌드 실패

- Vercel 빌드 로그 확인
- Root Directory가 `frontend`인지 확인
- `NEXT_PUBLIC_API_URL` 환경 변수 확인

### 인스타그램 로그인 실패

- 사용자명과 비밀번호 확인
- 2단계 인증 활성화 시 앱 비밀번호 사용
- 인스타그램 계정 상태 확인

---

## 📝 환경 변수 정리

### Railway (백엔드)

```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://remind-link.vercel.app,http://localhost:3000
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
```

### Vercel (프론트엔드)

```env
NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
```

---

## ✅ 완료!

이제 서비스 사용 가능:

- **프론트엔드**: https://remind-link.vercel.app
- **백엔드 API**: https://remind-link-api.railway.app/docs
- **인스타그램 연동**: 프론트엔드에서 연동 버튼 클릭
