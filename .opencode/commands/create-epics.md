---
description: "Translate approved GDDs + architecture into epics — one epic per architectural module. Defines scope, governing ADRs, engine risk, and untraced requirements. Does NOT break into stories — run /create-stories [epic-slug] after each epic is created."
agent: technical-director
---

<!-- GENERATED from .claude/skills/create-epics/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `create-epics` by calling the skill tool: skill({ name: "create-epics" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[system-name | layer: foundation|core|feature|presentation | all] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS