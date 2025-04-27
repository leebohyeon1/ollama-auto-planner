# Ollama 자동 기획서 분석 및 기능 생성 시스템

이 프로젝트는 Ollama 로컬 AI를 사용하여 기획서를 자동으로 분석하고, 필요한 기능을 생성하는 시스템입니다.

## 특징

- **장시간 자동 실행**: 5-6시간 동안 자동으로 실행됩니다.
- **자기 질의 메커니즘**: AI가 대답하고, 자신에게 다음 질문을 생성합니다.
- **맥락 유지**: 대화 기록을 유지하면서 기획서 내용을 계속 분석합니다.
- **진행 상황 기록**: 모든 대화 내용과 결과물을 로그 파일에 저장합니다.

## 요구 사항

- Python 3.8 이상
- [Ollama](https://ollama.ai/) 설치 및 실행
- 필요한 모델(mistral, llama3 등) 다운로드

## 설치 방법

1. 레포지토리 클론:
   ```
   git clone https://github.com/leebohyeon1/ollama-auto-planner.git
   cd ollama-auto-planner
   ```

2. 가상 환경 생성 및 활성화:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. 의존성 설치:
   ```
   pip install -r requirements.txt
   ```

4. Ollama 실행 및 모델 다운로드:
   ```
   # 별도 터미널에서 Ollama 서버 실행
   ollama serve
   
   # 모델 다운로드
   ollama pull mistral
   # 또는 다른 모델
   # ollama pull llama3
   ```

## 사용 방법

1. `planning_docs` 폴더에 분석할 기획서 파일(`.txt`, `.md` 등)을 넣습니다.

2. 설정 파일(`config.py`)에서 필요한 설정을 변경합니다:
   - 사용할 모델 이름
   - 실행 시간
   - 출력 형식 등

3. 프로그램 실행:
   ```
   python main.py
   ```

4. 결과 확인:
   - 대화 기록은 `conversation_log.txt`에 저장됩니다.
   - 생성된 기능 설계는 `output` 폴더에 저장됩니다.

## 주요 파일 설명

- `main.py`: 주 실행 스크립트
- `config.py`: 설정 파일
- `utils.py`: 유틸리티 함수들
- `models.py`: 데이터 모델 정의

## 라이센스

MIT

## 기여하기

이슈와 풀 리퀘스트를 환영합니다. 주요 변경 사항은 먼저 이슈를 열어 논의해주세요.
