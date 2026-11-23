**apple/coreai-models** — Apple's official repo for its Core AI framework: recipes that convert open Hugging Face models to Core AI format, a Swift package for running them on iOS and macOS, and agent skills for Claude Code, Codex and Gemini CLI. It needs iOS/macOS 27 and Xcode 27 and is BSD-3 licensed.
*Why it's worth a look:* this is the supported way to ship on-device models in a SwiftUI app, for example to summarise workouts or suggest the next session locally.
Source: [GitHub](https://github.com/apple/coreai-models)

**osaurus-ai/osaurus** — A native Swift agent harness for Apple Silicon Macs. It provides memory, tools, skills, scheduled automations and an orchestrator agent that hands work to sub-agents. It runs local MLX models and Apple's Foundation Models, works with cloud models too, and is both an MCP server and an MCP client. MIT license.
*Why it's worth a look:* it is a real-world SwiftUI codebase built around agents, and also a fully local agent you can run next to Xcode.
Source: [GitHub](https://github.com/osaurus-ai/osaurus)

**backnotprop/plannotator** — A local browser interface for reviewing coding agents' plans and diffs. You annotate lines, approve or reject, and the structured feedback goes back to the agent session. It works with Claude Code, Codex, Gemini CLI, OpenCode and others, and was one of the top TypeScript gainers this week (~2.8K stars). Apache-2.0/MIT.
*Why it's worth a look:* it makes plan review before the agent writes code much easier, which matters when an agent is writing most of an app rewrite.
Source: [GitHub](https://github.com/backnotprop/plannotator)

**alibaba/open-code-review** — An `ocr` CLI that sends Git diffs or whole files to an LLM agent that can read and search the codebase, then returns line-level review comments. It runs in GitHub Actions or GitLab CI, or as a skill inside Claude Code, Codex or Cursor, and works with OpenAI- or Anthropic-compatible endpoints. Apache-2.0, ~3.7K stars this week.
*Why it's worth a look:* it gives a solo developer an automated second reviewer on every pull request, at no cost beyond tokens.
Source: [GitHub](https://github.com/alibaba/open-code-review)

**apple/container** — Apple's Swift tool for running Linux containers in lightweight VMs, tuned for Apple Silicon, again among the top Swift repos this week (~550 new stars).
*Why it's worth a look:* you could run the old PWA's backend or a sandbox for agents locally without Docker Desktop while you migrate off the VPS.
Source: [GitHub](https://github.com/apple/container)
