---
description: "Read all open bugs in production/qa/bugs/, re-evaluate priority vs. severity, assign to sprints, surface systemic trends, and produce a triage report. Run at sprint start or when the bug count grows enough to need re-prioritization."
---

<!-- GENERATED from .claude/skills/bug-triage/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `bug-triage` by calling the skill tool: skill({ name: "bug-triage" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[sprint | full | trend]`

Arguments supplied by the user: $ARGUMENTS