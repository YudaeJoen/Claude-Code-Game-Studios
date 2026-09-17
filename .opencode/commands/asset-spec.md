---
description: "Generate per-asset visual specifications and AI generation prompts from GDDs, level docs, or character profiles. Produces structured spec files and updates the master asset manifest. Run after art bible and GDD/level design are approved, before production begins."
---

<!-- GENERATED from .claude/skills/asset-spec/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `asset-spec` by calling the skill tool: skill({ name: "asset-spec" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[system:<name> | level:<name> | character:<name>] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS