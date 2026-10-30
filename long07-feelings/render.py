"""Animate Long video 7 "Feelings & Emotions" (1920x1080) from timeline.json, with the new expression layers.

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L07 Feelings/Feelings and Emotions for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L07 Feelings"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "bluetee", "misheal": "pink"}
VOC = {"gul": "gul", "misheal": "mishu"}
ART = {"icecream": ROOT / "long05-body-parts/art/item_icecream.png", "flower": ROOT / "long05-body-parts/art/item_flower.png",
       "teddy": ROOT / "long04-good-habits/art/item_teddy.png", "ball": ROOT / "long04-good-habits/art/item_ball.png",
       "water": ROOT / "long04-good-habits/art/item_water.png", "dog": ROOT / "long01-animals-fun/art/fruit_puppy.png",
       "puppy": ROOT / "long01-animals-fun/art/fruit_puppy.png", "sun": ROOT / "long01-animals-fun/art/fruit_sunny.png",
       "medal": ROOT / "long01-animals-fun/art/fruit_star.png", "music": ROOT / "long05-body-parts/art/item_drum.png"}
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text
EMO_COL = {"happy": (255, 200, 40), "sad": (46, 140, 255), "angry": (240, 60, 60), "scared": (155, 93, 229), "surprised": (255, 159, 28),
           "excited": (255, 77, 109), "tired": (120, 130, 170), "shy": (255, 120, 170), "proud": (59, 193, 74), "calm": (80, 190, 210)}


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["item"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in (HERE / "art").glob("item_*.png")}
    for k, p in ART.items():
        G["item"][k] = Image.open(p).convert("RGBA")
    G["bg"] = {"room": Image.open(HERE / "art" / "bg_room.png").convert("RGBA")}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"] = {}, {}
    rng = np.random.default_rng(6)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]


def talking(n, t):
    env = G["env"][n]
    return env[min(int(t * FPS), len(env) - 1)]


def compose(n, t, emo=None, arms=True, wave=False):
    """Full-res 1200x2000 character with an emotion face (or normal talking face when emo is None)."""
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


def big_face(frame, n, t, emo, cx=960, cy=580, scale=0.95, shake=0.0):
    if scale < 0.03:
        return
    im = compose(n, t, emo, arms=False)
    crop = im.crop((150, 100, 1050, 1000)).resize((int(900 * scale), int(900 * scale)), Image.BICUBIC)
    bob = 6 * math.sin(t * 2) + shake
    frame.alpha_composite(crop, (int(cx - crop.width / 2 + shake), int(cy - crop.height / 2 + bob)))


def body(frame, n, t, emo, cx, feet=1075, scale=0.5, hop=0.0, rot=0.0, wave=False):
    im = compose(n, t, emo, wave=wave)
    sm = im.resize((int(1200 * scale), int(2000 * scale)), Image.BICUBIC)
    if rot:
        sm = sm.rotate(rot, center=(sm.width / 2, sm.height), resample=Image.BICUBIC)
    frame.alpha_composite(sm, (int(cx - sm.width / 2), int(feet - sm.height * 0.93 - hop)))
    return sm


def item(frame, key, cx, cy, size, rot=0.0, bottom=False):
    k = (key, int(size))
    if k not in G["sized"]:
        if len(G["sized"]) > 200:
            G["sized"].clear()
        im = G["item"][key]
        im = im.crop(im.getbbox())
        f = max(2, size) / max(im.size)
        G["sized"][k] = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
    im = G["sized"][k]
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    y = cy - im.height if bottom else cy - im.height / 2
    frame.alpha_composite(im, (int(cx - im.width / 2), int(y)))


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 20 * abs(math.cos(t * 5 + ph)) + 4
            d.rectangle((x - w / 2, y - 10, x + w / 2, y + 10), fill=col)


def hearts(frame, cx, cy, t, t0, n=6):
    d = ImageDraw.Draw(frame, "RGBA")
    for j in range(n):
        p = ((t - t0) * 0.6 + j / n) % 1
        x = cx + 220 * math.sin(j * 1.7 + t)
        y = cy - p * 350
        r = 30
        a = int(255 * (1 - p))
        d.ellipse((x - r, y - r * 0.8, x, y + r * 0.2), fill=(255, 77, 109, a))
        d.ellipse((x, y - r * 0.8, x + r, y + r * 0.2), fill=(255, 77, 109, a))
        d.polygon([(x - r, y - 0.15 * r), (x + r, y - 0.15 * r), (x, y + r)], fill=(255, 77, 109, a))


def badge(frame, x, y, text, col=(255, 107, 139)):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=col)


def label(frame, emo, t, t0, y=110, size=150):
    rt(frame, 960, y, emo.upper() + "!", int(size * ease_back((t - t0) / 0.3)), colour=EMO_COL.get(emo), start=t0, t=t)


def side_kids(frame, t, emo=None):
    for n, x in (("gul", 240), ("misheal", 1680)):
        body(frame, n, t, emo, x, scale=0.36, hop=4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0))))


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    cur = None
    for t0, emo in s["flips"]:
        if t >= t0:
            cur = (t0, emo)
    if t < s["title_t"]:
        emo = cur[1] if cur else "happy"
        sh = 12 * math.sin(t * 50) * max(0, 1 - (t - cur[0]) / 0.2) if cur else 0
        big_face(frame, "gul", t, emo, shake=sh)
        label(frame, emo, t, cur[0] if cur else 0, size=140)
    else:
        q = t - s["title_t"]
        confetti(frame, t, s["title_t"])
        for n, x, emo in (("gul", 640, "excited"), ("misheal", 1280, "happy")):
            body(frame, n, t, emo if t < s["kids_t"] else None, x, scale=0.48, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
        rt(frame, 960, 200, "FEELINGS!", int(230 * ease_back(q / 0.35)))
        if q < 0.35:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - q / 0.35)))))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rt(frame, 960, 380, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy")


def scene_feeling(frame, s, t):
    big_face(frame, s["who"], t, s["emo"])
    label(frame, s["emo"], t, s["label_t"] - 0.3)
    badge(frame, 160, 90, f"{s['num']}/10")
    if s["emo"] == "tired":
        for j in range(3):
            p = (t * 0.6 + j / 3) % 1
            rt(frame, 1380 + p * 120, 420 - p * 220, "Z", int(60 + 50 * p), colour=(150, 160, 255))
    if s["emo"] in ("happy", "proud", "excited"):
        d = ImageDraw.Draw(frame)
        for j in range(8):
            a = j / 8 * 2 * math.pi + t
            R.star(d, 960 + 520 * math.cos(a), 580 + 400 * math.sin(a), 24, RAINBOW[j % 6], rot=t * 2)
    if s["emo"] == "angry":
        for j, x in enumerate((700, 1220)):
            p = (t * 0.9 + j * 0.5) % 1
            d = ImageDraw.Draw(frame, "RGBA")
            r = 40 + 50 * p
            d.ellipse((x - r, 230 - p * 120 - r * 0.6, x + r, 230 - p * 120 + r * 0.6), fill=(240, 240, 245, int(220 * (1 - p))))


def scene_story(frame, s, t):
    who, other = s["who"], ("misheal" if s["who"] == "gul" else "gul")
    ev, ans = s["event_t"], s["answer_t"]
    felt = t >= ev + 1.0
    emo = s["emo"] if felt else None
    sx, ox = 760, 1260
    shake = 10 * math.sin(t * 40) if (s["emo"] == "scared" and felt and t < ans + 1) else 0
    body(frame, who, t, emo, sx + shake, scale=0.5, hop=(30 * abs(math.sin(t * 5)) if felt and s["emo"] in ("excited", "proud") else 0))
    body(frame, other, t, None, ox, scale=0.5)
    p = s["prop"]
    q = t - ev
    if p == "icecream":
        if t < ev + 0.9:
            item(frame, "icecream", sx + 150, 560, 200, rot=10 * math.sin(t * 3))
        else:
            k = min(1, (t - ev - 0.9) / 0.35)
            if k < 1:
                item(frame, "icecream", sx + 150, 560 + 420 * k * k, 200, rot=180 * k)
            else:
                item(frame, "icecream_drop", sx + 160, 1050, 230, bottom=True)
    elif p == "gift":
        if t < ev + 0.8:
            item(frame, "gift", sx + 220, 900, 260, rot=8 * math.sin(t * 12) if t > ev else 0)
        else:
            item(frame, "teddy", sx + 220, 860 - 40 * abs(math.sin(t * 4)), 260)
            confetti(frame, t, ev + 0.8) if t < ev + 3 else None
    elif p == "ball":
        item(frame, "ball" if t < ev + 1.0 else "ballbroken", sx + 220, 950 - (40 * abs(math.sin(t * 5)) if t < ev else 0), 220)
    elif p == "thunder":
        item(frame, "thunder", 960, 250, 340)
        if ev + 0.2 <= t < ev + 0.7 and int((t - ev) * 12) % 2 == 0:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 230, 150)))
        dr = ImageDraw.Draw(frame)
        for j in range(30):
            pp = (t * 1.3 + j / 30) % 1
            x = (j * 73) % 1920
            dr.line((x, 380 + pp * 600, x - 8, 410 + pp * 600), fill=(110, 170, 255), width=5)
    elif p == "balloons":
        if t >= ev:
            item(frame, "balloons", 1000, 380 - 30 * abs(math.sin(t * 2)), 380)
            confetti(frame, t, ev) if t < ev + 3 else None
    elif p == "puzzle":
        item(frame, "puzzle", sx + 240, 900, 230)
        if t >= ev + 0.5:
            d = ImageDraw.Draw(frame)
            for j in range(8):
                a = j / 8 * 2 * math.pi + t * 2
                R.star(d, sx + 240 + 170 * math.cos(a), 900 + 130 * math.sin(a), 20, RAINBOW[j % 6], rot=t * 3)
    elif p == "teddy":
        if t >= ans + 2.5:
            item(frame, "teddy", sx + 220, 880 - 30 * abs(math.sin(t * 4)), 240)
    elif p == "dog":
        if t >= ev + 0.8:
            k = min(1, (t - ev - 0.8) / 0.6)
            item(frame, "dog", 1700 - 500 * k, 900 - 20 * abs(math.sin(t * 8)), 300)
    elif p == "medal":
        if t >= ev + 0.6:
            item(frame, "medal", sx + 220, 560 - 20 * abs(math.sin(t * 4)), 220 * ease_back((t - ev - 0.6) / 0.4))
            confetti(frame, t, ev + 0.6) if t < ev + 3 else None
    if t >= ans:
        label(frame, s["emo"], t, ans)
    else:
        rt(frame, 960, 110, "HOW DO THEY FEEL?", int(100 * ease_back((t - s["t0"]) / 0.35)))


def scene_guess(frame, s, t):
    big_face(frame, s["who"], t, s["emo"])
    if t >= s["answer_t"]:
        label(frame, s["emo"], t, s["answer_t"])
    else:
        rt(frame, 960, 110, "HOW DOES IT FEEL?", int(100 * ease_back((t - s["t0"]) / 0.35)))
        rt(frame, 1480, 560, "?", int(220 + 20 * math.sin(t * 6)), colour=(255, 255, 255))


def scene_breathe(frame, s, t):
    cur = None
    for b_in, b_out in s["breaths"]:
        if b_in <= t < b_in + 2.0:
            cur = ("in", b_in)
        elif b_out <= t < b_out + 2.0:
            cur = ("out", b_out)
    d = ImageDraw.Draw(frame, "RGBA")
    if cur:
        ph, t0 = cur
        k = min(1, (t - t0) / 1.8)
        r = 120 + 200 * (k if ph == "in" else 1 - k)
        d.ellipse((960 - r, 560 - r, 960 + r, 560 + r), fill=(120, 210, 230, 80), outline=(80, 190, 210, 200), width=10)
        rt(frame, 960, 140, "BREATHE IN..." if ph == "in" else "BREATHE OUT...", 110, colour=(80, 190, 210))
    item(frame, "flower", 700, 600, 300 * (1.08 if cur and cur[0] == "in" else 1.0))
    item(frame, "candle", 1220, 600, 300, rot=(14 * math.sin(t * 20) if cur and cur[0] == "out" else 0))
    side_kids(frame, t, "calm")


def scene_tool(frame, s, t):
    q = t - s["t0"]
    badge(frame, 160, 90, f"TIP {s['num']}", (80, 190, 210))
    rt(frame, 960, 130, s["word"], int(110 * ease_back(q / 0.35)), maxw=1500)
    if s["prop"] == "count":
        dur = next(e["dur"] for e in G["lines"] if abs(e["t"] - s["say_t"]) < 0.01)
        n = int(max(0, min(5, (t - s["say_t"] - dur * 0.35) / (dur * 0.65) * 5 + 1)))
        for i in range(n):
            rt(frame, 960 + (i - 2) * 190, 580, str(i + 1), 200, colour=RAINBOW[i % 6])
    else:
        item(frame, s["prop"], 960, 600 + 10 * math.sin(t * 2), 380 * ease_back(q / 0.4))
    side_kids(frame, t, "calm")


def scene_dance(frame, s, t):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv = s["move"]
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, dx = 0, 0, 0
        if mv == "jump":
            hop = 90 * abs(math.sin(q * 5 + i))
        elif mv == "stomp":
            hop = 30 * abs(math.sin(q * 6 + i))
        elif mv == "sway":
            rot = 8 * math.sin(q * 2.5 + i)
        elif mv == "pop":
            hop = 50 * max(0, math.sin(q * 3))
        elif mv == "shake":
            dx = 14 * math.sin(q * 40)
        elif mv == "slow":
            hop = 10 * math.sin(q * 1.5)
        body(frame, n, t, s["emo"], x + dx, scale=0.55, hop=hop, rot=rot, wave=mv in ("jump", "pop"))
    word = next(e["text"] for e in G["lines"] if abs(e["t"] - s["say_t"]) < 0.01).split("!")[0].upper() + "!"
    rt(frame, 960, 110, word, int(120 * ease_back(q / 0.3)), colour=EMO_COL[s["emo"]], maxw=1500)


def scene_kind(frame, s, t):
    who = s["who"]
    helper = "misheal" if who == "gul" else "gul"
    happy = t >= s["happy_t"]
    body(frame, who, t, "happy" if happy else "sad", 680, scale=0.52, hop=(25 * abs(math.sin(t * 5)) if happy else 0))
    hx = 1600 if t < s["help_t"] else 1600 - 360 * ease_io(min(1, (t - s["help_t"]) / 0.8))
    body(frame, helper, t, None, hx, scale=0.52, wave=t >= s["help_t"])
    if t >= s["help_t"] + 0.5:
        item(frame, s["prop"], (680 + hx) / 2, 470 - 20 * abs(math.sin(t * 3)), 200)
    if happy:
        hearts(frame, 960, 600, t, s["happy_t"])
        rt(frame, 960, 110, "KIND FRIENDS!", int(110 * ease_back((t - s["happy_t"]) / 0.3)))
    else:
        rt(frame, 960, 110, "HOW CAN WE HELP?", int(100 * ease_back((t - s["t0"]) / 0.35)))


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 120, s["q"], int(80 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        big_face(frame, s["who"], t, s["emo"], cy=620, scale=0.8)
    else:
        rt(frame, 960, 600, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t)


def scene_outro(frame, s, t):
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy", x, scale=0.55, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    hearts(frame, 960, 700, t, s["t0"], 8)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 150, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)))
    else:
        rt(frame, 960, 150, "ALL FEELINGS ARE OKAY!", int(100 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


def scene_happy(frame, s, t):
    q = t - s["t0"]
    if s["prop"] == "question":
        rt(frame, 960, 560, "?", int(300 + 20 * math.sin(t * 6)), colour=(255, 200, 40))
        rt(frame, 960, 130, "WHAT MAKES YOU HAPPY?", int(100 * ease_back(q / 0.35)), maxw=1600)
    else:
        item(frame, s["prop"], 960, 560 + 10 * math.sin(t * 2), 400 * ease_back(q / 0.4))
        d = ImageDraw.Draw(frame)
        for j in range(8):
            a = j / 8 * 2 * math.pi + t
            R.star(d, 960 + 330 * math.cos(a), 560 + 260 * math.sin(a), 22, RAINBOW[j % 6], rot=t * 2)
        rt(frame, 960, 130, "HAPPY!", int(120 * ease_back(q / 0.3)), colour=EMO_COL["happy"])
    for n, x in (("gul", 240), ("misheal", 1680)):
        body(frame, n, t, "happy", x, scale=0.36, hop=12 * abs(math.sin(t * 3 + (1 if n == "gul" else 0))))


def scene_mirror(frame, s, t):
    big_face(frame, "gul", t, s["emo"], cx=640, cy=600, scale=0.75)
    big_face(frame, "misheal", t, s["emo"], cx=1280, cy=600, scale=0.75)
    label(frame, s["emo"], t, s["say_t"], size=130)


def scene_checkin(frame, s, t):
    q = t - s["t0"]
    emos = ["happy", "sad", "angry", "scared", "excited", "calm"]
    for i, e in enumerate(emos):
        x = 480 + (i % 3) * 480
        y = 400 + (i // 3) * 360
        big_face(frame, "misheal" if i % 2 else "gul", t, e, cx=x, cy=y, scale=0.32 * ease_back((q - i * 0.1) / 0.4) + 0.001)
        rt(frame, x, y + 165, e.upper(), 50, colour=EMO_COL[e])
    rt(frame, 960, 100, "HOW DO YOU FEEL TODAY?", int(100 * ease_back(q / 0.35)), maxw=1600)


SCENES = {"checkin": scene_checkin, "happy": scene_happy, "mirror": scene_mirror, "intro": scene_intro, "title": scene_title, "feeling": scene_feeling, "story": scene_story, "guess": scene_guess,
          "breathe": scene_breathe, "tool": scene_tool, "dance": scene_dance, "kind": scene_kind, "quiz": scene_quiz, "outro": scene_outro}


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
    dst = OUT / f"Feelings and Emotions for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
