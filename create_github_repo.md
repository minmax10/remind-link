# GitHub 레포지토리 생성 안내

## 현재 상태

브라우저에서 GitHub 로그인 페이지가 열려있습니다.

## 레포지토리 생성 방법

### 방법 1: 브라우저에서 직접 생성 (가장 간단)

1. **브라우저에서 GitHub 로그인**
   - 현재 열려있는 페이지에서 로그인
   - 또는 https://github.com/login 접속

2. **레포지토리 생성 페이지 이동**
   - https://github.com/new 접속
   - 또는 로그인 후 "New repository" 클릭

3. **레포지토리 설정**
   - **Repository name**: `remind-link`
   - **Description**: `인스타그램 저장 게시물 자동 수집 및 분류 서비스` (선택)
   - **Public** 또는 **Private** 선택
   - ⚠️ **"Initialize this repository with a README" 체크 해제** (중요!)
   - ⚠️ **"Add .gitignore" 선택 안 함**
   - ⚠️ **"Choose a license" 선택 안 함**

4. **"Create repository" 클릭**

5. **레포지토리 생성 완료!**

### 방법 2: GitHub CLI 사용 (고급 사용자용)

#### GitHub CLI 설치

1. **다운로드**: https://cli.github.com
2. **설치**: 다운로드한 파일 실행

#### GitHub CLI로 레포지토리 생성

PowerShell에서:

```powershell
cd C:\Users\john\Desktop\re-light\remind-link

# GitHub 로그인
gh auth login

# 레포지토리 생성 및 푸시 (한 번에)
gh repo create remind-link --public --source=. --remote=origin --push
```

또는 단계별로:

```powershell
# 1. 로그인
gh auth login

# 2. 레포지토리 생성
gh repo create remind-link --public --description "인스타그램 저장 게시물 자동 수집 및 분류 서비스"

# 3. 원격 저장소 설정
git remote add origin https://github.com/YOUR_USERNAME/remind-link.git

# 4. 푸시
git branch -M main
git push -u origin main
```

### 방법 3: GitHub API 사용 (고급)

Personal Access Token이 필요한 방법입니다.

1. **Personal Access Token 생성**
   - https://github.com/settings/tokens 접속
   - "Generate new token" → "Generate new token (classic)"
   - "repo" 권한 선택
   - 토큰 생성 및 복사

2. **API로 레포지토리 생성**

PowerShell에서:

```powershell
$token = "YOUR_PERSONAL_ACCESS_TOKEN"
$username = "YOUR_USERNAME"
$repoName = "remind-link"

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    name = $repoName
    description = "인스타그램 저장 게시물 자동 수집 및 분류 서비스"
    private = $false
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body

Write-Host "레포지토리 생성 완료: $($response.html_url)" -ForegroundColor Green

# 원격 저장소 설정
git remote add origin $response.clone_url
git branch -M main
git push -u origin main
```

## 권장 방법

**방법 1 (브라우저)**이 가장 간단하고 안전합니다.

1. 현재 브라우저에서 GitHub 로그인
2. https://github.com/new 접속
3. 레포지토리 이름: `remind-link`
4. "Initialize this repository with a README" 체크 해제
5. Create repository 클릭

## 레포지토리 생성 후

레포지토리 생성이 완료되면:

```powershell
cd C:\Users\john\Desktop\re-light\remind-link
.\auto_deploy_all.ps1
```

또는 수동으로:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/remind-link.git
git branch -M main
git push -u origin main
```

## 문제 해결

### GitHub CLI가 인식되지 않을 때
- PowerShell 재시작
- PATH 환경 변수 확인

### 푸시 실패 시
- Personal Access Token 사용
- 토큰 생성: https://github.com/settings/tokens
- `repo` 권한 선택
