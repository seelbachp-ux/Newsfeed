# Lessons — building my first AI agent

A plain-language record of what I learned building the Newsfeed digest agent,
written as short lessons so I (and anyone reading) can follow the thinking.

## 1. What an agent actually is
An agent is just a loop: a model gets a **goal**, can call **tools** (search,
run code, read files), looks at the **result**, decides the next step, and
repeats until done. A chatbot *answers*; an agent *acts in a loop*. That's the
whole secret — everything else is plumbing around that loop.

## 2. The tools are what make it useful
Same loop everywhere; only the tools change. Research agent = search tool.
Coding agent = file + shell tools. Data agent = code execution. Master one and
you understand them all.

## 3. Tuning an agent = writing, not coding
80% of how my agent behaves comes from the **system prompt** and the **tool
descriptions** — plain English. When a section came out weak or apologetic, the
fix was editing the prompt, not the code. (Example: I had to literally tell it
"never mention search limits — just write the briefing.")

## 4. Cost has two layers — and quality is gated by search, not model IQ
1. Model tokens. 2. Web search. For a news digest, every competent model
summarizes fine; what makes results good is **search recency/quality**. So the
optimum is *cheapest competent model + strong search*, not a smarter model.
Levers I used: cheaper model (Sonnet → Haiku), low effort, capped searches.

## 5. At low volume, cost optimization is mostly for learning
Running 3×/week, the gap between my setup and the absolute cheapest is a few
dollars a *month*. Switching providers to save that is a learning decision, not
an economic one. Don't pre-optimize — measure first (I built a cost meter).

## 6. The macOS gotcha: scheduled jobs can't touch protected folders
When *I* ran it in Terminal, it could write to iCloud. When `launchd` ran it at
7am, macOS privacy (TCC) blocked it — silently. Lesson: a background scheduler
has different permissions than your interactive session.

## 7. Architecture fix: only ONE program should touch the protected thing
Instead of granting permissions to python + `say` + `afconvert`, I made
everything write to a plain folder first, then have a single step copy to the
protected location. Fewer things needing permission = less fragility.

## 8. Going cloud removes the machine dependency — but changes delivery
Off-machine (GitHub Actions) meant the Mac-only bits (`say`, iCloud) had to be
swapped for cloud equivalents (Piper TTS, Telegram, a podcast feed on GitHub
Pages). The *research core* didn't change at all — only the edges.

## 9. Flaky bugs and honest tests
A bug that "works manually but fails on schedule" was actually **random**, not
manual-vs-scheduled. On GitHub Actions, a manual run and a scheduled run execute
the identical job — the only difference is what presses "go." And a good fix is
*structural* (remove the feature that breaks), not *lucky* (hope it passes).
The real bug: the newest web-search tool ran code in a sandbox ("container")
that the continuation call must reference; switching to the standard search tool
removed the failure mode entirely.

## 10. Delegation == prompting
Briefing an agent is the same skill as briefing a person: a clear goal, the
right access/tools, feedback after each step, and knowing when to stop. Vague
goals and missing access break both.
