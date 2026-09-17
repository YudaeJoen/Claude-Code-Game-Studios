---
description: "Audit the game for security vulnerabilities: save tampering, cheat vectors, network exploits, data exposure, and input validation gaps. Produces a prioritised security report with remediation guidance. Run before any public release or multiplayer launch."
agent: security-engineer
---

<!-- GENERATED from .claude/skills/security-audit/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `security-audit` by calling the skill tool: skill({ name: "security-audit" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[full | network | save | input | quick]`

Arguments supplied by the user: $ARGUMENTS