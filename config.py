"""
Ollama 자동 기획서 분석 시스템 설정 파일
"""
import os
from pathlib import Path

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent
PLANNING_DOCS_DIR = os.path.join(BASE_DIR, "planning_docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ollama API 설정
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi4"  # 사용할 모델 (예: "llama3", "mistral", "phi4")

# 실행 설정
MAX_RUNTIME_HOURS = 6  # 최대 실행 시간 (시간)
WAIT_TIME_SECONDS = 10  # 반복 간 대기 시간 (초)
MAX_ITERATIONS = 1000  # 최대 반복 횟수 (안전장치)

# 로깅 설정
CONVERSATION_LOG_FILE = "conversation_log.txt"
DETAILED_LOGGING = True  # 상세 로그 기록 여부

# 프롬프트 설정
SYSTEM_PROMPT = """
당신은 기획서를 분석하고 기능을 구현하는 AI 개발자입니다.
다음 기획서 내용을 분석하고 필요한 기능을 설계해주세요.
자세하고 구체적인 구현 방법과 코드 예시를 제공해주세요.
"""

INITIAL_QUESTION = "이 기획서에 따르면 어떤 핵심 기능들이 필요한가요?"

# 컨텍스트 관리 설정
MAX_CONVERSATION_HISTORY = 10  # 기억할 최대 대화 기록 수
SUMMARIZE_INTERVAL = 5  # 몇 번의 대화마다 요약할지 설정

# 출력 설정
SAVE_INTERMEDIATE_RESULTS = True  # 중간 결과 저장 여부
INTERMEDIATE_SAVE_INTERVAL = 5  # 몇 번의 대화마다 중간 결과를 저장할지

# 기능 추출 설정
EXTRACT_CODE_SNIPPETS = True  # 코드 스니펫 추출 여부
EXTRACT_ARCHITECTURE_DIAGRAMS = True  # 아키텍처 다이어그램 추출 여부

# 고급 설정
DEBUG_MODE = False  # 디버그 모드
VERBOSE_OUTPUT = True  # 상세 출력 여부
