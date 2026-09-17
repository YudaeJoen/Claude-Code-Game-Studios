# OpenCode Adapter

Runs CCGS under [opencode](https://opencode.ai) alongside Claude Code, so the same
agents, skills, hooks, and quality gates work in either tool — and so agents can run
on GPT, Claude, or any other provider opencode supports.

**`.claude/` is the single source of truth.** `.opencode/` is generated from it. Never
hand-edit `.opencode/agents/`, `.opencode/commands/`, or `.opencode/ccgs-manifest.json`
— the next regeneration overwrites them.

## Usage

```bash
python3 tools/opencode/generate-adapter.py          # regenerate .opencode/
python3 tools/opencode/generate-adapter.py --check  # CI: fail if out of date
```

Run it after editing any agent, skill, or rule. Then **restart opencode** — config,
agents, and plugins are loaded once at startup and never hot-reloaded.

## Non-interactive `opencode run` stalls — use the TUI or desktop app for real work

Across ~40 non-interactive runs on this machine, `opencode run` repeatedly hung
*before* creating a session: the log ends at `message=init` (sometimes followed by
`cleanup prune=7.days`), no `session.created` event, no error, and the process sits
idle until killed. During a stall nothing happens locally — the sqlite DB and WAL do
not change, no git or child process exists, the plugin has already loaded.

What is **ruled out**, each by direct test: the project directory (the same directory
stalls and then works), the OpenCode desktop app (stalls with it fully quit and
nothing holding the DB), stale locks or git mirrors (none exist), auto-update
(`autoupdate: false` changes nothing), and the CCGS plugin (`--pure` runs stall or
succeed the same way as normal runs).

What is **observed**: trivial prompts such as `Reply with exactly: OK` succeed in
4-9 s almost every time, even when launched at the same moment as a run that stalls.
Runs that stall reliably are `opencode run --command <any>` (even a one-line command
file), `opencode run --agent <subagent-mode agent>`, a message that is a slash
command (`"/start"`), and prompts that tell the model to load a skill. Runs that
exercise tools (`bash`, `read`, `apply_patch`, Tavily search) succeeded at other
times, so the trigger is not simply "uses tools".

The interactive TUI and the desktop app are the supported way to use CCGS under
opencode; the non-interactive runner was only ever a test harness here. If you must
script `opencode run`, keep the prompt plain, avoid `--command` and `--agent`, and
kill-and-retry after 60 s without `session.created` (`CCGS_HOOK_DEBUG=1` shows it).

**Do not set `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` or `OPENCODE_DISABLE_CLAUDE_CODE`.**
Those switches (found in the binary) turn off the Claude-compatibility layer that
makes opencode read `CLAUDE.md` and `.claude/skills/`, which this adapter relies on.

## Running /start

```bash
cd ~/Projects/Claude-Code-Game-Studios
opencode          # TUI; or open the folder in the OpenCode desktop app
```

Then type `/start`. It is an interactive onboarding skill: it asks where you are
(no idea / vague concept / clear design / existing work) through the `question`
tool and routes you to the right workflow. If the TUI hangs on its start screen,
quit and reopen it once.

## Verified end to end (opencode 1.18.29-1.18.30, 2026-09-17)

A non-interactive session was driven through every hook path in an isolated copy of
this repository. All of the following fired and behaved as specified:

| Path | Evidence |
|---|---|
| Plugin loads from `.opencode/plugins/` | `[ccgs] plugin loaded` / `manifest: 49 agents, 11 rules` |
| 49 agents, 72 skills | `opencode agent list`, `opencode debug skill` |
| SessionStart → system prompt | `session-start.sh -> exit 0`, `detect-gaps.sh -> exit 0` |
| PreToolUse bash gate | `validate-commit.sh`, `validate-push.sh` ran on `git status` |
| PostToolUse edit gate | `validate-assets.sh`, `validate-skill-change.sh` ran on `apply_patch` |
| Path-scoped rules | `rule delivered: .claude/rules/gameplay-code.md for src/gameplay/ccgs_probe.gd` |
| Read-path denial | `read` of `.env.example` returned tool error `CCGS: reading .env.example is denied (secrets).`; fixture value not disclosed. (A plain `.env` prompt never reached the hook — the model refused on its own, so that run proved nothing.) |
| Stop | `session.idle` → `session-stop.sh -> exit 0` |
| Web search via Tavily MCP | `tavily_tavily_search -> completed`, real URL returned (13 s) |
| Per-agent MCP gating | primary-mode probes: `tavily_tavily_search: true` searched; `false` and `tavily_*: false` both got no search tool |

Not yet exercised at runtime: `maxTurns` (needs a subagent exceeding its cap),
PreCompact/PostCompact (needs a compaction), `log-agent*.sh` (needs a `task` call).
Their hook signatures come from the installed type definitions, and the glob matcher
they share is unit-verified against all 11 rule globs.

Reproduce with:

```bash
CCGS_HOOK_DEBUG=1 opencode run "Reply with exactly: OK" --format json --print-logs
```

`[ccgs]` lines on stderr show every event type, hook script exit code, and rule
delivery.

## Web search (Tavily MCP)

opencode has no built-in search tool, so `WebSearch` grants are served by Tavily's
hosted MCP endpoint, declared in `opencode.json`:

```json
"mcp": {
  "tavily": {
    "type": "remote",
    "url": "https://mcp.tavily.com/mcp/?tavilyApiKey={env:TAVILY_API_KEY}",
    "enabled": true
  }
}
```

The key lives only in the environment. Put it in your shell profile:

```bash
echo 'export TAVILY_API_KEY="tvly-..."' >> ~/.zshrc && source ~/.zshrc
```

`{env:}` substitution works inside `url` (verified: `opencode mcp list` shows
`tavily connected`). Without the variable the server fails to connect and the 9
research agents simply have no search tool; nothing else breaks. Tavily's free tier
is 1,000 credits a month with no card, which covers this project's usage (Brave
dropped its free tier in February 2026).

The remote endpoint matters here: this machine has no `node`, `npx`, or `bun` on
PATH, so an npx-launched local MCP server could not run.

## Mixing providers

`model-map.json` controls which model each agent gets:

```json
{
  "tiers": {
    "haiku":  "openai/gpt-5.5",
    "sonnet": "openai/gpt-5.6-sol",
    "opus":   "openai/gpt-6-astra"
  },
  "overrides": { "technical-director": "openai/gpt-6-astra" }
}
```

`tiers` maps CCGS's `model:` alias; `overrides` pins one agent by name and wins over
its tier. The project default (`model` / `small_model`) lives in `opencode.json` and is
kept consistent by hand. Regenerate after editing either.

**`opencode models` lists more than your login can use.** This machine's only
credential is a ChatGPT-account Codex OAuth, and the API rejects most of the listed
models with `"not supported when using Codex with a ChatGPT account"`. Probed:

| Model | Result |
|---|---|
| `gpt-5.5`, `gpt-5.6-sol`, `gpt-6-astra` | respond |
| `gpt-5.3-codex-spark`, `gpt-5.4`, `gpt-5.4-mini` | rejected |

There is no lightweight model available under this login, so the haiku tier maps to
the cheapest working model rather than a true mini. `gpt-5.6-luna` / `-terra` are the
same generation as `-sol` and were not probed. Re-probe after changing credentials:

```bash
opencode run "Reply OK" --model openai/<id> --format json
```

To run CCGS agents on Claude under opencode, authenticate Anthropic first
(`opencode providers`) — no `anthropic/*` model resolves otherwise.

## What each piece maps to

| CCGS | opencode | Notes |
|------|----------|-------|
| `CLAUDE.md` | read directly | opencode falls back to `CLAUDE.md` when no `AGENTS.md` exists. Do **not** add an `AGENTS.md` — it would shadow `CLAUDE.md` and split the source of truth. |
| `.claude/skills/*/SKILL.md` | read directly | opencode natively scans `.claude/skills/`. Nothing is copied. |
| `.claude/agents/*.md` | `.opencode/agents/*.md` | Generated. Frontmatter rewritten; body verbatim. |
| slash commands | `.opencode/commands/*.md` | Generated wrappers that call `skill({ name })`. |
| `.claude/hooks/*.sh` | `.opencode/plugins/ccgs-hooks.ts` | Scripts run **unmodified**; the plugin feeds them Claude Code's stdin JSON and honours exit 2 = block. |
| `CLAUDE.md` `@` imports | `instructions` in `opencode.json` | opencode does not expand `@` imports. |
| `src/CLAUDE.md`, `design/CLAUDE.md`, `docs/CLAUDE.md` | `instructions` in `opencode.json` | Claude Code loads these when working inside that directory; opencode only walks *up* from cwd, so they are always-on here (~540 words). |
| `settings.json` permissions | `permission` in `opencode.json` | All 21 rules ported. `Read(**/.env*)` is enforced by the plugin. The redirect pattern `*>.env*` is carried over verbatim but unverified against opencode's command parser. |
| `.claude/rules/*.md` | plugin, `tool.execute.after` | Delivered on first edit of a governed path, once per rule per session. Not in `instructions` — that would defeat the scoping. |
| `maxTurns` | plugin, `tool.execute.before` | Per-agent ceiling from the manifest. |
| `WebSearch` | Tavily remote MCP, `tavily_tavily_search` | 9 research agents get it; every other agent gets `false`. |

### Hook-by-hook

| Claude Code | opencode hook | Scripts |
|---|---|---|
| SessionStart | `experimental.chat.system.transform` (cached per session) | session-start, detect-gaps |
| PreToolUse (Bash) | `tool.execute.before`, tool `bash` | validate-commit, validate-push |
| PostToolUse (Write/Edit) | `tool.execute.after`, tool `apply_patch` | validate-assets, validate-skill-change |
| SubagentStart / Stop | `tool.execute.before` / `after`, tool `task` | log-agent, log-agent-stop |
| PreCompact | `experimental.session.compacting` | pre-compact |
| PostCompact | event `session.compacted` → next system prompt | post-compact |
| Stop | event `session.idle` | session-stop |
| Notification | — (Windows toast only) | notify |

## Things that fail silently — check these first

Everything below was hit while building this. None produced an error message.

- **`opencode run --agent <name>` hangs when `<name>` is a `mode: subagent` agent.**
  It stops after `init` with no session, no error, forever. Every generated CCGS
  agent is a subagent, so drive them through the primary agent's `task` tool or
  make a throwaway `mode: primary` probe. This is the one reproducible stall.
- **MCP tool names are `<server>_<tool>` with hyphens turned into underscores.**
  Tavily's `tavily-search` becomes `tavily_tavily_search`. Read the name from a
  live `tool_use` event; do not derive it from the server's docs.
- **`opencode debug agent` never shows MCP keys** in the resolved `tools` map, in
  exact or wildcard form — but the map is honoured at runtime (verified with
  probes). Absence in debug output is not evidence the grant was dropped.
- **`opencode mcp list` prints the resolved URL, API key included.** Do not run it
  where the terminal is shared or logged.
- **Every export of a plugin module is invoked as a plugin.** Exporting a helper
  function makes opencode call it with `PluginInput` and log
  `failed to load plugin … x.replace is not a function`. Keep helpers un-exported.
- **`BunShellPromise` has no `.stdin()` method.** `stdin` is a read-only stream. Feed a
  script by piping: `` $`printf '%s' ${json} | bash ${path}` ``. The wrong call throws,
  the fail-soft wrapper swallows it, and every hook becomes a no-op.
- **`tool.execute.before` and `.after` are not symmetric.** Before: args on `output`.
  After: args on `input`; `output` holds `title`, `output`, `metadata`.
- **The tool registry is not what the docs list.** This build registers
  `read glob grep bash task webfetch todowrite skill question apply_patch` — no
  `write`, `edit`, `lsp`, `websearch`. Unknown keys in an agent's `tools:` are dropped
  without warning. `Write`/`Edit` map to `apply_patch`; `WebSearch` maps to the
  Tavily MCP tool (see below).
- **Duplicate keys in `tools:` discard the whole agent file** and fall back to
  defaults, silently. Confirm with `opencode debug agent <name>`.
- **`apply_patch` reports touched files in `output.metadata.files[]`**
  (`filePath`, `relativePath`). Use that, not the patch text.
- Directory names are plural (`agents/`, `commands/`, `plugins/`). `opencode agent
  create` writes the singular form, which is never loaded
  ([#14410](https://github.com/anomalyco/opencode/issues/14410)).

Authoritative hook signatures: `~/.opencode/node_modules/@opencode-ai/plugin/dist/`
(`index.d.ts`, `tool.d.ts`, `shell.d.ts`, `tui.d.ts`). Read those before the docs.

## Still open

**Per-skill model tiers.** 11 skills declare `model: haiku` / `opus`. opencode reads
only `name`, `description`, `license`, `compatibility`, `metadata` from `SKILL.md`. The
generated command wrapper restores the tier for slash-command invocation, not for
direct `skill` tool loads. Closing it means patching skill loading in core — the one
genuine fork candidate.

**Status line.** `@opencode-ai/plugin/tui` exposes routes and keymaps, so a TUI plugin
is feasible; it is a rewrite, not a port. Unbuilt.

**`memory` (17 agents), `skills` (6), `isolation` (1).** No counterpart; dropped.

**`allowed-tools` on skills.** Same frontmatter limitation; tool limits come from the
agent definition.

## Sources

- [Agents](https://opencode.ai/docs/agents/) · [Commands](https://opencode.ai/docs/commands/) · [Rules](https://opencode.ai/docs/rules/) · [Skills](https://opencode.ai/docs/skills/)
- [Plugins](https://opencode.ai/docs/plugins/) · [Custom tools](https://opencode.ai/docs/custom-tools/) · [Permissions](https://opencode.ai/docs/permissions/) · [Config](https://opencode.ai/docs/config/) · [Tools](https://opencode.ai/docs/tools/)
