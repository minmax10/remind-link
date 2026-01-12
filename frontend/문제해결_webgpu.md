# webgpu 모듈 오류 해결 가이드

## 문제
```
Module not found: Package path ./webgpu is not exported from package three
```

## 원인
`react-force-graph-3d`의 의존성인 `three-render-objects`가 `three/webgpu`를 import하려고 하지만, 
`three@0.160.0` 버전에서는 webgpu가 export되지 않습니다.

## 해결 방법

### 방법 1: webpack 설정으로 webgpu import 무시 (현재 적용됨)

`next.config.js`에서 webpack 설정을 통해 `three/webgpu` import를 스텁 모듈로 대체합니다.

### 방법 2: three 버전 업그레이드 (권장하지 않음)

```bash
npm install three@latest
```

하지만 이 경우 `react-force-graph-3d`와 호환성 문제가 발생할 수 있습니다.

### 방법 3: react-force-graph-3d 버전 다운그레이드

```bash
npm install react-force-graph-3d@1.24.0
```

### 방법 4: 다른 라이브러리 사용

- `@react-three/fiber` + `@react-three/drei` 직접 사용
- `vis-network` 사용

## 현재 적용된 해결책

1. `webpack.webgpu-stub.js`: 빈 모듈로 webgpu import 대체
2. `NormalModuleReplacementPlugin`: webgpu import를 스텁으로 교체
3. `IgnorePlugin`: webgpu import 완전히 무시

이 설정으로 빌드 오류가 해결되어야 합니다.
