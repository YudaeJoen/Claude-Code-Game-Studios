---
description: "Run the critical path smoke test gate before QA hand-off. Executes the automated test suite, verifies core functionality, and produces a PASS/FAIL report. Run after a sprint's stories are implemented and before manual QA begins. A failed smoke check means the build is not ready for QA."
---

<!-- GENERATED from .claude/skills/smoke-check/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `smoke-check` by calling the skill tool: skill({ name: "smoke-check" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[sprint | quick | --platform pc|console|mobile|all]`

Arguments supplied by the user: $ARGUMENTS