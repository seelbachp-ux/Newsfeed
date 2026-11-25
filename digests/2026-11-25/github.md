**sybil-solutions/skill-distill** — Turns a Claude Code or Codex session that went well into a skill that a cheaper open-weight model can follow to redo the task. The frontier model acts as teacher: it writes the skill and runs the student model in tmux on a fresh copy of the starting state. It then compares the result with the original, revises the skill at the first point where the student went wrong, and repeats until the outputs match. MIT license, about 750 stars, among the past week's top gainers.
*Why it's worth a look:* use it to hand routine tasks you repeat in the app repo, such as adding a new screen or a new data-model field, to a cheap local model.
Source: [GitHub](https://github.com/sybil-solutions/skill-distill)

**sous-labs/songe** — A background training engine for local models. It records how you use your agent, then in idle hours either folds your stated preferences into the model's instructions ("Quick Dream") or trains a small LoRA adapter ("Deep Dream"). It trains through MLX on Apple Silicon, has been tested end to end with LM Studio on macOS, installs via Homebrew, and keeps everything on the machine. Apache-2.0, about 740 stars in its first days.
*Why it's worth a look:* it is one of the few on-device fine-tuning tools built for Macs first, so your Mac could tune a local coding model while it sits idle.
Source: [GitHub](https://github.com/sous-labs/songe)

**cursor/plugins** — Cursor's official plugin specification and marketplace. Each plugin is a directory with a `plugin.json` manifest that bundles `SKILL.md` skills, `.mdc` rules and MCP server definitions. There are more than 100 plugins, covering developer tools, Google Workspace and Microsoft 365, payments and others. MIT license, about 19.3K stars, around 360 today.
*Why it's worth a look:* the format is close to Claude Code's plugins, so skills you write for one agent are getting easier to carry over to another.
Source: [GitHub](https://github.com/cursor/plugins)

**deterministic-machines/deslop-please** — A Rust linter based on *A Philosophy of Software Design*. It flags circular dependencies between modules, modules that depend on each other's internals, struct fields used from outside their type, and modules that expose many functions callers barely use. It comes with an `AGENTS.md` snippet so coding agents follow the same rules. MIT license, about 840 stars this week. Which languages it supports isn't documented; the examples are Rust.
*Why it's worth a look:* the rules are useful on their own as `AGENTS.md` guardrails against messy code structure, even if the tool can't parse Swift.
Source: [GitHub](https://github.com/deterministic-machines/deslop-please)

**elementalsouls/Claude-BugHunter** — A bundle of 84 Claude Code skills and 15 slash commands for authorised bug-bounty and red-team work. The skills are built from 681 publicly disclosed HackerOne reports and cover XSS, SSRF, IDOR, cloud IAM and more, with scope-check gates and Burp MCP integration. iOS is explicitly out of scope. Code is MIT and content is CC BY 4.0; about 21.8K stars, with around 1,800 today, the top gainer on GitHub.
*Why it's worth a look:* point the web skills at your own VPS backend before you retire it. Run them only against systems you own.
Source: [GitHub](https://github.com/elementalsouls/Claude-BugHunter)
