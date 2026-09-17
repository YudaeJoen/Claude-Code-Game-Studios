---
description: "Generate a soak test protocol for extended play sessions. Defines what to observe, measure, and log during long play sessions to surface slow leaks, fatigue effects, and edge cases that only appear after sustained play. Primarily used in Polish and Release phases."
---

<!-- GENERATED from .claude/skills/soak-test/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `soak-test` by calling the skill tool: skill({ name: "soak-test" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[duration: 30m | 1h | 2h | 4h] [focus: memory | stability | balance | all]`

Arguments supplied by the user: $ARGUMENTS