"""Animate Long video 9 "Who's in the Egg?" (1920x1080) from timeline.json. Eggs are drawn here so they can wobble and crack.

python render.py frames 100,900,...  -> preview contact sheet _chk.png
python render.py video               -> VIDEOS/L09 Whos in the Egg/Whos in the Egg vN.mp4
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

W, H, FPS = 1920, 1080, 30
INK, RAINBOW = R.INK, R.RAINBOW
OUT = ROOT / "VIDEOS" / "L09 Whos in the Egg"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "tee", "misheal": "pink"}
VOC = {"gul": "gul", "misheal": "mishu"}
L1 = ROOT / "long01-animals-fun/art"
ART = {"chick": L1 / "fruit_chick.png", "duckling": L1 / "fruit_duckling.png", "puppy": L1 / "fruit_puppy.png", "kitten": L1 / "fruit_kitten.png",
       "calf": L1 / "fruit_calf.png", "elephant": L1 / "fruit_elephant.png", "fish": L1 / "fruit_fish.png", "dino": ROOT / "long06-dinosaurs/art/dino_trex.png",
       "frog": ROOT / "long08-colors-shapes/art/item_frog.png"}
EGG = {  # colour, w, h, spots colour (None = plain)
    "chick": ((255, 244, 225), 220, 290, None), "duckling": ((205, 235, 222), 230, 300, None), "turtle": ((250, 250, 244), 230, 240, None),
    "robin": ((130, 205, 240), 190, 250, None), "crocodile": ((246, 242, 232), 200, 300, None), "penguin": ((240, 240, 236), 250, 320, None),
    "snake": ((240, 230, 200), 200, 290, (215, 200, 160)), "ostrich": ((245, 232, 200), 340, 420, (225, 205, 165)), "owl": ((252, 252, 250), 210, 230, None),
    "dino": ((150, 205, 120), 320, 400, (80, 150, 70)), "golden": ((255, 205, 60), 420, 520, (255, 235, 140)), "plain": ((250, 248, 240), 260, 330, None),
    "hummingbird": ((252, 252, 248), 36, 50, None), "chicken": ((250, 236, 215), 120, 155, None), "egg": ((255, 244, 225), 170, 220, None)}
SPOT = {  # where each egg sits: x, ground y, base under it
    "chick": (960, 880, "hay"), "duckling": (960, 740, "nest"), "turtle": (960, 900, "sand"), "robin": (1250, 760, "bush"),
    "crocodile": (960, 960, None), "penguin": (960, 860, None), "snake": (960, 920, "leaves"), "ostrich": (960, 930, None),
    "owl": (460, 640, None), "dino": (960, 930, None)}
NAME = {"chick": "BABY CHICK!", "duckling": "DUCKLING!", "turtle": "SEA TURTLE!", "robin": "BABY ROBIN!", "crocodile": "BABY CROCODILE!",
        "penguin": "BABY PENGUIN!", "snake": "BABY SNAKE!", "ostrich": "BABY OSTRICH!", "owl": "BABY OWL!", "dino": "BABY DINO!"}
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


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
    G["bg"]["valley"] = Image.open(ROOT / "long06-dinosaurs/art/bg_valley.png").convert("RGBA")
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"], G["eggs"] = {}, {}, {}
    rng = np.random.default_rng(9)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]


def dur(t0):
    return G["dur"].get(round(t0, 3), 1.5)


def talking(n, t):
    env = G["env"][n]
    return env[min(int(t * FPS), len(env) - 1)]


# ------------------------------------------------------------------ characters
def compose(n, t, emo=None, wave=False):
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
    key = (n, eyes, brw, mouth_l, tuple(ovs), wave or v > 0.12)
    if key in G["cache"]:
        return G["cache"][key]
    girl = n == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    for p in (["hair_back"] if girl else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_{'wave' if (wave or v > 0.12) else 'down'}_{o}", "neck", "head", eyes]:
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


def body(frame, n, t, emo, cx, feet=1075, scale=0.5, hop=0.0, rot=0.0, wave=False, sy=1.0):
    im = compose(n, t, emo, wave=wave)
    sm = im.resize((int(1200 * scale), int(2000 * scale * sy)), Image.BICUBIC)
    if rot:
        sm = sm.rotate(rot, center=(sm.width / 2, sm.height), resample=Image.BICUBIC)
    frame.alpha_composite(sm, (int(cx - sm.width / 2), int(feet - sm.height * 0.93 - hop)))


def side_kids(frame, t, emo=None, xs=(190, 1730), scale=0.34, feet=1075):
    for n, x in zip(("gul", "misheal"), xs):
        body(frame, n, t, emo, x, feet=feet, scale=scale, hop=4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0))))


# ------------------------------------------------------------------ drawing helpers
def item(frame, key, cx, cy, size, rot=0.0, bottom=False, alpha=1.0, flip=False):
    if size < 3:
        return
    k = (key, int(size), flip)
    if k not in G["sized"]:
        if len(G["sized"]) > 250:
            G["sized"].clear()
        im = G["item"][key]
        im = im.crop(im.getbbox())
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        f = size / max(im.size)
        G["sized"][k] = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
    im = G["sized"][k]
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * max(0, alpha))))
    y = cy - im.height if bottom else cy - im.height / 2
    frame.alpha_composite(im, (int(cx - im.width / 2), int(y)))


def egg_pts(w, h, n=90):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        x = math.cos(a) * (1 + 0.08 * math.sin(a))
        y = math.sin(a)
        pts.append((w / 2 + x * w / 2 * 0.96, h * 0.53 + y * h * 0.47 * (1 if y > 0 else 1.1)))
    return pts


def crack_line(w, h, n=9):
    return [(w * i / (n - 1), h * 0.45 + (h * 0.05 if i % 2 else -h * 0.05)) for i in range(n)]


def egg_parts(kind, scale=1.0):
    """(whole, top, bottom) RGBA images for an egg kind; cached."""
    key = (kind, round(scale, 2))
    if key in G["eggs"]:
        return G["eggs"][key]
    col, w, h, spots = EGG[kind]
    w, h = max(8, int(w * scale)), max(10, int(h * scale))
    S = 2
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(x * S, y * S) for x, y in egg_pts(w, h)]
    d.polygon(pts, fill=col)
    if spots:
        rng = np.random.default_rng(len(kind))
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        for _ in range(26 if kind != "golden" else 12):
            x, y, r = rng.uniform(0.1, 0.9) * w * S, rng.uniform(0.1, 0.95) * h * S, rng.uniform(0.03, 0.08) * w * S
            dl.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=spots + (255,))
        lay.putalpha(Image.fromarray(np.minimum(np.array(lay.getchannel("A")), np.array(im.getchannel("A")))))
        im.alpha_composite(lay)
        d = ImageDraw.Draw(im)
    d.ellipse((w * S * 0.25, h * S * 0.2, w * S * 0.42, h * S * 0.42), fill=(255, 255, 255, 110))
    d.line(pts + [pts[0]], fill=INK, width=max(3, int(7 * S * min(1, scale + 0.3))))
    whole = im.resize((w, h), Image.LANCZOS)
    cl = [(x * S, y * S) for x, y in crack_line(w, h)]
    top_m = Image.new("L", im.size, 0)
    ImageDraw.Draw(top_m).polygon([(0, 0), (w * S, 0)] + cl[::-1], fill=255)
    bot_m = Image.new("L", im.size, 0)
    ImageDraw.Draw(bot_m).polygon(cl + [(w * S, h * S), (0, h * S)], fill=255)
    parts = []
    for m in (top_m, bot_m):
        p = im.copy()
        p.putalpha(Image.fromarray(np.minimum(np.array(p.getchannel("A")), np.array(m))))
        ImageDraw.Draw(p).line(cl, fill=INK, width=max(3, int(6 * S * min(1, scale + 0.3))))
        parts.append(p.resize((w, h), Image.LANCZOS))
    if len(G["eggs"]) > 120:
        G["eggs"].clear()
    G["eggs"][key] = (whole, parts[0], parts[1])
    return G["eggs"][key]


def paste_rot(frame, im, cx, by, rot=0.0, anchor_bottom=True):
    """paste with rotation around the bottom-centre (like an egg rocking)"""
    if rot:
        big = Image.new("RGBA", (im.width * 2, im.height * 2), (0, 0, 0, 0))
        big.alpha_composite(im, (im.width // 2, 0))
        big = big.rotate(rot, center=(im.width, im.height), resample=Image.BICUBIC)
        frame.alpha_composite(big, (int(cx - im.width), int(by - im.height)))
    else:
        frame.alpha_composite(im, (int(cx - im.width / 2), int(by - im.height if anchor_bottom else by - im.height / 2)))


def draw_egg(frame, kind, cx, by, t, knocks=(), crack_t=None, hatch_t=None, scale=1.0, idle=True):
    whole, top, bot = egg_parts(kind, scale)
    rot = 3 * math.sin(t * 2.2) if idle else 0
    for kt in knocks:
        q = t - kt
        if 0 <= q < 0.5:
            rot += 10 * math.sin(q * 30) * (1 - q / 0.5)
    if crack_t is not None and crack_t <= t < (hatch_t or 1e9):
        q = t - crack_t
        rot += 7 * math.sin(q * 45)
    if hatch_t is not None and t >= hatch_t:
        return False
    paste_rot(frame, whole, cx, by, rot)
    if crack_t is not None and t >= crack_t:
        q = min(1, (t - crack_t) / 0.7)
        cl = crack_line(whole.width, whole.height)
        k = max(2, int(len(cl) * q))
        a = math.radians(-rot)
        pts = []
        for x, y in cl[:k]:
            dx, dy = x - whole.width / 2, y - whole.height
            pts.append((cx + dx * math.cos(a) - dy * math.sin(a), by + dx * math.sin(a) + dy * math.cos(a)))
        ImageDraw.Draw(frame).line(pts, fill=INK, width=max(3, int(7 * scale)))
    return True


def hatch(frame, kind, baby, cx, by, t, hatch_t, size=None, name_t=None, hat=True):
    """after hatch_t: bottom shell stays, baby pops up out of it, top shell flies up and lands on its head"""
    whole, top, bot = egg_parts(kind)
    q = t - hatch_t
    size = size or whole.height * 1.25
    rise = ease_back(min(1, q / 0.45))
    bob = 8 * abs(math.sin(t * 4)) if q > 0.6 else 0
    bcy = by - whole.height * 0.35 - size * 0.42 * rise - bob
    item(frame, baby, cx, bcy, size * (0.6 + 0.4 * rise))
    paste_rot(frame, bot, cx, by)
    if hat:
        k = min(1, q / 0.7)
        hx = cx + 120 * math.sin(math.pi * k) * (1 if kind != "owl" else -1)
        head_y = bcy - size * 0.42
        hy = (by - whole.height) + (head_y - top.height * 0.25 - (by - whole.height)) * k - 260 * math.sin(math.pi * k)
        hat_im = top.rotate(-360 * k + (-12 if k >= 1 else 0), resample=Image.BICUBIC, expand=True)
        frame.alpha_composite(hat_im, (int(hx - hat_im.width / 2), int(hy)))
    if q < 0.5:
        d = ImageDraw.Draw(frame)
        for j in range(10):
            a = j / 10 * 2 * math.pi
            r = 60 + 380 * q / 0.5
            R.star(d, cx + r * math.cos(a), by - whole.height * 0.6 + r * 0.7 * math.sin(a), int(26 * (1 - q / 0.5)) + 2, RAINBOW[j % 6], rot=q * 6)


def base(frame, kind, cx, by, w):
    if kind == "hay":
        item(frame, "hay", cx, by + 10, w * 1.6)
    elif kind == "nest":
        item(frame, "nest", cx, by + 5, w * 1.5)
    elif kind == "sand":
        d = ImageDraw.Draw(frame)
        d.ellipse((cx - w * 0.9, by - 40, cx + w * 0.9, by + 60), fill=(240, 214, 150), outline=INK, width=6)
    elif kind == "bush":
        d = ImageDraw.Draw(frame)
        for dx, dy, r in ((-160, 40, 110), (160, 40, 110), (0, 70, 140), (-80, -10, 100), (80, -10, 100)):
            d.ellipse((cx + dx - r, by + dy - r * 0.8, cx + dx + r, by + dy + r * 0.8), fill=(76, 175, 80), outline=INK, width=6)
        item(frame, "nest", cx, by + 5, w * 1.6)
    elif kind == "leaves":
        d = ImageDraw.Draw(frame)
        for k in range(7):
            a = -math.pi + k * math.pi / 6
            x, y = cx + 230 * math.cos(a), by + 10 + 50 * math.sin(a) * 0.3
            d.ellipse((x - 90, y - 30, x + 90, y + 30), fill=(93, 187, 70) if k % 2 else (62, 155, 75), outline=INK, width=5)


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


def word(frame, text, t, t0, y=120, size=130, col=None, maxw=1500, x=960):
    rt(frame, x, y, text, int(size * ease_back((t - t0) / 0.3)), colour=col, maxw=maxw)


def knock_words(frame, cx, cy, t, knocks):
    for j, kt in enumerate(knocks):
        q = t - kt
        if 0 <= q < 0.7:
            rt(frame, cx + (170 if j % 2 else -170), cy - 40 * q, "KNOCK!", int(70 * ease_back(q / 0.2)), colour=(255, 255, 255), maxw=500)


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    cx, by = 960, 900
    item(frame, "hay", cx, by + 10, 760)
    if t < s["hatch_t"]:
        draw_egg(frame, "golden", cx, by, t, knocks=s["knock_t"], crack_t=s["crack_t"], hatch_t=s["hatch_t"])
        knock_words(frame, cx, 520, t, s["knock_t"])
        d = ImageDraw.Draw(frame)
        for j in range(8):
            a = j / 8 * 2 * math.pi + t * 1.5
            R.star(d, cx + 330 * math.cos(a), by - 280 + 300 * math.sin(a), 20, (255, 230, 80), rot=t * 3)
    else:
        q = t - s["hatch_t"]
        whole, top, bot = egg_parts("golden")
        paste_rot(frame, bot, cx, by)
        if q < 1.0:
            frame.alpha_composite(top.rotate(-400 * q, expand=True), (int(cx - 150 - 700 * q), int(by - whole.height - 600 * q + 500 * q * q)))
        for j, (b, tx, ty) in enumerate((("chick", 520, 560), ("duckling", 760, 380), ("penguin", 1160, 380), ("turtle", 1400, 560))):
            k = ease_back(min(1, (q - j * 0.12) / 0.5))
            if k > 0:
                x = cx + (tx - cx) * k
                y = by - 300 + (ty - by + 300) * k - 20 * abs(math.sin(t * 5 + j))
                item(frame, b, x, y, 230 * max(0.1, k))
        confetti(frame, t, s["hatch_t"])
        if t >= s["title_t"]:
            k2 = t - s["title_t"]
            rt(frame, 960, 150, "WHO'S IN THE EGG?", int(170 * ease_back(k2 / 0.35)), maxw=1700)
            if t >= s["kids_t"] - 1.2:
                side_kids(frame, t, "excited" if t < s["kids_t"] else None)
            if k2 < 0.3:
                frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k2 / 0.3)))))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    for j in range(5):
        ang = j / 5 * 2 * math.pi + t * 0.6
        kind = ("chick", "duckling", "robin", "dino", "penguin")[j]
        whole, _, _ = egg_parts(kind, 0.5)
        paste_rot(frame, whole, 960 + 560 * math.cos(ang), 500 + 200 * math.sin(ang) + whole.height / 2, 8 * math.sin(t * 3 + j))
    rt(frame, 960, 400, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy")


def scene_egg(frame, s, t):
    b = s["baby"]
    cx, by, bs = SPOT[b]
    whole, _, _ = egg_parts(b)
    base(frame, bs, cx, by, whole.width)
    kx = (190, 1730) if cx == 960 else ((1250, 1680) if cx < 900 else (190, 560))
    side_kids(frame, t, None, xs=kx)
    badge(frame, 160, 90, f"{s['num']}/10")
    q = t - s["t0"]
    if t < s["hatch_t"]:
        sc = ease_back(min(1, q / 0.4))
        if sc < 0.98:
            im = whole.resize((max(2, int(whole.width * sc)), max(2, int(whole.height * sc))))
            paste_rot(frame, im, cx, by)
        else:
            draw_egg(frame, b, cx, by, t, knocks=s["knock_t"], crack_t=s["crack_t"], hatch_t=s["hatch_t"])
        knock_words(frame, cx, by - whole.height - 40, t, s["knock_t"])
        if t >= s["hint_t"]:
            rt(frame, 1080 if cx == 960 else 960, 120, "WHO'S IN THE EGG?", int(100 * ease_back((t - s["hint_t"]) / 0.3)), maxw=1300)
            rt(frame, cx + whole.width * 0.6 + 60 if cx < 1500 else cx - 300, by - whole.height * 0.8, "?", int(150 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
    else:
        size = {"ostrich": 520, "dino": 520, "snake": 360, "crocodile": 420, "penguin": 420}.get(b, whole.height * 1.3)
        hatch(frame, b, "dino" if b == "dino" else b, cx, by, t, s["hatch_t"], size=size)
        if t >= s["name_t"]:
            rt(frame, 1080 if cx == 960 else 960, 120, NAME[b], int(120 * ease_back((t - s["name_t"]) / 0.3)), maxw=1300)


def scene_count(frame, s, t):
    item(frame, "hay", 960, 900, 1400)
    side_kids(frame, t, xs=(150, 1770), scale=0.32)
    xs = [560 + i * 200 for i in range(5)]
    sleep = t >= s["sleep_t"] - 3.0
    for i, (x, ht) in enumerate(zip(xs, s["hatches"])):
        if t < ht:
            draw_egg(frame, "egg", x, 860, t + i, crack_t=ht - 0.6, hatch_t=ht, scale=0.9)
        else:
            hatch(frame, "egg", "chick", x, 860, t, ht, size=200, hat=False)
            rt(frame, x, 520, str(i + 1), int(90 * ease_back((t - ht) / 0.3)), colour=RAINBOW[i % 6])
            if sleep and i >= 3:
                for j in range(3):
                    p = (t * 0.6 + j / 3) % 1
                    rt(frame, x + 40 + p * 60, 600 - p * 120, "Z", int(40 + 30 * p), colour=(150, 160, 255))
    if t >= s["sleep_t"]:
        word(frame, "5 - 2 = 3", t, s["sleep_t"], size=140)
    elif t >= s["hatches"][-1]:
        word(frame, "5 CHICKS!", t, s["hatches"][-1], size=140)
    else:
        word(frame, "COUNT THE CHICKS!", t, s["t0"], size=110)


def scene_sizes(frame, s, t):
    side_kids(frame, t, xs=(150, 1770), scale=0.32)
    spots = [("hummingbird", 520, "HUMMINGBIRD"), ("chicken", 860, "CHICKEN"), ("ostrich", 1300, "OSTRICH")]
    for i, (k, x, lab) in enumerate(spots):
        t0 = s["shown"][i]
        if t < t0:
            continue
        sc = ease_back(min(1, (t - t0) / 0.4))
        whole, _, _ = egg_parts(k)
        im = whole.resize((max(2, int(whole.width * sc)), max(2, int(whole.height * sc))))
        paste_rot(frame, im, x, 860, 3 * math.sin(t * 2 + i))
        rt(frame, x, 930, lab, 54, colour=(255, 255, 255), maxw=380)
    if t >= s["small_t"]:
        d = ImageDraw.Draw(frame)
        r = 70 + 6 * math.sin(t * 8)
        d.ellipse((520 - r, 835 - r, 520 + r, 835 + r), outline=(255, 77, 109), width=10)
        word(frame, "SMALLEST!", t, s["small_t"], size=130, col=(255, 77, 109))
    elif t >= s["big_t"]:
        stars_ring(frame, 1300, 650, 260, 260, t, n=10)
        word(frame, "BIGGEST!", t, s["big_t"], size=140)
    else:
        word(frame, "BIG AND SMALL!", t, s["t0"], size=120)


def scene_sort(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for x, lab, col in ((420, "EGG", (255, 200, 40)), (1500, "BABY", (255, 120, 170))):
        d.rounded_rectangle((x - 300, 230, x + 300, 760), radius=40, fill=(255, 255, 255, 170), outline=INK, width=6)
        rt(frame, x, 290, lab, 90, colour=col)
    whole, _, _ = egg_parts("egg", 0.5)
    paste_rot(frame, whole, 420 - 230, 360, 0)
    hx, hy = 1500 - 230, 300
    d.ellipse((hx - 34, hy - 20, hx, hy + 10), fill=(255, 77, 109))
    d.ellipse((hx, hy - 20, hx + 34, hy + 10), fill=(255, 77, 109))
    d.polygon([(hx - 34, hy - 2), (hx + 34, hy - 2), (hx, hy + 36)], fill=(255, 77, 109))
    cnt = {"egg": 0, "baby": 0}

    def slot(side, i):
        bx = 420 if side == "egg" else 1500
        return bx - 140 + (i % 2) * 280, 450 + (i // 2) * 200

    for a, sd in s["done"]:
        x, y = slot(sd, cnt[sd])
        cnt[sd] += 1
        item(frame, a, x, y, 170)
    q = t - s["t0"]
    if t < s["answer_t"]:
        item(frame, s["animal"], 960, 560 + 10 * math.sin(t * 3), 380 * ease_back(q / 0.4))
        word(frame, "EGG OR BABY?", t, s["t0"], size=110)
    else:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x, y = slot(s["side"], cnt[s["side"]])
        item(frame, s["animal"], 960 + (x - 960) * k, 560 + (y - 560) * k - 150 * math.sin(math.pi * k), 380 - 210 * k)
        word(frame, "EGGS!" if s["side"] == "egg" else "BABY!", t, s["answer_t"], size=130, col=(255, 200, 40) if s["side"] == "egg" else (255, 120, 170))
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def arrow(d, a, b, col=(255, 255, 255)):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    sx, sy = a[0] + 130 * math.cos(ang), a[1] + 130 * math.sin(ang)
    ex, ey = b[0] - 130 * math.cos(ang), b[1] - 130 * math.sin(ang)
    d.line((sx, sy, ex, ey), fill=INK, width=20)
    d.line((sx, sy, ex, ey), fill=col, width=12)
    for s2 in (-1, 1):
        d.line((ex, ey, ex - 40 * math.cos(ang + s2 * 0.5), ey - 40 * math.sin(ang + s2 * 0.5)), fill=INK, width=14)


def scene_life(frame, s, t):
    steps = s["steps"]
    n = len(steps)
    cx, cy, r = 960, 590, 290
    pos = [(cx + r * 1.25 * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + r * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    d = ImageDraw.Draw(frame, "RGBA")
    d.ellipse((cx - r * 1.5, cy - r * 1.25, cx + r * 1.5, cy + r * 1.25), fill=(255, 255, 255, 120))
    for i, (key, t0) in enumerate(zip(steps, s["step_t"])):
        if t < t0:
            continue
        k = ease_back(min(1, (t - t0) / 0.4))
        x, y = pos[i]
        if key == "egg":
            whole, _, _ = egg_parts("egg", max(0.05, k))
            paste_rot(frame, whole, x, y + whole.height / 2, 3 * math.sin(t * 2))
        else:
            item(frame, key, x, y + 6 * math.sin(t * 2 + i), 240 * k)
        if i > 0:
            arrow(d, pos[i - 1], pos[i])
    if t >= s["cycle_t"]:
        arrow(d, pos[-1], pos[0], (255, 200, 40))
        a = t * 2
        stars_ring(frame, cx, cy, r * 1.25, r, t, n=6)
        word(frame, "LIFE CYCLE!", t, s["cycle_t"], size=130)
    else:
        word(frame, f"{s['name'].upper()} LIFE CYCLE", t, s["t0"], size=100)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_dance(frame, s, t):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv = s["move"]
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, sy = 0, 0, 1.0
        if mv == "curl":
            sy = 0.78
        elif mv == "wiggle":
            rot = 9 * math.sin(q * 9 + i)
        elif mv == "knock":
            hop = 18 * abs(math.sin(q * 8))
        elif mv == "pop":
            hop = 110 * max(0, math.sin(min(math.pi, q * 3)))
        elif mv == "flap":
            hop = 25 * abs(math.sin(q * 7 + i))
            rot = 4 * math.sin(q * 14)
        elif mv == "jump":
            hop = 80 * abs(math.sin(q * 5 + i))
        body(frame, n, t, "excited" if mv in ("pop", "jump") else "happy", x, scale=0.55, hop=hop, rot=rot, wave=mv in ("flap", "jump", "pop", "knock"), sy=sy)
    if mv == "curl":
        whole, top, bot = egg_parts("plain", 2.6)
        im = whole.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * 0.35)))
        frame.alpha_composite(im, (int(960 - im.width / 2), int(1075 - im.height)))
    if mv == "pop":
        d = ImageDraw.Draw(frame)
        for j in range(12):
            a = j / 12 * 2 * math.pi
            r = 150 + 500 * min(1, q / 0.8)
            x, y = 960 + r * math.cos(a), 600 + r * 0.6 * math.sin(a)
            d.polygon([(x, y - 22), (x + 20, y + 10), (x - 18, y + 14)], fill=(250, 246, 235), outline=INK, width=3)
    word(frame, s["word"], t, s["t0"], size=120)


def scene_listen(frame, s, t):
    b = s["baby"]
    cx, by = 960, 880
    side_kids(frame, t, xs=(190, 1730))
    if t < s["hatch_t"]:
        draw_egg(frame, "plain", cx, by, t, knocks=s["sound_t"], crack_t=s["hatch_t"] - 0.5, hatch_t=s["hatch_t"])
        d = ImageDraw.Draw(frame, "RGBA")
        for st in s["sound_t"]:
            q = t - st
            if 0 <= q < 1.0:
                for j in range(3):
                    r = 200 + 140 * j + 160 * q
                    al = int(220 * (1 - q))
                    d.arc((cx - r, by - 180 - r, cx + r, by - 180 + r), -40, 40, fill=(255, 255, 255, al), width=12)
                    d.arc((cx - r, by - 180 - r, cx + r, by - 180 + r), 140, 220, fill=(255, 255, 255, al), width=12)
        word(frame, "LISTEN!", t, s["t0"], size=130)
        rt(frame, 1300, 520, "?", int(150 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
    else:
        hatch(frame, "plain", b, cx, by, t, s["hatch_t"], size=400)
        word(frame, NAME.get(b, b.upper() + "!"), t, s["hatch_t"], size=120)


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 120, s["q"], int(80 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        item(frame, s["vis"], 960, 580, 420 * ease_back((t - s["answer_t"]) / 0.4))
        stars_ring(frame, 960, 580, 360, 260, t, n=8, r=20)
        side_kids(frame, t, "happy")
    else:
        rt(frame, 960, 580, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t)


def scene_outro(frame, s, t):
    for j, b in enumerate(("chick", "duckling", "turtle", "penguin", "owl", "crocodile", "robin", "snake")):
        x = (j * 240 + t * 120) % 2200 - 140
        item(frame, b, x, 960 - 25 * abs(math.sin(t * 5 + j)), 190)
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, scale=0.5, feet=900, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 140, "SO MANY BABIES!", int(120 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


HIDE = [(160, 600, 0.45), (1780, 640, 0.42), (930, 300, 0.4), (720, 1050, 0.45), (1210, 1010, 0.42)]   # x, bottom y, scale


def scene_hidden(frame, s, t):
    for i, (x, y, sc) in enumerate(HIDE):
        whole, _, _ = egg_parts(("chick", "robin", "duckling", "snake", "owl")[i], sc)
        paste_rot(frame, whole, x, y, 6 * math.sin(t * 2 + i))
    item(frame, "hay", 230, 760, 340)
    item(frame, "hay", 1700, 790, 320)
    d = ImageDraw.Draw(frame)
    for i, ft in enumerate(s["found"]):
        if t >= ft:
            x, y, sc = HIDE[i]
            whole, _, _ = egg_parts("chick", sc)
            cy = y - whole.height / 2
            r = 95 + 8 * math.sin((t - ft) * 9)
            d.ellipse((x - r, cy - r, x + r, cy + r), outline=(255, 77, 109), width=12)
            rt(frame, x + 90, cy - 90, str(i + 1), int(90 * ease_back((t - ft) / 0.3)), colour=RAINBOW[i % 6])
    if t >= s["found"][-1] + 1.0:
        word(frame, "ALL 5 EGGS!", t, s["found"][-1] + 1.0, size=130)
    else:
        word(frame, "FIND 5 EGGS!", t, s["t0"], size=120)
    side_kids(frame, t, xs=(420, 1500), scale=0.28)


def scene_home(frame, s, t):
    q = t - s["t0"]
    item(frame, s["baby"], 960, 400 + 12 * math.sin(t * 3), 300 * ease_back(q / 0.4))
    d = ImageDraw.Draw(frame)
    for i, h in enumerate(s["opts"]):
        x = 480 + i * 480
        k = ease_back((q - 0.2 - i * 0.12) / 0.4)
        if k <= 0.02:
            continue
        w, hh = int(400 * k), int(225 * k)
        thumb = G["bg"][h].resize((w, hh), Image.BILINEAR)
        good = t >= s["answer_t"] and h == s["home"]
        dim = t >= s["answer_t"] and h != s["home"]
        if dim:
            thumb = Image.blend(thumb, Image.new("RGBA", thumb.size, (255, 255, 255, 255)), 0.6)
        frame.alpha_composite(thumb, (int(x - w / 2), int(800 - hh / 2)))
        d.rounded_rectangle((x - w / 2, 800 - hh / 2, x + w / 2, 800 + hh / 2), radius=16, outline=(59, 193, 74) if good else INK, width=16 if good else 6)
        if good:
            stars_ring(frame, x, 800, 260, 160, t, n=8, r=18)
    if t >= s["answer_t"]:
        word(frame, {"ice": "ICE!", "river": "RIVER!", "tree": "TREE!", "beach": "BEACH!", "pond": "POND!", "savanna": "SAVANNA!"}[s["home"]], t, s["answer_t"], size=130, col=(59, 193, 74))
    else:
        word(frame, "WHERE DO I LIVE?", t, s["t0"], size=110)


def scene_fact(frame, s, t):
    q = t - s["t0"]
    badge(frame, 160, 90, f"FACT {s['num']}", (46, 168, 255))
    if s["vis"] == "hen":
        item(frame, "hen", 860, 560 + 8 * math.sin(t * 2), 420 * ease_back(q / 0.4))
        whole, _, _ = egg_parts("chicken")
        paste_rot(frame, whole, 1180, 780, 4 * math.sin(t * 3))
    elif s["vis"] == "kiwi":
        item(frame, "kiwi", 820, 560, 380 * ease_back(q / 0.4))
        whole, _, _ = egg_parts("chicken", 1.9)
        paste_rot(frame, whole, 1200, 800, 3 * math.sin(t * 2))
    else:
        item(frame, s["vis"], 960, 560 + 8 * math.sin(t * 2), 420 * ease_back(q / 0.4))
    stars_ring(frame, 960, 560, 420, 260, t * 0.5, n=8, r=18)
    word(frame, "WOW!" if t >= s["say_t"] + dur(s["say_t"]) else "DID YOU KNOW?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_finale(frame, s, t):
    cx, by = 960, 900
    item(frame, "hay", cx, by + 10, 760)
    if t < s["hatch_t"]:
        knocks = [n for n in s["nums"]]
        draw_egg(frame, "golden", cx, by, t, knocks=knocks, crack_t=s["nums"][2], hatch_t=s["hatch_t"])
        cur = None
        for i, n in enumerate(s["nums"]):
            if t >= n:
                cur = (i, n)
        if cur:
            rt(frame, 960, 150, str(5 - cur[0]), int(220 * ease_back((t - cur[1]) / 0.25)), colour=RAINBOW[cur[0] % 6])
        else:
            word(frame, "GOLDEN EGG!", t, s["t0"], size=140, col=(255, 200, 40))
        side_kids(frame, t, "excited")
    else:
        q = t - s["hatch_t"]
        whole, top, bot = egg_parts("golden")
        paste_rot(frame, bot, cx, by)
        babies = ("chick", "duckling", "turtle", "robin", "crocodile", "penguin", "snake", "ostrich", "owl", "dino")
        for j, b in enumerate(babies):
            ang = math.pi + math.pi * j / (len(babies) - 1)
            tx, ty = cx + 720 * math.cos(ang), 640 + 380 * math.sin(ang)
            k = ease_back(min(1, max(0, (q - j * 0.06) / 0.5)))
            if k > 0:
                item(frame, b, cx + (tx - cx) * k, by - 250 + (ty - by + 250) * k - 18 * abs(math.sin(t * 5 + j)), 210 * max(0.1, k))
        confetti(frame, t, s["hatch_t"])
        rt(frame, 960, 140, "HATCH!", int(200 * ease_back(q / 0.3)))
        if q < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - q / 0.3)))))


SCENES = {"intro": scene_intro, "title": scene_title, "egg": scene_egg, "count": scene_count, "sizes": scene_sizes, "sort": scene_sort,
          "life": scene_life, "dance": scene_dance, "listen": scene_listen, "quiz": scene_quiz, "outro": scene_outro,
          "hidden": scene_hidden, "home": scene_home, "fact": scene_fact, "finale": scene_finale}


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
        fs = [int(x) for x in sys.argv[2].split(",")]
        cols = 4
        sheet = Image.new("RGB", (480 * cols, 270 * ((len(fs) + cols - 1) // cols)))
        for i, f in enumerate(fs):
            sheet.paste(render_frame(f).resize((480, 270)), ((i % cols) * 480, (i // cols) * 270))
        sheet.save(HERE / "_chk.png")
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
    dst = OUT / f"Whos in the Egg {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
