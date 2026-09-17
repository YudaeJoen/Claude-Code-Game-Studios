---
description: "Fast sprint status check. Reads the current sprint plan, scans story files for status, and produces a concise progress snapshot with burndown assessment and emerging risks. Run at any time during a sprint for quick situational awareness. Use when user asks 'how is the sprint going', 'sprint update', 'show sprint progress'."
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/sprint-status/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `sprint-status` by calling the skill tool: skill({ name: "sprint-status" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[sprint-number or blank for current]`

Arguments supplied by the user: $ARGUMENTS