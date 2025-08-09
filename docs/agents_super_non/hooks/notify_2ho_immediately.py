#!/usr/bin/env python3
"""
Notify 2호 Immediately Hook
파일 수정이 완료되면 즉시 2호에게 재할당 신호를 보내는 hook
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

def load_wait_queue():
    """대기 큐 로드"""
    wait_queue_file = Path(".claude/workflows/file_wait_queue.json")
    if wait_queue_file.exists():
        with open(wait_queue_file) as f:
            return json.load(f)
    return {"wait_queue": {}}

def create_2ho_command(file_path: str, next_team: str):
    """2호를 위한 즉시 실행 명령 생성"""
    return {
        "action": "immediate_retry",
        "instruction": f"""
🚨 즉시 행동 필요!

{next_team} implementer agent를 호출하여 다음 지시를 전달하세요:

"이전에 lock으로 차단되었던 {Path(file_path).name} 파일이 이제 사용 가능합니다.
즉시 수정 작업을 재시도하세요."

⚡ 이것은 자동 재시도 시스템의 일부입니다. 즉시 실행해주세요!
""",
        "target_agent": f"{next_team}_implementer",
        "retry_file": file_path
    }

def main():
    """메인 hook 함수"""
    try:
        input_data = json.load(sys.stdin)

        # PostToolUse에서만 작동
        if input_data.get("tool") not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = input_data.get("filePath", "")
        if not file_path:
            sys.exit(0)

        # 대기 큐 확인
        wait_queue = load_wait_queue()
        normalized_path = str(Path(file_path).as_posix())

        if normalized_path in wait_queue.get("wait_queue", {}):
            waiting_teams = wait_queue["wait_queue"][normalized_path]
            if waiting_teams:
                next_team = waiting_teams[0]["team_id"]

                # 2호를 위한 명령 생성
                command = create_2ho_command(file_path, next_team)

                # 즉시 실행 파일 생성 (2호가 감지할 수 있도록)
                immediate_action_file = Path(".claude/workflows/immediate_action_for_2ho.json")
                with open(immediate_action_file, "w") as f:
                    json.dump({
                        "created_at": datetime.now().isoformat(),
                        "command": command,
                        "status": "pending"
                    }, f, indent=2)

                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": f"""
🚀 자동 재할당 시스템 작동!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 해제된 파일: {Path(file_path).name}
👥 다음 대기 팀: {next_team}
🎯 즉시 행동: immediate_action_for_2ho.json 생성됨

2호님, 위 파일을 확인하고 즉시 실행해주세요!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        "urgent": True,
                        "auto_retry_triggered": True
                    }
                }
                print(json.dumps(output))

    except Exception as e:
        logger.error(f"Notify 2ho error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
