"""Rhyme Shorts v4: Gul & Mishu chanting (E-I-E-I-O said in one go) over EXCITING kids music
(dance beat: kick, snare+clap, hats, bouncy bass, chords, tune on toy piano + lead). Own music only; PD tunes/words.
Reuses the rendered picture from rhyme_shorts.py (tools/_rhyme_<key>/v.mp4).

python tools/rhyme_v4.py
"""
import subprocess, sys, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(ROOT / "tools"))
import rhyme_shorts as RS

A, M, LS, SR = RS.A, RS.M, RS.LS, RS.SR
rng = np.random.default_rng(21)


def snare():
    n = int(0.2 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5 + np.diff(np.concatenate([[0], rng.standard_normal(n)])) * np.exp(-t / 0.06) * 0.8


def bass(m, d):
    f = A.mtof(m)
    n = int(d * SR)
    t = np.arange(n) / SR
    saw = 2 * ((f * t) % 1) - 1
    return (0.6 * np.sin(2 * np.pi * f * t) + 0.45 * np.convolve(saw, np.ones(12) / 12, mode="same")) * A.env(n, 0.004, 0.17)


def lead(m, d):
    f = A.mtof(m)
    n = int(d * SR)
    t = np.arange(n) / SR
    ph = np.cumsum(f * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t))) / SR
    x = np.sign(np.sin(2 * np.pi * ph)) * 0.5 + 0.25 * np.sin(4 * np.pi * ph)
    return np.convolve(x, np.ones(6) / 6, mode="same") * A.env(n, 0.01, 0.3)


def exciting_music(song, toks, total, beat):
    n = int(total * SR)
    m = np.zeros((n, 2))
    bars = int(round(total / (4 * beat)))
    for b in range(bars):
        ch = RS.CHORD[song["chords"][b % len(song["chords"])]]
        for q in range(4):
            tt = b * 4 * beat + q * beat
            A.add(m, LS.kick(), tt, 0.6)
            if q in (1, 3):
                A.add(m, snare(), tt, 0.35, 0.05)
                A.add(m, M.clap(), tt, 0.25, -0.05)
            for e in (0, 0.5):
                A.add(m, LS.hat(), tt + e * beat, 0.6, 0.3)
            for e, mm in ((0, ch[0] - 24), (0.5, ch[0] - 12), (0.75, ch[0] - 24)):
                A.add(m, bass(mm, beat * 0.42), tt + e * beat, 0.32)
            A.add(m, M.uke_chord([x + 12 for x in ch], 0.2), tt + beat / 2, 0.07, -0.3)
        if b % 2 == 1:                                           # little drum fill every 2 bars
            for k in range(4):
                A.add(m, snare(), b * 4 * beat + 3 * beat + k * beat / 4, 0.2 + 0.05 * k, 0.1)
    for tk in toks:                                              # the tune on toy piano + a bright lead
        k = len(tk["notes"])
        for i, nt in enumerate(tk["notes"]):
            at = tk["t"] + i * tk["dur"] / k
            A.add(m, M.toy_piano(nt + 12, 0.45), at, 0.1, 0.2)
            A.add(m, lead(nt + 12, min(0.4, tk["dur"] / k * 0.9)), at, 0.05, -0.2)
    return m


def vocals_v4(toks, total):
    """Like rhyme_shorts.vocals, but each E-I-E-I-O group is chanted as one phrase (sounds right)."""
    n = int(total * SR)
    v = np.zeros((n, 2))
    i = 0
    while i < len(toks):
        tk = toks[i]
        if tk["words"] == "E" and i + 4 < len(toks) and toks[i + 4]["words"] == "O":
            slot = toks[i + 4]["t"] + toks[i + 4]["dur"] * 0.6 - tk["t"]
            for who, g, pan in (("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)):
                A.add(v, RS.chant(who, "Ee-eye-ee-eye-oh", slot), tk["t"], g, pan)
            i += 5
            continue
        for who, g, pan in (("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)):
            A.add(v, RS.chant(who, tk["words"], tk["dur"]), tk["t"], g, pan)
        i += 1
    return v


def build(key, song, style, folder, name):
    toks, total, beat = RS.timeline(song)
    v = vocals_v4(toks, total)
    m = exciting_music(song, toks, total, beat)
    fx = np.zeros_like(m)
    for tk in toks:
        if style == "farm" and tk["words"] == "he had a cow":
            A.add(fx, RS.moo(), tk["t"] + tk["dur"] * 0.85, 0.5)
        if tk["words"] in ("O", "star", "high", "sky", "are"):
            A.add(fx, A.sfx_sparkle(), tk["t"], 0.2)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    m = m / np.abs(m).max() * (1 - 0.35 * e)[:, None]             # music ducks a little under the voices
    mix = v * 1.0 + m * 0.62 + fx * 0.4
    tmp = ROOT / "tools" / f"_rhyme_{key}"
    LS.finish_audio(mix, tmp / "a_v4.wav")
    out = ROOT / "VIDEOS" / folder / f"{name} v4.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "v.mp4"), "-i", str(tmp / "a_v4.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out)


if __name__ == "__main__":
    build("macdonald", RS.MACDONALD, "farm", "S14 Old MacDonald", "Old MacDonald - Short")
    build("twinkle", RS.TWINKLE, "night", "S15 Twinkle Twinkle", "Twinkle Twinkle - Short")
