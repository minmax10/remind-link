# Vercel Root Directory 설정 방법

## 문제

Vercel에서 레포지토리를 추가할 때 "프로젝트 설정 화면"에서 Root Directory를 찾지 못하는 경우가 있습니다.

## 해결 방법

### 방법 1: 레포지토리 추가 시 설정 (가장 쉬움)

1. https://vercel.com 접속
2. GitHub로 로그인
3. **"Add New..." 버튼 클릭** (또는 "Add New Project")
4. 레포지토리 검색: `minmax10/remind-link`
5. 레포지토리 선택
6. **"Configure Project" 버튼 클릭** (또는 자동으로 설정 화면으로 이동)
7. **"Root Directory" 입력란 찾기**:
   - "Framework Preset" 아래에 있음
   - 또는 "Build and Output Settings" 섹션에 있음
   - 기본값은 `.` (점 하나) 또는 비어있음
8. **`frontend` 입력**
9. **"Deploy" 버튼 클릭**

### 방법 2: 배포 후 Settings에서 변경

1. Vercel 대시보드에서 프로젝트 선택
2. **"Settings" 탭 클릭**
3. **"General" 섹션** 찾기
4. **"Root Directory" 항목** 찾기
5. **"Edit" 버튼 클릭**
6. **`frontend` 입력**
7. **"Save" 버튼 클릭**
8. **"Redeploy" 실행**

### 방법 3: vercel.json 파일 사용 (자동 인식)

프로젝트 루트에 `vercel.json` 파일을 만들면 자동으로 인식됩니다:

```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next",
  "installCommand": "cd frontend && npm install"
}
```

하지만 Root Directory 설정이 더 간단합니다.

---

## ⚠️ 중요

- Root Directory를 `frontend`로 설정하지 않으면 빌드가 실패합니다!
- Vercel은 Root Directory 내에서 `package.json`을 찾아 Next.js를 감지합니다.
- `frontend` 디렉토리 안에 `package.json`이 있어야 합니다.

---

## 찾기 어려운 경우

1. **Ctrl+F (또는 Cmd+F)**로 "Root Directory" 검색
2. **"Configure Project" 섹션**을 아래로 스크롤
3. **"Build and Output Settings" 섹션** 확인
4. **"Framework Preset" 옆** 확인

---

## ✅ 완료!

Root Directory를 `frontend`로 설정하면:
- Vercel이 `frontend/package.json`을 찾음
- Next.js 프로젝트로 자동 감지
- `frontend` 디렉토리에서 빌드 실행
- 배포가 정상적으로 진행됨
