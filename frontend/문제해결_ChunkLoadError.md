# ChunkLoadError 해결 가이드

## 문제
```
ChunkLoadError: Loading chunk app/page failed.
```

## 원인
Next.js의 코드 스플리팅된 청크를 로드하지 못하는 문제입니다. 주로:
1. 빌드 캐시 문제
2. webpack 청크 분할 설정 문제
3. SSR과 클라이언트 모듈 충돌 (Three.js 같은 경우)

## 해결 방법

### 1. 빌드 캐시 삭제
```bash
rm -rf .next
rm -rf node_modules/.cache
```

### 2. 동적 임포트 사용 (SSR 비활성화)
Three.js와 같은 클라이언트 전용 라이브러리는 SSR을 비활성화해야 합니다.

`app/page.tsx`에서:
```typescript
import dynamic from 'next/dynamic'

const Graph3D = dynamic(() => import('@/components/Graph3D'), {
  ssr: false,
})
```

### 3. webpack 청크 최적화
`next.config.js`에서 Three.js 관련 모듈을 별도 청크로 분리:

```javascript
config.optimization.splitChunks = {
  cacheGroups: {
    three: {
      name: 'three',
      test: /[\\/]node_modules[\\/](three|react-force-graph-3d)[\\/]/,
      chunks: 'all',
      priority: 20,
    },
  },
}
```

### 4. 서버 재시작
캐시 삭제 후 반드시 서버를 재시작하세요.

## 현재 적용된 해결책

✅ 동적 임포트로 SSR 비활성화
✅ webpack 청크 최적화 설정
✅ 빌드 캐시 삭제

이제 ChunkLoadError가 해결되어야 합니다.
