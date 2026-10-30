"""Animate "Getting Ready for Halloween" (1080x1920). The scene fills up step by step.

python render.py frames 30,200,...  -> preview PNGs
python render.py video              -> VIDEOS/H01 Getting Ready for Halloween/Getting Ready for Halloween - Short vN.mp4
"""
import json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
KIT = ROOT / "characters" / "layers"
OUT = ROOT / "VIDEOS" / "H01 Getting Ready for Halloween"
W, H, FPS = 1080, 1920, 30
S = 0.31
FONT = "C:/Windows/Fonts/seguibl.ttf"
INK = (58, 36, 32)
RAINBOW = [(255, 120, 30), (155, 93, 229), (59, 193, 74), (255, 77, 109), (46, 168, 255), (255, 200, 40)]
CHAR = {"gul": dict(outfit="bluetee", x=250, girl=False, voc="gul"),
        "misheal": dict(outfit="pink", x=830, girl=True, voc="mishu")}
CENTER = (540, 880, 520)
SPOT = {"jackolantern": (540, 1560, 300), "bat": (175, 560, 230), "ghost": (890, 800, 270),
        "blackcat": (170, 1090, 250), "candy": (540, 1150, 330)}
G = {}


# ------------------------------------------------------------------ setup
def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["S"] = {s["key"]: s for s in tl["steps"]}
    G["art"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in (HERE / "art").glob("item_*.png")}
    G["hat"] = {}
    for n in CHAR:
        h = Image.open(HERE / "art" / f"hat_{n}.png")
        G["hat"][n] = h.resize((int(h.width * S), int(h.height * S)), Image.LANCZOS)
    G["layers"] = {}
    for n in CHAR:
        G["layers"][n] = {p.stem: (lambda im: im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS))(Image.open(p))
                          for p in (KIT / n).glob("*.png")}
    G["env"] = {}
    for n, c in CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["fonts"], G["cache"] = {}, {}
    G["bg"] = background()


def font(size):
    if size not in G["fonts"]:
        G["fonts"][size] = ImageFont.truetype(FONT, size)
    return G["fonts"][size]


def ease_back(x):
    x = min(max(x, 0.0), 1.0)
    return 1 + 2.70158 * (x - 1) ** 3 + 1.70158 * (x - 1) ** 2


def ease_io(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def background():
    """Friendly lilac evening: soft sky, smiling moon, stars, white fence, grass. Nothing dark."""
    y = np.linspace(0, 1, H)[:, None, None]
    top, bot = np.array((176, 156, 240), float), np.array((255, 214, 186), float)
    img = (top * (1 - y) + bot * y).astype(np.uint8)
    im = Image.fromarray(np.repeat(img, W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(im)
    mx, my, r = 870, 470, 85                               # smiling moon
    d.ellipse((mx - r - 25, my - r - 25, mx + r + 25, my + r + 25), fill=(255, 245, 190, 255))
    d.ellipse((mx - r, my - r, mx + r, my + r), fill=(255, 226, 110), outline=INK, width=6)
    for ex in (mx - 30, mx + 30):
        d.arc((ex - 14, my - 22, ex + 14, my + 2), 200, 340, fill=INK, width=6)
    d.arc((mx - 30, my - 5, mx + 30, my + 40), 20, 160, fill=INK, width=6)
    d.ellipse((mx - 62, my + 8, mx - 38, my + 24), fill=(255, 160, 150))
    d.ellipse((mx + 38, my + 8, mx + 62, my + 24), fill=(255, 160, 150))
    d.polygon([(0, 1360), (300, 1300), (620, 1350), (900, 1290), (W, 1330), (W, H), (0, H)], fill=(150, 205, 120))
    for x in range(10, W, 105):                            # fence
        d.rounded_rectangle((x, 1180, x + 48, 1360), radius=12, fill=(255, 255, 255), outline=INK, width=5)
        d.polygon([(x, 1190), (x + 24, 1158), (x + 48, 1190)], fill=(255, 255, 255), outline=INK)
    d.rectangle((0, 1222, W, 1246), fill=(255, 255, 255), outline=INK, width=5)
    d.rectangle((0, 1300, W, 1324), fill=(255, 255, 255), outline=INK, width=5)
    d.rectangle((0, 1440, W, H), fill=(126, 196, 98))
    return im


# ------------------------------------------------------------------ drawing helpers
def rainbow_text(img, cx, cy, text, size, start=None, t=0.0):
    d = ImageDraw.Draw(img)
    f = font(size)
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + 6 * (len(text) - 1)
    if total > W - 70:
        size = int(size * (W - 70) / total)
        f = font(size)
        widths = [d.textlength(ch, font=f) for ch in text]
        total = sum(widths) + 6 * (len(text) - 1)
    x = cx - total / 2
    for i, ch in enumerate(text):
        dy = 0
        if start is not None:
            k = t - (start + i * 0.05)
            if 0 <= k < 0.3:
                dy = -math.sin(k / 0.3 * math.pi) * size * 0.3
        y = cy - size * 0.62 + dy
        d.text((x, y), ch, font=f, fill=INK, stroke_width=int(size * 0.13), stroke_fill=INK)
        d.text((x, y), ch, font=f, fill=RAINBOW[i % 6], stroke_width=int(size * 0.07), stroke_fill=(255, 255, 255))
        x += widths[i] + 6


def paste(frame, im, cx, cy, size, rot=0.0, sx=1.0, sy=1.0, alpha=1.0):
    w, h = max(1, int(size * sx)), max(1, int(size * sy))
    a = im.resize((w, h), Image.BICUBIC)
    if rot:
        a = a.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        arr = np.array(a)
        arr[:, :, 3] = (arr[:, :, 3] * alpha).astype(np.uint8)
        a = Image.fromarray(arr)
    frame.alpha_composite(a, (int(cx - a.width / 2), int(cy - a.height / 2)))


def spotlight(frame, cx, cy, r, k=1.0):
    if k <= 0:
        return
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for j, a in enumerate((50, 80, 120)):
        rr = r * (1.25 - 0.12 * j) * k
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 255, 255, a))
    frame.alpha_composite(layer)


def star_burst(frame, cx, cy, k, seed=0, n=10, reach=330):
    if not 0 <= k < 1:
        return
    d = ImageDraw.Draw(frame)
    for j in range(n):
        a = seed + j * 2 * math.pi / n
        r = 80 + reach * (1 - (1 - k) ** 2)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        sz = 30 * (1 - k) + 6
        pts = [(x + (sz if q % 2 == 0 else sz * 0.45) * math.cos(q * math.pi / 5 - math.pi / 2 + k * 3),
                y + (sz if q % 2 == 0 else sz * 0.45) * math.sin(q * math.pi / 5 - math.pi / 2 + k * 3)) for q in range(10)]
        d.polygon(pts, fill=RAINBOW[j % 6], outline=INK, width=3)


def twinkles(frame, t):
    d = ImageDraw.Draw(frame)
    for i, (x, y) in enumerate(((90, 180), (330, 120), (560, 210), (700, 90), (1000, 160), (420, 420), (120, 820), (1010, 1050))):
        s = 9 + 6 * (0.5 + 0.5 * math.sin(t * 3 + i * 1.7))
        d.polygon([(x, y - s), (x + s * 0.3, y - s * 0.3), (x + s, y), (x + s * 0.3, y + s * 0.3), (x, y + s),
                   (x - s * 0.3, y + s * 0.3), (x - s, y), (x - s * 0.3, y - s * 0.3)], fill=(255, 250, 210))


# ------------------------------------------------------------------ items
def place(key, t, s):
    """Centre while it's this item's step, then glide to its decoration spot."""
    nxt = s["t1"]
    if t < nxt:
        return CENTER, 1.0
    k = ease_io((t - nxt) / 0.7)
    (x0, y0, z0), (x1, y1, z1) = CENTER, SPOT[key]
    return (x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, z0 + (z1 - z0) * k), k


def draw_items(frame, t):
    S_ = G["S"]
    # pumpkin -> jack-o'-lantern (same object across two steps)
    p0, carve = S_["pumpkin"], S_["carve"]
    if t >= p0["t0"]:
        if t < carve["t1"]:
            pos, k = CENTER, 0
        else:
            pos, k = place("jackolantern", t, dict(t1=carve["t1"]))
        cx, cy, z = pos
        if t < p0["t0"] + 0.9:                             # rolls in from the left
            q = ease_io((t - p0["t0"]) / 0.9)
            cx = -300 + (cx + 300) * q
            rot = (1 - q) * -360
        else:
            rot = 0
        if t < carve["t1"]:
            spotlight(frame, cx, cy, z * 0.55)
        glow = carve["cues"]["glow"]
        bob = 8 * math.sin(t * 3)
        if t < glow:
            paste(frame, G["art"]["pumpkin"], cx, cy + bob, z, rot)
        else:
            m = min(1, (t - glow) / 0.35)
            if m < 1:
                paste(frame, G["art"]["pumpkin"], cx, cy + bob, z, 0, alpha=1 - m)
            pulse = 1 + 0.04 * math.sin(t * 6)
            paste(frame, G["art"]["jackolantern"], cx, cy + bob, z * pulse, 0, alpha=m)
            star_burst(frame, cx, cy, (t - glow) / 0.9, seed=0.3)
    for key, anim in (("bat", "flap"), ("ghost", "float"), ("blackcat", "walk"), ("candy", "pop")):
        s = S_[key]
        if t < s["t0"]:
            continue
        (cx, cy, z), k = place(key, t, s)
        rot, sx, sy = 0.0, 1.0, 1.0
        a = t - s["t0"]
        if anim == "flap":
            sx = 1 + 0.12 * math.sin(t * 16)
            cy += 15 * math.sin(t * 4)
            if a < 0.7:
                cy += (1 - ease_io(a / 0.7)) * 900
        elif anim == "float":
            cy += 22 * math.sin(t * 2.5)
            rot = 5 * math.sin(t * 2)
            alpha = min(1, a / 0.6)
        elif anim == "walk":
            if a < 1.0:
                cx = W + 250 - (W + 250 - cx) * ease_io(a / 1.0)
                cy -= 18 * abs(math.sin(a * 12))
            rot = 3 * math.sin(t * 2)
        elif anim == "pop":
            z *= ease_back(a / 0.5)
            cy += 6 * math.sin(t * 4)
        if t < s["t1"]:
            spotlight(frame, cx, cy, z * 0.55, min(1, a / 0.4))
        paste(frame, G["art"][key], cx, cy, z, rot, sx, sy, alpha=min(1, a / 0.6) if anim == "float" else 1.0)
        if anim == "pop" and "candy" in s["cues"]:            # candies jump out of the bucket
            c0 = s["cues"]["candy"]
            d = ImageDraw.Draw(frame)
            for j in range(8):
                q = (t - c0 - j * 0.08)
                if 0 <= q < 1.4:
                    ang = -math.pi / 2 + (j - 3.5) * 0.28
                    x = cx + math.cos(ang) * 420 * q
                    y = cy - z * 0.3 + math.sin(ang) * 420 * q + 520 * q * q
                    col = RAINBOW[j % 6]
                    d.ellipse((x - 22, y - 16, x + 22, y + 16), fill=col, outline=INK, width=3)
                    d.polygon([(x - 22, y), (x - 40, y - 12), (x - 40, y + 12)], fill=col, outline=INK)
                    d.polygon([(x + 22, y), (x + 40, y - 12), (x + 40, y + 12)], fill=col, outline=INK)


# ------------------------------------------------------------------ Gul & Mishu
def compose_char(name, t):
    c, L = CHAR[name], G["layers"][name]
    o = c["outfit"]
    env = G["env"][name]
    v = env[min(int(t * FPS), len(env) - 1)]
    talking = v > 0.12
    mouth = "smile" if not talking else ("o" if v < 0.5 else "open")
    eyes = "blink" if (t % 3.7) < 0.12 else "open"
    key = (name, eyes, mouth)
    if key not in G["cache"]:
        over = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for n in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if c["girl"] else []):
            over.alpha_composite(L[n])
        G["cache"][key] = over
    if (name, "under") not in G["cache"]:
        u = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for n in (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}"]:
            u.alpha_composite(L[n])
        G["cache"][(name, "under")] = u
    im = G["cache"][(name, "under")].copy()
    if talking:
        a = L[f"arm_r_wave_{o}"]
        im.alpha_composite(a.rotate(10 * math.sin(t * 7), center=(a.width * 0.66, a.height * 0.53), resample=Image.BICUBIC))
    else:
        im.alpha_composite(L[f"arm_r_down_{o}"])
    im.alpha_composite(G["cache"][key])
    return im, talking


def draw_kids(frame, t):
    hats = G["S"]["costume"]["cues"]
    party = G["S"]["end"]["cues"]["party"]
    for n, c in CHAR.items():
        im, talking = compose_char(n, t)
        hop = 10 * abs(math.sin(t * 5)) if talking else 3 * abs(math.sin(t * 1.6 + (1 if n == "gul" else 0)))
        if t >= party:
            hop = 45 * abs(math.sin((t - party) * 5 + (0.8 if n == "gul" else 0)))
        x, y = int(c["x"] - im.width / 2), int(1885 - im.height - hop)
        frame.alpha_composite(im, (x, y))
        ht = hats[f"hat_{n}"]
        if t >= ht:                                         # hat drops on with a poof
            k = (t - ht) / 0.5
            drop = (1 - min(1, k) ** 2) * 600 if k < 1 else 0
            frame.alpha_composite(G["hat"][n], (x, int(y - drop)))
            star_burst(frame, c["x"], y + 120, (t - ht - 0.45) / 0.7, seed=1.0, n=8, reach=160)


def render_frame(f):
    t = f / FPS
    frame = G["bg"].copy()
    twinkles(frame, t)
    draw_items(frame, t)
    # big word for the current step
    cur = next((s for s in G["steps"] if s["t0"] <= t < s["t1"]), G["steps"][-1])
    if cur["word"]:
        rainbow_text(frame, W / 2, 290, cur["word"], int(150 * ease_back((t - cur["t0"]) / 0.35)) or 1, start=cur["t0"], t=t)
    else:
        rainbow_text(frame, W / 2, 290, "HALLOWEEN", int(150 * ease_back(t / 0.5)) or 1, start=0.3, t=t)
        d = ImageDraw.Draw(frame)
        f2 = font(80)
        txt = "is coming!"
        w = d.textlength(txt, font=f2)
        if t > 0.6:
            d.text((W / 2 - w / 2, 380), txt, font=f2, fill=(255, 255, 255), stroke_width=9, stroke_fill=INK)
    if t >= G["S"]["end"]["cues"]["party"]:
        star_burst(frame, W / 2, 900, ((t - G["S"]["end"]["cues"]["party"]) % 1.2) / 1.2, seed=t, n=14, reach=500)
    draw_kids(frame, t)
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
    init()
    if sys.argv[1] == "frames":
        for f in [int(x) for x in sys.argv[2].split(",")]:
            render_frame(f).save(HERE / f"_f{f:04d}.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "4"))
    bnd = np.linspace(0, n, NW + 1).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k}.mp4")) for k in range(NW)]
    with Pool(NW, initializer=worker_init) as pool:
        parts = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Getting Ready for Halloween - Short {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
