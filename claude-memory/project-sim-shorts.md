---
name: project-sim-shorts
description: Gulraiz's faceless physics-simulation Shorts channel (country flag marble races), fully code-generated in ~/sim-shorts
metadata:
  type: project
---

On 2026-10-07 Gulraiz chose a faceless channel Claude can make end to end, after
weighing kids rhymes (needs a singer, low pay) and data maps. Picked: viral
"which country wins" flag marble races plus other physics-sim Shorts, aiming at YPP
via 1,000 subs + 10M Shorts views in 90 days. See [[project-youtube-kids]],
[[user-gulraiz]].

Pipeline in `~/sim-shorts`: `race_sim.py` (pymunk course + seed search; pick the seed
with the closest top-3 finish and most lead changes, never rig the winner),
`race_render.py` (PIL, 1080x1920 60fps, NW=8 parallel chunks, ~2 min),
`race_audio.py` (procedural music + per-country bounce notes + chimes),
then ffmpeg mux with loudnorm -14 LUFS and `-ar 48000`. Flags from flagcdn.com.
Deliverables in `VIDEOS/NN name/` like the ambient channel [[project-youtube-ambient]].
Upload as "not made for kids" to keep comments on (comment-driven growth).

01 Flag Marble Race v1 (seed 18, India wins, 58 s) delivered 2026-10-07.

2026-10-07: 90-day plan delivered as `~/sim-shorts/Channel Plan v1.xlsx` (built by a
scratch script; regenerate as v2, don't overwrite). 135 Shorts + 11 long videos,
start date 12 Oct 2026, phases Test / Double down / Scale, global English audience.
Recommended channel name "Bounce Arena" (backup "Marble Nations"); channel not
created yet. Formats still to build: escape the rings, last ball standing, odd emoji,
guess the flag, flag territory war, RPS war, ball grows, World Cup long series.

2026-10-07 later: he found the plan's ideas "boring" and AI-evolution channels low on
views. A scan of ~1,400 YouTube videos from the past month (script
`yt_scan.py` in that session's scratchpad) confirmed AI-evolution sims are weak
(median ~1.6K views). Small channels winning big were in what-if/space and
"how long would you survive" explainers (e.g. The Last Day, 26K subs, 1.5M views),
aviation-disaster explainers (incl. Urdu/Hindi, ZD Explain 304K on 1.4K subs),
long marble-race tournaments, and geography Shorts. Lesson: back niche advice
with this kind of outlier data, not with the famous top channels.
