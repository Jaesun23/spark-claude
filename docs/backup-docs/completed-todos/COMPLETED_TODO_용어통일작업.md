# Bootstrap → DNA 용어 통일 작업 지시서

> **작성일**: 2025-11-13
> **목적**: "Bootstrap" 용어를 "DNA 시스템"으로 통일 (142회)
> **범위**: 10개 파일

---

## 📊 파일별 작업량

```
00_CORE_METHODOLOGY.md:          74회 ⭐⭐⭐ (최우선!)
03G-00_adr_guide.md:              24회 ⭐⭐
00_FILE_NAMING_CONVENTION.md:    12회 ⭐
02G-00_structure_design_guide.md: 10회
08G-00_task_breakdown_guide.md:    9회
IMPLEMENTATION_CASES.md:           6회
06G-00_project_standards_guide.md: 3회
07G-00_blueprint_guide.md:         2회
01G-00_core_definition_guide.md:   1회
00_STAGE_STRUCTURE.md:             1회
-------------------------------------------
총 10개 파일, 142회
```

---

## 🔍 변경 패턴

### 패턴 1: Bootstrap ADR
```markdown
❌ Bootstrap ADR
✅ DNA 시스템 ADR
```

**위치 예시**:
- `docs/adr/bootstrap/` → `docs/adr/dna-systems/`
- "Bootstrap ADR (001-099)" → "DNA 시스템 ADR (001-011)"

### 패턴 2: Bootstrap 환경
```markdown
❌ Bootstrap 환경
✅ DNA 시스템 환경

❌ Bootstrap 기술 스택
✅ DNA 시스템 기술 스택

❌ Bootstrap 요소
✅ DNA 시스템 요소
```

### 패턴 3: Bootstrap vs 도메인
```markdown
❌ Bootstrap vs 도메인 구분
✅ DNA 시스템 vs 도메인 구분

❌ Bootstrap 범주
✅ DNA 시스템 범주
```

### 패턴 4: 문서 참조
```markdown
❌ 패밀리별 Bootstrap 요소 매트릭스
✅ 패밀리별 DNA 시스템 요소 매트릭스

❌ Bootstrap 단계
✅ DNA 시스템 단계
```

---

## 📋 파일별 작업 순서

### 우선순위 1: 00_CORE_METHODOLOGY.md (74회)

**작업**:
```bash
# 1. 파일 백업
cp 00_CORE_METHODOLOGY.md 00_CORE_METHODOLOGY.md.backup

# 2. 변경 (대소문자 모두)
sed -i '' 's/Bootstrap ADR/DNA 시스템 ADR/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/Bootstrap 환경/DNA 시스템 환경/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/Bootstrap 기술 스택/DNA 시스템 기술 스택/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/Bootstrap 요소/DNA 시스템 요소/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/Bootstrap 단계/DNA 시스템 단계/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/Bootstrap vs/DNA 시스템 vs/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/Bootstrap 범주/DNA 시스템 범주/g' 00_CORE_METHODOLOGY.md
sed -i '' 's/bootstrap/DNA 시스템/g' 00_CORE_METHODOLOGY.md

# 3. 검증
grep -i "bootstrap" 00_CORE_METHODOLOGY.md
# → 0개 나와야 함
```

**특별 주의**:
- "Bootstrap" 대문자 → "DNA 시스템"
- "bootstrap" 소문자 → "DNA 시스템"
- 문맥에 따라 "DNA 시스템" vs "DNA"만 사용할지 판단

---

### 우선순위 2: 03G-00_adr_guide.md (24회)

**작업**:
```bash
cp 03G-00_adr_guide.md 03G-00_adr_guide.md.backup
sed -i '' 's/Bootstrap ADR/DNA 시스템 ADR/g' 03G-00_adr_guide.md
sed -i '' 's/Bootstrap 기술 스택/DNA 시스템 기술 스택/g' 03G-00_adr_guide.md
sed -i '' 's/Bootstrap vs/DNA 시스템 vs/g' 03G-00_adr_guide.md
sed -i '' 's/Bootstrap:/DNA 시스템:/g' 03G-00_adr_guide.md
grep -i "bootstrap" 03G-00_adr_guide.md
```

**특별 주의**:
- 22줄: "확정된 Bootstrap 기술 스택" → "확정된 DNA 시스템 기술 스택"
- 섹션 제목: "Bootstrap ADR vs 도메인 ADR" → "DNA 시스템 ADR vs 도메인 ADR"

---

### 우선순위 3-10: 나머지 8개 파일

**일괄 작업 스크립트**:
```bash
#!/bin/bash

FILES=(
  "00_FILE_NAMING_CONVENTION.md"
  "02G-00_structure_design_guide.md"
  "08G-00_task_breakdown_guide.md"
  "IMPLEMENTATION_CASES.md"
  "06G-00_project_standards_guide.md"
  "07G-00_blueprint_guide.md"
  "01G-00_core_definition_guide.md"
  "00_STAGE_STRUCTURE.md"
)

for file in "${FILES[@]}"; do
  echo "Processing: $file"
  cp "$file" "${file}.backup"
  sed -i '' 's/Bootstrap ADR/DNA 시스템 ADR/g' "$file"
  sed -i '' 's/Bootstrap 환경/DNA 시스템 환경/g' "$file"
  sed -i '' 's/Bootstrap 기술 스택/DNA 시스템 기술 스택/g' "$file"
  sed -i '' 's/Bootstrap 요소/DNA 시스템 요소/g' "$file"
  sed -i '' 's/Bootstrap에/DNA 시스템에/g' "$file"
  sed -i '' 's/Bootstrap으로/DNA 시스템으로/g' "$file"
  sed -i '' 's/Bootstrap:/DNA 시스템:/g' "$file"
  sed -i '' 's/bootstrap/DNA 시스템/g' "$file"

  # 검증
  COUNT=$(grep -ic "bootstrap" "$file" || true)
  echo "  Remaining 'bootstrap': $COUNT"
done
```

---

## 🔍 특별 케이스

### Stage 2: 02G-00 (10회)
**위치**:
- 42줄: "패밀리별 Bootstrap 요소 매트릭스"
- 109줄: "Bootstrap 기술 스택"
- 117줄: "Bootstrap (A-C-A 패밀리 강제)"
- 기타 7곳

**주의**: "Stage 4-9: Bootstrap → Blueprint" → "Stage 4-9: DNA 시스템 → Blueprint"

### Stage 8: 08G-00 (9회)
**위치**:
- 110줄: "Bootstrap 환경 기반"
- 307줄: "# ✅ Bootstrap 환경 사용"
- 314줄: "import logging  # Bootstrap에 없음!"
- 기타 6곳

**주의**: 주석 내 "Bootstrap에 없음" → "DNA 시스템에 없음"

---

## ✅ 완료 기준

**각 파일별**:
```bash
grep -ic "bootstrap" <파일명>
# → 0 나와야 함
```

**전체 검증**:
```bash
grep -r -i "bootstrap" *.md | wc -l
# → 0 나와야 함
```

**수동 확인**:
- [ ] 00_CORE_METHODOLOGY.md: 74회 → 0회
- [ ] 03G-00_adr_guide.md: 24회 → 0회
- [ ] 나머지 8개 파일: 44회 → 0회
- [ ] 총계: 142회 → 0회

---

## 📝 작업 후 조치

1. **Git diff 확인**:
```bash
git diff 00_CORE_METHODOLOGY.md | head -50
```

2. **백업 파일 제거** (확인 후):
```bash
rm *.backup
```

3. **커밋**:
```bash
git add *.md
git commit -m "docs: Bootstrap → DNA 시스템 용어 통일 (142회)

✨ 용어 통일:
- Bootstrap → DNA 시스템 (일관성)
- 10개 파일, 142회 변경

📝 주요 변경:
- Bootstrap ADR → DNA 시스템 ADR
- Bootstrap 환경 → DNA 시스템 환경
- Bootstrap 기술 스택 → DNA 시스템 기술 스택

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

**예상 소요 시간**: 1-2시간
