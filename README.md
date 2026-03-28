# spark-claude

**Agent Definition Standard** — 실전, 이론, 과학이 수렴한 에이전트 정의 표준

---

## What is this?

AI 에이전트를 정의할 때 따라야 할 표준 규격과, 이를 적용한 소프트웨어 개발용
레퍼런스 에이전트 모음입니다.

이 표준은 세 가지 독립적 소스에서 수렴한 결과입니다:
- **SPARK** — 5개 프로젝트의 실전 경험에서 도출된 설계 원칙
- **TRAITS** — 150개 특성 카탈로그와 인지 부하 이론 연구
- **Anthropic Research** — 6편의 페르소나 신경과학 연구

## Quick Start

### 기존 에이전트 사용
`agents/` 디렉토리에서 필요한 에이전트 정의를 복사하여 프로젝트에 적용합니다.

### 새 에이전트 만들기
[AGENT_DEFINITION_STANDARD.md](AGENT_DEFINITION_STANDARD.md)의 가이드를 따릅니다.

## Reference Agents

| Agent | Purpose |
|-------|---------|
| [implementer](agents/implementer.md) | 구현 전문가 — feature implementation, testing, bug fixes |
| [diagnostician](agents/diagnostician.md) | 시스템 진단 전문가 — analysis, debugging, root cause investigation |
| [auditor](agents/auditor.md) | 품질 감사 전문가 — code review, compliance audit, quality gates |

## Documentation

| Document | Description |
|----------|-------------|
| [Agent Definition Standard](AGENT_DEFINITION_STANDARD.md) | 에이전트 정의 표준 규격 (7대 원칙 + 템플릿 + 체크리스트) |
| [TRAITS Research](docs/TRAITS_RESEARCH.md) | 특성 기반 동적 페르소나 시스템 연구 요약 |
| [Anthropic Persona Research](docs/ANTHROPIC_PERSONA_RESEARCH.md) | Anthropic 페르소나 연구 6편 요약 |
| [History](docs/history/) | SuperClaude v1.0 → Standard v5.0 발전사 |

## License

MIT — see [LICENSE](LICENSE)

---

> *Built with passion: One human, three AIs, infinite possibilities.*
> *— Jason, 1호, 2호, 제이*
