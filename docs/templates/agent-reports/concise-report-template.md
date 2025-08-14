# 간결 보고서 템플릿 (실행/구현 에이전트용)

## 적용 대상 에이전트
- implementer-spark
- tester-spark
- improver-spark
- cleaner-spark
- builder-spark
- gitter-spark
- spawner-spark
- tasker-spark
- indexer-spark
- 모든 team 에이전트 (team1-4)

## 템플릿 구조

```markdown
# Task Completion Report: [Task Name]

## Summary
- **Agent**: [agent-name]
- **Date**: [ISO-8601 timestamp]
- **Task**: [Original task description]
- **Status**: ✅ Completed | ⚠️ Partial | ❌ Blocked
- **Duration**: [Time taken]

## Work Performed
- [Bullet list of specific actions taken]
- [Files created/modified with paths]
- [Key decisions made]
- [Technologies/tools used]

## Results
- **Success Metrics**: [What was achieved]
- **Quality Checks**: [Tests passed, linting results, etc.]
- **Performance Impact**: [If applicable]
- **Coverage**: [Test coverage, code coverage, etc.]

## Issues & Resolutions
- [Any problems encountered and how they were resolved]
- [Workarounds applied]
- [Known limitations]

## Next Steps
- [Recommended follow-up actions]
- [Dependencies for other agents]
- [Maintenance considerations]

## Artifacts
- Output files: [List with paths]
- Test results: [Location]
- Related documentation: [Links]
- Configuration changes: [List]
```

## 사용 지침
1. 보고서 위치: `/docs/agents-task/[agent-name]/[task_name]_[timestamp].md`
2. 최소 분량: 150-300줄
3. 핵심 정보 위주로 간결하게 작성
4. 실행 결과와 메트릭 중심