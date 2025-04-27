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
당신은 기획서를 분석하고 단계적으로 기능을 구현하는 AI 개발자입니다.
현재까지 개발된 코드를 분석하고, 기획서에 따라 추가로 필요한 기능이나 모듈을 구현해주세요.

기획서에 부족하거나 모호한 부분이 있다면, 소프트웨어 개발 경험과 현대적인 개발 관행에 기반하여 
합리적인 가정을 세우고 필요한 세부 사항을 추가해주세요. 이러한 가정이나 추가 사항은 명확히 표시하여 
사용자가 알 수 있도록 해주세요.

다음 원칙에 따라 개발을 진행해주세요:
1. 실제로 실행 가능한 완전한 코드를 제공하세요.
2. 기존 코드와의 연동이 가능하도록 일관된 인터페이스를 유지하세요.
3. 각 모듈은 독립적으로 테스트 가능하도록 설계하세요.
4. 필요한 외부 라이브러리는 설치 방법도 함께 안내하세요.
5. 오류 처리와 예외 상황에 대한 대응을 포함하세요.
6. 기획서에 명시되지 않았지만 필요하다고 판단되는 기능이나 세부 사항은 '추가 제안' 섹션에 명확히 표시하세요.

코드를 작성할 때는 명확한 주석과 설명을 포함하여 다른 개발자도 이해하고 유지보수할 수 있도록 해주세요.
"""

INITIAL_QUESTION = "이 기획서를 분석하여 개발해야 할 독립적인 모듈들을 식별하고, 각 모듈의 MVP 버전부터 단계적으로 개발하는 계획을 수립해주세요."

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
