#!/usr/bin/env python3
"""
Improved Multi-Team SubagentStop Hook
더 정확한 팀 식별과 멀티 모드 감지
"""

import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

def is_multi_team_mode() -> bool:
    """멀티 팀 모드인지 확인"""
    coord_file = Path(".claude/workflows/multi_task_coordination.json")
    if not coord_file.exists():
        return False

    try:
        with open(coord_file) as f:
            coord = json.load(f)

        # 실제로 작업 중인 팀 수 확인
        active_teams = sum(
            1 for team in coord.get("teams", {}).values()
            if team.get("status") not in ["READY", "INACTIVE", None]
        )

        return active_teams >= 2  # 2개 이상 팀이 활성화되어 있으면 멀티 모드
    except:
        return False

def extract_team_from_transcript(transcript_path: str) -> str:
    """Transcript 경로에서 팀 ID 추출 시도"""
    if not transcript_path:
        return None

    # 경로에 team1_implementer 같은 패턴이 있는지 확인
    team_pattern = r'(team[1-4])_'
    match = re.search(team_pattern, transcript_path)
    if match:
        return match.group(1)

    # transcript 파일 내용에서 힌트 찾기 (읽을 수 있다면)
    try:
        transcript_file = Path(transcript_path)
        if transcript_file.exists():
            content = transcript_file.read_text()[:1000]  # 처음 1000자만
            # "team1_implementer" 같은 패턴 찾기
            match = re.search(r'(team[1-4])_\w+', content)
            if match:
                return match.group(1)
    except:
        pass

    return None

def find_most_recent_active_team() -> str:
    """가장 최근에 활동한 팀 찾기 (마지막 수단)"""
    recent_team = None
    recent_time = None

    for team_id in ["team1", "team2", "team3", "team4"]:
        team_file = Path(f".claude/workflows/{team_id}_current_task.json")
        if team_file.exists():
            try:
                # 파일 수정 시간 확인
                mtime = team_file.stat().st_mtime
                with open(team_file) as f:
                    data = json.load(f)
                    # IN_PROGRESS 상태이고 가장 최근에 수정된 팀
                    if data.get("status") == "IN_PROGRESS":
                        if recent_time is None or mtime > recent_time:
                            recent_time = mtime
                            recent_team = team_id
            except:
                continue

    return recent_team

def identify_team(input_data: dict) -> str:
    """여러 방법으로 팀 식별 시도"""

    # 1. transcript 경로에서 추출
    team_id = extract_team_from_transcript(input_data.get("transcript_path", ""))
    if team_id:
        logger.info(f"✅ Transcript에서 팀 식별: {team_id}")
        return team_id

    # 2. session_id에 힌트가 있는지 확인
    session_id = input_data.get("session_id", "")
    if "team1" in session_id.lower():
        return "team1"
    elif "team2" in session_id.lower():
        return "team2"
    elif "team3" in session_id.lower():
        return "team3"
    elif "team4" in session_id.lower():
        return "team4"

    # 3. 마지막 수단: 가장 최근 활동 팀
    team_id = find_most_recent_active_team()
    if team_id:
        logger.warning(f"⚠️ 추측으로 팀 식별: {team_id}")
        return team_id

    return None

def main():
    """메인 hook 함수"""
    try:
        input_data = json.load(sys.stdin)

        # 멀티 팀 모드가 아니면 종료
        if not is_multi_team_mode():
            logger.info("단일 작업 모드 - multi_team hook 스킵")
            sys.exit(0)

        logger.info("🚀 멀티 팀 모드 감지!")

        # 팀 식별
        team_id = identify_team(input_data)

        if not team_id:
            logger.error("❌ 팀을 식별할 수 없습니다")
            sys.exit(0)

        # 팀 상태 업데이트
        team_file = Path(f".claude/workflows/{team_id}_current_task.json")
        if team_file.exists():
            with open(team_file) as f:
                team_data = json.load(f)

            # 완료 표시
            team_data["status"] = "SUBAGENT_COMPLETE"
            team_data["completed_at"] = datetime.now().isoformat()

            with open(team_file, "w") as f:
                json.dump(team_data, f, indent=2)

            logger.info(f"✅ {team_id} 작업 완료!")

            # 다른 팀 상태 확인
            other_teams_status = []
            for other_team in ["team1", "team2", "team3", "team4"]:
                if other_team != team_id:
                    other_file = Path(f".claude/workflows/{other_team}_current_task.json")
                    if other_file.exists():
                        with open(other_file) as f:
                            other_data = json.load(f)
                            if other_data.get("status") == "IN_PROGRESS":
                                other_teams_status.append(other_team)

            if other_teams_status:
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "SubagentStop",
                        "additionalContext": f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 {team_id} 완료! 다음 작업 준비됨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

아직 작업 중: {', '.join(other_teams_status)}

2호님, {team_id}에게 다음 작업을 할당하거나
품질 검증 단계로 진행할 수 있습니다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        "team_complete": team_id,
                        "teams_in_progress": other_teams_status
                    }
                }
                print(json.dumps(output))

    except Exception as e:
        logger.error(f"Hook error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
