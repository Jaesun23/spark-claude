#!/usr/bin/env python3
"""
File Lock Hook for Multi-Team Coordination
Prevents concurrent file modifications by different teams
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

WAIT_QUEUE_FILE = Path(".claude/workflows/file_wait_queue.json")

def load_wait_queue() -> dict[str, Any]:
    """Load wait queue"""
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
    """Add team to wait queue"""
    queue = load_wait_queue()
    normalized_path = str(Path(file_path).as_posix())

    if normalized_path not in queue["wait_queue"]:
        queue["wait_queue"][normalized_path] = []

    # Check if team already waiting
    waiting_teams = [w["team_id"] for w in queue["wait_queue"][normalized_path]]
    if team_id not in waiting_teams:
        queue["wait_queue"][normalized_path].append({
            "team_id": team_id,
            "waiting_since": datetime.now().isoformat(),
            "locked_by": locked_by
        })
        save_wait_queue(queue)
        logger.info(f"📋 {team_id} added to wait queue for {file_path}")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

LOCK_FILE = Path(".claude/workflows/file_locks.json")
COORDINATION_FILE = Path(".claude/workflows/multi_task_coordination.json")

def load_locks() -> dict[str, dict[str, Any]]:
    """Load current file locks"""
    if LOCK_FILE.exists():
        with open(LOCK_FILE) as f:
            return json.load(f)
    return {"locks": {}, "version": 1}

def save_locks(locks: dict[str, dict[str, Any]]) -> None:
    """Save file locks"""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK_FILE, "w") as f:
        json.dump(locks, f, indent=2)

def get_current_team() -> str | None:
    """Determine which team is currently active"""
    # Check each team's current_task.json
    for team_id in ["team1", "team2", "team3", "team4"]:
        task_file = Path(f".claude/workflows/{team_id}_current_task.json")
        if task_file.exists():
            with open(task_file) as f:
                task_data = json.load(f)
                if task_data.get("status") == "IN_PROGRESS":
                    return team_id
    return None

def acquire_lock(file_path: str, team_id: str) -> bool:
    """Try to acquire a lock on a file"""
    locks = load_locks()

    # Normalize path
    normalized_path = str(Path(file_path).resolve())

    # Check if file is already locked
    if normalized_path in locks.get("locks", {}):
        lock_info = locks["locks"][normalized_path]
        if lock_info["team_id"] != team_id:
            # Check if lock is expired (e.g., 30 minutes)
            locked_at = datetime.fromisoformat(lock_info["locked_at"])
            age_minutes = (datetime.now() - locked_at).total_seconds() / 60

            if age_minutes < 5:  # 5분으로 단축
                logger.error(f"❌ File {file_path} is locked by {lock_info['team_id']} ({age_minutes:.1f} minutes ago)")
                return False
            else:
                logger.info(f"🔓 Expired lock on {file_path} (locked {age_minutes:.1f} minutes ago), acquiring for {team_id}")

    # Acquire lock
    if "locks" not in locks:
        locks["locks"] = {}

    locks["locks"][normalized_path] = {
        "team_id": team_id,
        "locked_at": datetime.now().isoformat(),
        "file_path": file_path
    }

    save_locks(locks)
    logger.info(f"🔒 {team_id} acquired lock on {file_path}")
    return True

def release_lock(file_path: str, team_id: str) -> bool:
    """Release a lock on a file"""
    locks = load_locks()
    normalized_path = str(Path(file_path).resolve())

    if normalized_path in locks.get("locks", {}):
        lock_info = locks["locks"][normalized_path]
        if lock_info["team_id"] == team_id:
            del locks["locks"][normalized_path]
            save_locks(locks)
            logger.info(f"🔓 {team_id} released lock on {file_path}")
            return True
    return False

def release_team_locks(team_id: str) -> None:
    """Release all locks held by a team"""
    locks = load_locks()

    # Find all locks held by this team
    team_locks = [
        path for path, info in locks.get("locks", {}).items()
        if info["team_id"] == team_id
    ]

    # Release them
    for path in team_locks:
        del locks["locks"][path]

    if team_locks:
        save_locks(locks)
        logger.info(f"🔓 Released {len(team_locks)} locks for {team_id}")

def check_file_conflict(file_path: str) -> str | None:
    """Check if a file operation would cause a conflict"""
    team_id = get_current_team()
    if not team_id:
        return None

    locks = load_locks()
    normalized_path = str(Path(file_path).resolve())

    if normalized_path in locks.get("locks", {}):
        lock_info = locks["locks"][normalized_path]
        if lock_info["team_id"] != team_id:
            return f"File is locked by {lock_info['team_id']}"

    return None

def main():
    """Main hook function for pre-write operations"""
    try:
        # Read input
        input_data = json.load(sys.stdin)

        # Get file path from input
        file_path = input_data.get("filePath", "")
        if not file_path:
            sys.exit(0)

        # Determine current team
        team_id = get_current_team()
        if not team_id:
            # Not in multi-team mode, allow operation
            sys.exit(0)

        # Check for conflicts
        conflict = check_file_conflict(file_path)
        if conflict:
            # Add to wait queue
            add_to_wait_queue(file_path, team_id, conflict)

            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreWriteFile",
                    "preventDefaultBehavior": True,
                    "errorMessage": f"❌ Cannot modify {file_path}: {conflict}. Please coordinate with other teams or wait for lock release.",
                    "additionalContext": (
                        f"⏳ {team_id}을(를) 대기 목록에 추가했습니다.\n"
                        f"📢 파일이 해제되면 자동으로 알림을 받게 됩니다."
                    )
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # Try to acquire lock
        if acquire_lock(file_path, team_id):
            # Allow the write operation
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreWriteFile",
                    "additionalContext": f"🔒 {team_id} has lock on {file_path}"
                }
            }
            print(json.dumps(output))
        else:
            # Prevent the write operation
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreWriteFile",
                    "preventDefaultBehavior": True,
                    "errorMessage": f"❌ Could not acquire lock on {file_path}. Another team is working on this file."
                }
            }
            print(json.dumps(output))

    except Exception as e:
        logger.error(f"Hook error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
