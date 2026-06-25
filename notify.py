"""
notify.py — sends the digest to Telegram.

Uses only the standard library (urllib), so there's nothing extra to install.
Reads two values from the environment (set as GitHub secrets in the cloud):
    TELEGRAM_BOT_TOKEN  — from @BotFather when you create your bot
    TELEGRAM_CHAT_ID    — your personal chat id (see README)
"""

import os
import re
import urllib.parse
import urllib.request

TELEGRAM_MAX = 4096  # Telegram's hard limit per message


def _to_plain(md):
    """Turn Markdown into clean text Telegram shows nicely (keeps links)."""
    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 — \2", md)  # [t](u) -> t — u
    md = re.sub(r"[#*`>_]", "", md)                           # drop md symbols
    return md.strip()


def _chunk(text, size=3500):
    """Split into <size pieces on blank-line boundaries (Telegram caps length)."""
    parts, cur = [], ""
    for para in text.split("\n\n"):
        if len(cur) + len(para) + 2 > size:
            if cur:
                parts.append(cur)
            cur = para[:size]  # safety: a single huge para still fits
        else:
            cur = f"{cur}\n\n{para}" if cur else para
    if cur:
        parts.append(cur)
    return parts or [text[:size]]


def send_telegram(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID.")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for piece in _chunk(_to_plain(text)):
        data = urllib.parse.urlencode({
            "chat_id": chat,
            "text": piece,
            "disable_web_page_preview": "true",
        }).encode()
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as resp:  # raises on HTTP error
            resp.read()
