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
echo "              16 Specialized Agents"
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
    echo -e "${GREEN}=== Installation Location Selection ===${NC}"
    echo ""
    print_option "1) Global Installation (~/.claude/)"
    echo "   Available for all projects"
    echo ""
    print_option "2) Project-specific Installation (project/.claude/)"
    echo "   Available for specific project only"
    echo ""
    print_option "3) Current Project Installation (./.claude/)"
    echo "   Overwrite current directory"
    echo ""
    
    read -p "Choice [1-3]: " location_choice
    
    case $location_choice in
        1)
            INSTALL_LOCATION="$HOME/.claude"
            print_status "Global installation selected: $INSTALL_LOCATION"
            
            if [ -d "$INSTALL_LOCATION" ]; then
                print_warning "Existing global installation detected"
                if ! check_conflicts "$INSTALL_LOCATION"; then
                    read -p "Ignore conflicts and continue? (y/N): " ignore_conflicts
                    if [[ ! "$ignore_conflicts" =~ ^[Yy]$ ]]; then
                        print_error "Installation cancelled"
                        exit 1
                    fi
                    USE_NAMESPACE=true
                fi
            fi
            ;;
        2)
            read -p "Enter project directory path: " project_dir
            if [ ! -d "$project_dir" ]; then
                print_error "Directory does not exist: $project_dir"
                exit 1
            fi
            INSTALL_LOCATION="$project_dir/.claude"
            print_status "Project installation selected: $INSTALL_LOCATION"
            ;;
        3)
            INSTALL_LOCATION="./.claude"
            print_status "Current project overwrite selected"
            ;;
        *)
            print_error "Invalid selection"
            exit 1
            ;;
    esac
}

# Function to select components
select_components() {
    echo ""
    echo -e "${GREEN}=== Installation Components Selection ===${NC}"
    echo ""
    
    print_option "Select components to install:"
    echo ""
    
    # Agents
    read -p "1) Install SPARK agents (16 agents)? (Y/n): " install_agents
    if [[ ! "$install_agents" =~ ^[Nn]$ ]]; then
        INSTALL_AGENTS=true
        print_success "✓ Agents scheduled for installation"
    fi
    
    # Commands
    read -p "2) Install single agent commands? (Y/n): " install_commands
    if [[ ! "$install_commands" =~ ^[Nn]$ ]]; then
        INSTALL_COMMANDS=true
        print_success "✓ Commands scheduled for installation"
        
        if [ "$USE_NAMESPACE" = true ]; then
            read -p "   Use namespace? (e.g., /spark:implement) (Y/n): " use_ns
            if [[ ! "$use_ns" =~ ^[Nn]$ ]]; then
                read -p "   Enter namespace prefix (default: spark): " ns_prefix
                NAMESPACE_PREFIX="${ns_prefix:-spark}"
                print_status "   Namespace: /$NAMESPACE_PREFIX:*"
            fi
        fi
    fi
    
    # Multi-agent pipelines
    read -p "3) Install multi-agent pipelines? (requires hooks) (Y/n): " install_multi
    if [[ ! "$install_multi" =~ ^[Nn]$ ]]; then
        INSTALL_MULTI_AGENT=true
        INSTALL_HOOKS=true
        INSTALL_WORKFLOWS=true
        print_success "✓ Multi-agent pipelines scheduled for installation"
        print_success "✓ Hook scripts automatically included (required for pipelines)"
        print_success "✓ Workflow configurations automatically included"
    else
        # Hooks (only if not installing multi-agent)
        read -p "4) Install hook scripts? (y/N): " install_hooks
        if [[ "$install_hooks" =~ ^[Yy]$ ]]; then
            INSTALL_HOOKS=true
            print_success "✓ Hooks scheduled for installation"
        fi
        
        # Workflows
        read -p "5) Install workflow settings? (y/N): " install_workflows
        if [[ "$install_workflows" =~ ^[Yy]$ ]]; then
            INSTALL_WORKFLOWS=true
            print_success "✓ Workflows scheduled for installation"
        fi
    fi
}

# Function to install agents
install_agents() {
    print_status "Installing agents..."
    mkdir -p "$INSTALL_LOCATION/agents"
    
    for agent in .claude/agents/*.md; do
        agent_name=$(basename "$agent")
        cp "$agent" "$INSTALL_LOCATION/agents/"
        echo "  ✓ $agent_name"
    done
    
    print_success "16 agents installation completed"
}

# Function to install commands
install_commands() {
    print_status "Installing commands..."
    mkdir -p "$INSTALL_LOCATION/commands"
    
    # Single-agent commands (only existing files)
    local single_agent_commands=(
        "spark-implement.md"
        "spark-analyze.md"
        "spark-test.md"
        "spark-design.md"
        "spark-fix.md"
        "spark-clean.md"
        "multi-implement.md"  # 4-team parallel implementation
    )
    
    for cmd_file in "${single_agent_commands[@]}"; do
        if [ -f ".claude/commands/$cmd_file" ]; then
            if [ -n "$NAMESPACE_PREFIX" ]; then
                # Apply namespace to command
                local new_name="${NAMESPACE_PREFIX}-${cmd_file#spark-}"
                cp ".claude/commands/$cmd_file" "$INSTALL_LOCATION/commands/$new_name"
                echo "  ✓ /$NAMESPACE_PREFIX:${cmd_file#spark-*.md} (namespaced)"
            else
                cp ".claude/commands/$cmd_file" "$INSTALL_LOCATION/commands/"
                echo "  ✓ /${cmd_file%.md}"
            fi
        fi
    done
    
    # Copy multi_implement.py utility if it exists
    if [ -f ".claude/commands/multi_implement.py" ]; then
        cp ".claude/commands/multi_implement.py" "$INSTALL_LOCATION/commands/"
        chmod +x "$INSTALL_LOCATION/commands/multi_implement.py"
        echo "  ✓ multi_implement.py (utility script)"
    fi
    
    print_success "Single agent commands installation completed"
}

# Function to install multi-agent pipelines
install_multi_agent() {
    print_status "Installing multi-agent pipelines..."
    
    # Multi-agent pipeline commands
    local multi_agent_commands=(
        "spark-launch.md"    # 5 agents
        "spark-refactor.md"  # 4 agents
        "spark-audit.md"     # 4 agents
        "spark-migrate.md"   # 5 agents
        "spark-optimize.md"  # 5 agents
    )
    
    for cmd_file in "${multi_agent_commands[@]}"; do
        if [ -f ".claude/commands/$cmd_file" ]; then
            cp ".claude/commands/$cmd_file" "$INSTALL_LOCATION/commands/"
            echo "  ✓ /${cmd_file%.md} (pipeline)"
        fi
    done
    
    print_success "Multi-agent pipelines installation completed"
}

# Function to install hooks
install_hooks() {
    print_status "Installing hook scripts..."
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
    
    print_success "Hook scripts installation completed"
}

# Function to install workflows
install_workflows() {
    print_status "Installing workflow templates..."
    
    if [[ "$INSTALL_LOCATION" == "$HOME/.claude" ]]; then
        # Global installation: Only install templates, not state files
        # JSON state files will be created per-project by hooks automatically
        print_status "Global installation detected - JSON state files will be created per-project"
        echo "  ✓ Workflow templates ready (per-project state management)"
    else
        # Project-specific installation: Create workflows directory and templates
        mkdir -p "$INSTALL_LOCATION/workflows"
        
        # Copy workflow template files if they exist
        if [ -d ".claude/workflows" ]; then
            for workflow in .claude/workflows/*.json; do
                if [ -f "$workflow" ]; then
                    workflow_name=$(basename "$workflow")
                    # Only copy template files, not state files
                    if [[ ! "$workflow_name" =~ ^(current_task|team[0-9]+_current_task)\.json$ ]]; then
                        cp "$workflow" "$INSTALL_LOCATION/workflows/"
                        echo "  ✓ $workflow_name (template)"
                    fi
                fi
            done
        fi
        
        echo "  ✓ Project-specific workflows directory created"
        echo "  ✓ JSON state files will be auto-created when needed"
    fi
    
    print_success "Workflow template installation completed"
}

# Function to install SPARK global guide and update CLAUDE.md
install_memory_reference() {
    print_status "Installing SPARK global guide and updating CLAUDE.md..."
    
    # Create backup directory if it doesn't exist
    local backup_dir="$INSTALL_LOCATION/.spark-backup"
    if [ ! -d "$backup_dir" ]; then
        mkdir -p "$backup_dir"
        echo "  ✓ Backup directory created: .spark-backup/"
    fi
    
    # Copy SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md to installation location
    if [ -f "SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" ]; then
        cp "SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" "$INSTALL_LOCATION/"
        echo "  ✓ SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md copied"
    else
        print_warning "SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md file not found"
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
        # Create backup before modifying
        if [ ! -f "$backup_dir/CLAUDE.md.original" ]; then
            cp "$claude_md" "$backup_dir/CLAUDE.md.original"
            echo "  ✓ CLAUDE.md backup created: .spark-backup/CLAUDE.md.original"
        else
            print_warning "Backup file already exists: .spark-backup/CLAUDE.md.original"
        fi
        
        # Check if reference already exists
        if grep -q "@SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md" "$claude_md"; then
            print_warning "SPARK reference already exists in CLAUDE.md"
        else
            # Add SPARK reference to the end of CLAUDE.md
            cat >> "$claude_md" << 'EOF'

---

@SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md
EOF
            print_success "SPARK reference added to CLAUDE.md"
        fi
    else
        print_warning "CLAUDE.md file not found - manual addition required"
        echo "  Add the following content to the end of your CLAUDE.md file:"
        echo "  @SPARK_GLOBAL_GUIDE_FOR_CLAUDE_MD.md"
    fi
    
    print_success "SPARK global guide installation completed"
}

# Function to configure settings.json
configure_settings() {
    print_status "Configuring settings.json..."
    
    local settings_file="$INSTALL_LOCATION/settings.json"
    local backup_dir="$INSTALL_LOCATION/.spark-backup"
    
    # Create backup directory if it doesn't exist
    if [ ! -d "$backup_dir" ]; then
        mkdir -p "$backup_dir"
    fi
    
    # Backup existing settings
    if [ -f "$settings_file" ]; then
        if [ ! -f "$backup_dir/settings.json.original" ]; then
            cp "$settings_file" "$backup_dir/settings.json.original"
            print_warning "Existing settings backed up: .spark-backup/settings.json.original"
        fi
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
        "description": "SPARK Persona Router - Task analysis and optimal agent selection",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH/spark_persona_router.py",
            "timeout": 60
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "description": "SPARK Quality Gates - Jason's 8-step strict validation",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH/spark_quality_gates.py",
            "timeout": 60
          }
        ]
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
        print_success "settings.json with hooks created"
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
        print_success "Basic settings.json created"
    fi
}

# Function to show installation summary
show_summary() {
    echo ""
    echo -e "${GREEN}⚡⚡⚡ Installation Complete! ⚡⚡⚡${NC}"
    echo ""
    echo -e "${CYAN}Installed Components:${NC}"
    
    [ "$INSTALL_AGENTS" = true ] && echo "  ✓ 16 SPARK agents"
    [ "$INSTALL_COMMANDS" = true ] && echo "  ✓ Single agent commands"
    [ "$INSTALL_MULTI_AGENT" = true ] && echo "  ✓ Multi-agent pipelines"
    [ "$INSTALL_HOOKS" = true ] && echo "  ✓ Hook scripts"
    [ "$INSTALL_WORKFLOWS" = true ] && echo "  ✓ Workflow settings"
    
    echo ""
    echo -e "${CYAN}Installation Location:${NC} $INSTALL_LOCATION"
    
    if [ -n "$NAMESPACE_PREFIX" ]; then
        echo -e "${CYAN}Namespace:${NC} /$NAMESPACE_PREFIX:*"
    fi
    
    echo ""
    echo -e "${GREEN}Next Steps:${NC}"
    echo "1. Restart Claude Code to load new settings"
    
    if [ "$INSTALL_COMMANDS" = true ]; then
        echo "2. Try SPARK commands:"
        if [ -n "$NAMESPACE_PREFIX" ]; then
            echo -e "   ${BLUE}/$NAMESPACE_PREFIX:implement \"user authentication\"${NC}"
            echo -e "   ${BLUE}/$NAMESPACE_PREFIX:test \"create unit tests\"${NC}"
        else
            echo -e "   ${BLUE}/spark-implement \"user authentication\"${NC}"
            echo -e "   ${BLUE}/spark-test \"create unit tests\"${NC}"
        fi
    fi
    
    if [ "$INSTALL_MULTI_AGENT" = true ]; then
        echo "3. Use multi-agent pipelines:"
        echo -e "   ${BLUE}/spark-launch \"new feature\"${NC} - Full development pipeline"
        echo -e "   ${BLUE}/spark-optimize \"improve performance\"${NC} - Performance optimization"
        echo -e "   ${BLUE}/spark-audit \"security check\"${NC} - Security audit"
    fi
    
    echo ""
    echo -e "${CYAN}Key Features:${NC}"
    echo "• significant token efficiency (verified)"
    echo "• 16 specialized agents"
    echo "• Jason's 8-step strict quality gates"
    echo "• Automatic persona activation"
    echo "• Parallel execution: Multiple Tasks in ONE MESSAGE"
    echo "• Fallback path support (global/project auto-detection)"
    
    if [ "$INSTALL_AGENTS" = true ]; then
        echo "• Memory reference auto-installation (CLAUDE.md updated)"
    fi
    
    if [[ "$INSTALL_LOCATION" == "$HOME/.claude" ]]; then
        echo ""
        echo -e "${YELLOW}Note:${NC}"
        echo "• Globally installed agents are available for all projects"
        echo "• Workflow files are stored in ~/.claude/workflows/"
        echo "• Create .claude/ directory for project-specific settings when needed"
        echo "• @SPARK_AGENTS_MEMORY_REFERENCE.md added to CLAUDE.md"
    fi
    
    echo ""
    echo -e "${BLUE}Documentation:${NC} https://github.com/Jaesun23/spark-claude"
    echo -e "${BLUE}Guide:${NC} /Users/jason/Projects/spark-claude/docs/SPARK_COMPLETE_GUIDE.md"
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
    echo -e "${YELLOW}=== Installation Confirmation ===${NC}"
    echo "Location: $INSTALL_LOCATION"
    echo "Components:"
    [ "$INSTALL_AGENTS" = true ] && echo "  • Agents"
    [ "$INSTALL_COMMANDS" = true ] && echo "  • Commands"
    [ "$INSTALL_MULTI_AGENT" = true ] && echo "  • Multi-agent pipelines"
    [ "$INSTALL_HOOKS" = true ] && echo "  • Hooks"
    [ "$INSTALL_WORKFLOWS" = true ] && echo "  • Workflows"
    echo ""
    
    read -p "Proceed with installation? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_warning "Installation cancelled"
        exit 0
    fi
    
    # Step 4: Create directories
    print_status "Creating directories..."
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