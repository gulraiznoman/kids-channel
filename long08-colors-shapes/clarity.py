import json, re, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
M = WhisperModel("small", device="cpu", compute_type="int8")
d = json.load(open("timeline.json")); x, sr = sf.read("mix.wav"); x = x.mean(axis=1)
seen, ok, n = set(), 0, 0
nums = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ").replace("'", ""))
for e in d["lines"]:
    if (e["who"], e["text"]) in seen: continue
    seen.add((e["who"], e["text"])); n += 1
    a = x[int((e["t"] - 0.1) * sr): int((e["t"] + e["dur"] + 0.15) * sr)].astype(np.float32)[::3]
    a = np.concatenate([np.zeros(4000, np.float32), a, np.zeros(4000, np.float32)])
    h = " ".join(s.text for s in M.transcribe(a, language="en", beam_size=5)[0]).strip()
    hh = " ".join(nums.get(w, w) for w in norm(h).split())
    w = [k for k in norm(e["text"]).split() if len(k) > 2]
    good = sum(k in hh for k in w) >= max(1, len(w) - 1) if w else True
    ok += good
    if not good: print("MISS", e["who"], e["text"], "->", h)
print(f"{ok}/{n} distinct lines clear")
