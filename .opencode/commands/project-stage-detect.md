---
description: "Automatically analyze project state, detect stage, identify gaps, and recommend next steps based on existing artifacts. Use when user asks 'where are we in development', 'what stage are we in', 'full project audit'."
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/project-stage-detect/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `project-stage-detect` by calling the skill tool: skill({ name: "project-stage-detect" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[optional: role filter like 'programmer' or 'designer']`

Arguments supplied by the user: $ARGUMENTS