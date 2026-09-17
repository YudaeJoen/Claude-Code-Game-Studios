---
description: "Generate player-facing patch notes from git history, sprint data, and internal changelogs. Translates developer language into clear, engaging player communication."
agent: community-manager
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/patch-notes/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `patch-notes` by calling the skill tool: skill({ name: "patch-notes" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[version] [--style brief|detailed|full]`

Arguments supplied by the user: $ARGUMENTS