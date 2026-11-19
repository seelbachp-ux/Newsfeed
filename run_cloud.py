"""
run_cloud.py — delivery step (GitHub Actions).

The research is done by a scheduled Claude routine (see ROUTINE.md), which
pushes one Markdown file per beat to digests/<date>/<key>.md. This script
picks up every digest that has no podcast episode yet, sends it to Telegram,
renders the episodes and rebuilds the feed.

Run with WATCHDOG=true (the scheduled run) it also alerts on Telegram when
today's digest never arrived — so a broken routine can't go silent.
"""

import glob
import os
from datetime import date

import config
from notify import send_telegram


def pending():
    """Digest dates with no podcast episode yet = not delivered."""
    days = sorted(os.path.basename(d.rstrip("/")) for d in glob.glob("digests/*/"))
    return [d for d in days if not glob.glob(f"docs/episodes/{d}-*.mp3")]


def load(day):
    """Sections in config.BEATS order; beats the routine skipped are left out."""
    sections = []
    for b in config.BEATS:
        path = f"digests/{day}/{b['key']}.md"
        if os.path.exists(path):
            with open(path) as f:
                sections.append({"key": b["key"], "title": b["title"], "text": f.read().strip()})
    return sections


def deliver(day):
    sections = load(day)
    for s in sections:
        send_telegram(f"{s['title']}\n\n{s['text']}")
    print(f"📨 {day}: sent {len(sections)} topic messages to Telegram.")

    # Podcast only where Kokoro + ffmpeg exist (the workflow sets FEED_BASE_URL).
    if os.environ.get("FEED_BASE_URL"):
        import speak
        for s in sections:
            speak.make_mp3(s["text"], f"docs/episodes/{day}-{s['key']}.mp3")
        print(f"🎧 {day}: {len(sections)} podcast episodes rendered.")


def main():
    days = pending()
    for day in days:
        deliver(day)
    if days and os.environ.get("FEED_BASE_URL"):
        import build_feed
        build_feed.build()

    today = date.today().isoformat()
    if os.environ.get("WATCHDOG") == "true" and not os.path.isdir(f"digests/{today}"):
        send_telegram(
            f"⚠️ No digest arrived for {today}. Check the routine at "
            "https://claude.ai/code/routines"
        )
        raise SystemExit("No digest today.")


if __name__ == "__main__":
    main()
