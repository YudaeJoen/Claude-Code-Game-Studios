---
description: "Scan all GDDs against the entity registry to detect cross-document inconsistencies: same entity with different stats, same item with different values, same formula with different variables. Grep-first approach — reads registry then targets only conflicting GDD sections rather than full document reads."
---

<!-- GENERATED from .claude/skills/consistency-check/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `consistency-check` by calling the skill tool: skill({ name: "consistency-check" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[full | since-last-review | entity:<name> | item:<name>]`

Arguments supplied by the user: $ARGUMENTS