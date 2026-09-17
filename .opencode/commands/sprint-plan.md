---
description: "Generates a new sprint plan or updates an existing one based on the current milestone, completed work, and available capacity. Pulls context from production documents and design backlogs."
---

<!-- GENERATED from .claude/skills/sprint-plan/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `sprint-plan` by calling the skill tool: skill({ name: "sprint-plan" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[new|update|status] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS