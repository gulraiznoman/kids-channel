"""Animate Long video 4 "Good Habits / Morning Routine" (1920x1080) from timeline.json.
Uses drawing helpers from long02-counting/render.py.

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L04 Good Habits/Good Habits for Kids vN.mp4
"""
import json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "long02-counting"))
import render as R

W, H, FPS = R.W, R.H, R.FPS
G = R.G
INK, RAINBOW = R.INK, R.RAINBOW
OUT = ROOT / "VIDEOS" / "L04 Good Habits"
ART_DIRS = [(HERE / "art", "item_"), (ROOT / "ep01-fruits" / "art", "fruit_"), (ROOT / "halloween01" / "art", "item_"),
            (ROOT / "long03-fruits-veg" / "art", "item_"), (ROOT / "long01-animals-fun" / "art", "fruit_")]
S = R.S
CHAR = {"gul": dict(home="polo", school="bluetee", x=250, girl=False, voc="gul"),
        "misheal": dict(home="kurta", school="pink", x=1670, girl=True, voc="mishu")}
ease_back, ease_io, rt, paste = R.ease_back, R.ease_io, R.rainbow_text, R.paste


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["fonts"], G["cache"], G["sized"] = {}, {}, {}
    G["art"] = {}
    for d, pre in ART_DIRS:
        for p in d.glob(f"{pre}*.png"):
            G["art"].setdefault(p.stem[len(pre):], Image.open(p).convert("RGBA"))
    G["layers"], G["mouth"] = {}, {}
    for n in CHAR:
        L = {p.stem: (lambda im: im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS))(Image.open(p))
             for p in (R.KIT / n).glob("*.png")}
        G["layers"][n] = L
        bb = L["mouth_smile"].getbbox()
        G["mouth"][n] = ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)
    G["env"] = {}
    for n, c in CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["bg"] = {n: Image.open(HERE / "art" / f"bg_{n}.png").convert("RGBA") for n in ("bedroom", "bathroom", "hall")}
    G["bg"]["kitchen"] = Image.open(ROOT / "long03-fruits-veg" / "art" / "bg_kitchen.png").convert("RGBA")
    G["bg"]["road"] = Image.open(ROOT / "long01-animals-fun" / "art" / "bg_road.png").convert("RGBA").resize((W, H), Image.LANCZOS)
    night = G["bg"]["bedroom"].copy()                                    # bedroom at night: navy wash + stars
    night.alpha_composite(Image.new("RGBA", night.size, (30, 36, 90, 150)))
    dn = ImageDraw.Draw(night)
    rng = np.random.default_rng(2)
    for _ in range(50):
        x, y, s2 = rng.uniform(0, W), rng.uniform(0, 700), rng.uniform(2, 5)
        dn.ellipse((x - s2, y - s2, x + s2, y + s2), fill=(255, 250, 210))
    G["bg"]["night"] = night
    G["SC"] = {}
    for s in tl["scenes"]:
        G["SC"].setdefault(s["kind"], s)


def spotlight(frame, cx, cy, r):
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 190), outline=(255, 214, 102, 255), width=8)
    frame.alpha_composite(lay)


def chant_text(frame, times, t, y=150):
    cur = None
    for t0 in times:
        if t >= t0:
            cur = t0
    if cur is not None:
        txt = next(e["text"] for e in G["lines"] if abs(e["t"] - cur) < 0.01)
        rt(frame, 960, y, txt.upper().rstrip("!"), int(90 * ease_back((t - cur) / 0.3)), maxw=1300)


def bubbles_at(frame, cx, cy, t, n=8, spread=120):
    d = ImageDraw.Draw(frame)
    for j in range(n):
        p = (t * 0.7 + j / n) % 1
        x = cx + spread * math.sin(j * 2.1 + t) * (0.4 + p)
        y = cy - p * 160
        r = 10 + 14 * ((j * 7) % 3)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(234, 246, 255), outline=(150, 200, 230), width=3)
        d.ellipse((x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.2), fill=(255, 255, 255))


# ------------------------------------------------------------------ Gul & Mishu (outfit change, sleepy eyes, toothbrush)
def outfit(n, t):
    dress = G["SC"].get("dress")
    key = "change_gul" if n == "gul" else "change_mishu"
    return CHAR[n]["school"] if dress and t >= dress[key] else CHAR[n]["home"]


def draw_kids(frame, t):
    wake = G["SC"]["wake"]
    brush = G["SC"]["brush"]
    bed = G["SC"]["bed"]
    for n, c in CHAR.items():
        L = G["layers"][n]
        o = outfit(n, t)
        env = G["env"][n]
        v = env[min(int(t * FPS), len(env) - 1)]
        talking = v > 0.12
        asleep = t < wake["wake_t"] - 0.3
        mouth = "smile" if not talking else ("o" if v < 0.5 else "open")
        eyes = "closed" if asleep else ("blink" if (t + (1.3 if n == "gul" else 0)) % 4.1 < 0.12 else "open")
        im = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for p in (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}"]:
            im.alpha_composite(L[p])
        stretching = bed["stretch_t"] <= t < bed["t1"]
        if talking or stretching:
            a = L[f"arm_r_wave_{o}"]
            ang = 18 * math.sin(t * 4) if stretching else 10 * math.sin(t * 7)
            im.alpha_composite(a.rotate(ang, center=(a.width * 0.66, a.height * 0.53), resample=Image.BICUBIC))
        else:
            im.alpha_composite(L[f"arm_r_down_{o}"])
        for p in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if c["girl"] else []):
            im.alpha_composite(L[p])
        hop = 10 * abs(math.sin(t * 5)) if talking else 4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0)))
        if stretching:
            hop = 45 * abs(math.sin(t * 3))
        x0, y0 = int(c["x"] - im.width / 2), int(1075 - 0.93 * im.height - hop)
        # poof when changing clothes
        dress = G["SC"].get("dress")
        if dress:
            q = t - dress["change_gul" if n == "gul" else "change_mishu"]
            if 0 <= q < 0.5:
                d = ImageDraw.Draw(frame)
                for j in range(10):
                    ang = j / 10 * 2 * math.pi
                    r = 120 + 200 * q
                    rr = 60 * (1 - q * 1.6) + 10
                    d.ellipse((c["x"] + r * math.cos(ang) - rr, 700 + r * math.sin(ang) * 1.4 - rr,
                               c["x"] + r * math.cos(ang) + rr, 700 + r * math.sin(ang) * 1.4 + rr), fill=(255, 255, 255))
        frame.alpha_composite(im, (x0, y0))
        mx, my = x0 + G["mouth"][n][0], y0 + G["mouth"][n][1]
        if asleep:                                                  # Zzz
            for j in range(3):
                p = (t * 0.6 + j / 3) % 1
                rt(frame, mx + 80 + p * 90, my - 140 - p * 160, "Z", int(40 + 30 * p), colour=(150, 160, 255))
        if brush["brush_t"] <= t < brush["rinse_t"]:                # little toothbrush + foam at the mouth
            off = 14 * math.sin(t * 22)
            paste(frame, "toothbrush", mx + 70 + off, my + 10, 170, -10 if n == "gul" else 10)
            bubbles_at(frame, mx, my + 10, t, n=4, spread=50)
        if brush["shine_t"] <= t < brush["brush_end"]:
            d = ImageDraw.Draw(frame)
            for j in range(3):
                R.star(d, mx - 50 + j * 50, my - 30 - 20 * abs(math.sin(t * 6 + j)), 14, (255, 230, 90), rot=t * 3)


# ------------------------------------------------------------------ helpers for this video
def tooth(frame, cx, cy, s, shiny, t):
    d = ImageDraw.Draw(frame)
    u = s / 300
    pts = [(cx - 130 * u, cy - 110 * u), (cx - 60 * u, cy - 150 * u), (cx, cy - 120 * u), (cx + 60 * u, cy - 150 * u),
           (cx + 130 * u, cy - 110 * u), (cx + 140 * u, cy), (cx + 100 * u, cy + 150 * u), (cx + 50 * u, cy + 160 * u),
           (cx + 20 * u, cy + 60 * u), (cx - 20 * u, cy + 60 * u), (cx - 50 * u, cy + 160 * u), (cx - 100 * u, cy + 150 * u), (cx - 140 * u, cy)]
    d.polygon(pts, fill=(255, 255, 255) if shiny else (255, 248, 214), outline=INK, width=8)
    for ex in (-45, 45):
        d.ellipse((cx + ex * u - 16 * u, cy - 50 * u - 22 * u, cx + ex * u + 16 * u, cy - 50 * u + 22 * u), fill=INK)
        d.ellipse((cx + ex * u - 8 * u, cy - 60 * u - 6 * u, cx + ex * u, cy - 60 * u + 2 * u), fill=(255, 255, 255))
    d.arc((cx - 40 * u, cy - 20 * u, cx + 40 * u, cy + 30 * u), 20, 160, fill=INK, width=int(8 * u) + 2)
    if not shiny:
        for j in range(5):
            d.ellipse((cx - 110 * u + j * 50 * u, cy + 70 * u + (j % 2) * 30 * u, cx - 90 * u + j * 50 * u, cy + 90 * u + (j % 2) * 30 * u), fill=(220, 200, 140))


def check(frame, cx, cy, s):
    d = ImageDraw.Draw(frame)
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=(76, 175, 80), outline=INK, width=4)
    d.line((cx - s * 0.5, cy, cx - s * 0.1, cy + s * 0.4, cx + s * 0.55, cy - s * 0.4), fill=(255, 255, 255), width=int(s * 0.25) + 1)


# ------------------------------------------------------------------ scenes
def scene_wake(frame, s, t):
    r = s["ring_t"]
    shake = 14 * math.sin(t * 50) if r <= t < r + 1.6 else 0
    spotlight(frame, 960, 520, 260)
    paste(frame, "clock", 960 + shake, 520, 400, shake * 0.6)
    if r <= t < r + 1.6:
        rt(frame, 960, 180, "RING RING!", int(140 * ease_back((t - r) / 0.3)))
    elif t >= s["wake_t"]:
        rt(frame, 960, 180, "GOOD MORNING!", int(130 * ease_back((t - s["wake_t"]) / 0.4)))
    else:
        rt(frame, 960, 180, "SHH... SLEEPING", 90, colour=(150, 160, 255))


def scene_bed(frame, s, t):
    k = (t - s["fix_t"]) / 0.4
    if t < s["fix_t"]:
        paste(frame, "bed_messy", 960, 620, 640)
    else:
        paste(frame, "bed_neat", 960, 620, 640 * (1 + 0.06 * max(0, 1 - k) * math.sin(k * 12)))
        R.stars_burst(frame, t)
    if t >= s["stretch_t"]:
        rt(frame, 960, 180, "STRETCH!", int(140 * ease_back((t - s["stretch_t"]) / 0.4)))
    elif t >= s["fix_t"]:
        rt(frame, 960, 180, "NICE AND NEAT!", int(120 * ease_back(k)))
    else:
        rt(frame, 960, 180, "MESSY BED!", int(120 * ease_back((t - s["t0"]) / 0.4)))


def scene_brush(frame, s, t):
    if t < s["brush_t"]:
        paste(frame, "toothpaste", 820, 560, 360)
        paste(frame, "toothbrush", 1110, 560, 360)
        if t >= s["paste_t"]:
            d = ImageDraw.Draw(frame)
            q = min(1, (t - s["paste_t"]) / 0.5)
            d.ellipse((1150 - 30 * q, 470 - 18 * q, 1150 + 30 * q, 470 + 18 * q), fill=(126, 217, 87), outline=INK, width=3)
        rt(frame, 960, 180, "PEA SIZE!", int(120 * ease_back((t - s["t0"]) / 0.4)))
        return
    shiny = t >= s["shine_t"]
    tooth(frame, 960, 600, 380, shiny, t)
    if t < s["rinse_t"]:
        off = 90 * math.sin(t * 7)
        paste(frame, "toothbrush", 960 + off, 560 + 60 * math.sin(t * 3.5), 420, 25 * math.sin(t * 7))
        bubbles_at(frame, 960, 700, t, n=12, spread=200)
        chant_text(frame, s["chant"], t)
    elif shiny:
        d = ImageDraw.Draw(frame)
        for j in range(10):
            ang = j / 10 * 2 * math.pi + t
            R.star(d, 960 + 330 * math.cos(ang), 600 + 300 * math.sin(ang), 26, (255, 225, 80), rot=t * 2)
        rt(frame, 960, 180, "SPARKLY CLEAN!", int(130 * ease_back((t - s["shine_t"]) / 0.4)))
    else:
        rt(frame, 960, 180, "RINSE AND SPIT!", int(120 * ease_back((t - s["rinse_t"]) / 0.4)))
        R.paste(frame, "water", 960, 380, 200)


def scene_wash(frame, s, t):
    steps = s["steps"]
    for i, (t0, word, icon) in enumerate(steps):                    # step badges along the top
        if t >= t0:
            x = 560 + i * 200
            g = ease_back((t - t0) / 0.4)
            paste(frame, icon, x, 160, 120 * g)
            R.badge(frame, x - 50, 110, i + 1, t - t0)
            rt(frame, x, 255, word, int(42 * g), colour=(255, 255, 255))
    cur = max([i for i, st in enumerate(steps) if t >= st[0]], default=-1)
    scrubbing = s["scrub_t"] <= t < s["scrub_end"]
    rub = 40 * math.sin(t * 9) if (scrubbing or cur == 2) else 0
    hand = G["art"]["hands"]
    for flip, x in ((False, 860), (True, 1060)):
        im = R.item("hands", 380)
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        frame.alpha_composite(im, (int(x - 190 + (rub if flip else -rub) * 0.6), int(620 - 190 + abs(rub) * 0.3)))
    if cur >= 2 and t < steps[3][0] if len(steps) > 3 else cur >= 2:
        bubbles_at(frame, 960, 680, t, n=14, spread=260)
    if len(steps) > 3 and steps[3][0] <= t < steps[4][0]:
        d = ImageDraw.Draw(frame)
        for j in range(14):
            p = (t * 1.5 + j / 14) % 1
            x = 860 + (j * 37) % 220
            d.ellipse((x - 9, 380 + p * 420 - 14, x + 9, 380 + p * 420 + 14), fill=(110, 190, 255))
    if len(steps) > 4 and t >= steps[4][0]:
        paste(frame, "towel", 960 + 60 * math.sin(t * 4), 620, 330)
    if scrubbing:
        chant_text(frame, s["chant"], t, y=360)
        if t >= s["chant"][0]:
            rt(frame, 960, 960, "SCRUB FOR 20 SECONDS!", 54, colour=(255, 255, 255))


def scene_dress(frame, s, t):
    keys = [k for t0, k in s["items"] if t >= t0]
    n = len(keys)
    for i, (t0, k) in enumerate(s["items"]):
        if t < t0:
            continue
        x = 960 + (i - (len(s["items"]) - 1) / 2) * 260
        g = ease_back((t - t0) / 0.4)
        y = 560 + 10 * math.sin(t * 2 + i)
        if t >= s["change_gul"]:                                       # clothes fly onto Gul and Mishu
            q = ease_io((t - s["change_gul"]) / 0.6)
            tx = 250 if i % 2 == 0 else 1670
            x, y, g = x + (tx - x) * q, y + (650 - y) * q, g * (1 - q)
        if g > 0.02:
            spotlight(frame, x, y, 120 * g) if t < s["change_gul"] else None
            paste(frame, k, x, y, 230 * g)
            rt(frame, x, y + 160, k.upper(), int(46 * g), colour=(255, 255, 255))
    if s["q_t"] <= t < s["items"][-1][0]:
        rt(frame, 960, 180, "SOCKS OR SHOES FIRST?", int(100 * ease_back((t - s["q_t"]) / 0.4)))
    elif t >= s["change_gul"]:
        rt(frame, 960, 180, "ALL DRESSED!", int(130 * ease_back((t - s["change_gul"]) / 0.4)))
    else:
        rt(frame, 960, 180, "GET DRESSED!", int(120 * ease_back((t - s["t0"]) / 0.4)))


def scene_breakfast(frame, s, t):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((470, 700, 1450, 760), radius=20, fill=(205, 150, 90), outline=INK, width=6)
    d.rectangle((520, 760, 560, 960), fill=(180, 125, 70), outline=INK, width=5)
    d.rectangle((1360, 760, 1400, 960), fill=(180, 125, 70), outline=INK, width=5)
    eaten = t >= s["eat_t"]
    for i, (t0, k) in enumerate(s["food"]):
        if t < t0:
            continue
        x = 560 + i * 160
        g = ease_back((t - t0) / 0.4)
        if eaten:
            g *= max(0.0, 1 - (t - s["eat_t"] - i * 0.1) / 0.6)
        size = 200 * g
        if size > 3:
            paste(frame, k, x, 610 - (20 if i % 2 else 0), size)
    cur = [k for t0, k in s["food"] if t >= t0]
    if eaten:
        rt(frame, 960, 180, "CHEW, CHEW, CHEW!", int(120 * ease_back((t - s["eat_t"]) / 0.4)))
    elif cur:
        last = [(t0, k) for t0, k in s["food"] if t >= t0][-1]
        rt(frame, 960, 180, last[1].upper(), int(140 * ease_back((t - last[0]) / 0.35)), start=last[0], t=t)


def scene_bag(frame, s, t):
    zipped = t >= s["zip_t"]
    paste(frame, "backpack", 960, 640, 460 * (1 + (0.05 * math.sin((t - s["zip_t"]) * 14) if zipped and t < s["zip_t"] + 0.6 else 0)))
    for i, (t0, k) in enumerate(s["packed"]):
        if t < t0:
            continue
        q = t - t0
        x0, y0 = 960, 300
        if q < 0.5:
            paste(frame, k, x0, y0, 220 * ease_back(q / 0.4))
        elif q < 1.1:
            k2 = ease_io((q - 0.5) / 0.6)
            paste(frame, k, x0, y0 + (560 - y0) * k2, 220 * (1 - 0.8 * k2))
        x = 560 + i * 200                                                # checklist row with green ticks
        paste(frame, k, x, 950, 110)
        if q > 0.9:
            check(frame, x + 45, 915, 26)
    if s["q_t"] <= t < s["packed"][-1][0]:
        rt(frame, 960, 160, "WHAT DID WE FORGET?", int(100 * ease_back((t - s["q_t"]) / 0.4)))
    elif zipped:
        rt(frame, 960, 160, "READY FOR SCHOOL!", int(120 * ease_back((t - s["zip_t"]) / 0.4)))


def scene_polite(frame, s, t):
    cur = None
    for t0, word, who in s["words"]:
        if t >= t0:
            cur = (t0, word, who)
    if cur:
        t0, word, who = cur
        g = ease_back((t - t0) / 0.4)
        d = ImageDraw.Draw(frame)
        x = 820 if who == "gul" else 1100
        w, h = 760 * g, 230 * g
        if w > 10:
            d.rounded_rectangle((x - w / 2, 330 - h / 2, x + w / 2, 330 + h / 2), radius=int(h / 2), fill=(255, 255, 255), outline=INK, width=8)
            tail = 520 if who == "gul" else 1400
            d.polygon([(x + (-120 if who == "gul" else 120), 330 + h / 2 - 6), (tail, 470), (x + (-40 if who == "gul" else 40), 330 + h / 2 - 6)],
                      fill=(255, 255, 255), outline=INK)
            rt(frame, x, 340, word, int(100 * g), maxw=int(w - 60))
    g0 = s["give_t"]
    if g0 <= t < g0 + 1.2:                                              # crayon passes from Gul to Mishu
        k = ease_io((t - g0) / 1.0)
        paste(frame, "crayon", 450 + (1470 - 450) * k, 700 - 200 * math.sin(k * math.pi), 180, k * 360)
    elif t >= g0 + 1.2:
        paste(frame, "crayon", 1470, 700, 150)
    b0 = s["bump_t"]
    if b0 <= t < b0 + 0.6:
        rt(frame, 960, 700, "BONK!", int(120 * ease_back((t - b0) / 0.2)), colour=(255, 159, 28))
    s0 = s["sneeze_t"]
    if s0 + 0.3 <= t < s0 + 1.1:
        rt(frame, 1400, 620, "ACHOO!", int(110 * ease_back((t - s0 - 0.3) / 0.2)), colour=(110, 190, 255))
    rt(frame, 960, 120, "MAGIC WORDS", 80, colour=(255, 255, 255))


def scene_habit(frame, s, t):
    a = t - s["t0"]
    spotlight(frame, 820, 560, 270)
    paste(frame, s["key"], 820, 560 + 8 * math.sin(t * 2.2), 420 * ease_back(a / 0.45))
    if t >= s["answer_t"]:
        q = t - s["answer_t"]
        paste(frame, "thumbsup" if s["good"] else "thumbsdown", 1260, 560 - 20 * abs(math.sin(q * 5)) * max(0, 1 - q), 300 * ease_back(q / 0.4))
        rt(frame, 960, 170, "GOOD HABIT!" if s["good"] else "BAD HABIT!", int(130 * ease_back(q / 0.35)),
           colour=None if s["good"] else (255, 107, 107))
    else:
        rt(frame, 960, 170, "GOOD OR BAD?", int(120 * ease_back(a / 0.4)))


def scene_outro(frame, s, t):
    for i, k in enumerate(("toothbrush", "soap", "bed_neat", "shirt", "oatmeal", "backpack", "sharing")):
        x = 540 + i * 140
        paste(frame, k, x, 560 - 30 * abs(math.sin(t * 3 + i)), 160 * ease_back((t - s["t0"] - i * 0.1) / 0.4))
    if t >= s["bye_t"]:
        rt(frame, 960, 230, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.4)))
    else:
        chant_text(frame, s["chant"], t, y=230)


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rt(frame, 960, 380, s["title"], int(150 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1300)


def scene_exercise(frame, s, t):
    cur = None
    for t0, word in s["moves"]:
        if t >= t0:
            cur = (t0, word)
    if cur:
        t0, word = cur
        q = t - t0
        rt(frame, 960, 420, word, int(220 * ease_back(q / 0.35) * (1 + 0.06 * math.sin(q * 10))))
        d = ImageDraw.Draw(frame)
        for j in range(8):
            ang = j / 8 * 2 * math.pi + q * 2
            R.star(d, 960 + 420 * math.cos(ang), 450 + 200 * math.sin(ang), 24, RAINBOW[j % 6], rot=q * 3)
    else:
        rt(frame, 960, 420, "LET'S MOVE!", int(160 * ease_back((t - s["t0"]) / 0.4)))


def scene_weather(frame, s, t):
    w = s["weather"]
    d = ImageDraw.Draw(frame)
    if w == "rainy":                                                     # rain drops falling
        for j in range(40):
            p = (t * 1.3 + j / 40) % 1
            x = (j * 97) % 1920
            d.line((x, -40 + p * 1100, x - 10, -10 + p * 1100), fill=(110, 170, 255), width=6)
        paste(frame, "cloudy", 960, 250, 360)
    elif w == "cold":
        for j in range(40):
            p = (t * 0.4 + j / 40) % 1
            x = (j * 97) % 1920 + 30 * math.sin(t + j)
            d.ellipse((x - 8, -20 + p * 1100 - 8, x + 8, -20 + p * 1100 + 8), fill=(255, 255, 255))
        paste(frame, "snowy", 960, 250, 340)
    else:
        paste(frame, "sunny", 960, 250, 360, t * 20)
    if t >= s["answer_t"]:
        n = len(s["items"])
        for i, k in enumerate(s["items"]):
            x = 960 + (i - (n - 1) / 2) * 300
            g = ease_back((t - s["answer_t"] - i * 0.3) / 0.4)
            if g > 0:
                spotlight(frame, x, 640, 140 * g)
                paste(frame, k, x, 640 + 8 * math.sin(t * 2 + i), 250 * g)
    else:
        rt(frame, 960, 560, {"rainy": "RAINY!", "cold": "COLD!", "sunny": "SUNNY!"}[w], int(150 * ease_back((t - s["t0"]) / 0.4)))


def scene_junk(frame, s, t):
    a = t - s["t0"]
    spotlight(frame, 820, 560, 260)
    paste(frame, s["key"], 820, 560 + 8 * math.sin(t * 2.2), 400 * ease_back(a / 0.45))
    if t >= s["answer_t"]:
        q = t - s["answer_t"]
        paste(frame, "thumbsup" if s["healthy"] else "thumbsdown", 1260, 560, 280 * ease_back(q / 0.4))
        rt(frame, 960, 170, "HEALTHY!" if s["healthy"] else "JUNK FOOD!", int(140 * ease_back(q / 0.35)),
           colour=None if s["healthy"] else (255, 107, 107))
    else:
        rt(frame, 960, 170, "HEALTHY OR JUNK?", int(115 * ease_back(a / 0.4)))


def scene_road(frame, s, t):
    green = t >= s["green_t"]
    paste(frame, "traffic_green" if green else "traffic_red", 1400, 470, 420)
    if s["left_t"] <= t < s["right_t"]:
        rt(frame, 760, 300, "<< LOOK LEFT", 90, colour=(255, 255, 255))
    elif s["right_t"] <= t < s["hold_t"]:
        rt(frame, 760, 300, "LOOK RIGHT >>", 90, colour=(255, 255, 255))
    elif s["hold_t"] <= t < s["green_t"]:
        paste(frame, "sharing", 760, 420, 260)
        rt(frame, 760, 220, "HOLD HANDS!", 100)
    elif green:
        rt(frame, 760, 220, "GREEN: GO!", int(130 * ease_back((t - s["green_t"]) / 0.35)), colour=(59, 193, 74))
    else:
        rt(frame, 760, 220, "RED: STOP!", int(130 * ease_back((t - s["red_t"]) / 0.35)), colour=(255, 77, 77))


def scene_tidy(frame, s, t):
    paste(frame, "toybox", 960, 720, 440)
    for i, (t0, k) in enumerate(s["toys"]):
        q = t - t0
        x0, y0 = 520 + i * 176, 940
        if q < 0:                                                        # toys lying on the floor, waiting
            paste(frame, k, x0, y0, 140, 15 * math.sin(i * 2))
            continue
        if q < 1.0:
            k2 = ease_io(q / 1.0)
            paste(frame, k, x0 + (960 - x0) * k2, y0 + (620 - y0) * k2 - 300 * math.sin(k2 * math.pi), 160 * (1 - 0.4 * k2), k2 * 360)
    if t >= s["done_t"]:
        rt(frame, 960, 230, "ALL TIDY!", int(150 * ease_back((t - s["done_t"]) / 0.4)))
    else:
        rt(frame, 960, 230, "TIDY UP!", int(130 * ease_back((t - s["t0"]) / 0.4)))


def scene_help(frame, s, t):
    cur = None
    for t0, keys, word in s["jobs"]:
        if t >= t0:
            cur = (t0, keys, word)
    if cur:
        t0, (a, b), word = cur
        q = t - t0
        g = ease_back(q / 0.4)
        paste(frame, a, 780, 600 + 10 * math.sin(t * 3), 320 * g, 12 * math.sin(t * 2))
        paste(frame, b, 1140, 620, 320 * g)
        if a == "watering_can":
            d = ImageDraw.Draw(frame)
            for j in range(10):
                p = (t * 1.6 + j / 10) % 1
                d.ellipse((930 + j * 8 - 8, 520 + p * 140 - 12, 930 + j * 8 + 8, 520 + p * 140 + 12), fill=(110, 190, 255))
        rt(frame, 960, 220, word, int(100 * g), maxw=1300)


def scene_bedtime(frame, s, t):
    cur = None
    for t0, k, word in s["steps"]:
        if t >= t0:
            cur = (t0, k, word)
    if t >= s["sleep_t"]:
        paste(frame, "moon", 960, 520, 420, 6 * math.sin(t))
        rt(frame, 960, 200, "GOOD NIGHT!", int(150 * ease_back((t - s["sleep_t"]) / 0.4)))
        for j in range(3):
            p = (t * 0.6 + j / 3) % 1
            rt(frame, 1150 + p * 120, 420 - p * 200, "Z", int(50 + 40 * p), colour=(170, 180, 255))
        return
    if cur:
        t0, k, word = cur
        q = t - t0
        spotlight(frame, 960, 560, 250)
        paste(frame, k, 960, 560 + 8 * math.sin(t * 2), 400 * ease_back(q / 0.4))
        if k == "bathtub":
            bubbles_at(frame, 960, 470, t, n=10, spread=200)
        rt(frame, 960, 200, word, int(120 * ease_back(q / 0.35)))


SCENES = {"exercise": scene_exercise, "weather": scene_weather, "junk": scene_junk, "road": scene_road, "tidy": scene_tidy,
          "help": scene_help, "bedtime": scene_bedtime, "wake": scene_wake, "bed": scene_bed, "brush": scene_brush, "wash": scene_wash, "dress": scene_dress,
          "breakfast": scene_breakfast, "bag": scene_bag, "polite": scene_polite, "habit": scene_habit,
          "outro": scene_outro, "title": scene_title}


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SCENES[sc["kind"]](frame, sc, t)
    if sc["kind"] not in ("bed",):
        R.stars_burst(frame, t)
    draw_kids(frame, t)
    R.your_turn(frame, t)
    return frame.convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
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
    dst = OUT / f"Good Habits for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
