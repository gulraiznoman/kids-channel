"""Short "What's Inside?": cut-open surprise reveals (apple star, orange wheel, watermelon, tomato). 1080x1920.

python short.py audio      -> timeline.json, vocal_*.wav, mix.wav
python short.py frames N,N -> preview PNGs
python short.py video      -> VIDEOS/S04 What's Inside/What's Inside - Short vN.mp4
"""
import hashlib, json, math, os, subprocess, sys, pathlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "voices"))
sys.path.insert(0, str(ROOT / "ep02-colours"))
sys.path.insert(0, str(ROOT / "song01-animal-dance"))
sys.path.insert(0, str(ROOT / "long02-counting"))
import render as R                                     # text / item / paste helpers (long02)

W, H, FPS = 1080, 1920, 30
OUT = ROOT / "VIDEOS" / "S04 What's Inside"
INK, RAINBOW = R.INK, R.RAINBOW
SR = 48000
CACHE = HERE / "words"
CACHE.mkdir(exist_ok=True)
# whole art (file), inside art (file), question asker, question, answer
FRUITS = [
    (ROOT / "ep01-fruits/art/fruit_apple.png", HERE / "art/item_apple_half.png", "mishu", "What's inside the apple?", "A hidden star! With little seeds!", "A STAR!"),
    (ROOT / "ep01-fruits/art/fruit_orange.png", HERE / "art/item_orange_half.png", "gul", "What's inside the orange?", "Juicy slices, like a wheel!", "SLICES!"),
    (HERE / "art/item_watermelon_whole.png", HERE / "art/item_watermelon_half.png", "mishu", "What's inside the watermelon?", "Red and juicy, with black seeds!", "RED & JUICY!"),
    (ROOT / "long03-fruits-veg/art/item_tomato.png", HERE / "art/item_tomato_half.png", "gul", "What's inside the tomato?", "Tiny seeds, in little rooms!", "TINY SEEDS!"),
]
CHAR = {"gul": dict(outfit="tee", x=250, girl=False, voc="gul"), "misheal": dict(outfit="pink", x=830, girl=True, voc="mishu")}
S = 0.31


# ================================================================== audio
def build_audio():
    import kidvoice
    import audio_mix as A
    import music as M

    def line(who, text):
        c = kidvoice.CHARACTERS[who]
        p = CACHE / f"{who}_{hashlib.md5((who + text + str(c)).encode()).hexdigest()[:10]}.wav"
        if not p.exists():
            kidvoice.say_as(who, text, p)
        x, sr = sf.read(p)
        idx = np.where(np.abs(x) > 0.03 * np.abs(x).max())[0]
        return x[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.05 * sr)]

    t, lines, voc, steps, fx = 0.4, [], {"gul": [], "mishu": []}, [], []

    def say(who, text, gap):
        nonlocal t
        singers = ["gul", "mishu"] if who == "both" else [who]
        d = 0
        for s in singers:
            x = line(s, text)
            voc[s].append((t, x * ((0.9 if s == "mishu" else 0.45) if who == "both" else 1.0)))
            d = max(d, len(x) / SR)
        lines.append(dict(who=who, text=text, t=round(t, 3), dur=round(d, 3)))
        st = t
        t += d + gap
        return round(st, 3)

    say("mishu", "What's inside? Let's find out!", 0.3)
    intro_end = t
    for k, (_, _, who, q, a, word) in enumerate(FRUITS):
        other = "gul" if who == "mishu" else "mishu"
        s = dict(t0=round(t, 3))
        fx.append(("pop", t))
        t += 0.45
        s["q_t"] = say(who, q, 0.9)                     # a beat to guess
        s["cut_t"] = round(t, 3)
        fx.append(("chop", t))
        t += 0.55
        s["a_t"] = say(other, a, 0.5)
        s["t1"] = round(t, 3)
        steps.append(s)
    end_t = say("both", "Which one is your favourite?", 1.2)
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
    json.dump(dict(lines=lines, steps=steps, intro_end=intro_end, end_t=end_t, total=total), open(HERE / "timeline.json", "w"), indent=1)
    # music: G major, 112 BPM, plucky kalimba-like tune + soft claps (new sound for this Short)
    mus = np.zeros((n, 2))
    B = 60 / 112
    tune = [67, 71, 74, 71, 72, 69, 66, 69, 67, 71, 74, 79, 76, 74, 71, 0]
    bass = [43, 43, 48, 50]
    i, tt = 0, 0.0
    while tt < total:
        if tune[i % 16]:
            A.add(mus, M.toy_piano(tune[i % 16], 0.5), tt, 0.05, 0.2)
        if i % 4 == 0:
            A.add(mus, M.tuba(bass[(i // 4) % 4], B * 2.5), tt, 0.18)
        if i % 4 == 2:
            A.add(mus, M.clap(), tt, 0.12, 0.1)
        tt += B / 2
        i += 1
    ts = np.arange(n) / SR
    mus *= (np.clip(ts / 0.3, 0, 1) * np.clip((total - ts) / 0.8, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.12)
    A.add(v, tracks["mishu"], 0, 1.0, 0.12)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.4 * e)[:, None]
    rng = np.random.default_rng(6)
    f = np.zeros((n, 2))
    for kind, at in fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.3)
        else:
            m = int(0.25 * SR)
            tt2 = np.arange(m) / SR
            thud = np.sin(2 * np.pi * np.cumsum(150 * np.exp(-tt2 / 0.04) + 60) / SR) * np.exp(-tt2 / 0.06)
            swish = np.convolve(rng.standard_normal(m), np.ones(3) / 3, mode="same") * np.exp(-((tt2 - 0.08) / 0.05) ** 2) * 0.5
            A.add(f, swish, at, 0.5)
            A.add(f, thud, at + 0.15, 0.7)
            A.add(f, A.sfx_sparkle(), at + 0.25, 0.25)
    mix = v + mus * 0.24 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    sf.write(HERE / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s")


# ================================================================== video
G = R.G


def init():
    G.update(json.load(open(HERE / "timeline.json")))
    G["fonts"], G["cache"], G["sized"] = {}, {}, {}
    G["art"] = {}
    for k, (whole, half, *_r) in enumerate(FRUITS):
        G["art"][f"w{k}"] = Image.open(whole).convert("RGBA")
        G["art"][f"h{k}"] = Image.open(half).convert("RGBA")
    bg = Image.open(ROOT / "long03-fruits-veg/art/bg_kitchen.png").convert("RGBA")
    k = H / bg.height
    bg = bg.resize((int(bg.width * k), H), Image.LANCZOS)
    x0 = (bg.width - W) // 2
    G["bg"] = bg.crop((x0, 0, x0 + W, H))
    G["layers"] = {}
    for n in CHAR:
        G["layers"][n] = {p.stem: (lambda im: im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS))(Image.open(p))
                          for p in (R.KIT / n).glob("*.png")}
    G["env"] = {}
    for n, c in CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)


def board(frame):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((120, 1120, 960, 1230), radius=40, fill=(205, 150, 90), outline=INK, width=8)
    d.ellipse((880, 1150, 920, 1190), fill=(150, 100, 60), outline=INK, width=5)


def knife(frame, k):
    """Knife slicing down through the fruit, k in 0..1."""
    d = ImageDraw.Draw(frame)
    y = 420 + 700 * k
    d.polygon([(330, y), (760, y - 60), (760, y + 30), (330, y + 40)], fill=(225, 232, 240), outline=INK)
    d.rounded_rectangle((760, y - 70, 930, y + 40), radius=24, fill=(255, 90, 110), outline=INK, width=6)


def kids(frame, t):
    for n, c in CHAR.items():
        L = G["layers"][n]
        o = c["outfit"]
        env = G["env"][n]
        v = env[min(int(t * FPS), len(env) - 1)]
        talking = v > 0.12
        mouth = "smile" if not talking else ("o" if v < 0.5 else "open")
        im = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for p in (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}"]:
            im.alpha_composite(L[p])
        im.alpha_composite(L[f"arm_r_wave_{o}"] if talking else L[f"arm_r_down_{o}"])
        for p in ["neck", "head", "eyes_blink" if (t + (1 if n == "gul" else 0)) % 3.9 < 0.12 else "eyes_open", "brows",
                  f"mouth_{mouth}", "hair_front"] + (["earrings"] if c["girl"] else []):
            im.alpha_composite(L[p])
        hop = 12 * abs(math.sin(t * 5)) if talking else 4 * abs(math.sin(t * 1.5 + (1 if n == "gul" else 0)))
        frame.alpha_composite(im, (int(c["x"] - im.width / 2), int(1890 - im.height - hop)))


def render_frame(f):
    t = f / FPS
    frame = G["bg"].copy()
    board(frame)
    steps = G["steps"]
    cur = next((k for k, s in enumerate(steps) if s["t0"] <= t < s["t1"]), None)
    if t < G["intro_end"]:
        R.rainbow_text(frame, W / 2, 330, "WHAT'S", int(170 * R.ease_back(t / 0.4)), maxw=980)
        R.rainbow_text(frame, W / 2, 520, "INSIDE?", int(190 * R.ease_back((t - 0.2) / 0.4)), maxw=980)
        for k in range(4):                                                  # the four fruits waiting in a row
            R.paste(frame, f"w{k}", 180 + k * 240, 960 - 15 * abs(math.sin(t * 4 + k)), 210 * R.ease_back((t - 0.3 - k * 0.12) / 0.4))
    elif cur is not None:
        s = steps[cur]
        a = t - s["t0"]
        cx, cy = 540, 860
        bob = 8 * math.sin(t * 2.4)
        if t < s["cut_t"]:
            R.paste(frame, f"w{cur}", cx, cy + bob, 640 * R.ease_back(a / 0.4))
            R.rainbow_text(frame, W / 2, 330, "WHAT'S INSIDE?", int(120 * R.ease_back(a / 0.35)), maxw=980)
            if t > s["q_t"] + 0.6:                                          # little "?" wobble while guessing
                R.rainbow_text(frame, 860, 560, "?", int(170 + 15 * math.sin(t * 8)), colour=(255, 255, 255))
        elif t < s["cut_t"] + 0.35:
            k = (t - s["cut_t"]) / 0.35
            R.paste(frame, f"w{cur}", cx, cy + bob, 640)
            knife(frame, k)
        else:
            k = (t - s["cut_t"] - 0.35) / 0.4
            lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))                # soft glow behind the reveal
            dd = ImageDraw.Draw(lay)
            dd.ellipse((cx - 380, cy - 380, cx + 380, cy + 380), fill=(255, 255, 255, 170))
            frame.alpha_composite(lay)
            R.paste(frame, f"h{cur}", cx, cy + bob, 660 * R.ease_back(k), 0)
            d = ImageDraw.Draw(frame)
            for j in range(12):
                q = min(1, (t - s["cut_t"] - 0.35) / 0.8)
                if q < 1:
                    ang = j / 12 * 2 * math.pi
                    R.star(d, cx + (300 + 160 * q) * math.cos(ang), cy + (300 + 160 * q) * math.sin(ang), int(30 * (1 - q)) + 4, RAINBOW[j % 6])
            R.rainbow_text(frame, W / 2, 330, FRUITS[cur][5], int(140 * R.ease_back(k)), start=s["cut_t"] + 0.35, t=t, maxw=980)
    else:
        for k in range(4):
            R.paste(frame, f"h{k}", 300 + (k % 2) * 480, 720 + (k // 2) * 420 - 12 * abs(math.sin(t * 3 + k)), 400)
        R.rainbow_text(frame, W / 2, 300, "YOUR FAVOURITE?", int(110 * R.ease_back((t - G["end_t"]) / 0.4)), maxw=980)
    kids(frame, t)
    return frame.convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(lo, hi):
        p.stdin.write(render_frame(f).tobytes())
    p.stdin.close()
    p.wait()
    return path


if __name__ == "__main__":
    if sys.argv[1] == "audio":
        build_audio()
        sys.exit()
    init()
    if sys.argv[1] == "frames":
        for f in [int(x) for x in sys.argv[2].split(",")]:
            render_frame(f).save(HERE / f"_f{f:04d}.png")
        sys.exit()
    from multiprocessing import Pool
    n = int(G["total"] * FPS)
    bnd = np.linspace(0, n, 5).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k}.mp4")) for k in range(4)]
    with Pool(4, initializer=worker_init) as pool:
        parts = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"What's Inside - Short {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
