"""
build_feed.py — regenerate the podcast RSS feed from the episodes on disk.

Scans docs/episodes/*.mp3 and writes docs/feed.xml. GitHub Pages serves the
docs/ folder, so the feed becomes a real podcast you can subscribe to.
Needs FEED_BASE_URL (e.g. https://you.github.io/ai-digest), set in the workflow.
"""

import glob
import os
from datetime import datetime
from email.utils import formatdate

DOCS = "docs"
EPISODES_DIR = os.path.join(DOCS, "episodes")


def build():
    base = os.environ["FEED_BASE_URL"].rstrip("/")
    items = []

    # Newest first.
    for path in sorted(glob.glob(os.path.join(EPISODES_DIR, "*.mp3")), reverse=True):
        name = os.path.basename(path)         # e.g. 2026-06-26.mp3
        date_str = name[:-4]                   # 2026-06-26
        size = os.path.getsize(path)
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            dt = datetime.utcnow()
        items.append(f"""    <item>
      <title>Digest — {date_str}</title>
      <enclosure url="{base}/episodes/{name}" length="{size}" type="audio/mpeg"/>
      <guid isPermaLink="false">{name}</guid>
      <pubDate>{formatdate(dt.timestamp())}</pubDate>
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>My AI Digest</title>
    <link>{base}/</link>
    <description>Daily personal research digest: AI and GitHub.</description>
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
