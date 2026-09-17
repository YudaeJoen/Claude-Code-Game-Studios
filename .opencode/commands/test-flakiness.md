---
description: "Detect non-deterministic (flaky) tests by reading CI run logs or test result history. Aggregates pass rates per test, identifies intermittent failures, recommends quarantine or fix, and maintains a flaky test registry. Best run during Polish phase or after multiple CI runs."
---

<!-- GENERATED from .claude/skills/test-flakiness/SKILL.md — do not edit. Run tools/opencode/generate-adapter.py -->

Load the CCGS skill `test-flakiness` by calling the skill tool: skill({ name: "test-flakiness" })

Then follow that skill's instructions exactly, start to finish. It is authoritative over any default approach you would otherwise take.

Expected arguments: `[ci-log-path | scan | registry]`

Arguments supplied by the user: $ARGUMENTS