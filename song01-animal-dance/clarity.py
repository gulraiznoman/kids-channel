"""Clarity check: transcribe each sung word with faster-whisper; score = share of words recognised."""
import json, re, subprocess, sys
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
M = WhisperModel("small", device="cpu", compute_type="int8")
ev = json.load(open("notes.json"))["events"]
hits = {}
for who in ("gul", "mishu"):
    x, sr = sf.read(sys.argv[2] if len(sys.argv) > 2 else f"vocal_{who}.wav")
    x = x.mean(axis=1) if x.ndim == 2 else x
    ok = n = 0
    for e in ev:
        if e["who"] != who:
            continue
        a = x[int(e["t"] * sr): int((e["t"] + e["dur"]) * sr)]
        a = np.concatenate([np.zeros(sr // 4), a, np.zeros(sr // 4)]).astype(np.float32)
        a16 = a[::3] if sr == 48000 else a
        segs, _ = M.transcribe(a16, language="en", beam_size=5, without_timestamps=True)
        heard = " ".join(s.text for s in segs).lower()
        want = re.sub(r"[^a-z]", "", e["word"].lower())
        good = want[:4] in re.sub(r"[^a-z]", "", heard)
        ok += good; n += 1
        if "-v" in sys.argv: print(who, e["word"], "->", heard.strip(), "OK" if good else "MISS")
    hits[who] = f"{ok}/{n}"
print("recognised:", hits)
