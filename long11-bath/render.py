"""Animate Long video 11 "Bath Time & Sink or Float" (1920x1080) from timeline.json.
Gul & Mishu sit in a bubble bath (heads above the foam) or stand beside it.

python render.py frames 100,900,...  -> preview contact sheet _sheet.png
python render.py video               -> VIDEOS/L11 Bath Time/Bath Time for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L11 Bath Time"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "tee", "misheal": "yellow"}
VOC = {"gul": "gul", "misheal": "mishu"}
L1, L4, L5, L6, A11 = ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art", ROOT / "long05-body-parts/art", ROOT / "long06-dinosaurs/art", HERE / "art"
ART = {"towel": L4 / "item_towel.png", "soap": L4 / "item_soap.png", "pyjamas": A11 / "item_pyjamas.png", "ball": L4 / "item_ball.png",
       "apple": ROOT / "ep01-fruits/art/fruit_apple.png", "egg": L6 / "item_egg.png", "boat": L1 / "fruit_boat.png", "whale": L1 / "fruit_whale.png",
       "fish": L1 / "fruit_fish.png", "hand": L5 / "item_hand.png", "arm": L5 / "item_card_arm.png", "leg": L5 / "item_card_leg.png",
       "foot": L5 / "item_card_foot.png", "ear": L5 / "item_ear.png", "orange": ROOT / "ep01-fruits/art/fruit_orange.png",
       "grapes": ROOT / "ep01-fruits/art/fruit_grapes.png", "banana": ROOT / "ep01-fruits/art/fruit_banana.png",
       "carrot": ROOT / "long03-fruits-veg/art/item_carrot.png", "duckling": L1 / "fruit_duckling.png", "frog": ROOT / "long08-colors-shapes/art/item_frog.png",
       "turtle": ROOT / "long09-eggs/art/item_turtle.png", "penguin": ROOT / "long09-eggs/art/item_penguin.png"}
for k in ("duck", "sponge", "shampoo", "rock", "key", "coin", "spoon", "leaf", "toothbrush_cup"):
    ART[k] = A11 / f"item_{k}.png"
COLS = {"red": (232, 53, 46), "blue": (46, 140, 255), "yellow": (255, 200, 40), "green": (76, 195, 74), "purple": (150, 80, 220),
        "orange": (255, 140, 26), "pink": (255, 130, 180)}
TUB = (420, 740, 1500, 1010)          # tub box (x0, rim y, x1, bottom)
SURF, BOTTOM = 470, 880               # sink/float tank water surface and floor
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    ART.update({"sunny": L1 / "fruit_sunny.png", "snowy": L1 / "fruit_snowy.png", "dirt": ROOT / "long12-trucks/art/item_dirt.png",
                "dolphin": L1 / "fruit_dolphin.png", "octopus": L1 / "fruit_octopus.png", "crab": L1 / "fruit_crab.png", "starfish": L1 / "fruit_starfish.png"})
    G["item"] = {k: Image.open(p).convert("RGBA") for k, p in ART.items()}
    G["bg"] = {"bath": Image.open(A11 / "bg_bath.png").convert("RGBA")}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"] = {}, {}
    rng = np.random.default_rng(11)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]
    G["float"] = [(rng.uniform(0, W), rng.uniform(0, 1), rng.uniform(18, 55), rng.uniform(0.04, 0.12), rng.uniform(0, 6.28)) for _ in range(28)]
    G["foam"] = [(rng.uniform(TUB[0] + 20, TUB[2] - 20), rng.uniform(-30, 30), rng.uniform(40, 75)) for _ in range(46)]
    G["burst"] = [(rng.uniform(-1, 1), rng.uniform(0.6, 1.4), rng.uniform(25, 70)) for _ in range(40)]


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


def body(frame, n, t, emo, cx, feet=1075, scale=0.5, hop=0.0, rot=0.0, wave=False):
    im = compose(n, t, emo, wave=wave)
    sm = im.resize((int(1200 * scale), int(2000 * scale)), Image.BICUBIC)
    if rot:
        sm = sm.rotate(rot, center=(sm.width / 2, sm.height), resample=Image.BICUBIC)
    frame.alpha_composite(sm, (int(cx - sm.width / 2), int(feet - sm.height * 0.93 - hop)))


def head(frame, n, t, emo, cx, cy, scale=0.42, rot=0.0):
    im = compose(n, t, emo)
    crop = im.crop((150, 60, 1050, 1000)).resize((int(900 * scale), int(940 * scale)), Image.BICUBIC)
    if rot:
        crop = crop.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(crop, (int(cx - crop.width / 2), int(cy - crop.height / 2)))


def side_kids(frame, t, emo=None, xs=(170, 1750), scale=0.32):
    for n, x in zip(("gul", "misheal"), xs):
        body(frame, n, t, emo, x, scale=scale, hop=4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0))))


# ------------------------------------------------------------------ helpers
def item(frame, key, cx, cy, size, rot=0.0, alpha=1.0):
    if size < 3:
        return
    k = (key, int(size))
    if k not in G["sized"]:
        if len(G["sized"]) > 250:
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


def bubble(d, x, y, r, col=None, a=200):
    c = col or (225, 245, 255)
    d.ellipse((x - r, y - r, x + r, y + r), fill=c + (int(a * 0.45),), outline=(150, 200, 235, a), width=max(2, int(r / 9)))
    d.ellipse((x - r * 0.55, y - r * 0.6, x - r * 0.15, y - r * 0.25), fill=(255, 255, 255, a))


def floaters(frame, t, n=28):
    d = ImageDraw.Draw(frame, "RGBA")
    for x0, ph, r, sp, w in G["float"][:n]:
        y = H - ((t * sp + ph) % 1) * (H + 120)
        bubble(d, x0 + 30 * math.sin(t + w), y, r)


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


def badge(frame, x, y, text, col=(46, 168, 255)):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=col)


def word(frame, text, t, t0, y=120, size=130, col=None, maxw=1500, x=960):
    rt(frame, x, y, text, int(size * ease_back((t - t0) / 0.3)), colour=col, maxw=maxw)


# ------------------------------------------------------------------ the bathtub
def tub_back(frame, water=1.0):
    d = ImageDraw.Draw(frame, "RGBA")
    x0, ry, x1, by = TUB
    d.rounded_rectangle((x0, ry - 40, x1, ry + 40), radius=40, fill=(245, 248, 252), outline=INK, width=8)
    if water > 0:
        wy = ry - 20 + (1 - water) * 50
        d.rounded_rectangle((x0 + 30, wy, x1 - 30, ry + 36), radius=20, fill=(130, 205, 245, 255))
    d.rectangle((x1 - 70, ry - 210, x1 - 40, ry - 30), fill=(200, 205, 215), outline=INK, width=6)       # tap
    d.rounded_rectangle((x1 - 160, ry - 225, x1 - 40, ry - 190), radius=14, fill=(200, 205, 215), outline=INK, width=6)


def tub_front(frame, t, foam=1.0, water=1.0):
    d = ImageDraw.Draw(frame, "RGBA")
    x0, ry, x1, by = TUB
    if foam > 0:
        for fx, fy, r in G["foam"]:
            rr = r * foam
            y = ry + fy * 0.5 - 6 * math.sin(t * 2 + fx * 0.01)
            d.ellipse((fx - rr, y - rr * 0.75, fx + rr, y + rr * 0.75), fill=(255, 255, 255, 255), outline=(200, 225, 240, 255), width=3)
    d.rounded_rectangle((x0, ry + 10, x1, by), radius=60, fill=(255, 255, 255), outline=INK, width=8)
    d.rounded_rectangle((x0 + 30, ry + 40, x1 - 30, ry + 70), radius=14, fill=(232, 240, 248))
    for fx in (x0 + 90, x1 - 90):
        d.ellipse((fx - 40, by - 20, fx + 40, by + 50), fill=(255, 200, 40), outline=INK, width=6)


def bath_kids(frame, t, emo=None, foam=1.0, water=1.0, hop=0.0, emo2=None, bob=True):
    tub_back(frame, water)
    for n, x, e in (("gul", 760, emo), ("misheal", 1160, emo2 if emo2 is not None else emo)):
        b = 8 * math.sin(t * 2 + (0 if n == "gul" else 1.4)) if bob else 0
        head(frame, n, t, e, x, 515 + b - hop, scale=0.46)
    tub_front(frame, t, foam, water)


def tap_stream(frame, t, a=1.0):
    d = ImageDraw.Draw(frame, "RGBA")
    x = TUB[2] - 140
    for j in range(5):
        xx = x + (j - 2) * 6
        d.line((xx, TUB[1] - 200, xx + 4 * math.sin(t * 20 + j), TUB[1] + 20), fill=(120, 200, 245, int(220 * a)), width=8)


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    floaters(frame, t, 12)
    q = t - s["burst_t"]
    kids_in = t >= s["title_t"]
    if kids_in:
        k = t - s["title_t"]
        bath_kids(frame, t, "excited" if t < s["kids_t"] else None, hop=-80 * (1 - ease_back(min(1, k / 0.5))))
        rt(frame, 960, 200, "BATH TIME!", int(220 * ease_back(k / 0.35)), maxw=1500)
        if k < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k / 0.3)))))
    else:
        tub_back(frame)
        tub_front(frame, t, foam=1.0 + 0.4 * max(0, math.sin(min(1, q / 0.5) * math.pi)))
    d = ImageDraw.Draw(frame, "RGBA")
    if 0 <= q < 2.4:
        for dx, sp, r in G["burst"]:
            x = 960 + dx * 700 * min(1, q / 1.2)
            y = TUB[1] - sp * 900 * q + 260 * q * q
            if y < H:
                bubble(d, x, y, r)
    if t >= s["duck_t"]:
        k = t - s["duck_t"]
        y = TUB[1] - 40 - 380 * math.sin(min(1, k / 0.6) * math.pi * 0.5) if k < 0.6 else TUB[1] - 420 + 20 * math.sin(t * 4)
        item(frame, "duck", 1180 if kids_in else 960, y if not kids_in else TUB[1] - 20 + 6 * math.sin(t * 3), 200 if kids_in else 260)


def scene_title(frame, s, t):
    floaters(frame, t)
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rt(frame, 960, 400, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.34)
    item(frame, "duck", 960, 650 + 15 * math.sin(t * 3), 180)


def scene_need(frame, s, t):
    q = t - s["t0"]
    badge(frame, 160, 90, f"{s['num']}/6")
    for i, k in enumerate(s["done"]):
        item(frame, k, 520 + i * 180, 220, 140)
    item(frame, s["key"], 960, 560 + 10 * math.sin(t * 2.5), 380 * ease_back(q / 0.4))
    word(frame, s["key"].upper() + "!", t, s["say_t"], y=850, size=110)
    side_kids(frame, t, xs=(170, 1750))


def scene_fill(frame, s, t):
    q = t - s["tap_t"]
    water = min(1, max(0, q / 4.0))
    in_tub = t >= s["jump_t"]
    if in_tub:
        k = t - s["jump_t"]
        bath_kids(frame, t, "excited", foam=min(1, k / 0.8), hop=-60 * (1 - ease_back(min(1, k / 0.5))))
        d = ImageDraw.Draw(frame, "RGBA")
        if k < 1.0:
            for j in range(16):
                a = j / 16 * math.pi
                r = 120 + 500 * k
                bubble(d, 960 - math.cos(a) * r, TUB[1] - math.sin(a) * r * 0.6 + 300 * k * k, 18)
        word(frame, "SPLASH!", t, s["jump_t"], size=160, col=(46, 140, 255))
    else:
        tub_back(frame, water)
        tub_front(frame, t, foam=0, water=water)
        if water < 1:
            tap_stream(frame, t)
        side_kids(frame, t, xs=(200, 1720))
        if t >= s["rule_t"]:
            word(frame, "ALWAYS WITH A GROWN-UP!", t, s["rule_t"], size=100, col=(255, 77, 109), maxw=1700)
        elif t >= s["check_t"]:
            word(frame, "WARM, NOT HOT!", t, s["check_t"], size=120, col=(255, 140, 26))
            item(frame, "hand", 960, 520, 220, rot=200)
        else:
            word(frame, "FILL THE BATH!", t, s["t0"], size=120)


def scene_wash(frame, s, t):
    q = t - s["t0"]
    part = s["part"]
    hair = part == "hair"
    bath_kids(frame, t, "calm" if hair else "happy")
    d = ImageDraw.Draw(frame, "RGBA")
    if hair:
        for x in (760, 1160):
            for j in range(9):
                a = j / 9 * math.pi + t
                bubble(d, x + 150 * math.cos(a), 380 - 50 * abs(math.sin(a)) - 10 * math.sin(t * 4 + j), 30)
        item(frame, "shampoo", 960, 250 + 10 * math.sin(t * 3), 210 * ease_back(q / 0.4))
    elif part == "face":
        sx, sy = 760 + 70 * math.cos(t * 6), 520 + 50 * math.sin(t * 6)
        item(frame, "sponge", sx, sy, 160, rot=20 * math.sin(t * 6))
    else:
        cx, cy = 960, 175
        d.rounded_rectangle((cx - 130, cy - 130, cx + 130, cy + 130), radius=40, fill=(255, 255, 255, 230), outline=INK, width=6)
        item(frame, s["key"], cx, cy, 220 * ease_back(q / 0.4))
        item(frame, "sponge", cx + 90 * math.cos(t * 6), cy + 60 * math.sin(t * 6), 130, rot=20 * math.sin(t * 6))
        for j in range(int(min(8, q * 4))):
            bubble(d, cx - 140 + (j * 47) % 280, cy - 120 + (j * 83) % 240, 18 + (j % 3) * 6)
    word(frame, f"WASH YOUR {part.upper()}!", t, s["t0"], y=110, size=110, col=(46, 140, 255))


def scene_rinse(frame, s, t):
    q = t - s["pour_t"]
    bath_kids(frame, t, "happy", foam=max(0.25, 1 - q / 2.5))
    d = ImageDraw.Draw(frame, "RGBA")
    if q < 2.5:
        for x in (760, 1160):
            for j in range(7):
                xx = x - 120 + j * 40
                d.line((xx, 0, xx + 6 * math.sin(t * 15 + j), 380), fill=(120, 200, 245, 200), width=10)
    else:
        stars_ring(frame, 960, 560, 520, 220, t, n=10)
    word(frame, "SQUEAKY CLEAN!" if q > 2.0 else "RINSE!", t, s["pour_t"] + (2.0 if q > 2.0 else 0), size=140, col=(46, 140, 255))


BUB_POS = [(420 + i * 120, 250 + 70 * math.sin(i * 0.9)) for i in range(10)]


def scene_bubbles(frame, s, t):
    bath_kids(frame, t, "excited")
    d = ImageDraw.Draw(frame, "RGBA")
    popped = [p for p in s["pops"] if t >= p + 0.1]
    for i, (x, y) in enumerate(BUB_POS):
        if i < len(popped):
            k = t - s["pops"][i] - 0.1
            if k < 0.35:
                r = 55 + 60 * k / 0.35
                d.ellipse((x - r, y - r, x + r, y + r), outline=(150, 210, 250, int(255 * (1 - k / 0.35))), width=6)
            rt(frame, x, y, str(i + 1), int(70 * ease_back(k / 0.25)), colour=RAINBOW[i % 6])
        else:
            bubble(d, x, y + 8 * math.sin(t * 2 + i), 55)
    n = len(popped)
    word(frame, f"{n} BUBBLES!" if n else "POP AND COUNT!", t, s["pops"][n - 1] if n else s["t0"], size=120)


def scene_popcol(frame, s, t):
    bath_kids(frame, t, "happy")
    d = ImageDraw.Draw(frame, "RGBA")
    for i, (c, rgb) in enumerate(COLS.items()):
        x, y = 360 + i * 200, 230 + 30 * math.sin(t * 2 + i)
        if c == s["col"] and t >= s["pop_t"] + 0.1:
            k = t - s["pop_t"] - 0.1
            if k < 0.4:
                r = 70 + 80 * k / 0.4
                d.ellipse((x - r, y - r, x + r, y + r), outline=rgb + (int(255 * (1 - k / 0.4)),), width=10)
            continue
        bubble(d, x, y, 70, col=rgb, a=230)
    word(frame, f"POP THE {s['col'].upper()}!", t, s["t0"], y=110, size=110, col=COLS[s["col"]])


def tank(frame, t, done=(), splash_t=None):
    d = ImageDraw.Draw(frame, "RGBA")
    x0, x1 = 600, 1320
    d.rounded_rectangle((x0, 300, x1, 940), radius=24, fill=(240, 250, 255, 120), outline=INK, width=8)
    wave = [(x, SURF + 8 * math.sin(t * 2.5 + x * 0.02)) for x in range(x0 + 8, x1 - 7, 12)]
    d.polygon(wave + [(x1 - 8, 932), (x0 + 8, 932)], fill=(110, 195, 245, 170))
    d.line(wave, fill=(70, 160, 230, 255), width=6)
    nf = ns = 0
    for key, res in done:
        if res == "float":
            x = x0 + 70 + nf * 96
            nf += 1
            item(frame, key, x, SURF - 25 + 8 * math.sin(t * 2.5 + x * 0.02), 100, rot=6 * math.sin(t * 2 + x))
        else:
            x = x0 + 70 + ns * 96
            ns += 1
            item(frame, key, x, BOTTOM, 95)
    return nf, ns


def scene_sinkintro(frame, s, t):
    tank(frame, t)
    rt(frame, 1520, SURF - 10, "FLOAT", 80, colour=(46, 140, 255))
    rt(frame, 1520, BOTTOM - 20, "SINK", 80, colour=(120, 120, 140))
    d = ImageDraw.Draw(frame)
    d.line((1520, SURF + 60, 1520, BOTTOM - 80), fill=INK, width=12)
    d.polygon([(1490, BOTTOM - 100), (1550, BOTTOM - 100), (1520, BOTTOM - 60)], fill=INK)
    word(frame, "SINK OR FLOAT?", t, s["t0"], size=120)
    side_kids(frame, t, xs=(200, 1780), scale=0.3)


def scene_sink(frame, s, t):
    nf, ns = tank(frame, t, s["done"])
    key, res = s["key"], s["res"]
    q = t - s["t0"]
    x0 = 600
    tx = x0 + 70 + (nf if res == "float" else ns) * 96
    if t < s["drop_t"]:
        item(frame, key, 960, 200 + 12 * math.sin(t * 3), 200 * ease_back(q / 0.4))
        rt(frame, 1450, 250, "?", int(150 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
    else:
        k = min(1, (t - s["drop_t"]) / (0.5 if res == "float" else 1.0))
        x = 960 + (tx - 960) * k
        if res == "float":
            y = 200 + (SURF - 25 - 200) * ease_back(k)
        else:
            y = 200 + (BOTTOM - 200) * (k ** 1.6)
        item(frame, key, x, y, 200 - 80 * k)
        kk = t - s["drop_t"] - 0.25
        if 0 <= kk < 0.6:
            d = ImageDraw.Draw(frame, "RGBA")
            for j in range(10):
                a = math.pi + j / 9 * math.pi
                r = 40 + 200 * kk
                d.ellipse((960 + math.cos(a) * r - 10, SURF + math.sin(a) * r * 0.8 - 10 + 200 * kk * kk,
                           960 + math.cos(a) * r + 10, SURF + math.sin(a) * r * 0.8 + 10 + 200 * kk * kk), fill=(120, 200, 245, 220))
    if t >= s["answer_t"]:
        word(frame, "FLOATS!" if res == "float" else "SINKS!", t, s["answer_t"], size=150, col=(46, 140, 255) if res == "float" else (110, 110, 130))
    else:
        word(frame, f"{key.upper()}: SINK OR FLOAT?", t, s["t0"], size=100, maxw=1600)
    side_kids(frame, t, xs=(200, 1780), scale=0.3)


def scene_sinksum(frame, s, t):
    tank(frame, t, s["done"])
    rt(frame, 1520, SURF - 10, "FLOAT", 80, colour=(46, 140, 255))
    rt(frame, 1520, BOTTOM - 20, "SINK", 80, colour=(120, 120, 140))
    word(frame, "YOU'RE A SCIENTIST!", t, s["t0"], size=110)
    side_kids(frame, t, "excited", xs=(200, 1780), scale=0.3)


def scene_toy(frame, s, t):
    bath_kids(frame, t, None)
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.4:
            for j in range(3):
                r = 120 + 110 * j + 140 * (q % 0.7)
                d.arc((960 - r, 380 - r, 960 + r, 380 + r), -50, 50, fill=(255, 255, 255, 200), width=10)
                d.arc((960 - r, 380 - r, 960 + r, 380 + r), 130, 230, fill=(255, 255, 255, 200), width=10)
        rt(frame, 960, 380, "?", int(200 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], size=120)
    else:
        k = ease_back((t - s["answer_t"]) / 0.4)
        item(frame, s["toy"], 960, TUB[1] - 120 * k + 8 * math.sin(t * 3), 260 * max(0.1, k))
        word(frame, s["toy"].upper() + "!", t, s["answer_t"], size=140)


def scene_drain(frame, s, t):
    q = t - s["drain_t"]
    water = max(0, 1 - q / 4.0)
    tub_back(frame, water)
    d = ImageDraw.Draw(frame, "RGBA")
    if water > 0:
        cx, cy = TUB[0] + 160, TUB[1] + 10
        for j in range(4):
            a0 = (t * 400 + j * 90) % 360
            r = 30 + 14 * j
            d.arc((cx - r, cy - r * 0.4, cx + r, cy + r * 0.4), a0, a0 + 120, fill=(60, 140, 210, 255), width=6)
    tub_front(frame, t, foam=water, water=water)
    item(frame, "duck", 1160, TUB[1] - 30 + (1 - water) * 30 + 6 * math.sin(t * 3), 200)
    side_kids(frame, t, "happy", xs=(200, 1720))
    word(frame, "GLUG, GLUG!", t, s["drain_t"], size=150, col=(46, 140, 255))


def scene_order(frame, s, t):
    keys = ["towel", "pyjamas", "toothbrush_cup"]
    start = {"towel": 2, "pyjamas": 0, "toothbrush_cup": 1}
    times = {"towel": s["o1"], "pyjamas": s["o2"], "toothbrush_cup": s["o3"]}
    d = ImageDraw.Draw(frame, "RGBA")
    for i, lab in enumerate(("FIRST", "NEXT", "LAST")):
        x = 560 + i * 400
        d.rounded_rectangle((x - 160, 330, x + 160, 690), radius=30, fill=(255, 255, 255, 170), outline=INK, width=6)
        rt(frame, x, 760, lab, 70, colour=RAINBOW[i * 2])
    for k in keys:
        tk = times[k]
        a, b = 560 + start[k] * 400, 560 + keys.index(k) * 400
        f = ease_io(min(1, max(0, (t - tk) / 0.6)))
        x = a + (b - a) * f
        y = 510 - 160 * math.sin(math.pi * f)
        item(frame, k, x, y, 260)
        if t >= tk + 0.6:
            rt(frame, b + 120, 360, str(keys.index(k) + 1), 80, colour=(59, 193, 74))
    word(frame, "WHAT COMES FIRST?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(150, 1780), scale=0.28)


def scene_dance(frame, s, t):
    floaters(frame, t)
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv = s["move"]
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, dx = 0, 0, 0
        if mv == "scrub":
            rot = 6 * math.sin(q * 12 + i)
        elif mv == "splash":
            hop = 70 * abs(math.sin(q * 5 + i))
        elif mv == "shake":
            dx = 16 * math.sin(q * 40)
        elif mv == "pop":
            hop = 40 * abs(math.sin(q * 7 + i))
        elif mv == "wiggle":
            rot = 9 * math.sin(q * 9 + i)
        elif mv == "dry":
            dx = 30 * math.sin(q * 6 + i)
        body(frame, n, t, "excited" if mv in ("splash", "pop") else "happy", x + dx, scale=0.55, hop=hop, rot=rot, wave=True)
    if mv == "dry":
        item(frame, "towel", 960, 520, 260, rot=15 * math.sin(q * 6))
    word(frame, s["word"], t, s["t0"], size=120)


def scene_quiz(frame, s, t):
    floaters(frame, t, 10)
    q = t - s["t0"]
    rt(frame, 960, 120, s["q"], int(80 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        if s["vis"] == "grownup":
            rt(frame, 960, 560, "GROWN-UP!", int(170 * k), colour=(255, 77, 109), maxw=1200)
        else:
            item(frame, s["vis"], 960, 560, 380 * k)
        stars_ring(frame, 960, 560, 360, 250, t, n=8, r=20)
        side_kids(frame, t, "happy")
    else:
        rt(frame, 960, 560, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t)


def scene_outro(frame, s, t):
    floaters(frame, t)
    bath_kids(frame, t, "happy" if t >= s["bye_t"] else None)
    item(frame, "duck", 960, TUB[1] - 20 + 8 * math.sin(t * 3), 180)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 150, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 150, "SQUEAKY CLEAN!", int(130 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


def scene_muddy(frame, s, t):
    q = t - s["t0"]
    for n, x in (("gul", 760), ("misheal", 1160)):
        emo = ("sad" if t < s["germ_t"] else "happy") if n == "gul" else ("surprised" if q < 2.5 else None)
        body(frame, n, t, emo, x, scale=0.5, hop=25 * abs(math.sin(t * 6)) if n == "gul" and q < 2.0 else 0)
    d = ImageDraw.Draw(frame, "RGBA")
    rng = np.random.default_rng(4)
    for j in range(22):
        x = 760 + rng.uniform(-150, 150)
        y = 1075 - rng.uniform(40, 820)
        r = rng.uniform(14, 34)
        d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=(122, 82, 44, 230))
    if t >= s["germ_t"]:
        word(frame, "WASH AWAY DIRT & GERMS!", t, s["germ_t"], size=100, col=(46, 140, 255), maxw=1700)
    else:
        word(frame, "OH NO! MUDDY!", t, s["t0"], size=140, col=(122, 82, 44))


def scene_bubsize(frame, s, t):
    bath_kids(frame, t, "happy")
    d = ImageDraw.Draw(frame, "RGBA")
    sizes = [70, 140] if s["n"] == 2 else [60, 120, 190]
    order = [1, 0] if s["n"] == 2 else [0, 2, 1]
    xs = [700, 1220] if s["n"] == 2 else [560, 960, 1360]
    target = (max if s["ans"] == "big" else min)(range(len(sizes)), key=lambda i: sizes[order[i]])
    for i, x in enumerate(xs):
        r = sizes[order[i]]
        y = 250 + 15 * math.sin(t * 2 + i)
        if t >= s["answer_t"] and i == target:
            k = t - s["answer_t"]
            r *= 1 + 0.08 * math.sin(k * 10)
            d.ellipse((x - r - 18, y - r - 18, x + r + 18, y + r + 18), outline=(59, 193, 74, 255), width=10)
        bubble(d, x, y, r)
    word(frame, ("BIGGER?" if s["n"] == 2 else "BIGGEST?") if s["ans"] == "big" else "SMALLER?", t, s["t0"], size=130)


def scene_ducks(frame, s, t):
    tub_back(frame)
    for n, x in (("gul", 760), ("misheal", 1160)):
        head(frame, n, t, "excited", x, 515 + 8 * math.sin(t * 2 + (0 if n == "gul" else 1.4)), scale=0.46)
    tub_front(frame, t)
    n = sum(1 for d0 in s["dts"] if t >= d0)
    for i in range(n):
        x = 520 + i * 220
        k = ease_back(min(1, (t - s["dts"][i]) / 0.4))
        item(frame, "duck", x, TUB[1] - 40 - 60 * k + 6 * math.sin(t * 3 + i), 160 * k)
        rt(frame, x, TUB[1] - 200, str(i + 1), int(80 * k), colour=RAINBOW[i % 6])
    word(frame, f"{n} DUCKS!" if n else "COUNT THE DUCKS!", t, s["dts"][n - 1] if n else s["t0"], size=120)


def scene_swim(frame, s, t):
    floaters(frame, t, 10)
    bath_kids(frame, t, "excited")
    k = ease_back(min(1, (t - s["t0"]) / 0.5))
    item(frame, s["animal"], 960, TUB[1] - 150 * k + 10 * math.sin(t * 3), 300 * max(0.1, k))
    word(frame, s["animal"].upper() + "!", t, s["say_t"], size=130, col=(46, 140, 255))


def scene_rubadub(frame, s, t):
    floaters(frame, t, 12)
    bath_kids(frame, t, "happy")
    for i in range(3):
        item(frame, "duck", 760 + i * 200, TUB[1] - 30 - 25 * abs(math.sin(t * 4 + i)), 170, rot=8 * math.sin(t * 4 + i))
    cur = s["l3"] if t >= s["l3"] else (s["l2"] if t >= s["l2"] else s["l1"])
    word(frame, "RUB-A-DUB-DUB!", t, cur, size=140)


def scene_surprise(frame, s, t):
    bath_kids(frame, t, "excited")
    d = ImageDraw.Draw(frame, "RGBA")
    cx, cy = 960, 260
    if t < s["pop_t"] + 0.1:
        r = 150 + 8 * math.sin(t * 5)
        bubble(d, cx, cy, r)
        d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=(255, 255, 255, 120))
        rt(frame, cx, cy, "?", 140, colour=(120, 160, 220))
    else:
        k = t - s["pop_t"] - 0.1
        if k < 0.4:
            r = 150 + 120 * k / 0.4
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(150, 210, 250, int(255 * (1 - k / 0.4))), width=10)
        item(frame, s["key"], cx, cy + 6 * math.sin(t * 3), 260 * ease_back(k / 0.4))
        word(frame, s["key"].upper() + "!", t, s["pop_t"] + 0.1, y=110, size=130)


def scene_opp(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, (w, ic, t0, col) in enumerate(((s["w1"], s["i1"], s["a_t"], (255, 107, 107)), (s["w2"], s["i2"], s["b_t"], (46, 140, 255)))):
        x = 600 + j * 720
        if t < t0:
            continue
        k = ease_back((t - t0) / 0.35)
        d.rounded_rectangle((x - 280, 230, x + 280, 760), radius=40, fill=(255, 255, 255, 200), outline=INK, width=6)
        if ic == "drop":
            r = 120 * k
            d.polygon([(x, 380 - r * 1.5), (x + r, 500), (x - r, 500)], fill=(110, 195, 245))
            d.ellipse((x - r, 500 - r, x + r, 500 + r), fill=(110, 195, 245), outline=INK, width=6)
        elif ic in ("bigbubble", "smallbubble"):
            bubble(d, x, 480, (150 if ic == "bigbubble" else 50) * k)
        else:
            item(frame, ic, x, 480, 300 * k)
        rt(frame, x, 690, w.upper() + "!", int(90 * k), colour=col)
    word(frame, "OPPOSITES!", t, s["t0"], size=120)
    side_kids(frame, t, xs=(150, 1770), scale=0.28)


def scene_thisway(frame, s, t):
    bath_kids(frame, t, "happy")
    d = ImageDraw.Draw(frame, "RGBA")
    cx, cy = 960, 175
    d.rounded_rectangle((cx - 130, cy - 130, cx + 130, cy + 130), radius=40, fill=(255, 255, 255, 230), outline=INK, width=6)
    item(frame, "hand", cx, cy, 220)
    item(frame, "soap", cx + 70 * math.cos(t * 5), cy + 50 * math.sin(t * 5), 110)
    for j in range(8):
        bubble(d, cx - 120 + (j * 37) % 240, cy - 110 + (j * 61) % 220, 16 + (j % 3) * 5)
    cur = max([x for x in s["l"] if t >= x] or [s["t0"]])
    word(frame, "THIS IS THE WAY!", t, s["t0"], y=1000, size=90, col=(46, 140, 255))


SCENES = {"intro": scene_intro, "title": scene_title, "need": scene_need, "fill": scene_fill, "wash": scene_wash, "rinse": scene_rinse,
          "bubbles": scene_bubbles, "popcol": scene_popcol, "sinkintro": scene_sinkintro, "sink": scene_sink, "sinksum": scene_sinksum,
          "toy": scene_toy, "drain": scene_drain, "order": scene_order, "dance": scene_dance, "quiz": scene_quiz, "outro": scene_outro,
          "muddy": scene_muddy, "bubsize": scene_bubsize, "ducks": scene_ducks, "swim": scene_swim,
          "rubadub": scene_rubadub, "surprise": scene_surprise, "opp": scene_opp, "thisway": scene_thisway}


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
        sheet.save(HERE / "_sheet.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "3"))
    parts = 24
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Bath Time for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=0", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
