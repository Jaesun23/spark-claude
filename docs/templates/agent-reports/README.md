# Agent Report Templates

이 디렉토리는 SPARK 에이전트들의 보고서 작성을 위한 템플릿을 보관합니다.

## 📁 템플릿 종류

### 1. detailed-report-template.md
- **용도**: 분석/설계 성격의 에이전트용 상세 보고서
- **대상**: analyzer, designer, troubleshooter, estimater, loader, explainer, documenter
- **분량**: 500-800줄 이상
- **특징**: 9-12개 주요 섹션, 상세한 증거 기반 분석

### 2. concise-report-template.md  
- **용도**: 실행/구현 성격의 에이전트용 간결 보고서
- **대상**: implementer, tester, improver, cleaner, builder, gitter, spawner, tasker, indexer, team agents
- **분량**: 150-300줄
- **특징**: 핵심 정보 위주, 실행 결과 중심

## 📍 실제 보고서 저장 위치
모든 에이전트 보고서는 다음 위치에 저장됩니다:
```
/docs/agents-task/[agent-name]/[task_name]_[timestamp].md
```

## ⚠️ 중요 사항
- 이 템플릿들은 **참고용**입니다
- 실제 작동하는 지침은 각 에이전트 파일(`.claude/agents/*.md`)에 있습니다
- 어제(2025-08-13) 작업한 버전이 공식 버전입니다

## 📅 생성 일자
- 2025-08-14: 오늘 작업한 템플릿을 별도 보관용으로 정리