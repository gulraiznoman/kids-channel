---
name: feedback-skytrack-work
description: "How to work on SkyTrack — no em dashes, test across regions, be honest about data limits"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 03ef80f1-2ba8-4f17-927f-922ec9bc1880
  modified: 2026-07-28T12:28:21.907Z
---

Working style the user wants on SkyTrack [[project-skytrack]]:

- NO em dashes (—) in any user-facing text (titles, meta, placeholders, toasts, notes). Use commas / colons / periods. Empty-value placeholders use an en dash (–). Code comments are exempt.
- Verify trail/data fixes by TESTING ACROSS MANY FLIGHTS AND REGIONS (fetch real traces via the local API and simulate the logic), not a single screenshot, then also screenshot-verify with Edge headless. The user explicitly demanded this thoroughness before publishing.
- Be blunt and honest that remaining trail imperfections come from free-data limits, not code; do not over-promise ("110%").

**Why:** the user is publishing this and got frustrated by repeated one-off "fixes" that didn't hold across other flights.

**How to apply:** after any data/trail change, run a region-sweep test (Pakistan/Gulf/India/Europe), screenshot-verify, then deploy per [[reference-skytrack-deploy]].

- GLOBAL, never Pakistan-specific (said 2026-10-12, repeatedly): SkyTrack is a worldwide tracker like FR24/FlightAware. All user-facing copy, blog topics, examples and CTAs use worldwide examples (EK623, BA117, AA100; Heathrow, Dubai, JFK, Singapore, Tokyo, Istanbul). No PIA-specific articles, no per-country text swapping on content pages. Pakistan may only appear as one item in a factual list, and even then prefer neutral wording (oceans, Africa, Central Asia).
