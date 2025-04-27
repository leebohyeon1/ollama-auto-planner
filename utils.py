"""
유틸리티 함수 모음
"""
import os
import re
import json
import logging
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

import config

# 로깅 설정
def setup_logging():
    """로깅 설정을 초기화합니다."""
    if not os.path.exists(config.LOG_DIR):
        os.makedirs(config.LOG_DIR)
    
    log_file = os.path.join(config.LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG_MODE else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# 폴더 초기화
def init_folders():
    """필요한 폴더 구조를 초기화합니다."""
    folders = [
        config.PLANNING_DOCS_DIR,
        config.OUTPUT_DIR,
        config.LOG_DIR
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"Created folder: {folder}")

# 기획서 로드
def load_planning_docs() -> str:
    """planning_docs 폴더에서 기획서 파일들을 로드합니다."""
    if not os.path.exists(config.PLANNING_DOCS_DIR):
        logging.error(f"Planning docs directory not found: {config.PLANNING_DOCS_DIR}")
        return ""
    
    all_content = []
    
    for file_name in os.listdir(config.PLANNING_DOCS_DIR):
        file_path = os.path.join(config.PLANNING_DOCS_DIR, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith(('.txt', '.md', '.docx')):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_content.append(f"# {file_name}\n\n{content}\n\n")
                    logging.info(f"Loaded planning document: {file_name}")
            except Exception as e:
                logging.error(f"Error loading file {file_name}: {e}")
    
    if not all_content:
        logging.warning("No planning documents found. Please add documents to the planning_docs folder.")
        return ""
    
    return "\n".join(all_content)

# Ollama API 호출
def query_ollama(prompt: str, model: str = None) -> str:
    """Ollama API를 호출하여 응답을 받습니다."""
    if model is None:
        model = config.MODEL_NAME
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(config.OLLAMA_API_URL, json=payload)
        
        if response.status_code == 200:
            return response.json().get("response", "응답을 받지 못했습니다.")
        else:
            error_msg = f"API 오류 (코드: {response.status_code}): {response.text}"
            logging.error(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"API 호출 중 예외 발생: {str(e)}"
        logging.error(error_msg)
        return error_msg

# 대화 기록 관리
class ConversationHistory:
    def __init__(self, max_history: int = config.MAX_CONVERSATION_HISTORY):
        self.history = []
        self.max_history = max_history
        self.summary = ""
    
    def add(self, question: str, answer: str):
        """대화 기록에 질문과 답변을 추가합니다."""
        self.history.append((question, answer))
        
        # 최대 기록 수를 넘으면 가장 오래된 기록 제거
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_formatted_history(self) -> str:
        """형식화된 대화 기록을 반환합니다."""
        return "\n\n".join([f"질문: {q}\n답변: {a}" for q, a in self.history])
    
    def summarize(self) -> str:
        """현재 대화 기록을 요약합니다."""
        if not self.history:
            return ""
        
        history_text = self.get_formatted_history()
        prompt = f"""다음은 기획서에 관한 대화 기록입니다. 이 대화 내용을 간결하게 요약해주세요:

{history_text}

요약:"""
        
        self.summary = query_ollama(prompt)
        return self.summary
    
    def clear(self):
        """대화 기록을 초기화합니다."""
        self.history = []
        self.summary = ""

# 다음 질문 생성
def generate_next_question(response: str) -> str:
    """AI 응답을 분석하여 다음 질문을 생성합니다."""
    prompt = f"""
다음 AI 응답을 분석하고, 기획서 구현을 더 발전시키기 위한 가장 관련성 있고 깊이 있는 후속 질문을 생성해주세요:

{response}

질문:"""
    
    return query_ollama(prompt)

# 결과 저장
def save_result(content: str, file_name: str = None):
    """결과를 파일에 저장합니다."""
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
    
    if file_name is None:
        file_name = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    file_path = os.path.join(config.OUTPUT_DIR, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logging.info(f"Result saved to {file_path}")
    return file_path

# 코드 스니펫 추출
def extract_code_snippets(text: str) -> List[Dict[str, str]]:
    """텍스트에서 코드 스니펫을 추출합니다."""
    pattern = r"```([a-zA-Z0-9_]*)\n([\s\S]*?)```"
    matches = re.findall(pattern, text)
    
    snippets = []
    for lang, code in matches:
        snippets.append({
            "language": lang.strip() or "text",
            "code": code.strip()
        })
    
    return snippets

# 아키텍처 다이어그램 추출 및 생성
def extract_architecture_diagrams(text: str) -> List[Dict[str, str]]:
    """텍스트에서 아키텍처 다이어그램 설명을 추출하고 다이어그램을 생성합니다."""
    # 다이어그램 추출 로직 (실제로는 더 복잡한 구현이 필요할 수 있음)
    # 여기서는 간단한 구현만 제공
    pattern = r"# 아키텍처 다이어그램\n([\s\S]*?)(?=\n#|\Z)"
    matches = re.findall(pattern, text)
    
    diagrams = []
    for match in matches:
        diagrams.append({
            "description": match.strip(),
            "type": "architecture"
        })
    
    return diagrams

# 상태 저장 및 복구
def save_state(state: Dict[str, Any], file_name: str = "state.json"):
    """현재 실행 상태를 저장합니다."""
    file_path = os.path.join(config.OUTPUT_DIR, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    logging.info(f"State saved to {file_path}")

def load_state(file_name: str = "state.json") -> Dict[str, Any]:
    """저장된 실행 상태를 로드합니다."""
    file_path = os.path.join(config.OUTPUT_DIR, file_name)
    
    if not os.path.exists(file_path):
        logging.info(f"No saved state found at {file_path}")
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        logging.info(f"State loaded from {file_path}")
        return state
    except Exception as e:
        logging.error(f"Error loading state: {e}")
        return {}
