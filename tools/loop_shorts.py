"""Looping music Shorts (1080x1920, no talking): one cute action, catchy original tune, end flows into the start.

python tools/loop_shorts.py share   -> VIDEOS/S12 Gul Shares Food/Gul Shares Food - Short v1.mp4   (16 s)
python tools/loop_shorts.py ducks   -> VIDEOS/S13 Mishu Dances with Ducklings/Duckling Dance - Short v1.mp4 (12 s)
"""
import math, os, subprocess, sys, pathlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ep02-colours"))
sys.path.insert(0, str(ROOT / "song01-animal-dance"))
import audio_mix as A
import music as M

W, H, FPS, SR = 1080, 1920, 30, 48000
KIT = ROOT / "characters" / "layers"
INK = (58, 36, 32)
BPM = 120
B = 60 / BPM
RAINBOW = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]


def load(p, size=None):
    im = Image.open(p).convert("RGBA")
    if size:
        bb = im.getbbox()
        im = im.crop(bb)
        k = size / max(im.size)
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return im


def paste(frame, im, cx, cy, scale=1.0, rot=0.0, sx=1.0, sy=1.0, bottom=False):
    w, h = max(1, int(im.width * scale * sx)), max(1, int(im.height * scale * sy))
    a = im.resize((w, h), Image.BICUBIC)
    if rot:
        a = a.rotate(rot, resample=Image.BICUBIC, expand=True)
    y = cy - a.height if bottom else cy - a.height / 2
    frame.alpha_composite(a, (int(cx - a.width / 2), int(y)))


def heart(d, x, y, r, col, a=255):
    d.ellipse((x - r, y - r * 0.8, x, y + r * 0.2), fill=col + (a,))
    d.ellipse((x, y - r * 0.8, x + r, y + r * 0.2), fill=col + (a,))
    d.polygon([(x - r * 0.98, y - 0.15 * r), (x + r * 0.98, y - 0.15 * r), (x, y + r * 1.05)], fill=col + (a,))


def note(d, x, y, s, col, a=255):
    d.ellipse((x - s, y - s * 0.75, x + s, y + s * 0.75), fill=col + (a,))
    d.line((x + s - 3, y, x + s - 3, y - 3.2 * s), fill=col + (a,), width=max(3, int(s / 3)))
    d.line((x + s - 3, y - 3.2 * s, x + s + 1.4 * s, y - 2.4 * s), fill=col + (a,), width=max(3, int(s / 3)))


def character(name, outfit, eyes="open", mouth="smile", wave=0.0, waving=True):
    L = KIT / name
    girl = name == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    for p in (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}", "neck", "head", f"eyes_{eyes}", "brows",
                                                 f"mouth_{mouth}", "hair_front"] + (["earrings"] if girl else []):
        im.alpha_composite(CACHE.setdefault((name, p), Image.open(L / f"{p}.png")))
    arm = CACHE.setdefault((name, f"arm_r_{'wave' if waving else 'down'}_{outfit}"),
                           Image.open(L / f"arm_r_{'wave' if waving else 'down'}_{outfit}.png"))
    if wave:
        arm = arm.rotate(wave, center=(790, 1050), resample=Image.BICUBIC)
    im.alpha_composite(arm)
    return im


CACHE = {}


# ================================================================== backgrounds
def bg_farm():
    bg = Image.open(ROOT / "long01-animals-fun" / "art" / "bg_farm.png").convert("RGBA")
    k = H / bg.height
    bg = bg.resize((int(bg.width * k), H), Image.LANCZOS)
    x0 = (bg.width - W) // 2
    return bg.crop((x0, 0, x0 + W, H))


def bg_pond():
    y = np.linspace(0, 1, H)[:, None, None]
    img = (np.array((120, 205, 255), float) * (1 - y) + np.array((220, 245, 255), float) * y).astype(np.uint8)
    im = Image.fromarray(np.repeat(img, W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.ellipse((760, 140, 960, 340), fill=(255, 224, 102))
    for cx, cy, s in ((200, 260, 1.0), (640, 420, 0.8), (900, 600, 0.7)):
        for dx, dy, r in ((0, 0, 70), (60, -30, 80), (130, 0, 70), (60, 20, 60)):
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255))
    d.polygon([(0, 1050), (300, 980), (700, 1030), (1080, 960), (1080, 1920), (0, 1920)], fill=(140, 214, 110))
    d.ellipse((-200, 1380, 1280, 1820), fill=(90, 180, 240), outline=INK, width=8)
    d.ellipse((-120, 1430, 1200, 1770), fill=(120, 200, 250))
    for x, yy in ((140, 1520), (420, 1640), (760, 1500), (930, 1680)):
        d.ellipse((x - 60, yy - 18, x + 60, yy + 18), outline=(200, 235, 255), width=5)
    rng = np.random.default_rng(3)
    for _ in range(30):
        x, yy = rng.uniform(0, W), rng.uniform(1080, 1370)
        c = RAINBOW[int(rng.integers(6))]
        d.ellipse((x - 12, yy - 12, x + 12, yy + 12), fill=c)
        d.ellipse((x - 5, yy - 5, x + 5, yy + 5), fill=(255, 240, 150))
    for x in (60, 1010):                                         # reeds
        for j in range(4):
            d.line((x + j * 14, 1420, x + j * 14 + 10, 1180), fill=(70, 150, 60), width=10)
            d.ellipse((x + j * 14, 1170, x + j * 14 + 22, 1240), fill=(140, 90, 50))
    return im


# ================================================================== music (loops seamlessly: whole bars, no fades)
rng = np.random.default_rng(9)


def kick():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(50 + 140 * np.exp(-t / 0.035)) / SR) * np.exp(-t / 0.14)


def hat():
    n = int(0.05 * SR)
    return np.diff(np.diff(np.concatenate([[0, 0], rng.standard_normal(n)]))) * A.env(n, 0.001, 0.012) * 0.3


def tune(total, prog, melody, root_shift=0, extra=None):
    n = int(total * SR)
    m = np.zeros((n, 2))
    bars = int(round(total / (4 * B)))
    for bar in range(bars):
        t0 = bar * 4 * B
        ch = [x + root_shift for x in prog[bar % len(prog)]]
        for q in range(4):
            tt = t0 + q * B
            A.add(m, kick(), tt, 0.5)
            if q in (1, 3):
                A.add(m, M.clap(), tt, 0.3, 0.05)
            A.add(m, hat(), tt + B / 2, 0.6, 0.3)
            A.add(m, M.tuba(ch[0] - 24 + (7 if q == 2 else 0), B * 0.7), tt, 0.3)
            A.add(m, M.uke_chord([x + 12 for x in ch], 0.22), tt + B / 2, 0.06, -0.3)
        for i, nt in enumerate(melody[(bar % 2) * 8:(bar % 2) * 8 + 8]):
            if nt:
                A.add(m, M.toy_piano(nt + root_shift + 12, 0.45), t0 + i * B / 2, 0.08, 0.2)
                A.add(m, M.xylo(nt + root_shift, 0.3), t0 + i * B / 2, 0.05, -0.2)
    if extra:
        extra(m)
    return m


def finish_audio(m, path):
    m = m / max(1e-9, np.abs(m).max()) * 0.9
    sf.write(path, m.astype(np.float32), SR, subtype="PCM_16")


# ================================================================== SHORT 1: Gul shares his food
SHARE = [("duckling", "item_corn", ROOT / "long03-fruits-veg/art/item_corn.png"),
         ("bunny", "item_carrot", ROOT / "long03-fruits-veg/art/item_carrot.png"),
         ("puppy", "item_bone", ROOT / "long05-body-parts/art/item_bone.png"),
         ("kitten", "item_milk", ROOT / "long04-good-habits/art/item_milk.png")]
SEG = 4.0          # seconds per animal; 4 animals = 16 s loop
OFFSET = 2.0       # the Short opens mid-dance (the hook), and the loop wraps cleanly


def share_assets():
    G = {"bg": bg_farm(), "animals": {}, "food": {}}
    for a, f, fp in SHARE:
        G["animals"][a] = load(ROOT / "long01-animals-fun" / "art" / f"fruit_{a}.png", 430)
        G["food"][a] = load(fp, 170)
    G["basket"] = load(ROOT / "long03-fruits-veg" / "art" / "item_basket.png", 300)
    return G


def share_frame(G, t_out):
    t = (t_out + OFFSET) % (SEG * len(SHARE))
    i = int(t // SEG)
    u = t - i * SEG                                              # 0..4 within this animal's turn
    a, _, _ = SHARE[i]
    fr = G["bg"].copy()
    d = ImageDraw.Draw(fr, "RGBA")
    beat = (t_out / B) % 1
    # Gul (left), with a basket of food at his feet
    eating = 2.0 <= u < 3.5
    giving = 1.0 <= u < 2.0
    g = character("gul", "tee", eyes="closed" if eating and (u % 0.5) < 0.35 else "open",
                  mouth="open" if eating else "smile", wave=(-25 * math.sin((u - 1.0) * math.pi) if giving else 10 * math.sin(t_out * 6)))
    hop = 14 * abs(math.sin(t_out * math.pi / B))
    paste(fr, g, 330, 1830 - hop, scale=0.55, bottom=True)
    paste(fr, G["basket"], 300, 1880, bottom=True)
    # the animal: hop in, receive food, happy dance, hop out
    ax, ay = 790, 1830
    if u < 1.0:                                                  # hop in from the right
        k = u / 1.0
        ax = 1300 - 510 * (1 - (1 - k) ** 2)
        ay -= 120 * abs(math.sin(k * 3 * math.pi))
        rot, sx, sy = 0, 1, 1
    elif u < 3.5:                                                # wait, eat, dance on the beat
        dance = u >= 2.0
        ay -= (60 if dance else 15) * abs(math.sin(t_out * math.pi / B))
        rot = (14 * math.sin(t_out * 2 * math.pi / B)) if dance else 0
        sq = 1 + (0.08 if dance and beat < 0.15 else 0)
        sx, sy = sq, 2 - sq
    else:                                                        # hop away to the right, happy
        k = (u - 3.5) / 0.5
        ax = 790 + 520 * k * k
        ay -= 140 * abs(math.sin(k * 2 * math.pi))
        rot, sx, sy = -10 * k, 1, 1
    paste(fr, G["animals"][a], ax, ay, rot=rot, sx=sx, sy=sy, bottom=True)
    # the food: flies from Gul's hand to the animal, then gets nibbled smaller
    if giving:
        k = u - 1.0
        fx = 560 + (ax - 120 - 560) * k
        fy = 1230 + (ay - 300 - 1230) * k - 260 * math.sin(k * math.pi)
        paste(fr, G["food"][a], fx, fy, rot=k * 360)
    elif 2.0 <= u < 2.9:
        k = (u - 2.0) / 0.9
        paste(fr, G["food"][a], ax - 120, ay - 300, scale=max(0.05, 1 - k), rot=8 * math.sin(u * 30))
    # hearts + music notes floating up while it dances
    if 2.0 <= u < 3.6:
        q = u - 2.0
        for j in range(5):
            p = (q * 0.8 + j / 5) % 1
            heart(d, ax - 160 + j * 80 + 20 * math.sin(q * 5 + j), ay - 450 - p * 380, 26 + 8 * (j % 2), RAINBOW[j % 6], int(255 * (1 - p)))
    for j in range(4):
        p = (t_out * 0.25 + j / 4) % 1
        note(d, 120 + j * 260, 900 - p * 600, 22, RAINBOW[(j + 2) % 6], int(200 * math.sin(p * math.pi)))
    return fr.convert("RGB")


def share_audio(path):
    total = SEG * len(SHARE)
    prog = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]
    mel = [72, 76, 79, 76, 77, 76, 74, 0, 74, 77, 81, 79, 76, 74, 72, 0]

    def sfx(m):
        for i in range(len(SHARE)):
            base = (i * SEG - OFFSET) % total
            A.add(m, M.boing(), (base + 0.05) % total, 0.25)               # hop in
            A.add(m, A.sfx_whoosh(), (base + 1.05) % total, 0.25)         # food flies
            A.add(m, A.sfx_pop(), (base + 1.95) % total, 0.4)
            for k in range(3):                                             # nom nom
                A.add(m, A.sfx_pop() * 0.6, (base + 2.1 + k * 0.25) % total, 0.25)
            A.add(m, A.sfx_sparkle(), (base + 2.9) % total, 0.3)
            if SHARE[i][0] == "duckling":
                A.add(m, M.quack(), (base + 3.0) % total, 0.4)
                A.add(m, M.quack(), (base + 3.25) % total, 0.4)
    m = tune(total, prog, mel, 0, sfx)
    finish_audio(m, path)


# ================================================================== SHORT 2: Mishu dances with five ducklings
DUCK_T = 12.0


def ducks_assets():
    G = {"bg": bg_pond(), "duck": load(ROOT / "long01-animals-fun" / "art" / "fruit_duckling.png", 230)}
    return G


def ducks_frame(G, t):
    fr = G["bg"].copy()
    d = ImageDraw.Draw(fr, "RGBA")
    lb = t / B
    beat = lb % 1
    # Mishu dancing in the middle
    m = character("misheal", "pink", eyes="closed" if int(lb) % 4 == 3 and beat < 0.5 else "open",
                  mouth="open" if beat < 0.5 else "smile", wave=18 * math.sin(lb * math.pi))
    hop = 30 * abs(math.sin(lb * math.pi))
    sway = 6 * math.sin(lb * math.pi / 2)
    m = m.rotate(sway, center=(600, 1900), resample=Image.BICUBIC)
    paste(fr, m, 540, 1500 - hop, scale=0.62, bottom=True)
    # five ducklings in a wave line on the water; every 2 beats one of them spins
    spinner = int(lb // 2) % 5
    for i in range(5):
        x = 120 + i * 210
        ph = lb - i * 0.25
        y = 1690 - 70 * max(0, math.sin(ph * math.pi))
        rot = 0
        if i == spinner:
            rot = 360 * min(1, (lb % 2) / 1.0)
        flip = (int(lb) % 2 == 0) == (i % 2 == 0)
        im = G["duck"].transpose(Image.FLIP_LEFT_RIGHT) if flip else G["duck"]
        sq = 1.08 if (ph % 1) < 0.12 else 1.0
        paste(fr, im, x, y, rot=rot, sx=sq, sy=2 - sq, bottom=True)
        if ph % 1 < 0.2:                                         # splash ripples on landing
            r = 40 + 200 * (ph % 1)
            d.ellipse((x - r, y - 16, x + r, y + 16), outline=(255, 255, 255, int(220 * (1 - (ph % 1) / 0.2))), width=6)
    for j in range(5):
        p = (t * 0.22 + j / 5) % 1
        note(d, 90 + j * 220, 1000 - p * 650, 24, RAINBOW[j % 6], int(220 * math.sin(p * math.pi)))
    for j in range(3):
        p = (t * 0.3 + j / 3) % 1
        heart(d, (200 if j % 2 else 880) + 60 * math.sin(t + j * 2), 700 - p * 400, 30, (255, 107, 139), int(230 * math.sin(p * math.pi)))
    return fr.convert("RGB")


def ducks_audio(path):
    prog = [[65, 69, 72], [70, 74, 77], [72, 76, 79], [65, 69, 72]]
    mel = [77, 77, 81, 77, 84, 81, 77, 0, 79, 79, 82, 79, 77, 76, 77, 0]

    def sfx(m):
        for b in range(int(DUCK_T / B)):
            if b % 2 == 1:
                A.add(m, M.quack(), b * B + B / 2, 0.35, -0.3 + 0.15 * (b % 5))
            if b % 2 == 0:
                A.add(m, A.sfx_sparkle() * 0.5, b * B + 0.05, 0.15)
    m = tune(DUCK_T, prog, mel, 0, sfx)
    finish_audio(m, path)


# ================================================================== build
def build(key):
    if key == "share":
        G, fn, total = share_assets(), share_frame, SEG * len(SHARE)
        out = ROOT / "VIDEOS" / "S12 Gul Shares Food" / f"Gul Shares Food - Short {os.environ.get('VER', 'v1')}.mp4"
        audio = share_audio
    else:
        G, fn, total = ducks_assets(), ducks_frame, DUCK_T
        out = ROOT / "VIDEOS" / "S13 Mishu Dances with Ducklings" / f"Duckling Dance - Short {os.environ.get('VER', 'v1')}.mp4"
        audio = ducks_audio
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "tools" / f"_loop_{key}"
    tmp.mkdir(exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "frames":
        for t in (0.0, total * 0.2, total * 0.45, total * 0.7, total - 1 / FPS):
            fn(G, t).save(tmp / f"f{t:05.2f}.png")
        print("frames in", tmp)
        return
    audio(tmp / "a.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp / "v.mp4")],
                         stdin=subprocess.PIPE)
    for f in range(int(total * FPS)):
        p.stdin.write(fn(G, f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "v.mp4"), "-i", str(tmp / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    build(sys.argv[1])
