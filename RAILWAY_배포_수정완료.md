# ✅ Railway 배포 설정 수정 완료!

## 문제점

Railway에서 레포지토리를 선택하면 바로 배포가 시작되고, Settings에 Source 섹션이 없어서 Root Directory를 설정할 수 없었습니다.

## 해결 방법

Railway 설정 파일을 프로젝트 루트로 이동하고, `backend` 디렉토리로 자동 이동하도록 수정했습니다.

### 변경 사항

1. **railway.json** 파일을 프로젝트 루트로 이동
2. **nixpacks.toml** 파일을 프로젝트 루트로 이동
3. 설정 파일에서 `cd backend &&` 명령어로 backend 디렉토리로 이동하도록 설정

### 결과

이제 **Root Directory를 수동으로 설정할 필요가 없습니다!**

Railway가 프로젝트 루트의 `railway.json` 파일을 자동으로 인식하고, 설정에 따라 `backend` 디렉토리로 이동하여 배포합니다.

---

## 🚀 새로운 배포 방법 (매우 간단!)

### 1단계: Railway에서 레포지토리 추가

1. https://railway.app/new 접속
2. GitHub로 로그인
3. "GitHub Repository" 선택
4. `minmax10/remind-link` 레포지토리 선택
5. **"Deploy" 클릭** (또는 자동으로 배포 시작)

**끝!** Root Directory 설정 불필요!

Railway가 자동으로:
- 프로젝트 루트의 `railway.json` 파일 인식
- `backend` 디렉토리로 이동
- `requirements.txt` 설치
- `uvicorn app.main:app` 실행

---

## 📋 나머지 설정 (배포 후)

배포가 시작된 후 다음 설정만 하면 됩니다:

### PostgreSQL 데이터베이스 추가

1. Railway 대시보드에서 프로젝트 클릭
2. **"New" 버튼 클릭** → **"Database"** → **"Add PostgreSQL"**
3. 생성 완료 후 **"Connect" 탭**에서 `DATABASE_URL` 복사

### 환경 변수 설정

1. 프로젝트 대시보드에서 **"Variables" 탭 클릭**
2. 다음 환경 변수 추가:

```
DATABASE_URL=<PostgreSQL URL (위에서 복사)>
SECRET_KEY=<랜덤 문자열 생성>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

**SECRET_KEY 생성 방법:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## ✅ 완료!

이제 Railway 배포가 훨씬 간단해졌습니다!

- ✅ Root Directory 수동 설정 불필요
- ✅ railway.json 파일이 자동으로 인식됨
- ✅ backend 디렉토리 자동 인식
- ✅ 배포가 자동으로 진행됨
