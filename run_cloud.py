"""
run_cloud.py — the cloud entry point (for GitHub Actions).

It reuses the SAME research logic as the local version (build_digest), but
instead of saving to iCloud + audio, it sends the text to Telegram.
The local `digest.py` still works on your Mac unchanged.
"""

from digest import build_digest
from notify import send_telegram


def main():
    today, text = build_digest()   # does the research + prints the cost
    send_telegram(text)
    print(f"\n📨 Sent the {today} digest to Telegram.")


if __name__ == "__main__":
    main()
