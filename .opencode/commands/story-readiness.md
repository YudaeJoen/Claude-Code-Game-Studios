---
description: "Validate that a story file is implementation-ready. Checks for embedded GDD requirements, ADR references, engine notes, clear acceptance criteria, and no open design questions. Produces READY / NEEDS WORK / BLOCKED verdict with specific gaps. Use when user says 'is this story ready', 'can I start on this story', 'is story X ready to implement'."
model: openai/gpt-5.5
---

<!-- GENERATED from .claude/skills/story-readiness/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `story-readiness` by calling the skill tool: skill({ name: "story-readiness" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[story-file-path or 'all' or 'sprint']`

Arguments supplied by the user: $ARGUMENTS