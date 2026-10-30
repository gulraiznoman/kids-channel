"""Animate Long video 10 "ABC Phonics" (1920x1080) from timeline.json.

python render.py frames 100,900,...  -> preview contact sheet _sheet.png
python render.py video               -> VIDEOS/L10 ABC Phonics/ABC Phonics for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L10 ABC Phonics"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "bluetee", "misheal": "kurta"}
VOC = {"gul": "gul", "misheal": "mishu"}
E1, L1, L3, L4, L5, L6, L7, L8, L9 = (ROOT / "ep01-fruits/art", ROOT / "long01-animals-fun/art", ROOT / "long03-fruits-veg/art", ROOT / "long04-good-habits/art",
                                      ROOT / "long05-body-parts/art", ROOT / "long06-dinosaurs/art", ROOT / "long07-feelings/art", ROOT / "long08-colors-shapes/art", ROOT / "long09-eggs/art")
ART = {"apple": E1 / "fruit_apple.png", "airplane": L1 / "fruit_airplane.png", "ball": L4 / "item_ball.png", "banana": E1 / "fruit_banana.png",
       "cat": L1 / "fruit_kitten.png", "car": L1 / "fruit_car.png", "dog": L1 / "fruit_puppy.png", "dinosaur": L6 / "dino_trex.png",
       "elephant": L1 / "fruit_elephant.png", "egg": L6 / "item_egg.png", "fish": L1 / "fruit_fish.png", "frog": L8 / "item_frog.png",
       "grapes": E1 / "fruit_grapes.png", "gift": L7 / "item_gift.png", "hat": L8 / "item_tophat.png", "hen": L9 / "item_hen.png",
       "ice cream": L5 / "item_icecream.png", "jellyfish": L1 / "fruit_jellyfish.png", "kite": L8 / "item_kite.png", "kiwi": E1 / "fruit_kiwi.png",
       "lion": L1 / "fruit_cub.png", "lemon": E1 / "fruit_lemon.png", "monkey": L1 / "fruit_monkey.png", "moon": L4 / "item_moon.png",
       "nest": L9 / "item_nest.png", "nose": L5 / "item_nose.png", "octopus": L1 / "fruit_octopus.png", "ostrich": L9 / "item_ostrich.png",
       "penguin": L9 / "item_penguin.png", "pizza": L8 / "item_pizza.png", "queen": HERE / "art/item_queen.png", "rainbow": L1 / "fruit_rainbow.png",
       "robin": L9 / "item_robin.png", "sun": L1 / "fruit_sunny.png", "snake": L9 / "item_snake.png", "turtle": L9 / "item_turtle.png",
       "train": L1 / "fruit_train.png", "umbrella": L4 / "item_umbrella.png", "violin": HERE / "art/item_violin.png", "whale": L1 / "fruit_whale.png",
       "watermelon": E1 / "fruit_watermelon.png", "xylophone": HERE / "art/item_xylophone.png", "box": L4 / "item_toybox.png",
       "yo-yo": HERE / "art/item_yoyo.png", "zebra": HERE / "art/item_zebra.png",
       "hen": L9 / "item_hen.png", "sun": L1 / "fruit_sunny.png", "bus": L1 / "fruit_bus.png"}
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WORD1 = dict(zip(ABC, ["apple", "ball", "cat", "dog", "elephant", "fish", "grapes", "hat", "ice cream", "jellyfish", "kite", "lion", "monkey",
                       "nest", "octopus", "penguin", "queen", "rainbow", "sun", "turtle", "umbrella", "violin", "whale", "xylophone", "yo-yo", "zebra"]))
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


def lcol(L):
    return RAINBOW[ABC.index(L) % 6] if L in ABC else RAINBOW[0]


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["item"] = {k: Image.open(p).convert("RGBA") for k, p in ART.items()}
    G["bg"] = {"abcpark": Image.open(HERE / "art/bg_abcpark.png").convert("RGBA"), "board": Image.open(L8 / "bg_board.png").convert("RGBA")}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"] = {}, {}
    rng = np.random.default_rng(10)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]
    G["drops"] = [(rng.uniform(80, W - 80), rng.uniform(0, 1.2), rng.uniform(80, 150)) for _ in range(26)]


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


def item(frame, key, cx, cy, size, rot=0.0):
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
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


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


def tile(frame, ch, cx, cy, size, col, bg=(255, 255, 255), outline=INK):
    d = ImageDraw.Draw(frame)
    h = size / 2
    d.rounded_rectangle((cx - h, cy - h, cx + h, cy + h), radius=int(size * 0.18), fill=bg, outline=outline, width=max(4, int(size * 0.05)))
    rt(frame, cx, cy + size * 0.04, ch, int(size * 0.72), colour=col, maxw=int(size * 0.9))


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    q = t - s["rain_t"]
    burst = t - s["title_t"]
    for i, L in enumerate(ABC):
        row, col = divmod(i, 13)
        tx, ty = 200 + col * 127, 560 + row * 170                # neat A-M / N-Z rows
        k = q - i * 0.05
        if k < 0:
            continue
        if burst < 0:
            y = min(ty, -100 + 2600 * k * k)
            if y >= ty:
                y = ty - abs(math.sin((k - 0.25) * 9)) * 40 * max(0, 1 - (k - 0.25) * 1.5)
            rt(frame, tx, y, L, 110, colour=lcol(L))
        elif burst < 0.6:                                         # letters fly away when ABC! slams in
            a = math.atan2(ty - 540, tx - 960)
            f = burst / 0.6
            rt(frame, tx + math.cos(a) * 900 * f, ty + math.sin(a) * 600 * f - 200 * f, L, int(110 * (1 - f)), colour=lcol(L))
    if t >= s["title_t"]:
        k2 = t - s["title_t"]
        for n, x in (("gul", 640), ("misheal", 1280)):
            body(frame, n, t, "excited" if t < s["kids_t"] else None, x, scale=0.46, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
        rt(frame, 960, 190, "A B C!", int(230 * ease_back(k2 / 0.35)), maxw=1500)
        if k2 < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k2 / 0.3)))))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    for j in range(8):
        ang = j / 8 * 2 * math.pi + t * 0.6
        L = ABC[(j * 3) % 26]
        rt(frame, 960 + 600 * math.cos(ang), 450 + 230 * math.sin(ang), L, int(120 * ease_back((k - j * 0.05) / 0.4)), colour=lcol(L))
    rt(frame, 960, 420, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.34)


def scene_letter(frame, s, t):
    L = s["L"]
    c = lcol(L)
    q = t - s["t0"]
    badge(frame, 160, 90, f"{s['num']}/26")
    pulse = 1.0
    if t >= s["snd_t"]:
        pulse += 0.08 * abs(math.sin((t - s["snd_t"]) * 9)) * max(0, 1 - (t - s["snd_t"]) / 1.5)
    sz = int(400 * ease_back(q / 0.35) * pulse)
    rt(frame, 560, 470, L + L.lower(), sz, colour=c, maxw=820)
    if t >= s["w1_t"]:
        k = ease_back((t - s["w1_t"]) / 0.4)
        has2 = bool(s.get("w2")) and "w2_t" in s and t >= s["w2_t"]
        x1 = 1240 if not has2 else 1150 - 60 * min(1, (t - s["w2_t"]) / 0.4)
        item(frame, s["w1"], x1, 470 + 8 * math.sin(t * 2.5), 340 * k)
        rt(frame, x1, 730, s["w1"].upper(), int(70 * k), colour=c, maxw=420)
        if has2:
            k2 = ease_back((t - s["w2_t"]) / 0.4)
            item(frame, s["w2"], 1480, 480 + 8 * math.sin(t * 2.5 + 1), 280 * k2)
            rt(frame, 1480, 730, s["w2"].upper(), int(62 * k2), colour=c, maxw=380)
    if t >= s["snd_t"]:
        snd = next((l["text"].split(",")[0] for l in G["lines"] if abs(l["t"] - s["snd_t"]) < 0.01), "")
        if L != "X":
            rt(frame, 560, 790, snd.upper() + "!", int(90 * ease_back((t - s["snd_t"]) / 0.3)), colour=(255, 255, 255), maxw=500)
    side_kids(frame, t, xs=(150, 1780), scale=0.28)


def scene_allletters(frame, s, t):
    q = t - s["t0"]
    for i, L in enumerate(ABC):
        x = 270 + (i % 13) * 115
        y = 380 + (i // 13) * 200 - 25 * abs(math.sin(t * 5 + i * 0.4))
        tile(frame, L, x, y, 100 * ease_back((q - i * 0.02) / 0.3), lcol(L))
    word(frame, "A TO Z!", t, s["t0"], size=150)
    confetti(frame, t, s["t0"])
    side_kids(frame, t, "excited", xs=(500, 1420), scale=0.36)


def scene_fast(frame, s, t):
    cur = 0
    for i, ts in enumerate(s["ts"]):
        if t >= ts:
            cur = i
    L = ABC[cur]
    k = ease_back((t - s["ts"][cur]) / 0.15)
    tile(frame, L, 720, 480, 380 * k, lcol(L))
    item(frame, WORD1[L], 1240, 480, 300 * k)
    for i in range(cur + 1):
        rt(frame, 160 + i * 61, 900, ABC[i], 70, colour=lcol(ABC[i]))
    word(frame, "SUPER FAST!", t, s["t0"], size=110)


def qbox(frame, cx, cy, size, t):
    d = ImageDraw.Draw(frame)
    pu = 1 + 0.05 * math.sin(t * 7)
    h = size / 2 * pu
    d.rounded_rectangle((cx - h, cy - h, cx + h, cy + h), radius=30, outline=(255, 255, 255), width=10)
    rt(frame, cx, cy, "?", int(size * 0.7), colour=(255, 255, 255))


def scene_first(frame, s, t):
    q = t - s["t0"]
    item(frame, s["word"], 760, 420 + 8 * math.sin(t * 2.5), 340 * ease_back(q / 0.4))
    rt(frame, 760, 650, s["word"].upper(), int(70 * ease_back(q / 0.4)), colour=(255, 255, 255), maxw=500)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.35)
        tile(frame, s["L"], 1230, 430, 300 * k, lcol(s["L"]))
        stars_ring(frame, 1230, 430, 220, 200, t, n=6, r=18)
    else:
        qbox(frame, 1230, 430, 300, t)
    rt(frame, 960, 175, "FIRST LETTER?", int(90 * ease_back(q / 0.35)), colour=(255, 255, 255), maxw=1100)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_match(frame, s, t):
    q = t - s["t0"]
    L = s["L"]
    tile(frame, L, 620, 430, 300 * ease_back(q / 0.35), lcol(L))
    for i, o in enumerate(s["opts"]):
        x = 1040 + i * 210
        k = ease_back((q - 0.2 - i * 0.1) / 0.35)
        good = t >= s["answer_t"] and o == L.lower()
        dim = t >= s["answer_t"] and not good
        tile(frame, o, x, 450 - (30 * abs(math.sin((t - s["answer_t"]) * 6)) if good else 0), 170 * k,
             (200, 200, 200) if dim else lcol(L), bg=(255, 255, 255) if not dim else (235, 235, 235), outline=(59, 193, 74) if good else INK)
    if t >= s["answer_t"]:
        rt(frame, 960, 175, f"BIG {L}, SMALL {L.lower()}!", int(90 * ease_back((t - s["answer_t"]) / 0.3)), colour=(255, 255, 255), maxw=1100)
    else:
        rt(frame, 960, 175, f"FIND THE SMALL {L}!", int(90 * ease_back(q / 0.35)), colour=(255, 255, 255), maxw=1100)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_hunt(frame, s, t):
    q = t - s["t0"]
    for i, ch in enumerate(s["grid"]):
        x = 540 + (i % 4) * 280
        y = 400 + (i // 4) * 260 + 10 * math.sin(t * 3 + i)
        found = t >= s["answer_t"] and ch == s["L"]
        k = ease_back((q - i * 0.05) / 0.3)
        tile(frame, ch, x, y - (30 * abs(math.sin((t - s["answer_t"]) * 6)) if found else 0), 190 * k, lcol(s["L"]) if found else (90, 90, 110),
             outline=(255, 77, 109) if found else INK)
    if t >= s["answer_t"]:
        word(frame, f"{s['grid'].count(s['L'])} {s['L']}s!", t, s["answer_t"], size=140, col=lcol(s["L"]))
    else:
        word(frame, f"FIND THE {s['L']}s!", t, s["t0"], size=120)
    side_kids(frame, t, xs=(160, 1760), scale=0.3)


STROKES = {
    "A": [[(-0.33, 0.45), (0, -0.45), (0.33, 0.45)], [(-0.17, 0.1), (0.17, 0.1)]],
    "B": [[(-0.28, 0.45), (-0.28, -0.45)],
          [(-0.28, -0.45)] + [(0.02 + 0.22 * math.sin(a), -0.225 - 0.225 * math.cos(a)) for a in np.linspace(0, math.pi, 12)] + [(-0.28, 0.0)],
          [(-0.28, 0.0)] + [(0.05 + 0.25 * math.sin(a), 0.225 - 0.225 * math.cos(a)) for a in np.linspace(0, math.pi, 12)] + [(-0.28, 0.45)]],
    "C": [[(0.42 * math.cos(a), 0.45 * math.sin(a)) for a in np.linspace(-0.8, -2 * math.pi + 0.8, 30)]],
    "O": [[(0.38 * math.sin(a), -0.45 * math.cos(a)) for a in np.linspace(0, -2 * math.pi, 40)]],
}


def scene_trace(frame, s, t):
    L = s["L"]
    cx, cy, S = 960, 450, 520
    strokes = [[(cx + x * S, cy + y * S) for x, y in st] for st in STROKES[L]]
    d = ImageDraw.Draw(frame)
    for st in strokes:                                           # dotted guide
        for i in range(len(st) - 1):
            a, b = st[i], st[i + 1]
            n = max(2, int(math.dist(a, b) / 26))
            for j in range(n):
                if j % 2 == 0:
                    x0, y0 = a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n
                    d.ellipse((x0 - 6, y0 - 6, x0 + 6, y0 + 6), fill=(230, 240, 235))
    if "draw_t" in s and t >= s["draw_t"]:
        p = min(1, (t - s["draw_t"]) / 2.8)
        lens = [sum(math.dist(st[i], st[i + 1]) for i in range(len(st) - 1)) for st in strokes]
        left = p * sum(lens)
        head = None
        for st, ln in zip(strokes, lens):
            if left <= 0:
                break
            pts = [st[0]]
            acc = 0
            for i in range(len(st) - 1):
                seg = math.dist(st[i], st[i + 1])
                if acc + seg <= left:
                    pts.append(st[i + 1])
                    acc += seg
                else:
                    k = (left - acc) / seg
                    pts.append((st[i][0] + (st[i + 1][0] - st[i][0]) * k, st[i][1] + (st[i + 1][1] - st[i][1]) * k))
                    acc = left
                    break
            d.line(pts, fill=INK, width=46, joint="curve")
            d.line(pts, fill=lcol(L), width=34, joint="curve")
            head = pts[-1]
            left -= ln
        if head and p < 1:
            R.star(d, head[0], head[1], 34, (255, 230, 60), rot=t * 6)
        if p >= 1:
            stars_ring(frame, cx, cy, 330, 300, t, n=8, r=20)
    rt(frame, 960, 175, f"DRAW {L}!", int(100 * ease_back((t - s["t0"]) / 0.35)), colour=(255, 255, 255), maxw=900)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_body(frame, s, t):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    L = s["L"]
    rt(frame, 960, 520, L, int(760 + 30 * math.sin(q * 5)), colour=lcol(L))
    for i, (n, x) in enumerate((("gul", 640), ("misheal", 1280))):
        hop = 40 * abs(math.sin(q * 5 + i)) if L in ("Y", "X") else 12 * abs(math.sin(q * 4 + i))
        rot = {"C": 10, "O": 0}.get(L, 0) * (1 if i == 0 else -1)
        body(frame, n, t, "excited" if L in ("Y", "X") else "happy", x, scale=0.52, hop=hop, rot=rot, wave=True)
    word(frame, f"{L}!", t, s["t0"], size=130, col=lcol(L))


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 175, s["q"], int(72 * ease_back(q / 0.35)), colour=(255, 255, 255), maxw=1200)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.35)
        v = s["vis"]
        if v in ABC:
            tile(frame, v, 960, 460, 320 * k, lcol(v))
        else:
            rt(frame, 960, 460, v, int(300 * k), colour=RAINBOW[2])
        stars_ring(frame, 960, 460, 280, 220, t, n=8, r=20)
        side_kids(frame, t, "happy", xs=(150, 1770))
    else:
        qbox(frame, 960, 460, 300, t)
        side_kids(frame, t, xs=(150, 1770))


def scene_outro(frame, s, t):
    for i, L in enumerate(ABC):
        x = (i * 120 + t * 160) % 3200 - 150
        rt(frame, x, 1000 - 25 * abs(math.sin(t * 5 + i)), L, 90, colour=lcol(L))
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, scale=0.5, feet=940, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 140, "YOU KNOW YOUR ABC!", int(110 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


def scene_lower(frame, s, t):
    cur = 0
    for i, ts in enumerate(s["ts"]):
        if t >= ts:
            cur = i
    L = ABC[cur]
    k = ease_back((t - s["ts"][cur]) / 0.15)
    tile(frame, L.lower(), 960, 470, 380 * k, lcol(L))
    for i in range(cur + 1):
        rt(frame, 200 + i * 59, 780, ABC[i].lower(), 70, colour=lcol(ABC[i]))
    word(frame, "SMALL LETTER SOUNDS!", t, s["t0"], size=100)
    side_kids(frame, t, xs=(110, 1810), scale=0.24)


def scene_pics(frame, s, t):
    q = t - s["t0"]
    L = s["L"]
    tile(frame, L + L.lower(), 960, 250, 200 * ease_back(q / 0.35), lcol(L))
    for i, p in enumerate(s["pics"]):
        x = 420 + i * 360
        k = ease_back((q - 0.2 - i * 0.1) / 0.35)
        good = p[0].upper() == L
        d = ImageDraw.Draw(frame, "RGBA")
        if t >= s["answer_t"]:
            col = (59, 193, 74, 255) if good else (200, 200, 200, 255)
            d.rounded_rectangle((x - 150, 450, x + 150, 750), radius=30, fill=(255, 255, 255, 200), outline=col, width=14 if good else 6)
        else:
            d.rounded_rectangle((x - 150, 450, x + 150, 750), radius=30, fill=(255, 255, 255, 200), outline=INK, width=6)
        item(frame, p, x, 600 - (25 * abs(math.sin((t - s["answer_t"]) * 6)) if good and t >= s["answer_t"] else 0), 240 * k)
        if t >= s["answer_t"] and good:
            rt(frame, x, 800, p.upper(), 60, colour=lcol(L), maxw=330)
    word(frame, f"STARTS WITH {L}?", t, s["t0"], y=110, size=100)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_spell(frame, s, t):
    letters = s["letters"]
    for i, (ch, st) in enumerate(zip(letters, s["snd_t"])):
        if t < st:
            continue
        hop = 30 * max(0, 1 - (t - st) / 0.4)
        tile(frame, ch, 700 + i * 260, 360 - hop, 220 * ease_back((t - st) / 0.3), lcol(ch))
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        item(frame, s["word"], 960, 610, 230 * k)
        rt(frame, 1290, 610, s["word"].upper() + "!", int(110 * k), colour=(255, 255, 255), maxw=380)
    rt(frame, 960, 175, "SOUND IT OUT!", int(90 * ease_back((t - s["t0"]) / 0.35)), colour=(255, 255, 255), maxw=900)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


SCENES = {"intro": scene_intro, "title": scene_title, "letter": scene_letter, "allletters": scene_allletters, "fast": scene_fast,
          "first": scene_first, "match": scene_match, "hunt": scene_hunt, "trace": scene_trace, "body": scene_body, "quiz": scene_quiz,
          "outro": scene_outro,
          "lower": scene_lower, "pics": scene_pics, "spell": scene_spell}


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
    dst = OUT / f"ABC Phonics for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=0", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
