# ✅ 배포 체크리스트

## 배포 전 확인사항

### ✅ 완료된 작업

- [x] GitHub 레포지토리 생성 및 푸시
- [x] 배포 가이드 작성 (`deploy_to_production.md`)
- [x] 인스타그램 연동 가이드 작성 (`INSTAGRAM_SETUP.md`)
- [x] Railway 설정 파일 생성 (`backend/railway.json`)
- [x] Nixpacks 설정 파일 생성 (`backend/nixpacks.toml`)
- [x] Vercel 설정 파일 생성 (`frontend/vercel.json`)
- [x] PostgreSQL 라이브러리 추가 (`psycopg2-binary`)
- [x] 데이터베이스 자동 초기화 설정 (startup 이벤트)

### 📋 배포 시 확인사항

#### Railway 백엔드 배포

- [ ] Railway 계정 생성 및 로그인
- [ ] GitHub 레포지토리 연결: `minmax10/remind-link`
- [ ] Root Directory: `backend` 설정
- [ ] PostgreSQL 데이터베이스 추가
- [ ] 환경 변수 설정:
  - [ ] `DATABASE_URL` (PostgreSQL 연결 URL)
  - [ ] `SECRET_KEY` (JWT 시크릿 키)
  - [ ] `ALGORITHM=HS256`
  - [ ] `ACCESS_TOKEN_EXPIRE_MINUTES=30`
  - [ ] `ALLOWED_ORIGINS` (프론트엔드 URL 포함)
- [ ] 배포 URL 확인 및 저장

#### Vercel 프론트엔드 배포

- [ ] Vercel 계정 생성 및 로그인
- [ ] GitHub 레포지토리 연결: `minmax10/remind-link`
- [ ] Root Directory: `frontend` 설정
- [ ] 환경 변수 설정:
  - [ ] `NEXT_PUBLIC_API_URL` (Railway 백엔드 URL)
- [ ] 배포 URL 확인 및 저장

#### 배포 후 설정

- [ ] Railway CORS 설정 업데이트 (프론트엔드 URL 추가)
- [ ] 데이터베이스 초기화 확인 (자동 실행됨)
- [ ] 프론트엔드에서 백엔드 API 연결 테스트
- [ ] 회원가입/로그인 기능 테스트
- [ ] 인스타그램 연동 기능 테스트

### 🔧 환경 변수 생성

#### SECRET_KEY 생성

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

이 명령어를 실행하여 생성된 값을 `SECRET_KEY`로 사용하세요.

### 📝 배포 URL 기록

배포 완료 후 다음 URL들을 기록하세요:

- **Railway 백엔드 URL**: `https://______________.railway.app`
- **Vercel 프론트엔드 URL**: `https://______________.vercel.app`

### 🚨 문제 해결

배포 중 문제가 발생하면:

1. **Railway 로그 확인**: Railway Dashboard → Deployments → Logs
2. **Vercel 로그 확인**: Vercel Dashboard → Deployments → Logs
3. **환경 변수 확인**: 모든 필수 환경 변수가 설정되었는지 확인
4. **데이터베이스 연결 확인**: PostgreSQL이 생성되고 `DATABASE_URL`이 올바른지 확인
5. **CORS 설정 확인**: `ALLOWED_ORIGINS`에 프론트엔드 URL이 포함되어 있는지 확인

### 📚 참고 문서

- `deploy_to_production.md` - 상세 배포 가이드
- `INSTAGRAM_SETUP.md` - 인스타그램 연동 가이드
