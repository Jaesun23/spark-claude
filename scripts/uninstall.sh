#!/bin/bash

# SPARK Universal AI Agent System Uninstaller
# Removes SPARK from your Claude Code environment

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
echo "⚠️  SPARK Uninstaller  ⚠️"
echo -e "${NC}"
echo "This script will remove SPARK components."
echo ""

# Select location to uninstall from
echo -e "${CYAN}=== Select Location to Uninstall ===${NC}"
echo ""
echo "1) Remove global installation (~/.claude/)"
echo "2) Remove project-specific installation"
echo "3) Cancel"
echo ""

read -p "Choice [1-3]: " choice

case $choice in
    1)
        UNINSTALL_LOCATION="$HOME/.claude"
        print_status "Global installation removal selected: $UNINSTALL_LOCATION"
        ;;
    2)
        read -p "Enter project directory path: " project_dir
        if [ ! -d "$project_dir" ]; then
            print_error "Directory does not exist: $project_dir"
            exit 1
        fi
        UNINSTALL_LOCATION="$project_dir/.claude"
        print_status "Project installation removal selected: $UNINSTALL_LOCATION"
        ;;
    3)
        print_warning "Uninstallation cancelled"
        exit 0
        ;;
    *)
        print_error "Invalid selection"
        exit 1
        ;;
esac

# Check if SPARK is installed
if [ ! -d "$UNINSTALL_LOCATION" ]; then
    print_error "Installed SPARK not found: $UNINSTALL_LOCATION"
    exit 1
fi

echo ""
echo -e "${YELLOW}=== Components to Remove ===${NC}"
echo ""

# List what will be removed
echo "The following items will be removed:"
[ -d "$UNINSTALL_LOCATION/agents" ] && echo "  • SPARK agents (*.md files)"
[ -d "$UNINSTALL_LOCATION/commands" ] && echo "  • SPARK commands (spark-*.json)"
[ -d "$UNINSTALL_LOCATION/hooks" ] && echo "  • SPARK hooks (spark_*.py)"
[ -d "$UNINSTALL_LOCATION/workflows" ] && echo "  • SPARK workflow settings"
[ -f "$UNINSTALL_LOCATION/SPARK_AGENTS_MEMORY_REFERENCE.md" ] && echo "  • Memory reference file"
[ -f "$UNINSTALL_LOCATION/SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" ] && echo "  • SPARK global guide file"
[ -f "$UNINSTALL_LOCATION/CLAUDE.md" ] && echo "  • SPARK section in CLAUDE.md"
[ -f "$HOME/.claude/CLAUDE.md" ] && echo "  • SPARK references in ~/.claude/CLAUDE.md"

echo ""
read -p "Are you sure you want to remove them? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    print_warning "Uninstallation cancelled"
    exit 0
fi

# Remove SPARK components
print_status "Removing SPARK components..."

# Remove agents
if [ -d "$UNINSTALL_LOCATION/agents" ]; then
    rm -f "$UNINSTALL_LOCATION/agents"/*-spark.md
    echo "  ✓ Agents removed"
fi

# Remove commands
if [ -d "$UNINSTALL_LOCATION/commands" ]; then
    rm -f "$UNINSTALL_LOCATION/commands"/spark-*.json
    echo "  ✓ Commands removed"
fi

# Remove hooks
if [ -d "$UNINSTALL_LOCATION/hooks" ]; then
    rm -f "$UNINSTALL_LOCATION/hooks"/spark_*.py
    echo "  ✓ Hooks removed"
fi

# Remove workflows (optional - ask user)
if [ -d "$UNINSTALL_LOCATION/workflows" ]; then
    read -p "Remove workflow files as well? (work state will be deleted) (y/N): " remove_workflows
    if [[ "$remove_workflows" =~ ^[Yy]$ ]]; then
        rm -rf "$UNINSTALL_LOCATION/workflows"
        echo "  ✓ Workflows removed"
    fi
fi

# Remove memory reference file
if [ -f "$UNINSTALL_LOCATION/SPARK_AGENTS_MEMORY_REFERENCE.md" ]; then
    rm -f "$UNINSTALL_LOCATION/SPARK_AGENTS_MEMORY_REFERENCE.md"
    echo "  ✓ Memory reference file removed"
fi

# Remove SPARK global guide file
if [ -f "$UNINSTALL_LOCATION/SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" ]; then
    rm -f "$UNINSTALL_LOCATION/SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md"
    echo "  ✓ SPARK global guide file removed"
fi

# Check for backup directory
backup_dir="$UNINSTALL_LOCATION/.spark-backup"

# Restore original CLAUDE.md from backup
claude_md_locations=(
    "$UNINSTALL_LOCATION/CLAUDE.md"
    "$HOME/.claude/CLAUDE.md"
)

claude_md_restored=false

if [ -f "$backup_dir/CLAUDE.md.original" ]; then
    for claude_md in "${claude_md_locations[@]}"; do
        if [ -f "$claude_md" ] && grep -q "@SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" "$claude_md"; then
            print_status "Restoring original CLAUDE.md at $claude_md..."
            cp "$backup_dir/CLAUDE.md.original" "$claude_md"
            echo "  ✓ Original CLAUDE.md restored from backup"
            claude_md_restored=true
            break
        fi
    done
fi

if [ "$claude_md_restored" = false ]; then
    print_warning "No backup file found or CLAUDE.md doesn't contain SPARK references"
    echo "  If you manually added SPARK references, please remove them manually:"
    echo "  - @SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md"
fi

# Restore original settings.json from backup
if [ -f "$backup_dir/settings.json.original" ]; then
    print_status "Restoring original settings.json..."
    cp "$backup_dir/settings.json.original" "$UNINSTALL_LOCATION/settings.json"
    echo "  ✓ Original settings.json restored"
fi

# Remove backup directory after restoration
if [ -d "$backup_dir" ]; then
    rm -rf "$backup_dir"
    echo "  ✓ Backup directory removed: .spark-backup/"
fi

# Clean up settings.json (remove hooks section if it only contains SPARK hooks)
if [ -f "$UNINSTALL_LOCATION/settings.json" ] && [ ! -f "$backup_dir/settings.json.original" ]; then
    read -p "Remove SPARK hook settings from settings.json? (y/N): " remove_hooks
    if [[ "$remove_hooks" =~ ^[Yy]$ ]]; then
        cp "$UNINSTALL_LOCATION/settings.json" "$UNINSTALL_LOCATION/settings.json.backup"
        print_warning "settings.json backed up - manually check hooks section"
        echo "  Backup file: settings.json.backup"
    fi
fi

echo ""
print_success "SPARK removal completed!"
echo ""
echo -e "${CYAN}Removal Results:${NC}"
echo "• SPARK agents, commands, and hooks have been removed"
echo "• Backup files have been created (.backup)"
echo ""
echo -e "${YELLOW}Note:${NC}"
echo "• Restart Claude Code to apply changes"
echo "• If there are issues, you can restore using backup files"
echo ""
echo "Thank you for using SPARK! 👋"