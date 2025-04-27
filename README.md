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
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
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
   - 기본적으로 예제 기획서(`example_plan.md`)가 포함되어 있습니다.

2. 설정 파일(`config.py`)에서 필요한 설정을 변경합니다:
   - 사용할 모델 이름
   - 실행 시간
   - 출력 형식 등

3. 프로그램 실행:
   ```
   # Windows (기본 스크립트)
   run.bat
   
   # Windows (단순 버전 - 호환성 문제 발생 시)
   run_simple.bat
   
   # Mac/Linux
   chmod +x run.sh
   ./run.sh
   ```

4. 실행 옵션:
   ```
   # Windows
   run.bat --model llama3 --runtime 8 --output my_project.json

   # Mac/Linux
   ./run.sh --model llama3 --runtime 8 --output my_project.json
   ```
   - `--model`: 사용할 Ollama 모델 (기본값: mistral)
   - `--runtime`: 실행 시간(시간) (기본값: 6)
   - `--output`: 결과 파일 이름 (기본값: project.json)
   - `--resume`: 이전 상태에서 계속 실행
   - `--debug`: 디버그 모드 활성화

5. 결과 확인:
   - 대화 기록은 `conversation_log.txt`에 저장됩니다.
   - 생성된 기능 설계는 `output` 폴더에 저장됩니다.

## Windows 사용 시 주의사항

Windows에서 실행 문제가 발생하는 경우:

1. `run_simple.bat`을 사용해보세요 - 더 단순한 버전의 실행 스크립트입니다.
2. 직접 명령어로 실행할 수도 있습니다:
   ```
   python main.py --model mistral --runtime 6 --output project.json
   ```
3. 가상 환경 활성화가 안 되는 경우 PowerShell에서는 다음 명령어로 실행 정책을 변경해볼 수 있습니다:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## 주요 파일 설명

- `main.py`: 주 실행 스크립트
- `config.py`: 설정 파일
- `utils.py`: 유틸리티 함수들
- `models.py`: 데이터 모델 정의
- `run.sh`: Mac/Linux용 실행 스크립트
- `run.bat`: Windows용 실행 스크립트
- `run_simple.bat`: Windows용 단순 실행 스크립트 (호환성 문제 발생 시 사용)

## 라이센스

MIT

## 기여하기

이슈와 풀 리퀘스트를 환영합니다. 주요 변경 사항은 먼저 이슈를 열어 논의해주세요.
