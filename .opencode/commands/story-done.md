---
description: "End-of-story completion review. Reads the story file, verifies each acceptance criterion against the implementation, checks for GDD/ADR deviations, prompts code review, updates story status to Complete, and surfaces the next ready story from the sprint."
---

<!-- GENERATED from .claude/skills/story-done/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `story-done` by calling the skill tool: skill({ name: "story-done" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[story-file-path] [--review full|lean|solo]`

Arguments supplied by the user: $ARGUMENTS