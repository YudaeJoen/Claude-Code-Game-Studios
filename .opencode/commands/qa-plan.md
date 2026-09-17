---
description: "Generate a QA test plan for a sprint or feature. Reads GDDs and story files, classifies stories by test type (Logic/Integration/Visual/UI), and produces a structured test plan covering automated tests required, manual test cases, smoke test scope, and playtest sign-off requirements. Run before sprint begins or when starting a major feature."
agent: qa-lead
---

<!-- GENERATED from .claude/skills/qa-plan/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `qa-plan` by calling the skill tool: skill({ name: "qa-plan" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[sprint | feature: system-name | story: path]`

Arguments supplied by the user: $ARGUMENTS