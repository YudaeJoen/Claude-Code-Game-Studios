---
description: "Auto-generates a changelog from git commits, sprint data, and design documents. Produces both internal and player-facing versions."
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/changelog/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `changelog` by calling the skill tool: skill({ name: "changelog" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[version|sprint-number]`

Arguments supplied by the user: $ARGUMENTS