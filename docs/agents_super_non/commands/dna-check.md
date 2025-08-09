---
description: "🧬 V5 DNA 시스템 전체 건강도 검사"
tools: ["bash", "read"]
---

# 🧬 DNA v3.5 시스템 건강도 검사

Memory-One-Spark V5의 모든 DNA 시스템을 종합 검사하세요.

## 실행할 검사들

### 1. 전체 품질 검사
```bash
echo "🧬 DNA v3.5 전체 품질 검사 시작..."
python scripts/quality_check.py
```

### 2. 아키텍처 건강도
```bash
echo "🏗️ DNA 아키텍처 검증..."
uv run lint-imports --config .import-linter.toml
```

### 3. 8개 DNA 시스템 개별 점검

#### 🏗️ Skeletal System (골격계)
프로젝트 구조와 Clean Architecture 준수를 확인하세요.

#### 🧠 Nervous System (신경계)
로깅 시스템이 Infrastructure가 아닌 Nervous에 위치하는지 확인하세요.

#### 🛡️ Immune System (면역계)
보안 검사를 실행하고 품질 규칙 위반을 확인하세요.

#### 🔔 Endocrine System (내분비계)
설정 파일 무결성과 환경 변수를 검증하세요.

#### 🩸 Circulatory System (순환계)
데이터 플로우와 의존성 주입 패턴을 확인하세요.

#### 👁️ Sensory System (감각계)
MCP 인터페이스와 API 엔드포인트를 검증하세요.

#### 🍽️ Digestive System (소화계)
데이터 처리 파이프라인과 Vector/NLP/CRAG 시스템을 확인하세요.

#### 🔄 Reproductive System (생식계)
빌드 설정과 배포 준비 상태를 검증하세요.

### 4. V4 문제 방지 검증

#### 순환참조 방지
```bash
echo "🔄 V4 순환참조 방지 검증..."
if uv run lint-imports --config .import-linter.toml | grep -q "violations"; then
    echo "❌ 아키텍처 위반 발견!"
else
    echo "✅ 아키텍처 정상"
fi
```

#### 로깅 시스템 위치 확인
```bash
echo "📝 로깅 시스템 위치 검증..."
if find src/infrastructure -name "*log*" -type f | grep -q .; then
    echo "❌ 로깅이 Infrastructure에 잘못 위치!"
else
    echo "✅ 로깅이 Nervous System에 올바르게 위치"
fi
```

### 5. 결과 보고
모든 검사 결과를 종합하여 보고하세요:
- ✅ GREEN: 모든 시스템 정상
- ⚠️ YELLOW: 경고사항 있음
- ❌ RED: 문제 발견, 즉시 수정 필요
