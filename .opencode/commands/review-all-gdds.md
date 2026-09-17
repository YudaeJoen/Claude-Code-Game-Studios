---
description: "Holistic cross-GDD consistency and game design review. Reads all system GDDs simultaneously and checks for contradictions between them, stale references, ownership conflicts, formula incompatibilities, and game design theory violations (dominant strategies, economic imbalance, cognitive overload, pillar drift). Run after all MVP GDDs are written, before architecture begins."
model: openai/gpt-6-astra
---

<!-- GENERATED from .claude/skills/review-all-gdds/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `review-all-gdds` by calling the skill tool: skill({ name: "review-all-gdds" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[focus: full | consistency | design-theory | since-last-review]`

Arguments supplied by the user: $ARGUMENTS