# Remind Link Frontend

옵시디언 스타일의 3D 그래프 뷰를 제공하는 Next.js 프론트엔드 애플리케이션입니다.

## 기능

- 🌐 **3D 그래프 뷰**: 옵시디언 스타일의 인터랙티브 3D 지구본 형태 시각화
- 🎨 **카테고리별 색상**: 각 카테고리별로 다른 색상의 노드 표시
- 🔗 **인터랙티브**: 마우스 드래그로 회전, 스크롤로 줌, 노드 클릭으로 콘텐츠 열기
- 📊 **실시간 데이터**: 백엔드 API와 연동하여 실시간 콘텐츠 표시

## 시작하기

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

### 빌드

```bash
npm run build
npm start
```

## 기술 스택

- **Next.js 14**: React 프레임워크
- **TypeScript**: 타입 안정성
- **Tailwind CSS**: 스타일링
- **react-force-graph-3d**: 3D 그래프 렌더링
- **Three.js**: 3D 그래픽 라이브러리
- **Axios**: HTTP 클라이언트

## 문제 해결

### 빌드 오류: webgpu 모듈을 찾을 수 없음

이 문제는 `three`와 `react-force-graph-3d` 버전 호환성 문제입니다. 
다음 버전을 사용하세요:

```bash
npm install react-force-graph-3d@1.25.0 three@0.160.0
```

### CORS 오류

백엔드 서버의 CORS 설정을 확인하세요. `backend/app/main.py`에서 
`allowed_origins`에 `http://localhost:3000`이 포함되어 있어야 합니다.

## 구조

```
frontend/
├── app/              # Next.js App Router
│   ├── page.tsx      # 메인 페이지 (3D 그래프)
│   └── layout.tsx    # 레이아웃
├── components/        # React 컴포넌트
│   └── Graph3D.tsx   # 3D 그래프 컴포넌트
└── next.config.js    # Next.js 설정
```
