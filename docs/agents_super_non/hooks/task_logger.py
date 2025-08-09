#!/usr/bin/env python3
"""
PostToolUse hook for Task tool
Logs task execution and updates tracking
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

# 프롬프트 미리보기 길이
PROMPT_PREVIEW_LENGTH = 100


def main() -> None:
    try:
        # stdin에서 JSON 읽기
        input_data = json.load(sys.stdin)

        # Task 정보 추출
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        description = tool_input.get("description", "Unknown task")
        prompt = tool_input.get("prompt", "")

        # description에서 에이전트 타입 추출
        agent_type = "unknown"
        if "Implementation" in description:
            agent_type = "implementer"
            emoji = "1️⃣"
        elif "Testing" in description:
            agent_type = "tester"
            emoji = "2️⃣"
        elif "Quality" in description:
            agent_type = "quality"
            emoji = "3️⃣"
        elif "Review" in description:
            agent_type = "reviewer"
            emoji = "4️⃣"
        elif "Report" in description:
            agent_type = "reporter"
            emoji = "5️⃣"
        else:
            emoji = "📝"

        print(f"{emoji} Task 실행됨: {description}", file=sys.stderr)

        # current_task.json 업데이트 (있는 경우)
        task_file = os.path.join(
            os.environ.get("CLAUDE_PROJECT_DIR", "."),
            ".claude/workflows/current_task.json",
        )

        if os.path.exists(task_file):
            try:
                with Path(task_file).open() as f:
                    current_task = json.load(f)
            except Exception:
                current_task = {}

            # Task 실행 로그 추가
            if "task_executions" not in current_task:
                current_task["task_executions"] = []

            current_task["task_executions"].append(
                {
                    "timestamp": datetime.now().isoformat(),  # noqa: DTZ005
                    "description": description,
                    "agent_type": agent_type,
                    "prompt_preview": prompt[:PROMPT_PREVIEW_LENGTH] + "..."
                    if len(prompt) > PROMPT_PREVIEW_LENGTH
                    else prompt,
                }
            )

            # 현재 실행 중인 에이전트 기록
            current_task["current_agent"] = agent_type

            # 파일 다시 저장
            try:
                with Path(task_file).open("w") as f:
                    json.dump(current_task, f, indent=2)
                print(f"✅ Task 실행 기록 저장됨 ({agent_type})", file=sys.stderr)

                # 진행 상황 표시
                execution_count = len(current_task["task_executions"])
                print(f"   진행: {execution_count}번째 Task 호출", file=sys.stderr)

            except Exception as e:
                print(f"⚠️ Task 기록 저장 실패 (무시): {e}", file=sys.stderr)
        else:
            # current_task.json이 없으면 경고
            msg = "⚠️ current_task.json이 없습니다. /implement 명령어로 시작했는지 확인하세요."
            logger.warning(msg)

        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"❌ 잘못된 JSON 입력: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 오류 발생: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
