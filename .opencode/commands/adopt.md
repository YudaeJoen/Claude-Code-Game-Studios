---
description: "Brownfield onboarding — audits existing project artifacts for template format compliance (not just existence), classifies gaps by impact, and produces a numbered migration plan. Run this when joining an in-progress project or upgrading from an older template version. Distinct from /project-stage-detect (which checks what exists) — this checks whether what exists will actually work with the template's skills."
agent: technical-director
---

<!-- GENERATED from .claude/skills/adopt/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `adopt` by calling the skill tool: skill({ name: "adopt" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[focus: full | gdds | adrs | stories | infra]`

Arguments supplied by the user: $ARGUMENTS