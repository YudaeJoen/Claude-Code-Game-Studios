---
description: "Validate readiness to advance between development phases. Produces a PASS/CONCERNS/FAIL verdict with specific blockers and required artifacts. Use when user says 'are we ready to move to X', 'can we advance to production', 'check if we can start the next phase', 'pass the gate'."
model: openai/gpt-6-astra
---

<!-- GENERATED from .claude/skills/gate-check/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `gate-check` by calling the skill tool: skill({ name: "gate-check" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[target-phase: systems-design | technical-setup | pre-production | production | polish | release] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS