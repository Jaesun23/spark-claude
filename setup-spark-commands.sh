#!/bin/bash

# SPARK 명령어 설정 스크립트
# 사용법: source setup-spark-commands.sh

SPARK_DIR="/Users/jason/Projects/spark-claude"

echo "🚀 SPARK 명령어 설정 중..."

# 셸 종류 확인
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "⚠️ 지원되지 않는 셸입니다. 수동으로 설정해주세요."
    exit 1
fi

echo "📝 $SHELL_NAME 셸 감지됨"

# 이미 설정되어 있는지 확인
if grep -q "SPARK Commands" "$SHELL_RC" 2>/dev/null; then
    echo "✅ SPARK 명령어가 이미 설정되어 있습니다."
else
    # 설정 추가
    cat >> "$SHELL_RC" << 'EOL'

# SPARK Commands
alias spark-convert="python3 /Users/jason/Projects/spark-claude/spark-convert-agents"
alias spark-agents-to-txt="python3 /Users/jason/Projects/spark-claude/spark-convert-agents"
alias spark-agents="ls -la /Users/jason/Projects/spark-claude/.claude/agents/"

# SPARK 도움말
spark-help() {
    echo "🚀 SPARK 명령어 목록:"
    echo "  spark-convert         - MD 파일을 TXT로 변환"
    echo "  spark-agents-to-txt   - MD 파일을 TXT로 변환 (동일)"
    echo "  spark-agents          - 에이전트 목록 보기"
    echo "  spark-help            - 이 도움말 보기"
    echo ""
    echo "📚 spark-convert 옵션:"
    echo "  spark-convert                    # 기본 변환"
    echo "  spark-convert --no-combine       # 개별 파일만"
    echo "  spark-convert -o ~/Desktop       # 출력 위치 지정"
    echo "  spark-convert -q                 # 조용한 모드"
}

EOL
    echo "✅ $SHELL_RC에 SPARK 명령어가 추가되었습니다."
fi

# 현재 세션에도 적용
alias spark-convert="python3 $SPARK_DIR/spark-convert-agents"
alias spark-agents-to-txt="python3 $SPARK_DIR/spark-convert-agents"
alias spark-agents="ls -la $SPARK_DIR/.claude/agents/"

spark-help() {
    echo "🚀 SPARK 명령어 목록:"
    echo "  spark-convert         - MD 파일을 TXT로 변환"
    echo "  spark-agents-to-txt   - MD 파일을 TXT로 변환 (동일)"
    echo "  spark-agents          - 에이전트 목록 보기"
    echo "  spark-help            - 이 도움말 보기"
    echo ""
    echo "📚 spark-convert 옵션:"
    echo "  spark-convert                    # 기본 변환"
    echo "  spark-convert --no-combine       # 개별 파일만"
    echo "  spark-convert -o ~/Desktop       # 출력 위치 지정"
    echo "  spark-convert -q                 # 조용한 모드"
}

echo ""
echo "🎉 SPARK 명령어 설정 완료!"
echo ""
echo "사용 가능한 명령어:"
echo "  • spark-convert       - MD → TXT 변환"
echo "  • spark-agents        - 에이전트 목록"
echo "  • spark-help          - 도움말"
echo ""
echo "💡 새 터미널을 열거나 'source $SHELL_RC'를 실행하면 영구적으로 사용할 수 있습니다."