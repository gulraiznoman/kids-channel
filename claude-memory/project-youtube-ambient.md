---
name: project-youtube-ambient
description: "Gulraiz's YouTube relaxing/ambient video channel and the fully procedural generator built for it"
metadata: 
  node_type: memory
  type: project
  originSessionId: f76e5fa8-a6a2-432f-80c9-c8f33d543aed
  modified: 2026-09-09T07:35:36.293Z
---

Gulraiz is making relaxing/ambient videos for a YouTube channel. Everything
lives in the `ambient-video` folder in his home directory. Two pieces built
2026-09-09:

1. **Aurora over a lake**, 4:30, dark and cool, drone score (`visual.py`,
   `synth.py`), modelled on the 3-hour nature-scenery compilations.
2. **Flying above the clouds**, 4:30, bright and warm, melodic piano score
   (`sky_visual.py`, `sky_synth.py`), modelled on Peder B. Helland /
   Soothing Relaxation.
3. **Zen spa** (lotus flowers, candles, bamboo water spout, reflective pool),
   4:16, bright and warm, healing piano + flute + water + birds, built
   2026-09-11 and modelled on Relaxing Calming Music (@relaxingcalmming).
   `zen_build.py` draws the static art once and caches PNGs;
   `zen_visual.py` animates on top (bokeh, flames, stream, ripples, sway,
   camera). This bright spa look is what he actually wants.

His workflow: he sends a reference YouTube link and expects a piece in that
style at 3-5 minutes, plus a thumbnail and full upload metadata (title,
description, tags), without having to ask for those separately.

The deliberate constraint is that **everything is generated from code** — no stock
footage, no stock music, no third-party assets at all. `visual.py` renders the
scene, `synth.py` + `mix.sh` generate the score. He chose this over downloading
free stock clips.

**Why:** YouTube's reused-content policy is what blocks monetization for most
channels in this genre (stock clips + a stock track, nothing added). Generating
everything removes the licensing problem entirely. He also has a $0 budget, so
paid stock was never an option. See [[user-gulraiz]].

**How to apply:** Keep new pieces fully procedural — do not suggest downloading
stock assets, it defeats the point. `README.md` in that folder documents both
pipelines and the traps (ffmpeg `loudnorm` silently leaves output at 192 kHz;
`afir` defaults to `irnorm=1` which buries a long impulse by ~86 dB; ripple
amplitude above ripple wavelength causes chevron aliasing). Render with `NW=6`
for parallelism — single-process is 11x slower. Version each render rather than
overwriting, per [[feedback-versioned-deliverables]].

The visuals loop seamlessly by construction (all oscillators use whole cycle
counts), so long 1-hour / 3-hour cuts are cheap. The audio does not loop yet —
its slot envelopes fade to silence at both ends and would need to wrap.

## Update 2026-09-14: real footage, folders, Shorts

- He called the drawn/procedural videos "too fake and AI generated". Default is now
  REAL footage and REAL nature recordings from Mixkit, checking the licence on every
  asset: `data-license="videoFree"` / `sfxFree` allow monetised YouTube; skip
  `videoRestricted`. Prefer 4K (`-2160.mp4`) so 9:16 crops stay sharp. Mixkit
  rate-limits page fetches (429): throttle about 3 s. Scripts: `stock_fetch.py`,
  `short_build.py` (32 s multi-shot loop Short), `loop_short.py` (6-10 s single-shot loops).
- Deliverables live in `ambient-video/VIDEOS/NN <name>/`: `UPLOAD THIS - ....mp4`,
  `THUMBNAIL.jpg`, `upload details.md`, and `old versions - do not upload/`. He asked
  for one folder per video, never mixed. New videos go straight into a new numbered folder.
- He wants Shorts short: 6-10 s single-shot loops, or about 30 s. Seamless loops.

## Update 2026-10-10: what the analytics actually say

Channel @airborneexpeditions6 (UCuhK0e4psWHwJezx2jNZIgQ), 62 subs, 4,995
lifetime views. Studio, last 28 days: 4,311 views, 17.6 watch hours, +8 subs.

- **Shorts are the channel.** 13 Shorts carry ~4,642 lifetime views; 13
  long-form videos carry 339 between them. 17.6 h over 4,311 views is 14.7 s
  per view, so essentially all watch time is Shorts.
- **Retention is fine, conversion is not.** Shorts hold 74-165% (over 100% =
  loops). But 8 subs from 4,311 views is 0.19% against a normal 0.5-1%. That,
  not reach, is the thing to fix.
- **Shorts watch time does not count toward the 4,000-hour YPP threshold.**
  Only long-form does, and long-form produces ~3.4 h per month here. Do not
  recommend longer Shorts to "bank watch hours"; it buys nothing. Shorts are
  for reach and subscribers, and reach follows retention percentage and
  swipe-away rate, which favour shorter.
- Subscribers acquired through Shorts rarely watch long-form, which is why a
  new 20-minute upload can sit at 0 views with 62 subscribers.
- Honest odds given to him: 1,000 subs in 12 months likely (~70%), 4,000 watch
  hours unlikely (~20%). Metadata and SEO were never the bottleneck and should
  not be sold as the fix.

## Duplicate footage: check by content, never by filename

The stock library is 291 files but only **211 distinct source clips**. The same
video is saved under different names (`cabin/snow.mp4` is the Swiss Alps
timelapse; `sunrise/cloud.mp4` is the Alps clip) and sometimes re-encoded at a
different resolution so even the bytes differ. Filenames also lie outright:
`fire/wood-fire.mp4` is a dog beside a lake in daylight.

`clipmap.py` unions by content hash AND by Mixkit slug; `dupe_check.py` reads
the live channel and blocks a batch that reuses footage, reuses a file under
another name, or shares two significant words with a published title. **Run
`python dupe_check.py` before delivering any batch.** He asked explicitly for
no repeated or similar videos and titles.
