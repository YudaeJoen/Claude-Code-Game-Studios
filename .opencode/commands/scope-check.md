---
description: "Analyze a feature or sprint for scope creep by comparing current scope against the original plan. Flags additions, quantifies bloat, and recommends cuts. Use when user says 'any scope creep', 'scope review', 'are we staying in scope'."
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/scope-check/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `scope-check` by calling the skill tool: skill({ name: "scope-check" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[feature-name or sprint-N]`

Arguments supplied by the user: $ARGUMENTS