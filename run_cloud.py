"""
run_cloud.py — the cloud entry point (for GitHub Actions).

It reuses the SAME research logic as the local version (build_digest), but
instead of saving to iCloud + audio, it sends the text to Telegram.
The local `digest.py` still works on your Mac unchanged.
"""

import os
import traceback

from digest import build_digest
from notify import send_telegram


def main():
    # Research first. If THIS fails, you'd otherwise get total silence — so we
    # ping Telegram with the error, then re-raise so the run still shows red.
    try:
        today, sections, cost = build_digest()   # research + prints cost
    except Exception as e:
        try:
            send_telegram(f"⚠️ Digest run FAILED during research:\n{type(e).__name__}: {e}")
        except Exception:
            pass
        raise

    # One Telegram message per topic. Cost footer goes on the last message only
    # (and not into the section text, so the podcast audio doesn't read it).
    for i, s in enumerate(sections):
        body = f"{s['title']}\n\n{s['text']}"
        if i == len(sections) - 1:
            body += "\n\n" + cost
        send_telegram(body)
    print(f"\n📨 Sent {len(sections)} topic messages to Telegram.")

    # Podcast: one episode per topic. Only runs when FEED_BASE_URL is set (the
    # cloud, where Piper + ffmpeg exist). Wrapped so a TTS/feed hiccup can't
    # undo the Telegram delivery above.
    if os.environ.get("FEED_BASE_URL"):
        try:
            import speak
            import build_feed
            for s in sections:
                speak.make_mp3(s["text"], f"docs/episodes/{today}-{s['key']}.mp3")
            build_feed.build()
            print(f"🎧 {len(sections)} podcast episodes + feed updated.")
        except Exception:
            print("⚠️ Podcast step failed (Telegram already sent):")
            traceback.print_exc()
            raise


if __name__ == "__main__":
    main()
