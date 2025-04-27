#!/usr/bin/env python3
"""
Ollama 자동 기획서 분석 시스템

기획서를 자동으로 분석하고 기능을 생성하는 시스템입니다.
5-6시간 동안 실행되며 AI가 자동으로 기능을 분석하고 설계합니다.
"""
import os
import time
import json
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import config
import utils
from models import Project, Component, Feature, CodeSnippet

# 로거 설정
logger = None

def parse_arguments():
    """명령줄 인수를 파싱합니다."""
    parser = argparse.ArgumentParser(description="Ollama 자동 기획서 분석 시스템")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default=config.MODEL_NAME,
        help=f"사용할 Ollama 모델 (기본값: {config.MODEL_NAME})"
    )
    
    parser.add_argument(
        "--runtime", 
        type=float, 
        default=config.MAX_RUNTIME_HOURS,
        help=f"최대 실행 시간 (시간 단위, 기본값: {config.MAX_RUNTIME_HOURS})"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="project.json",
        help="결과 프로젝트 파일 이름 (기본값: project.json)"
    )
    
    parser.add_argument(
        "--resume", 
        action="store_true",
        help="이전 상태에서 계속 실행할지 여부"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="디버그 모드 활성화"
    )
    
    return parser.parse_args()

def setup_environment(args):
    """환경을 설정합니다."""
    global logger
    
    # 디버그 모드 설정
    if args.debug:
        config.DEBUG_MODE = True
    
    # 로깅 설정
    logger = utils.setup_logging()
    
    # 필요한 폴더 생성
    utils.init_folders()
    
    # 모델 이름 설정
    if args.model != config.MODEL_NAME:
        config.MODEL_NAME = args.model
        logger.info(f"모델 변경: {config.MODEL_NAME}")
    
    # 실행 시간 설정
    if args.runtime != config.MAX_RUNTIME_HOURS:
        config.MAX_RUNTIME_HOURS = args.runtime
        logger.info(f"실행 시간 변경: {config.MAX_RUNTIME_HOURS}시간")

def create_prompt(planning_doc: str, conversation_history: utils.ConversationHistory, question: str) -> str:
    """프롬프트를 생성합니다."""
    # 이전 대화 요약이 있으면 포함
    summary = ""
    if conversation_history.summary:
        summary = f"\n\n이전 대화 요약:\n{conversation_history.summary}\n\n"
    
    # 최근 대화 기록
    history = conversation_history.get_formatted_history()
    
    # 최종 프롬프트
    prompt = f"""{config.SYSTEM_PROMPT}

# 기획서 내용
{planning_doc}

{summary}# 이전 대화 내용
{history}

# 현재 질문
{question}

자세하고 구체적인 답변을 제공해주세요. 코드 예시와 구현 방법을 포함해주세요.
"""
    
    return prompt

def process_response(response: str, project: Project) -> Project:
    """AI 응답을 처리하고 프로젝트 모델을 업데이트합니다."""
    # 코드 스니펫 추출
    if config.EXTRACT_CODE_SNIPPETS:
        code_snippets = utils.extract_code_snippets(response)
        
        # 추출된 코드 스니펫 처리
        for snippet_data in code_snippets:
            # CodeSnippet 객체 생성
            snippet = CodeSnippet(
                language=snippet_data["language"],
                code=snippet_data["code"]
            )
            
            # 파일로 저장
            if config.SAVE_INTERMEDIATE_RESULTS:
                snippet.save_to_file(config.OUTPUT_DIR)
            
            # 새 기능인지 확인하고 기능 추가 또는 업데이트
            # (실제로는 더 복잡한 기능 추출 및 매칭 로직이 필요할 수 있음)
            feature_name = f"Feature_{len(project.components[0].features) + 1}" if project.components else "Feature_1"
            feature_desc = f"자동 생성된 기능 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # 첫 번째 컴포넌트가 없으면 생성
            if not project.components:
                component = Component(
                    name="Main Component",
                    description="기획서에서 자동 생성된 메인 컴포넌트"
                )
                project.components.append(component)
            
            # 새 기능 생성 및 코드 스니펫 추가
            feature = Feature(
                name=feature_name,
                description=feature_desc
            )
            feature.code_snippets.append(snippet)
            
            # 컴포넌트에 기능 추가
            project.components[0].features.append(feature)
    
    # 프로젝트 updated_at 갱신
    project.updated_at = datetime.now()
    
    return project

def main():
    """메인 실행 함수"""
    # 인수 파싱
    args = parse_arguments()
    
    # 환경 설정
    setup_environment(args)
    
    # 시작 메시지
    logger.info("=" * 50)
    logger.info("Ollama 자동 기획서 분석 시스템 시작")
    logger.info(f"모델: {config.MODEL_NAME}")
    logger.info(f"최대 실행 시간: {config.MAX_RUNTIME_HOURS}시간")
    logger.info("=" * 50)
    
    # 기획서 로드
    planning_doc = utils.load_planning_docs()
    if not planning_doc:
        logger.error("기획서를 찾을 수 없습니다. planning_docs 폴더에 기획서 파일을 추가해주세요.")
        return
    
    # 상태 초기화 또는 복구
    conversation_history = utils.ConversationHistory(max_history=config.MAX_CONVERSATION_HISTORY)
    
    # 프로젝트 초기화 또는 복구
    project = None
    state = {}
    if args.resume:
        # 이전 상태 복구
        state = utils.load_state()
        if state:
            logger.info("이전 상태에서 계속합니다.")
            
            # 대화 기록 복구
            if "conversation_history" in state:
                for q, a in state["conversation_history"]:
                    conversation_history.add(q, a)
                
                if "summary" in state:
                    conversation_history.summary = state["summary"]
            
            # 프로젝트 복구
            if "project" in state and os.path.exists(os.path.join(config.OUTPUT_DIR, "project.json")):
                project = Project.load_from_json(os.path.join(config.OUTPUT_DIR, "project.json"))
                logger.info(f"프로젝트 '{project.name}' 로드됨")
            
            # 현재 질문 복구
            current_question = state.get("current_question", config.INITIAL_QUESTION)
            logger.info(f"이전 질문: {current_question}")
        else:
            logger.warning("이전 상태를 찾을 수 없습니다. 새로 시작합니다.")
            current_question = config.INITIAL_QUESTION
    else:
        # 새로 시작
        current_question = config.INITIAL_QUESTION
    
    # 프로젝트가 없으면 새로 생성
    if not project:
        project = Project(
            name=f"자동생성_프로젝트_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description="기획서에서 자동으로 생성된 프로젝트"
        )
    
    # 종료 시간 설정
    end_time = datetime.now() + timedelta(hours=config.MAX_RUNTIME_HOURS)
    
    # 반복 카운터
    iteration = state.get("iteration", 1)
    
    try:
        # 메인 루프
        while datetime.now() < end_time and iteration <= config.MAX_ITERATIONS:
            logger.info(f"\n--- 반복 #{iteration} ---")
            logger.info(f"현재 질문: {current_question}")
            
            # 프롬프트 생성
            prompt = create_prompt(planning_doc, conversation_history, current_question)
            
            # Ollama API 호출
            logger.info("Ollama API 호출 중...")
            response = utils.query_ollama(prompt)
            logger.info(f"응답 받음: {len(response)} 글자")
            
            # 대화 기록 업데이트
            conversation_history.add(current_question, response)
            
            # 응답 처리 및 프로젝트 업데이트
            project = process_response(response, project)
            
            # 중간 결과 저장
            if config.SAVE_INTERMEDIATE_RESULTS and iteration % config.INTERMEDIATE_SAVE_INTERVAL == 0:
                project.save_to_json(os.path.join(config.OUTPUT_DIR, "project.json"))
                logger.info("중간 프로젝트 저장됨")
            
            # 대화 기록 요약 (주기적으로)
            if iteration % config.SUMMARIZE_INTERVAL == 0:
                logger.info("대화 기록 요약 생성 중...")
                conversation_history.summarize()
                logger.info("요약 생성됨")
            
            # 대화 기록 저장
            with open(config.CONVERSATION_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n--- 반복 #{iteration} ---\n")
                f.write(f"질문: {current_question}\n")
                f.write(f"응답: {response}\n")
                f.write("-" * 50 + "\n")
            
            # 다음 질문 생성
            logger.info("다음 질문 생성 중...")
            current_question = utils.generate_next_question(response)
            logger.info(f"다음 질문 생성됨: {current_question}")
            
            # 현재 상태 저장
            state = {
                "iteration": iteration,
                "current_question": current_question,
                "conversation_history": conversation_history.history,
                "summary": conversation_history.summary,
                "last_updated": datetime.now().isoformat()
            }
            utils.save_state(state)
            
            # 반복 증가
            iteration += 1
            
            # 제어를 위해 잠시 대기
            logger.info(f"{config.WAIT_TIME_SECONDS}초 대기 중...")
            time.sleep(config.WAIT_TIME_SECONDS)
    
    except KeyboardInterrupt:
        logger.info("\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.exception(f"오류 발생: {e}")
    finally:
        # 최종 결과 저장
        logger.info("최종 결과 저장 중...")
        
        # 프로젝트 저장
        output_file = os.path.join(config.OUTPUT_DIR, args.output)
        project.save_to_json(output_file)
        logger.info(f"프로젝트가 {output_file}에 저장되었습니다.")
        
        # 실행 통계
        total_runtime = datetime.now() - (end_time - timedelta(hours=config.MAX_RUNTIME_HOURS))
        logger.info("=" * 50)
        logger.info("실행 완료")
        logger.info(f"총 반복 횟수: {iteration - 1}")
        logger.info(f"총 실행 시간: {total_runtime}")
        logger.info(f"생성된 기능 수: {sum(len(comp.features) for comp in project.components)}")
        logger.info("=" * 50)

if __name__ == "__main__":
    main()
