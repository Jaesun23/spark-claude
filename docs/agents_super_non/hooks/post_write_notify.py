#!/usr/bin/env python3
"""
Post-Write Notification Hook
Notifies when teams complete modifications to shared files
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

LOCK_FILE = Path(".claude/workflows/file_locks.json")
NOTIFICATION_FILE = Path(".claude/workflows/file_notifications.json")

# 공통 파일 목록
SHARED_FILES = [
    "src/dna/endocrine/constants.py",
    "src/dna/skeletal/types.py",
    ".import-linter.toml",
    "pyproject.toml"
]

def is_shared_file(file_path: str) -> bool:
    """Check if file is a shared resource"""
    normalized = str(Path(file_path).as_posix())
    return any(shared in normalized for shared in SHARED_FILES)

def get_current_team() -> str:
    """Determine which team is currently active"""
    for team_id in ["team1", "team2", "team3", "team4"]:
        task_file = Path(f".claude/workflows/{team_id}_current_task.json")
        if task_file.exists():
            try:
                with open(task_file) as f:
                    task_data = json.load(f)
                    if task_data.get("status") == "IN_PROGRESS":
                        return team_id
            except:
                continue
    return "unknown"

def load_notifications() -> dict[str, Any]:
    """Load current notifications"""
    if NOTIFICATION_FILE.exists():
        with open(NOTIFICATION_FILE) as f:
            return json.load(f)
    return {"notifications": [], "version": 1}

def save_notifications(notifications: dict[str, Any]) -> None:
    """Save notifications"""
    NOTIFICATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTIFICATION_FILE, "w") as f:
        json.dump(notifications, f, indent=2)

def load_wait_queue() -> dict[str, Any]:
    """Load wait queue to check waiting teams"""
    wait_queue_file = Path(".claude/workflows/file_wait_queue.json")
    if wait_queue_file.exists():
        with open(wait_queue_file) as f:
            return json.load(f)
    return {"wait_queue": {}, "version": 1}

def save_wait_queue(queue: dict[str, Any]) -> None:
    """Save wait queue after clearing waiting teams"""
    wait_queue_file = Path(".claude/workflows/file_wait_queue.json")
    wait_queue_file.parent.mkdir(parents=True, exist_ok=True)
    with open(wait_queue_file, "w") as f:
        json.dump(queue, f, indent=2)

def add_notification(file_path: str, team_id: str, operation: str) -> None:
    """Add a notification for completed file operation"""
    notifications = load_notifications()

    notification = {
        "timestamp": datetime.now().isoformat(),
        "team_id": team_id,
        "file_path": file_path,
        "operation": operation,
        "status": "completed",
        "is_shared": is_shared_file(file_path)
    }

    if "notifications" not in notifications:
        notifications["notifications"] = []

    notifications["notifications"].append(notification)

    # Keep only last 50 notifications
    if len(notifications["notifications"]) > 50:
        notifications["notifications"] = notifications["notifications"][-50:]

    save_notifications(notifications)

def release_file_lock(file_path: str, team_id: str) -> None:
    """Release lock on file after successful write"""
    if not LOCK_FILE.exists():
        return

    try:
        with open(LOCK_FILE) as f:
            locks = json.load(f)

        normalized_path = str(Path(file_path).resolve())

        if normalized_path in locks.get("locks", {}):
            lock_info = locks["locks"][normalized_path]
            if lock_info["team_id"] == team_id:
                del locks["locks"][normalized_path]

                with open(LOCK_FILE, "w") as f:
                    json.dump(locks, f, indent=2)

                logger.info(f"🔓 {team_id} released lock on {file_path}")
    except Exception as e:
        logger.error(f"Failed to release lock: {e}")

def main():
    """Main hook function for post-write operations"""
    try:
        # Read input
        input_data = json.load(sys.stdin)

        # Extract file path and operation
        file_path = input_data.get("filePath", "")
        operation = input_data.get("operation", "write")

        if not file_path:
            sys.exit(0)

        # Get current team
        team_id = get_current_team()

        # Add notification
        add_notification(file_path, team_id, operation)

        # Release lock
        release_file_lock(file_path, team_id)

        # Check if there are teams waiting for this file
        wait_queue = load_wait_queue()
        normalized_path = str(Path(file_path).as_posix())
        waiting_teams = []

        if normalized_path in wait_queue.get("wait_queue", {}):
            waiting_teams = [w["team_id"] for w in wait_queue["wait_queue"][normalized_path]]
            # Clear the wait queue for this file
            del wait_queue["wait_queue"][normalized_path]
            save_wait_queue(wait_queue)

        # Special notification for shared files
        if is_shared_file(file_path):
            if waiting_teams:
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": (
                            f"📢 {team_id} 완료: {Path(file_path).name}\n"
                            f"🔓 공통 파일 잠금 해제됨\n"
                            f"⏳ 대기 중인 팀: {', '.join(waiting_teams)}\n"
                            f"➡️ **즉시 재시도 필요**: {waiting_teams[0]}에게 {Path(file_path).name} 수정을 다시 시도하도록 지시하세요!"
                        ),
                        "action_required": {
                            "type": "retry_file_operation",
                            "team": waiting_teams[0],
                            "file": file_path,
                            "waiting_teams": waiting_teams
                        }
                    }
                }
            else:
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": (
                            f"📢 {team_id} 완료: {Path(file_path).name}\n"
                            f"🔓 공통 파일 잠금 해제됨\n"
                            f"✅ 다른 팀이 이제 이 파일을 수정할 수 있습니다."
                        )
                    }
                }
        else:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": f"✅ {team_id}: {Path(file_path).name} 수정 완료"
                }
            }

        print(json.dumps(output))

    except Exception as e:
        logger.error(f"Post-write hook error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
