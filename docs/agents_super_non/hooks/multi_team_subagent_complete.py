#!/usr/bin/env python3
"""
Multi-Team SubagentStop Hook
각 팀의 subagent 완료를 개별적으로 추적하고 2호에게 알림
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

def get_team_from_session(session_id: str, transcript_path: str) -> str:
    """세션 ID나 transcript 경로에서 팀 ID 추출"""
    # transcript 경로나 다른 방법으로 팀 식별
    for team_id in ["team1", "team2", "team3", "team4"]:
        team_file = Path(f".claude/workflows/{team_id}_current_task.json")
        if team_file.exists():
            with open(team_file) as f:
                task_data = json.load(f)
                # 현재 IN_PROGRESS인 팀 찾기
                if task_data.get("status") == "IN_PROGRESS":
                    return team_id
    return None

def update_team_status(team_id: str, agent_name: str, session_id: str):
    """특정 팀의 상태 업데이트"""
    team_file = Path(f".claude/workflows/{team_id}_current_task.json")

    if not team_file.exists():
        return

    with open(team_file) as f:
        team_data = json.load(f)

    # 완료된 agent 추가
    if "completed_agents" not in team_data:
        team_data["completed_agents"] = []

    team_data["completed_agents"].append({
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "session_id": session_id
    })

    # 상태 업데이트
    if agent_name == "implementer":
        team_data["status"] = "IMPLEMENTATION_COMPLETE"
        logger.info(f"✅ {team_id} Implementation 완료!")
    elif agent_name == "quality":
        team_data["status"] = "QUALITY_COMPLETE"
    elif agent_name == "tester":
        team_data["status"] = "TESTING_COMPLETE"

    # 저장
    with open(team_file, "w") as f:
        json.dump(team_data, f, indent=2)

def check_all_teams_status():
    """모든 팀의 상태 확인 및 다음 단계 결정"""
    teams_status = {}
    for team_id in ["team1", "team2", "team3", "team4"]:
        team_file = Path(f".claude/workflows/{team_id}_current_task.json")
        if team_file.exists():
            with open(team_file) as f:
                team_data = json.load(f)
                teams_status[team_id] = team_data.get("status", "UNKNOWN")

    # 완료된 팀 수 계산
    completed = sum(1 for status in teams_status.values()
                   if "COMPLETE" in status)

    return teams_status, completed

def generate_next_action(team_id: str, teams_status: dict):
    """완료된 팀에 대한 다음 작업 생성"""
    # 다른 팀들이 아직 작업 중인지 확인
    working_teams = [t for t, s in teams_status.items()
                    if t != team_id and s == "IN_PROGRESS"]

    if working_teams:
        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 {team_id} 완료! 다음 작업 가능!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{team_id}가 작업을 완료했습니다.
아직 작업 중인 팀: {', '.join(working_teams)}

2호님, {team_id}에게 다음 작업을 할당할 수 있습니다:
1. 다음 Task 할당 (남은 작업이 있다면)
2. Quality/Test 단계로 진행
3. 다른 팀 지원

명령 예시:
@{team_id}_quality
이전 구현을 검증하세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return None

def main():
    """메인 hook 함수"""
    try:
        input_data = json.load(sys.stdin)

        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        # 어느 팀의 subagent인지 확인
        team_id = get_team_from_session(session_id, transcript_path)

        if not team_id:
            logger.warning("팀을 식별할 수 없습니다.")
            sys.exit(0)

        # agent 타입 추측 (transcript나 다른 정보에서)
        agent_name = "implementer"  # 기본값

        # 팀 상태 업데이트
        update_team_status(team_id, agent_name, session_id)

        # 전체 팀 상태 확인
        teams_status, completed_count = check_all_teams_status()

        logger.info(f"📊 전체 진행 상황: {completed_count}/4 팀 완료")
        for t, s in teams_status.items():
            logger.info(f"   {t}: {s}")

        # 다음 작업 제안
        next_action = generate_next_action(team_id, teams_status)

        if next_action:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SubagentStop",
                    "additionalContext": next_action,
                    "team_complete": team_id,
                    "all_teams_status": teams_status
                }
            }
            print(json.dumps(output))

    except Exception as e:
        logger.error(f"Multi-team SubagentStop error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
