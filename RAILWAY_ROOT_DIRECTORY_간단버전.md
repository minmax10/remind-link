# 🔧 Railway Root Directory - 간단 가이드

## ⚠️ 중요: Railway에서 Root Directory는 두 가지 위치에 있을 수 있습니다

### 방법 1: 프로젝트 추가 시 (가장 쉬움!)

레포지토리를 추가할 때 바로 설정하는 것이 가장 쉽습니다:

1. https://railway.app/new 접속
2. GitHub로 로그인
3. "GitHub Repository" 선택
4. `minmax10/remind-link` 레포지토리 선택
5. **레포지토리를 선택하면 설정 화면이 나타납니다**
6. **"Root Directory" 입력란에 `backend` 입력**
7. "Deploy" 클릭

**이 방법이 가장 쉽습니다!**

---

### 방법 2: 이미 배포된 프로젝트에서 (Settings에서)

만약 이미 배포했다면:

1. Railway 대시보드에서 **프로젝트 클릭**
2. **서비스(Service) 클릭** (보통 프로젝트 이름과 동일)
3. **"Settings" 탭 클릭**
4. Settings 페이지를 **아래로 스크롤**
5. **"Source" 또는 "Build" 섹션 찾기**
6. **"Root Directory" 입력란에 `backend` 입력**
7. **"Save" 클릭**

---

## 🔍 찾기 어려운 경우

### Ctrl+F로 검색하세요!

1. Settings 페이지에서 **Ctrl+F (또는 Cmd+F)** 누르기
2. **"Root Directory"** 검색
3. 검색 결과 클릭하면 바로 이동!

### 또는

1. Settings 페이지에서 **Ctrl+F (또는 Cmd+F)** 누르기
2. **"Source"** 검색
3. Source 섹션 안에 Root Directory가 있습니다

---

## 💡 팁

- **가장 쉬운 방법**: 레포지토리를 처음 추가할 때 Root Directory 설정
- **이미 배포했다면**: Settings → Source 섹션에서 찾기
- **찾기 어렵다면**: Ctrl+F로 "Root Directory" 또는 "Source" 검색

---

## 🚨 여전히 못 찾는다면

Railway UI가 업데이트되어 위치가 변경되었을 수 있습니다.

**대안:**
1. 프로젝트를 삭제하고 다시 추가할 때 Root Directory 설정
2. 또는 Railway 지원팀에 문의: support@railway.app
