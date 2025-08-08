# /clean-spark - SPARK Project Cleanup Command

**Purpose**: Comprehensive project cleanup and technical debt reduction with SPARK intelligence

## Execution Instructions

When this command is called, use the Task tool to launch the `cleaner-spark` agent:

```
Use the Task tool with subagent_type "cleaner-spark" to perform comprehensive project cleanup.
Pass the user's specific cleanup request as the prompt parameter.
The cleaner-spark agent will analyze, clean, and optimize the project structure while maintaining functionality.
```

## Usage Examples

```bash
/clean-spark "full project cleanup and optimization"
/clean-spark "remove unused dependencies and files"
/clean-spark "fix code quality issues and linting violations"
/clean-spark "optimize directory structure and documentation"
```

## Cleanup Capabilities

- **File Management**: Remove duplicates, temporary files, empty directories
- **Code Quality**: Fix linting issues, improve formatting, add type hints
- **Dependencies**: Remove unused packages, optimize requirements
- **Structure**: Organize directories, consolidate similar functionality
- **Documentation**: Clean up outdated docs, fix broken references

## SPARK Quality Assurance

All cleanup operations ensure:
- No functionality is broken (verified by quality gates)
- Code quality improvements (Ruff + MyPy compliance)
- Project structure follows SPARK architectural patterns
- 88.4% token efficiency maintained throughout cleanup process