#!/usr/bin/env python3
"""
PostToolUse hook for Write/Edit/MultiEdit tools
Runs quality checks after file modifications
"""

import json
import logging
import sys
from pathlib import Path

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

        # Python 파일인 경우 품질 검사
        if file_path.endswith(".py"):
            logger.info(f"✨ 품질 검사 시작: {file_path}")

            # ruff 실행 (pre-commit hooks will handle security checks)
            # Using explicit path for safety
            uv_path = Path("/usr/bin/env").parent / "uv"
            try:
                import subprocess

                result = subprocess.run(  # noqa: S603
                    [str(uv_path), "run", "ruff", "check", file_path, "--fix"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    logger.info(f"✅ Ruff 검사 통과: {file_path}")
                else:
                    logger.warning(f"⚠️ Ruff 경고: {result.stdout}")
            except Exception as e:
                logger.warning(f"⚠️ Ruff 실행 중 오류 (무시): {e}")

            # 커스텀 품질 검사 스크립트 실행 (있는 경우)
            import os

            quality_script = (
                Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
                / ".claude"
                / "workflows"
                / "check_quality_standards.py"
            )
            if quality_script.exists():
                try:
                    python_path = Path("/usr/bin/python3")
                    import subprocess

                    result = subprocess.run(  # noqa: S603
                        [str(python_path), str(quality_script), file_path],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode == 0:
                        logger.info(f"✅ 품질 기준 통과: {file_path}")
                except Exception as e:
                    logger.warning(f"⚠️ 품질 검사 중 오류 (무시): {e}")

        # 항상 성공 (도구 실행을 방해하지 않음)
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"❌ 잘못된 JSON 입력: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
