---
description: "Guided, section-by-section authoring of the master architecture document for the game. Reads all GDDs, the systems index, existing ADRs, and the engine reference library to produce a complete architecture blueprint before any code is written. Engine-version-aware: flags knowledge gaps and validates decisions against the pinned engine version."
agent: technical-director
---

<!-- GENERATED from .claude/skills/create-architecture/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `create-architecture` by calling the skill tool: skill({ name: "create-architecture" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[focus-area: full | layers | data-flow | api-boundaries | adr-audit] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS