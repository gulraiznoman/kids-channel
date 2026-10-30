"""Animate Long video 2 "Count 1 to 10" (1920x1080, 30 fps) from timeline.json.

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L02 Count 1 to 10/Count 1 to 10 for Kids vN.mp4
"""
import json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
KIT = ROOT / "characters" / "layers"
OUT = ROOT / "VIDEOS" / "L02 Count 1 to 10"
W, H, FPS = 1920, 1080, 30
S = 0.38
FONT = "C:/Windows/Fonts/seguibl.ttf"
INK = (58, 36, 32)
RAINBOW = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
CHAR = {"gul": dict(outfit="tee", x=250, girl=False, voc="gul"), "misheal": dict(outfit="yellow", x=1670, girl=True, voc="mishu")}
STAGE = (500, 400, 1420, 930)                      # x0, y0, x1, y1 for counted objects
ART_DIRS = [(ROOT / "ep01-fruits" / "art", "fruit_"), (ROOT / "long01-animals-fun" / "art", "fruit_"),
            (ROOT / "halloween01" / "art", "item_")]
G = {}


# ------------------------------------------------------------------ setup
def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["fonts"], G["cache"], G["sized"] = {}, {}, {}
    keys = {s["key"] for s in tl["scenes"] if "key" in s} | {"fish"}
    G["art"] = {}
    for k in keys:
        for d, pre in ART_DIRS:
            p = d / f"{pre}{k}.png"
            if p.exists():
                G["art"][k] = Image.open(p).convert("RGBA")
                break
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
    L1 = ROOT / "long01-animals-fun" / "art"
    G["bg"] = {"rainbow": load_bg(L1 / "bg_rainbow.png"), "garden": load_bg(L1 / "bg.png"), "farm": load_bg(L1 / "bg_farm.png"),
               "road": load_bg(L1 / "bg_road.png"), "beach": load_bg(L1 / "bg_beach.png"),
               "halloween": bg_halloween(), "space": bg_space()}


def load_bg(p):
    return Image.open(p).convert("RGBA").resize((W, H), Image.LANCZOS)


def gradient(top, bot):
    y = np.linspace(0, 1, H)[:, None, None]
    img = (np.array(top, float) * (1 - y) + np.array(bot, float) * y).astype(np.uint8)
    return Image.fromarray(np.repeat(img, W, axis=1)).convert("RGBA")


def bg_halloween():
    im = gradient((176, 156, 240), (255, 214, 186))
    d = ImageDraw.Draw(im)
    mx, my, r = 1640, 170, 80
    d.ellipse((mx - r - 22, my - r - 22, mx + r + 22, my + r + 22), fill=(255, 245, 190))
    d.ellipse((mx - r, my - r, mx + r, my + r), fill=(255, 226, 110), outline=INK, width=6)
    for ex in (mx - 28, mx + 28):
        d.arc((ex - 13, my - 20, ex + 13, my + 2), 200, 340, fill=INK, width=6)
    d.arc((mx - 28, my - 4, mx + 28, my + 38), 20, 160, fill=INK, width=6)
    d.polygon([(0, 860), (500, 820), (1000, 860), (1500, 810), (W, 850), (W, H), (0, H)], fill=(150, 205, 120))
    for x in range(10, W, 100):
        d.rounded_rectangle((x, 720, x + 44, 880), radius=10, fill=(255, 255, 255), outline=INK, width=5)
    d.rectangle((0, 760, W, 782), fill=(255, 255, 255), outline=INK, width=5)
    d.rectangle((0, 830, W, 852), fill=(255, 255, 255), outline=INK, width=5)
    d.rectangle((0, 960, W, H), fill=(126, 196, 98))
    return im


def bg_space():
    im = gradient((38, 52, 120), (110, 70, 170))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(3)
    for _ in range(140):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H * 0.85), rng.uniform(2, 6)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 250, 220))
    d.ellipse((1500, 90, 1700, 290), fill=(255, 150, 120), outline=INK, width=6)
    d.ellipse((1460, 170, 1740, 210), outline=(255, 220, 140), width=10)
    d.ellipse((150, 120, 260, 230), fill=(120, 220, 200), outline=INK, width=5)
    d.ellipse((-200, 930, W + 200, 1400), fill=(150, 150, 175), outline=INK, width=6)
    for cx, cy, r in ((500, 1010, 40), (1200, 990, 30), (1500, 1040, 50)):
        d.ellipse((cx - r, cy - r * 0.5, cx + r, cy + r * 0.5), fill=(120, 120, 150))
    return im


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


def rainbow_text(img, cx, cy, text, size, start=None, t=0.0, colour=None, maxw=1100):
    if size < 2:
        return
    d = ImageDraw.Draw(img)
    f = font(size)
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + 6 * (len(text) - 1)
    if total > maxw:
        size = max(2, int(size * maxw / total))
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
        d.text((x, y), ch, font=f, fill=colour or RAINBOW[i % 6], stroke_width=int(size * 0.07), stroke_fill=(255, 255, 255))
        x += widths[i] + 6


def item(key, size):
    size = max(2, int(size))
    k = (key, size)
    if k not in G["sized"]:
        if len(G["sized"]) > 400:
            G["sized"].clear()
        G["sized"][k] = G["art"][key].resize((size, size), Image.BICUBIC)
    return G["sized"][k]


def paste(frame, key, cx, cy, size, rot=0.0):
    a = item(key, size)
    if rot:
        a = a.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(a, (int(cx - a.width / 2), int(cy - a.height / 2)))


def star(d, cx, cy, r, col, rot=0.0):
    pts = [(cx + (r if k % 2 == 0 else r * 0.45) * math.cos(rot + k * math.pi / 5 - math.pi / 2),
            cy + (r if k % 2 == 0 else r * 0.45) * math.sin(rot + k * math.pi / 5 - math.pi / 2)) for k in range(10)]
    d.polygon(pts, fill=col, outline=INK, width=4)


def badge(frame, cx, cy, n, k):
    s = ease_back(k / 0.3)
    r = int(36 * s)
    if r < 3:
        return
    d = ImageDraw.Draw(frame)
    d.ellipse((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), fill=INK)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RAINBOW[(n - 1) % 6])
    f = font(max(8, int(44 * s)))
    txt = str(n)
    w = d.textlength(txt, font=f)
    d.text((cx - w / 2, cy - 44 * s * 0.62), txt, font=f, fill=(255, 255, 255), stroke_width=3, stroke_fill=INK)


# ------------------------------------------------------------------ layouts
def grid(n, box=STAGE):
    x0, y0, x1, y1 = box
    cols = n if n <= 5 else math.ceil(n / 2)
    rows = 1 if n <= 5 else 2
    cell = min((x1 - x0) / cols, (y1 - y0) / rows)
    size = min(360 if n == 1 else 320 if n <= 3 else 280, cell * 0.88)
    pts = []
    for i in range(n):
        r, c = divmod(i, cols)
        in_row = cols if r < rows - 1 else n - cols * (rows - 1)
        cx = (x0 + x1) / 2 + (c - (in_row - 1) / 2) * cell
        cy = (y0 + y1) / 2 + (r - (rows - 1) / 2) * cell
        pts.append((cx, cy))
    return pts, size


def counted(frame, key, pts, size, t, appear, count_t):
    """Objects pop in at `appear[i]`, then jump and get a number badge at `count_t[i]`."""
    for i, (cx, cy) in enumerate(pts):
        if t < appear[i]:
            continue
        s = ease_back((t - appear[i]) / 0.35)
        bob = 5 * math.sin(t * 2.4 + i)
        jump = 0
        if i < len(count_t) and count_t[i] <= t < count_t[i] + 0.35:
            jump = -40 * math.sin((t - count_t[i]) / 0.35 * math.pi)
        paste(frame, key, cx, cy + bob + jump, size * s)
        if i < len(count_t) and t >= count_t[i]:
            badge(frame, cx + size * 0.36, cy - size * 0.36 + jump, i + 1, t - count_t[i])


def stars_burst(frame, t):
    d = ImageDraw.Draw(frame)
    for st in G["stars"]:
        k = t - st
        if 0 <= k < 1.2:
            for j in range(10):
                a = j / 10 * 2 * math.pi + 0.3
                r = 160 + 380 * min(1, k / 0.6)
                rr = int(36 * (1 - max(0, (k - 0.7) / 0.5))) + 1
                star(d, 960 + r * math.cos(a), 600 + r * math.sin(a) * 0.7, rr, RAINBOW[j % 6], rot=k * 3)


def your_turn(frame, t):
    for p0, p1 in G["prompts"]:
        if p0 <= t < p1:
            k = t - p0
            sc = ease_back(k / 0.3) * (1 + 0.04 * math.sin(k * 9))
            w, h = int(520 * sc), int(110 * sc)
            if w > 10:
                d = ImageDraw.Draw(frame)
                d.rounded_rectangle((960 - w // 2, 955, 960 + w // 2, 955 + h), radius=h // 2, fill=(255, 255, 255), outline=INK, width=6)
                f = font(max(8, int(62 * sc)))
                txt = "YOUR TURN!"
                tw = d.textlength(txt, font=f)
                d.text((960 - tw / 2, 955 + h * 0.5 - 62 * sc * 0.62), txt, font=f, fill=(255, 77, 109), stroke_width=4, stroke_fill=(255, 255, 255))


# ------------------------------------------------------------------ scenes
def scene_number(frame, s, t):
    n = s["n"]
    if t >= s["numeral_t"] - 0.3:
        k = (t - s["numeral_t"] + 0.3) / 0.4
        rainbow_text(frame, 960, 250, str(n), int(230 * ease_back(k)), colour=RAINBOW[(n - 1) % 6])
        if t >= s["numeral_t"] + 0.4:
            rainbow_text(frame, 960, 360, ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN"][n - 1],
                         int(70 * ease_back((t - s["numeral_t"] - 0.4) / 0.3)))
    pts, size = grid(n, (500, 440, 1420, 950))
    counted(frame, s["key"], pts, size, t, s["count_t"], s["count_t"])


def scene_count(frame, s, t):
    n = s["n"]
    pts, size = grid(n)
    appear = [s["t0"] + 0.25 + i * 0.07 for i in range(n)]
    counted(frame, s["key"], pts, size, t, appear, s["count_t"])
    if t < s["count_t"][0]:
        if t > s["t0"] + 0.6:
            rainbow_text(frame, 960, 230, "HOW MANY?", int(130 * ease_back((t - s["t0"] - 0.6) / 0.4)))
    elif t >= s["answer_t"]:
        rainbow_text(frame, 960, 230, str(n), int(200 * ease_back((t - s["answer_t"]) / 0.4)), colour=RAINBOW[(n - 1) % 6])


def scene_add(frame, s, t):
    a, b = s["a"], s["b"]
    lp, ls = grid(a, (480, 430, 900, 930))
    rp, rs = grid(b, (1020, 430, 1440, 930))
    size = min(ls, rs, 240)
    app_l = [s["left_t"] + i * 0.1 for i in range(a)]
    app_r = [s["right_t"] + i * 0.1 for i in range(b)]
    counted(frame, s["key"], lp, size, t, app_l, s["count_t"][:a])
    counted(frame, s["key"], rp, size, t, app_r, s["count_t"][a:])
    if t >= s["right_t"] - 0.2:
        rainbow_text(frame, 960, 665, "+", int(150 * ease_back((t - s["right_t"] + 0.2) / 0.3)), colour=(255, 255, 255))
    if t >= s["answer_t"]:
        rainbow_text(frame, 960, 230, f"{a} + {b} = {a + b}", int(160 * ease_back((t - s["answer_t"]) / 0.4)))
    elif t >= s["left_t"]:
        rainbow_text(frame, 960, 230, f"{a} + {b}" if t >= s["right_t"] else f"{a}", int(150 * ease_back((t - s["left_t"]) / 0.4)))


def scene_song(frame, s, t):
    nums = s["count_t"] + s["count2_t"]
    for i, ct in enumerate(nums):
        if t >= ct:
            x = 960 + (i - 4.5) * 110
            rainbow_text(frame, x, 200, str(i + 1), int(110 * ease_back((t - ct) / 0.3)), colour=RAINBOW[i % 6])
    # fish: jumps up when caught (line 1), swims away (line 2)
    l1, l2 = s["line1_t"], s["line2_t"]
    if t < l1:
        x, y, rot = 960 + 220 * math.sin(t * 1.2), 760 + 20 * math.sin(t * 3), 0
    elif t < l2:
        k = min(1, (t - l1) / 0.6)
        x, y, rot = 960, 760 - 260 * math.sin(k * math.pi / 2) + 10 * math.sin(t * 8), 15 * math.sin(t * 10)
    else:
        k = (t - l2) / 1.6
        x, y, rot = 960 + k * 900, 500 + 260 * min(1, k * 2) + 20 * math.sin(t * 6), -10
    paste(frame, "fish", x, y, 300, rot)


def scene_rhyme_end(frame, s, t):
    paste(frame, "fish", 960 + 60 * math.sin(t * 2), 640 + 20 * math.sin(t * 5), 340, 10 * math.sin(t * 6))
    rainbow_text(frame, 960, 250, "SILLY FISH!", int(120 * ease_back((t - s["t0"]) / 0.4)))


def rocket(frame, cx, cy, scale, t, flame):
    d = ImageDraw.Draw(frame)
    u = scale
    if flame > 0:
        for j, col in enumerate(((255, 120, 40), (255, 200, 60), (255, 250, 200))):
            fl = (150 - j * 40) * flame * (1 + 0.15 * math.sin(t * 40 + j))
            w = (60 - j * 16) * u
            d.polygon([(cx - w, cy + 150 * u), (cx + w, cy + 150 * u), (cx, cy + 150 * u + fl * u)], fill=col)
    d.polygon([(cx - 70 * u, cy + 60 * u), (cx - 140 * u, cy + 170 * u), (cx - 70 * u, cy + 140 * u)], fill=(255, 77, 109), outline=INK)
    d.polygon([(cx + 70 * u, cy + 60 * u), (cx + 140 * u, cy + 170 * u), (cx + 70 * u, cy + 140 * u)], fill=(255, 77, 109), outline=INK)
    d.rounded_rectangle((cx - 72 * u, cy - 120 * u, cx + 72 * u, cy + 150 * u), radius=int(40 * u), fill=(245, 245, 250), outline=INK, width=6)
    d.polygon([(cx - 72 * u, cy - 100 * u), (cx, cy - 250 * u), (cx + 72 * u, cy - 100 * u)], fill=(255, 77, 109), outline=INK)
    d.ellipse((cx - 38 * u, cy - 70 * u, cx + 38 * u, cy + 6 * u), fill=(120, 200, 255), outline=INK, width=6)
    d.ellipse((cx - 18 * u, cy - 56 * u, cx - 2 * u, cy - 40 * u), fill=(255, 255, 255))
    d.rectangle((cx - 72 * u, cy + 70 * u, cx + 72 * u, cy + 92 * u), fill=(255, 200, 40), outline=INK, width=4)


def scene_rocket(frame, s, t):
    L = s["launch_t"]
    for i, ct in enumerate(s["count_t"]):
        nxt = s["count_t"][i + 1] if i + 1 < len(s["count_t"]) else L
        if ct <= t < nxt:
            rainbow_text(frame, 960, 240, str(10 - i), int(220 * ease_back((t - ct) / 0.3)), colour=RAINBOW[i % 6])
    if t < L:
        shake = 0
        if t >= s["count_t"][0]:
            shake = (t - s["count_t"][0]) / max(0.1, L - s["count_t"][0]) * 8 * math.sin(t * 60)
        rocket(frame, 960 + shake, 700, 1.25, t, 0.25 if t > s["count_t"][-1] else 0)
    else:
        k = t - L
        y = 700 - 900 * k * k
        d = ImageDraw.Draw(frame)
        for j in range(10):                                   # smoke clouds on the launch pad
            q = k * 0.8 + j * 0.03
            x = 960 + (j - 4.5) * 90 * (1 + q)
            r = 60 + 60 * min(1, q)
            d.ellipse((x - r, 930 - r * 0.7, x + r, 930 + r * 0.7), fill=(240, 240, 245))
        if y > -500:
            rocket(frame, 960, y, 1.25, t, 1.0)
        rainbow_text(frame, 960, 240, "BLAST OFF!", int(170 * ease_back(k / 0.4)))


def scene_intro(frame, s, t):
    rainbow_text(frame, 960, 180, "GUL & MISHU", int(140 * ease_back(t / 0.6)))
    if t > 0.6:
        rainbow_text(frame, 960, 330, "COUNT 1 TO 10!", int(100 * ease_back((t - 0.6) / 0.5)), colour=(255, 255, 255))
    for i in range(10):
        k = t - 1.0 - i * 0.12
        if k > 0:
            rainbow_text(frame, 960 + (i - 4.5) * 95, 600 - 25 * abs(math.sin(t * 3 + i * 0.6)), str(i + 1),
                         int(100 * ease_back(k / 0.3)), colour=RAINBOW[i % 6])


def scene_outro(frame, s, t):
    for i in range(10):
        k = t - s["t0"] - i * 0.1
        if k > 0:
            rainbow_text(frame, 960 + (i - 4.5) * 95, 560 - 25 * abs(math.sin(t * 3 + i * 0.6)), str(i + 1),
                         int(110 * ease_back(k / 0.3)), colour=RAINBOW[i % 6])
    if t >= s["bye_t"]:
        rainbow_text(frame, 960, 260, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.4)))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rainbow_text(frame, 960, 380, s["title"], int(160 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t)


SCENES = {"number": scene_number, "count": scene_count, "add": scene_add, "song": scene_song, "rhyme_end": scene_rhyme_end,
          "rocket": scene_rocket, "intro": scene_intro, "outro": scene_outro, "title": scene_title}


# ------------------------------------------------------------------ characters
def compose_char(name, t):
    c, L = CHAR[name], G["layers"][name]
    o = c["outfit"]
    env = G["env"][name]
    v = env[min(int(t * FPS), len(env) - 1)]
    talking = v > 0.12
    mouth = "smile" if not talking else ("o" if v < 0.5 else "open")
    eyes = "blink" if (t + (1.3 if name == "gul" else 0)) % 4.1 < 0.12 else "open"
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
    for n, c in CHAR.items():
        im, talking = compose_char(n, t)
        hop = 10 * abs(math.sin(t * 5)) if talking else 4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0)))
        frame.alpha_composite(im, (int(c["x"] - im.width / 2), int(1075 - 0.93 * im.height - hop)))


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SCENES[sc["kind"]](frame, sc, t)
    stars_burst(frame, t)
    draw_kids(frame, t)
    your_turn(frame, t)
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
    NW = int(os.environ.get("NW", "6"))
    parts = 24                                              # small chunks so a crash loses little
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Count 1 to 10 for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
