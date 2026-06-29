# Build-in-public posts — Newsfeed agent

Draft snippets for LinkedIn / X. Edit to taste; pick the ones that fit.

---

## LinkedIn — the story post

I just built my first AI agent — and it runs itself in the cloud.

It's a personal research agent. Three times a week it searches the web for
what's new in AI and open source, writes me a short briefing, sends it to
Telegram, and turns it into a podcast episode I can listen to in the car.

The thing that surprised me most: building an agent is mostly **clear writing**,
not heavy coding. An "agent" is just a loop — give a model a goal and some
tools (here: web search), let it search, read, decide, repeat. The behavior
lives in the instructions you write, not in clever code.

What I learned along the way:
• Quality depends on search quality, not how "smart" the model is
• Cost has levers (model choice, effort, search caps) — I added a meter and got
  it to ~10 cents a run
• Cloud scheduling (GitHub Actions) means it runs whether my laptop is on or not

Next: a leadership-news section, and a "what's trending" radar.

If you've been meaning to try building an agent — start tiny. One job, one tool.

---

## LinkedIn — the lesson post (shorter)

A bug taught me something this week.

My agent "worked when I ran it manually, but failed on schedule." Classic.

The instinct is "scheduled runs are different." They're not — on GitHub Actions
the manual and scheduled runs are the *identical* job; the only difference is
what triggers them. The real cause was a random failure that I'd just gotten
lucky on manually.

The fix that mattered wasn't a tweak-and-hope. It was *structural* — I removed
the feature causing the failure entirely, so the failure mode can't happen.

Lesson: when a test passes intermittently, a passing run proves nothing. Fix the
mechanism, not the symptom.

---

## X / Twitter — thread

1/ Built my first AI agent this week. It researches AI + open-source news 3×/wk,
DMs me a digest on Telegram, and makes a podcast I listen to in the car. Runs in
the cloud, no laptop needed. 🧵

2/ The big unlock: an "agent" is just a loop. Goal → call a tool (web search) →
read result → decide → repeat. The intelligence is in the *instructions*, not
fancy code.

3/ 90% of tuning it was editing the prompt. Weak output? Reworded the prompt.
That's the skill — writing, not engineering.

4/ Cost lessons: quality comes from search, not model size. So: cheapest
competent model + good search. Added a cost meter → ~$0.10/run.

5/ Best debugging lesson: "works manually, fails on schedule" was just a flaky
bug I'd gotten lucky on. Same job both ways. Fix the mechanism, not the symptom.

6/ If you've been putting off building an agent: start tiny. One job, one tool.
You'll get it running in an afternoon.
