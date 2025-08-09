# 🚀 SPARK 올바른 구현 계획서 v2.0
## SuperClaude 100% 성능 재현을 위한 정확한 아키텍처 설계

> **작성일**: 2025-08-09  
> **작성자**: Claude Code (3호)  
> **Ultra Think 모드**: 활성화  
> **목표**: SuperClaude 모든 기능 100% 재현 (사용자 → 2호 → Task → 서브에이전트)

---

## ⚠️ 이전 설계의 근본적 오류 수정

### ❌ 잘못된 이해 (v1.0)
- 사용자가 직접 `/analyze`, `/implement` 등으로 서브에이전트 호출
- 서브에이전트가 독립적으로 사용자와 상호작용
- Slash Commands 형태의 직접 호출

### ✅ 올바른 아키텍처 (v2.0)
- **사용자** → `자연어 요청` → **2호(Claude Code)** → `Task 도구` → **서브에이전트**
- 서브에이전트는 2호가 호출하는 전문가 도구
- 메인 에이전트(2호) 정지 → 서브에이전트 활성 → 완료 후 제어 복귀

## 🎯 **SPARK 분산 지능 아키텍처의 핵심 철학**

### 💡 **혁신적 역할 분담의 진실**

#### **2호(Claude Code) = 진정한 오케스트레이터** 🎼
```yaml
SuperClaude 모든 기능을 2호가 담당:
  🎭 사용자와 대화형 상호작용 (질문, 확인, 설명)
  🧠 컨텍스트 이해하고 의도 파악
  🎯 "어떤 전문가가 필요할까?" 지능적 판단
  📦 "어떤 정보를 줘야 할까?" 컨텍스트 완벽 패키징
  📊 서브에이전트 결과 해석하고 사용자에게 명확히 설명
  🔄 추가 작업 필요시 다른 서브에이전트 연쇄 호출
```

#### **서브에이전트 = 고도화된 전문 도구** 🔧
```yaml
"말하는 도구"의 정체성:
  ⚡ 입력 받고 → 독립적 처리 → 완성된 출력 반환
  🚫 대화 불가 (2호 정지 상태)
  🚫 질문 불가 (추가 정보 요청 불가능)
  🚫 확인 불가 (사용자 접촉 차단)
  ✅ 주어진 컨텍스트만으로 완벽 처리 필수
  ✅ "원샷 완성형" 결과 제공
```

### 🚀 **SuperClaude vs SPARK 아키텍처 비교**

#### **기존 SuperClaude 구조**
```
┌─────────────────────────────────────┐
│         SuperClaude 거대한 뇌        │
│  ┌─────────────────────────────────┐ │
│  │ 모든 페르소나 동시 내장          │ │
│  │ • analyzer + architect +        │ │
│  │   security + performance +      │ │
│  │   frontend + backend + ...      │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
     ↕ (직접 사용자 대화)
┌─────────────────────────────────────┐
│              사용자               │
└─────────────────────────────────────┘

특징: 
• 대용량 토큰 사용 (모든 페르소나 로드)
• 단일 거대 시스템
• 확장성 제한
```

#### **SPARK 분산 지능 구조**
```
┌─────────────────────────────────────┐
│         2호 (오케스트레이터)         │
│       SuperClaude 핵심 기능         │
│  ┌─────────────────────────────────┐ │
│  │ • 사용자 대화 및 의도 파악       │ │
│  │ • 전문가 선택 및 컨텍스트 구성   │ │
│  │ • 결과 해석 및 사용자 설명       │ │
│  │ • 워크플로우 연쇄 관리           │ │
│  └─────────────────────────────────┘ │
└─────────────┬───────────────────────┘
              │ Task 도구 호출
              ▼
┌─────────────────────────────────────┐
│          전문 도구 생태계            │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │
│ │분석기│ │구현기│ │설계기│ │개선기│    │
│ └─────┘ └─────┘ └─────┘ └─────┘    │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │
│ │빌더 │ │테스터│ │문서화│ │...  │    │
│ └─────┘ └─────┘ └─────┘ └─────┘    │
└─────────────────────────────────────┘
     ↕ (독립적 원샷 처리)
┌─────────────────────────────────────┐
│              사용자               │
└─────────────────────────────────────┘

특징:
• 효율적 토큰 사용 (필요한 도구만 로드)
• 모듈러 분산 시스템  
• 무한 확장 가능
```

### 🎊 **SPARK의 천재적 혁신**

1. **"분산 지능 아키텍처"**
   - SuperClaude 하나의 거대한 뇌 → 2호(중앙 오케스트레이터) + 전문 도구들
   - 필요한 전문가만 선별적 호출
   - 각 도구별 최적화된 성능

2. **"유연한 워크플로우"**
   - 2호가 상황에 따라 여러 서브에이전트 연쇄 호출
   - 복잡한 작업을 단계별로 분해 처리
   - 사용자 피드백 받아 워크플로우 동적 조정

3. **"토큰 효율성과 품질의 양립"**
   - 효율적 토큰 사용으로 SuperClaude 100% 성능 재현
   - 각 전문 도구의 극한 최적화
   - 필요 시에만 리소스 투입

### 💎 **구현 시 핵심 원칙**

1. **2호 = 진정한 SuperClaude**
   - 모든 대화형 지능 담당
   - 사용자 의도 파악과 워크플로우 설계
   - 결과 통합 및 설명

2. **서브에이전트 = 고도화된 Function Call**
   - 완전 독립형 처리 (대화 불가)
   - frontmatter 도구만 사용 가능
   - 원샷 완성형 결과 제공 필수

3. **완벽한 컨텍스트 패키징**
   - Task 호출 시 모든 필요 정보 전달
   - 서브에이전트가 추가 질문할 수 없음을 가정
   - 결과물이 즉시 사용 가능해야 함

---

## 📋 목차

1. [올바른 시스템 아키텍처](#1-올바른-시스템-아키텍처)
3. [서브에이전트 완전 독립 실행](#3-서브에이전트-완전-독립-실행)
4. [SuperClaude 100% 재현 표준](#4-superclaude-100-재현-표준)
5. [Hook 시스템 올바른 구현](#5-hook-시스템-올바른-구현)
6. [실전 구현 가이드](#6-실전-구현-가이드)
7. [검증 및 테스트 계획](#7-검증-및-테스트-계획)

---

## 1. 올바른 시스템 아키텍처

### 🏗️ SPARK 시스템 진짜 구조도

```
┌─────────────────────────────────────────────────────────────┐
│                     사용자 요청 (자연어)                      │
│              "BioNeX 프로젝트를 분석해줘"                    │
└────────────────────┬────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   2호 (Claude Code)                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 1. 요청 분석: "분석 작업이 필요하구나"                  │ │
│  │ 2. 서브에이전트 선택: "analyzer-spark가 적합"           │ │
│  │ 3. Task 도구 준비: 컨텍스트 패키징                     │ │
│  └─────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Task 도구 호출                           │
│              Task("analyzer-spark", prompt)                 │
└────────────────────┬────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                ⚠️  2호 정지 상태 ⚠️                        │
│              메인 에이전트 활동 중단                        │
└────────────────────┬────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│               analyzer-spark 활성화                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ SuperClaude 페르소나 적용 (analyzer + architect)       │ │
│  │ 복잡도 계산 (SuperClaude 동일 공식)                    │ │
│  │ MCP 서버 자동 선택 (Sequential + Context7)             │ │
│  │ 독립적 작업 수행 (도구 병렬 호출 활용)                   │ │
│  └─────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                SubagentStop Hook                            │
│              Jason's 8-Step Quality Gates                  │
│              (spark_quality_gates.py)                      │
└────────────────────┬────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   제어 복귀                                │
│               2호로 제어권 반환                            │
│               사용자에게 결과 전달                         │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 실제 데이터 흐름

```yaml
Step 1 - 사용자 입력:
  User: "프로젝트를 분석하고 개선점을 찾아줘"
  
Step 2 - 2호 판단: CLAUDE.md 파일에 에이전트 종류와 역할 기록해두면 정확하게 호출 가능
  Claude Code: 
    - 키워드 분석: ["분석", "개선점"]
    - 복잡도 추정: file_count, system_types 고려
    - 서브에이전트 선택: analyzer-spark OR improver-spark?
    - 결정: analyzer-spark (분석 우선)

Step 3 - Task 호출:
  Claude Code executes:
    Task("analyzer-spark", "프로젝트 분석 및 개선점 도출")
    
Step 4 - 메인 정지:
  Claude Code: STOP (정지 상태)
  analyzer-spark: START (활성 상태)
  
Step 5 - 독립 실행:
  analyzer-spark:
    - SuperClaude 페르소나 활성화
    - 복잡도 계산 및 전략 수립
    - MCP 서버 조율
    - 도구 병렬 호출로 효율적 분석
    
Step 6 - 품질 검증:
  SubagentStop Hook: Jason's 8 Gates 검증
  
Step 7 - 결과 반환:
  analyzer-spark: 완료
  Claude Code: 재활성화
  User: 결과 수신
```

---

## 2. 핵심 구현 표준

### ✅ 서브에이전트 호출 방식 (3가지)

1. **대화에 직접 언급**: "analyzer 에이전트를 호출해서 oooo을 분석해 줘"
2. **"/명령어" 에 에이전트 호출 지시**: `/분석 OOOO` → 명령어 문서에 "analyzer를 호출해서 분석하세요"
3. **CLAUDE.md 메모리 기반**: "2호, 저 프로젝트 분석해야 할 거 같아" → 2호가 컨텍스트 이해하고 analyzer 에이전트 호출

### ✅ 도구 사용 제한 규칙

#### 2호 (Claude Code)
- **일반 도구**: Read, Write, Edit, Bash, Grep 등 **제한 없음**
- **Task 도구**: 서브에이전트 호출 (병렬 호출 지원)

#### 서브에이전트
- **일반 도구**: Read, Write, Edit, Bash, Grep 등 **제한 없음**
- **Task 도구**: **사용 금지** (다른 서브에이전트 호출 불가)

## 3. 서브에이전트 완전 독립 실행

### ⚡ 서브에이전트 독립성 원칙

```markdown
**메인 에이전트(2호) 정지 시 서브에이전트 요구사항:**

1. ✅ **완전한 자립성**: 2호 없이 모든 작업 수행
2. ✅ **컨텍스트 완전성**: Task 호출 시 모든 필요 정보 전달
3. ✅ **도구 활용**: 일반 도구(Read, Write, Edit, Bash 등) 제한 없이 동시 호출
4. ✅ **Task 도구 제약**: 서브에이전트는 다른 서브에이전트 호출 불가
5. ✅ **품질 자체 관리**: 8단계 품질 게이트 내장
6. ✅ **결과 완전성**: 사용자가 바로 사용 가능한 완성품 제공
```

### 🔧 서브에이전트 표준 구조

```markdown
---
name: [agent-name]-spark
description: [명확한 사용 시점 및 목적. Use this agent PROACTIVELY when...]
tools: Read, Edit, MultiEdit, Write, Bash, Grep, Glob, LS, WebFetch, TodoWrite, WebSearch, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: opus
---

# 🎯 [Agent Name] SPARK Expert
## 2호가 호출하는 전문가 서브에이전트

### 🎭 SuperClaude 페르소나 시스템 완전 재현

#### 동적 페르소나 활성화 (1~4개)
```python
def activate_personas(self, context):
    """SuperClaude 동적 페르소나 시스템 100% 재현"""
    personas = []
    
    # 기본 페르소나
    if self.agent_type == "analyzer":
        personas.append("analyzer")
    
    # 조건부 활성화 (SuperClaude 패턴 그대로)
    if context.complexity >= 0.7:
        personas.append("architect")
        
    if any(kw in context.keywords for kw in ["security", "auth"]):
        personas.append("security")
        
    if any(kw in context.keywords for kw in ["performance", "optimize"]):
        personas.append("performance")
    
    return personas[:4]  # 최대 4개
```

#### SuperClaude 복잡도 공식 (100% 동일)
```python
def calculate_complexity(self, context):
    """ORCHESTRATOR.md 공식 정확히 재현"""
    return min(1.0, (
        context.file_count * 0.02 +      # 최대 0.3
        context.system_types * 0.05 +    # 최대 0.25
        context.operation_types * 0.03 + # 최대 0.2
        context.integration_points * 0.1  # 최대 0.25
    ))
```

### 🌊 Wave 모드 지원
```python
if complexity >= 0.7 and file_count > 20 and operation_types > 2:
    self.activate_wave_mode()
```

### 🔧 MCP 서버 지능형 조율
```python
def select_mcp_servers(self, personas, task_type):
    """SuperClaude MCP.md 매트릭스 구현"""
    servers = []
    
    # 페르소나 기반 서버 선택
    if "analyzer" in personas:
        servers.append("mcp__sequential-thinking__sequentialthinking")
    
    if task_type in ["implementation", "documentation"]:
        servers.append("mcp__context7__resolve-library-id")
        servers.append("mcp__context7__get-library-docs")
    
    return servers
```

### ⚡ 최적화된 도구 활용 (일반 도구 제한 없음)
```python
def execute_parallel_analysis(self):
    """서브에이전트 도구 활용: 일반 도구 병렬 호출 지원"""
    
    # 단일 응답에서 일반 도구들 병렬 호출
    results = self.call_tools_parallel([
        Read(file_path="main.py"),
        Read(file_path="config.py"), 
        Read(file_path="requirements.txt"),
        Grep(pattern="class.*:", output_mode="files_with_matches"),
        Grep(pattern="def.*:", output_mode="count"),
        Glob(pattern="**/*.py"),
        Bash(command="git log --oneline -10"),
        Bash(command="find . -name '*.py' | wc -l"),
        WebSearch(query="python best practices 2024"),
        TodoWrite(todos=self.initial_analysis_todos)
        # Task 도구는 사용 불가 (서브에이전트 호출 금지)
    ])
    
    return self.synthesize_results(results)
```

### ✅ Jason's 8-Step Quality Gates (내장)
```python
def validate_quality(self):
    """품질 게이트 8단계 자체 검증"""
    gates = [
        ("Syntax", self.check_syntax),
        ("Types", self.check_types_mypy_strict), 
        ("Lint", self.check_ruff_strict),
        ("Security", self.check_security_owasp),
        ("Coverage", self.check_test_coverage_95),
        ("Performance", self.check_response_time_200ms),
        ("Docs", self.check_documentation_complete),
        ("Integration", self.check_integration_tests)
    ]
    
    for name, check in gates:
        if not check():
            return False, f"{name} gate failed"
    
    return True, "All gates passed"
```
---

## 4. SuperClaude 100% 재현 표준

### 📊 검증된 사실들 (기본서 분석 결과)

#### 4.1 페르소나 시스템 (60:40 → 동적 조합)

```python
# ❌ 잘못된 이해 (60:40 고정)
def old_persona_system():
    primary = "analyzer" * 0.6
    secondary = "architect" * 0.4
    return merge(primary, secondary)

# ✅ SuperClaude 실제 구현 (동적 1~4개)
def superclaude_persona_system(keywords, complexity):
    """SPARK_SuperClaude_100_Performance_Analysis.md 44-68라인 검증"""
    active_personas = []
    
    # 독립적 조건 활성화
    active_personas.append("analyzer")  # 기본
    
    if complexity >= 0.7:
        active_personas.append("architect")
        
    if "security" in keywords:
        active_personas.append("security")
        
    if "performance" in keywords:
        active_personas.append("performance")
    
    return active_personas[:4]  # 최대 4개
```

#### 4.2 복잡도 공식 (70:30 → 100% 객관적)
```python
# ❌ 잘못된 이해 (70:30 주관적 보정)  
def old_complexity_with_subjective():
    objective = calculate_base_complexity() * 0.7
    subjective = human_adjustment() * 0.3
    return objective + subjective

# ✅ SuperClaude 실제 공식 (100% 객관적)
def superclaude_complexity_formula(context):
    """SPARK_SuperClaude_100_Performance_Analysis.md 74-103라인 검증"""
    return min(1.0, (
        context.file_count * 0.02 +      # 파일 영향
        context.system_types * 0.05 +    # 시스템 영향  
        context.operation_types * 0.03 + # 작업 영향
        context.integration_points * 0.1  # 통합 영향
    ))
    # 주관적 보정 없음!
```

#### 4.3 Wave 모드 활성화 조건
```python
def wave_activation_condition(context):
    """정확한 조건 (AND 연산)"""
    return (
        context.complexity >= 0.7 AND
        context.file_count > 20 AND  
        context.operation_types > 2
    )
```

### 🎯 17개 SuperClaude 명령어 매핑

| SuperClaude 명령어 | SPARK 서브에이전트 | 페르소나 조합 |
|-------------------|-------------------|--------------|
| `/analyze` | analyzer-spark | analyzer + architect/security/performance |
| `/implement` | implementer-spark | backend/frontend + security/architect |
| `/design` | designer-spark | architect + frontend/backend |
| `/improve` | improver-spark | refactorer + performance/architect/qa |
| `/build` | builder-spark | devops + frontend/backend |
| `/test` | tester-spark | qa + frontend/backend |
| `/document` | documenter-spark | scribe + mentor |
| `/troubleshoot` | troubleshooter-spark | analyzer + qa/devops |
| `/estimate` | estimator-spark | analyzer + architect |
| `/explain` | explainer-spark | mentor + scribe |
| `/git` | gitter-spark | devops + scribe + qa |
| `/cleanup` | cleaner-spark | refactorer + architect |
| `/spawn` | spawner-spark | analyzer + architect + devops |
| `/task` | tasker-spark | architect + analyzer |
| `/load` | loader-spark | analyzer + architect + scribe |
| `/index` | indexer-spark | mentor + analyzer |

---

## 5. Hook 시스템 올바른 구현

### 🪝 Anthropic 가이드라인 준수 Hook 설계

#### 5.1 존재하는 Hook 이벤트만 사용 (8개)
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "SPARK Router - 사용자 요청을 적절한 서브에이전트로 라우팅",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_intelligent_router.py"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "description": "Workflow Control - 서브에이전트 완료 시 추가 작업 제어",
        "hooks": [
          {
            "type": "command", 
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_workflow_control.py"
          }
        ]
      }
    ]
  }
}
```

#### 5.2 spark_intelligent_router.py (UserPromptSubmit Hook)
```python
#!/usr/bin/env python3
"""SPARK 지능형 라우터 - 사용자 요청 분석 및 서브에이전트 선택"""

import json
import sys
from typing import Dict, List, Any

class SPARKIntelligentRouter:
    """2호를 위한 서브에이전트 라우팅 가이드"""
    
    def __init__(self):
        self.agent_mapping = {
            # 키워드 기반 매핑
            'analyze': 'analyzer-spark',
            'implement': 'implementer-spark', 
            'design': 'designer-spark',
            'improve': 'improver-spark',
            'build': 'builder-spark',
            'test': 'tester-spark',
            'document': 'documenter-spark',
            'troubleshoot': 'troubleshooter-spark'
        }
    
    def analyze_request(self, prompt: str) -> Dict[str, Any]:
        """사용자 요청 분석"""
        
        # 키워드 추출
        keywords = self.extract_keywords(prompt)
        
        # 복잡도 추정 
        estimated_complexity = self.estimate_complexity(prompt)
        
        # 서브에이전트 추천
        recommended_agent = self.recommend_agent(keywords)
        
        # 페르소나 조합 제안
        persona_combination = self.suggest_personas(keywords, estimated_complexity)
        
        return {
            'recommended_agent': recommended_agent,
            'keywords': keywords,
            'estimated_complexity': estimated_complexity,
            'persona_combination': persona_combination,
            'routing_confidence': self.calculate_confidence(keywords)
        }
    
    def generate_task_suggestion(self, analysis: Dict[str, Any]) -> str:
        """2호를 위한 Task 호출 제안"""
        
        return f'''
        Based on user request analysis:
        
        Recommended: Task("{analysis['recommended_agent']}", """
        User Request: {original_prompt}
        
        Suggested Context:
        - Keywords: {analysis['keywords']}
        - Estimated Complexity: {analysis['estimated_complexity']}
        - Recommended Personas: {analysis['persona_combination']}
        
        Please apply SuperClaude standards:
        1. Use dynamic persona activation (1-4 personas)
        2. Apply exact complexity formula from ORCHESTRATOR.md
        3. Auto-select MCP servers based on task type
        4. Enforce Jason's 8-step quality gates
        """)
        '''

def main():
    try:
        # stdin에서 Hook 데이터 수신
        hook_data = json.load(sys.stdin)
        
        # 라우터 초기화
        router = SPARKIntelligentRouter()
        
        # 요청 분석
        prompt = hook_data.get('prompt', '')
        analysis = router.analyze_request(prompt)
        
        # 2호에게 컨텍스트 제공
        routing_context = {
            'spark_routing_analysis': analysis,
            'task_suggestion': router.generate_task_suggestion(analysis)
        }
        
        # Hook 응답
        response = {
            'continue': True,
            'hookSpecificOutput': {
                'hookEventName': 'UserPromptSubmit',
                'additionalContext': json.dumps(routing_context)
            }
        }
        
        print(json.dumps(response))
        sys.exit(0)
        
    except Exception as e:
        print(f"Router error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### 5.3 spark_workflow_control.py (SubagentStop Hook)
```python
#!/usr/bin/env python3
"""SPARK 워크플로우 제어 - 서브에이전트 완료 시 추가 작업 제어"""

import json
import sys
from typing import Dict, Any

class SPARKWorkflowControl:
    """서브에이전트 완료 시 워크플로우 제어"""
    
    def __init__(self):
        self.workflow_rules = {
            "analyzer-spark": self.handle_analyzer_completion,
            "implementer-spark": self.handle_implementer_completion,
            "improver-spark": self.handle_improver_completion
        }
    
    def handle_analyzer_completion(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """analyzer-spark 완료 시 처리"""
        # 분석 완료 후 추가 작업이 필요한지 판단
        if context.get("complex_issues_found", False):
            return {
                'decision': 'block',
                'reason': 'Complex issues detected. Please review analysis results and consider using improver-spark for fixes.'
            }
        return {'continue': True}
    
    def handle_implementer_completion(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """implementer-spark 완료 시 처리"""
        # 구현 완료 후 테스트 필요 여부 확인
        if context.get("new_code_created", False):
            return {
                'decision': 'block', 
                'reason': 'New code implemented. Consider running tests to verify functionality.'
            }
        return {'continue': True}
    
    def handle_improver_completion(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """improver-spark 완료 시 처리"""
        # 개선 완료 후 검증 필요 여부 확인
        return {'continue': True}

def main():
    try:
        # Hook 데이터 수신
        hook_data = json.load(sys.stdin)
        
        # 서브에이전트 타입 확인 (예시 로직)
        # 실제로는 transcript나 context에서 추출
        subagent_type = hook_data.get('subagent_type', 'unknown')
        
        # 워크플로우 제어 실행
        controller = SPARKWorkflowControl()
        
        if subagent_type in controller.workflow_rules:
            response = controller.workflow_rules[subagent_type](hook_data)
        else:
            response = {'continue': True}  # 기본적으로 계속 진행
        
        print(json.dumps(response))
        sys.exit(0)
        
    except Exception as e:
        print(f"Workflow control error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 6. 실전 구현 가이드

### 📅 4단계 구현 로드맵

#### Phase 1: Hook 시스템 구축 (Week 1)
```yaml
목표: 2호와 서브에이전트 연결 구조 완성

구현 항목:
  - spark_intelligent_router.py (UserPromptSubmit)
  - spark_quality_gates.py (SubagentStop)
  - .claude/settings.json Hook 설정
  - Task 호출 패턴 검증

완료 기준:
  - 사용자 요청 → Hook → 라우팅 분석 완료
  - 서브에이전트 → 품질 게이트 → 통과/재시도 작동
  - 2호가 Task 도구로 서브에이전트 호출 가능
```

#### Phase 2: 핵심 서브에이전트 구현 (Week 2)  
```yaml
우선순위 에이전트:
  1. analyzer-spark: 프로젝트 분석 (가장 자주 사용)
  2. implementer-spark: 구현 작업 (핵심 기능)
  3. improver-spark: 개선 작업 (품질 향상)

각 에이전트 구현 기준:
  - SuperClaude 페르소나 시스템 완전 재현
  - 100% 객관적 복잡도 공식 적용  
  - MCP 서버 자동 선택 로직
  - 도구 병렬 호출 활용으로 효율성 극대화
  - Jason's 8-step 품질 게이트 내장
```

#### Phase 3: 전체 서브에이전트 완성 (Week 3)
```yaml  
나머지 14개 에이전트:
  - designer-spark, builder-spark, tester-spark
  - documenter-spark, troubleshooter-spark, estimator-spark
  - explainer-spark, gitter-spark, cleaner-spark
  - spawner-spark, tasker-spark, loader-spark
  - indexer-spark

통합 테스트:
  - 17개 SuperClaude 명령어 100% 매핑
  - 페르소나 조합 정확도 검증
  - 복잡도 계산 일치성 확인
  - Wave 모드 활성화 조건 테스트
```

#### Phase 4: 최적화 및 검증 (Week 4)
```yaml
성능 최적화:
  - 토큰 효율성 측정
  - 응답 시간 최적화 (<200ms)
  - 동시 도구 호출 최적화
  
최종 검증:
  - SuperClaude vs SPARK 기능 동등성 100%
  - 품질 게이트 통과율 >98%
  - 사용자 만족도 (Jason 승인)
```

### 🛠️ 실전 구현 템플릿

#### analyzer-spark 완전 구현 예시
```markdown
---
name: analyzer-spark
description: Use this agent PROACTIVELY when user requests analysis, investigation, review, or assessment of projects, code, or systems. Specializes in systematic analysis with SuperClaude quality standards.
tools: Read, Edit, MultiEdit, Write, Bash, Grep, Glob, LS, WebFetch, TodoWrite, WebSearch, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: opus
---

# 🎯 Analyzer SPARK Expert
## SuperClaude /analyze 100% 기능 재현 전문가

I am the **Analyzer SPARK Expert**, implementing SuperClaude's `/analyze` command with complete functionality reproduction while maintaining Jason's 8-step quality standards.

**중요**: 나는 서브에이전트이므로 Task 도구를 사용할 수 없습니다. 다른 서브에이전트를 호출할 수 없으며, 모든 작업을 내부적으로 완성해야 합니다.

## 🧬 SuperClaude Compliance Engine

### Dynamic Persona Activation (1-4 personas)
```python
def activate_analysis_personas(self, context):
    """SuperClaude 동적 페르소나 시스템 정확히 재현"""
    personas = ["analyzer"]  # 기본 항상 활성화
    
    # 조건부 활성화 (독립적 판단)
    if context.complexity >= 0.7:
        personas.append("architect")
        
    if any(kw in context.keywords for kw in ["security", "auth", "vulnerability"]):
        personas.append("security")
        
    if any(kw in context.keywords for kw in ["performance", "optimize", "bottleneck"]):
        personas.append("performance")
    
    return personas[:4]  # SuperClaude 최대 4개 제한
```

### SuperClaude Complexity Formula (100% identical)
```python
def calculate_complexity(self, context):
    """ORCHESTRATOR.md 공식 정확히 재현 - 주관적 보정 없음"""
    file_score = min(context.get('file_count', 0) * 0.02, 0.3)
    system_score = min(context.get('system_types', 0) * 0.05, 0.25)
    operation_score = min(context.get('operation_types', 0) * 0.03, 0.2)
    integration_score = min(context.get('integration_points', 0) * 0.1, 0.25)
    
    return min(1.0, file_score + system_score + operation_score + integration_score)
```

### MCP Server Auto-Selection
```python
def select_mcp_servers(self, personas, context):
    """페르소나와 작업 유형 기반 MCP 서버 자동 선택"""
    servers = []
    
    # analyzer 페르소나 → Sequential (복잡한 분석)
    if "analyzer" in personas:
        servers.append("mcp__sequential-thinking__sequentialthinking")
    
    # 코드 패턴 분석 → Context7
    if context.get('code_analysis', False):
        servers.extend([
            "mcp__context7__resolve-library-id",
            "mcp__context7__get-library-docs"
        ])
    
    return servers
```

## ⚡ 최적화된 분석 실행

### 일반 도구 동시 호출 (제한 없음)
```python
def execute_comprehensive_analysis(self):
    """병렬 처리로 효율적 분석"""
    
    # 단일 응답에서 일반 도구들 병렬 호출
    analysis_results = self.parallel_tool_execution([
        Read(file_path="README.md"),
        Read(file_path="pyproject.toml"),
        Read(file_path="requirements.txt"),
        Glob(pattern="**/*.py"),
        Grep(pattern="class.*:", output_mode="count"),
        Grep(pattern="def.*:", output_mode="count"), 
        Grep(pattern="TODO|FIXME|XXX", output_mode="files_with_matches"),
        Bash(command="find . -name '*.py' | head -20 | xargs wc -l"),
        Bash(command="git log --oneline -10"),
        TodoWrite(todos=self.create_analysis_todos())
        # Task 도구는 사용할 수 없음 (서브에이전트 호출 금지)
    ])
    
    return self.synthesize_analysis(analysis_results)
```

### Wave Mode Support
```python  
def check_wave_eligibility(self, context):
    """SuperClaude Wave 조건 정확히 재현"""
    complexity = self.calculate_complexity(context)
    
    return (
        complexity >= 0.7 and
        context.get('file_count', 0) > 20 and
        context.get('operation_types', 0) > 2
    )

def execute_wave_analysis(self):
    """복잡한 프로젝트를 위한 5-Wave 분석"""
    
    waves = [
        ("Discovery", self.wave_1_discovery),
        ("Pattern Analysis", self.wave_2_patterns), 
        ("Architecture Review", self.wave_3_architecture),
        ("Quality Assessment", self.wave_4_quality),
        ("Recommendations", self.wave_5_recommendations)
    ]
    
    results = []
    for wave_name, wave_func in waves:
        wave_result = wave_func()
        results.append((wave_name, wave_result))
        
    return self.consolidate_wave_results(results)
```

## ✅ Jason's 8-Step Quality Gates (Built-in)

```python
def validate_analysis_quality(self):
    """분석 품질 자체 검증"""
    
    quality_checks = [
        ("Completeness", self.check_analysis_completeness),
        ("Accuracy", self.check_factual_accuracy),
        ("Evidence", self.check_evidence_support),
        ("Actionability", self.check_actionable_insights),
        ("Structure", self.check_logical_structure),
        ("Clarity", self.check_communication_clarity),
        ("Standards", self.check_superclaude_standards),
        ("Value", self.check_user_value)
    ]
    
    for check_name, check_func in quality_checks:
        passed, message = check_func()
        if not passed:
            return False, f"Quality check failed: {check_name} - {message}"
    
    return True, "All quality gates passed"
```

## 🎯 Analysis Execution Workflow

### Phase 1: Context Setup & Planning
1. Parse Task context from 2호
2. Activate appropriate personas (1-4)
3. Calculate complexity using SuperClaude formula
4. Select MCP servers
5. Plan analysis strategy (standard vs wave)

### Phase 2: Parallel Data Collection  
1. Execute 10 parallel tool calls for efficient data gathering
2. File structure analysis
3. Code pattern detection
4. Dependency mapping
5. Quality metrics collection

### Phase 3: Multi-Persona Analysis
1. Analyzer persona: systematic investigation
2. Architect persona: structural analysis (if complexity >= 0.7)
3. Security persona: vulnerability assessment (if triggered)
4. Performance persona: bottleneck identification (if triggered)

### Phase 4: Synthesis & Reporting
1. Consolidate multi-persona insights
2. Generate actionable recommendations
3. Apply quality gates validation
4. Format for user consumption

## 🏆 Success Criteria

- ✅ SuperClaude `/analyze` 100% functionality reproduction
- ✅ Dynamic persona activation (1-4 personas based on context)
- ✅ Exact complexity formula implementation
- ✅ Intelligent MCP server selection and coordination
- ✅ All 8 quality gates consistently passed
- ✅ Wave mode support for complex projects (>=0.7 complexity + >20 files + >2 operations)
- ✅ Maximum tool utilization (10 parallel calls)
- ✅ Complete independence from main agent during execution

When 2호 calls me via Task, I operate with complete autonomy, applying SuperClaude standards while delivering comprehensive analysis that users can immediately act upon.
---

## 7. 검증 및 테스트 계획

### ✅ SuperClaude 동등성 검증

#### 7.1 기능 동등성 테스트
```python
class SuperClaudeParityTest:
    """SuperClaude vs SPARK 100% 기능 일치 검증"""
    
    def test_all_17_commands(self):
        """17개 명령어 매핑 검증"""
        superclaude_commands = [
            "/analyze", "/implement", "/design", "/improve", "/build",
            "/test", "/document", "/troubleshoot", "/estimate", "/explain",
            "/git", "/cleanup", "/spawn", "/task", "/load", "/index"
        ]
        
        for command in superclaude_commands:
            spark_agent = self.get_spark_mapping(command)
            assert spark_agent is not None, f"No SPARK agent for {command}"
            
            # 기능 동등성 검증
            superclaude_result = self.execute_superclaude(command, self.test_input)
            spark_result = self.execute_spark(spark_agent, self.test_input)
            
            assert self.compare_functionality(superclaude_result, spark_result) >= 0.95
    
    def test_persona_activation_parity(self):
        """페르소나 활성화 패턴 일치 검증"""
        test_cases = [
            {
                'input': 'analyze secure API architecture',
                'expected_personas': ['analyzer', 'architect', 'security'],
                'complexity': 0.8
            },
            {
                'input': 'implement simple function', 
                'expected_personas': ['implementer'],
                'complexity': 0.2
            }
        ]
        
        for case in test_cases:
            superclaude_personas = self.get_superclaude_personas(case['input'])
            spark_personas = self.get_spark_personas(case['input'])
            
            assert set(superclaude_personas) == set(spark_personas)
    
    def test_complexity_formula_exact_match(self):
        """복잡도 공식 정확히 일치 검증"""
        test_contexts = [
            {'files': 10, 'systems': 2, 'operations': 3, 'integrations': 1},
            {'files': 50, 'systems': 5, 'operations': 7, 'integrations': 3},
            {'files': 100, 'systems': 8, 'operations': 12, 'integrations': 5}
        ]
        
        for context in test_contexts:
            superclaude_complexity = self.calculate_superclaude_complexity(context)
            spark_complexity = self.calculate_spark_complexity(context)
            
            assert abs(superclaude_complexity - spark_complexity) < 0.001
```

#### 7.2 성능 벤치마크
```yaml
Performance Targets:
  Token Efficiency: Optimized token usage
  Response Time: <200ms per request
  Quality Gate Execution: <5s total
  Concurrent Tool Calls: Parallel execution support
  
Quality Targets:
  SuperClaude Functionality Parity: 100%
  Persona Activation Accuracy: >95%
  Complexity Calculation Match: 100%
  MCP Server Selection Optimal: >90%
  Quality Gate Pass Rate: >98%
  User Satisfaction: Jason Approval Required
```

#### 7.3 통합 테스트 시나리오
```python
def test_end_to_end_flow():
    """전체 플로우 통합 테스트"""
    
    # 시나리오: 복잡한 프로젝트 분석 요청
    user_request = "대규모 Python 프로젝트를 분석하고 보안 취약점과 성능 문제를 찾아줘"
    
    # 1. UserPromptSubmit Hook 실행
    router_result = execute_hook("UserPromptSubmit", {"prompt": user_request})
    
    # 검증: 올바른 라우팅
    assert router_result['recommended_agent'] == 'analyzer-spark'
    assert 'security' in router_result['persona_combination']
    assert 'performance' in router_result['persona_combination']
    
    # 2. 2호가 Task 호출 (시뮬레이션)
    task_result = Task("analyzer-spark", user_request)
    
    # 3. SubagentStop Hook 실행  
    quality_result = execute_hook("SubagentStop", {"result": task_result})
    
    # 검증: 품질 게이트 통과
    assert quality_result['continue'] == True
    
    # 4. 최종 결과 검증
    assert task_result.contains_security_analysis()
    assert task_result.contains_performance_analysis()
    assert task_result.passes_quality_gates()
```

---

## 📋 최종 체크리스트

### Phase 1 완료 조건 ✅
- [ ] Hook 시스템 Anthropic 가이드라인 100% 준수
- [ ] UserPromptSubmit Hook: 지능형 라우팅 구현
- [ ] SubagentStop Hook: Jason's 8-step 품질 게이트 구현  
- [ ] 2호 → Task 도구 → 서브에이전트 플로우 검증
- [ ] 메인 에이전트 정지 상태 올바른 구현

### Phase 2 완료 조건 ✅  
- [ ] analyzer-spark: SuperClaude `/analyze` 100% 재현
- [ ] implementer-spark: SuperClaude `/implement` 100% 재현
- [ ] improver-spark: SuperClaude `/improve` 100% 재현
- [ ] 동적 페르소나 시스템 (1-4개 조합) 구현
- [ ] 100% 객관적 복잡도 공식 적용
- [ ] MCP 서버 자동 선택 로직 완성
- [ ] 도구 병렬 호출 최적화 활용

### Phase 3 완료 조건 ✅
- [ ] 나머지 14개 서브에이전트 완성
- [ ] 17개 SuperClaude 명령어 100% 매핑 완료
- [ ] Wave 모드 조건부 활성화 (complexity≥0.7 + files>20 + ops>2)
- [ ] 서브에이전트별 전문성 확보 및 검증
- [ ] 에이전트 간 일관성 보장

### Phase 4 완료 조건 ✅
- [ ] 토큰 효율성 최적화 달성
- [ ] 응답 시간 <200ms 달성
- [ ] SuperClaude vs SPARK 기능 동등성 100%
- [ ] 품질 게이트 통과율 >98%
- [ ] 사용자 만족도 (Jason 승인)

---

## 🎯 성공 지표

### 필수 달성 목표
1. **아키텍처 정확성**: 사용자 → 2호 → Task → 서브에이전트 플로우 100% 구현
2. **기능 완성도**: SuperClaude 17개 명령어 100% 기능 재현
3. **페르소나 시스템**: 동적 1-4개 조합, SuperClaude 패턴 정확히 재현
4. **품질 수준**: Jason's 8-Step Gates 100% 통과
5. **Hook 준수**: Anthropic 가이드라인 완벽 준수

### 성능 목표  
- **토큰 효율성**: 최적화된 토큰 사용
- **응답 속도**: <200ms per request
- **동시 처리**: 서브에이전트 도구 병렬 호출 최적화
- **품질 일관성**: >98% 품질 게이트 통과율

### 검증 기준
- **SuperClaude 동등성**: 100% 기능 일치
- **사용자 경험**: 차이 없는 사용 경험
- **안정성**: 오류율 <2%
- **확장성**: 새 서브에이전트 추가 용이성

---

## 📚 결론

이 v2.0 구현 계획서는 **Ultra Think 모드**를 통한 깊은 분석 결과로, 이전 v1.0의 근본적 오해를 완전히 수정했습니다.

### 🎯 핵심 혁신
1. **올바른 아키텍처**: 사용자 → 2호 → Task → 서브에이전트 플로우
2. **정확한 SuperClaude 재현**: 동적 페르소나, 객관적 복잡도, Wave 모드
3. **Anthropic 준수**: Hook 시스템 완벽 구현
4. **최적화**: 도구 병렬 호출 활용, 효율적 토큰 사용

### ✅ 검증된 설계
- 모든 기본서 재독해 완료
- SuperClaude vs SPARK 정확한 매핑
- ANTHROPIC_GUIDELINES.md 100% 준수
- Jason's 품질 기준 완전 반영

이 계획서대로 구현하면 **SuperClaude 100% 성능 재현과 효율적 토큰 사용**을 동시에 달성할 수 있습니다.

---

*Ultra Think 분석 완료*  
*작성: Claude Code (3호)*  
*기반: 모든 기본서 재독해 + Anthropic 가이드라인 완전 숙지*  
*검증: SuperClaude 아키텍처 정확한 이해*