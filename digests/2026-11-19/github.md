**apple/coreai-models** — Apple's recipes for converting Hugging Face models to Core AI's `.aimodel` format, plus a Swift package for running them in iOS and macOS apps. It also ships agent skills for Claude Code, Codex and Gemini CLI. Requires iOS/macOS 27 and Xcode 27.
*Why it matters:* This is the official route to adding on-device models to a SwiftUI app, such as smart workout summaries with no server.
Source: [GitHub](https://github.com/apple/coreai-models)

**NVIDIA/SkillEvaluator** — A framework for testing agent skills and plugins: static quality and security checks, a check that predicts whether an agent will load a skill, duplicate detection, and live runs with and without the skill. Includes CI templates. Supports Claude Code, Codex, OpenCode and Copilot CLI.
*Why it matters:* If you write your own agent skills, this tells you whether they actually change what the agent does.
Source: [GitHub](https://github.com/NVIDIA/SkillEvaluator)

**mvanhorn/last30days-skill** — An agent skill that researches a topic across Reddit, X, YouTube, HN, Polymarket and the web, then summarizes the results. It gained over 1,000 stars in a day.
*Why it matters:* A ready-made pattern for multi-source research agents, close to the kind of digest pipeline you already run.
Source: [GitHub](https://github.com/mvanhorn/last30days-skill)

**apple/container** — Apple's tool for running Linux containers in lightweight VMs on Apple silicon. It is the top trending Swift repo this week (about 800 new stars).
*Why it matters:* It's a native, Docker-free way to run your old VPS backend locally while you migrate off it.
Source: [GitHub](https://github.com/apple/container)

**HKUDS/CLI-Anything** — Generates command-line interfaces for existing software so AI agents can drive it. Around 60K stars and still climbing.
*Why it matters:* For an agent, a CLI is often more reliable than screen-scraping or a custom MCP server, which makes it worth trying for your own dev tooling.
Source: [GitHub](https://github.com/HKUDS/CLI-Anything)
