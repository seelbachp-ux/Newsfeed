"""
config.py — everything you'll want to tweak lives here.

This file is intentionally "just settings + prompts." The actual agent logic
is in digest.py. Keeping them apart means you can change *what* the agent
researches (here) without touching *how* it runs (there).
"""

# ── Model ────────────────────────────────────────────────────────────────
# Sonnet is far cheaper than Opus ($3/$15 vs $5/$25 per 1M tokens) and plenty
# smart for summarizing news. For rock-bottom cost use "claude-haiku-4-5"
# ($1/$5); switch back to "claude-opus-4-8" if you ever want maximum quality.
MODEL = "claude-sonnet-4-6"

# ── Cost controls ────────────────────────────────────────────────────────
# Cap how many web searches Claude may run per beat (each costs ~$0.01).
MAX_SEARCHES_PER_BEAT = 4
# Effort controls how much Claude thinks / how many tools it uses.
# "low" is cheapest and fine for summaries; "medium"/"high" cost more.
EFFORT = "low"

# Prices per 1M tokens — used ONLY to print an estimated cost after each run.
PRICING = {
    "claude-opus-4-8":   {"in": 5.0, "out": 25.0},
    "claude-sonnet-4-6": {"in": 3.0, "out": 15.0},
    "claude-haiku-4-5":  {"in": 1.0, "out": 5.0},
}
WEB_SEARCH_COST = 0.01  # ~$10 per 1,000 searches

# ── Where the digest lands ───────────────────────────────────────────────
import os

# Files are first generated here — a plain folder the scheduler can always
# write to (no macOS privacy restrictions apply to it).
LOCAL_DIR = os.path.expanduser("~/ai-digest/output")

# ...then copied into this iCloud Drive folder, which syncs to your iPhone's
# Files app. iCloud is privacy-protected, so the SCHEDULED runs need Python
# to have "Full Disk Access" (one-time macOS setting) for this copy to work.
ICLOUD_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/AI Digest"
)

# ── Voice for the audio version ──────────────────────────────────────────
# "" = use the macOS system default voice (always works).
# To hear the options:   say -v '?'
# Nicer voices (e.g. "Zoe (Premium)") can be downloaded in
# System Settings → Accessibility → Spoken Content → System Voice.
VOICE = ""  # e.g. "Samantha" or "Daniel" once you've confirmed it's installed

# ── Who this digest is for ───────────────────────────────────────────────
# Injected into every beat so Claude knows what "relevant to you" means.
# Edit this as your focus shifts — it's the single most powerful knob here.
PROFILE = """
The reader is an indie developer currently rebuilding a workout-tracking app
as a native iOS app in SwiftUI (migrating away from a PWA/VPS setup). They
care about: Swift / SwiftUI, native iOS, AI agents and agent tooling, and
solo/indie-developer workflows. Skip anything not relevant to those interests.
"""

# ── System prompt: the agent's standing instructions ─────────────────────
SYSTEM_PROMPT = f"""
You are a sharp, skeptical research assistant producing a short daily briefing.

{PROFILE}

Rules for every item you report:
- Only include genuinely RECENT items (roughly the last 7 days). If you can't
  confirm something is recent, leave it out.
- Format each item as:
    **Headline** — one or two plain sentences on what it is.
    *Why it matters:* one short sentence.
    Source: a markdown link to the primary source.
- Rank by genuine significance, newest/most important first.
- Be concise. No hype, no filler, no "in today's fast-moving world" intros.
- If you genuinely find nothing noteworthy for a section, say so in one line.
Write in clean Markdown. Do not add a top-level title — the script adds that.
"""

# ── The beats: one research task per section of the digest ───────────────
# Each beat is just a name + a prompt. Adding a beat later = copy a dict,
# change the prompt. That's the whole "add a topic" workflow.
BEATS = [
    {
        "key": "ai",
        "title": "🤖 Latest in AI",
        "prompt": (
            "Search the web for the most important AI developments from the "
            "past week: new model releases, major company announcements, "
            "notable new tools, interesting startups/funding, and emerging "
            "trends. Give me the top 5–7."
        ),
    },
    {
        "key": "github",
        "title": "🐙 GitHub & open source",
        "prompt": (
            "Search for currently trending GitHub repositories and notable "
            "new open-source projects from the past week that are relevant "
            "to my coding journey (Swift/SwiftUI, native iOS, AI agent "
            "tooling, indie-dev workflows). Give me the top 5 with a one-line "
            "note on why each is worth a look."
        ),
    },
]
