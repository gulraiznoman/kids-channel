---
name: project-vanar-content
description: Vanar ecosystem marketing (via Inflectiv/Big Immersive): workspace location, what holds the rules, current state as of Oct 2026
metadata:
  type: project
---
User (Big Immersive) runs Vanar ecosystem social content published as/with Inflectiv. As of 2026-10-05 the source of truth is a Claude Code workspace unzipped at `C:\Users\BiM Pro -057\Downloads\vanar-content\` (from vanar-content.zip, git repo, 1 commit).

Read its `CLAUDE.md` first: voice rules (no contractions, no dashes OR hyphens in copy, banned words, X under 200 chars with URL = 23, British "Organisation" with the spelling ruling still open), precedence order, and skills (/post, /weekly-recap, /replies, /calendar, /design-brief, /partnership, /genesis-email, /colleague-message, /brand-check). Dated state lives in `context/current-state.md`; recap variation log in `recaps/variation-log.md` (next is week 8). `scripts/brand_check.py` works on this machine with `python`; openpyxl is installed.

Older loose files (plans, briefs, videos, AMA scripts, `Inflectiv-Vanar-Project-Memory.md` from July) sit in Downloads as Vanar*.docx/xlsx/mp4; the workspace supersedes the July memory (e.g. site is now onvanar.com, Genesis opened 1 Oct 2026, Kayon out).

**Why:** next sessions should work inside the workspace rules instead of re-deriving them.
**How to apply:** for any Vanar task, cd into the workspace and follow its CLAUDE.md and skills; it overrides general Inflectiv habits. Related: [[project-inflectiv-socials]], [[feedback-versioned-deliverables]].

Jaka Kotnik also reviews Vanar copy and gets annoyed by corrections he has to repeat (2026-10-05: Genesis credits are never "claimed"; they arrive on sign up and belong to the account, not an Org). Before drafting, check the workspace `context/current-state.md` corrections; record every new reviewer correction there, and in `scripts/brand_check.py` where it can be caught automatically.

2026-10-07: reviewer was sharp that I sent copy calling onvanar.com/showcase Orgs "real" (they are examples; the page says "Real businesses, not chatbots" which means business types). Never treat a page summary as fact for claims about real users, customers or results; if a claim implies something is live or real, flag it as unverified instead of writing it.
