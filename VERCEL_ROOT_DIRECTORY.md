# 🔧 Vercel Root Directory 설정 방법

## Root Directory란?

Root Directory는 Vercel이 코드를 빌드할 때 어느 폴더를 기준으로 할지 지정하는 설정입니다.

우리 프로젝트는 다음과 같은 구조입니다:
```
remind-link/
├── backend/     ← 백엔드 코드
├── frontend/    ← 프론트엔드 코드 (여기!)
└── docs/
```

따라서 **Vercel 배포 시**: Root Directory를 `frontend`로 설정해야 합니다

---

## Vercel에서 Root Directory 설정하는 방법

### 1단계: 프로젝트 추가

1. https://vercel.com/new 접속
2. GitHub로 로그인
3. "Import Git Repository"에서 `minmax10/remind-link` 검색 후 선택
4. "Import" 클릭

### 2단계: 프로젝트 설정 화면에서 Root Directory 설정

프로젝트 설정 화면이 나타납니다:

1. **"Configure Project"** 섹션에서
2. **"Root Directory"** 항목 찾기 (기본값은 `.` 또는 비어있음)
3. **입력란 옆의 "Edit" 버튼 클릭** (또는 직접 클릭)
4. `frontend` 입력
5. 설정 확인 후 **"Deploy" 버튼 클릭**

### 위치 설명

- 프로젝트 설정 화면의 왼쪽 또는 상단에 있습니다
- "Framework Preset", "Build Command" 등과 같은 섹션에 있습니다
- 드롭다운이나 입력 필드 형태로 되어 있습니다

---

## 확인 방법

Root Directory가 올바르게 설정되었는지 확인:

1. 배포 전: 설정 화면에서 Root Directory가 `frontend`로 표시되는지 확인
2. 배포 후: Project Settings → General → Root Directory 확인
3. 빌드 로그에서:
   - `Installing dependencies in frontend` 같은 메시지 확인
   - 빌드 경로가 `frontend/`로 시작하는지 확인

---

## 문제 해결

### Root Directory를 설정했는데도 빌드가 실패하는 경우

1. 설정 화면에서 Root Directory가 정확히 `frontend`로 입력되었는지 확인 (앞뒤 공백 없이)
2. 배포 로그 확인 (Deployments → 최신 배포 → Build Logs)
3. Project Settings → General에서 Root Directory 재확인

### Root Directory 설정이 보이지 않는 경우

1. 프로젝트를 처음 추가할 때 설정 화면에서 찾기
2. 이미 배포된 경우: Project Settings → General에서 수정 가능
3. 브라우저 새로고침

---

## 배포 후 Root Directory 변경하기

이미 배포된 프로젝트의 Root Directory를 변경하려면:

1. Vercel 대시보드에서 프로젝트 선택
2. **Settings 탭 클릭**
3. **General 섹션**으로 스크롤
4. **"Root Directory" 항목 찾기**
5. "Edit" 클릭 후 `frontend` 입력
6. **"Save" 클릭**
7. 새 배포가 자동으로 시작됩니다

---

## 참고

- Vercel은 Root Directory 설정을 변경하면 자동으로 새 배포를 시작합니다
- Root Directory를 설정하지 않으면 루트 디렉토리(`.`)를 기준으로 빌드합니다
- 우리 프로젝트는 `frontend` 폴더 안에 Next.js 코드가 있으므로 반드시 `frontend`로 설정해야 합니다
