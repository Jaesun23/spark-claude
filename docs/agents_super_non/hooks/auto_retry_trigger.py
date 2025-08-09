#!/usr/bin/env python3
"""
Auto Retry Trigger
자동으로 대기 중인 팀에게 재시도를 트리거하는 메커니즘
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def check_and_trigger_retries():
    """알림을 확인하고 대기 중인 팀에게 재시도 트리거"""
    notifications_file = Path(".claude/workflows/file_notifications.json")

    if not notifications_file.exists():
        return

    with open(notifications_file) as f:
        notifications = json.load(f)

    # 최근 알림 확인 (최근 1분 이내)
    recent_notifications = []
    for notif in notifications.get("notifications", []):
        timestamp = datetime.fromisoformat(notif["timestamp"])
        age_seconds = (datetime.now() - timestamp).total_seconds()
        if age_seconds < 60:  # 1분 이내
            recent_notifications.append(notif)

    # 대기 큐 확인
    wait_queue_file = Path(".claude/workflows/file_wait_queue.json")
    if wait_queue_file.exists():
        with open(wait_queue_file) as f:
            wait_queue = json.load(f)

        # 해제된 파일에 대한 대기 팀 확인
        for notif in recent_notifications:
            file_path = notif["file_path"]
            normalized_path = str(Path(file_path).as_posix())

            if normalized_path in wait_queue.get("wait_queue", {}):
                waiting_teams = wait_queue["wait_queue"][normalized_path]
                if waiting_teams:
                    first_team = waiting_teams[0]["team_id"]

                    # 해당 팀의 current_task.json 업데이트
                    team_task_file = Path(f".claude/workflows/{first_team}_current_task.json")
                    if team_task_file.exists():
                        with open(team_task_file) as f:
                            task_data = json.load(f)

                        # 재시도 플래그 설정
                        task_data["retry_pending"] = {
                            "file": file_path,
                            "reason": "lock_released",
                            "timestamp": datetime.now().isoformat()
                        }

                        with open(team_task_file, "w") as f:
                            json.dump(task_data, f, indent=2)

                        print(f"🔔 {first_team}: {Path(file_path).name} 재시도 준비 완료!")

def main():
    """Hook 또는 독립 실행용 메인 함수"""
    try:
        # stdin이 있으면 hook으로 실행됨
        if not sys.stdin.isatty():
            input_data = json.load(sys.stdin)
            # Hook으로 실행될 때의 로직

        # 독립 실행 시
        check_and_trigger_retries()

    except Exception as e:
        print(f"Auto retry error: {e}")

if __name__ == "__main__":
    main()
