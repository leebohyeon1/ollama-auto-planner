# Windows 사용자를 위한 실행 가이드

배치 파일이 제대로 실행되지 않는 경우, 명령 프롬프트(CMD)나 PowerShell을 통해 직접 스크립트를 실행하는 방법을 안내합니다.

## 명령 프롬프트(CMD)에서 실행하기

1. **명령 프롬프트 열기**
   - Windows 검색에서 `cmd`를 입력하고 '명령 프롬프트' 앱을 실행합니다.

2. **프로젝트 폴더로 이동**
   ```
   cd 경로\ollama-auto-planner
   ```
   예: `cd C:\Users\username\Documents\ollama-auto-planner`

3. **가상 환경 생성** (처음 한 번만)
   ```
   python -m venv venv
   ```

4. **가상 환경 활성화**
   ```
   venv\Scripts\activate
   ```
   
   명령 프롬프트 앞에 `(venv)`가 표시되면 활성화된 것입니다.

5. **필요한 패키지 설치** (처음 한 번만)
   ```
   pip install -r requirements.txt
   ```

6. **Ollama 서버 확인**
   - 별도의 명령 프롬프트 창에서 Ollama가 실행 중인지 확인하세요.
   - 실행 중이 아니라면 `ollama serve` 명령으로 실행합니다.

7. **프로그램 실행**
   ```
   python main.py --model mistral --runtime 6 --output project.json
   ```

## PowerShell에서 실행하기

1. **PowerShell 열기**
   - Windows 검색에서 `powershell`을 입력하고 PowerShell을 실행합니다.

2. **실행 정책 확인 및 설정** (필요한 경우)
   ```
   Get-ExecutionPolicy
   ```
   
   정책이 'Restricted'인 경우, 다음 명령을 실행합니다:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **프로젝트 폴더로 이동**
   ```
   cd 경로\ollama-auto-planner
   ```

4. **가상 환경 생성** (처음 한 번만)
   ```
   python -m venv venv
   ```

5. **가상 환경 활성화**
   ```
   .\venv\Scripts\Activate.ps1
   ```

6. **필요한 패키지 설치** (처음 한 번만)
   ```
   pip install -r requirements.txt
   ```

7. **Ollama 서버 확인**
   - 별도의 PowerShell 창에서 Ollama가 실행 중인지 확인하세요.
   - 실행 중이 아니라면 `ollama serve` 명령으로 실행합니다.

8. **프로그램 실행**
   ```
   python main.py --model mistral --runtime 6 --output project.json
   ```

## 문제 해결

1. **"가상 환경을 활성화할 수 없습니다" 오류**
   - PowerShell에서 다음 명령을 실행한 후 다시 시도:
     ```
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

2. **"Python을 찾을 수 없습니다" 오류**
   - Python이 설치되어 있는지 확인
   - 설치되어 있다면 PATH에 추가되었는지 확인

3. **"pip을 찾을 수 없습니다" 오류**
   - Python 설치 시 pip이 함께 설치되었는지 확인
   - Python 설치 경로의 Scripts 폴더가 PATH에 추가되어 있는지 확인

4. **"ollama 명령을 찾을 수 없습니다" 오류**
   - Ollama가 설치되어 있는지 확인
   - Ollama 설치 경로가 PATH에 추가되어 있는지 확인

5. **"모듈을 찾을 수 없습니다" 오류**
   - 가상 환경이 활성화되었는지 확인
   - `pip install -r requirements.txt` 명령이 성공적으로 실행되었는지 확인

## 직접 실행 가이드 (가상 환경 없이)

가상 환경 설정에 문제가 있는 경우, 다음과 같이 직접 실행할 수 있습니다:

1. **필요한 패키지 설치**
   ```
   pip install requests python-dotenv tqdm pyyaml colorama
   ```

2. **프로그램 실행**
   ```
   python main.py --model mistral --runtime 6 --output project.json
   ```

## 파일 구조 확인하기

프로그램이 올바르게 설정되었는지 확인하려면 다음 명령으로 필요한 파일이 모두 있는지 확인하세요:

```
dir
```

다음 파일들이 있어야 합니다:
- main.py
- utils.py
- models.py
- config.py
- requirements.txt
- planning_docs 폴더 (기획서 파일이 들어 있어야 함)
