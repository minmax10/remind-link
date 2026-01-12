# 🚀 배포 상태

## ⚠️ 자동 배포 제한사항

Railway와 Vercel 배포는 웹 브라우저를 통한 **로그인과 인증**이 필요합니다.
따라서 완전 자동화는 불가능하며, 아래 가이드를 따라 수동으로 진행해야 합니다.

## 📋 배포 가이드

### Railway 백엔드 배포

1. **접속**: https://railway.app/new
2. **로그인**: GitHub 계정으로 로그인
3. **레포지토리 선택**: `minmax10/remind-link`
4. **설정**:
   - Root Directory: `backend`
   - PostgreSQL 데이터베이스 추가
   - 환경 변수 설정 (가이드 참고)

### Vercel 프론트엔드 배포

1. **접속**: https://vercel.com/new
2. **로그인**: GitHub 계정으로 로그인
3. **레포지토리 선택**: `minmax10/remind-link`
4. **설정**:
   - Root Directory: `frontend`
   - 환경 변수 설정 (Railway URL 사용)

## 📝 상세 가이드

- `deploy_to_production.md` - 단계별 배포 가이드
- `DEPLOYMENT_CHECKLIST.md` - 배포 체크리스트
