# 문제 진단 및 해결 가이드

## 발견된 문제들

### 1. 한글 인코딩 문제
**증상**: PowerShell에서 한글이 깨져서 표시됨
**원인**: PowerShell 기본 인코딩이 CP949로 설정되어 있음
**해결**: UTF-8 인코딩 설정 필요

### 2. 여러 서버 프로세스 실행
**증상**: 여러 개의 Python/uvicorn 프로세스가 동시에 실행됨
**원인**: 이전에 실행한 서버가 종료되지 않음
**해결**: 기존 프로세스 종료 후 재시작

### 3. 서버 시작 확인 실패
**증상**: 서버가 시작되었지만 헬스 체크가 실패함
**원인**: 서버 시작 시간이 필요하거나 포트 충돌
**해결**: 재시도 로직 추가 및 포트 확인

## 해결 방법

### 한글 인코딩 설정
PowerShell에서 다음 명령 실행:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
```

### 서버 정리 및 재시작
```powershell
# 기존 프로세스 종료
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"} | Stop-Process -Force

# 서버 재시작
cd C:\Users\john\Desktop\re-light\remind-link\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 포트 확인
```powershell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

## 현재 상태

- ✅ 데이터베이스 파일 존재: `remindlink.db`
- ✅ 환경 변수 파일 존재: `.env`
- ✅ 가상환경 존재: `venv/`
- ⚠️ 서버 프로세스: 여러 개 실행 중 (정리 필요)
- ⚠️ 한글 인코딩: UTF-8 설정 필요

## 권장 사항

1. 서버 시작 전 항상 기존 프로세스 정리
2. UTF-8 인코딩 설정 스크립트 사용
3. 서버 시작 후 최소 5-8초 대기
4. 별도 PowerShell 창에서 서버 실행하여 로그 확인
