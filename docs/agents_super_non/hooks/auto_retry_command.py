#!/usr/bin/env python3
"""
Auto Retry Command Generator
파일 lock이 해제되면 2호가 즉시 실행할 수 있는 명령을 생성
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    """PostToolUse hook - 파일 수정 완료 시 재시도 명령 생성"""
    try:
        input_data = json.load(sys.stdin)

        # Write/Edit 작업 후에만 동작
        tool = input_data.get("tool", "")
        if tool not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = input_data.get("filePath", "")
        if not file_path:
            sys.exit(0)

        # 대기 큐 확인
        wait_queue_file = Path(".claude/workflows/file_wait_queue.json")
        if not wait_queue_file.exists():
            sys.exit(0)

        with open(wait_queue_file) as f:
            wait_queue = json.load(f)

        normalized_path = str(Path(file_path).as_posix())
        if normalized_path not in wait_queue.get("wait_queue", {}):
            sys.exit(0)

        waiting_teams = wait_queue["wait_queue"][normalized_path]
        if not waiting_teams:
            sys.exit(0)

        next_team = waiting_teams[0]["team_id"]

        # 대기 큐에서 제거
        wait_queue["wait_queue"][normalized_path] = waiting_teams[1:]
        if not wait_queue["wait_queue"][normalized_path]:
            del wait_queue["wait_queue"][normalized_path]

        with open(wait_queue_file, "w") as f:
            json.dump(wait_queue, f, indent=2)

        # 2호가 바로 실행할 수 있는 명령 생성
        retry_command = f"""
@{next_team}_implementer

이전에 lock으로 차단되었던 {Path(file_path).name} 파일이 이제 사용 가능합니다.
해당 파일에 대한 수정 작업을 즉시 재시도하세요.

이것은 자동 재시도 시스템에 의한 지시입니다.
"""

        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 **2호님, 아래 명령을 복사해서 즉시 실행해주세요!**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{retry_command}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 파일 lock 자동 재할당 시스템
• 해제된 파일: {Path(file_path).name}
• 다음 대기 팀: {next_team}
• 남은 대기 팀: {len(waiting_teams) - 1}개
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                "auto_command_generated": True,
                "next_team": next_team,
                "file_released": file_path
            }
        }

        print(json.dumps(output))

    except Exception as e:
        # 에러는 조용히 처리 (hook이 실패해도 작업은 계속되어야 함)
        sys.exit(0)

if __name__ == "__main__":
    main()
