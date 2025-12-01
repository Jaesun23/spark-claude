# 📋 체크리스트 전달 프로토콜 가이드

**작성자**: 2호  
**버전**: 1.0  
**작성일**: 2025-09-08

## 🎯 체크리스트의 역할

체크리스트는 **에이전트의 완전한 작업 명세서**입니다. 에이전트는 2호의 컨텍스트를 공유하지 않으므로, 체크리스트만으로 독립적으로 완벽한 작업을 수행할 수 있어야 합니다.

## 📝 체크리스트 전달 템플릿

### 1. 단일 에이전트 호출

```python
Task("implementer-spark", """
작업: [작업명]
체크리스트 위치: /docs/blueprints/checklists/[체크리스트파일명].md

필수 준수사항:
1. 체크리스트의 9단계를 모두 읽고 완전히 따를 것
2. ShellCheck 0 violations 달성 (SC1091, SC2154 제외)
3. 품질 기준 미달 시 스스로 수정 후 재검증
4. 결과를 ~/.claude/workflows/current_task.json에 기록

추가 강조사항:
- [특별히 강조할 사항]
- [이전 실패에서 배운 주의사항]
""")
```

### 2. 팀 에이전트 병렬 호출 (multi-implement)

```python
# Phase 1: Implementation (ONE MESSAGE에 모든 Task)
Task("team1-implementer-spark", """
작업: AKL-02 load_mcp_keys.sh 개선
체크리스트 위치: /docs/blueprints/checklists/Checklist_AKL-02_load_mcp_keys개선.md

필수 준수사항:
1. 체크리스트의 9단계를 완전히 따를 것
2. ShellCheck 0 violations 달성 - 절대 타협 없음!
3. 결과를 team1_current_task.json에 기록 (READ & WRITE)
4. 재시도 메커니즘 구현 필수
""")

Task("team2-implementer-spark", """
작업: AKL-04 mcp-wrapper.sh 복구  
체크리스트 위치: /docs/blueprints/checklists/Checklist_AKL-04_mcp_wrapper복구.md

필수 준수사항:
1. 체크리스트의 9단계를 완전히 따를 것
2. ShellCheck 0 violations 달성 - 절대 타협 없음!
3. 결과를 team2_current_task.json에 기록 (READ & WRITE)
4. 환경변수 브리지 10개 모두 구현
""")
```

## 🔍 체크리스트 품질 판단 기준

### 완전한 체크리스트의 조건
- ✅ 9단계 구조를 따름
- ✅ 각 단계별 구체적 명령어 포함
- ✅ 검증 기준이 명확하고 측정 가능
- ✅ 보안 원칙과 품질 기준 명시
- ✅ 자주 하는 실수와 해결책 포함
- ✅ 코드 예시나 템플릿 제공

### 불완전한 체크리스트 보완 방법
```python
# 체크리스트가 불완전할 때 2호가 추가 지시
additional_emphasis = """
특별 주의사항:
- API 키는 절대 하드코딩하지 말 것
- 모든 함수에 에러 처리 추가
- 로깅은 5단계 레벨로 구현
- 테스트 커버리지 95% 이상 달성
"""
```

## 📊 품질 검증 후 재작업 지시

### Phase 후 품질 검증
```python
# Phase 1 완료 후
json_data = read_json("team1_current_task.json")

if json_data['quality']['violations'] > 0:
    # 구체적인 위반사항과 함께 재작업 지시
    Task("team1-implementer-spark", f"""
    품질 기준 미달! 다음을 반드시 수정:
    
    ShellCheck violations: {json_data['quality']['shellcheck_errors']}
    - 현재: {json_data['quality']['violations']} violations
    - 목표: 0 violations
    
    체크리스트 Step 7-9를 다시 확인하고 수정하세요.
    특히 SC2086 (unquoted variables) 주의!
    """)
```

## 🎮 2호의 판단 포인트

### 언제 추가 지시를 해야 하는가?

1. **체크리스트만으로 충분한 경우**
   - 체크리스트가 완전하고 상세함
   - 이전에 성공 경험이 있는 작업
   - 단순하고 명확한 작업

2. **추가 지시가 필요한 경우**
   - 체크리스트에 없는 새로운 요구사항
   - 이전 실패에서 배운 교훈 강조
   - 특정 품질 기준 강화 필요
   - 보안이나 성능 관련 특별 주의

### 재작업 지시 전략

```python
class RetryStrategy:
    def decide_retry(self, agent_type: str, failure_count: int):
        if agent_type == "implementer":
            if failure_count < 3:
                return "구체적 수정사항과 함께 재시도"
            else:
                return "2호가 직접 수정"
        
        elif agent_type == "tester":
            if failure_count < 2:
                return "커버리지 목표와 함께 재시도"
            else:
                return "최소 요구사항으로 타협"
        
        elif agent_type == "qc-spark":
            # 품질 전문가는 성공할 때까지
            return "계속 재시도"
```

## 📋 체크리스트 전달 체크포인트

### 전달 전 확인사항
- [ ] 체크리스트 파일이 실제로 존재하는가?
- [ ] 경로가 정확한가?
- [ ] 9단계 구조를 따르는가?
- [ ] ShellCheck 품질 기준이 명시되었는가?
- [ ] JSON 파일 기록 지시가 포함되었는가?

### 전달 시 포함사항
- [ ] 작업명과 체크리스트 경로
- [ ] 필수 준수사항 4가지
- [ ] 추가 강조사항 (필요시)
- [ ] JSON 파일명 (팀 작업시)

### 전달 후 검증
- [ ] 에이전트가 체크리스트를 읽었는가?
- [ ] JSON이 업데이트되었는가?
- [ ] 품질 기준을 충족했는가?
- [ ] 재작업이 필요한가?

## 💡 Best Practices

1. **명확한 경로 제공**
   ```python
   # GOOD
   체크리스트 위치: /docs/blueprints/checklists/Checklist_AKL-02.md
   
   # BAD
   체크리스트: AKL-02를 참고하세요
   ```

2. **품질 기준 강조**
   ```python
   # GOOD
   ShellCheck 0 violations 달성 - 절대 타협 없음!
   
   # BAD
   품질 기준을 지켜주세요
   ```

3. **JSON 역할 명시**
   ```python
   # GOOD
   결과를 team1_current_task.json에 기록 (READ & WRITE)
   
   # BAD
   JSON 파일 확인
   ```

4. **구체적 재작업 지시**
   ```python
   # GOOD
   SC2086 오류 3개 수정: 변수를 큰따옴표로 감싸세요
   
   # BAD
   ShellCheck 오류를 수정하세요
   ```

## 🏆 성공 사례

```python
# 완벽한 체크리스트 전달 예시
Task("team1-implementer-spark", """
작업: API Key Lifecycle 시스템 구현
체크리스트 위치: /docs/blueprints/checklists/Checklist_AKL-02_load_mcp_keys개선.md

필수 준수사항:
1. 체크리스트의 9단계를 모두 읽고 완전히 따를 것
2. ShellCheck 0 violations 달성 (SC1091, SC2154 제외 - 문서화 필수)
3. 결과를 team1_current_task.json에 기록 (READ & WRITE)
4. 품질 기준 미달 시 스스로 수정 후 재검증

특별 강조사항:
- Service Account 토큰은 절대 하드코딩 금지
- 3회 재시도 메커니즘 필수 구현
- 모든 API 키는 마스킹 처리
- 성능 목표: 5초 이내 완료

이전 실패 경험:
- launchctl 명령어 권한 문제 주의
- 1Password CLI v2.30+ 버전 확인
""")

# 결과: 한 번에 성공, ShellCheck 0 violations 달성
```

---

**Remember**: 체크리스트는 에이전트의 유일한 가이드입니다. 완전하고 명확하게 전달하세요!