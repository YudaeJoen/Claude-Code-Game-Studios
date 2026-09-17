---
description: "Break a single epic into implementable story files. Reads the epic, its GDD, governing ADRs, and control manifest. Each story embeds its GDD requirement TR-ID, ADR guidance, acceptance criteria, story type, and test evidence path. Run after /create-epics for each epic."
agent: lead-programmer
---

<!-- GENERATED from .claude/skills/create-stories/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `create-stories` by calling the skill tool: skill({ name: "create-stories" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[epic-slug | epic-path] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS