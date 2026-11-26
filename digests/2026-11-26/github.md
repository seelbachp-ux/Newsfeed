**apple/coreai-models** — Apple's official recipes for exporting models to the new Core AI `.aimodel` format. It includes Python building blocks for writing models in PyTorch, a Swift package of runtime utilities for using the models in an app, command-line tools for running them on a Mac, and agent skills. It requires iOS/macOS 27 and Xcode 27. BSD-3 license, about 2.4K stars, and on this week's Swift trending list.
*Why it's worth a look:* this is the reference for running on-device models in a SwiftUI app, for example rep counting or workout summaries without a server.
Source: [GitHub](https://github.com/apple/coreai-models)

**osaurus-ai/osaurus** — An open-source agent harness for macOS written in Swift, with no Electron. It runs local models through MLX (Gemma, Qwen, GPT-OSS, Llama), Apple's Foundation Models, or cloud APIs. It also offers sub-agents, scheduled workflows and memory, and a Linux VM sandbox for running code. It works as both an MCP server and an MCP client, so you can expose its tools to Claude Code. MIT license, about 8.2K stars.
*Why it's worth a look:* it is a real-world SwiftUI codebase built around local LLMs, and also a usable local agent.
Source: [GitHub](https://github.com/osaurus-ai/osaurus)

**backnotprop/plannotator** — A local, browser-based tool for annotating agent plans, specs, markdown and code diffs and sending your feedback back to the agent. It also has an "Inbox" window where agents can ask you questions. It works with Claude Code, Codex, Gemini CLI, Copilot CLI, OpenCode and others. Licensed Apache-2.0 or MIT, about 15.1K stars, with around 1.8K this week.
*Why it's worth a look:* it gives you a proper review step for an agent's plan before it touches your Xcode project.
Source: [GitHub](https://github.com/backnotprop/plannotator)

**n8n-io/nod** — n8n's open-source personal agent. It runs on your machine with the model of your choice, handles web and app tasks across Gmail, Calendar, Slack and Notion, and asks before it acts. It keeps credentials in a vault the model never sees, logs every action, and sets monthly spending caps for API models. It runs on macOS 14+, with Windows and Linux in preview. Apache-2.0, about 3.6K stars, with around 1K this week. It is a research preview, and usage-data sharing is on by default.
*Why it's worth a look:* use it to hand off the admin side of running a solo app, such as support email, App Store reminders and invoices.
Source: [GitHub](https://github.com/n8n-io/nod)

**google-labs-code/stitch-skills** — Google's library of agent skills for the Stitch design MCP server. It has plugins for creating designs, turning designs into code and generating `DESIGN.md` files, and works with Claude Code, Codex, Gemini CLI, Cursor and others. Apache-2.0, about 13.1K stars, with around 2.6K this week. Code generation targets React and React Native, not SwiftUI.
*Why it's worth a look:* the `DESIGN.md` workflow is useful for giving an agent your app's visual rules, even if you write the SwiftUI yourself.
Source: [GitHub](https://github.com/google-labs-code/stitch-skills)
