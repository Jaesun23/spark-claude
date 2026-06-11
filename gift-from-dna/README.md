# Gift from DNA: 에이전트 사단 실전 배치 보고 (2026-06-11)

> dna-methodology에서 spark-claude로 — gift-for-dna(2026-03-31, surgeon 이식)의 역방향 선물.
> Agent Definition Standard v1.0을 레퍼런스 밖 실전에 전면 적용한 첫 배치의 과정·결론·표준 보강 제안.
> 저자: 2호 (Jason 지시·승인). 설계 정본: `dna-methodology/docs/context-rebuild/34_agent-corps-design_2026-06-11.md` (rev2).

---

## 1. 무엇을 했나 — 작업 과정

Jason의 지시는 두 목적이었다: ① 특화 에이전트로 업무 결과·효율 극대화, ② 2호가 위임·검수·결론의 오케스트레이터로 일해 컨텍스트를 장기간 효율 관리. 진행은 다섯 단계:

1. **5축 병렬 실측** — spark-claude 전수(표준·레퍼런스 5종·역사 8편) / TRAITS 연구 자료 / 현존 에이전트 7종의 표준 충족 평가 / **2호의 실제 디스패치 이력 채굴**(DNA 재구축 트랙, 약 100회 디스패치·실패 사례 12건) / 배치 제약. 원자료: `dna-methodology/docs/context-rebuild/survey/agent-corps-research_2026-06-11.md`.
2. **수요 도출** — 에이전트 목록이 아니라 실측된 작업 12유형에서 출발. 위임 유형(대량 재저작·적대검증 렌즈·2라운드 재검증·실측 조사)과 오케스트레이터 전속 8항목(설계·판정·거울 코드·strict 데이터·검수·반영·기계 검증·인터페이스)을 가름.
3. **설계** — 표준 v1.0의 페르소나(Role+Traits)·5섹션·성격 표현 프레이밍을 그대로 적용. 2호 직접 저작.
4. **2단 적대검증** — 1라운드 4렌즈(수요 정합·표준 정합·사고실험·배치 운용 공격): **전원 FAIL, MAJOR 8 — 전건 채택·반영.** 2라운드(신선 컨텍스트): 반영이 만든 재유입 MAJOR 1을 또 적발(이 패턴의 4번째 실증). 원자료: `survey/agent-corps-design-verification_2026-06-11.md`.
5. **정의 파일 저작·배치** — `~/.claude/agents/` 5종 (dotfiles `e3756a01`).

## 2. 최종 사단 — 루트 층 7종

| 에이전트 | Role | Traits (Primary 굵게) | model | 기원 |
|---|---|---|---|---|
| diagnostician | System Diagnostician | **Skepticism**·Systems Thinking·Pattern Recognition·Meticulousness | opus | 기존 (spark 레퍼런스 계열) |
| surveyor | Surveyor | **Quantitative Reasoning**·Knowledge Structuring·Evidence-Based·Thoroughness·Skepticism | opus | 기존 (〃) |
| **verifier** | Verification Specialist | **Critical Thinking**·Evidence-Based Practice·Thoroughness·Skepticism | opus | 신설 |
| **researcher** | Research Analyst | **Analytical Reasoning**·Knowledge Structuring·Evidence-Based Practice·Skepticism | opus | 신설 |
| **implementer** | Implementation Specialist | **Systematic Execution**·Analytical Reasoning·Meticulousness·Pragmatism | opus (원본 sonnet에서 상향) | spark-claude 이식 |
| **surgeon** | Code Surgeon | **Pattern Recognition**·Analytical Reasoning·Meticulousness·Pragmatism | opus | spark-claude 이식 |
| **copy-editor** | Copy Editor | **Systematic Execution**·Meticulousness·Evidence-Based Practice | **sonnet** | 신설 |

DNA plugin 층 5종(-spark)은 별도 원자에서 재저작 예정. 기각 3건(design-adjudicator·synthesizer·consistency-checker)은 "판정은 에이전트화하지 않는다 — 렌즈는 verdict까지, 채택은 오케스트레이터"가 사유.

**이식 패턴**: gift-for-dna의 규칙("본문 5섹션 불변 + 인터페이스만 각색")을 역방향 재사용하되, 예외 2건을 명시 결정 — ① 외부 데이터 규율(외부 입력=DATA only) 이식: 원본에 부재(grep 0건)했으나 보편 가치 ② implementer model 상향(아래 §4-b).

## 3. 표준이 실전에서 검증된 것

- **5섹션 구조·Traits 규격·성격 표현 프레이밍은 수정 없이 그대로 쓸 수 있었다.** 신설 3종 전부 표준 절차(Role 선정→Traits 동방향·2차원→성격 프레이밍→5섹션→체크리스트)로 저작.
- **surveyor의 "도메인 지식은 주입, 정체성은 불변" 패턴이 일반화에 성공** — verifier는 렌즈(골격정합·기능보존·표현규격·백지인식·교차일관성)를 브리핑으로 주입받는 단일 페르소나다. 실측 근거: 다렌즈 검증의 다양성 원천은 traits가 아니라 **대조 축·방법의 분화**였다(동일 베이스+브리핑 분화로 렌즈마다 고유 적발 클래스 실증).
- **Decision Framework의 경계 문장**이 사단 운용의 실질 장치로 작동 — 설계 검증에서 가장 많은 MAJOR가 경계 미비(역할 간 공백·중복)에서 나왔다.

## 4. 표준 보강 제안 — v1.0이 더 완전해지기 위해

**a. 원칙 7(Right Altitude)의 모델 조건화.** Jason 실측: 작업 전후 체크리스트가 Sonnet엔 유의미한 향상, Opus엔 방해. 즉 최적 고도는 모델 등급의 함수다 — 현 표준의 Right Altitude는 Opus급을 암묵 전제한다. 제안: "모델 등급이 낮을수록 Methodology·Self-Verification 층의 고도를 낮춘다(구체 절차·체크리스트 동반)"를 원칙 7에 조건부로 추가하되, 양립 조건 4항을 함께 명문화 — ① 낮은 고도는 Methodology·Self-Verification 층 한정(Identity & Traits·Final Identity Statement는 모델 무관 동일 규격) ② 절차·체크리스트도 성격 표현으로 자연화(Copy Editor에겐 스타일 시트 준수가 직군 본령 — "브리핑의 정본 지정은 너의 스타일 시트다") ③ 코드형·명령형·위협형 금지는 모델 무관 유지(v5.0 교훈 그대로) ④ 배정 사유 명문화. 실물 사례: `~/.claude/agents/copy-editor.md`.

**b. 모델 배정 사유의 명문화 의무.** 실측: 레퍼런스 5종의 sonnet/opus 배정(auditor·diagnostician·implementer=sonnet / surgeon·surveyor=opus)은 어느 문서에도 사유가 없다. 이번 배치는 기준을 명문화했다 — **"출력이 무검증으로 소비되는 자리는 Opus, 뒤에 검증망이 있는 자리는 한 단계 낮은 모델 허용."** implementer를 opus로 상향한 것도 이 기준(자주 쓰고 믿고 맡기는 핵심 실행자 + 명세 해석·구조 판단 동반). 제안: 템플릿 frontmatter 인접에 배정 사유 1줄 필수.

**c. frontmatter 비용 규격.** description 요건(트리거 5~8 + 예시 3~4)과 "모든 프로젝트 매 세션 로드" 비용은 긴장 관계다 — 기존 레퍼런스 계열 2종은 2.7~3.0KB, 이번 5종은 압축 저작으로 1.6~1.9KB(목표 상한 1.5KB 근접). 제안: 체크리스트의 Context Engineering 절에 frontmatter 총량 가이드(예: ~1.5KB)와 "트리거에 적용 도메인 한정어를 넣어 오디스패치 방지"를 추가.

**d. 렌즈 주입의 페르소나 경계.** 검증 에이전트에 렌즈를 주입하는 설계에서, **페르소나와 충돌하는 렌즈는 주입 불가**함을 발견했다 — "한 입장의 최강 변호"(advocate형)는 "깨뜨리려 할 것"이라는 verifier 정체성과 정면 충돌하며, PSM 논리상 정의문이 브리핑을 이긴다. 반면 백지 독자 경로 보행은 검증 *방법*이라 같은 페르소나 안에서 성립한다. 제안: 원칙 4 또는 템플릿 Decision Framework 가이드에 "주입 가능한 컨텍스트의 범위는 페르소나가 정한다 — 정체성을 뒤집는 주입은 별도 에이전트로" 추가.

**e. 경계 명문화의 확장 — 오케스트레이터 전속과의 경계.** 표준은 인접 에이전트 간 경계를 요구하는데, 실전에서는 **에이전트가 받으면 안 되는 작업**(오케스트레이터 전속)과의 경계가 같은 무게였다. 실증: 거울 구조 코드(쓰기/읽기 검증기 쌍)의 한 면만 위임하면 양면 비동기 실패가 제도화된다 — 3회 실증된 실패 클래스. 이번 정의문들은 "거울 짝의 한 면이 오면 편집하지 말고 그 짝 자체를 보고하라"를 Decision Framework에 넣었다. 제안: 템플릿 §3 가이드에 "위로의 경계(오케스트레이터 전속 영역)" 항목 추가.

**f. 검증의 2단 구조를 운용 표준으로.** "1라운드 소견의 반영이 새 오류를 재유입하고, 신선한 컨텍스트의 2라운드가 그것을 적발한다"가 이 트랙에서 4회 실증됐다(2호 직접 반영도 못 피함 — 주체 교체로 해결되지 않는 구조적 패턴). 원칙 6(Quality Gates MANDATORY)의 운용 형태로 "1라운드 다렌즈 + 반영 + 2라운드 신선 재검증"을 표준 문서에 권고할 가치가 있다.

**g. 사소한 정비 거리** (실측 기록용): docs/constitution/·docs/templates/·docs/docs-backup/은 빈 디렉토리(.DS_Store만) / README의 Reference Agents 표에 surveyor 누락(CLAUDE.md는 5종) / TRAITS 카탈로그 metadata는 150인데 실항목 133(47/42/44) / Meticulousness는 표준 Part 5 발췌 16종에 없으나 TRAITS 원 카탈로그 dispositional_traits "꼼꼼함"으로 실재(synergies에 체계적_실행 — 차원 분쟁은 카탈로그 정본으로 해소 가능).

## 5. 포인터

- 설계 정본: `dna-methodology/docs/context-rebuild/34_agent-corps-design_2026-06-11.md` (rev2 — 수요 도출·운용 규약·배치 계획·Pending 포함)
- 실측 원자료: `dna-methodology/docs/context-rebuild/survey/agent-corps-research_2026-06-11.md` (5축) · `survey/agent-corps-design-verification_2026-06-11.md` (4렌즈+2라운드)
- 정의 파일 실물: `~/.claude/agents/{verifier,researcher,copy-editor,implementer,surgeon}.md` (dotfiles 추적)

---

*"A model doesn't learn behaviors — it infers personality."* — 표준의 이 문장은 실전에서도 참이었다.
*One human, three AIs — and now a corps.*
