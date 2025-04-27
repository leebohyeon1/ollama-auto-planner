@echo on
:: 가장 단순한 실행 스크립트 - 오류 확인 가능

echo 프로그램을 시작합니다...

:: Python 설치 확인
python --version
if %errorlevel% neq 0 (
    echo Python이 설치되어 있지 않거나 PATH에 등록되지 않았습니다.
    echo Python을 설치한 후 다시 시도해주세요.
    pause
    exit /b 1
)

:: 필요한 폴더 생성
mkdir planning_docs 2>nul
mkdir output 2>nul
mkdir logs 2>nul

:: 직접 메인 스크립트 실행
python main.py --model phi4 --runtime 6 --output project.json

:: 실행 종료
echo 프로그램 실행이 완료되었습니다.
pause
