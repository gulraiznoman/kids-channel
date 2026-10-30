"""Animate Long video 14 "Count 1 to 20" (1920x1080) from timeline.json.

python render.py frames 100,900,...  -> preview contact sheet _sheet.png
python render.py video               -> VIDEOS/L14 Count to 20/Count to 20 for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L14 Count to 20"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "tee", "misheal": "kurta"}
VOC = {"gul": "gul", "misheal": "mishu"}
E1, L1, L4, L5, L8 = ROOT / "ep01-fruits/art", ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art", ROOT / "long05-body-parts/art", ROOT / "long08-colors-shapes/art"
ART = {"apple": E1 / "fruit_apple.png", "star": L1 / "fruit_star.png", "fish": L1 / "fruit_fish.png", "duckling": L1 / "fruit_duckling.png",
       "strawberry": E1 / "fruit_strawberry.png", "ball": L4 / "item_ball.png", "cupcake": L8 / "item_cupcake.png",
       "flower": L5 / "item_flower.png", "heart": L1 / "fruit_heart.png", "shoes": L4 / "item_shoes.png",
       "hand": L5 / "item_hand.png", "foot": L5 / "item_card_foot.png"}
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["item"] = {k: Image.open(p).convert("RGBA") for k, p in ART.items()}
    G["bg"] = {"rainbow": Image.open(L1 / "bg_rainbow.png").convert("RGBA").resize((W, H)),
               "board": Image.open(L8 / "bg_board.png").convert("RGBA"),
               "playroom": Image.open(L5 / "bg_playroom.png").convert("RGBA").resize((W, H)),
               "space": R.bg_space().convert("RGBA")}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"] = {}, {}
    rng = np.random.default_rng(14)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]
    G["drops"] = [(rng.uniform(100, W - 100), rng.uniform(0, 1.0)) for _ in range(20)]


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
    if key == "balloon":
        d = ImageDraw.Draw(frame)
        col = RAINBOW[int(cx * 7 + cy) % 6]
        r = size * 0.4
        d.line((cx, cy + r * 1.2, cx + 6, cy + size * 0.9), fill=INK, width=3)
        d.ellipse((cx - r, cy - r * 1.2, cx + r, cy + r * 1.2), fill=col, outline=INK, width=max(3, int(size / 25)))
        d.ellipse((cx - r * 0.5, cy - r * 0.8, cx - r * 0.15, cy - r * 0.3), fill=(255, 255, 255))
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


def badge(frame, x, y, text, col=(46, 168, 255)):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=col)


def word(frame, text, t, t0, y=120, size=130, col=None, maxw=1500, x=960):
    rt(frame, x, y, text, int(size * ease_back((t - t0) / 0.3)), colour=col, maxw=maxw)


def current(ts, t):
    n = 0
    for i, x in enumerate(ts):
        if t >= x:
            n = i + 1
    return n


def tenframe(frame, cx, cy, n, cell=70, col=(255, 77, 109)):
    """two ten-frames side by side: first fills to 10, second holds the rest"""
    d = ImageDraw.Draw(frame)
    for f in range(2):
        x0 = cx - 5 * cell - 30 + f * (5 * cell + 60) - (5 * cell + 60) / 2 + 5 * cell / 2 + 15
        for i in range(10):
            x = x0 + (i % 5) * cell
            y = cy + (i // 5) * cell
            d.rectangle((x, y, x + cell, y + cell), fill=(255, 255, 255), outline=INK, width=4)
            k = f * 10 + i
            if k < n:
                c = col if f == 0 else (46, 168, 255)
                d.ellipse((x + 10, y + 10, x + cell - 10, y + cell - 10), fill=c, outline=INK, width=3)


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    q = t - s["rain_t"]
    for i in range(20):
        x, delay = G["drops"][i]
        k = q - delay * 0.8
        if k < 0:
            continue
        floor = 880 + (i % 3) * 40
        y = min(floor, -100 + 2400 * k * k)
        if t < s["title_t"] or t < s["title_t"] + 0.5:
            sz = 110 if t < s["title_t"] else int(110 * max(0, 1 - (t - s["title_t"]) / 0.5))
            if sz > 4:
                rt(frame, x, y - 50, str(i + 1), sz, colour=RAINBOW[i % 6])
    if t >= s["title_t"]:
        k2 = t - s["title_t"]
        for n, x in (("gul", 640), ("misheal", 1280)):
            body(frame, n, t, "excited" if t < s["kids_t"] else None, x, scale=0.46, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
        rt(frame, 960, 190, "COUNT TO 20!", int(210 * ease_back(k2 / 0.35)), maxw=1500)
        if k2 < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k2 / 0.3)))))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    for j in range(8):
        ang = j / 8 * 2 * math.pi + t * 0.6
        rt(frame, 960 + 600 * math.cos(ang), 460 + 230 * math.sin(ang), str(11 + j), int(110 * ease_back((k - j * 0.05) / 0.4)), colour=RAINBOW[j % 6])
    rt(frame, 960, 420, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.32)


def scene_warm(frame, s, t):
    n = current(s["ts"], t)
    for i in range(n):
        x = 260 + i * 155
        rt(frame, x, 300 - 20 * abs(math.sin(t * 5 + i)), str(i + 1), 120, colour=RAINBOW[i % 6])
    clap = any(0 <= t - x < 0.25 for x in s["ts"])
    for i, (nm, x) in enumerate((("gul", 700), ("misheal", 1220))):
        body(frame, nm, t, "excited", x, feet=1075, scale=0.4, hop=30 if clap else 0, wave=clap)
    word(frame, "CLAP AND COUNT!", t, s["t0"], size=110)


def scene_teen(frame, s, t):
    n = s["n"]
    q = t - s["t0"]
    badge(frame, 160, 90, f"{n - 10}/10")
    rt(frame, 520, 360, str(n), int(300 * ease_back(q / 0.35)), colour=RAINBOW[n % 6])
    rt(frame, 520, 560, WORDS[n].upper(), int(80 * ease_back((q - 0.2) / 0.35)), colour=(255, 255, 255), maxw=520)
    if t >= s.get("ten_t", 1e9):
        tenframe(frame, 1240, 200, n if t >= s["ten_t"] + 0.8 else 10)
        rt(frame, 1080, 420, "10", 70, colour=(255, 77, 109))
        if t >= s["ten_t"] + 0.8:
            rt(frame, 1440, 420, f"+ {n - 10}", 70, colour=(46, 168, 255))
    if t >= s["count_t"]:
        cols = 10
        for i in range(n):
            x = 840 + (i % cols) * 76
            y = 540 + (i // cols) * 90
            if t >= s["count_t"] + i * 0.05:
                item(frame, s["art"], x, y, 66)
    side_kids(frame, t, xs=(150, 1770), scale=0.26)


def scene_move(frame, s, t):
    n = current(s["ts"], t)
    mv = s["move"]
    beat = any(0 <= t - x < 0.25 for x in s["ts"])
    for i, (nm, x) in enumerate((("gul", 560), ("misheal", 1360))):
        hop = (110 if beat else 0) if mv == "jump" else (25 if beat else 0)
        body(frame, nm, t, "excited", x, scale=0.5, hop=hop, wave=mv == "clap" and beat)
    if n:
        rt(frame, 960, 470, str(n), int(320 * ease_back((t - s["ts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    word(frame, {"jump": "JUMP!", "clap": "CLAP!", "stomp": "STOMP!"}[mv], t, s["t0"], size=140)
    d = ImageDraw.Draw(frame)
    for i in range(20):
        x = 200 + i * 80
        d.ellipse((x - 22, 1000 - 22, x + 22, 1000 + 22), fill=RAINBOW[i % 6] if i < n else (255, 255, 255), outline=INK, width=4)


def scene_howmany(frame, s, t):
    n = current(s["ts"], t)
    total = s["n"]
    cols = 10 if total > 10 else 5
    for i in range(total):
        x = 960 - (cols - 1) * 75 + (i % cols) * 150
        y = 360 + (i // cols) * 170
        item(frame, s["art"], x, y + (6 * math.sin(t * 3 + i)), 110)
        if i < n:
            d = ImageDraw.Draw(frame)
            d.ellipse((x + 30, y - 75, x + 76, y - 29), fill=(255, 255, 255), outline=INK, width=4)
            rt(frame, x + 53, y - 52, str(i + 1), 36, colour=RAINBOW[i % 6])
    if t >= s["answer_t"]:
        word(frame, f"{total}!", t, s["answer_t"], size=160)
        stars_ring(frame, 960, 520, 700, 330, t, n=10)
    else:
        word(frame, "HOW MANY?", t, s["t0"], size=120)
    side_kids(frame, t, xs=(110, 1810), scale=0.24)


def numline(frame, nums, cy, t, hide=None, show=False, ans=None, t_ans=0):
    d = ImageDraw.Draw(frame)
    n = len(nums)
    x0 = 960 - (n - 1) * 115
    d.line((x0 - 100, cy + 95, x0 + (n - 1) * 230 + 100, cy + 95), fill=(255, 255, 255), width=8)
    for i, v in enumerate(nums):
        x = x0 + i * 230
        d.rounded_rectangle((x - 90, cy - 90, x + 90, cy + 90), radius=26, fill=(255, 255, 255), outline=INK, width=6)
        if v is None:
            if show:
                rt(frame, x, cy, str(ans), int(120 * ease_back((t - t_ans) / 0.3)), colour=(59, 193, 74))
            else:
                rt(frame, x, cy, "?", int(120 + 10 * math.sin(t * 6)), colour=(150, 160, 180))
        else:
            rt(frame, x, cy, str(v), 110, colour=RAINBOW[v % 6])


def scene_after(frame, s, t):
    show = t >= s["answer_t"]
    numline(frame, [s["n"], None], 420, t, show=show, ans=s["ans"], t_ans=s["answer_t"])
    rt(frame, 960, 175, "WHAT COMES NEXT?", int(90 * ease_back((t - s["t0"]) / 0.35)), colour=(255, 255, 255), maxw=1100)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_missing(frame, s, t):
    show = t >= s["answer_t"]
    numline(frame, s["row"], 420, t, show=show, ans=s["ans"], t_ans=s["answer_t"])
    rt(frame, 960, 175, "MISSING NUMBER!", int(90 * ease_back((t - s["t0"]) / 0.35)), colour=(255, 255, 255), maxw=1100)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_twos(frame, s, t):
    n = current(s["ts"], t)
    for i in range(n):
        x = 210 + (i % 5) * 380
        y = 380 + (i // 5) * 330
        item(frame, "shoes", x, y, 200)
        rt(frame, x, y + 130, str((i + 1) * 2), 90, colour=RAINBOW[i % 6])
    word(frame, "COUNT BY TWOS!", t, s["t0"], size=110)


def scene_rocket(frame, s, t):
    n = current(s["ts"], t)
    L = s["blast_t"]
    if t < L:
        if n:
            rt(frame, 960, 230, str(21 - n), int(220 * ease_back((t - s["ts"][n - 1]) / 0.25)), colour=RAINBOW[n % 6])
        shake = 6 * math.sin(t * 60) * min(1, n / 20)
        R.rocket(frame, 960 + shake, 700, 1.25, t, 0.25 if n >= 18 else 0)
    else:
        k = t - L
        d = ImageDraw.Draw(frame)
        for j in range(10):
            qq = k * 0.8 + j * 0.03
            x = 960 + (j - 4.5) * 90 * (1 + qq)
            r = 60 + 60 * min(1, qq)
            d.ellipse((x - r, 930 - r * 0.7, x + r, 930 + r * 0.7), fill=(240, 240, 245))
        y = 700 - 900 * k * k
        if y > -500:
            R.rocket(frame, 960, y, 1.25, t, 1.0)
        rt(frame, 960, 230, "BLAST OFF!", int(170 * ease_back(k / 0.4)))
    side_kids(frame, t, "excited", xs=(250, 1670), scale=0.3, feet=1000)


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 140, s["q"], int(72 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        rt(frame, 960, 540, str(s["vis"]), int(300 * ease_back((t - s["answer_t"]) / 0.35)), colour=RAINBOW[s["vis"] % 6])
        stars_ring(frame, 960, 540, 330, 230, t, n=8, r=20)
        side_kids(frame, t, "happy")
    else:
        rt(frame, 960, 540, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t)


def scene_outro(frame, s, t):
    for i in range(20):
        x = (i * 120 + t * 160) % 2600 - 150
        rt(frame, x, 1000 - 25 * abs(math.sin(t * 5 + i)), str(i + 1), 80, colour=RAINBOW[i % 6])
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, scale=0.5, feet=930, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 140, "YOU CAN COUNT TO 20!", int(110 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


def hand(frame, cx, cy, fingers, scale=1.0, col=(237, 194, 160)):
    d = ImageDraw.Draw(frame)
    k = scale
    d.rounded_rectangle((cx - 60 * k, cy - 40 * k, cx + 60 * k, cy + 80 * k), radius=int(40 * k), fill=col, outline=INK, width=5)
    for i in range(5):
        a = math.radians(-140 + i * 25)
        up = i < fingers
        L = (110 if up else 40) * k
        x0, y0 = cx + 45 * k * math.cos(a), cy + 45 * k * math.sin(a)
        x1, y1 = cx + (45 * k + L) * math.cos(a), cy + (45 * k + L) * math.sin(a)
        d.line((x0, y0, x1, y1), fill=INK, width=int(32 * k) + 6)
        d.line((x0, y0, x1, y1), fill=col, width=int(32 * k))


def scene_fingers(frame, s, t):
    nf = current(s["f_ts"], t)
    nt = current(s["t_ts"], t)
    toes = (1 if t >= s["t_ts"][0] - 0.8 else 0) + nt
    d = ImageDraw.Draw(frame)
    for j in range(2):
        item(frame, "hand", 560 + j * 300, 400, 260)
        item(frame, "foot", 1120 + j * 300, 420, 260)
    for i in range(20):
        x = 210 + i * 79
        c = RAINBOW[i % 6] if i < nf + toes else (255, 255, 255)
        d.ellipse((x - 26, 640, x + 26, 692), fill=c, outline=INK, width=4)
    total = nf + toes
    if total:
        rt(frame, 960, 860, str(total), 150, colour=RAINBOW[total % 6])
    if t >= s["sum_t"]:
        word(frame, "10 + 10 = 20!", t, s["sum_t"], size=140)
    else:
        word(frame, "FINGERS AND TOES!", t, s["t0"], size=110)


def scene_hide(frame, s, t):
    n = current(s["ts"], t)
    d = ImageDraw.Draw(frame)
    d.rectangle((1430, 520, 1490, 900), fill=(138, 90, 43), outline=INK, width=5)
    for dx, dy, r in ((-90, -40, 110), (80, -60, 120), (0, -150, 130)):
        d.ellipse((1460 + dx - r, 470 + dy - r, 1460 + dx + r, 470 + dy + r), fill=(76, 175, 80), outline=INK, width=5)
    if t < s["hide_t"]:
        body(frame, "misheal", t, None, 1100, scale=0.42)
    elif t < s["found_t"]:
        k = min(1, (t - s["hide_t"]) / 1.0)
        if k < 1:
            body(frame, "misheal", t, "excited", 1100 + 380 * k, scale=0.42)
    else:
        body(frame, "misheal", t, "excited", 1640, scale=0.42, hop=30 * abs(math.sin(t * 5)), wave=True)
    hiding = s["hide_t"] <= t < s["found_t"]
    body(frame, "gul", t, "calm" if hiding else "surprised" if t < s["found_t"] + 1 else "happy", 560, scale=0.45)
    if n and t < s["found_t"]:
        rt(frame, 960, 380, str(n), int(220 * ease_back((t - s["ts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    if t >= s["found_t"]:
        word(frame, "FOUND YOU!", t, s["found_t"], size=150)
    else:
        word(frame, "HIDE AND SEEK!", t, s["t0"], size=120)


def group(frame, cx, n, art, t):
    for i in range(n):
        x = cx - 200 + (i % 5) * 100
        y = 330 + (i // 5) * 110
        item(frame, art, x, y + 4 * math.sin(t * 3 + i), 80)


def scene_more(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, (n, art) in enumerate((s["g1"], s["g2"])):
        cx = 560 + j * 800
        good = t >= s["answer_t"] and j == s["ans"]
        d.rounded_rectangle((cx - 290, 250, cx + 290, 760), radius=30, fill=(255, 255, 255, 190), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        group(frame, cx, n, art, t)
        if t >= s["answer_t"]:
            rt(frame, cx, 830, str(n), 110, colour=(59, 193, 74) if good else (150, 150, 160))
    word(frame, "MORE!" if t >= s["answer_t"] else "WHICH HAS MORE?", t, s["answer_t"] if t >= s["answer_t"] else s["t0"], size=120)


def scene_onemore(frame, s, t):
    n = s["n"]
    tenframe(frame, 960, 250, n + (1 if t >= s["answer_t"] else 0))
    rt(frame, 700, 650, str(n), 150, colour=RAINBOW[n % 6])
    rt(frame, 900, 650, "+ 1 =", 110, colour=(255, 255, 255))
    if t >= s["answer_t"]:
        rt(frame, 1180, 650, str(n + 1), int(160 * ease_back((t - s["answer_t"]) / 0.3)), colour=(59, 193, 74))
    else:
        rt(frame, 1180, 650, "?", int(150 + 10 * math.sin(t * 6)), colour=(255, 255, 255))
    rt(frame, 960, 175, "ONE MORE!", int(90 * ease_back((t - s["t0"]) / 0.35)), colour=(255, 255, 255), maxw=900)
    side_kids(frame, t, xs=(150, 1770), scale=0.3)


def scene_fives(frame, s, t):
    n = current(s["ts"], t)
    for i in range(4):
        if i < n:
            item(frame, "hand", 360 + i * 400, 470, 240)
            rt(frame, 360 + i * 400, 720, str((i + 1) * 5), 110, colour=RAINBOW[i % 6])
    word(frame, "COUNT BY FIVES!", t, s["t0"], size=120)
    side_kids(frame, t, xs=(150, 1770), scale=0.26)


SCENES = {"fingers": scene_fingers, "hide": scene_hide, "more": scene_more, "onemore": scene_onemore, "fives": scene_fives, "intro": scene_intro, "title": scene_title, "warm": scene_warm, "teen": scene_teen, "move": scene_move, "howmany": scene_howmany,
          "after": scene_after, "missing": scene_missing, "twos": scene_twos, "rocket": scene_rocket, "quiz": scene_quiz, "outro": scene_outro}


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
    dst = OUT / f"Count to 20 for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=0", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
