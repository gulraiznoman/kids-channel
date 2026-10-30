"""Voice audition: Kokoro (free, Apache-2.0, offline) voices shifted younger for Gul and Mishu.
python audition.py -> one WAV per candidate in this folder
"""
import pathlib, subprocess
import numpy as np, soundfile as sf
from kokoro import KPipeline

HERE = pathlib.Path(__file__).resolve().parent
pipe = KPipeline(lang_code="a")

LINES = {
    "mishu": "Hi friends! I'm Mishu! Gul, look! What's this? Apple! Can you say apple?",
    "gul": "Hi friends! I'm Gul! It's a red, shiny apple! Great job! Let's go!",
}
CANDIDATES = [
    ("Kid Mishu A", "mishu", "af_heart", 7, 1.08),
    ("Kid Mishu B", "mishu", "af_bella", 7, 1.08),
    ("Kid Gul A", "gul", "af_sarah", 5, 1.08),
    ("Kid Gul B", "gul", "af_heart", 4, 1.04),
]


def say(text, voice, speed):
    chunks = [a for _, _, a in pipe(text, voice=voice, speed=speed)]
    return np.concatenate([c.numpy() if hasattr(c, "numpy") else c for c in chunks])


for label, who, voice, st, speed in CANDIDATES:
    raw = HERE / f"_raw_{label}.wav"
    sf.write(raw, say(LINES[who], voice, speed), 24000)
    out = HERE / f"{label}.wav"
    ratio = 2 ** (st / 12)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-af", f"rubberband=pitch={ratio:.4f},aresample=48000", str(out)], check=True)
    raw.unlink()
    print("wrote", out.name)
