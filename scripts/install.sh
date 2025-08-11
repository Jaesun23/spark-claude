#!/bin/bash

# SPARK Universal AI Agent System Installer v3.0
# Interactive installer with multi-agent pipeline support
# Features: Component selection, namespace configuration, hook management

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
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

print_option() {
    echo -e "${CYAN}$1${NC}"
}

# Banner
clear
echo -e "${MAGENTA}"
echo "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
echo "     SPARK Universal AI Agent System Installer v3.0"
echo "     88.4% Token Efficiency • 16 Specialized Agents"
echo "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -d ".claude" ]; then
    print_error "This script must be run from the SPARK project root directory"
    print_error "Make sure you're in the directory containing the .claude folder"
    exit 1
fi

# Installation variables
INSTALL_LOCATION=""
INSTALL_AGENTS=false
INSTALL_COMMANDS=false
INSTALL_HOOKS=false
INSTALL_WORKFLOWS=false
INSTALL_MULTI_AGENT=false
USE_NAMESPACE=false
NAMESPACE_PREFIX=""

# Function to check for conflicts
check_conflicts() {
    local target_dir="$1"
    local conflicts=()
    
    if [ -d "$target_dir/agents" ] && [ -d ".claude/agents" ]; then
        for agent in .claude/agents/*.md; do
            agent_name=$(basename "$agent")
            if [ -f "$target_dir/agents/$agent_name" ]; then
                conflicts+=("Agent: $agent_name")
            fi
        done
    fi
    
    if [ -d "$target_dir/commands" ] && [ -d ".claude/commands" ]; then
        for cmd in .claude/commands/*.json; do
            cmd_name=$(basename "$cmd")
            if [ -f "$target_dir/commands/$cmd_name" ]; then
                conflicts+=("Command: $cmd_name")
            fi
        done
    fi
    
    if [ ${#conflicts[@]} -gt 0 ]; then
        print_warning "Detected potential conflicts:"
        for conflict in "${conflicts[@]}"; do
            echo "  - $conflict"
        done
        return 1
    fi
    return 0
}

# Function to select installation location
select_location() {
    echo -e "${GREEN}=== 설치 위치 선택 ===${NC}"
    echo ""
    print_option "1) 전역 설치 (~/.claude/)"
    echo "   모든 프로젝트에서 SPARK 사용 가능"
    echo ""
    print_option "2) 프로젝트별 설치 (프로젝트/.claude/)"
    echo "   특정 프로젝트에서만 사용"
    echo ""
    print_option "3) 현재 프로젝트 설치 (./.claude/)"
    echo "   현재 디렉토리에 덮어쓰기"
    echo ""
    
    read -p "선택 [1-3]: " location_choice
    
    case $location_choice in
        1)
            INSTALL_LOCATION="$HOME/.claude"
            print_status "전역 설치 선택: $INSTALL_LOCATION"
            
            if [ -d "$INSTALL_LOCATION" ]; then
                print_warning "기존 전역 설치 발견됨"
                if ! check_conflicts "$INSTALL_LOCATION"; then
                    read -p "충돌을 무시하고 계속할까요? (y/N): " ignore_conflicts
                    if [[ ! "$ignore_conflicts" =~ ^[Yy]$ ]]; then
                        print_error "설치 취소됨"
                        exit 1
                    fi
                    USE_NAMESPACE=true
                fi
            fi
            ;;
        2)
            read -p "프로젝트 디렉토리 경로 입력: " project_dir
            if [ ! -d "$project_dir" ]; then
                print_error "디렉토리가 존재하지 않음: $project_dir"
                exit 1
            fi
            INSTALL_LOCATION="$project_dir/.claude"
            print_status "프로젝트 설치 선택: $INSTALL_LOCATION"
            ;;
        3)
            INSTALL_LOCATION="./.claude"
            print_status "현재 프로젝트 덮어쓰기 선택"
            ;;
        *)
            print_error "잘못된 선택"
            exit 1
            ;;
    esac
}

# Function to select components
select_components() {
    echo ""
    echo -e "${GREEN}=== 설치 구성요소 선택 ===${NC}"
    echo ""
    
    print_option "설치할 구성요소를 선택하세요:"
    echo ""
    
    # Agents
    read -p "1) SPARK 에이전트 (16개) 설치? (Y/n): " install_agents
    if [[ ! "$install_agents" =~ ^[Nn]$ ]]; then
        INSTALL_AGENTS=true
        print_success "✓ 에이전트 설치 예정"
    fi
    
    # Commands
    read -p "2) 단일 에이전트 명령어 설치? (Y/n): " install_commands
    if [[ ! "$install_commands" =~ ^[Nn]$ ]]; then
        INSTALL_COMMANDS=true
        print_success "✓ 명령어 설치 예정"
        
        if [ "$USE_NAMESPACE" = true ]; then
            read -p "   네임스페이스 사용? (예: /spark:implement) (Y/n): " use_ns
            if [[ ! "$use_ns" =~ ^[Nn]$ ]]; then
                read -p "   네임스페이스 접두어 입력 (기본: spark): " ns_prefix
                NAMESPACE_PREFIX="${ns_prefix:-spark}"
                print_status "   네임스페이스: /$NAMESPACE_PREFIX:*"
            fi
        fi
    fi
    
    # Multi-agent pipelines
    read -p "3) 다중 에이전트 파이프라인 설치? (훅 필요) (Y/n): " install_multi
    if [[ ! "$install_multi" =~ ^[Nn]$ ]]; then
        INSTALL_MULTI_AGENT=true
        INSTALL_HOOKS=true
        INSTALL_WORKFLOWS=true
        print_success "✓ 다중 에이전트 파이프라인 설치 예정"
        print_success "✓ 훅 및 워크플로우 자동 포함"
    else
        # Hooks (only if not installing multi-agent)
        read -p "4) 훅 스크립트 설치? (y/N): " install_hooks
        if [[ "$install_hooks" =~ ^[Yy]$ ]]; then
            INSTALL_HOOKS=true
            print_success "✓ 훅 설치 예정"
        fi
        
        # Workflows
        read -p "5) 워크플로우 설정 설치? (y/N): " install_workflows
        if [[ "$install_workflows" =~ ^[Yy]$ ]]; then
            INSTALL_WORKFLOWS=true
            print_success "✓ 워크플로우 설치 예정"
        fi
    fi
}

# Function to install agents
install_agents() {
    print_status "에이전트 설치 중..."
    mkdir -p "$INSTALL_LOCATION/agents"
    
    for agent in .claude/agents/*.md; do
        agent_name=$(basename "$agent")
        cp "$agent" "$INSTALL_LOCATION/agents/"
        echo "  ✓ $agent_name"
    done
    
    print_success "16개 에이전트 설치 완료"
}

# Function to install commands
install_commands() {
    print_status "명령어 설치 중..."
    mkdir -p "$INSTALL_LOCATION/commands"
    
    # Single-agent commands
    local single_agent_commands=(
        "spark-implement.json"
        "spark-analyze.json"
        "spark-test.json"
        "spark-design.json"
        "spark-troubleshoot.json"
        "spark-improve.json"
        "spark-explain.json"
        "spark-estimate.json"
        "spark-document.json"
        "spark-git.json"
        "spark-build.json"
        "spark-spawn.json"
        "spark-index.json"
        "spark-task.json"
        "spark-clean.json"
        "spark-loader.json"
    )
    
    for cmd_file in "${single_agent_commands[@]}"; do
        if [ -f ".claude/commands/$cmd_file" ]; then
            if [ -n "$NAMESPACE_PREFIX" ]; then
                # Apply namespace to command
                local new_name="${NAMESPACE_PREFIX}-${cmd_file#spark-}"
                cp ".claude/commands/$cmd_file" "$INSTALL_LOCATION/commands/$new_name"
                echo "  ✓ /$NAMESPACE_PREFIX:${cmd_file#spark-*.json} (namespaced)"
            else
                cp ".claude/commands/$cmd_file" "$INSTALL_LOCATION/commands/"
                echo "  ✓ /${cmd_file%.json}"
            fi
        fi
    done
    
    print_success "단일 에이전트 명령어 설치 완료"
}

# Function to install multi-agent pipelines
install_multi_agent() {
    print_status "다중 에이전트 파이프라인 설치 중..."
    
    # Multi-agent pipeline commands
    local multi_agent_commands=(
        "spark-launch.json"    # 5 agents
        "spark-refactor.json"  # 4 agents
        "spark-audit.json"     # 4 agents
        "spark-migrate.json"   # 5 agents
        "spark-optimize.json"  # 5 agents
    )
    
    for cmd_file in "${multi_agent_commands[@]}"; do
        if [ -f ".claude/commands/$cmd_file" ]; then
            cp ".claude/commands/$cmd_file" "$INSTALL_LOCATION/commands/"
            echo "  ✓ /${cmd_file%.json} (pipeline)"
        fi
    done
    
    print_success "다중 에이전트 파이프라인 설치 완료"
}

# Function to install hooks
install_hooks() {
    print_status "훅 스크립트 설치 중..."
    mkdir -p "$INSTALL_LOCATION/hooks"
    
    # Copy all Python hook scripts
    for hook in .claude/hooks/*.py; do
        if [ -f "$hook" ]; then
            hook_name=$(basename "$hook")
            cp "$hook" "$INSTALL_LOCATION/hooks/"
            chmod +x "$INSTALL_LOCATION/hooks/$hook_name"
            echo "  ✓ $hook_name"
        fi
    done
    
    print_success "훅 스크립트 설치 완료"
}

# Function to install workflows
install_workflows() {
    print_status "워크플로우 설정 설치 중..."
    mkdir -p "$INSTALL_LOCATION/workflows"
    
    # Copy workflow JSON files if they exist
    if [ -d ".claude/workflows" ]; then
        for workflow in .claude/workflows/*.json; do
            if [ -f "$workflow" ]; then
                workflow_name=$(basename "$workflow")
                cp "$workflow" "$INSTALL_LOCATION/workflows/"
                echo "  ✓ $workflow_name"
            fi
        done
    fi
    
    # Create empty JSON files for state management
    if [ ! -f "$INSTALL_LOCATION/workflows/current_task.json" ]; then
        echo '{}' > "$INSTALL_LOCATION/workflows/current_task.json"
        echo "  ✓ current_task.json (초기화)"
    fi
    
    if [ ! -f "$INSTALL_LOCATION/workflows/unified_context.json" ]; then
        echo '{}' > "$INSTALL_LOCATION/workflows/unified_context.json"
        echo "  ✓ unified_context.json (초기화)"
    fi
    
    print_success "워크플로우 설정 설치 완료"
}

# Function to install memory reference and update CLAUDE.md
install_memory_reference() {
    print_status "메모리 레퍼런스 설치 및 CLAUDE.md 업데이트 중..."
    
    # Copy SPARK_AGENTS_MEMORY_REFERENCE.md to installation location
    if [ -f "docs/SPARK_AGENTS_MEMORY_REFERENCE.md" ]; then
        cp "docs/SPARK_AGENTS_MEMORY_REFERENCE.md" "$INSTALL_LOCATION/"
        echo "  ✓ SPARK_AGENTS_MEMORY_REFERENCE.md 복사됨"
    else
        print_warning "SPARK_AGENTS_MEMORY_REFERENCE.md 파일을 찾을 수 없음"
        return
    fi
    
    # Update CLAUDE.md if it exists
    local claude_md="$INSTALL_LOCATION/CLAUDE.md"
    
    # Check if CLAUDE.md exists in target location
    if [ ! -f "$claude_md" ]; then
        # If global installation, check home directory
        if [[ "$INSTALL_LOCATION" == "$HOME/.claude" ]]; then
            claude_md="$HOME/.claude/CLAUDE.md"
        fi
    fi
    
    if [ -f "$claude_md" ]; then
        # Check if reference already exists
        if grep -q "@SPARK_AGENTS_MEMORY_REFERENCE.md" "$claude_md"; then
            print_warning "CLAUDE.md에 이미 SPARK 레퍼런스가 있음"
        else
            # Add SPARK reference to the end of CLAUDE.md
            cat >> "$claude_md" << 'EOF'

---

## 🚀 SPARK Agents Reference
<!-- SPARK-REFERENCE-START - Remove this section when uninstalling SPARK -->
@SPARK_AGENTS_MEMORY_REFERENCE.md

**⚠️ SPARK 제거 시 주의사항:**
1. 이 섹션 전체를 삭제하세요 (SPARK-REFERENCE-START부터 SPARK-REFERENCE-END까지)
2. `SPARK_AGENTS_MEMORY_REFERENCE.md` 파일도 삭제하세요
3. 삭제 명령어: 
   ```bash
   # CLAUDE.md에서 SPARK 섹션 제거 (수동 편집 필요)
   # 레퍼런스 파일 삭제
   rm ~/.claude/SPARK_AGENTS_MEMORY_REFERENCE.md
   ```
<!-- SPARK-REFERENCE-END -->
EOF
            print_success "CLAUDE.md에 SPARK 레퍼런스 추가됨"
        fi
    else
        print_warning "CLAUDE.md 파일을 찾을 수 없음 - 수동으로 추가 필요"
        echo "  다음 내용을 CLAUDE.md 파일 끝에 추가하세요:"
        echo "  @SPARK_AGENTS_MEMORY_REFERENCE.md"
    fi
    
    print_success "메모리 레퍼런스 설치 완료"
}

# Function to configure settings.json
configure_settings() {
    print_status "settings.json 구성 중..."
    
    local settings_file="$INSTALL_LOCATION/settings.json"
    local backup_file="$INSTALL_LOCATION/settings.json.backup"
    
    # Backup existing settings
    if [ -f "$settings_file" ]; then
        cp "$settings_file" "$backup_file"
        print_warning "기존 설정 백업: $backup_file"
    fi
    
    # Create new settings based on installation choices
    if [ "$INSTALL_MULTI_AGENT" = true ] || [ "$INSTALL_HOOKS" = true ]; then
        # Determine hook path based on installation location
        if [[ "$INSTALL_LOCATION" == "$HOME/.claude" ]]; then
            HOOK_PATH="$HOME/.claude/hooks"
        else
            HOOK_PATH="\$CLAUDE_PROJECT_DIR/.claude/hooks"
        fi
        
        cat > "$settings_file" << EOF
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "$HOOK_PATH/spark_persona_router.py",
        "description": "SPARK 페르소나 라우터 - 작업 분석 및 최적 에이전트 선택"
      }
    ],
    "SubagentStop": [
      {
        "command": "$HOOK_PATH/spark_quality_gates.py",
        "description": "SPARK 품질 게이트 - Jason의 8단계 엄격 검증"
      }
    ]
  },
  "commandTimeout": 120000,
  "enableHooks": true,
  "sparkConfig": {
    "version": "3.0",
    "tokenEfficiency": 0.884,
    "qualityGates": {
      "strictMode": true,
      "maxRetries": 3,
      "targets": {
        "unitTest": 95,
        "integrationTest": 85,
        "overallCoverage": 90
      }
    }
  }
}
EOF
        print_success "훅이 포함된 settings.json 생성됨"
    else
        # Minimal settings without hooks
        cat > "$settings_file" << 'EOF'
{
  "commandTimeout": 120000,
  "sparkConfig": {
    "version": "3.0",
    "tokenEfficiency": 0.884
  }
}
EOF
        print_success "기본 settings.json 생성됨"
    fi
}

# Function to show installation summary
show_summary() {
    echo ""
    echo -e "${GREEN}⚡⚡⚡ 설치 완료! ⚡⚡⚡${NC}"
    echo ""
    echo -e "${CYAN}설치된 구성요소:${NC}"
    
    [ "$INSTALL_AGENTS" = true ] && echo "  ✓ 16개 SPARK 에이전트"
    [ "$INSTALL_COMMANDS" = true ] && echo "  ✓ 단일 에이전트 명령어"
    [ "$INSTALL_MULTI_AGENT" = true ] && echo "  ✓ 다중 에이전트 파이프라인"
    [ "$INSTALL_HOOKS" = true ] && echo "  ✓ 훅 스크립트"
    [ "$INSTALL_WORKFLOWS" = true ] && echo "  ✓ 워크플로우 설정"
    
    echo ""
    echo -e "${CYAN}설치 위치:${NC} $INSTALL_LOCATION"
    
    if [ -n "$NAMESPACE_PREFIX" ]; then
        echo -e "${CYAN}네임스페이스:${NC} /$NAMESPACE_PREFIX:*"
    fi
    
    echo ""
    echo -e "${GREEN}다음 단계:${NC}"
    echo "1. Claude Code 재시작하여 새 설정 로드"
    
    if [ "$INSTALL_COMMANDS" = true ]; then
        echo "2. SPARK 명령어 사용해보기:"
        if [ -n "$NAMESPACE_PREFIX" ]; then
            echo "   ${BLUE}/$NAMESPACE_PREFIX:implement \"user authentication\"${NC}"
            echo "   ${BLUE}/$NAMESPACE_PREFIX:test \"create unit tests\"${NC}"
        else
            echo "   ${BLUE}/spark-implement \"user authentication\"${NC}"
            echo "   ${BLUE}/spark-test \"create unit tests\"${NC}"
        fi
    fi
    
    if [ "$INSTALL_MULTI_AGENT" = true ]; then
        echo "3. 다중 에이전트 파이프라인 사용:"
        echo "   ${BLUE}/spark-launch \"new feature\"${NC} - 전체 개발 파이프라인"
        echo "   ${BLUE}/spark-optimize \"improve performance\"${NC} - 성능 최적화"
        echo "   ${BLUE}/spark-audit \"security check\"${NC} - 보안 감사"
    fi
    
    echo ""
    echo -e "${CYAN}주요 기능:${NC}"
    echo "• 88.4% 토큰 효율성 (검증됨)"
    echo "• 16개 전문 에이전트"
    echo "• Jason의 8단계 엄격 품질 게이트"
    echo "• 자동 페르소나 활성화"
    echo "• Task 동시 호출 패턴"
    echo "• Fallback 경로 지원 (전역/프로젝트 자동 감지)"
    
    if [ "$INSTALL_AGENTS" = true ]; then
        echo "• 메모리 레퍼런스 자동 설치 (CLAUDE.md 업데이트)"
    fi
    
    if [[ "$INSTALL_LOCATION" == "$HOME/.claude" ]]; then
        echo ""
        echo -e "${YELLOW}참고:${NC}"
        echo "• 전역 설치된 에이전트는 모든 프로젝트에서 사용 가능"
        echo "• 워크플로우 파일은 ~/.claude/workflows/에 저장됨"
        echo "• 프로젝트별 설정이 필요한 경우 .claude/ 디렉토리 생성"
        echo "• CLAUDE.md에 @SPARK_AGENTS_MEMORY_REFERENCE.md 추가됨"
    fi
    
    echo ""
    echo -e "${BLUE}문서:${NC} https://github.com/Jaesun23/spark-claude"
    echo -e "${BLUE}가이드:${NC} /Users/jason/Projects/spark-claude/docs/SPARK_COMPLETE_GUIDE.md"
    echo ""
    print_success "Happy coding with SPARK! ⚡"
}

# Main installation flow
main() {
    # Step 1: Select installation location
    select_location
    
    # Step 2: Select components
    select_components
    
    # Step 3: Confirm installation
    echo ""
    echo -e "${YELLOW}=== 설치 확인 ===${NC}"
    echo "위치: $INSTALL_LOCATION"
    echo "구성요소:"
    [ "$INSTALL_AGENTS" = true ] && echo "  • 에이전트"
    [ "$INSTALL_COMMANDS" = true ] && echo "  • 명령어"
    [ "$INSTALL_MULTI_AGENT" = true ] && echo "  • 다중 에이전트 파이프라인"
    [ "$INSTALL_HOOKS" = true ] && echo "  • 훅"
    [ "$INSTALL_WORKFLOWS" = true ] && echo "  • 워크플로우"
    echo ""
    
    read -p "설치를 진행할까요? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_warning "설치 취소됨"
        exit 0
    fi
    
    # Step 4: Create directories
    print_status "디렉토리 생성 중..."
    mkdir -p "$INSTALL_LOCATION"
    
    # Step 5: Install components
    [ "$INSTALL_AGENTS" = true ] && install_agents
    [ "$INSTALL_COMMANDS" = true ] && install_commands
    [ "$INSTALL_MULTI_AGENT" = true ] && install_multi_agent
    [ "$INSTALL_HOOKS" = true ] && install_hooks
    [ "$INSTALL_WORKFLOWS" = true ] && install_workflows
    
    # Step 6: Configure settings
    configure_settings
    
    # Step 7: Install memory reference (always install if agents are installed)
    [ "$INSTALL_AGENTS" = true ] && install_memory_reference
    
    # Step 8: Show summary
    show_summary
}

# Run main function
main