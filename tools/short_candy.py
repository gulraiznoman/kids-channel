"""Short S19: TOO MUCH CANDY! Gul gobbles candy (hook at 0:00), gets a tummy ache (green face), Mishu explains and gives
fruit, crunch crunch, he feels strong. Ends "Candy is a little treat. Fruits make you strong!".
Reuses the character/face helpers from short_angry.py.   python tools/short_candy.py frames|video
"""
import math, os, subprocess, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
_argv = sys.argv[1:]
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(ROOT / "tools"))
import short_angry as SA

RS, RV, A, M, LS, R, SR = SA.RS, SA.RV, SA.A, SA.M, SA.LS, SA.R, SA.SR
W, H, FPS, INK = SA.W, SA.H, SA.FPS, SA.INK
TMP = ROOT / "tools" / "_candy"
TMP.mkdir(exist_ok=True)
FLOOR = SA.FLOOR
EAT = [0.15, 0.6, 1.05, 1.5, 1.95, 2.4]          # candy goes in
ACHE = (3.2, 6.4)
TALK = (6.4, 10.0)
FRUIT = (10.0, 15.0)
FRUIT_T = [10.3, 11.3, 12.3]
YAY = 15.0
END = 17.6
TOTAL = 22.0
LINES = [("gul", "Candy! Yummy, yummy!", 0.3, 1.6), ("gul", "Ouch! My tummy hurts!", 3.4, 1.8),
         ("mishu", "Too much candy is not good for your tummy!", 6.6, 2.6), ("mishu", "Try some yummy fruit!", 10.1, 1.6),
         ("gul", "Crunch, crunch! I feel strong!", 12.9, 1.9), ("both", "Yay! Healthy food!", YAY + 0.2, 1.7),
         ("mishu", "Candy is a little treat. Fruits make you strong!", END + 0.2, 3.0)]
SA.LINES = LINES
CANDY_COLS = [(255, 77, 109), (46, 168, 255), (255, 200, 40), (155, 93, 229), (59, 193, 74), (255, 159, 28)]
FRUITS = [("apple", ROOT / "ep01-fruits/art/fruit_apple.png"), ("banana", ROOT / "ep01-fruits/art/fruit_banana.png"),
          ("carrot", ROOT / "long03-fruits-veg/art/item_carrot.png")]


# ------------------------------------------------------------------ audio
rng = np.random.default_rng(19)


def munch():
    out = np.zeros(int(0.3 * SR))
    for k in range(3):
        n = int(0.05 * SR)
        x = np.convolve(rng.standard_normal(n), np.ones(4) / 4, mode="same") * np.exp(-np.arange(n) / SR / 0.015)
        out[int(k * 0.08 * SR):int(k * 0.08 * SR) + n] += x
    return out


def crunch():
    out = np.zeros(int(0.5 * SR))
    for k in range(5):
        n = int(0.04 * SR)
        x = np.diff(np.concatenate([[0], rng.standard_normal(n)])) * np.exp(-np.arange(n) / SR / 0.012)
        out[int(k * 0.07 * SR):int(k * 0.07 * SR) + n] += x * 1.4
    return out


def rumble():
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    f = 70 + 25 * np.sin(2 * np.pi * 3 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
    x += np.convolve(rng.standard_normal(n), np.ones(80) / 80, mode="same") * 6
    return x * np.minimum(1, t / 0.1) * np.minimum(1, (1.4 - t) / 0.3) * 0.8


def audio(path):
    n = int(TOTAL * SR)
    v = np.zeros((n, 2))
    for who, text, t, slot in LINES:
        for w, g, pan in ((("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)) if who == "both" else ((who, 1.0, -0.1 if who == "gul" else 0.1),)):
            A.add(v, RS.chant(w, text, slot), t, g, pan)
    RS.CHORD.setdefault("D", [62, 66, 69])
    RS.CHORD.setdefault("Em", [64, 67, 71])
    beat = 0.44
    song = {"chords": ["G", "Em", "C", "D"]}
    tune = [79, 81, 83, 86, 83, 81, 79, 0, 76, 79, 81, 83, 81, 79, 76, 0]
    toks = [dict(t=i * beat, dur=beat, notes=[tune[i % 16]]) for i in range(int(TOTAL / beat)) if tune[i % 16]]
    m = RV.exciting_music(song, toks, TOTAL, beat)
    g = np.ones(n)                                             # music dips during the tummy ache
    g[int(ACHE[0] * SR):int(TALK[1] * SR)] = 0.35
    g = np.convolve(g, np.ones(SR // 2) / (SR // 2), mode="same")
    m *= g[:, None]
    fx = np.zeros_like(m)
    for k, t in enumerate(EAT):
        A.add(fx, A.sfx_pop(), t, 0.45, -0.3 + 0.12 * k)
        A.add(fx, munch(), t + 0.15, 0.5)
    A.add(fx, rumble(), ACHE[0] + 0.1, 0.9)
    A.add(fx, M.boing(), ACHE[0], 0.3)
    for t in FRUIT_T:
        A.add(fx, A.sfx_whoosh(), t, 0.3)
        A.add(fx, crunch(), t + 0.5, 0.7)
    A.add(fx, A.sfx_sparkle(), YAY, 0.6)
    for k in range(4):
        A.add(fx, M.clap(), YAY + 0.2 + k * 0.25, 0.4)
    A.add(fx, A.sfx_ding(84), END + 0.2, 0.3)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    m = m / np.abs(m).max() * (1 - 0.35 * e)[:, None]
    LS.finish_audio(v + m * 0.5 + fx * 0.6, path)


# ------------------------------------------------------------------ pictures
def make_bg():
    y = np.linspace(0, 1, H)[:, None, None]
    wall = np.array([214, 240, 255], float) * (1 - 0.1 * y) + 255 * 0.1 * y
    img = Image.fromarray(np.repeat(np.clip(wall, 0, 255).astype(np.uint8), W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for yy in range(0, FLOOR - 120, 90):                       # kitchen tiles
        d.line((0, yy, W, yy), fill=(190, 225, 245), width=4)
    for xx in range(0, W, 90):
        d.line((xx, 0, xx, FLOOR - 120), fill=(190, 225, 245), width=4)
    d.rectangle((0, FLOOR - 120, W, H), fill=(230, 196, 150))
    d.rectangle((0, FLOOR - 130, W, FLOOR - 112), fill=(255, 255, 255), outline=INK, width=5)
    d.rounded_rectangle((680, 300, 1000, 600), radius=18, fill=(158, 216, 255), outline=INK, width=8)
    d.line((840, 300, 840, 600), fill=INK, width=8)
    d.line((680, 450, 1000, 450), fill=INK, width=8)
    d.rectangle((90, 520, 420, 545), fill=(192, 138, 85), outline=INK, width=5)
    for i, c in enumerate(((255, 120, 120), (255, 210, 90), (120, 200, 255))):
        d.rounded_rectangle((110 + i * 105, 420, 190 + i * 105, 518), radius=14, fill=c, outline=INK, width=5)
    return img


def table(fr):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((420, 1240, 1060, 1300), radius=16, fill=(200, 140, 90), outline=INK, width=7)
    for x in (470, 1010):
        d.rectangle((x - 18, 1300, x + 18, FLOOR + 60), fill=(170, 115, 70), outline=INK, width=6)


def candy_img(i, size=110):
    S = size * 2
    im = Image.new("RGBA", (S * 2, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = CANDY_COLS[i % 6]
    cx, cy, r = S, S / 2, S * 0.32
    for side in (-1, 1):
        d.polygon([(cx + side * r * 0.8, cy), (cx + side * r * 2.0, cy - r * 0.8), (cx + side * r * 2.0, cy + r * 0.8)], fill=c, outline=INK, width=8)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c, outline=INK, width=8)
    d.arc((cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6), 200, 300, fill=(255, 255, 255), width=10)
    return im.resize((size * 2, size), Image.LANCZOS)


def lollipop(size=260):
    im = Image.new("RGBA", (size, int(size * 1.7)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = size * 0.45
    cx, cy = size / 2, size / 2
    d.rectangle((cx - 9, cy, cx + 9, size * 1.65), fill=(255, 255, 255), outline=INK, width=4)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 120, 170), outline=INK, width=7)
    for k in range(4):
        rr = r * (0.85 - k * 0.2)
        d.arc((cx - rr, cy - rr, cx + rr, cy + rr), k * 60, k * 60 + 220, fill=(255, 255, 255), width=10)
    return im


def text(fr, s, t, t0, y=230, size=170, col=None):
    R.rainbow_text(fr, W / 2, y, s, int(size * R.ease_back((t - t0) / 0.25)), colour=col, maxw=1000)


def frame_at(t):
    fr = G["bg"].copy()
    if t < ACHE[0]:
        table(fr)
        eaten = sum(1 for e in EAT if t >= e + 0.35)
        for i, e0 in enumerate(EAT):
            if t >= e0 + 0.35:
                continue
            x, y = 560 + (i % 3) * 170, 1185 - (i // 3) * 70
            k = (t - e0) / 0.35 if t >= e0 else 0
            gx, gy = 330, 900
            fr.alpha_composite(G["candy"][i], (int(x + (gx - x) * k - 110), int(y + (gy - y) * k - 55 - 160 * math.sin(math.pi * k))))
        fr.alpha_composite(G["lolly"], (900, 960))
        SA.full(fr, "gul", "excited", 300, t, scale=0.46, hop=18 * abs(math.sin(t * 9)))
        R.rainbow_text(fr, W / 2, 230, "CANDY!", int(200 * (1 + 0.06 * math.sin(t * 14))), colour=(255, 77, 109), maxw=1000)
        if eaten:
            R.rainbow_text(fr, W / 2, 420, f"x{eaten}", int(120 * R.ease_back((t - EAT[eaten - 1] - 0.35) / 0.2)), colour=(255, 255, 255), maxw=500)
    elif t < ACHE[1]:
        q = t - ACHE[0]
        sh = 10 * math.sin(t * 40) * max(0.2, 1 - q / 2)
        SA.face_close(fr, "gul", "sad", t, shake=sh, red=0)
        im = fr.copy()
        g = Image.new("RGBA", fr.size, (120, 200, 90, int(70 * min(1, q / 0.6))))
        fr.alpha_composite(g)
        text(fr, "TUMMY ACHE!", t, ACHE[0], size=170, col=(90, 170, 60))
    elif t < TALK[1]:
        table(fr)
        fr.alpha_composite(G["lolly"], (410, 800))
        SA.full(fr, "gul", "sad", 250, t)
        SA.full(fr, "misheal", None, 830, t, wave=True)
        text(fr, "TOO MUCH CANDY!", t, TALK[0], size=150, col=(255, 77, 109))
        d = ImageDraw.Draw(fr)
        d.line((420, 800, 660, 1060), fill=(240, 60, 60), width=22)
        d.ellipse((400, 790, 680, 1070), outline=(240, 60, 60), width=22)
    elif t < YAY:
        table(fr)
        got = sum(1 for f in FRUIT_T if t >= f + 0.5)
        for i, (key, _) in enumerate(FRUITS):
            f0 = FRUIT_T[i]
            if t < f0:
                fr.alpha_composite(G["fruit"][key], (int(440 + i * 100 - 100), int(1150 - 100)))
            elif t < f0 + 0.5:
                k = (t - f0) / 0.5
                x = 440 + i * 100 + (330 - 440 - i * 100) * k
                y = 1150 + (900 - 1150) * k - 200 * math.sin(math.pi * k)
                fr.alpha_composite(G["fruit"][key], (int(x - 100), int(y - 100)))
        strong = t >= LINES[4][2]
        SA.full(fr, "gul", "excited" if strong else "happy", 250, t, hop=40 * abs(math.sin(t * 6)) if strong else 0, wave=strong)
        SA.full(fr, "misheal", "happy", 860, t, wave=True)
        if strong:
            text(fr, "STRONG!", t, LINES[4][2], size=200, col=(59, 193, 74))
            d = ImageDraw.Draw(fr)
            for j in range(8):
                a = j / 8 * 2 * math.pi + t
                R.star(d, 250 + 260 * math.cos(a), 1000 + 300 * math.sin(a), 22, R.RAINBOW[j % 6], rot=t * 2)
        else:
            text(fr, "YUMMY FRUIT!", t, FRUIT[0], size=160, col=(59, 193, 74))
        if got:
            R.rainbow_text(fr, W / 2, 420, ["APPLE!", "BANANA!", "CARROT!"][got - 1], int(110 * R.ease_back((t - FRUIT_T[got - 1] - 0.5) / 0.2)), maxw=700)
    else:
        hop = 50 * abs(math.sin((t - YAY) * 5))
        SA.full(fr, "gul", "excited", 250, t, hop=hop, wave=True)
        SA.full(fr, "misheal", "happy", 860, t, hop=hop * 0.8, wave=True)
        for i, (key, _) in enumerate(FRUITS):
            fr.alpha_composite(G["fruit"][key], (int(340 + i * 200 - 100), int(700 - 25 * abs(math.sin(t * 5 + i)))))
        if t >= END:
            d = ImageDraw.Draw(fr, "RGBA")
            d.rounded_rectangle((60, 130, 1020, 560), radius=50, fill=(255, 255, 255, 230), outline=INK, width=8)
            R.rainbow_text(fr, W / 2, 230, "CANDY = LITTLE TREAT", int(80 * R.ease_back((t - END) / 0.3)), colour=(255, 77, 109), maxw=900)
            R.rainbow_text(fr, W / 2, 430, "FRUIT = STRONG!", int(130 * R.ease_back((t - END - 1.3) / 0.3)), colour=(59, 193, 74), maxw=900)
        else:
            text(fr, "HEALTHY FOOD!", t, YAY, size=160)
            d = ImageDraw.Draw(fr)
            for x0, y0, sp, ph, col in G["confetti"]:
                y = y0 + (t - YAY) * sp
                if -30 < y < H:
                    x = x0 + 40 * math.sin(t * 2 + ph)
                    w = 22 * abs(math.cos(t * 5 + ph)) + 4
                    d.rectangle((x - w / 2, y - 12, x + w / 2, y + 12), fill=col)
    return fr.convert("RGB")


G = {}


def load():
    SA.load()
    SA.G["bg"] = make_bg()
    G.update(bg=SA.G["bg"], candy=[candy_img(i) for i in range(6)], lolly=lollipop(),
             fruit={k: LS.load(p, 200) for k, p in FRUITS}, confetti=SA.G["confetti"])
    fixed = {}
    for k, im in G["fruit"].items():
        sq = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        sq.alpha_composite(im, ((200 - im.width) // 2, (200 - im.height) // 2))
        fixed[k] = sq
    G["fruit"] = fixed


def main():
    load()
    if _argv and _argv[0] == "frames":
        ts = [float(x) for x in _argv[1].split(",")] if len(_argv) > 1 else [0.0, 0.5, 1.4, 2.9, 4.0, 7.5, 10.6, 13.5, 16.0, 20.5]
        sheet = Image.new("RGB", (270 * 5, 480 * ((len(ts) + 4) // 5)))
        for i, t in enumerate(ts):
            sheet.paste(frame_at(t).resize((270, 480)), ((i % 5) * 270, (i // 5) * 480))
        sheet.save(TMP / "_sheet.png")
        print("sheet", TMP / "_sheet.png")
        return
    audio(TMP / "a.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(TMP / "v.mp4")],
                         stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)):
        p.stdin.write(frame_at(f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    out = ROOT / "VIDEOS" / "S19 Too Much Candy" / f"Too Much Candy - Short {os.environ.get('VER', 'v1')}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "v.mp4"), "-i", str(TMP / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
