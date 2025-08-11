#!/bin/bash

# SPARK 범용 AI 에이전트 시스템 제거 프로그램
# Claude Code 환경에서 SPARK를 제거합니다

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
clear
echo -e "${RED}"
echo "⚠️  SPARK 제거 프로그램  ⚠️"
echo -e "${NC}"
echo "이 스크립트는 SPARK 구성요소를 제거합니다."
echo ""

# Select location to uninstall from
echo -e "${CYAN}=== 제거할 위치 선택 ===${NC}"
echo ""
echo "1) 전역 설치 제거 (~/.claude/)"
echo "2) 프로젝트별 설치 제거"
echo "3) 취소"
echo ""

read -p "선택 [1-3]: " choice

case $choice in
    1)
        UNINSTALL_LOCATION="$HOME/.claude"
        print_status "전역 설치 제거 선택: $UNINSTALL_LOCATION"
        ;;
    2)
        read -p "프로젝트 디렉토리 경로 입력: " project_dir
        if [ ! -d "$project_dir" ]; then
            print_error "디렉토리가 존재하지 않음: $project_dir"
            exit 1
        fi
        UNINSTALL_LOCATION="$project_dir/.claude"
        print_status "프로젝트 설치 제거 선택: $UNINSTALL_LOCATION"
        ;;
    3)
        print_warning "제거 취소됨"
        exit 0
        ;;
    *)
        print_error "잘못된 선택"
        exit 1
        ;;
esac

# Check if SPARK is installed
if [ ! -d "$UNINSTALL_LOCATION" ]; then
    print_error "설치된 SPARK를 찾을 수 없음: $UNINSTALL_LOCATION"
    exit 1
fi

echo ""
echo -e "${YELLOW}=== 제거할 구성요소 ===${NC}"
echo ""

# List what will be removed
echo "다음 항목들이 제거됩니다:"
[ -d "$UNINSTALL_LOCATION/agents" ] && echo "  • SPARK 에이전트 (*.md 파일)"
[ -d "$UNINSTALL_LOCATION/commands" ] && echo "  • SPARK 명령어 (spark-*.json)"
[ -d "$UNINSTALL_LOCATION/hooks" ] && echo "  • SPARK 훅 (spark_*.py)"
[ -d "$UNINSTALL_LOCATION/workflows" ] && echo "  • SPARK 워크플로우 설정"
[ -f "$UNINSTALL_LOCATION/SPARK_AGENTS_MEMORY_REFERENCE.md" ] && echo "  • 메모리 레퍼런스 파일"
[ -f "$UNINSTALL_LOCATION/SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" ] && echo "  • SPARK 글로벌 가이드 파일"
[ -f "$UNINSTALL_LOCATION/CLAUDE.md" ] && echo "  • CLAUDE.md의 SPARK 섹션"
[ -f "$HOME/.claude/CLAUDE.md" ] && echo "  • ~/.claude/CLAUDE.md의 SPARK 레퍼런스"

echo ""
read -p "정말로 제거하시겠습니까? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    print_warning "제거 취소됨"
    exit 0
fi

# Remove SPARK components
print_status "SPARK 구성요소 제거 중..."

# Remove agents
if [ -d "$UNINSTALL_LOCATION/agents" ]; then
    rm -f "$UNINSTALL_LOCATION/agents"/*-spark.md
    echo "  ✓ 에이전트 제거됨"
fi

# Remove commands
if [ -d "$UNINSTALL_LOCATION/commands" ]; then
    rm -f "$UNINSTALL_LOCATION/commands"/spark-*.json
    echo "  ✓ 명령어 제거됨"
fi

# Remove hooks
if [ -d "$UNINSTALL_LOCATION/hooks" ]; then
    rm -f "$UNINSTALL_LOCATION/hooks"/spark_*.py
    echo "  ✓ 훅 제거됨"
fi

# Remove workflows (optional - ask user)
if [ -d "$UNINSTALL_LOCATION/workflows" ]; then
    read -p "워크플로우 파일도 제거할까요? (작업 상태가 삭제됩니다) (y/N): " remove_workflows
    if [[ "$remove_workflows" =~ ^[Yy]$ ]]; then
        rm -rf "$UNINSTALL_LOCATION/workflows"
        echo "  ✓ 워크플로우 제거됨"
    fi
fi

# Remove memory reference file
if [ -f "$UNINSTALL_LOCATION/SPARK_AGENTS_MEMORY_REFERENCE.md" ]; then
    rm -f "$UNINSTALL_LOCATION/SPARK_AGENTS_MEMORY_REFERENCE.md"
    echo "  ✓ 메모리 레퍼런스 파일 제거됨"
fi

# Remove SPARK global guide file
if [ -f "$UNINSTALL_LOCATION/SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" ]; then
    rm -f "$UNINSTALL_LOCATION/SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md"
    echo "  ✓ SPARK 글로벌 가이드 파일 제거됨"
fi

# 백업 디렉토리 확인
backup_dir="$UNINSTALL_LOCATION/.spark-backup"

# 백업에서 원본 CLAUDE.md 복원
claude_md_locations=(
    "$UNINSTALL_LOCATION/CLAUDE.md"
    "$HOME/.claude/CLAUDE.md"
)

claude_md_restored=false

if [ -f "$backup_dir/CLAUDE.md.original" ]; then
    for claude_md in "${claude_md_locations[@]}"; do
        if [ -f "$claude_md" ] && grep -q "@SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" "$claude_md"; then
            print_status "$claude_md에서 CLAUDE.md 원본 복원 중..."
            cp "$backup_dir/CLAUDE.md.original" "$claude_md"
            echo "  ✓ 백업에서 CLAUDE.md 원본 복원 완료"
            claude_md_restored=true
            break
        fi
    done
fi

if [ "$claude_md_restored" = false ]; then
    print_warning "백업 파일이 없거나 CLAUDE.md에 SPARK 레퍼런스가 없습니다"
    echo "  수동으로 SPARK 레퍼런스를 추가했다면 직접 제거하세요:"
    echo "  - @SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md"
fi

# 백업에서 원본 settings.json 복원
if [ -f "$backup_dir/settings.json.original" ]; then
    print_status "settings.json 원본 복원 중..."
    cp "$backup_dir/settings.json.original" "$UNINSTALL_LOCATION/settings.json"
    echo "  ✓ settings.json 원본 복원 완료"
fi

# 복원 후 백업 디렉토리 제거
if [ -d "$backup_dir" ]; then
    rm -rf "$backup_dir"
    echo "  ✓ 백업 디렉토리 제거됨: .spark-backup/"
fi

# settings.json 정리 (SPARK 훅만 포함된 경우 훅 섹션 제거)
if [ -f "$UNINSTALL_LOCATION/settings.json" ] && [ ! -f "$backup_dir/settings.json.original" ]; then
    read -p "settings.json에서 SPARK 훅 설정을 제거할까요? (y/N): " remove_hooks
    if [[ "$remove_hooks" =~ ^[Yy]$ ]]; then
        cp "$UNINSTALL_LOCATION/settings.json" "$UNINSTALL_LOCATION/settings.json.backup"
        print_warning "settings.json 백업됨 - 수동으로 훅 섹션을 확인하세요"
        echo "  백업 파일: settings.json.backup"
    fi
fi

echo ""
print_success "SPARK 제거 완료!"
echo ""
echo -e "${CYAN}제거 결과:${NC}"
echo "• SPARK 에이전트, 명령어, 훅이 제거되었습니다"
echo "• 백업 파일이 생성되었습니다 (.backup)"
echo ""
echo -e "${YELLOW}참고:${NC}"
echo "• Claude Code를 재시작하면 변경사항이 적용됩니다"
echo "• 문제가 있으면 백업 파일을 사용하여 복구할 수 있습니다"
echo ""
echo "SPARK를 사용해 주셔서 감사합니다! 👋"