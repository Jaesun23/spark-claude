#!/usr/bin/env python3
"""
Lock Wait Manager Hook
Tracks which teams are waiting for specific files and notifies 2호 when they become available
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

WAIT_QUEUE_FILE = Path(".claude/workflows/file_wait_queue.json")
LOCK_FILE = Path(".claude/workflows/file_locks.json")

def load_wait_queue() -> dict[str, Any]:
    """Load current wait queue"""
    if WAIT_QUEUE_FILE.exists():
        with open(WAIT_QUEUE_FILE) as f:
            return json.load(f)
    return {"wait_queue": {}, "version": 1}

def save_wait_queue(queue: dict[str, Any]) -> None:
    """Save wait queue"""
    WAIT_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(WAIT_QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

def add_to_wait_queue(file_path: str, team_id: str, locked_by: str) -> None:
    """Add a team to the wait queue for a file"""
    queue = load_wait_queue()

    normalized_path = str(Path(file_path).as_posix())

    if normalized_path not in queue["wait_queue"]:
        queue["wait_queue"][normalized_path] = []

    # Check if team is already waiting
    waiting_teams = [w["team_id"] for w in queue["wait_queue"][normalized_path]]
    if team_id not in waiting_teams:
        queue["wait_queue"][normalized_path].append({
            "team_id": team_id,
            "waiting_since": datetime.now().isoformat(),
            "locked_by": locked_by,
            "attempt_count": 1
        })
    else:
        # Increment attempt count
        for wait_info in queue["wait_queue"][normalized_path]:
            if wait_info["team_id"] == team_id:
                wait_info["attempt_count"] += 1

    save_wait_queue(queue)
    logger.info(f"📋 {team_id} added to wait queue for {file_path}")

def get_waiting_teams(file_path: str) -> list[dict[str, Any]]:
    """Get list of teams waiting for a file"""
    queue = load_wait_queue()
    normalized_path = str(Path(file_path).as_posix())

    return queue["wait_queue"].get(normalized_path, [])

def clear_wait_queue(file_path: str) -> list[str]:
    """Clear wait queue for a file and return waiting teams"""
    queue = load_wait_queue()
    normalized_path = str(Path(file_path).as_posix())

    waiting_teams = []
    if normalized_path in queue["wait_queue"]:
        waiting_teams = [w["team_id"] for w in queue["wait_queue"][normalized_path]]
        del queue["wait_queue"][normalized_path]
        save_wait_queue(queue)

    return waiting_teams

def check_file_lock_released(file_path: str) -> bool:
    """Check if a file lock has been released"""
    if not LOCK_FILE.exists():
        return True

    try:
        with open(LOCK_FILE) as f:
            locks = json.load(f)

        normalized_path = str(Path(file_path).resolve())
        return normalized_path not in locks.get("locks", {})
    except:
        return True

def main():
    """Main hook function - called when a file operation is blocked"""
    try:
        # Read input
        input_data = json.load(sys.stdin)

        # Check if this is a lock conflict notification
        error_message = input_data.get("errorMessage", "")
        if "is locked by" in error_message:
            # Extract team and file info
            import re
            match = re.search(r"File (.*?) is locked by (team\d+)", error_message)
            if match:
                file_path = match.group(1)
                locked_by = match.group(2)

                # Get requesting team
                team_id = input_data.get("team_id", "unknown")

                # Add to wait queue
                add_to_wait_queue(file_path, team_id, locked_by)

                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "FileLockConflict",
                        "additionalContext": (
                            f"⏳ {team_id} 대기 등록: {Path(file_path).name}\n"
                            f"🔒 현재 {locked_by}가 작업 중\n"
                            f"📢 작업 완료 시 자동으로 알림을 받습니다."
                        )
                    }
                }
                print(json.dumps(output))

        # Check if this is a file release notification
        elif "released lock on" in input_data.get("message", ""):
            match = re.search(r"released lock on (.*?)$", input_data["message"])
            if match:
                file_path = match.group(1)

                # Get waiting teams
                waiting_teams = clear_wait_queue(file_path)

                if waiting_teams:
                    output = {
                        "hookSpecificOutput": {
                            "hookEventName": "FileLockReleased",
                            "additionalContext": (
                                f"🔓 {Path(file_path).name} 잠금 해제!\n"
                                f"📢 대기 중인 팀: {', '.join(waiting_teams)}\n"
                                f"➡️ 2호님, 다음 팀에게 재시도를 지시해주세요:\n"
                                f"   {waiting_teams[0]} → {Path(file_path).name} 수정 재시도"
                            ),
                            "waiting_teams": waiting_teams,
                            "released_file": file_path
                        }
                    }
                    print(json.dumps(output))

    except Exception as e:
        logger.error(f"Lock wait manager error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
