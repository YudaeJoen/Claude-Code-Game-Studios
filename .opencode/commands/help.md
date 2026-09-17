---
description: "Analyzes what is done and the users query and offers advice on what to do next. Use if user says what should I do next or what do I do now or I'm stuck or I don't know what to do"
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/help/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `help` by calling the skill tool: skill({ name: "help" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[optional: what you just finished, e.g. 'finished design-review' or 'stuck on ADRs']`

Arguments supplied by the user: $ARGUMENTS