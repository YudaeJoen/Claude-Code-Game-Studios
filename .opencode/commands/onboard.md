---
description: "Generates a contextual onboarding document for a new contributor or agent joining the project. Summarizes project state, architecture, conventions, and current priorities relevant to the specified role or area."
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/onboard/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `onboard` by calling the skill tool: skill({ name: "onboard" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[role|area]`

Arguments supplied by the user: $ARGUMENTS