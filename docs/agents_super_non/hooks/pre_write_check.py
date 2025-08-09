#!/usr/bin/env python3
"""
PreToolUse hook for Write/Edit/MultiEdit tools
Validates file operations before they happen
"""

import json
import logging
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

        # 도구 정보 추출
        tool_input = input_data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        # src/**/*.py 파일인지 확인
        if file_path.startswith("src/") and file_path.endswith(".py"):
            logger.info(f"🔍 Python 파일 작성 준비: {file_path}")

            # 필수 DNA imports 확인을 위한 준비
            # 실제로는 여기서 추가 검증 로직을 구현할 수 있음

        # tests/**/*.py 파일인지 확인
        elif file_path.startswith("tests/") and file_path.endswith(".py"):
            logger.info(f"🧪 테스트 파일 작성 준비: {file_path}")

        # 정상 진행 (exit code 0)
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"❌ 잘못된 JSON 입력: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
