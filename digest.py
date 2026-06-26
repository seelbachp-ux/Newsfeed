"""
digest.py — the agent.

The whole thing is the classic agent loop you learned about:
    1. Give Claude a goal (a "beat" prompt).
    2. Give it a tool (web search).
    3. Claude searches, reads, and writes a section.
    4. We collect every section, save it, and turn it into audio.

Run it with:   python digest.py
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta

import anthropic
from dotenv import load_dotenv

import config

load_dotenv()  # reads ANTHROPIC_API_KEY from a .env file if present


# ── Step 1: ask Claude to research one beat ──────────────────────────────
def coverage_sentence(today=None):
    """Describe the date range this run should cover.

    Schedule is Mon/Wed/Fri, and each run covers everything since the previous
    run, so nothing is missed despite skipping Tue/Thu:
      Monday    → back to Friday  (sweeps the weekend)
      Wednesday → back to Monday  (picks up Tuesday)
      Friday    → back to Wednesday (picks up Thursday)
    """
    today = today or date.today()
    days_back = {0: 3, 2: 2, 4: 2}.get(today.weekday(), 2)  # Mon=0..Sun=6
    since = today - timedelta(days=days_back)
    return (
        f"COVERAGE WINDOW: only include items published from "
        f"{since:%A %B %d} through {today:%A %B %d} — i.e. everything new since "
        f"the previous brief. Ignore anything older; it was already covered."
    )


def run_beat(client, beat, system):
    """Run a single research beat. Returns (section_text, usage_totals)."""
    print(f"  → researching: {beat['title']} ...", flush=True)

    messages = [{"role": "user", "content": beat["prompt"]}]
    totals = {"in": 0, "out": 0, "searches": 0}

    # Server-side web search: Claude runs the search/read loop on Anthropic's
    # side. Occasionally it hits an internal step limit and returns
    # "pause_turn" — we just re-send to let it continue.
    while True:
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=8000,
            system=system,
            thinking={"type": "adaptive"},
            output_config={"effort": config.EFFORT},  # "low" = cheaper
            tools=[{
                # Standard web search (no code-execution sandbox) — reliable.
                # The newer "..._20260209" variant adds code-based result
                # filtering that can fail mid-run with a container_id error.
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": config.MAX_SEARCHES_PER_BEAT,  # cap search cost
            }],
            messages=messages,
        )

        # Tally token + search usage so we can estimate the cost.
        u = response.usage
        totals["in"] += getattr(u, "input_tokens", 0) or 0
        totals["out"] += getattr(u, "output_tokens", 0) or 0
        stu = getattr(u, "server_tool_use", None)
        if stu:
            totals["searches"] += getattr(stu, "web_search_requests", 0) or 0

        if response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            continue
        break

    # The response is a list of blocks (thinking, tool calls, text...).
    # We only want the final written text.
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    return text, totals


# ── Step 2: stitch the sections into one digest ──────────────────────────
def print_cost(t):
    """Estimate and print what this run cost, from the tallied usage."""
    price = config.PRICING.get(config.MODEL, {"in": 0, "out": 0})
    cost = (
        t["in"] / 1_000_000 * price["in"]
        + t["out"] / 1_000_000 * price["out"]
        + t["searches"] * config.WEB_SEARCH_COST
    )
    print(f"\n💸 Estimated cost this run: ${cost:.3f}")
    print(
        f"   ({t['in']:,} input + {t['out']:,} output tokens, "
        f"{t['searches']} web searches, model {config.MODEL})"
    )


def build_digest():
    client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY from the env
    today = date.today().isoformat()

    # Build the system prompt once, with the date range this run should cover.
    system = config.SYSTEM_PROMPT + "\n\n" + coverage_sentence()

    grand = {"in": 0, "out": 0, "searches": 0}
    parts = [f"# Daily Digest — {today}\n"]
    for beat in config.BEATS:
        section, totals = run_beat(client, beat, system)
        for k in grand:
            grand[k] += totals[k]
        parts.append(f"## {beat['title']}\n\n{section}\n")

    print_cost(grand)
    return today, "\n".join(parts)


# ── Step 3a: save the Markdown to the local folder ───────────────────────
def write_markdown(today, text):
    os.makedirs(config.LOCAL_DIR, exist_ok=True)
    path = os.path.join(config.LOCAL_DIR, f"digest-{today}.md")
    with open(path, "w") as f:
        f.write(text)
    return path


# ── Step 3b: make an audio version you can play in the car ───────────────
def markdown_to_speech_text(text):
    """Strip Markdown so the text reads naturally aloud (and skip raw URLs)."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # [label](url) -> label
    text = re.sub(r"https?://\S+", "", text)               # drop bare URLs
    text = re.sub(r"[#*`>_]", "", text)                    # drop markdown symbols
    text = re.sub(r"\n{3,}", "\n\n", text)                 # tidy blank lines
    return text.strip()


def make_audio(today, text):
    os.makedirs(config.LOCAL_DIR, exist_ok=True)
    speech = markdown_to_speech_text(text)
    aiff = os.path.join(config.LOCAL_DIR, f"digest-{today}.aiff")
    m4a = os.path.join(config.LOCAL_DIR, f"digest-{today}.m4a")

    say_cmd = ["say", "-o", aiff]
    if config.VOICE:
        say_cmd += ["-v", config.VOICE]
    say_cmd += [speech]
    subprocess.run(say_cmd, check=True)

    # afconvert (built into macOS) shrinks the big AIFF into a compact m4a.
    try:
        subprocess.run(
            ["afconvert", aiff, m4a, "-f", "m4af", "-d", "aac"], check=True
        )
        os.remove(aiff)
        return m4a
    except (subprocess.CalledProcessError, FileNotFoundError):
        return aiff  # fall back to the AIFF if conversion isn't available


# ── Tie it together ──────────────────────────────────────────────────────
def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit(
            "No ANTHROPIC_API_KEY found. Copy .env.example to .env and add "
            "your key (get one at https://console.anthropic.com)."
        )

    print("Building your digest...\n")
    today, text = build_digest()

    md_path = write_markdown(today, text)
    print(f"\n✅ Markdown saved (local): {md_path}")

    audio_path = make_audio(today, text)
    print(f"🔊 Audio saved (local):    {audio_path}")

    # Final step: copy into iCloud so it reaches your phone. This is the only
    # step that touches the protected iCloud folder.
    try:
        os.makedirs(config.ICLOUD_DIR, exist_ok=True)
        for name in (f"digest-{today}.md", f"digest-{today}.m4a"):
            src = os.path.join(config.LOCAL_DIR, name)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(config.ICLOUD_DIR, name))
        print(f"☁️  Copied to iCloud:      {config.ICLOUD_DIR}")
        print("\nOpen them on your phone via Files → iCloud Drive → AI Digest.")
    except PermissionError:
        print(
            "\n⚠️  Couldn't copy to iCloud — macOS is blocking it.\n"
            "    Your files are safe here: " + config.LOCAL_DIR + "\n"
            "    To let scheduled runs reach iCloud, give Python "
            "'Full Disk Access' (see README)."
        )


if __name__ == "__main__":
    main()
