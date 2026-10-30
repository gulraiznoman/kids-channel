"""Animate Long video 6 "Dinosaurs for Kids" (1920x1080) from timeline.json.

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L06 Dinosaurs/Dinosaurs for Kids vN.mp4
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

W, H, FPS = 1920, 1080, 30
INK, RAINBOW = R.INK, R.RAINBOW
OUT = ROOT / "VIDEOS" / "L06 Dinosaurs"
KIT = ROOT / "characters" / "layers"
S = 0.36
CHAR = {"gul": dict(outfit="tee", x=230, girl=False, voc="gul"), "misheal": dict(outfit="yellow", x=1690, girl=True, voc="mishu")}
SIZE = {"big": 600, "mid": 460, "small": 230}
SOUND_TEXT = {"brachiosaurus": "HONK!", "parasaurolophus": "HONK!", "diplodocus": "HONK!", "pteranodon": "SKREE!",
              "velociraptor": "SQUEAK!", "compsognathus": "SQUEAK!"}
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


def load_crop(p, size):
    im = Image.open(p).convert("RGBA")
    im = im.crop(im.getbbox())
    k = size / max(im.size)
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    R.G["fonts"] = {}
    G["dino"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in (HERE / "art").glob("dino_*.png")}
    G["item"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in (HERE / "art").glob("item_*.png")}
    G["bg"] = {n: Image.open(HERE / "art" / f"bg_{n}.png").convert("RGBA") for n in ("valley", "dig")}
    G["layers"] = {n: {p.stem: (lambda im: im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS))(Image.open(p))
                       for p in (KIT / n).glob("*.png")} for n in CHAR}
    G["hat"] = {n: (lambda im: im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS))(Image.open(HERE / "art" / f"hat_{n}.png"))
                for n in CHAR}
    G["env"] = {}
    for n, c in CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["sized"], G["cache"] = {}, {}
    rng = np.random.default_rng(5)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]


def sized(kind, key, size):
    k = (kind, key, int(size))
    if k not in G["sized"]:
        if len(G["sized"]) > 300:
            G["sized"].clear()
        G["sized"][k] = load_crop(HERE / "art" / f"{kind}_{key}.png", max(2, int(size)))
    return G["sized"][k]


def put(frame, kind, key, cx, base_y, size, rot=0.0, sx=1.0, sy=1.0, flip=False, bottom=True, alpha=1.0):
    im = sized(kind, key, size)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if sx != 1 or sy != 1:
        im = im.resize((max(1, int(im.width * sx)), max(1, int(im.height * sy))), Image.BICUBIC)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * alpha).astype(np.uint8)
        im = Image.fromarray(a)
    y = base_y - im.height if bottom else base_y - im.height / 2
    frame.alpha_composite(im, (int(cx - im.width / 2), int(y)))
    return im


def plain(frame, cx, cy, text, size, fill=(255, 255, 255)):
    d = ImageDraw.Draw(frame)
    f = R.font(size)
    while d.textlength(text, font=f) > 1500 and size > 20:
        size -= 2
        f = R.font(size)
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, cy - size * 0.62), text, font=f, fill=fill, stroke_width=max(2, int(size * 0.14)), stroke_fill=INK)


def badge(frame, x, y, text):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=(108, 194, 74))


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 20 * abs(math.cos(t * 5 + ph)) + 4
            d.rectangle((x - w / 2, y - 10, x + w / 2, y + 10), fill=col)


def roar_bubble(frame, x, y, t, t0, text="ROAR!"):
    q = t - t0
    if 0 <= q < 1.3:
        s = ease_back(q / 0.25)
        d = ImageDraw.Draw(frame)
        pts = []
        for k in range(20):
            a = k * math.pi / 10
            r = (150 if k % 2 == 0 else 115) * s
            pts.append((x + r * 1.35 * math.cos(a), y + r * 0.75 * math.sin(a)))
        if s > 0.05:
            d.polygon(pts, fill=(255, 235, 80), outline=INK, width=6)
            rt(frame, x, y + 8, text, int(80 * s) or 1, colour=(255, 90, 60))


# ------------------------------------------------------------------ kids with explorer hats
def draw_kids(frame, t, big_hop=False):
    for n, c in CHAR.items():
        L = G["layers"][n]
        o = c["outfit"]
        env = G["env"][n]
        v = env[min(int(t * FPS), len(env) - 1)]
        talking = v > 0.12
        mouth = "smile" if not talking else ("o" if v < 0.5 else "open")
        eyes = "blink" if (t + (1.3 if n == "gul" else 0)) % 4.1 < 0.12 else "open"
        key = (n, eyes, mouth, talking)
        if key not in G["cache"]:
            im = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
            for p in (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}"]:
                im.alpha_composite(L[p])
            im.alpha_composite(L[f"arm_r_{'wave' if talking else 'down'}_{o}"])
            for p in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if c["girl"] else []):
                im.alpha_composite(L[p])
            im.alpha_composite(G["hat"][n])
            if len(G["cache"]) > 40:
                G["cache"].clear()
            G["cache"][key] = im
        im = G["cache"][key]
        hop = 10 * abs(math.sin(t * 5)) if talking else 4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0)))
        if big_hop:
            hop = 40 * abs(math.sin(t * 4 + (0.8 if n == "gul" else 0)))
        frame.alpha_composite(im, (int(c["x"] - im.width / 2), int(1078 - 0.93 * im.height - hop)))


# ------------------------------------------------------------------ scenes
GROUND = 1000


def scene_intro(frame, s, t):
    ck, hk, tk = s["crack_t"], s["hatch_t"], s["title_t"]
    shake = 14 * math.sin(t * 60) if t < ck + 0.2 else 0
    if t < hk + 0.4:
        wob = (6 + 10 * min(1, t / 1.2)) * math.sin(t * 25) if t < hk else 0
        put(frame, "item", "egg", 960 + shake, GROUND, 520, rot=wob)
        if t >= ck:
            d = ImageDraw.Draw(frame)
            q = min(1, (t - ck) / 0.5)
            pts = [(960 - 160 * q, 760), (920, 730), (980, 790), (1040, 740), (960 + 160 * q, 775)]
            d.line(pts, fill=INK, width=8)
    if t >= hk:
        q = t - hk
        put(frame, "item", "egg_bottom", 960, GROUND, 520)
        put(frame, "item", "egg_top", 960 + 300 * min(1, q / 0.6), GROUND - 300 - 400 * math.sin(min(1, q / 0.6) * math.pi / 1.2), 380,
            rot=q * 240, bottom=False)
        sc = ease_back(q / 0.4)
        put(frame, "dino", "trex", 960, GROUND - 210, 380 * sc, rot=6 * math.sin(t * 8))
        roar_bubble(frame, 1300, 520, t, hk + 0.1)
    if t >= tk:
        confetti(frame, t, tk)
        q = (t - tk) / 0.35
        rt(frame, 960, 200, "DINOSAURS!", int(220 * ease_back(q)))
        if q < 1:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - q)))))
    if t >= s["kids_t"] - 0.6:
        draw_kids(frame, t, big_hop=t < s["kids_t"] + 1.5)


def walk_in(s, t, size, from_right=True):
    """Dinosaur stomps in from the side and stops in the centre."""
    q = min(1, (t - s["t0"]) / 1.0)
    x = 960 + (1 - ease_io(q)) * (1300 if from_right else -1300)
    stomp = abs(math.sin((t - s["t0"]) * math.pi * 3)) if q < 1 else 0
    return x, stomp


def scene_dino(frame, s, t):
    size = SIZE[s["size"]]
    x, st = walk_in(s, t, size)
    rot = 4 * math.sin(t * 9) if st else 3 * math.sin(t * 2)
    sq = 1.0
    if s["roar_t"] <= t < s["roar_t"] + 0.6:
        sq = 1 + 0.12 * math.sin((t - s["roar_t"]) * 20) * (1 - (t - s["roar_t"]) / 0.6)
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((x - size * 0.45, GROUND - 30, x + size * 0.45, GROUND + 25), fill=(40, 70, 30, 80))
    frame.alpha_composite(lay)
    im = put(frame, "dino", s["key"], x, GROUND - 25 * st, size, rot=rot, sx=sq, sy=2 - sq)
    roar_bubble(frame, x + im.width * 0.35, GROUND - im.height - 30, t, s["roar_t"],
                SOUND_TEXT.get(s["key"], "ROAR!"))
    badge(frame, 160, 90, f"{s['num']}/12")
    if t >= s["label_t"] - 0.6:
        rt(frame, 960, 100, s["label"], int(130 * ease_back((t - s["label_t"] + 0.6) / 0.35)), start=s["label_t"] - 0.6, t=t, maxw=1500)
    if t >= s["label_t"]:
        plain(frame, 960, 205, s["fact"].split("!")[0] + "!", 44)


def scene_dance(frame, s, t):
    k = s["key"]
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    x, y, rot, sx, sy = 960, GROUND, 0, 1.0, 1.0
    if s["word"] in ("STOMP!", "ROAR!"):
        y -= 50 * abs(math.sin(q * 6))
        sx = sy = 1.0
    elif s["word"] == "STRETCH!":
        sy = 1 + 0.12 * abs(math.sin(q * 2.5))
    elif s["word"] == "FLAP!":
        y -= 150 + 60 * math.sin(q * 5)
        sx = 1 + 0.12 * math.sin(q * 14)
    elif s["word"] == "SWISH!":
        rot = 10 * math.sin(q * 6)
    elif s["word"] == "RUN!":
        x = 960 + 500 * math.sin(q * 1.6)
        y -= 30 * abs(math.sin(q * 12))
    put(frame, "dino", k, x, y, SIZE["big"] if k != "velociraptor" else 480, rot=rot, sx=sx, sy=sy, flip=(s["word"] == "RUN!" and math.cos(q * 1.6) < 0))
    rt(frame, 960, 140, s["word"], int(200 * (1 + 0.06 * math.sin(q * 10)) * ease_back(q / 0.3)))
    if s["word"] == "ROAR!":
        roar_bubble(frame, 1300, 450, t, s["say_t"] + 1.2)
    draw_kids(frame, t, big_hop=True)


def scene_size(frame, s, t):
    q = t - s["t0"]
    xb, xs = (1130, 760) if s["flip"] else (760, 1130)
    if s.get("extra"):
        xs = 1380
    big = put(frame, "dino", s["big"], xb, GROUND, 680 * ease_back(q / 0.5))
    small = put(frame, "dino", s["small"], xs, GROUND, (230 if s["small"] == "compsognathus" else 330) * ease_back((q - 0.3) / 0.5))
    if s.get("extra") and "extra_t" in s and t >= s["extra_t"]:
        put(frame, "item", "building", xb + 300, GROUND, 600 * ease_back((t - s["extra_t"]) / 0.5))
    if t >= s["answer_t"]:
        qa = t - s["answer_t"]
        rt(frame, xb, GROUND - big.height - 60 - 20 * abs(math.sin(qa * 5)), "BIG!", int(120 * ease_back(qa / 0.3)))
        rt(frame, xs, GROUND - small.height - 50, "small", int(70 * ease_back(qa / 0.3)), colour=(255, 255, 255))
    else:
        rt(frame, 960, 110, "WHICH IS BIGGER?", int(110 * ease_back(q / 0.35)))


def scene_eat(frame, s, t):
    q = t - s["t0"]
    for name, x, label in (("leaves", 640, "PLANTS"), ("meat", 1280, "MEAT")):
        put(frame, "item", name, x, 930, 220)
        rt(frame, x, 990, label, 60, colour=(255, 255, 255))
    x, y = 960, 760
    if t >= s["answer_t"]:
        k = ease_io((t - s["answer_t"]) / 0.9)
        tx = 700 if s["plant"] else 1220
        x = 960 + (tx - 960) * k
    put(frame, "dino", s["key"], x, y - 20 * abs(math.sin(q * 4)) - 40, 400 * ease_back(q / 0.4), flip=(t >= s["answer_t"] and s["plant"]))
    if t >= s["answer_t"]:
        rt(frame, 960, 120, "PLANTS!" if s["plant"] else "MEAT!", int(130 * ease_back((t - s["answer_t"]) / 0.3)),
           colour=(76, 175, 80) if s["plant"] else (224, 90, 70))
    else:
        rt(frame, 960, 120, "PLANTS OR MEAT?", int(110 * ease_back(q / 0.35)))


def scene_eatsum(frame, s, t):
    put(frame, "item", "leaves", 640, 760, 300)
    put(frame, "item", "meat", 1280, 760, 280)
    rt(frame, 640, 860, "HERBIVORE", 72)
    rt(frame, 1280, 860, "CARNIVORE", 72)
    put(frame, "dino", "triceratops", 640, 520, 260)
    put(frame, "dino", "trex", 1280, 520, 260)


def scene_egg(frame, s, t):
    q = t - s["t0"]
    if t < s["hatch_t"]:
        wob = 8 * math.sin(t * 20) if t >= s["crack_t"] - 1.5 else 3 * math.sin(t * 3)
        egg = sized("item", "egg", 440 * ease_back(q / 0.4)).copy()
        a = np.array(egg).astype(float)
        col = np.array([int(s["colour"][i:i + 2], 16) for i in (1, 3, 5)], float)
        tint = (a[:, :, 0] > 200) & (a[:, :, 1] > 200) & (a[:, :, 2] > 180)
        a[tint, :3] = a[tint, :3] * 0.55 + col * 0.45
        egg = Image.fromarray(a.astype(np.uint8)).rotate(wob, resample=Image.BICUBIC, expand=True)
        frame.alpha_composite(egg, (int(960 - egg.width / 2), int(GROUND - egg.height)))
        if t >= s["crack_t"]:
            d = ImageDraw.Draw(frame)
            d.line([(860, 760), (920, 730), (970, 780), (1030, 735), (1070, 770)], fill=INK, width=8)
        rt(frame, 960, 110, "WHO WILL HATCH?", int(110 * ease_back(q / 0.35)))
    else:
        h = t - s["hatch_t"]
        put(frame, "item", "egg_bottom", 960, GROUND, 440)
        put(frame, "item", "egg_top", 960 - 260 * min(1, h / 0.6), GROUND - 260 - 300 * math.sin(min(1, h / 0.6) * math.pi / 1.2), 320, rot=-h * 200, bottom=False)
        put(frame, "dino", s["key"], 960, GROUND - 180, 330 * ease_back(h / 0.4), rot=8 * math.sin(t * 7))
        rt(frame, 960, 110, "BABY " + s["key"].upper().replace("TREX", "T-REX") + "!", int(110 * ease_back(h / 0.3)), maxw=1500)


def scene_foot(frame, s, t):
    q = t - s["t0"]
    for i, (x, y, r) in enumerate(((560, 880, -20), (960, 800, 10), (1360, 880, -15))):
        if q > i * 0.3:
            put(frame, "item", "footprint", x, y, 300 * ease_back((q - i * 0.3) / 0.3), rot=r, bottom=False)
    for i, ct in enumerate(s["count_t"]):
        if t >= ct:
            R.badge(frame, 960 + (i - 1) * 75, 640 - (60 if i == 1 else 0), i + 1, t - ct)
    if t >= s["reveal_t"]:
        h = t - s["reveal_t"]
        put(frame, "dino", "trex", 960, 700, 420 * ease_back(h / 0.4))
        roar_bubble(frame, 1300, 330, t, s["reveal_t"])
        rt(frame, 960, 110, "T-REX!", int(140 * ease_back(h / 0.3)))
    else:
        rt(frame, 960, 110, "WHOSE FOOTPRINT?", int(110 * ease_back(q / 0.35)))


def scene_dig(frame, s, t):
    fx, fy, fw = 960, 760, 760
    fossil = sized("item", "fossil", fw)
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    lay.alpha_composite(fossil, (int(fx - fossil.width / 2), int(fy - fossil.height / 2)))
    k = min(1, max(0, (t - s["brush_t"]) / max(0.5, s["reveal_t"] - s["brush_t"])))
    mask = Image.new("L", frame.size, 0)
    md = ImageDraw.Draw(mask)
    r = 40 + 520 * k
    md.ellipse((fx - r * 1.2, fy - r * 0.7, fx + r * 1.2, fy + r * 0.7), fill=255)
    sand = Image.new("RGBA", frame.size, (221, 184, 114, 255))
    reveal = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    reveal.paste(lay, (0, 0), mask)
    sand.alpha_composite(reveal)
    region = (int(fx - fossil.width / 2) - 30, int(fy - fossil.height / 2) - 30, int(fx + fossil.width / 2) + 30, int(fy + fossil.height / 2) + 30)
    frame.paste(sand.crop(region), region[:2])
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle(region, radius=30, outline=(150, 110, 60), width=10)
    if t < s["reveal_t"] + 0.5:
        bx = fx + 300 * math.sin((t - s["brush_t"]) * 5)
        put(frame, "item", "brush", bx, fy - 60, 230, rot=20 * math.sin(t * 10), bottom=False)
    if t >= s["reveal_t"]:
        confetti(frame, t, s["reveal_t"]) if t < s["reveal_t"] + 2.5 else None
        rt(frame, 960, 110, "FOSSIL!", int(140 * ease_back((t - s["reveal_t"]) / 0.3)))
    else:
        rt(frame, 960, 110, "BRUSH, BRUSH!", int(110 * ease_back((t - s["t0"]) / 0.35)))
    if t >= s["word_t"]:
        plain(frame, 960, 250, "PALEONTOLOGIST = fossil digger", 52)


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 130, s["q"], int(90 * ease_back(q / 0.35)), maxw=1500)
    if t >= s["answer_t"]:
        h = t - s["answer_t"]
        if s["key"] == "fossil":
            put(frame, "item", "fossil", 960, 640, 520 * ease_back(h / 0.4), bottom=False)
        else:
            put(frame, "dino", s["key"], 960, GROUND, (300 if s["key"] == "compsognathus" else 560) * ease_back(h / 0.4))
    else:
        rt(frame, 960, 600, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))


def scene_outro(frame, s, t):
    q = t - s["t0"]
    keys = list(G["dino"].keys())
    for i, k in enumerate(keys):
        x = ((q * 260 + i * 220) % 2900) - 400
        put(frame, "dino", k, x, GROUND - 20 * abs(math.sin(t * 6 + i)), 230)
    rt(frame, 960, 200, "BYE BYE!" if t >= s["bye_t"] else "ROAR!", int(180 * ease_back((t - (s["bye_t"] if t >= s["bye_t"] else s["t0"])) / 0.35)))
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rt(frame, 960, 420, s["title"], int(150 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)


def scene_sound(frame, s, t):
    q = t - s["t0"]
    if t < s["reveal_t"]:
        d = ImageDraw.Draw(frame)
        cx, cy = 960, 560
        d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=(255, 255, 255), outline=INK, width=8)
        d.polygon([(cx - 70, cy - 40), (cx - 20, cy - 40), (cx + 40, cy - 95), (cx + 40, cy + 95), (cx - 20, cy + 40), (cx - 70, cy + 40)], fill=(255, 107, 139), outline=INK)
        if t >= s["sound_t"]:
            for j in range(3):
                r = 180 + j * 60 + 30 * ((t * 2) % 1)
                d.arc((cx - r, cy - r, cx + r, cy + r), -40, 40, fill=(255, 255, 255), width=10)
        rt(frame, 960, 130, "WHO'S THAT SOUND?", int(110 * ease_back(q / 0.35)))
    else:
        h = t - s["reveal_t"]
        put(frame, "dino", s["key"], 960, GROUND, (280 if s["key"] == "compsognathus" else 560) * ease_back(h / 0.4))
        rt(frame, 960, 130, s["key"].upper().replace("TREX", "T-REX") + "!", int(120 * ease_back(h / 0.3)), maxw=1500)


def scene_countd(frame, s, t):
    q = t - s["t0"]
    n = s["n"]
    size = 300 if s["key"] != "compsognathus" else 200
    for i in range(n):
        x = 960 + (i - (n - 1) / 2) * (size * 0.85)
        y = GROUND - (50 if i % 2 else 0)
        put(frame, "dino", s["key"], x, y - 12 * abs(math.sin(t * 4 + i)), size * ease_back((q - i * 0.12) / 0.4))
        if i < len(s["count_t"]) and t >= s["count_t"][i]:
            R.badge(frame, x, y - size * 0.9, i + 1, t - s["count_t"][i])
    if t >= s["answer_t"]:
        rt(frame, 960, 130, str(n), int(220 * ease_back((t - s["answer_t"]) / 0.3)), colour=RAINBOW[n % 6])
    else:
        rt(frame, 960, 130, "HOW MANY?", int(120 * ease_back(q / 0.35)))


FACT_VIS = {"bird": ("dinochick", None)}


def scene_fact(frame, s, t):
    q = t - s["t0"]
    badge(frame, 160, 90, f"FACT {s['num']}")
    v = s["vis"]
    if v == "bird":
        put(frame, "dino", "trex", 760, GROUND, 520 * ease_back(q / 0.4))
        chick = Image.open(ROOT / "long01-animals-fun" / "art" / "fruit_chick.png").convert("RGBA")
        chick = chick.crop(chick.getbbox())
        k = 200 / max(chick.size) * ease_back((q - 0.3) / 0.4)
        if k > 0.02:
            chick = chick.resize((int(chick.width * k), int(chick.height * k)), Image.LANCZOS)
            frame.alpha_composite(chick, (int(1180 - chick.width / 2), int(GROUND - chick.height)))
    elif v in ("volcano", "egg"):
        put(frame, "item", v, 960, GROUND, 520 * ease_back(q / 0.4), rot=4 * math.sin(t * 3) if v == "egg" else 0)
    else:
        put(frame, "dino", v, 960, GROUND, 600 * ease_back(q / 0.4))
    if t >= s["say_t"]:
        txt = next(e["text"] for e in G["lines"] if abs(e["t"] - s["say_t"]) < 0.01)
        plain(frame, 960, 150, txt, 50)


def scene_abc(frame, s, t):
    q = t - s["t0"]
    rt(frame, 620, 520, s["letter"], int(380 * ease_back(q / 0.35)), colour=RAINBOW["ABDPST".index(s["letter"]) % 6])
    put(frame, "dino", s["key"], 1230, GROUND, 520 * ease_back((q - 0.2) / 0.4), rot=3 * math.sin(t * 3))
    if t >= s["say_t"]:
        rt(frame, 960, 130, s["key"].upper().replace("TREX", "T-REX"), int(110 * ease_back((t - s["say_t"]) / 0.3)), maxw=1500)


SCENES = {"abc": scene_abc, "sound": scene_sound, "countd": scene_countd, "fact": scene_fact, "intro": scene_intro, "dino": scene_dino, "dance": scene_dance, "size": scene_size, "eat": scene_eat, "eatsum": scene_eatsum,
          "egg": scene_egg, "foot": scene_foot, "dig": scene_dig, "quiz": scene_quiz, "outro": scene_outro, "title": scene_title}
NO_KIDS = {"intro", "dance"}


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SCENES[sc["kind"]](frame, sc, t)
    R.stars_burst(frame, t) if hasattr(R, "stars_burst") and "stars" in R.G else None
    if sc["kind"] not in NO_KIDS:
        draw_kids(frame, t)
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
    dst = OUT / f"Dinosaurs for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
