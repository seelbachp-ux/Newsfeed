# Routine instructions — research the digest

You are the research half of a personal news digest. A GitHub Action handles
delivery (Telegram + podcast) as soon as you push. Your only job is to write
the sections and push them.

## 1. Work out the date and coverage window

- Today = `date -u +%F` (runs Mon/Wed/Fri ~04:17 UTC).
- The coverage window is everything since the previous brief:
  Monday → since Friday, Wednesday → since Monday, Friday → since Wednesday.
  Any other weekday (manual run) → the last 2 days.

## 2. Read the brief

Open `config.py`. It is the single source of truth:
- `PROFILE` — who the reader is.
- `SYSTEM_PROMPT` — the rules for every item (format, ranking, tone,
  coverage window). Follow them exactly.
- `BEATS` — one research task per section. Do each `prompt`.

Ignore `MODEL`, `EFFORT`, `MAX_SEARCHES_PER_BEAT` and `PRICING`; those are for
the old local script. Do not run `digest.py` (it needs an API key you don't have).

## 3. Research each beat

Use web search and fetch to check sources. Only report items you can confirm
are inside the coverage window.

The beat with `"context": "reddit_radar"` needs live data first. Fetch
`https://apewisdom.io/api/v1.0/filter/all-stocks/page/1` (curl or web fetch)
and use the top 12 results: `ticker`, `name`, `mentions` vs `mentions_24h_ago`,
`rank` vs `rank_24h_ago`. If that fetch fails, web-search for currently
trending Reddit stock tickers instead.

## 4. Write the files

For each beat, write `digests/<today>/<key>.md` (for example
`digests/2026-11-20/ai.md`). Each file holds only that section's body in
Markdown. No title, because delivery adds it. Never mention tools, searches
or limits.

## 5. Commit and push

Commit only `digests/<today>/` with the message `Digest <today>`, then push
to `main`. If the push is rejected because main moved, `git pull --rebase` and
push again. If pushing to main isn't allowed, push to a branch named
`claude/digest-<today>` instead; delivery picks up either. Don't open a PR,
and don't change any other file.
