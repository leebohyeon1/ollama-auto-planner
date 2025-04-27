@echo off
:: Ollama 자동 기획서 분석 시스템 실행 스크립트 (단순 버전)

echo Ollama 자동 기획서 분석 시스템을 시작합니다...
echo.

:: 가상 환경 확인 및 생성
if not exist venv (
    echo 가상 환경을 생성합니다...
    python -m venv venv
    if errorlevel 1 (
        echo 가상 환경 생성 실패. Python이 설치되어 있는지 확인하세요.
        goto :error
    )
    echo 가상 환경이 생성되었습니다.
)

:: 가상 환경 활성화
echo 가상 환경을 활성화합니다...
call venv\Scripts\activate
if errorlevel 1 (
    echo 가상 환경 활성화 실패.
    goto :error
)
echo 가상 환경이 활성화되었습니다.

:: 의존성 설치
echo 필요한 패키지를 설치합니다...
pip install -r requirements.txt
if errorlevel 1 (
    echo 패키지 설치 실패.
    goto :error
)
echo 패키지 설치가 완료되었습니다.

:: 필요한 디렉토리 확인 및 생성
if not exist planning_docs mkdir planning_docs
if not exist output mkdir output
if not exist logs mkdir logs

:: Ollama 실행 확인
echo Ollama 서버 실행 상태를 확인합니다...
curl -s http://localhost:11434/api/tags > nul 2>&1
if errorlevel 1 (
    echo Ollama 서버가 실행되고 있지 않습니다.
    echo 별도의 터미널에서 'ollama serve' 명령을 실행한 후 다시 시도해주세요.
    goto :error
)
echo Ollama 서버가 실행 중입니다.

:: 매개변수 초기화 (기본값)
set MODEL=mistral
set RUNTIME=6
set OUTPUT=project.json
set RESUME=
set DEBUG=

:: 기획서 존재 확인
dir /b planning_docs\*.* > nul 2>&1
if errorlevel 1 (
    echo 기획서 파일이 존재하지 않습니다.
    echo planning_docs 폴더에 기획서 파일(.txt, .md 등)을 추가한 후 다시 시도해주세요.
    goto :error
)
echo 기획서 파일이 존재합니다. 분석을 시작합니다.
echo.

:: 프로그램 실행
echo 모델: %MODEL%
echo 실행 시간: %RUNTIME% 시간
echo 출력 파일: %OUTPUT%
echo.

:: 프로그램 실행
python main.py --model %MODEL% --runtime %RUNTIME% --output %OUTPUT%
if errorlevel 1 (
    echo 프로그램 실행 중 오류가 발생했습니다.
    goto :error
)

echo 실행이 완료되었습니다.
echo 결과 파일: output\%OUTPUT%
echo 로그 파일: logs\ 디렉토리에서 확인할 수 있습니다.
echo.

:: 가상 환경 비활성화
call venv\Scripts\deactivate
goto :eof

:error
echo.
echo 오류가 발생했습니다. 프로그램을 종료합니다.
exit /b 1
