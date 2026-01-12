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

   Railway Variables 탭에서 다음 변수들을 추가하세요:
   
   ```
   DATABASE_URL=<PostgreSQL URL (위 8번에서 복사)>
   SECRET_KEY=4I96Crx9dSTMUO8ZcimdLCQ6eO4k1xY8uxO9QlN51TA
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALLOWED_ORIGINS=http://localhost:3000
   PYTHONIOENCODING=utf-8
   LC_ALL=C.UTF-8
   LANG=C.UTF-8
   ```
   
   ⚠️ **참고**:
   - `DATABASE_URL`은 PostgreSQL 추가 후 Connect 탭에서 복사
   - `INSTAGRAM_USERNAME`과 `INSTAGRAM_PASSWORD`는 나중에 사용자 화면에서 입력
   - 환경 변수는 `환경변수_일괄복사.txt` 파일에서 복사 가능

10. **배포 완료 후 URL 확인** (예: `https://remind-link-api.railway.app`)
    - 이 URL을 복사해두세요!

---

### 2단계: Vercel 프론트엔드 배포

1. **접속**: https://vercel.com
2. **로그인**: GitHub 계정으로 로그인
3. **"Add New..." 버튼 클릭** (또는 "Add New Project")
4. **레포지토리 검색 및 선택**: `minmax10/remind-link` 검색 후 선택
5. **프로젝트 설정 화면에서 "Configure Project" 클릭**

6. **Root Directory 설정** (⚠️ 중요!):

   - **"Root Directory"** 입력란 찾기
   - 입력란 옆에 **"Edit" 버튼**이 있을 수 있음
   - 또는 바로 입력 가능
   - **`frontend` 입력**
   - **"Deploy" 버튼 클릭**

   ```
   NEXT_PUBLIC_API_URL=https://remind-link-api.railway.app
   ```

   (위에서 복사한 Railway 백엔드 URL 사용)

8. **Deploy** 클릭
9. **배포 완료 후 URL 확인** (예: `https://remind-link.vercel.app`)
   - 이 URL을 복사해두세요!

---

## 📝 수동 배포 방법

### Railway 수동 배포

1. Railway 대시보드에서 프로젝트 선택
2. **Deployments** 탭 클릭
3. **"Redeploy" 버튼** 클릭 (최신 커밋으로 재배포)
4. 또는 **"Manual Deploy" 버튼** 클릭 (특정 커밋 선택)

### Vercel 수동 배포

1. Vercel 대시보드에서 프로젝트 선택
2. **Deployments** 탭 클릭
3. **"Redeploy" 버튼** 클릭 (최신 커밋으로 재배포)
4. 또는 특정 배포 옆 **"..." 메뉴** → **"Redeploy"**

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
PYTHONIOENCODING=utf-8
LC_ALL=C.UTF-8
LANG=C.UTF-8
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
```

⚠️ **한글 깨짐 방지**: `PYTHONIOENCODING`, `LC_ALL`, `LANG` 환경 변수 필수!

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
