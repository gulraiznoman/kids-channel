"""Animate Long video 13 "Wild Animals Safari" (1920x1080) from timeline.json.

python render.py frames 100,900,...  -> preview contact sheet _sheet.png
python render.py video               -> VIDEOS/L13 Wild Animals/Wild Animals for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L13 Wild Animals"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "bluetee", "misheal": "yellow"}
VOC = {"gul": "gul", "misheal": "mishu"}
L1, L9, L10, A13 = ROOT / "long01-animals-fun/art", ROOT / "long09-eggs/art", ROOT / "long10-abc/art", HERE / "art"
ART = {"elephant": L1 / "fruit_elephant.png", "monkey": L1 / "fruit_monkey.png", "zebra": L10 / "item_zebra.png", "snake": L9 / "item_snake.png",
       "owl": L9 / "item_owl.png", "penguin": L9 / "item_penguin.png", "crocodile": L9 / "item_crocodile.png", "cub": L1 / "fruit_cub.png",
       "meat": ROOT / "long06-dinosaurs/art/item_meat.png", "leaves": ROOT / "long06-dinosaurs/art/item_leaves.png",
       "banana": ROOT / "ep01-fruits/art/fruit_banana.png", "fish": L1 / "fruit_fish.png"}
for k in ("lion", "giraffe", "tiger", "hippo", "rhino", "gorilla", "kangaroo", "panda", "bear", "parrot", "flamingo", "cheetah", "camel", "koala", "wolf"):
    ART[k] = A13 / f"item_{k}.png"
BGS = {"savanna": L9 / "bg_savanna.png", "jungle": L9 / "bg_jungle.png", "ice": L9 / "bg_ice.png", "pond": L9 / "bg_pond.png",
       "desert": A13 / "bg_desert.png", "forest": A13 / "bg_forest.png", "outback": A13 / "bg_outback.png"}
BIG = {"elephant": 600, "giraffe": 640, "hippo": 560, "rhino": 560, "camel": 580, "bear": 540, "gorilla": 520}
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["item"] = {k: Image.open(p).convert("RGBA") for k, p in ART.items()}
    G["bg"] = {k: Image.open(p).convert("RGBA") for k, p in BGS.items()}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"] = {}, {}
    rng = np.random.default_rng(13)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]


def dur(t0):
    return G["dur"].get(round(t0, 3), 1.5)


def talking(n, t):
    env = G["env"][n]
    return env[min(int(t * FPS), len(env) - 1)]


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


def side_kids(frame, t, emo=None, xs=(160, 1760), scale=0.3, feet=1075):
    for n, x in zip(("gul", "misheal"), xs):
        body(frame, n, t, emo, x, feet=feet, scale=scale, hop=4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0))))


def item(frame, key, cx, cy, size, rot=0.0, flip=False):
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
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def standing(frame, key, cx, ground, size, t, walk=0.0):
    """animal standing on the ground (bottom anchored), gentle bob; walk>0 adds a stepping bounce"""
    im = G["item"][key]
    bb = im.getbbox()
    asp = (bb[3] - bb[1]) / (bb[2] - bb[0])
    hgt = size * min(1.0, asp) if asp < 1 else size
    bob = (14 * abs(math.sin(t * 8)) if walk > 0 else 4 * math.sin(t * 2))
    item(frame, key, cx, ground - hgt / 2 - bob, size, rot=(3 * math.sin(t * 8) if walk > 0 else 0))


def jeep(frame, t, x, ground=1010, scale=1.0, moving=False):
    k = scale
    for n, dx in (("gul", -60), ("misheal", 70)):
        body(frame, n, t, "happy" if moving else None, x + dx * k, feet=ground - 70 * k, scale=0.28 * k, wave=True,
             hop=6 * abs(math.sin(t * 9)) * k if moving else 0)
    d = ImageDraw.Draw(frame)
    lw = max(4, int(7 * k))
    d.rounded_rectangle((x - 230 * k, ground - 230 * k, x + 230 * k, ground - 70 * k), radius=int(30 * k), fill=(110, 170, 70), outline=INK, width=lw)
    d.rectangle((x - 230 * k, ground - 170 * k, x + 230 * k, ground - 150 * k), fill=(90, 140, 55))
    d.line((x + 150 * k, ground - 230 * k, x + 120 * k, ground - 330 * k), fill=INK, width=lw)
    d.rounded_rectangle((x + 230 * k, ground - 200 * k, x + 290 * k, ground - 110 * k), radius=int(18 * k), fill=(60, 60, 70), outline=INK, width=lw)
    for wx in (x - 140 * k, x + 140 * k):
        r = 55 * k
        d.ellipse((wx - r, ground - 70 * k - r, wx + r, ground - 70 * k + r), fill=(43, 43, 51), outline=INK, width=lw)
        a = t * 10 if moving else 0
        d.ellipse((wx - r * 0.45, ground - 70 * k - r * 0.45, wx + r * 0.45, ground - 70 * k + r * 0.45), fill=(200, 204, 214))
        d.line((wx, ground - 70 * k, wx + r * 0.4 * math.cos(a), ground - 70 * k + r * 0.4 * math.sin(a)), fill=(110, 115, 128), width=lw)


def waves(frame, cx, cy, t, t0, dur_=1.4):
    q = t - t0
    if not 0 <= q < dur_:
        return
    d = ImageDraw.Draw(frame, "RGBA")
    for j in range(3):
        r = 120 + 90 * j + 120 * (q % 0.7)
        d.arc((cx - r, cy - r, cx + r, cy + r), -50, 50, fill=(255, 255, 255, 210), width=10)
        d.arc((cx - r, cy - r, cx + r, cy + r), 130, 230, fill=(255, 255, 255, 210), width=10)


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


def badge(frame, x, y, text, col=(255, 159, 28)):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=col)


def word(frame, text, t, t0, y=120, size=130, col=None, maxw=1500, x=960):
    rt(frame, x, y, text, int(size * ease_back((t - t0) / 0.3)), colour=col, maxw=maxw)


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    q = t - s["roar_t"]
    shake = 16 * math.sin(t * 60) * max(0, 1 - q / 0.8) if 0 <= q < 0.8 else 0
    if t >= s["title_t"]:
        x, _ = 420, 0
        jeep(frame, t, 420, moving=False)
        standing(frame, "lion", 1300, 1000, 560, t)
        k = t - s["title_t"]
        rt(frame, 960, 180, "WILD ANIMALS!", int(210 * ease_back(k / 0.35)), maxw=1600)
        if k < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k / 0.3)))))
    else:
        k = min(1, max(0, q / 0.5))
        x = 2300 - (2300 - 960) * ease_io(k)
        y = 1000 - 300 * math.sin(math.pi * k) if k < 1 else 1000
        standing(frame, "lion", x + shake, y, 780, t)
        if q >= 0.4:
            rt(frame, 960, 200, "ROAR!", int(240 * ease_back((q - 0.4) / 0.25)), colour=(255, 159, 28), maxw=1200)


def scene_habitat(frame, s, t):
    q = t - s["t0"]
    x = -400 + (960 + 400) * ease_io(min(1, q / 1.4))
    jeep(frame, t, x, moving=q < 1.4)
    rt(frame, 960, 220, s["title"], int(170 * ease_back(q / 0.4)), maxw=1500)


def scene_animal(frame, s, t):
    key = s["key"]
    q = t - s["t0"]
    jeep(frame, t, 420, scale=0.85)
    k = min(1, q / 0.8)
    x = 2200 - (2200 - 1300) * ease_io(k)
    size = BIG.get(key, 480)
    if key in ("parrot", "owl"):
        item(frame, key, x, 520 + 15 * math.sin(t * 3), size * 0.8)
    else:
        standing(frame, key, x, 1000, size, t, walk=1.0 if k < 1 else 0)
    waves(frame, 1300, 600, t, s["snd_t"])
    badge(frame, 160, 90, f"{s['num']}/22")
    if t >= s["name_t"]:
        word(frame, s["name"].upper() + "!", t, s["name_t"], size=140, col=(255, 159, 28))


def scene_allanimals(frame, s, t):
    keys = ["lion", "elephant", "giraffe", "zebra", "tiger", "monkey", "panda", "kangaroo", "penguin", "flamingo", "camel", "koala"]
    for i, k in enumerate(keys):
        x = 180 + (i % 6) * 310
        y = 420 + (i // 6) * 360 - 15 * abs(math.sin(t * 4 + i))
        item(frame, k, x, y, 240)
    confetti(frame, t, s["t0"])
    word(frame, "22 WILD ANIMALS!", t, s["t0"], size=130)


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    for j, key in enumerate(("lion", "elephant", "giraffe", "monkey", "panda")):
        ang = j / 5 * 2 * math.pi + t * 0.5
        item(frame, key, 960 + 600 * math.cos(ang), 520 + 230 * math.sin(ang), 190 * ease_back((k - j * 0.06) / 0.4))
    rt(frame, 960, 420, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.32)


def card_row(frame, t, keys, good=None, t_ans=None):
    d = ImageDraw.Draw(frame, "RGBA")
    for i, key in enumerate(keys):
        x = 420 + i * 540
        ok = t_ans is not None and t >= t_ans and key == good
        dim = t_ans is not None and t >= t_ans and key != good
        d.rounded_rectangle((x - 230, 330, x + 230, 800), radius=30, fill=(255, 255, 255, 110 if dim else 210), outline=(59, 193, 74) if ok else INK, width=14 if ok else 6)
        item(frame, key, x, 570 - (25 * abs(math.sin((t - t_ans) * 6)) if ok else 0), 380)
        if ok:
            stars_ring(frame, x, 570, 260, 260, t, n=8, r=18)


def scene_record(frame, s, t):
    card_row(frame, t, s["opts"], s["ans"], s["answer_t"])
    if t >= s["answer_t"]:
        word(frame, s["ans"].upper() + "!", t, s["answer_t"], size=130, col=(59, 193, 74))
    else:
        word(frame, "WHICH ONE?", t, s["t0"], size=120)
    side_kids(frame, t, scale=0.26, xs=(110, 1810))


def scene_sound(frame, s, t):
    side_kids(frame, t, xs=(190, 1730))
    if t < s["answer_t"]:
        waves(frame, 960, 520, t, s["snd_t"], 1.6)
        rt(frame, 960, 520, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], size=130)
    else:
        k = ease_back((t - s["answer_t"]) / 0.4)
        item(frame, s["key"], 960, 560, 460 * max(0.1, k))
        word(frame, s["key"].upper() + "!", t, s["answer_t"], size=140, col=(255, 159, 28))


def scene_home(frame, s, t):
    q = t - s["t0"]
    item(frame, s["key"], 960, 330 + 10 * math.sin(t * 3), 320 * ease_back(q / 0.4))
    d = ImageDraw.Draw(frame)
    for i, h in enumerate(s["opts"]):
        x = 480 + i * 480
        k = ease_back((q - 0.2 - i * 0.12) / 0.4)
        if k <= 0.02:
            continue
        w, hh = int(400 * k), int(225 * k)
        thumb = G["bg"][h].resize((w, hh), Image.BILINEAR)
        good = t >= s["answer_t"] and h == s["home"]
        if t >= s["answer_t"] and not good:
            thumb = Image.blend(thumb, Image.new("RGBA", thumb.size, (255, 255, 255, 255)), 0.6)
        frame.alpha_composite(thumb, (int(x - w / 2), int(800 - hh / 2)))
        d.rounded_rectangle((x - w / 2, 800 - hh / 2, x + w / 2, 800 + hh / 2), radius=16, outline=(59, 193, 74) if good else INK, width=16 if good else 6)
        if good:
            stars_ring(frame, x, 800, 260, 160, t, n=8, r=18)
    word(frame, "WHERE DO I LIVE?" if t < s["answer_t"] else s["home"].upper() + "!", t, s["t0"] if t < s["answer_t"] else s["answer_t"], size=110,
         col=None if t < s["answer_t"] else (59, 193, 74))


def scene_baby(frame, s, t):
    standing(frame, s["key"], 640, 960, 520, t)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        if s["key"] == "lion":
            item(frame, "cub", 1300, 760, 300 * k)
        else:
            standing(frame, s["key"], 1300, 960, 260 * k, t, walk=1.0)
        rt(frame, 1300, 480, s["baby"].upper() + "!", int(120 * k), colour=(255, 107, 139), maxw=600)
        stars_ring(frame, 1300, 760, 220, 160, t, n=8, r=18)
    else:
        rt(frame, 1300, 700, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
    word(frame, "BABY ANIMALS!", t, s["t0"], size=120, col=(255, 107, 139))


def scene_count(frame, s, t):
    n = sum(1 for c in s["cts"] if t >= c)
    for i in range(n):
        tx = 160 + (i % 5) * 400
        gy = 640 if i < 5 else 1020
        q = min(1, (t - s["cts"][i]) / 0.5)
        x = 2200 - (2200 - tx) * ease_io(q)
        standing(frame, "zebra", x, gy, 280, t, walk=1.0 if q < 1 else 0)
        if q >= 1:
            rt(frame, tx, gy - 290, str(i + 1), 70, colour=RAINBOW[i % 6])
    word(frame, f"{n} ZEBRAS!" if n else "COUNT THE ZEBRAS!", t, s["cts"][n - 1] if n else s["t0"], size=110)


def scene_dance(frame, s, t):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv = s["move"]
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, dx = 0, 0, 0
        if mv == "stomp":
            hop = 30 * abs(math.sin(q * 6 + i))
        elif mv == "jump":
            hop = 100 * abs(math.sin(q * 5 + i))
        elif mv == "swing":
            rot = 12 * math.sin(q * 5 + i)
        elif mv == "stretch":
            hop = 40 + 20 * math.sin(q * 3)
        elif mv == "roar":
            dx = 10 * math.sin(q * 30) if (q % 1.5) < 0.5 else 0
        elif mv == "waddle":
            rot = 10 * math.sin(q * 8)
            dx = 20 * math.sin(q * 4)
        body(frame, n, t, "excited" if mv in ("roar", "jump") else "happy", x + dx, scale=0.55, hop=hop, rot=rot, wave=True)
    pic = {"stomp": "elephant", "jump": "kangaroo", "swing": "monkey", "stretch": "giraffe", "roar": "lion", "waddle": "penguin"}[mv]
    item(frame, pic, 960, 470, 260)
    word(frame, s["word"], t, s["t0"], size=110)


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
    keys = ["lion", "elephant", "giraffe", "zebra", "monkey", "panda", "kangaroo", "penguin"]
    for i, k in enumerate(keys):
        x = (i * 260 + t * 130) % 2300 - 190
        standing(frame, k, x, 1050, 230, t, walk=1.0)
    jeep(frame, t, 960, ground=840, scale=0.9)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 140, "FAVOURITE ANIMAL?", int(120 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


def bamboo(frame, cx, cy, size):
    d = ImageDraw.Draw(frame)
    for j in range(3):
        x = cx - size * 0.25 + j * size * 0.25
        d.rounded_rectangle((x - size * 0.07, cy - size * 0.45, x + size * 0.07, cy + size * 0.45), radius=int(size * 0.05), fill=(126, 200, 80), outline=INK, width=5)
        for k in range(3):
            y = cy - size * 0.3 + k * size * 0.3
            d.line((x - size * 0.07, y, x + size * 0.07, y), fill=INK, width=5)
        d.ellipse((x + size * 0.05, cy - size * 0.4, x + size * 0.25, cy - size * 0.3), fill=(93, 187, 70), outline=INK, width=3)


def food(frame, key, cx, cy, size):
    if key == "bamboo":
        bamboo(frame, cx, cy, size)
    else:
        item(frame, key, cx, cy, size)


def scene_eat(frame, s, t):
    q = t - s["t0"]
    standing(frame, s["key"], 480, 760, 380, t)
    d = ImageDraw.Draw(frame, "RGBA")
    for i, f in enumerate(s["opts"]):
        x, y = 1020 + i * 280, 520
        good = t >= s["answer_t"] and f == s["food"]
        dim = t >= s["answer_t"] and not good
        d.rounded_rectangle((x - 120, y - 130, x + 120, y + 130), radius=30, fill=(255, 255, 255, 110 if dim else 220),
                            outline=(59, 193, 74) if good else INK, width=12 if good else 6)
        if good:
            k = min(1, (t - s["answer_t"]) / 0.6)
            food(frame, f, x + (560 - x) * k, y + (640 - y) * k, 180 - 60 * k)
        else:
            food(frame, f, x, y, 180 * ease_back((q - 0.2 - i * 0.1) / 0.35) + 1)
    word(frame, s["food"].upper() + "!" if t >= s["answer_t"] else "WHAT DO I EAT?", t, s["answer_t"] if t >= s["answer_t"] else s["t0"], size=120,
         col=(59, 193, 74) if t >= s["answer_t"] else None)
    side_kids(frame, t, xs=(110, 1810), scale=0.24)


def bush(frame, cx, cy, sc=1.0):
    d = ImageDraw.Draw(frame)
    for dx, dy, r in ((-230, 40, 170), (230, 40, 170), (0, 70, 210), (-120, -60, 160), (120, -60, 160), (0, -120, 150)):
        d.ellipse((cx + dx * sc - r * sc, cy + dy * sc - r * sc, cx + dx * sc + r * sc, cy + dy * sc + r * sc), fill=(76, 175, 80), outline=INK, width=6)
    for j in range(10):
        x = cx + (j - 4.5) * 80 * sc
        d.ellipse((x - 14, cy + 10 * math.sin(j) - 14, x + 14, cy + 10 * math.sin(j) + 14), fill=(255, 107, 139))


def scene_hide(frame, s, t):
    key = s["key"]
    rev = t >= s["reveal_t"]
    k = min(1, (t - s["reveal_t"]) / 0.5) if rev else 0
    peek = 40 * math.sin(t * 3)
    standing(frame, key, 960 + 200 + peek * (0 if rev else 1), 980, BIG.get(key, 480) * 0.9, t)
    if k < 1:
        bush(frame, 960 - 900 * ease_io(k), 820)
    if rev:
        word(frame, key.upper() + "!", t, s["reveal_t"], size=140, col=(255, 159, 28))
        stars_ring(frame, 1160, 700, 320, 260, t, n=8, r=18)
    else:
        word(frame, "WHO'S HIDING?", t, s["t0"], size=120)
        rt(frame, 960, 330, "?", int(140 + 12 * math.sin(t * 6)), colour=(255, 255, 255))
    side_kids(frame, t, xs=(110, 1810), scale=0.24)


def pattern_card(frame, x, y, pat, good, dim):
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((x - 230, y - 160, x + 230, y + 160), radius=30, fill=(255, 236, 190, 120 if dim else 255),
                        outline=(59, 193, 74) if good else INK, width=14 if good else 6)
    if pat == "stripes":
        for j in range(6):
            xx = x - 170 + j * 68
            d.line((xx, y - 110, xx + 30, y + 110), fill=(43, 43, 51, 120 if dim else 255), width=22)
    else:
        for j in range(12):
            xx = x - 170 + (j % 4) * 110 + (35 if (j // 4) % 2 else 0)
            yy = y - 100 + (j // 4) * 100
            d.ellipse((xx - 24, yy - 20, xx + 24, yy + 20), fill=(110, 70, 40, 120 if dim else 255))
    rt(frame, x, y + 210, pat.upper(), 70, colour=(59, 193, 74) if good else (255, 255, 255))


def scene_pattern(frame, s, t):
    rev = t >= s["answer_t"]
    for j, pat in enumerate(("spots", "stripes")):
        x = 560 + j * 800
        good = rev and pat == s["pat"]
        pattern_card(frame, x, 500, pat, good, rev and not good)
    if rev:
        k = min(1, (t - s["answer_t"]) / 0.6)
        tx = 560 if s["pat"] == "spots" else 1360
        item(frame, s["key"], 960 + (tx - 960) * k, 500 - 220 * math.sin(math.pi * k) * (1 - k) - 20 * k, 300)
        word(frame, s["pat"].upper() + "!", t, s["answer_t"], size=140, col=(59, 193, 74))
    else:
        item(frame, s["key"], 960, 560 + 10 * math.sin(t * 3), 320)
        word(frame, "SPOTS OR STRIPES?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(110, 1810), scale=0.24)


SCENES = {"intro": scene_intro, "habitat": scene_habitat, "animal": scene_animal, "allanimals": scene_allanimals, "title": scene_title,
          "record": scene_record, "sound": scene_sound, "home": scene_home, "baby": scene_baby, "count": scene_count, "dance": scene_dance,
          "quiz": scene_quiz, "outro": scene_outro, "eat": scene_eat, "hide": scene_hide, "pattern": scene_pattern}


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
    dst = OUT / f"Wild Animals for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=0", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
