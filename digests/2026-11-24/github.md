**mjmirza/app-store-compliance** — A playbook of 124 App Store and Google Play rejection patterns, each with a fix. It also includes a guard script that scans a project and returns BLOCKED, CLEAR or NOT CHECKED, covering privacy manifests, permission strings, in-app purchase rules, account deletion and demo accounts. It can be installed as a Claude Code, Codex or Cursor hook that blocks `fastlane` or `xcrun altool` submits when it finds a critical problem, and adds an `/app-store-audit` command. About 761 stars today. The license is custom: free for individuals and companies under $20M in revenue.
*Why it's worth a look:* run it before submitting the SwiftUI rewrite for the first time, since HealthKit permission strings and the account-deletion rule are classic reasons for rejection.
Source: [GitHub](https://github.com/mjmirza/app-store-compliance)

**driceroland/Search** — A small, quiet macOS browser: about 42K lines of Swift using SwiftUI, AppKit and WKWebView, with no third-party dependencies. It has ad blocking through `WKContentRuleList`, Chrome extensions through `WKWebExtension`, keychain password storage and split view. MIT license, about 920 new stars this week, the top Swift gainer.
*Why it's worth a look:* it is a sizeable SwiftUI app with no dependencies, useful for seeing how SwiftUI and AppKit are combined in a real codebase.
Source: [GitHub](https://github.com/driceroland/Search)

**HKUDS/CLI-Anything** — Generates a command-line interface, plus a SKILL.md file, for existing software so agents can drive it. The CLI works the real app rather than reimplementing it, and comes with a REPL and JSON output. It also runs CLI-Hub, a registry of CLIs built by the community. Works with Claude Code, Codex, Cursor, Copilot CLI and others. Apache-2.0, about 790 stars today.
*Why it's worth a look:* it is a fast way to give your coding agent control of tools that only have a GUI or a messy interface.
Source: [GitHub](https://github.com/HKUDS/CLI-Anything)

**Tracer-Cloud/opensre** — A self-hosted CLI agent that reads a failed CI run, separates flaky-infrastructure failures from real code failures, and pushes a fix to the PR branch for review. It can mask identifiers before calling an LLM and post summaries to Slack or Telegram. Public alpha, Apache-2.0, about 440 stars today.
*Why it's worth a look:* it is an open-source alternative to paid "fix my CI" bots, which helps once Xcode Cloud or GitHub Actions builds start failing at night.
Source: [GitHub](https://github.com/Tracer-Cloud/opensre)

**google-labs-code/stitch-skills** — Official Agent Skills for Google's Stitch design tool, used through its MCP server. They generate and edit screens, extract a DESIGN.md file from existing code, and manage design systems. They work in Claude Code, Codex, Gemini CLI and Cursor. Apache-2.0, about 420 stars today. The build skills output React and React Native only, not SwiftUI.
*Why it's worth a look:* the design-system and DESIGN.md skills are still useful for keeping an agent consistent when it builds SwiftUI screens.
Source: [GitHub](https://github.com/google-labs-code/stitch-skills)
