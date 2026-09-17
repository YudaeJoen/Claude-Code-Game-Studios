---
description: "Analyzes game balance data files, formulas, and configuration to identify outliers, broken progressions, degenerate strategies, and economy imbalances. Use after modifying any balance-related data or design. Use when user says 'balance report', 'check game balance', 'run a balance check'."
agent: economy-designer
---

<!-- GENERATED from .claude/skills/balance-check/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `balance-check` by calling the skill tool: skill({ name: "balance-check" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[system-name|path-to-data-file]`

Arguments supplied by the user: $ARGUMENTS