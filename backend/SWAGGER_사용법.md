# Swagger UI 사용법 (한글 가이드)

## 🔐 OAuth2 인증 화면이란?

Swagger UI에서 보이는 "OAuth2PasswordBearer" 화면은 **API 인증을 위한 로그인 화면**입니다.

### 화면 설명

```
Scopes (스코프): 애플리케이션에 부여할 데이터 접근 권한 수준
- 각 API는 하나 이상의 스코프를 선언할 수 있습니다

OAuth2PasswordBearer (OAuth2, password)
- 인증 방식: 비밀번호 기반 인증
- 토큰 URL: /api/auth/login
- 플로우: password (비밀번호 방식)
```

### 사용 방법

1. **"Authorize" 버튼 클릭**
   - Swagger UI 페이지 상단 오른쪽의 자물쇠 아이콘 또는 "Authorize" 버튼 클릭

2. **로그인 정보 입력**
   - **사용자명 (username)**: 이메일 주소 입력
     - 예: `user@example.com`
   - **비밀번호 (password)**: 비밀번호 입력

3. **"Authorize" 버튼 클릭**
   - 입력한 정보로 로그인하고 토큰을 받습니다

4. **토큰 자동 저장**
   - 토큰이 자동으로 저장되어 이후 모든 API 호출에 사용됩니다
   - 페이지를 새로고침해도 토큰이 유지됩니다 (persistAuthorization 설정)

### 주의사항

- **사용자명 = 이메일**: OAuth2PasswordRequestForm은 `username` 필드를 사용하지만, 우리 시스템에서는 이메일을 사용합니다
- **토큰 만료**: 토큰은 30분 후 만료됩니다 (설정에서 변경 가능)
- **토큰 수동 사용**: 토큰을 직접 복사하여 사용하려면:
  ```javascript
  // 브라우저 콘솔에서
  localStorage.setItem('access_token', '받은토큰')
  ```

### 문제 해결

**"401 Unauthorized" 오류가 발생하는 경우:**
1. 이메일과 비밀번호가 올바른지 확인
2. 먼저 `/api/auth/register`로 회원가입했는지 확인
3. 토큰이 만료되었는지 확인 (다시 로그인)

**토큰을 수동으로 설정하는 방법:**
1. `/api/auth/login` API를 직접 호출하여 토큰 받기
2. 받은 `access_token` 값을 복사
3. 브라우저 콘솔에서:
   ```javascript
   localStorage.setItem('access_token', '여기에토큰붙여넣기')
   ```

## 📝 API 사용 순서

1. **회원가입** (`POST /api/auth/register`)
   - 이메일, 비밀번호, 이름 입력
   - 새 계정 생성

2. **로그인** (`POST /api/auth/login` 또는 Authorize 버튼)
   - 이메일과 비밀번호로 로그인
   - 토큰 받기

3. **인스타그램 연동** (`POST /api/integrations/instagram/connect`)
   - 인스타그램 사용자명과 비밀번호 입력
   - 연동 완료

4. **동기화** (`POST /api/integrations/{id}/sync`)
   - 저장된 게시물 가져오기

5. **콘텐츠 조회** (`GET /api/contents`)
   - 저장된 콘텐츠 목록 보기
