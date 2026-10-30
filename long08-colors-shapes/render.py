"""Animate Long video 8 "Colors & Shapes" (1920x1080) from timeline.json.

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L08 Colors and Shapes/Colors and Shapes for Kids vN.mp4
"""
import importlib.util, json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("l02render", ROOT / "long02-counting" / "render.py")
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
sys.path.insert(0, str(ROOT / "characters"))
from expressions import EMOTIONS
_aspec = importlib.util.spec_from_file_location("l08art", HERE / "art.py")
_art = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(_art)
HUNT = _art.HUNT

W, H, FPS = 1920, 1080, 30
INK, RAINBOW = R.INK, R.RAINBOW
OUT = ROOT / "VIDEOS" / "L08 Colors and Shapes"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "polo", "misheal": "yellow"}
VOC = {"gul": "gul", "misheal": "mishu"}
L1, L3, L4 = ROOT / "long01-animals-fun/art", ROOT / "long03-fruits-veg/art", ROOT / "long04-good-habits/art"
ART = {"firetruck": L1 / "fruit_firetruck.png", "duckling": L1 / "fruit_duckling.png", "whale": L1 / "fruit_whale.png",
       "piglet": L1 / "fruit_piglet.png", "starfish": L1 / "fruit_starfish.png", "train": L1 / "fruit_train.png",
       "pumpkinveg": L3 / "item_pumpkinveg.png", "eggplant": L3 / "item_eggplant.png", "tomato": L3 / "item_tomato.png",
       "corn": L3 / "item_corn.png", "broccoli": L3 / "item_broccoli.png", "blueberries": L3 / "item_blueberries.png",
       "clock": L4 / "item_clock.png", "book": L4 / "item_book.png", "moon": L4 / "item_moon.png", "ball": L4 / "item_ball.png",
       "egg": ROOT / "long06-dinosaurs/art/item_egg.png", "drum": ROOT / "long05-body-parts/art/item_drum.png",
       "strawberry": ROOT / "ep01-fruits/art/fruit_strawberry.png"}
COL = {"red": (232, 53, 46), "orange": (255, 140, 26), "yellow": (255, 210, 40), "green": (76, 195, 74), "blue": (46, 140, 255),
       "purple": (140, 75, 210), "pink": (255, 130, 180), "brown": (135, 82, 45), "black": (35, 35, 42), "white": (255, 255, 255),
       "grey": (150, 152, 165), "indigo": (85, 60, 200), "violet": (180, 100, 235), "teal": (40, 190, 200), "mint": (120, 225, 180),
       "tan": (225, 170, 100), "sky": (150, 215, 255), "dark": (60, 60, 70), "cream": (240, 242, 250)}
SHAPE_COL = {"circle": "red", "square": "blue", "triangle": "yellow", "rectangle": "green", "oval": "purple", "star": "orange",
             "heart": "pink", "diamond": "teal", "pentagon": (255, 107, 60), "hexagon": (255, 180, 0), "crescent": (255, 225, 90)}
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


def cv(c):
    return COL[c] if isinstance(c, str) else c


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["item"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in (HERE / "art").glob("item_*.png")}
    for k, p in ART.items():
        G["item"][k] = Image.open(p).convert("RGBA")
    G["bg"] = {p.stem[3:]: Image.open(p).convert("RGBA") for p in (HERE / "art").glob("bg_*.png")}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"], G["shp"] = {}, {}, {}
    rng = np.random.default_rng(8)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]
    G["rain"] = [(rng.uniform(0, W), rng.uniform(-300, 0), rng.uniform(500, 900), ["circle", "square", "triangle", "star", "heart", "diamond"][int(rng.integers(6))],
                  RAINBOW[int(rng.integers(6))], rng.uniform(60, 120), rng.uniform(-2, 2)) for _ in range(26)]
    G["blob"] = {}


def dur(t0):
    return G["dur"].get(round(t0, 3), 1.5)


def talking(n, t):
    env = G["env"][n]
    return env[min(int(t * FPS), len(env) - 1)]


# ------------------------------------------------------------------ characters
def compose(n, t, emo=None, arms=True, wave=False):
    L = G["full"][n]
    o = OUTFIT[n]
    v = talking(n, t)
    if emo:
        eyes, brw, mouth, ovs = EMOTIONS[emo]
        mouth_l = f"x_mouth_{mouth}"
    else:
        eyes, brw, ovs = ("blink" if (t + (1.3 if n == "gul" else 0)) % 4.1 < 0.12 else "open"), None, []
        eyes = f"eyes_{eyes}"
        mouth_l = "mouth_smile" if v < 0.12 else ("mouth_o" if v < 0.5 else "mouth_open")
    key = (n, eyes, brw, mouth_l, tuple(ovs), arms, wave or v > 0.12)
    if key in G["cache"]:
        return G["cache"][key]
    girl = n == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    base = (["hair_back"] if girl else []) + [f"body_{o}"]
    if arms:
        base += [f"arm_l_{o}", f"arm_r_{'wave' if (wave or v > 0.12) else 'down'}_{o}"]
    for p in base + ["neck", "head", eyes]:
        im.alpha_composite(L[p])
    if "lids" in ovs:
        im.alpha_composite(L["x_over_lids"])
    im.alpha_composite(L[f"x_brows_{brw}"] if brw else L["brows"])
    im.alpha_composite(L[mouth_l])
    im.alpha_composite(L["hair_front"])
    if girl:
        im.alpha_composite(L["earrings"])
    for ov in ovs:
        if ov != "lids":
            im.alpha_composite(L[f"x_over_{ov}"])
    if len(G["cache"]) > 80:
        G["cache"].clear()
    G["cache"][key] = im
    return im


def body(frame, n, t, emo, cx, feet=1075, scale=0.5, hop=0.0, rot=0.0, wave=False):
    im = compose(n, t, emo, wave=wave)
    sm = im.resize((int(1200 * scale), int(2000 * scale)), Image.BICUBIC)
    if rot:
        sm = sm.rotate(rot, center=(sm.width / 2, sm.height), resample=Image.BICUBIC)
    frame.alpha_composite(sm, (int(cx - sm.width / 2), int(feet - sm.height * 0.93 - hop)))


def side_kids(frame, t, emo=None, xs=(190, 1730), scale=0.34, feet=1075):
    for n, x in zip(("gul", "misheal"), xs):
        body(frame, n, t, emo, x, feet=feet, scale=scale, hop=4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0))))


# ------------------------------------------------------------------ drawing helpers
def item(frame, key, cx, cy, size, rot=0.0, alpha=1.0):
    if size < 3:
        return
    k = (key, int(size))
    if k not in G["sized"]:
        if len(G["sized"]) > 200:
            G["sized"].clear()
        im = G["item"][key]
        im = im.crop(im.getbbox())
        f = size / max(im.size)
        G["sized"][k] = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
    im = G["sized"][k]
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * max(0, alpha))))
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def unit_pts(shape):
    if shape == "square":
        return [(-.42, -.42), (.42, -.42), (.42, .42), (-.42, .42)]
    if shape == "rectangle":
        return [(-.48, -.3), (.48, -.3), (.48, .3), (-.48, .3)]
    if shape == "triangle":
        return [(0, -.44), (.48, .38), (-.48, .38)]
    if shape == "diamond":
        return [(0, -.47), (.34, 0), (0, .47), (-.34, 0)]
    if shape in ("pentagon", "hexagon"):
        n = 5 if shape == "pentagon" else 6
        return [(.47 * math.cos(-math.pi / 2 + 2 * math.pi * k / n), .47 * math.sin(-math.pi / 2 + 2 * math.pi * k / n)) for k in range(n)]
    if shape == "star":
        return [((.49 if k % 2 == 0 else .2) * math.cos(-math.pi / 2 + k * math.pi / 5), (.49 if k % 2 == 0 else .2) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    if shape == "heart":
        pts = []
        for k in range(72):
            a = k / 72 * 2 * math.pi
            pts.append((16 * math.sin(a) ** 3 / 34, -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) / 34 - 0.04))
        return pts
    return None


def draw_shape_on(d, shape, w, h, col, width=8):
    """draw a shape filling a w x h box (pixel units) on draw d"""
    if shape == "circle":
        d.ellipse((width, width, w - width, h - width), fill=col, outline=INK, width=width)
    elif shape == "oval":
        d.ellipse((width + (w * 0.18 if w <= h else 0), width + (h * 0.18 if h < w * 0.9 and w <= h else 0), w - width - (w * 0.18 if w <= h else 0), h - width), fill=col, outline=INK, width=width)
    elif shape == "crescent":
        d.ellipse((width, width, w - width, h - width), fill=col, outline=INK, width=width)
    elif shape in ("rect", "block"):
        d.rectangle((width / 2, width / 2, w - width / 2, h - width / 2), fill=col, outline=INK, width=width)
    elif shape == "tri":
        d.polygon([(w / 2, width), (w - width, h - width), (width, h - width)], fill=col, outline=INK, width=width)
    else:
        s = max(w, h)
        pts = [(w / 2 + x * s, h / 2 + y * s) for x, y in unit_pts(shape)]
        d.polygon(pts, fill=col, outline=INK, width=width)


def shape_img(shape, size, col, face=True):
    size = max(8, int(size) // 4 * 4)
    key = (shape, size, col, face)
    if key in G["shp"]:
        return G["shp"][key]
    S = size * 2
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = max(4, S // 45)
    if shape == "oval":
        d.ellipse((S * 0.2, S * 0.04, S * 0.8, S * 0.96), fill=col, outline=INK, width=lw)
    elif shape == "circle":
        d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), fill=col, outline=INK, width=lw)
    elif shape == "crescent":
        d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), fill=col, outline=INK, width=lw)
        m = Image.new("L", (S, S), 0)
        ImageDraw.Draw(m).ellipse((S * 0.28, S * -0.04, S * 1.12, S * 0.8), fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel("A")), 255 - np.array(m))))
        d = ImageDraw.Draw(im)
        d.arc((S * 0.28, S * -0.04, S * 1.12, S * 0.8), 90, 250, fill=INK, width=lw)
    else:
        draw_shape_on(d, shape, S, S, col, lw)
    if face and shape != "crescent":
        dy = {"triangle": 0.1, "heart": -0.02, "star": 0.02}.get(shape, 0)
        ex = 0.09 if shape in ("star", "diamond", "oval") else 0.11
        for sx in (-1, 1):
            x, y = S * (0.5 + sx * ex), S * (0.47 + dy)
            r = S * 0.035
            d.ellipse((x - r, y - r, x + r, y + r), fill=INK)
            d.ellipse((x - r * 0.3 + r * 0.3, y - r * 0.6, x + r * 0.3 + r * 0.3, y), fill=(255, 255, 255))
        cy = S * (0.56 + dy)
        d.arc((S * 0.43, cy - S * 0.05, S * 0.57, cy + S * 0.05), 15, 165, fill=INK, width=max(3, lw - 2))
        for sx in (-1, 1):
            x, y = S * (0.5 + sx * (ex + 0.06)), S * (0.56 + dy)
            d.ellipse((x - S * 0.03, y - S * 0.018, x + S * 0.03, y + S * 0.018), fill=(255, 140, 160))
    im = im.resize((size, size), Image.LANCZOS)
    if len(G["shp"]) > 300:
        G["shp"].clear()
    G["shp"][key] = im
    return im


def shape(frame, shp, cx, cy, size, col=None, face=True, rot=0.0):
    if size < 8:
        return
    im = shape_img(shp, size, cv(col or SHAPE_COL[shp]), face)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def piece(frame, shp, cx, cy, w, h, col, rot=0.0):
    """a stretched building block: rect / tri / circle / oval"""
    w, h = max(4, int(w)), max(4, int(h))
    key = ("pc", shp, w, h, col)
    if key not in G["shp"]:
        im = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if shp in ("circle", "oval"):
            d.ellipse((5, 5, w * 2 - 5, h * 2 - 5), fill=cv(col), outline=INK, width=10)
        else:
            draw_shape_on(d, shp, w * 2, h * 2, cv(col), 10)
        G["shp"][key] = im.resize((w, h), Image.LANCZOS)
    im = G["shp"][key]
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def blob(frame, cx, cy, r, col, seed=0, alpha=255):
    if r < 2:
        return
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(frame, "RGBA")
    c = cv(col) + (alpha,)
    oc = INK + (alpha,) if cv(col) in (COL["white"], COL["yellow"]) else None
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c, outline=oc, width=4 if oc else 0)
    for k in range(8):
        a = k / 8 * 2 * math.pi + rng.uniform(-0.3, 0.3)
        rr = r * rng.uniform(1.05, 1.35)
        s = r * rng.uniform(0.12, 0.28)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        d.ellipse((x - s, y - s, x + s, y + s), fill=c, outline=oc, width=3 if oc else 0)
    for k in range(5):
        a = k / 5 * 2 * math.pi + 0.4
        x, y = cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a)
        s = r * 0.35
        d.ellipse((x - s, y - s, x + s, y + s), fill=c)


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 20 * abs(math.cos(t * 5 + ph)) + 4
            d.rectangle((x - w / 2, y - 10, x + w / 2, y + 10), fill=col)


def stars_ring(frame, cx, cy, rx, ry, t, n=8, r=22):
    d = ImageDraw.Draw(frame)
    for j in range(n):
        a = j / n * 2 * math.pi + t
        R.star(d, cx + rx * math.cos(a), cy + ry * math.sin(a), r, RAINBOW[j % 6], rot=t * 2)


def badge(frame, x, y, text, col=(255, 107, 139)):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=col)


def word(frame, text, t, t0, y=120, size=130, col=None, maxw=1500):
    rt(frame, 960, y, text, int(size * ease_back((t - t0) / 0.3)), colour=col, maxw=maxw)


def bucket_img(col):
    key = ("bucket", col)
    if key not in G["shp"]:
        im = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.arc((60, 20, 240, 180), 180, 360, fill=INK, width=8)
        d.polygon([(40, 90), (260, 90), (232, 280), (68, 280)], fill=(205, 210, 222), outline=INK, width=7)
        d.ellipse((40, 70, 260, 112), fill=cv(col), outline=INK, width=7)
        d.rectangle((60, 150, 240, 200), fill=cv(col), outline=None)
        d.line((48, 150, 252, 150), fill=INK, width=5)
        d.line((52, 200, 248, 200), fill=INK, width=5)
        G["shp"][key] = im
    return G["shp"][key]


def bucket(frame, col, cx, cy, rot=0.0, scale=1.0):
    im = bucket_img(col)
    if scale != 1.0:
        im = im.resize((int(300 * scale), int(300 * scale)), Image.BICUBIC)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def rainbow_arcs(frame, cx, cy, r0, w, t=None, times=None, grow=0.45):
    d = ImageDraw.Draw(frame)
    cols = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    for i, c in enumerate(cols):
        k = 1.0 if times is None else (0 if t < times[i] else min(1, (t - times[i]) / grow))
        if k <= 0:
            continue
        r = r0 - i * w
        if r <= w:
            continue
        d.arc((cx - r, cy - r, cx + r, cy + r), 180, 180 + 180 * ease_io(k), fill=COL[c], width=w + 2)


def cloud(frame, cx, cy, s=1.0):
    d = ImageDraw.Draw(frame)
    for dx, dy, r in ((0, 0, 70), (-70, 15, 50), (70, 15, 55), (35, -35, 50), (-35, -30, 45)):
        d.ellipse((cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s), fill=(255, 255, 255))


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    for i, (t0, c) in enumerate(s["splats"]):
        if t >= t0:
            x, y = [(420, 330), (1500, 300), (900, 640), (300, 780), (1620, 760), (1180, 260)][i]
            blob(frame, x, y, 150 * ease_back((t - t0) / 0.25), c, seed=i)
    if t >= s["title_t"]:
        q = t - s["title_t"]
        for x0, y0, sp, shp, col, sz, spin in G["rain"]:
            y = y0 + q * sp
            if y > 980:
                y = 980 - abs(math.sin((y - 980) / 120)) * 80
            shape(frame, shp, x0, y, sz, col=col, face=False, rot=spin * q * 40)
        for n, x in (("gul", 640), ("misheal", 1280)):
            body(frame, n, t, "excited" if t < s["kids_t"] else None, x, scale=0.48, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
        rt(frame, 960, 190, "COLORS & SHAPES!", int(190 * ease_back(q / 0.35)), maxw=1700)
        if q < 0.35:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - q / 0.35)))))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    for j, shp in enumerate(("circle", "square", "triangle", "star", "heart", "diamond")):
        ang = j / 6 * 2 * math.pi + t * 0.6
        shape(frame, shp, 960 + 560 * math.cos(ang), 430 + 220 * math.sin(ang), 110 * ease_back((k - j * 0.06) / 0.4), face=False, rot=t * 30)
    rt(frame, 960, 400, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy")


def crayon(frame, col, x, y, ang=35, L=470, Wd=92):
    c = cv(col)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def P(u, v):   # u along the crayon (0 = tip), v across
        return (x + u * sa + v * ca, y - u * ca + v * sa)
    d = ImageDraw.Draw(frame)
    d.polygon([P(90, -Wd / 2), P(L, -Wd / 2), P(L, Wd / 2), P(90, Wd / 2)], fill=c, outline=INK, width=6)
    d.polygon([P(0, 0), P(90, -Wd / 2), P(90, Wd / 2)], fill=c, outline=INK, width=6)
    lab = (255, 255, 255) if col != "white" else (220, 222, 235)
    d.polygon([P(130, -Wd / 2), P(L - 50, -Wd / 2), P(L - 50, Wd / 2), P(130, Wd / 2)], fill=lab, outline=INK, width=4)
    for u in (150, L - 70):
        d.line([P(u, -Wd / 2), P(u, Wd / 2)], fill=c, width=10)


def scribble_path(p):
    pts = []
    for k in range(int(140 * p) + 1):
        u = k / 140
        pts.append((960 + 330 * math.sin(u * math.pi * 9) * (0.45 + 0.55 * math.sin(u * math.pi)), 330 + 440 * u))
    return pts


def scene_crayon(frame, s, t):
    side_kids(frame, t)
    badge(frame, 160, 90, f"{s['num']}/10")
    c = s["col"]
    pop = s["pop_t"]
    if t < pop:
        p = min(1, (t - s["t0"]) / 2.2)
        pts = scribble_path(p)
        d = ImageDraw.Draw(frame)
        if len(pts) > 1:
            if c in ("white", "yellow"):
                d.line(pts, fill=INK, width=78, joint="curve")
            d.line(pts, fill=COL[c], width=64, joint="curve")
        tip = pts[-1]
        crayon(frame, c, tip[0], tip[1])
        word(frame, f"{c.upper()} CRAYON!", t, s["t0"], size=110, col=COL[c] if c != "white" else None)
    else:
        q = t - pop
        if q < 0.4:
            d = ImageDraw.Draw(frame, "RGBA")
            r = 150 + 500 * q / 0.4
            d.ellipse((960 - r, 560 - r, 960 + r, 560 + r), outline=COL[c] + (int(255 * (1 - q / 0.4)),), width=30)
        if c == "white":
            d = ImageDraw.Draw(frame, "RGBA")
            d.ellipse((960 - 290, 560 - 290, 960 + 290, 560 + 290), fill=(120, 190, 240, 140))
        if c == "black":
            stars_ring(frame, 960, 560, 330, 270, t, n=8, r=18)
        item(frame, s["art"], 960, 560 + 10 * math.sin(t * 2.5), 440 * ease_back(q / 0.4))
        word(frame, f"{c.upper()}!", t, pop, size=160, col=COL[c])


def scene_primary(frame, s, t):
    q = t - s["show_t"]
    for i, c in enumerate(("red", "yellow", "blue")):
        k = ease_back((q - i * 0.35) / 0.4)
        if k > 0.02:
            bucket(frame, c, 560 + i * 400, 560, scale=1.1 * k)
            rt(frame, 560 + i * 400, 790, c.upper(), int(80 * k), colour=COL[c])
    word(frame, "PRIMARY COLORS", t, s["t0"], size=120)
    side_kids(frame, t)


def scene_mix(frame, s, t):
    c1, c2, res = s["c1"], s["c2"], s["res"]
    d = ImageDraw.Draw(frame)
    # bowl
    bx, by = 960, 760
    d.ellipse((bx - 300, by - 70, bx + 300, by + 70), fill=(255, 255, 255), outline=INK, width=8)
    lvl = 0
    if t >= s["pour1_t"] + 0.3:
        lvl = 1
    if t >= s["pour2_t"] + 0.3:
        lvl = 2
    if lvl:
        rx, ry = 265, 52
        if t >= s["reveal_t"]:
            d.ellipse((bx - rx, by - ry, bx + rx, by + ry), fill=COL[res], outline=INK if res == "white" else None)
        elif lvl == 1:
            d.ellipse((bx - rx, by - ry, bx + rx, by + ry), fill=COL[c1])
        else:
            d.ellipse((bx - rx, by - ry, bx + rx, by + ry), fill=COL[c1])
            spin = (t - s["swirl_t"]) * 5 if t >= s["swirl_t"] else 0
            for k in range(3):
                a0 = math.degrees(spin) + k * 120
                d.pieslice((bx - rx, by - ry, bx + rx, by + ry), a0, a0 + 60, fill=COL[c2])
            d.ellipse((bx - 90, by - 18, bx + 90, by + 18), fill=COL[c2] if int(spin * 2) % 2 else COL[c1])
    d.chord((bx - 300, by - 70, bx + 300, by + 230), 0, 180, fill=(255, 255, 255), outline=INK, width=8)
    d.rectangle((bx - 302, by - 2, bx + 302, by + 2), fill=INK)
    # buckets pour
    for c, x, side, tp in ((c1, 560, 1, s["pour1_t"]), (c2, 1360, -1, s["pour2_t"])):
        k = t - tp
        tilt = 0
        if 0 <= k < 1.5:
            tilt = 55 * (ease_io(k / 0.35) if k < 1.15 else 1 - ease_io((k - 1.15) / 0.35))
        bucket(frame, c, x, 420, rot=-side * tilt, scale=1.0)
        if 0.3 <= k < 1.25:
            lip = (x + side * 150, 360)
            pts = [lip, (bx - side * 120, by - 30)]
            if c in ("white", "yellow"):
                d.line(pts, fill=INK, width=40)
            d.line(pts, fill=COL[c], width=32)
    # equation
    rt(frame, 420, 120, c1.upper(), 100, colour=COL[c1], maxw=380)
    rt(frame, 680, 120, "+", 110, colour=(255, 255, 255))
    rt(frame, 950, 120, c2.upper(), 100, colour=COL[c2], maxw=380)
    rt(frame, 1215, 120, "=", 110, colour=(255, 255, 255))
    if t >= s["reveal_t"]:
        rt(frame, 1480, 120, res.upper() + "!", int(110 * ease_back((t - s["reveal_t"]) / 0.3)), colour=COL[res], maxw=440)
        stars_ring(frame, bx, by, 380, 120, t, n=8, r=20)
    else:
        rt(frame, 1480, 120, "?", int(120 + 10 * math.sin(t * 6)), colour=(255, 255, 255))
    side_kids(frame, t, xs=(150, 1770), scale=0.32)


def scene_rainbow(frame, s, t):
    rainbow_arcs(frame, 960, 960, 780, 70, t, s["arcs"])
    cloud(frame, 960 - 545, 950, 1.6)
    cloud(frame, 960 + 545, 950, 1.6)
    cols = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    cur = None
    for i, a in enumerate(s["arcs"]):
        if t >= a:
            cur = (i, a)
    if t >= s["fact_t"]:
        word(frame, "7 COLORS!", t, s["fact_t"], size=150)
        if t >= s["fact_t"] + dur(s["fact_t"]) + 0.3:
            d = ImageDraw.Draw(frame)
            for j in range(26):
                p = (t * 1.2 + j / 26) % 1
                x = 120 + (j * 47) % 560
                d.line((x, 240 + p * 500, x - 8, 270 + p * 500), fill=(90, 150, 255), width=5)
            d.ellipse((1580, 150, 1780, 350), fill=COL["yellow"], outline=INK, width=6)
    elif cur:
        i, a = cur
        word(frame, cols[i].upper() + "!", t, a, size=150, col=COL[cols[i]])
    else:
        word(frame, "RAINBOW!", t, s["t0"], size=150)
    side_kids(frame, t, "happy", xs=(180, 1740), scale=0.32)


def wagon(frame, x, col, t, moving):
    d = ImageDraw.Draw(frame)
    y0 = 760 + (3 * math.sin(t * 20 + x) if moving else 0)
    d.rounded_rectangle((x - 115, y0, x + 115, y0 + 130), radius=14, fill=COL[col], outline=INK, width=7)
    d.rectangle((x - 125, y0 - 10, x + 125, y0 + 10), fill=tuple(int(v * 0.8) for v in COL[col]), outline=INK, width=5)
    for wx in (x - 65, x + 65):
        a = t * 8 if moving else 0
        d.ellipse((wx - 34, 880, wx + 34, 948), fill=(70, 70, 80), outline=INK, width=6)
        d.line((wx + 22 * math.cos(a), 914 + 22 * math.sin(a), wx - 22 * math.cos(a), 914 - 22 * math.sin(a)), fill=(200, 200, 210), width=6)
    d.line((x - 115, 900, x - 145, 900), fill=INK, width=8)
    return y0


def scene_train(frame, s, t):
    side_kids(frame, t, xs=(1660, 1820), scale=0.28, feet=870)
    q = t - s["t0"]
    ph = s["phase"]
    off = 0
    if ph == "in":
        off = 1800 * (1 - ease_io(min(1, q / 2.6)))
    elif ph == "out":
        off = -2300 * min(1, max(0, q - 0.5) / 3.0) ** 2
    moving = (ph == "in" and q < 2.6) or (ph == "out" and q > 0.5)
    wx = {c: 640 + i * 260 + off for i, c in enumerate(("red", "yellow", "green", "blue"))}
    ys = {c: wagon(frame, wx[c], c, t, moving) for c in wx}
    # cargo already loaded
    count = {}
    for art, c in s.get("loaded", []):
        j = count.get(c, 0)
        count[c] = j + 1
        item(frame, art, wx[c] + (-50 if j == 0 else 50), ys[c] - 40, 120)
    ex = 330 + off
    item(frame, "train", ex, 925 - 165 + (3 * math.sin(t * 20) if moving else 0), 340)
    d = ImageDraw.Draw(frame, "RGBA")
    for j in range(4):
        p = (t * 0.8 + j / 4) % 1
        r = 25 + 40 * p
        d.ellipse((ex - 85 - r + 30 * p, 600 - 260 * p - r, ex - 85 + r + 30 * p, 600 - 260 * p + r), fill=(255, 255, 255, int(200 * (1 - p))))
    if ph == "load":
        c = s["col"]
        if t < s["answer_t"]:
            item(frame, s["art"], 960, 380 + 15 * math.sin(t * 3), 230 * ease_back(q / 0.4))
            word(frame, "WHICH WAGON?", t, s["t0"], size=110)
        else:
            k = min(1, (t - s["answer_t"]) / 0.6)
            j = count.get(c, 0)
            tx, ty = wx[c] + (-50 if j == 0 else 50), ys[c] - 40
            item(frame, s["art"], 960 + (tx - 960) * ease_io(k), 380 + (ty - 380) * ease_io(k) - 200 * math.sin(math.pi * k), 230 - 110 * k)
            word(frame, f"{c.upper()} WAGON!", t, s["answer_t"], size=120, col=COL[c])
            if k >= 1:
                stars_ring(frame, tx, ty, 120, 70, t, n=6, r=16)
    elif ph == "in":
        word(frame, "COLOR TRAIN!", t, s["t0"], size=140)
    else:
        word(frame, "CHOO CHOO!", t, s["t0"], size=150)


def perimeter_point(pts, u):
    segs = [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
    lens = [math.dist(a, b) for a, b in segs]
    L = sum(lens) * (u % 1)
    for (a, b), l in zip(segs, lens):
        if L <= l:
            k = L / max(l, 1e-6)
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        L -= l
    return pts[0]


def outline_pts(shp, cx, cy, size):
    u = unit_pts(shp)
    if u is None:
        if shp == "oval":
            return [(cx + 0.3 * size * math.cos(a / 60 * 2 * math.pi), cy + 0.46 * size * math.sin(a / 60 * 2 * math.pi)) for a in range(60)]
        return [(cx + 0.44 * size * math.cos(a / 60 * 2 * math.pi - math.pi / 2), cy + 0.44 * size * math.sin(a / 60 * 2 * math.pi - math.pi / 2)) for a in range(60)]
    return [(cx + x * size, cy + y * size) for x, y in u]


def scene_shape(frame, s, t):
    side_kids(frame, t, xs=(150, 1770), scale=0.32)
    badge(frame, 160, 90, f"{s['num']}/11", (46, 168, 255))
    shp, n = s["shape"], s["n"]
    cx, cy, size = 720, 450, 400
    q = t - s["t0"]
    shape(frame, shp, cx, cy + 6 * math.sin(t * 2), size * ease_back(q / 0.4))
    if t >= s["name_t"]:
        rt(frame, 960, 175, shp.upper() + "!", int(120 * ease_back((t - s["name_t"]) / 0.3)), colour=cv(SHAPE_COL[shp]), maxw=900)
    # count sides / points
    ct = s["count_t"]
    if n and t >= ct:
        dd = dur(ct)
        k = int(max(0, min(n, (t - ct - 0.12 * dd) / (0.8 * dd) * n + 1)))
        pts = outline_pts(shp, cx, cy, size)
        d = ImageDraw.Draw(frame)
        if shp == "star":
            for i in range(k):
                x, y = pts[2 * i]
                d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=(255, 255, 255), outline=INK, width=5)
                rt(frame, x, y, str(i + 1), 46, colour=RAINBOW[i % 6])
        else:
            for i in range(k):
                a, b = pts[i], pts[(i + 1) % len(pts)]
                d.line((a, b), fill=(255, 255, 255), width=20)
                d.line((a, b), fill=(255, 230, 60), width=12)
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                vx, vy = mx - cx, my - cy
                l = math.hypot(vx, vy) or 1
                x, y = mx + vx / l * 60, my + vy / l * 60
                d.ellipse((x - 32, y - 32, x + 32, y + 32), fill=(255, 255, 255), outline=INK, width=5)
                rt(frame, x, y, str(i + 1), 44, colour=RAINBOW[i % 6])
    if t >= s["ex_t"]:
        k = ease_back((t - s["ex_t"]) / 0.45)
        item(frame, s["ex"], 1250 + 300 * (1 - min(1, (t - s["ex_t"]) / 0.45)), 450 + 8 * math.sin(t * 2.4), 330 * max(0.05, k))
    if "air_t" in s and t >= s["air_t"]:
        pts = outline_pts(shp, cx, cy, size)
        d = ImageDraw.Draw(frame)
        u0 = (t - s["air_t"]) / 2.2
        for j in range(14):
            x, y = perimeter_point(pts, u0 - j * 0.012)
            r = 22 - j * 1.3
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255), outline=(255, 210, 40), width=4)


def scene_hunt(frame, s, t):
    side_kids(frame, t, xs=(470, 1810), scale=0.3)
    shp = s["shape"]
    kind, geo = HUNT[shp]
    found = t >= s["found_t"]
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((40, 40, 260, 260), radius=30, fill=(255, 255, 255, 230), outline=INK, width=6)
    shape(frame, shp, 150, 150, 170, face=False)
    if found:
        k = t - s["found_t"]
        pulse = 1 + 0.06 * math.sin(k * 10)
        for wdt, col in ((26, (255, 255, 255, 230)), (14, (255, 60, 120, 255))):
            if kind == "poly":
                cxp = sum(p[0] for p in geo) / len(geo)
                cyp = sum(p[1] for p in geo) / len(geo)
                pts = [(cxp + (x - cxp) * pulse * 1.08, cyp + (y - cyp) * pulse * 1.08) for x, y in geo]
                d.line(pts + [pts[0]], fill=col, width=wdt, joint="curve")
            elif kind == "rect":
                x0, y0, x1, y1 = geo
                e = 12 * pulse
                d.rectangle((x0 - e, y0 - e, x1 + e, y1 + e), outline=col, width=wdt)
            elif kind == "circle":
                x, y, r = geo
                r = (r + 14) * pulse
                d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wdt)
            else:
                x0, y0, x1, y1 = geo
                e = 14 * pulse
                d.ellipse((x0 - e, y0 - e, x1 + e, y1 + e), outline=col, width=wdt)
        word(frame, f"{shp.upper()}!", t, s["found_t"], y=340 if shp not in ("triangle", "circle", "diamond") else 620, size=120, col=cv(SHAPE_COL[shp]))
        if k < 1.0:
            cx, cy = {"poly": lambda: (sum(p[0] for p in geo) / len(geo), sum(p[1] for p in geo) / len(geo)),
                      "rect": lambda: ((geo[0] + geo[2]) / 2, (geo[1] + geo[3]) / 2), "circle": lambda: (geo[0], geo[1]),
                      "ellipse": lambda: ((geo[0] + geo[2]) / 2, (geo[1] + geo[3]) / 2)}[kind]()
            stars_ring(frame, cx, cy, 120 + 150 * k, 90 + 110 * k, t, n=8, r=20)
    else:
        rt(frame, 1100, 110, f"FIND A {shp.upper()}!", int(100 * ease_back((t - s["t0"]) / 0.35)), maxw=1300)


BUILD = {  # piece kind, dx, dy, w, h, colour, rotation
    "house": [("rect", 0, 110, 330, 300, "yellow", 0), ("tri", 0, -130, 460, 190, "red", 0), ("rect", 0, 190, 100, 140, "blue", 0),
              ("rect", -100, 60, 70, 70, "sky", 0), ("rect", 100, 60, 70, 70, "sky", 0)],
    "rocket": [("rect", 0, 40, 160, 340, "cream", 0), ("tri", 0, -200, 160, 160, "red", 0), ("tri", -115, 160, 80, 140, "red", 0),
               ("tri", 115, 160, 80, 140, "red", 0), ("circle", 0, 0, 90, 90, "blue", 0)],
    "car": [("rect", 0, 70, 560, 150, "red", 0), ("rect", -10, -50, 300, 110, "orange", 0), ("circle", -160, 160, 120, 120, "dark", 0),
            ("circle", 160, 160, 120, 120, "dark", 0)],
    "icecream": [("tri", 0, 170, 210, 300, "tan", 180), ("circle", -60, -20, 180, 180, "pink", 0), ("circle", 60, -20, 180, 180, "mint", 0),
                 ("circle", 0, -150, 64, 64, "red", 0)],
    "fish": [("oval", -40, 0, 400, 250, "orange", 0), ("tri", 220, 0, 180, 200, "orange", 90), ("circle", -140, -30, 54, 54, "dark", 0)],
}
BUILD_NAME = {"house": "HOUSE!", "rocket": "ROCKET!", "car": "CAR!", "icecream": "ICE CREAM!", "fish": "FISH!"}


def scene_build(frame, s, t):
    side_kids(frame, t, xs=(170, 1750), scale=0.32)
    cx, cy = 960, 570
    rev = t >= s["reveal_t"]
    bob = 12 * math.sin(t * 4) if rev else 0
    for i, (kind, dx, dy, w, h, col, rot) in enumerate(BUILD[s["thing"]]):
        t0 = s["build_t"] + 0.3 + i * 0.55
        if t < t0:
            continue
        k = min(1, (t - t0) / 0.45)
        sx = [-900, 900, 0, -900, 900][i % 5]
        sy = [0, 0, -800, -500, -500][i % 5]
        e = ease_back(k)
        piece(frame, kind, cx + dx + sx * (1 - e), cy + dy + sy * (1 - e) + bob, w, h, col, rot)
    if rev:
        word(frame, BUILD_NAME[s["thing"]], t, s["reveal_t"], size=140)
        stars_ring(frame, cx, cy, 420, 300, t, n=10, r=22)
    else:
        word(frame, "WHAT DID WE MAKE?", t, s["t0"], size=100)


SOLID_NAME = {"sphere": "SPHERE", "cube": "CUBE", "cone": "CONE", "cylinder": "CYLINDER", "pyramid3d": "PYRAMID"}


def scene_solid(frame, s, t):
    side_kids(frame, t, xs=(150, 1770), scale=0.32)
    cx, cy = 720, 450
    q = t - s["pop_t"]
    m = min(1, max(0, (q - 0.5) / 0.5))
    if m < 1:
        f = s["flat"]
        im = shape_img(f, 340 * ease_back(q / 0.35), cv(SHAPE_COL[f]), False).copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * (1 - m))))
        frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    if m > 0:
        item(frame, s["solid"], cx, cy + 6 * math.sin(t * 2), 380 * (0.8 + 0.2 * m), alpha=m, rot=(t * 20 % 360 if s["solid"] == "sphere" else 0) * 0)
    if q > 0.8:
        rt(frame, 960, 175, SOLID_NAME[s["solid"]] + "!", int(120 * ease_back((q - 0.8) / 0.3)), colour=(255, 255, 255), maxw=900)
    if t >= s["ex_t"]:
        k = min(1, (t - s["ex_t"]) / 0.45)
        item(frame, s["ex"], 1250 + 300 * (1 - k), 450 + 8 * math.sin(t * 2.4), 320 * max(0.05, ease_back(k)))


def scene_pattern(frame, s, t):
    side_kids(frame, t, xs=(150, 1770), scale=0.32)
    seq = s["seq"]
    n = len(seq) + 1
    gap = 190
    x0 = 960 - (n - 1) * gap / 2
    dd = dur(s["read_t"])
    for i, (shp, col) in enumerate(seq):
        ti = s["read_t"] + dd * i / len(seq)
        if t >= ti:
            shape(frame, shp, x0 + i * gap, 430 + 8 * math.sin(t * 3 + i), 160 * ease_back((t - ti) / 0.3), col=col)
    x = x0 + (n - 1) * gap
    if t >= s["answer_t"]:
        k = min(1, (t - s["answer_t"]) / 0.4)
        shp, col = s["ans"]
        shape(frame, shp, x, 430 - 300 * (1 - ease_back(k)), 170, col=col)
        stars_ring(frame, x, 430, 130, 110, t, n=6, r=16)
    else:
        d = ImageDraw.Draw(frame)
        pu = 1 + 0.05 * math.sin(t * 7)
        d.rounded_rectangle((x - 85 * pu, 430 - 85 * pu, x + 85 * pu, 430 + 85 * pu), radius=20, outline=(255, 255, 255), width=8)
        rt(frame, x, 430, "?", 130, colour=(255, 255, 255))
    rt(frame, 960, 175, "WHAT COMES NEXT?", int(90 * ease_back((t - s["t0"]) / 0.35)), colour=(255, 255, 255), maxw=1200)


DANCE_WORD = {"circle": "BIG CIRCLE!", "triangle": "TRIANGLE!", "star": "STAR JUMP!", "square": "SQUARE!", "rainbow": "RAINBOW WIGGLE!", "heart": "HEART HANDS!"}


def scene_dance(frame, s, t):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv, shp = s["move"], s["shape"]
    if shp == "rainbow":
        rainbow_arcs(frame, 960, 1000, 700, 60)
    else:
        size = 820 + 40 * math.sin(q * 4)
        pts = outline_pts(shp, 960, 560, size) if shp != "heart" else [(960 + x * size, 560 + y * size) for x, y in unit_pts("heart")]
        d = ImageDraw.Draw(frame, "RGBA")
        c = cv(SHAPE_COL[shp])
        d.polygon(pts, fill=c + (70,))
        d.line(pts + [pts[0]], fill=c + (255,), width=16, joint="curve")
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, dx = 0, 0, 0
        if mv == "jump":
            hop = 90 * abs(math.sin(q * 5 + i))
        elif mv == "sway":
            rot = 8 * math.sin(q * 2.5 + i)
        elif mv == "pop":
            hop = 50 * max(0, math.sin(q * 3))
        elif mv == "shake":
            dx = 14 * math.sin(q * 30)
            rot = 5 * math.sin(q * 6)
        elif mv == "slow":
            hop = 10 * math.sin(q * 1.5)
        body(frame, n, t, "excited" if mv == "jump" else "happy", x + dx, scale=0.55, hop=hop, rot=rot, wave=mv in ("jump", "pop", "slow"))
    word(frame, DANCE_WORD[shp], t, s["t0"], size=120, col=cv(SHAPE_COL.get(shp, "red")) if shp != "rainbow" else None)


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 120, s["q"], int(80 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        kind, v = s["vis"]
        if kind == "shape":
            shape(frame, v, 960, 580, 420 * k)
        elif kind == "item":
            item(frame, v, 960, 580, 400 * k)
        elif kind == "blob":
            blob(frame, 960, 580, 190 * k, v, seed=3)
        else:
            rainbow_arcs(frame, 960, 820, int(420 * max(0.2, k)), 46)
        stars_ring(frame, 960, 580, 360, 260, t, n=8, r=20)
        side_kids(frame, t, "happy")
    else:
        rt(frame, 960, 580, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t)


def scene_outro(frame, s, t):
    rainbow_arcs(frame, 960, 1000, 760, 60)
    for j, shp in enumerate(("circle", "square", "triangle", "star", "heart", "diamond", "hexagon", "oval")):
        ang = j / 8 * 2 * math.pi + t * 0.5
        shape(frame, shp, 960 + 760 * math.cos(ang), 480 + 300 * math.sin(ang), 120, rot=10 * math.sin(t * 2 + j))
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, scale=0.55, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 150, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 150, "FIND SHAPES AT HOME!", int(100 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


SCENES = {"intro": scene_intro, "title": scene_title, "crayon": scene_crayon, "primary": scene_primary, "mix": scene_mix,
          "rainbow": scene_rainbow, "train": scene_train, "shape": scene_shape, "hunt": scene_hunt, "build": scene_build,
          "solid": scene_solid, "pattern": scene_pattern, "dance": scene_dance, "quiz": scene_quiz, "outro": scene_outro}


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SCENES[sc["kind"]](frame, sc, t)
    for p0, p1 in G["prompts"]:
        if p0 <= t < p1:
            k = t - p0
            sc2 = ease_back(k / 0.3) * (1 + 0.04 * math.sin(k * 9))
            w, h = int(520 * sc2), int(110 * sc2)
            if w > 10:
                d = ImageDraw.Draw(frame)
                d.rounded_rectangle((960 - w // 2, 955, 960 + w // 2, 955 + h), radius=h // 2, fill=(255, 255, 255), outline=INK, width=6)
                f2 = R.font(max(8, int(62 * sc2)))
                tw = d.textlength("YOUR TURN!", font=f2)
                d.text((960 - tw / 2, 955 + h * 0.5 - 62 * sc2 * 0.62), "YOUR TURN!", font=f2, fill=(255, 77, 109), stroke_width=4, stroke_fill=(255, 255, 255))
    for st in G["stars"]:
        k = t - st
        if 0 <= k < 1.2:
            d = ImageDraw.Draw(frame)
            for j in range(10):
                a = j / 10 * 2 * math.pi + 0.3
                r = 160 + 380 * min(1, k / 0.6)
                R.star(d, 960 + r * math.cos(a), 600 + r * math.sin(a) * 0.7, int(36 * (1 - max(0, (k - 0.7) / 0.5))) + 1, RAINBOW[j % 6], rot=k * 3)
    return frame.convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    if os.path.exists(path):
        n = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                            "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
        if n.isdigit() and int(n) == hi - lo:
            return path
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
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
            render_frame(f).save(HERE / f"_f{f:05d}.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "4"))
    parts = 24
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Colors and Shapes for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
