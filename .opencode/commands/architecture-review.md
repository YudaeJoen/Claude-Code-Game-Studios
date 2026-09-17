---
description: "Validates completeness and consistency of the project architecture against all GDDs. Builds a traceability matrix mapping every GDD technical requirement to ADRs, identifies coverage gaps, detects cross-ADR conflicts, verifies engine compatibility consistency across all decisions, and produces a PASS/CONCERNS/FAIL verdict. The architecture equivalent of /design-review."
agent: technical-director
model: openai/gpt-6-astra
---

<!-- GENERATED from .claude/skills/architecture-review/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `architecture-review` by calling the skill tool: skill({ name: "architecture-review" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[focus: full | coverage | consistency | engine | single-gdd path/to/gdd.md]`

Arguments supplied by the user: $ARGUMENTS