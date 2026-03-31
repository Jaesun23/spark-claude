# Gift for DNA Methodology: surgeon-spark

> From spark-claude to dna-methodology — a new agent for the family.

---

## What is this?

**surgeon-spark** is the 4th reference agent created in the spark-claude Agent Definition Standard project. This directory contains a DNA-adapted version, ready to be integrated into the dna-methodology plugin.

## Agent Summary

| Item | Detail |
|------|--------|
| **Name** | `surgeon-spark` |
| **Role** | Code Surgeon — code modernization, dead code removal, complexity reduction |
| **Model** | opus |
| **Primary Trait** | Pattern Recognition |
| **Supporting Traits** | Analytical Reasoning, Meticulousness, Pragmatism |

## How it fits in DNA

The DNA methodology currently has 5 agents:

| Agent | Domain | Relationship to Surgeon |
|-------|--------|------------------------|
| `diagnostician` | System diagnosis | Diagnostician finds what's broken; surgeon improves what's working but stale |
| `implementer-spark` | Feature implementation | Implementer builds new; surgeon modernizes existing |
| `audit-spark` | Quality audit | Auditor evaluates against criteria; surgeon fixes the code |
| `security-spark` | Security verification | Security finds vulnerabilities; surgeon can modernize insecure patterns |
| `red-team-spark` | Adversarial testing | Red-team attacks; surgeon strengthens through cleanup |

**surgeon-spark fills the gap**: no existing DNA agent takes working-but-outdated code and transforms it into clean, modern, efficient code while preserving behavior.

## Integration Steps

1. Copy `surgeon-spark.md` to `agents/` in dna-methodology
2. Update `agents/README.md` to add surgeon-spark to the agent table
3. Update `CLAUDE.md` Section 9 (Quick Reference) to include the new agent
4. Bump plugin version if appropriate

## Design Lineage

- Follows the **Agent Definition Standard v1.0** (5-section structure)
- Traits validated through convergent discovery + thought experiment simulation
- Directional coherence verified: all 4 traits converge toward "precise craftsman" cluster
- Boundary with other agents explicitly defined in Decision Framework

## Task Dispatch Format (DNA style)

```
Task("surgeon-spark", "Purpose: [what to improve]. Scope: Read+Edit: [paths]. Done Criteria: [verification conditions].")
```

---

*Created: 2026-03-31*
*Origin: spark-claude Agent Definition Standard project*
*By: Jason & 2ho*
