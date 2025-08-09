#!/usr/bin/env python3
"""
UserPromptSubmit hook
Routes specific commands and adds context
"""

import json
import logging
import re
import sys

# Set up logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def main() -> None:
    try:
        # stdin에서 JSON 읽기
        input_data = json.load(sys.stdin)

        # 프롬프트 추출
        prompt = input_data.get("prompt", "")

        # /implement 패턴 확인
        implement_match = re.match(
            r"^/implement\s+(TASK-[A-Z0-9]+-[0-9]+|docs/planning/.*\.md|.*\.md)", prompt
        )
        if implement_match:
            logger.info("🚀 완전 자동화 워크플로우 시작 - 구멍 방지 시스템 활성화...")
            logger.info("📋 5개 전문 에이전트가 순차적으로 작업을 처리합니다:")
            logger.info("  1️⃣ Implementer - 코드 구현")
            logger.info("  2️⃣ Tester - 테스트 작성")
            logger.info("  3️⃣ Quality - 품질 검증")
            logger.info("  4️⃣ Reviewer - 아키텍처 리뷰")
            logger.info("  5️⃣ Reporter - 최종 보고서")

            # hookSpecificOutput으로 컨텍스트 추가
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "🚀 V5 자동화 워크플로우가 활성화되었습니다. "
                        "5개 전문 에이전트가 순차적으로 작업을 처리합니다.\n\n"
                        "중요: 반드시 Task 도구를 5번 호출하여 각 에이전트를 순차적으로 실행하세요."
                    ),
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # stage1-next 패턴 확인
        if prompt.strip() == "/stage1-next":
            logger.info("🔍 Stage 1 다음 체크리스트 확인 중...")

            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "📊 Stage 1 Bootstrap 진행 상황을 확인하고 다음 체크리스트를 실행합니다."
                    ),
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # 품질관리 패턴 확인
        if prompt.strip() == "/품질관리" or prompt.strip() == "/quality":
            logger.info("🛡️ V5 품질 관리 시스템 활성화...")

            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "🛡️ V5 코드 품질 무결점 달성을 위한 통합 품질 관리를 시작합니다. "
                        "모든 품질 도구에서 0개 위반을 목표로 합니다."
                    ),
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # dna-check 패턴 확인
        if prompt.strip().startswith("/dna-check"):
            logger.info("🧬 DNA 시스템 건강도 검사 시작...")

            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "🧬 DNA v3.5 시스템의 전체 건강도를 검사합니다. "
                        "8개 DNA 시스템의 상태를 종합적으로 점검합니다."
                    ),
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # 일반 프롬프트는 그대로 통과
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"❌ 잘못된 JSON 입력: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
