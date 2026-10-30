"""Original upbeat backing for "Animal Dance" + mix with vocals.  python music.py -> mix.wav"""
import json, sys, pathlib
import numpy as np, soundfile as sf
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "ep02-colours"))
import audio_mix as A                      # tone/env/add/mtof helpers from the episode engine
import song

SR = A.SR
B = song.BEAT
rng = np.random.default_rng(5)


def kick():
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)


def clap():
    n = int(0.2 * SR); x = rng.standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))
    e = sum(np.exp(-np.clip(np.arange(n) / SR - d, 0, None) / 0.03) * (np.arange(n) / SR >= d) for d in (0, 0.012, 0.024))
    return x * e * 0.5


def hat():
    n = int(0.05 * SR); x = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
    return x * A.env(n, 0.001, 0.01)


def stomp():                                # big low thud for the elephant
    n = int(0.5 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.18)


def boing():                                # bunny hop
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 300 + 500 * np.sin(np.pi * t / 0.35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.15)


def whoosh():                               # monkey swing
    return A.sfx_whoosh()


SFX = {"stomp": (stomp, 0.8), "jump": (boing, 0.35), "swing": (whoosh, 0.5), "quack": (None, 0)}


def backing(total, notes):
    n = int(total * SR)
    m = np.zeros((n, 2))
    prog = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]    # C F G C
    k, c, h = kick(), clap(), hat()
    uke = ((1, 1), (2, 0.5), (3, 0.3), (4, 0.15))
    bar, b = 4 * B, 0
    t = 0.0
    while t < total - 0.5:
        ch = prog[b % 4]
        for q in range(4):
            tt = t + q * B
            A.add(m, k, tt, 0.55 if q % 2 == 0 else 0.35)
            if q % 2 == 1:
                A.add(m, c, tt, 0.35, 0.1)
            A.add(m, h, tt + B / 2, 0.12, 0.4)
            A.add(m, A.tone(A.mtof(ch[0] - 24 + (7 if q == 2 else 0)), B * 0.9, ((1, 1), (2, 0.4), (3, 0.15)), 0.004, 0.25), tt, 0.32)
            for j, nt in enumerate(ch):        # off-beat ukulele chops
                A.add(m, A.tone(A.mtof(nt), 0.3, uke, 0.002, 0.1), tt + B / 2 + j * 0.01, 0.05, -0.3)
        t += bar; b += 1
    for who, word, beat, beats, midi in notes:  # glockenspiel doubles the tune so it reads as a song
        if who not in ("both", "gul") and any(w == word and wh == "both" for wh, w, *_ in notes):
            continue
        ns = midi if isinstance(midi, list) else [midi]
        for i, nt in enumerate(ns):
            A.add(m, A.tone(A.mtof(nt + 12), 0.8, ((1, 1), (2.76, 0.25), (5.4, 0.08)), 0.002, 0.35),
                  (beat + i * beats / len(ns)) * B, 0.022, 0.25)
    tt = np.arange(n) / SR
    return m * (np.clip(tt / 0.3, 0, 1) * np.clip((total - tt) / 0.8, 0, 1))[:, None]


if __name__ == "__main__":
    meta = json.load(open("notes.json"))
    total = meta["total"] + 0.5
    notes, _ = song.notes()
    mus = backing(total, notes)
    n = len(mus)
    voc = np.zeros((n, 2))
    for s, pan in (("gul", -0.12), ("mishu", 0.12)):
        x, _ = sf.read(f"vocal_{s}.wav")
        A.add(voc, x[:n], 0, 1.0, pan)
    fx = np.zeros((n, 2))
    for b0, b1, who, key, act in song.verse_spans():
        f, g = SFX[act]
        if f:
            for q in (4, 5, 6):
                A.add(fx, f(), (b0 + q) * B, g)
    # voice presence: lift 2-5 kHz so words cut through the music
    for ch in range(2):
        v = voc[:, ch]
        lo = np.convolve(v, np.ones(10) / 10, mode="same")             # < ~4.8 kHz
        lo2 = np.convolve(v, np.ones(24) / 24, mode="same")            # < ~2 kHz
        voc[:, ch] = v + 0.9 * (lo - lo2)
    voc /= np.abs(voc).max() / 0.9
    # duck the music while anyone sings
    e = np.abs(voc).mean(axis=1)
    win = int(0.08 * SR)
    e = np.convolve(e, np.ones(win) / win, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    duck = 1 - 0.45 * e
    mus = mus / max(1e-9, np.abs(mus).max()) * duck[:, None]
    mix = voc * 1.0 + mus * 0.45 + fx * 0.3
    mix /= np.abs(mix).max() / 0.9
    sf.write("mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print("mix.wav", round(total, 1), "s")
