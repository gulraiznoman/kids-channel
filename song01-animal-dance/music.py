"""v3 children's backing for "Animal Dance" + mix with the chanted vocals.  python music.py -> mix.wav

Toy piano plays the tune, xylophone fills the gaps, boom-chick tuba + ukulele, hand claps,
shaker, slide whistles and a kids' "Yay!" at the end.
"""
import json, sys, pathlib
import numpy as np, soundfile as sf
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "ep02-colours"))
import audio_mix as A                      # tone/env/add/mtof helpers from the episode engine
import song

SR = A.SR
B = song.BEAT
rng = np.random.default_rng(5)


def env_ad(n, a, d):
    return A.env(n, a, d)


def toy_piano(m, dur=0.7):
    """Bright, slightly out-of-tune metal bars: what toy pianos sound like."""
    f = A.mtof(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / 0.08)
         + 0.35 * np.sin(2 * np.pi * f * 3.97 * t) * np.exp(-t / 0.04) + 0.2 * np.sin(2 * np.pi * f * 6.3 * t) * np.exp(-t / 0.02))
    return x * env_ad(n, 0.001, 0.32)


def xylo(m, dur=0.35):
    f = A.mtof(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t / 0.02)
    return x * env_ad(n, 0.001, 0.09)


def tuba(m, dur):
    f = A.mtof(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) + 0.2 * np.sin(2 * np.pi * 3 * f * t)
    e = np.minimum(1, t / 0.03) * np.exp(-t / 0.35)
    return x * e


def uke_chord(ch, dur=0.35):
    out = np.zeros(int((dur + 0.05) * SR))
    for j, nt in enumerate(ch):
        x = A.tone(A.mtof(nt), dur, ((1, 1), (2, 0.5), (3, 0.3), (4, 0.15)), 0.002, 0.12)
        i = int(j * 0.012 * SR)
        out[i:i + len(x)] += x[: len(out) - i]
    return out


def clap():
    n = int(0.18 * SR)
    x = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
    t = np.arange(n) / SR
    e = sum(np.exp(-np.clip(t - d, 0, None) / 0.025) * (t >= d) for d in (0, 0.01, 0.022))
    return x * e * 0.4


def shaker():
    n = int(0.06 * SR)
    return np.diff(np.concatenate([[0], rng.standard_normal(n)])) * env_ad(n, 0.004, 0.015)


def slide_whistle(f0, f1, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.015 * np.sin(2 * np.pi * 6 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.05)


def stomp():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(45 + 70 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.15)


def boing():
    n = int(0.4 * SR)
    t = np.arange(n) / SR
    f = 220 * 2 ** (1.6 * t / 0.4) * (1 + 0.08 * np.sin(2 * np.pi * 18 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2)


def quack():                                # cartoon duck: nasal buzz with a falling pitch
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    f = 520 - 180 * t / 0.22
    ph = np.cumsum(f) / SR
    saw = 2 * (ph % 1) - 1
    return np.tanh(3 * saw * np.sin(2 * np.pi * ph * 2.02)) * env_ad(n, 0.005, 0.09)


SFX = {"stomp": (stomp, 0.9), "jump": (boing, 0.45), "swing": (lambda: slide_whistle(500, 1300, 0.35), 0.25),
       "quack": (quack, 0.35)}
PROG = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]    # C F G C


def backing(total, notes, spans):
    n = int(total * SR)
    m = np.zeros((n, 2))
    cl, sh = clap(), shaker()
    bar, b, t = 4 * B, 0, 0.0
    while t < total - 0.5:
        ch = PROG[b % 4]
        for q in range(4):
            tt = t + q * B
            if q % 2 == 0:                                       # boom ...
                A.add(m, tuba(ch[0] - 24 + (7 if q == 2 else 0), B * 0.8), tt, 0.32)
            else:                                                # ... chick
                A.add(m, uke_chord([x + 12 for x in ch]), tt, 0.06, -0.3)
                A.add(m, cl, tt, 0.22, 0.15)
            A.add(m, sh, tt + B / 2, 0.06, 0.4)
            A.add(m, sh, tt, 0.035, 0.4)
        t += bar
        b += 1
    # toy piano doubles the tune (one octave up, soft so the words stay on top)
    for who, word, beat, beats, midi in notes:
        ns = midi if isinstance(midi, list) else [midi]
        for i, nt in enumerate(ns):
            A.add(m, toy_piano(nt + 12), (beat + i * beats / len(ns)) * B, 0.05, 0.2)
    # xylophone answers in the gaps: a little run at the end of each verse
    for b0, b1, who, key, act in spans:
        for i, nt in enumerate((72, 74, 76, 79)):
            A.add(m, xylo(nt + 12), (b0 + 7 + i * 0.25) * B, 0.12, -0.2)
        for i, nt in enumerate((79, 76)):
            A.add(m, xylo(nt + 12), (b0 + 3 + i * 0.5) * B, 0.1, 0.2)
    # slide whistles: intro and into the chorus
    A.add(m, slide_whistle(400, 1400, 0.6), 0.1, 0.12)
    A.add(m, slide_whistle(500, 1600, 0.5), (spans[-1][1] - 1) * B, 0.12)
    tt = np.arange(n) / SR
    return m * (np.clip(tt / 0.2, 0, 1) * np.clip((total - tt) / 0.8, 0, 1))[:, None]


if __name__ == "__main__":
    import sing
    meta = json.load(open("notes.json"))
    total = meta["total"] + 0.8
    notes, end_beats = song.notes()
    spans = song.verse_spans()
    mus = backing(total, notes, spans)
    n = len(mus)
    voc = np.zeros((n, 2))
    for s, pan in (("gul", -0.12), ("mishu", 0.12)):
        x, _ = sf.read(f"vocal_{s}.wav")
        A.add(voc, x[:n], 0, 1.0, pan)
    for s, pan in (("gul", -0.3), ("mishu", 0.3)):              # kids cheer at the end
        A.add(voc, sing.chant(s, "Yay", 2, 72), (end_beats - 1.6) * B, 0.7, pan)
    fx = np.zeros((n, 2))
    for b0, b1, who, key, act in spans:
        f, g = SFX[act]
        hits = (7.25, 7.6) if act == "quack" else (4, 5, 6)      # duck quacks answer after the words
        for q in hits:
            A.add(fx, f(), (b0 + q) * B + 0.02, g)
    voc /= np.abs(voc).max() / 0.9
    e = np.abs(voc).mean(axis=1)                                 # duck the music a little while they chant
    win = int(0.08 * SR)
    e = np.convolve(e, np.ones(win) / win, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.3 * e)[:, None]
    mix = voc * 1.0 + mus * 0.55 + fx * 0.3
    mix /= np.abs(mix).max() / 0.9
    sf.write("mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print("mix.wav", round(total, 1), "s")
