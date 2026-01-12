# ✅ Railway 배포 최종 설정

## 문제점

Railway에서 Root Directory를 `/backend`로 설정했는데도 "Railpack could not determine how to build the app" 에러가 발생했습니다.

## 해결 방법

Railway는 Root Directory 내에서 `nixpacks.toml` 파일을 찾아 Python 프로젝트를 자동으로 감지합니다. `railway.json` 파일은 선택사항이며, 때로는 충돌을 일으킬 수 있습니다.

### 최종 설정

1. **Root Directory**: `/backend` (Railway Settings에서 설정)
2. **설정 파일**: `backend/nixpacks.toml`만 사용
3. **railway.json**: 제거 (nixpacks.toml이 더 명확함)

### nixpacks.toml 구조

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = [
    "pip install --upgrade pip",
    "pip install -r requirements.txt"
]

[start]
cmd = "PYTHONIOENCODING=utf-8 LC_ALL=C.UTF-8 LANG=C.UTF-8 python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

---

## 🚀 배포 방법

1. **Railway Settings에서 Root Directory 확인**:
   - Settings 탭 → Root Directory: `/backend`

2. **배포 시작**:
   - Railway가 자동으로 `backend/nixpacks.toml` 파일을 찾음
   - Python 프로젝트로 자동 감지
   - `requirements.txt` 설치
   - 설정된 명령어로 실행

---

## 📋 환경 변수 설정 (Variables 탭)

배포 후 다음 환경 변수를 추가하세요:

```
DATABASE_URL=<PostgreSQL URL>
SECRET_KEY=<랜덤 문자열>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
PYTHONIOENCODING=utf-8
LC_ALL=C.UTF-8
LANG=C.UTF-8
```

---

## ✅ 완료!

- ✅ Root Directory: `/backend`
- ✅ nixpacks.toml: `backend/nixpacks.toml`
- ✅ Python 자동 감지
- ✅ UTF-8 인코딩 설정
- ✅ 한글 깨짐 방지
