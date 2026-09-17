---
description: "Configure the project's game engine and version. Pins the engine in CLAUDE.md, detects knowledge gaps, and populates engine reference docs via WebSearch when the version is beyond the LLM's training data."
---

<!-- GENERATED from .claude/skills/setup-engine/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `setup-engine` by calling the skill tool: skill({ name: "setup-engine" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[engine] | [engine version] | refresh | upgrade [old-version] [new-version] | no args for guided selection`

Arguments supplied by the user: $ARGUMENTS