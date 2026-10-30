"""v2 "Vehicles and what they do": calm, one vehicle at a time (name, job, real sound).

python edu.py  -> voices (approved kidvoice), timeline edu.json, vocal_gul/mishu.wav, mix.wav
"""
import json, sys, pathlib
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "voices"))
sys.path.insert(0, str(HERE.parent / "ep02-colours"))
import kidvoice
import audio_mix as A
import music as M                                    # instruments + vehicle sound effects

SR = A.SR
CACHE = HERE / "words"
CACHE.mkdir(exist_ok=True)

# key, name said by Mishu, job said by Gul, sound effect, background colour, job icon
VEHICLES = [
    ("firetruck", "Fire truck!", "It puts out fires!", "siren_euro", (255, 226, 214), "fire"),
    ("police", "Police car!", "It keeps us safe!", "siren", (214, 228, 255), "badge"),
    ("ambulance", "Ambulance!", "It helps sick people!", "siren", (255, 222, 230), "heart"),
    ("bus", "Big school bus!", "It takes kids to school!", "horn", (255, 243, 200), "abc"),
    ("train", "Train!", "It goes on tracks! Choo-choo!", "whistle", (214, 245, 222), "tracks"),
]
INTRO = [("both", "Let's learn vehicles!")]
OUTRO = [("mishu", "Which one do you like best?"), ("both", "Bye bye!")]


def line(who, text):
    import hashlib
    c = kidvoice.CHARACTERS[who]
    p = CACHE / f"line_{who}_{hashlib.md5((who + text + str(c)).encode()).hexdigest()[:10]}.wav"
    if not p.exists():
        kidvoice.say_as(who, text, p)
    x, sr = sf.read(p)
    idx = np.where(np.abs(x) > 0.03 * np.abs(x).max())[0]
    return x[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.05 * sr)]


def sfx(kind):
    if kind == "siren_euro":
        return M.siren(1.6, euro=True), 0.35
    if kind == "siren":
        return M.siren(1.6), 0.3
    if kind == "horn":
        h = M.horn()
        x = np.zeros(int(0.9 * SR))
        for t0 in (0.0, 0.3):
            x[int(t0 * SR): int(t0 * SR) + len(h)] += h
        return x, 0.6
    w = M.train_whistle()
    x = np.zeros(int(1.6 * SR))
    for q in range(8):
        c = M.chuff()
        x[int(q * 0.2 * SR): int(q * 0.2 * SR) + len(c)] += c * 0.6
    x[int(0.7 * SR): int(0.7 * SR) + len(w)] += w
    return x, 0.4


def build():
    ev, segs = [], []                               # spoken lines, vehicle segments
    voc = {"gul": [], "mishu": []}
    t = 0.6

    def say(who, text, at):
        for s in (["gul", "mishu"] if who == "both" else [who]):
            x = line(s, text)
            voc[s].append((at, x * (0.8 if who == "both" else 1.0)))
        d = max(len(line(s, text)) for s in (["gul", "mishu"] if who == "both" else [who])) / SR
        ev.append(dict(who=who, text=text, t=round(at, 3), dur=round(d, 3)))
        return d

    t += say(*INTRO[0], t) + 0.5
    intro_end = t
    fx = []
    for key, name, job, snd, col, icon in VEHICLES:
        s = dict(key=key, name=name.rstrip("!").upper(), col=col, icon=icon, t0=round(t, 3))
        t += 0.9                                    # drive in
        s["t_name"] = round(t, 3)
        t += say("mishu", name, t) + 0.35
        s["t_job"] = round(t, 3)
        t += say("gul", job, t) + 0.25
        x, g = sfx(snd)
        s["t_sound"] = round(t, 3)
        fx.append((t, x, g))
        t += len(x) / SR + 0.1
        s["t_out"] = round(t, 3)
        t += 0.55                                   # drive out
        s["t1"] = round(t, 3)
        segs.append(s)
    outro = round(t, 3)
    t += 0.8                                        # line-up appears
    t += say(*OUTRO[0], t) + 0.4
    t += say(*OUTRO[1], t) + 0.9
    total = round(t, 2)
    n = int(total * SR)
    tracks = {}
    for s, items in voc.items():
        y = np.zeros(n)
        for at, x in items:
            i = int(at * SR)
            y[i:i + len(x)] += x[: n - i]
        tracks[s] = y
        sf.write(HERE / f"vocal_{s}.wav", (y / max(1e-9, np.abs(y).max()) * 0.9).astype(np.float32), SR, subtype="PCM_16")
    json.dump(dict(events=ev, segs=segs, intro_end=intro_end, outro=outro, total=total), open(HERE / "edu.json", "w"), indent=1)
    # soft music: ukulele + toy piano only, no drums
    mus = np.zeros((n, 2))
    B = 0.5
    prog = M.PROG
    k, bar = 0, 0.0
    tune = [72, 76, 79, 76, 77, 74, 72, 67]
    while bar < total:
        ch = prog[k % 4]
        for q in range(4):
            tt = bar + q * B
            A.add(mus, M.uke_chord([x + 12 for x in ch]), tt + B / 2, 0.05, -0.2)
            if q in (0, 2):
                A.add(mus, M.tuba(ch[0] - 24, B * 0.8), tt, 0.16)
        for q in range(2):
            A.add(mus, M.toy_piano(tune[(k * 2 + q) % 8] + 12), bar + q * 2 * B, 0.035, 0.2)
        bar += 4 * B
        k += 1
    tt = np.arange(n) / SR
    mus *= (np.clip(tt / 0.5, 0, 1) * np.clip((total - tt) / 1.0, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.1)
    A.add(v, tracks["mishu"], 0, 1.0, 0.1)
    v /= np.abs(v).max() / 0.9
    f = np.zeros((n, 2))
    for at, x, g in fx:
        A.add(f, x, at, g)
    for s in segs:                                  # soft whoosh as each vehicle drives in and out
        A.add(f, A.sfx_whoosh(), s["t0"] + 0.2, 0.12)
        A.add(f, A.sfx_whoosh(), s["t_out"], 0.12)
    mix = v + mus / max(1e-9, np.abs(mus).max()) * 0.22 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    sf.write(HERE / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s, {len(ev)} lines")


if __name__ == "__main__":
    build()
