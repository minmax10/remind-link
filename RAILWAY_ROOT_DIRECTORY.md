# 🔧 Railway Root Directory 설정 방법

## Root Directory란?

Root Directory는 Railway가 코드를 빌드할 때 어느 폴더를 기준으로 할지 지정하는 설정입니다.

우리 프로젝트는 다음과 같은 구조입니다:
```
remind-link/
├── backend/     ← 여기가 백엔드 코드
├── frontend/    ← 여기가 프론트엔드 코드
└── docs/
```

따라서:
- **Railway 배포 시**: Root Directory를 `backend`로 설정해야 합니다
- **Vercel 배포 시**: Root Directory를 `frontend`로 설정해야 합니다

---

## Railway에서 Root Directory 설정하는 방법

### 1단계: 프로젝트 배포 시작

1. https://railway.app/new 접속
2. GitHub로 로그인
3. "GitHub Repository" 선택
4. `minmax10/remind-link` 레포지토리 선택
5. "Deploy" 클릭

### 2단계: Settings 탭에서 Root Directory 설정

배포가 시작되면 프로젝트 대시보드가 표시됩니다.

1. 상단 메뉴에서 **"Settings" 탭 클릭**
2. Settings 페이지에서 아래로 스크롤
3. **"Root Directory"** 항목 찾기
4. 입력란에 `backend` 입력
5. **"Update" 또는 "Save" 버튼 클릭**

### 3단계: 재배포

Root Directory를 변경한 후:
1. 상단 메뉴에서 **"Deployments" 탭 클릭**
2. 최신 배포 옆의 **"..." 메뉴 클릭**
3. **"Redeploy" 선택**

또는 자동으로 재배포될 수도 있습니다.

---

## 확인 방법

Root Directory가 올바르게 설정되었는지 확인:

1. Settings 탭에서 Root Directory가 `backend`로 표시되는지 확인
2. Deployments 탭에서 로그 확인:
   - 로그에 `/app/backend` 또는 `/app` 경로가 보여야 합니다
   - `uvicorn app.main:app` 같은 명령어가 실행되어야 합니다

---

## 문제 해결

### Root Directory를 설정했는데도 배포가 실패하는 경우

1. Settings에서 Root Directory가 정확히 `backend`로 입력되었는지 확인 (앞뒤 공백 없이)
2. 재배포를 수동으로 실행
3. Deployments → Logs에서 오류 메시지 확인

### Root Directory 설정이 보이지 않는 경우

1. 프로젝트가 완전히 배포된 후 Settings 탭을 확인
2. 브라우저 새로고침 (F5)
3. 다른 브라우저에서 시도

---

## 참고

- Railway는 Root Directory 설정을 변경하면 자동으로 재배포를 시작합니다
- Root Directory를 설정하지 않으면 루트 디렉토리(`.`)를 기준으로 빌드합니다
- 우리 프로젝트는 `backend` 폴더 안에 코드가 있으므로 반드시 `backend`로 설정해야 합니다
