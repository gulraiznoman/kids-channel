"""Soundtrack: voice lines + gentle original music + sound effects.  python audio_mix.py OUT.wav"""
import json, sys, wave, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
SR = 48000
BPM = 112
BEAT = 60 / BPM


def env(n, a=0.003, d=0.25):
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    na = max(1, int(a * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)


def tone(f, dur, harm=((1, 1),), a=0.003, d=0.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return sum(amp * np.sin(2 * np.pi * f * k * t) for k, amp in harm) * env(n, a, d)


def add(buf, x, t0, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= len(buf):
        return
    x = x[:len(buf) - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(x), 0] += x * g * l
    buf[i:i + len(x), 1] += x * g * r


def read_wav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def music(total):
    """Light 'garden' loop: ukulele-ish plucks, marimba melody, soft shaker. C-F-G-C / Am-F-G-C."""
    rng = np.random.default_rng(1)
    n = int(total * SR)
    m = np.zeros((n, 2))
    prog = [[60, 64, 67], [53, 57, 60], [55, 59, 62], [60, 64, 67],
            [57, 60, 64], [53, 57, 60], [55, 59, 62], [60, 64, 67]]
    melody = [76, 79, 81, 79, 76, 74, 72, 74, 76, 74, 72, 69, 72, 74, 76, 72]
    uke = ((1, 1), (2, 0.5), (3, 0.3), (4, 0.15), (5, 0.08))
    mar = ((1, 1), (4, 0.2), (10, 0.04))
    shaker_n = rng.standard_normal(int(0.05 * SR))
    shaker_n = np.diff(np.concatenate([[0], shaker_n])) * env(len(shaker_n), 0.002, 0.012)
    bar = 4 * BEAT
    t, b = 0.0, 0
    while t < total:
        ch = prog[b % len(prog)]
        for k in range(8):                                   # strummed 8ths
            tt = t + k * BEAT / 2
            acc = 1.0 if k % 2 == 0 else 0.6
            for j, note in enumerate(ch):
                add(m, tone(mtof(note + 2), 0.5, uke, 0.002, 0.16), tt + j * 0.012, 0.035 * acc, -0.25)
            add(m, shaker_n, tt + BEAT / 4, 0.05, 0.35)
        add(m, tone(mtof(ch[0] - 10), bar, ((1, 1), (2, 0.3)), 0.01, 0.9), t, 0.09)
        if b % 2 == 0:                                       # melody every other bar pair
            for k in range(8):
                note = melody[(b * 4 + k) % len(melody)]
                add(m, tone(mtof(note + 2), 0.6, mar, 0.002, 0.22), t + k * BEAT / 2, 0.05, 0.2)
        t += bar
        b += 1
    tt = np.arange(n) / SR
    fade = np.clip(tt / 1.5, 0, 1) * np.clip((total - tt) / 2.5, 0, 1)
    return m * fade[:, None]


def sfx_pop():
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    f = 300 + 900 * t / 0.18
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.06)


def sfx_sparkle():
    out = np.zeros(int(1.0 * SR))
    for k, m in enumerate([84, 88, 91, 96]):
        x = tone(mtof(m), 0.8, ((1, 1), (2.01, 0.3)), 0.002, 0.25)
        i = int(k * 0.07 * SR)
        out[i:i + len(x)] += x[:len(out) - i]
    return out


def sfx_whoosh():
    rng = np.random.default_rng(3)
    n = int(0.45 * SR)
    x = rng.standard_normal(n)
    # crude band sweep: smooth with moving average of shrinking width
    y = np.convolve(x, np.ones(40) / 40, mode="same") - np.convolve(x, np.ones(400) / 400, mode="same")
    shape = np.sin(np.linspace(0, np.pi, n)) ** 2
    return y * shape * 2.0


def sfx_ding(m=79):
    return tone(mtof(m), 0.5, ((1, 1), (3, 0.2)), 0.002, 0.15)


if __name__ == "__main__":
    tl = json.load(open(HERE / "timeline.json"))
    total = tl["total"]
    n = int(total * SR)
    voice = np.zeros((n, 2))
    fx = np.zeros((n, 2))
    pop, spark, whoosh = sfx_pop(), sfx_sparkle(), sfx_whoosh()
    for b in tl["beats"]:
        if "wav" in b:
            x = read_wav(HERE / "audio" / b["wav"])
            add(voice, x, b["t"], 1.0, -0.15 if b["who"] == "gul" else 0.15)
        if "fruit_in" in b:
            add(fx, pop, b["t"] + 0.05, 0.35)
        if "fruit_out" in b:
            add(fx, whoosh, b["t"], 0.25)
        if b.get("stars"):
            add(fx, spark, b["t"], 0.22)
        if "spell" in b:
            for i in range(len(b["spell"])):
                add(fx, sfx_ding(72 + [0, 2, 4, 7, 9, 12, 14, 16, 19, 21][i % 10]), b["t"] + i * 0.11, 0.07)
        if b.get("prompt"):
            add(fx, sfx_ding(84), b["t"], 0.15)
    voice /= max(1e-9, np.abs(voice).max()) / 0.9
    mus = music(total)
    mix = voice + fx + mus * 1.4
    mix /= max(1e-9, np.abs(mix).max()) / 0.9
    with wave.open(sys.argv[1], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
    print("wrote", sys.argv[1], f"{total:.1f}s")
