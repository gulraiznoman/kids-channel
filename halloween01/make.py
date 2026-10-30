"""Halloween Short 1: "Getting Ready for Halloween" (story: Gul & Mishu prepare, the scene fills up).

python make.py -> timeline.json, vocal_gul.wav, vocal_mishu.wav, mix.wav
"""
import hashlib, json, subprocess, sys, pathlib
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "voices"))
sys.path.insert(0, str(ROOT / "ep02-colours"))
sys.path.insert(0, str(ROOT / "song01-animal-dance"))
import kidvoice
import audio_mix as A
import music as M

SR = A.SR
CACHE = HERE / "words"
CACHE.mkdir(exist_ok=True)

# step key, big word on screen, lines (who, text, cue at line start), sound effect after the lines
STEPS = [
    ("intro", None, [("mishu", "Halloween is coming!", None), ("gul", "Let's get ready!", None)], None),
    ("pumpkin", "PUMPKIN!", [("gul", "Look! A big orange pumpkin!", None)], "boing"),
    ("carve", "JACK-O'-LANTERN!", [("mishu", "Let's give it a happy face!", None), ("gul", "Jack-o'-lantern!", "glow")], None),
    ("costume", "COSTUMES!", [("gul", "Costume time! I'm a pumpkin!", "hat_gul"), ("mishu", "And I'm a little witch!", "hat_misheal")], None),
    ("bat", "BAT!", [("mishu", "A little bat! Flap, flap!", None)], "flap"),
    ("ghost", "GHOST!", [("gul", "A friendly ghost! Boo!", None), ("mishu", "Hello, ghosty!", None)], None),
    ("blackcat", "BLACK CAT!", [("mishu", "A black cat!", None)], "meow"),
    ("candy", "TRICK OR TREAT!", [("both", "Trick or treat!", None), ("gul", "Yummy candy!", "candy")], None),
    ("end", "HAPPY HALLOWEEN!", [("both", "Happy Halloween!", "party")], None),
]


def line(who, text):
    c = kidvoice.CHARACTERS[who]
    p = CACHE / f"{who}_{hashlib.md5((who + text + str(c)).encode()).hexdigest()[:10]}.wav"
    if not p.exists():
        kidvoice.say_as(who, text, p)
    x, sr = sf.read(p)
    idx = np.where(np.abs(x) > 0.03 * np.abs(x).max())[0]
    return x[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.05 * sr)]


def load_mp3(path, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR)] + (["-t", str(dur)] if dur else []) + ["-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(float)
    return x / max(1e-9, np.abs(x).max())


def flap():
    rng = np.random.default_rng(2)
    out = np.zeros(int(0.9 * SR))
    for k in range(5):
        n = int(0.08 * SR)
        x = np.convolve(rng.standard_normal(n), np.ones(30) / 30, mode="same") * A.env(n, 0.005, 0.03)
        i = int(k * 0.17 * SR)
        out[i:i + n] += x * 4
    return out


SFX = {
    "boing": lambda: (M.boing(), 0.35),
    "flap": lambda: (flap(), 0.5),
    "meow": lambda: (line("gul", "Meow, meow!") * 1.0, 0.9),          # own voice, no stock sound (channel rule)
}


def build():
    ev, steps = [], []
    voc = {"gul": [], "mishu": []}
    fx = []
    t = 0.5
    for key, word, lines, after in STEPS:
        s = dict(key=key, word=word, t0=round(t, 3), cues={})
        t += 0.6 if key != "intro" else 0.0                # item arrives before the line
        for who, text, cue in lines:
            if cue:
                s["cues"][cue] = round(t, 3)
            singers = ["gul", "mishu"] if who == "both" else [who]
            d = 0
            for sname in singers:
                x = line(sname, text)
                voc[sname].append((t, x * (0.8 if who == "both" else 1.0)))
                d = max(d, len(x) / SR)
            ev.append(dict(who=who, text=text, t=round(t, 3), dur=round(d, 3)))
            t += d + 0.35
        if after:
            x, g = SFX[after]()
            fx.append((t, x, g))
            s["cues"]["sfx"] = round(t, 3)
            t += len(x) / SR * 0.8
        t += 0.3
        s["t1"] = round(t, 3)
        steps.append(s)
    t += 1.2                                               # hold the finished scene
    total = round(t, 2)
    n = int(total * SR)
    tracks = {}
    for sname, items in voc.items():
        y = np.zeros(n)
        for at, x in items:
            i = int(at * SR)
            y[i:i + len(x)] += x[: n - i]
        tracks[sname] = y
        sf.write(HERE / f"vocal_{sname}.wav", (y / max(1e-9, np.abs(y).max()) * 0.9).astype(np.float32), SR, subtype="PCM_16")
    json.dump(dict(events=ev, steps=steps, total=total), open(HERE / "timeline.json", "w"), indent=1)

    # playful "spooky-cute" backing: plucky bass walk + xylophone, soft, no drums
    mus = np.zeros((n, 2))
    B = 0.5
    walk = [45, 48, 50, 51, 52, 51, 50, 48]               # A C D Eb E Eb D C (cartoon spooky walk)
    tune = [69, 72, 76, 75, 76, 72, 69, 0, 69, 72, 74, 72, 71, 67, 69, 0]
    i, tt = 0, 0.0
    while tt < total:
        A.add(mus, M.tuba(walk[i % 8], B * 0.7), tt, 0.22)
        if i % 2 == 1:
            A.add(mus, M.uke_chord([69, 72, 76] if (i // 8) % 2 == 0 else [62, 65, 69]), tt, 0.04, -0.25)
        nt = tune[i % 16]
        if nt:
            A.add(mus, M.xylo(nt + 12), tt, 0.09, 0.25)
        tt += B
        i += 1
    ts = np.arange(n) / SR
    mus *= (np.clip(ts / 0.4, 0, 1) * np.clip((total - ts) / 1.0, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.1)
    A.add(v, tracks["mishu"], 0, 1.0, 0.1)
    v /= np.abs(v).max() / 0.9
    f = np.zeros((n, 2))
    for at, x, g in fx:
        A.add(f, x, at, g)
    for s in steps:                                        # magic sparkle as each new thing appears
        if s["key"] not in ("intro",):
            A.add(f, A.sfx_sparkle(), s["t0"] + 0.1, 0.18)
        for cue in ("glow", "hat_gul", "hat_misheal", "candy", "party"):
            if cue in s["cues"]:
                A.add(f, A.sfx_sparkle(), s["cues"][cue], 0.25)
                A.add(f, A.sfx_pop(), s["cues"][cue], 0.3)
    mix = v + mus / max(1e-9, np.abs(mus).max()) * 0.24 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    sf.write(HERE / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s, {len(ev)} lines")


if __name__ == "__main__":
    build()
