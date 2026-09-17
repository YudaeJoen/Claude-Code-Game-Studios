#!/usr/bin/env python3
"""Generate the OpenCode adapter from the canonical .claude/ definitions.

.claude/ is the single source of truth. This script derives .opencode/ from it,
so the two never need to be maintained by hand. Re-run after editing any agent,
skill, or hook.

Usage:
    python3 tools/opencode/generate-adapter.py          # write files
    python3 tools/opencode/generate-adapter.py --check  # report drift, write nothing
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / ".claude"
OPENCODE = ROOT / ".opencode"
MODEL_MAP = json.loads((Path(__file__).parent / "model-map.json").read_text())

# The tool registry actually resolved by opencode 1.18.29. Verify against your
# version with:  opencode debug agent <name>  — keys not in the registry are
# silently dropped, which is how WebSearch grants went missing before.
# ("invalid" also appears in resolved output; it is internal, so we never emit it.)
ALL_TOOLS = [
    "read", "glob", "grep", "bash", "task",
    "webfetch", "todowrite", "skill", "question", "apply_patch",
]

# Claude Code tool name -> opencode tool name.
#   Write/Edit  -> apply_patch : this build has no separate write/edit tool.
#   WebSearch   -> webfetch    : DOWNGRADE. No search tool exists in this build,
#                                so the agent can fetch a known URL but cannot
#                                discover pages. Add "websearch" here if your
#                                version registers one.
TOOL_MAP = {
    "Read": "read",
    "Glob": "glob",
    "Grep": "grep",
    "Write": "apply_patch",
    "Edit": "apply_patch",
    "Bash": "bash",
    "Task": "task",
    "WebFetch": "webfetch",
    "WebSearch": "webfetch",
}

# Grants that are a downgrade rather than a faithful mapping, reported per run.
DOWNGRADED = {"WebSearch": "webfetch (fetch-only; no search)"}

# Always granted regardless of the Claude-side list:
#   skill    - CCGS is skill-driven; every agent must be able to load one.
#   question - the collaboration protocol requires agents to ask before writing.
ALWAYS_ON = ["skill", "question"]

# Frontmatter keys with no opencode counterpart. Dropped, and reported.
UNPORTABLE = ["memory", "skills", "isolation"]

FM_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def parse_frontmatter(text):
    """Return (dict, body). Only the leading --- block counts; horizontal rules
    later in the document are body content, not frontmatter."""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm, body = {}, m.group(2)
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip() != line:
            continue  # skip blanks and nested/indented values
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip('"')
    return fm, body


def resolve_model(name, tier):
    """Per-agent override beats tier mapping. Returns None when no tier declared."""
    if name in MODEL_MAP["overrides"]:
        return MODEL_MAP["overrides"][name]
    return MODEL_MAP["tiers"].get(tier)


def yaml_escape(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_rules():
    """Read .claude/rules/*.md and return [{file, paths[], body}] for the plugin.
    opencode has no path-scoped rule mechanism, so the plugin re-implements it."""
    rules = []
    for path in sorted((CLAUDE / "rules").glob("*.md")):
        text = path.read_text()
        m = FM_RE.match(text)
        if not m:
            continue
        globs = re.findall(r'^\s*-\s*"?([^"\n]+?)"?\s*$', m.group(1), re.M)
        if not globs:
            continue
        rules.append({
            "file": str(path.relative_to(ROOT)),
            "paths": globs,
            "body": m.group(2).strip(),
        })
    return rules


def build_agent(path, report):
    fm, body = parse_frontmatter(path.read_text())
    name = fm.get("name", path.stem)

    granted = set()
    for raw in (fm.get("tools") or "").split(","):
        raw = raw.strip()
        if not raw:
            continue
        if raw in TOOL_MAP:
            granted.add(TOOL_MAP[raw])
            if raw in DOWNGRADED:
                report.setdefault("downgraded", {}).setdefault(raw, []).append(name)
        else:
            report.setdefault("unknown_tools", set()).add(raw)

    for key in UNPORTABLE:
        if key in fm:
            report.setdefault("dropped_fields", {}).setdefault(key, []).append(name)
    # maxTurns has no native counterpart but the plugin enforces it, so carry the
    # value through the manifest rather than losing it.
    try:
        report.setdefault("max_turns", {})[name] = int(fm.get("maxTurns", 0)) or None
    except ValueError:
        pass

    lines = ["---", f"description: {yaml_escape(fm.get('description', ''))}", "mode: subagent"]
    model = resolve_model(name, fm.get("model", ""))
    if model:
        lines.append(f"model: {model}")
    granted.update(ALWAYS_ON)
    lines.append("tools:")
    for tool in ALL_TOOLS:  # ALL_TOOLS is the full key set — emit each key exactly
        lines.append(f"  {tool}: {'true' if tool in granted else 'false'}")
    lines.append("---")
    lines.append("")
    lines.append(f"<!-- GENERATED from .claude/agents/{path.name} — do not edit."
                 f" Run tools/opencode/generate-adapter.py -->")
    lines.append(body.lstrip("\n"))
    return name, "\n".join(lines)


def build_command(path, report):
    """A command is a thin wrapper: opencode reads .claude/skills/ natively, so the
    skill body stays the single source of truth and the command only routes to it."""
    fm, _ = parse_frontmatter(path.read_text())
    name = fm.get("name", path.parent.name)

    lines = ["---", f"description: {yaml_escape(fm.get('description', ''))}"]
    if fm.get("agent"):
        lines.append(f"agent: {fm['agent']}")
    model = resolve_model(name, fm.get("model", ""))
    if model:
        lines.append(f"model: {model}")
    lines.append("---")
    lines.append("")
    lines.append(f"<!-- GENERATED from .claude/skills/{name}/SKILL.md — do not edit."
                 f" Run tools/opencode/generate-adapter.py -->")
    lines.append("")
    hint = fm.get("argument-hint", "")
    lines.append(f'Load the CCGS skill `{name}` by calling the skill tool: '
                 f'skill({{ name: "{name}" }})')
    lines.append("")
    lines.append("Then follow that skill's instructions exactly, start to finish. It is "
                 "authoritative over any default approach you would otherwise take.")
    lines.append("")
    if hint:
        lines.append(f"Expected arguments: `{hint}`")
        lines.append("")
    lines.append("Arguments supplied by the user: $ARGUMENTS")

    if fm.get("allowed-tools"):
        report.setdefault("allowed_tools_lost", []).append(name)
    return name, "\n".join(lines)


def main():
    check = "--check" in sys.argv
    report, written = {}, []

    agents = sorted((CLAUDE / "agents").glob("*.md"))
    skills = sorted((CLAUDE / "skills").glob("*/SKILL.md"))

    outputs = {}
    for p in agents:
        name, content = build_agent(p, report)
        outputs[OPENCODE / "agents" / f"{name}.md"] = content
    for p in skills:
        name, content = build_command(p, report)
        outputs[OPENCODE / "commands" / f"{name}.md"] = content

    manifest = {
        "_generated_by": "tools/opencode/generate-adapter.py",
        "agents": {n: {"maxTurns": t} for n, t in sorted(report.get("max_turns", {}).items()) if t},
        "rules": parse_rules(),
    }
    outputs[OPENCODE / "ccgs-manifest.json"] = json.dumps(manifest, indent=2) + "\n"

    drift = []
    for dest, content in outputs.items():
        if not dest.exists() or dest.read_text() != content:
            drift.append(dest.relative_to(ROOT))
        if not check:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            written.append(dest)

    print(f"agents:   {len(agents)}")
    print(f"commands: {len(skills)}")
    if check:
        print(f"\ndrift: {len(drift)} file(s) out of date"
              + ("" if not drift else "\n  " + "\n  ".join(str(d) for d in drift[:10])))
        return 1 if drift else 0
    print(f"written:  {len(written)} files under .opencode/")

    if report.get("dropped_fields"):
        print("\nDropped — no opencode counterpart:")
        for key, names in sorted(report["dropped_fields"].items()):
            print(f"  {key}: {len(names)} agent(s) — {', '.join(sorted(names)[:4])}"
                  + (" ..." if len(names) > 4 else ""))
    if report.get("downgraded"):
        print("\nDowngraded grants:")
        for src, names in sorted(report["downgraded"].items()):
            print(f"  {src} -> {DOWNGRADED[src]} — {len(names)} agent(s)")
    if report.get("unknown_tools"):
        print(f"\nUnmapped tools: {', '.join(sorted(report['unknown_tools']))}")
    if report.get("allowed_tools_lost"):
        print(f"\nallowed-tools not enforceable on {len(report['allowed_tools_lost'])} "
              f"command(s) — opencode ignores that field on skills; "
              f"tool limits come from the agent instead.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
