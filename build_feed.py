"""
build_feed.py — regenerate the podcast RSS feed from the episodes on disk.

Scans docs/episodes/*.mp3 and writes docs/feed.xml. GitHub Pages serves the
docs/ folder, so the feed becomes a real podcast you can subscribe to.
Needs FEED_BASE_URL (e.g. https://you.github.io/Newsfeed), set in the workflow.

Filenames are either:
  2026-06-29-reddit.mp3   (per-topic episode — current format)
  2026-06-29.mp3          (old combined episode — still supported)
"""

import glob
import html
import os
from datetime import datetime
from email.utils import formatdate

import config

DOCS = "docs"
EPISODES_DIR = os.path.join(DOCS, "episodes")

# key -> nice label, taken from the configured beats
# (e.g. "reddit" -> "📈 Reddit ticker radar").
LABELS = {b["key"]: b["title"] for b in config.BEATS}


def _title_and_date(name):
    """Filename -> (episode title, YYYY-MM-DD). Handles both name formats."""
    stem = name[:-4]                                  # drop .mp3
    date_str = stem[:10]                              # 2026-06-29
    topic = stem[11:] if len(stem) > 10 else ""       # reddit  ("" for old files)
    if topic:
        label = LABELS.get(topic, topic.replace("-", " ").title())
    else:
        label = "Daily digest"
    return f"{label} — {date_str}", date_str


def build():
    base = os.environ["FEED_BASE_URL"].rstrip("/")
    items = []

    # Newest first.
    for path in sorted(glob.glob(os.path.join(EPISODES_DIR, "*.mp3")), reverse=True):
        name = os.path.basename(path)
        size = os.path.getsize(path)
        title, date_str = _title_and_date(name)
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            dt = datetime.utcnow()
        items.append(f"""    <item>
      <title>{html.escape(title)}</title>
      <enclosure url="{base}/episodes/{name}" length="{size}" type="audio/mpeg"/>
      <guid isPermaLink="false">{name}</guid>
      <pubDate>{formatdate(dt.timestamp())}</pubDate>
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>My AI Digest</title>
    <link>{base}/</link>
    <description>Daily personal research digest: AI, GitHub, and a Reddit ticker radar.</description>
    <language>en-us</language>
    <itunes:author>AI Digest Agent</itunes:author>
    <itunes:explicit>false</itunes:explicit>
{chr(10).join(items)}
  </channel>
</rss>
"""
    with open(os.path.join(DOCS, "feed.xml"), "w") as f:
        f.write(rss)
    print(f"Feed updated with {len(items)} episode(s).")


if __name__ == "__main__":
    build()
