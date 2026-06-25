# AI Digest Agent

A tiny personal research agent. Each run, it searches the web for recent items
in your topics, writes a short Markdown digest, and produces an audio version —
both dropped into your iCloud `AI Digest` folder so they sync to your phone.

It's built on the **classic agent loop**: give the model a goal + a tool
(web search), let it search/read/decide, and collect the result.

## Files
- `config.py` — settings + prompts. **Edit this to change what it researches.**
- `digest.py` — the agent itself (the loop, saving, audio).

## Setup (one time)
```sh
cd ~/ai-digest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then paste your real API key into .env
```
Get an API key at https://console.anthropic.com.

## Run
```sh
source .venv/bin/activate
python digest.py
```

## Customize
- **Add a topic:** copy a dict in `BEATS` (config.py) and change its prompt.
- **Change focus:** edit `PROFILE` in config.py.
- **Nicer voice:** run `say -v '?'`, pick one, set `VOICE` in config.py.

## Cost
Each run prints an estimated cost (`💸 Estimated cost this run: $...`). Levers
live in `config.py`: `MODEL` (Sonnet ≪ Opus; Haiku is cheapest), `EFFORT`
("low" is cheapest), and `MAX_SEARCHES_PER_BEAT`.

## Automated runs (launchd) + Full Disk Access
A `launchd` job (`~/Library/LaunchAgents/com.philipp.aidigest.plist`) runs this
on a schedule. Scheduled runs generate files in `output/` (always works), then
**Python copies them into iCloud** — and macOS blocks that copy unless Python
has **Full Disk Access**:

1. System Settings → Privacy & Security → **Full Disk Access**
2. Click **+**, then in the dialog press **Cmd+Shift+G** and paste:
   `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`
3. Select `python3.9`, make sure its toggle is **ON**.

Test a scheduled run on demand:
`launchctl kickstart -k gui/$(id -u)/com.philipp.aidigest` then check `digest.log`.

(Manual runs from Terminal already work — Terminal has its own access.)

## Roadmap (the build-in-public arc)
1. ✅ AI + GitHub beats, iCloud + audio delivery
2. Add a Leadership beat
3. Add a Reddit "trending tickers" beat (radar, not advice)
4. Run automatically every morning (schedule it)
5. Turn the audio into a private podcast feed for CarPlay auto-play
