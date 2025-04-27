#!/bin/bash
# Ollama 자동 기획서 분석 시스템 실행 스크립트

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${BLUE}"
echo "  ____  _  _                               _         _____  _                               "
echo " / __ \| || |                     /\      (_)       |  __ \| |                              "
echo "| |  | | || |__ _ _ __ ___   __ _|  \      _ ______ | |__) | | __ _ _ __  _ __   ___ _ __  "
echo "| |  | | |__/ _\` | '_ \` _ \ / _\` | . \    | |______||  ___/| |/ _\` | '_ \| '_ \ / _ \ '__| "
echo "| |__| | | | (_| | | | | | | (_| | |\  \   | |      | |    | | (_| | | | | | | |  __/ |    "
echo " \____/|_|  \__,_|_| |_| |_|\__,_|_| \__\  |_|      |_|    |_|\__,_|_| |_|_| |_|\___|_|    "
echo -e "${NC}"
echo -e "${GREEN}자동 기획서 분석 및 기능 생성 시스템${NC}"
echo

# 가상 환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}가상 환경을 생성합니다...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}가상 환경이 생성되었습니다.${NC}"
fi

# 가상 환경 활성화
echo -e "${YELLOW}가상 환경을 활성화합니다...${NC}"
source venv/bin/activate
echo -e "${GREEN}가상 환경이 활성화되었습니다.${NC}"

# 의존성 설치
echo -e "${YELLOW}필요한 패키지를 설치합니다...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}패키지 설치가 완료되었습니다.${NC}"

# 필요한 디렉토리 확인 및 생성
mkdir -p planning_docs
mkdir -p output
mkdir -p logs

# Ollama 실행 확인
echo -e "${YELLOW}Ollama 서버 실행 상태를 확인합니다...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo -e "${GREEN}Ollama 서버가 실행 중입니다.${NC}"
else
    echo -e "${RED}Ollama 서버가 실행되고 있지 않습니다.${NC}"
    echo -e "${YELLOW}별도의 터미널에서 'ollama serve' 명령을 실행한 후 다시 시도해주세요.${NC}"
    exit 1
fi

# 매개변수 처리
MODEL="mistral"
RUNTIME=6
OUTPUT="project.json"
RESUME=""
DEBUG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --runtime)
            RUNTIME="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --resume)
            RESUME="--resume"
            shift
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        *)
            echo -e "${RED}알 수 없는 매개변수: $1${NC}"
            exit 1
            ;;
    esac
done

# 모델 존재 확인
echo -e "${YELLOW}모델 '$MODEL'을 확인합니다...${NC}"
if curl -s http://localhost:11434/api/tags | grep -q "$MODEL"; then
    echo -e "${GREEN}모델 '$MODEL'이(가) 존재합니다.${NC}"
else
    echo -e "${RED}모델 '$MODEL'이(가) 존재하지 않습니다.${NC}"
    echo -e "${YELLOW}모델을 다운로드합니다...${NC}"
    ollama pull $MODEL
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}모델 다운로드에 실패했습니다. 올바른 모델 이름인지 확인하세요.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}모델 '$MODEL'이(가) 다운로드되었습니다.${NC}"
fi

# 기획서 존재 확인
PLANNING_FILES=$(ls -1 planning_docs | wc -l)
if [ $PLANNING_FILES -eq 0 ]; then
    echo -e "${RED}기획서 파일이 존재하지 않습니다.${NC}"
    echo -e "${YELLOW}planning_docs 폴더에 기획서 파일(.txt, .md 등)을 추가한 후 다시 시도해주세요.${NC}"
    exit 1
fi

echo -e "${GREEN}기획서 파일이 존재합니다. 분석을 시작합니다.${NC}"

# 프로그램 실행
echo -e "${BLUE}Ollama 자동 기획서 분석 시스템을 시작합니다...${NC}"
echo -e "${YELLOW}모델: ${NC}$MODEL"
echo -e "${YELLOW}실행 시간: ${NC}$RUNTIME 시간"
echo -e "${YELLOW}출력 파일: ${NC}$OUTPUT"
echo

# 프로그램 실행
python main.py --model $MODEL --runtime $RUNTIME --output $OUTPUT $RESUME $DEBUG

# 실행 완료
echo -e "${GREEN}실행이 완료되었습니다.${NC}"
echo -e "${YELLOW}결과 파일: ${NC}output/$OUTPUT"
echo -e "${YELLOW}로그 파일: ${NC}logs/ 디렉토리에서 확인할 수 있습니다."
echo

# 가상 환경 비활성화
deactivate
