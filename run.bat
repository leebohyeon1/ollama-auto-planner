@echo off
:: Ollama 자동 기획서 분석 시스템 실행 스크립트 (Windows용)
setlocal EnableDelayedExpansion

:: 색상 정의
set "BLUE=[94m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: 로고 출력
echo %BLUE%
echo   ____  _  _                               _         _____  _                               
echo  / __ \| || |                     /\      (_)       |  __ \| |                              
echo ^| |  | | || |__ _ _ __ ___   __ _|  \      _ ______ | |__) | | __ _ _ __  _ __   ___ _ __  
echo ^| |  | | |__/ _` | '_ ` _ \ / _` | . \    | |______||  ___/| |/ _` | '_ \| '_ \ / _ \ '__| 
echo ^| |__| | | | (_| | | | | | | (_| | |\  \   | |      | |    | | (_| | | | | | | |  __/ |    
echo  \____/|_|  \__,_|_| |_| |_|\__,_|_| \__\  |_|      |_|    |_|\__,_|_| |_|_| |_|\___|_|    
echo %NC%
echo %GREEN%자동 기획서 분석 및 기능 생성 시스템%NC%
echo.

:: 가상 환경 확인 및 생성
if not exist venv (
    echo %YELLOW%가상 환경을 생성합니다...%NC%
    python -m venv venv
    echo %GREEN%가상 환경이 생성되었습니다.%NC%
)

:: 가상 환경 활성화
echo %YELLOW%가상 환경을 활성화합니다...%NC%
call venv\Scripts\activate.bat
echo %GREEN%가상 환경이 활성화되었습니다.%NC%

:: 의존성 설치
echo %YELLOW%필요한 패키지를 설치합니다...%NC%
pip install -r requirements.txt
echo %GREEN%패키지 설치가 완료되었습니다.%NC%

:: 필요한 디렉토리 확인 및 생성
if not exist planning_docs mkdir planning_docs
if not exist output mkdir output
if not exist logs mkdir logs

:: Ollama 실행 확인
echo %YELLOW%Ollama 서버 실행 상태를 확인합니다...%NC%
curl -s http://localhost:11434/api/tags > nul
if %errorlevel% neq 0 (
    echo %RED%Ollama 서버가 실행되고 있지 않습니다.%NC%
    echo %YELLOW%별도의 터미널에서 'ollama serve' 명령을 실행한 후 다시 시도해주세요.%NC%
    exit /b 1
) else (
    echo %GREEN%Ollama 서버가 실행 중입니다.%NC%
)

:: 매개변수 처리
set "MODEL=mistral"
set "RUNTIME=6"
set "OUTPUT=project.json"
set "RESUME="
set "DEBUG="

:parse_args
if "%~1"=="" goto end_parse_args
if "%~1"=="--model" (
    set "MODEL=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--runtime" (
    set "RUNTIME=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--output" (
    set "OUTPUT=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--resume" (
    set "RESUME=--resume"
    shift
    goto parse_args
)
if "%~1"=="--debug" (
    set "DEBUG=--debug"
    shift
    goto parse_args
)
echo %RED%알 수 없는 매개변수: %~1%NC%
exit /b 1

:end_parse_args

:: 모델 존재 확인
echo %YELLOW%모델 '%MODEL%'을 확인합니다...%NC%
curl -s http://localhost:11434/api/tags | findstr /c:"%MODEL%" > nul
if %errorlevel% neq 0 (
    echo %RED%모델 '%MODEL%'이(가) 존재하지 않습니다.%NC%
    echo %YELLOW%모델을 다운로드합니다...%NC%
    ollama pull %MODEL%
    
    if %errorlevel% neq 0 (
        echo %RED%모델 다운로드에 실패했습니다. 올바른 모델 이름인지 확인하세요.%NC%
        exit /b 1
    )
    
    echo %GREEN%모델 '%MODEL%'이(가) 다운로드되었습니다.%NC%
) else (
    echo %GREEN%모델 '%MODEL%'이(가) 존재합니다.%NC%
)

:: 기획서 존재 확인
dir /b planning_docs\* > nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%기획서 파일이 존재하지 않습니다.%NC%
    echo %YELLOW%planning_docs 폴더에 기획서 파일(.txt, .md 등)을 추가한 후 다시 시도해주세요.%NC%
    exit /b 1
)

echo %GREEN%기획서 파일이 존재합니다. 분석을 시작합니다.%NC%

:: 프로그램 실행
echo %BLUE%Ollama 자동 기획서 분석 시스템을 시작합니다...%NC%
echo %YELLOW%모델: %NC%%MODEL%
echo %YELLOW%실행 시간: %NC%%RUNTIME% 시간
echo %YELLOW%출력 파일: %NC%%OUTPUT%
echo.

:: 프로그램 실행
python main.py --model %MODEL% --runtime %RUNTIME% --output %OUTPUT% %RESUME% %DEBUG%

:: 실행 완료
echo %GREEN%실행이 완료되었습니다.%NC%
echo %YELLOW%결과 파일: %NC%output\%OUTPUT%
echo %YELLOW%로그 파일: %NC%logs\ 디렉토리에서 확인할 수 있습니다.
echo.

:: 가상 환경 비활성화
call venv\Scripts\deactivate.bat

endlocal
