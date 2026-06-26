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
        today, text = build_digest()   # does the research + prints the cost
    except Exception as e:
        try:
            send_telegram(f"⚠️ Digest run FAILED during research:\n{type(e).__name__}: {e}")
        except Exception:
            pass
        raise

    send_telegram(text)
    print(f"\n📨 Sent the {today} digest to Telegram.")

    # Podcast step — only runs when FEED_BASE_URL is set (i.e. in the cloud,
    # where Piper + ffmpeg are installed). Skipped on a plain local run.
    # Wrapped so a TTS/feed hiccup can't undo the Telegram delivery above.
    if os.environ.get("FEED_BASE_URL"):
        try:
            import speak
            import build_feed
            speak.make_mp3(text, f"docs/episodes/{today}.mp3")
            build_feed.build()
            print("🎧 Podcast episode + feed updated.")
        except Exception:
            print("⚠️ Podcast step failed (Telegram already sent):")
            traceback.print_exc()
            raise


if __name__ == "__main__":
    main()
