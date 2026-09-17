---
description: "Creates a structured bug report from a description, or analyzes code to identify potential bugs. Ensures every bug report has full reproduction steps, severity assessment, and context."
---

<!-- GENERATED from .claude/skills/bug-report/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `bug-report` by calling the skill tool: skill({ name: "bug-report" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[description] | analyze [path-to-file]`

Arguments supplied by the user: $ARGUMENTS