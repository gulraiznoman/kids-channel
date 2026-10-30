# Gul & Mishu (kids YouTube channel)

Everything used to make the Gul & Mishu videos: scripts, character art, voice tools, plans.
Videos and audio are NOT in this repo (kept separately).

## Key files
- `CONTENT LOG.md`: every video made so far. Check it before making a new one (no repeats).
- `PLAN Nov 2026 - Jan 2027.md`: the 3-month upload plan.
- `claude-memory/`: Claude's notes (channel rules, preferences, lessons learned). On a new laptop,
  copy these into `~/.claude/projects/<project>/memory/` so Claude remembers how the channel works.
- `characters/`: Gul & Mishu layer kit + `expressions.py` (feelings faces).
- `longNN-*/`: one folder per long video: `art.py` (props/backgrounds), `make.py` (script, voices, music),
  `render.py` (animation), `clarity.py` (speech check).
- `tools/`: Shorts, thumbnails (`thumb_fun.py`), music helpers.
- `voices/kidvoice.py`: the Gul & Mishu voices (Kokoro TTS + Praat).

## Setting up a new laptop
1. Install Python 3.12, ffmpeg (on PATH), and Google Chrome (art is rendered with headless Chrome).
2. `pip install -r requirements.txt`
3. Make a video: `cd long12-trucks && python art.py && python make.py && python render.py video`
   (output goes to `VIDEOS/<name>/`).
