"""
run_cloud.py — the cloud entry point (for GitHub Actions).

It reuses the SAME research logic as the local version (build_digest), but
instead of saving to iCloud + audio, it sends the text to Telegram.
The local `digest.py` still works on your Mac unchanged.
"""

import os

from digest import build_digest
from notify import send_telegram


def main():
    today, text = build_digest()   # does the research + prints the cost
    send_telegram(text)
    print(f"\n📨 Sent the {today} digest to Telegram.")

    # Podcast step — only runs when FEED_BASE_URL is set (i.e. in the cloud,
    # where Piper + ffmpeg are installed). Skipped on a plain local run.
    if os.environ.get("FEED_BASE_URL"):
        import speak
        import build_feed
        speak.make_mp3(text, f"docs/episodes/{today}.mp3")
        build_feed.build()
        print("🎧 Podcast episode + feed updated.")


if __name__ == "__main__":
    main()
