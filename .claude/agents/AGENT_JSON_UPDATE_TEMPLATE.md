# Agent JSON File Management Update Template

## Phase 0: Task Initialization Update

Replace existing Phase 0 with:

```markdown
### Phase 0: Task Initialization (작업 초기화)

**Step 1: Determine Project Context**
```bash
# Find project root (look for .git, pyproject.toml, package.json)
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
WORKFLOW_DIR="${PROJECT_ROOT}/.claude/workflows"

# Create directory structure if needed
mkdir -p "${WORKFLOW_DIR}/active"
mkdir -p "${WORKFLOW_DIR}/results"
mkdir -p "${WORKFLOW_DIR}/locks"

echo "Working in project: ${PROJECT_ROOT}"
echo "Workflow directory: ${WORKFLOW_DIR}"
```

**Step 2: Check for Parallel Execution**
```bash
# For team agents - use fixed naming
TASK_FILE="${WORKFLOW_DIR}/active/team{N}_current_task.json"

# For regular agents - check if parallel instance needed
AGENT_NAME="{agent-name}"
if [ -f "${WORKFLOW_DIR}/active/current_task.json" ]; then
    # Check if same agent already running
    if grep -q "\"current_agent\": \"${AGENT_NAME}\"" "${WORKFLOW_DIR}/active/current_task.json"; then
        # Generate instance ID for parallel execution
        INSTANCE_ID=$(date +%s%N | md5sum | head -c 8)
        TASK_FILE="${WORKFLOW_DIR}/active/${AGENT_NAME}_${INSTANCE_ID}_current.json"
        echo "Parallel execution detected. Using: ${TASK_FILE}"
    fi
else
    TASK_FILE="${WORKFLOW_DIR}/active/current_task.json"
fi
```

**Step 3: Initialize Task JSON**
```bash
# Read task or create new
if [ -f "${TASK_FILE}" ]; then
    cat "${TASK_FILE}"
else
    # Initialize from template
    cp "${WORKFLOW_DIR}/templates/current_task_template.json" "${TASK_FILE}"
fi
```
```

## Phase 5B: JSON Update & Quality Verification Update

Replace existing Phase 5B Step 3 with:

```markdown
**Step 3: Update JSON and Verify**

```bash
# Use project-specific workflow directory
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
WORKFLOW_DIR="${PROJECT_ROOT}/.claude/workflows"

# Determine correct JSON file
AGENT_NAME="{agent-name}"
TASK_FILE="${WORKFLOW_DIR}/active/{appropriate-json-file}"

# Update JSON with quality results
cat > "${TASK_FILE}" << 'EOF'
{
  "version": "4.1",
  "project_root": "${PROJECT_ROOT}",
  "workflow_dir": "${WORKFLOW_DIR}",
  // ... rest of JSON
}
EOF

# Run quality gates verification
echo "{\"subagent\": \"${AGENT_NAME}\", \"json_file\": \"${TASK_FILE}\"}" | \
python3 ${PROJECT_ROOT}/.claude/hooks/spark_quality_gates.py

# On success, archive the result
if [ $? -eq 0 ]; then
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    RESULT_FILE="${WORKFLOW_DIR}/results/${TIMESTAMP}_${AGENT_NAME}_result.json"
    cp "${TASK_FILE}" "${RESULT_FILE}"
    echo "✅ Results archived to: ${RESULT_FILE}"
    
    # Clean up active file (unless team agent)
    if [[ ! "${TASK_FILE}" =~ team[1-4]_current_task.json ]]; then
        rm "${TASK_FILE}"
    fi
fi
```
```

## File Lock Management Addition

Add to Phase 1 (Planning):

```markdown
**Step 2.5: Acquire File Locks**

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LOCK_FILE="${PROJECT_ROOT}/.claude/workflows/locks/file_locks.json"

# List files to be modified
FILES_TO_MODIFY=("src/core.py" "src/api.py")

# Check and acquire locks
python3 << 'EOF'
import json
import os
from datetime import datetime, timedelta

lock_file = "${LOCK_FILE}"
files_to_lock = ${FILES_TO_MODIFY[@]}
agent_name = "${AGENT_NAME}"

# Load existing locks
if os.path.exists(lock_file):
    with open(lock_file, 'r') as f:
        locks = json.load(f)
else:
    locks = {}

# Check for conflicts
conflicts = []
for file in files_to_lock:
    if file in locks:
        lock_info = locks[file]
        if datetime.fromisoformat(lock_info['expires_at']) > datetime.now():
            conflicts.append(f"{file} locked by {lock_info['locked_by']}")

if conflicts:
    print(f"❌ Cannot proceed. Conflicts: {conflicts}")
    exit(1)

# Acquire locks
for file in files_to_lock:
    locks[file] = {
        'locked_by': agent_name,
        'locked_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
    }

# Save locks
with open(lock_file, 'w') as f:
    json.dump(locks, f, indent=2)

print(f"✅ Acquired locks for {len(files_to_lock)} files")
EOF
```
```

## Critical Changes Summary

1. **Always use PROJECT_ROOT/.claude/workflows/** not ~/.claude/workflows/
2. **Check for parallel execution** and use unique filenames
3. **Implement file locking** for parallel agents
4. **Archive results with timestamps** for tracking
5. **Clean up active files** after completion

## Migration Checklist

For each agent file:
- [ ] Update Phase 0 to determine PROJECT_ROOT
- [ ] Update Phase 5B to use project-specific paths  
- [ ] Add file lock acquisition in Phase 1
- [ ] Add file lock release in Phase 5B
- [ ] Add parallel execution detection
- [ ] Test with multiple simultaneous calls