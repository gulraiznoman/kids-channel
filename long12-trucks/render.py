"""Animate Long video 12 "Excavator & Construction Trucks" (1920x1080) from timeline.json.
Truck bodies come from art/truck_*.png (800x400 viewBox, ground y=380, facing left); wheels and moving parts are drawn here.

python render.py frames 100,900,...  -> preview contact sheet _sheet.png
python render.py video               -> VIDEOS/L12 Trucks/Excavator and Trucks for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L12 Trucks"
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "polo", "misheal": "pink"}
VOC = {"gul": "gul", "misheal": "mishu"}
A12 = HERE / "art"
WHEELS = {"dumptruck": [(150, 340, 40), (560, 340, 40), (660, 340, 40)], "mixer": [(150, 340, 40), (560, 340, 40), (660, 340, 40)],
          "crane": [(150, 340, 40), (560, 340, 40), (660, 340, 40)], "towtruck": [(150, 340, 40), (560, 340, 40), (660, 340, 40)],
          "garbage": [(150, 340, 40), (560, 340, 40), (660, 340, 40)], "roller": [(620, 335, 45)], "monster": [(190, 305, 75), (610, 305, 75)],
          "excavator": [], "bulldozer": []}
NAMES = {"excavator": "EXCAVATOR", "dumptruck": "DUMP TRUCK", "bulldozer": "BULLDOZER", "mixer": "CEMENT MIXER", "crane": "CRANE TRUCK",
         "roller": "ROAD ROLLER", "garbage": "GARBAGE TRUCK", "firetruck": "FIRE TRUCK", "towtruck": "TOW TRUCK", "monster": "MONSTER TRUCK"}
YEL, YDK = (255, 194, 26), (224, 160, 0)
G = {}
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["truck"] = {p.stem[6:]: Image.open(p).convert("RGBA") for p in A12.glob("truck_*.png")}
    G["item"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in A12.glob("item_*.png")}
    G["item"]["firetruck"] = Image.open(ROOT / "long01-animals-fun/art/fruit_firetruck.png").convert("RGBA")
    G["item"]["car"] = Image.open(ROOT / "long01-animals-fun/art/fruit_car.png").convert("RGBA")
    for k, pth in (("fossil", "long06-dinosaurs/art/item_fossil.png"), ("coin", "long11-bath/art/item_coin.png"),
                   ("ball", "long04-good-habits/art/item_ball.png"), ("key", "long11-bath/art/item_key.png"), ("rock", "long11-bath/art/item_rock.png"),
                   ("bone", "long05-body-parts/art/item_bone.png"), ("egg", "long06-dinosaurs/art/item_egg.png")):
        G["item"][k] = Image.open(ROOT / pth).convert("RGBA")
    G["bg"] = {p.stem[3:]: Image.open(p).convert("RGBA") for p in A12.glob("bg_*.png")}
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(HERE / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"], G["tsz"] = {}, {}, {}
    rng = np.random.default_rng(12)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]
    G["dirt"] = [(rng.uniform(-1, 1), rng.uniform(0.5, 1.3), rng.uniform(8, 22)) for _ in range(40)]


def dur(t0):
    return G["dur"].get(round(t0, 3), 1.5)


def talking(n, t):
    env = G["env"][n]
    return env[min(int(t * FPS), len(env) - 1)]


# ------------------------------------------------------------------ characters (with hard hats)
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
    hat = G["item"]["hardhat"].crop(G["item"]["hardhat"].getbbox())
    hat = hat.resize((780, int(780 * hat.height / hat.width)), Image.LANCZOS)
    im.alpha_composite(hat, (600 - 390, 250 - hat.height // 2))
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


# ------------------------------------------------------------------ drawing helpers
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


def wheel(d, x, y, r, ang):
    d.ellipse((x - r, y - r, x + r, y + r), fill=(43, 43, 51), outline=INK, width=max(3, int(r * 0.12)))
    d.ellipse((x - r * 0.5, y - r * 0.5, x + r * 0.5, y + r * 0.5), fill=(201, 204, 214), outline=INK, width=max(2, int(r * 0.08)))
    for j in range(4):
        a = ang + j * math.pi / 2
        d.line((x, y, x + r * 0.45 * math.cos(a), y + r * 0.45 * math.sin(a)), fill=(110, 115, 128), width=max(2, int(r * 0.1)))


def truck(frame, key, cx, gy, k, t, act=None, p=0.0, spin=0.0):
    """Draw truck `key` with viewBox (400,380) at frame (cx, gy); k = pixels per viewBox unit.
    act/p animate the moving part (p 0..1)."""
    V = lambda vx, vy: (cx + (vx - 400) * k, gy + (vy - 380) * k)
    d = ImageDraw.Draw(frame)
    lw = max(3, int(6 * k))
    if key == "firetruck":
        item(frame, "firetruck", cx, gy - 160 * k, 760 * k)
        return
    # parts drawn BEHIND the body
    if key == "crane":
        bx, by = V(640, 210)
        ang = math.radians(-160 + 25 * p)
        L = 470 * k
        tx, ty = bx + L * math.cos(ang), by + L * math.sin(ang)
        d.line((bx, by, tx, ty), fill=INK, width=int(46 * k) + 6)
        d.line((bx, by, tx, ty), fill=(255, 159, 28), width=int(46 * k))
        hook_y = gy - (40 + 330 * p) * k
        d.line((tx, ty, tx, hook_y), fill=INK, width=max(2, int(5 * k)))
        item(frame, "slide", tx, hook_y + 90 * k, 200 * k)
    key2 = (key, round(k, 3))
    if key2 not in G["tsz"]:
        if len(G["tsz"]) > 60:
            G["tsz"].clear()
        im = G["truck"][key]
        G["tsz"][key2] = im.resize((max(2, int(800 * k)), max(2, int(400 * k))), Image.LANCZOS)
    im = G["tsz"][key2]
    frame.alpha_composite(im, (int(cx - 400 * k), int(gy - 380 * k)))
    d = ImageDraw.Draw(frame)
    for wx, wy, r in WHEELS.get(key, []):
        x, y = V(wx, wy)
        wheel(d, x, y, r * k, spin)
    if key == "excavator":
        P = V(230, 220)
        a1 = math.radians(205 + 30 * p)
        a2 = math.radians(115 - 45 * p)
        J = (P[0] + 270 * k * math.cos(a1), P[1] + 270 * k * math.sin(a1))
        B = (J[0] + 210 * k * math.cos(a2), J[1] + 210 * k * math.sin(a2))
        for a, b in ((P, J), (J, B)):
            d.line((a, b), fill=INK, width=int(44 * k) + 6)
            d.line((a, b), fill=YEL, width=int(44 * k))
        for c in (P, J):
            d.ellipse((c[0] - 16 * k, c[1] - 16 * k, c[0] + 16 * k, c[1] + 16 * k), fill=(74, 79, 92), outline=INK, width=lw)
        ba = a2 + math.radians(60 - 90 * p)
        pts = [B, (B[0] + 95 * k * math.cos(ba), B[1] + 95 * k * math.sin(ba)),
               (B[0] + 95 * k * math.cos(ba + 1.2), B[1] + 95 * k * math.sin(ba + 1.2)), (B[0] + 40 * k * math.cos(ba + 1.9), B[1] + 40 * k * math.sin(ba + 1.9))]
        d.polygon(pts, fill=YDK, outline=INK, width=lw)
        if p > 0.6:
            d.ellipse((pts[1][0] - 30 * k, pts[1][1] - 20 * k, pts[1][0] + 30 * k, pts[1][1] + 20 * k), fill=(160, 112, 63))
    elif key == "dumptruck":
        piv = V(740, 300)
        th = math.radians(38 * p)
        def rot(vx, vy):
            dx, dy = (vx - 740) * k, (vy - 300) * k
            return (piv[0] + dx * math.cos(th) - dy * math.sin(th), piv[1] + dx * math.sin(th) + dy * math.cos(th))
        bed = [rot(270, 300), rot(740, 300), rot(760, 170), rot(250, 170)]
        d.polygon(bed, fill=(255, 159, 28), outline=INK, width=lw)
        d.line((rot(300, 235), rot(720, 235)), fill=(224, 130, 20), width=max(2, int(10 * k)))
        if p < 0.5:
            pile = [rot(290, 172), rot(400, 120), rot(520, 105), rot(640, 125), rot(730, 172)]
            d.polygon(pile, fill=(160, 112, 63), outline=INK, width=lw)
    elif key == "mixer":
        c = V(480, 215)
        rx, ry = 230 * k, 95 * k
        d.ellipse((c[0] - rx, c[1] - ry, c[0] + rx, c[1] + ry), fill=(230, 232, 240), outline=INK, width=lw)
        for j in range(5):
            ph = (spin * 0.5 + j / 5) % 1
            x = c[0] - rx + 2 * rx * ph
            hh = ry * math.sqrt(max(0, 1 - ((x - c[0]) / rx) ** 2))
            d.line((x - 20 * k, c[1] - hh, x + 20 * k, c[1] + hh), fill=(255, 107, 107), width=max(3, int(14 * k)))
    elif key == "roller":
        x, y = V(150, 310)
        r = 70 * k
        d.ellipse((x - r, y - r, x + r, y + r), fill=(176, 180, 192), outline=INK, width=lw)
        for j in range(6):
            a = spin + j * math.pi / 3
            d.line((x + r * 0.2 * math.cos(a), y + r * 0.2 * math.sin(a), x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a)), fill=(120, 124, 136), width=max(2, int(6 * k)))
    elif key == "bulldozer":
        pass


def drive_x(t, t_in, x_to, d=1.0, x_from=None):
    x_from = W + 700 if x_from is None else x_from
    q = min(1, max(0, (t - t_in) / d))
    return x_from + (x_to - x_from) * ease_io(q), q


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 20 * abs(math.cos(t * 5 + ph)) + 4
            d.rectangle((x - w / 2, y - 10, x + w / 2, y + 10), fill=col)


def dirt_burst(frame, cx, cy, q, scale=1.0):
    if not 0 <= q < 1.4:
        return
    d = ImageDraw.Draw(frame)
    for dx, sp, r in G["dirt"]:
        x = cx + dx * 500 * scale * q
        y = cy - sp * 700 * scale * q + 900 * scale * q * q
        d.ellipse((x - r * scale, y - r * scale, x + r * scale, y + r * scale), fill=(160, 112, 63), outline=(122, 82, 44))


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


def act_p(act, t, t0):
    """0..1 motion for a truck action starting at t0"""
    q = t - t0
    if q < 0:
        return 0.0
    if act == "dig":
        return 0.5 - 0.5 * math.cos(min(q, 3.0) * 2 * math.pi / 1.5)
    if act in ("dump", "lift"):
        return ease_io(min(1, q / 1.4))
    return 0.0


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    q = t - s["smash_t"]
    shake = 14 * math.sin(t * 60) * max(0, 1 - q / 0.5) if 0 <= q < 0.5 else 0
    p = min(1, max(0, (t - s["engine_t"]) / 0.5)) if t < s["smash_t"] + 0.2 else max(0, 1 - (t - s["smash_t"] - 0.2) / 1.0)
    p = 0.15 + 0.85 * p if t < s["title_t"] else 0.5 - 0.5 * math.cos((t - s["title_t"]) * 2)
    truck(frame, "excavator", 1150 + shake, 960, 1.15, t, p=p)
    dirt_burst(frame, 760 + shake, 960, q, 1.2)
    if t >= s["title_t"]:
        k = t - s["title_t"]
        rt(frame, 960, 180, "BIG TRUCKS!", int(220 * ease_back(k / 0.35)), maxw=1500)
        if t >= s["kids_t"] - 1.0:
            side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(230, 1690), scale=0.36)
        if k < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k / 0.3)))))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    for j, key in enumerate(("excavator", "dumptruck", "mixer")):
        truck(frame, key, 420 + j * 540, 900, 0.5, t, spin=t * 3, p=0.5 + 0.5 * math.sin(t * 2))
    rt(frame, 960, 380, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1600)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.3)


def scene_team(frame, s, t):
    key = s["key"]
    x, q = drive_x(t, s["in_t"], 1060)
    p = act_p(s["act"], t, s["act_t"])
    spin = -(x - 1060) / 40 + ((t - s["act_t"]) * 6 if s["act"] in ("spin", "roll") and t >= s["act_t"] else 0)
    if s["act"] == "push" and t >= s["act_t"]:
        x -= 160 * min(1, (t - s["act_t"]) / 1.6)
        item(frame, "dirt", x - 470, 900, 280)
    if s["act"] == "roll" and t >= s["act_t"]:
        x -= 200 * min(1, (t - s["act_t"]) / 1.8)
    bob = 4 * math.sin(t * 20) if q < 1 else 0
    truck(frame, key, x, 930 + bob, 1.05, t, p=p, spin=spin)
    if s["act"] == "dig" and t >= s["act_t"]:
        dirt_burst(frame, x - 420, 930, (t - s["act_t"]) % 1.5, 0.6)
    badge(frame, 160, 90, f"{s['num']}/6")
    if t >= s["name_t"]:
        word(frame, NAMES[key] + "!", t, s["name_t"], size=130, col=(255, 159, 28))
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


STEP_ICON = ["excavator", "dumptruck", "bulldozer", "mixer", "crane", "roller"]


def scene_build(frame, s, t):
    k = s["step"]
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((420, 30, 1500, 150), radius=30, fill=(255, 255, 255, 200), outline=INK, width=5)
    for i, key in enumerate(STEP_ICON):
        x = 510 + i * 180
        truck(frame, key, x, 135, 0.18, t)
        if i < k or (i == k and t >= s["act_t"] + 1.6):
            d.line((x - 30, 70, x - 5, 100, x + 40, 45), fill=(59, 193, 74), width=12, joint="curve")
    gx = 640
    if k <= 1:
        pile = 1.0 if k == 1 else min(1, max(0, (t - s["act_t"]) / 3.0))
        if k == 1:
            pile = max(0, 1 - (t - s["act_t"]) / 1.2)
        if pile > 0.02:
            item(frame, "dirt", gx, 900 - 120 * pile, 320 * pile)
    if k == 3:
        r = 300 * min(1, max(0, (t - s["act_t"]) / 2.5))
        d.ellipse((gx - r, 930 - r * 0.15, gx + r, 930 + r * 0.15), fill=(176, 180, 192, 255), outline=INK, width=5)
    if k == 5:
        d.rectangle((0, 935, 1920, 990), fill=(150, 154, 166))
        x_r = 1500 - 900 * min(1, max(0, (t - s["act_t"]) / 2.5))
        d.rectangle((x_r, 935, 1920, 990), fill=(120, 124, 136))
    x, q = drive_x(t, s["in_t"], 1180)
    p = act_p(s["act"], t, s["act_t"])
    spin = -(x - 1180) / 40 + ((t - s["act_t"]) * 6 if s["act"] in ("spin", "roll") and t >= s["act_t"] else 0)
    if s["act"] == "push" and t >= s["act_t"]:
        x -= 200 * min(1, (t - s["act_t"]) / 1.6)
    if s["act"] == "roll" and t >= s["act_t"]:
        x -= 500 * min(1, (t - s["act_t"]) / 2.5)
    truck(frame, s["key"], x, 930, 0.95, t, p=p, spin=spin)
    if s["act"] == "dig" and t >= s["act_t"]:
        dirt_burst(frame, x - 380, 930, (t - s["act_t"]) % 1.5, 0.5)
    if s["act"] == "spin" and t >= s["act_t"]:
        d.line((x - 240, 840, gx + 40, 920), fill=(150, 154, 166), width=26)
    side_kids(frame, t, xs=(150, 1800), scale=0.24)


def scene_playground(frame, s, t):
    q = t - s["reveal_t"]
    item(frame, "slide", 620, 640, 420 * ease_back(q / 0.5))
    item(frame, "swing", 1260, 650, 400 * ease_back((q - 0.2) / 0.5))
    for i, key in enumerate(("excavator", "dumptruck", "roller")):
        truck(frame, key, 330 + i * 640, 1060, 0.32, t)
    for n, x in (("gul", 860), ("misheal", 1060)):
        body(frame, n, t, "excited", x, feet=930, scale=0.4, hop=40 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    confetti(frame, t, s["reveal_t"])
    word(frame, "TA-DA! PLAYGROUND!", t, s["reveal_t"], size=120)


def scene_job(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 140, s["q"], int(80 * ease_back(q / 0.35)), maxw=1600)
    d = ImageDraw.Draw(frame, "RGBA")
    for i, key in enumerate(s["opts"]):
        x = 420 + i * 540
        good = t >= s["answer_t"] and key == s["ans"]
        dim = t >= s["answer_t"] and not good
        d.rounded_rectangle((x - 240, 420, x + 240, 760), radius=30, fill=(255, 255, 255, 120 if dim else 210),
                            outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        truck(frame, key, x, 700 - (25 * abs(math.sin((t - s["answer_t"]) * 6)) if good else 0), 0.5 * ease_back((q - i * 0.1) / 0.35), t, spin=t * 2,
              p=0.5 + 0.5 * math.sin(t * 2.5) if good else 0)
        if good:
            rt(frame, x, 810, NAMES[key] + "!", 60, colour=(59, 193, 74), maxw=470)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_city(frame, s, t):
    key = s["key"]
    x, q = drive_x(t, s["in_t"], 960)
    jump = 0
    if s["act"] == "jump" and t >= s["act_t"]:
        jq = (t - s["act_t"]) % 2.0
        jump = 280 * math.sin(min(1, jq / 1.0) * math.pi) if jq < 1.0 else 0
    shake = 6 * math.sin(t * 40) if s["act"] == "crunch" and 0 <= t - s["act_t"] < 1.0 else 0
    truck(frame, key, x + shake, 960 - jump, 0.95, t, spin=-(x - 960) / 40)
    if s["act"] == "siren" and t >= s["act_t"]:
        d = ImageDraw.Draw(frame, "RGBA")
        on = int(t * 6) % 2
        for j, col in enumerate(((255, 40, 40), (40, 120, 255))):
            a = 230 if (j == on) else 60
            d.ellipse((x - 120 + j * 120 - 40, 520, x - 120 + j * 120 + 40, 600), fill=col + (a,))
    word(frame, NAMES[key] + "!", t, s["in_t"] + 0.6, size=130, col=(255, 159, 28))
    side_kids(frame, t, xs=(130, 1790), scale=0.26, feet=760)


def scene_count(frame, s, t):
    keys = ["excavator", "dumptruck", "bulldozer", "mixer", "crane", "roller", "garbage", "towtruck", "monster", "firetruck"]
    n = sum(1 for c in s["cts"] if t >= c)
    for i in range(n):
        x0 = 140 + (i % 5) * 410
        gy = 690 if i < 5 else 1010
        x, q = drive_x(t, s["cts"][i], x0, 0.5)
        truck(frame, keys[i], x, gy, 0.42, t, spin=-(x - x0) / 30)
        if q >= 1:
            rt(frame, x0, gy - 230, str(i + 1), 80, colour=RAINBOW[i % 6])
    word(frame, f"{n} TRUCKS!" if n else "COUNT THE TRUCKS!", t, s["cts"][n - 1] if n else s["t0"], size=120)


def scene_sound(frame, s, t):
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.6:
            for j in range(3):
                r = 140 + 110 * j + 140 * (q % 0.8)
                d.arc((960 - r, 480 - r, 960 + r, 480 + r), -50, 50, fill=(255, 255, 255, 210), width=12)
                d.arc((960 - r, 480 - r, 960 + r, 480 + r), 130, 230, fill=(255, 255, 255, 210), width=12)
        rt(frame, 960, 480, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], size=130)
    else:
        x, q = drive_x(t, s["answer_t"], 960, 0.7)
        truck(frame, s["key"], x, 960, 0.9, t, spin=-(x - 960) / 40)
        word(frame, NAMES[s["key"]] + "!", t, s["answer_t"], size=130, col=(255, 159, 28))
    side_kids(frame, t, xs=(130, 1790), scale=0.26, feet=760)


def scene_safety(frame, s, t):
    x = W + 600 - ((t - s["t0"]) * 260) % (W + 1400)
    truck(frame, "dumptruck", x, 1000, 0.75, t, spin=t * 4)
    wave = t >= s["s3"]
    for n, xx in (("gul", 880), ("misheal", 1040)):
        body(frame, n, t, "happy", xx, feet=770, scale=0.36, wave=wave, hop=10 * abs(math.sin(t * 5)) if wave else 0)
    if t >= s["s3"]:
        word(frame, "WAVE HELLO!", t, s["s3"], size=130)
    elif t >= s["s2"]:
        word(frame, "HOLD A GROWN-UP'S HAND!", t, s["s2"], size=100, col=(255, 77, 109), maxw=1700)
    else:
        word(frame, "STAY SAFE!", t, s["t0"], size=130, col=(255, 77, 109))


def scene_dance(frame, s, t):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv = s["move"]
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, dx = 0, 0, 0
        if mv == "dig":
            hop = 40 * abs(math.sin(q * 5 + i))
            rot = 8 * math.sin(q * 5)
        elif mv == "push":
            dx = 40 * math.sin(q * 4)
            rot = -6
        elif mv == "spin":
            rot = 10 * math.sin(q * 8 + i)
        elif mv == "lift":
            hop = 60 * abs(math.sin(q * 3 + i))
        elif mv == "back":
            dx = 50 * math.sin(q * 3)
        elif mv == "honk":
            hop = 90 * abs(math.sin(q * 5 + i))
        body(frame, n, t, "excited" if mv in ("honk", "lift") else "happy", x + dx, scale=0.52, hop=hop, rot=rot, wave=True)
    word(frame, s["word"], t, s["t0"], size=120, col=(255, 159, 28))


def scene_quiz(frame, s, t):
    q = t - s["t0"]
    rt(frame, 960, 120, s["q"], int(78 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        v = s["vis"]
        if v in G["truck"]:
            truck(frame, v, 960, 760, 0.7 * k, t, p=0.5 + 0.5 * math.sin(t * 2.5), spin=t * 3)
        else:
            item(frame, v, 960, 560, 360 * k)
        stars_ring(frame, 960, 560, 400, 260, t, n=8, r=20)
        side_kids(frame, t, "happy", scale=0.28, xs=(130, 1790))
    else:
        rt(frame, 960, 560, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t, scale=0.28, xs=(130, 1790))


def scene_outro(frame, s, t):
    item(frame, "slide", 380, 640, 330)
    item(frame, "swing", 1560, 650, 320)
    for i, key in enumerate(("excavator", "bulldozer", "mixer")):
        truck(frame, key, 420 + i * 540, 1060, 0.38, t, spin=t * 3, p=0.5 + 0.5 * math.sin(t * 2 + i))
    for n, x in (("gul", 820), ("misheal", 1100)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, feet=920, scale=0.44, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE! BEEP BEEP!", int(140 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 140, "YOUR FAVOURITE TRUCK?", int(110 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)


COLRGB = {"yellow": (255, 194, 26), "red": (232, 53, 46), "green": (59, 181, 74), "blue": (46, 140, 255), "purple": (155, 93, 229), "orange": (255, 159, 28)}


def scene_part(frame, s, t):
    k = 1.15
    cx, gy = 1060, 900
    truck(frame, s["key"], cx, gy, k, t, p=1.0 if s["key"] == "crane" else 0.4, spin=0)
    vx, vy = s["xy"]
    if s["key"] == "excavator" and s["part"] == "bucket":
        vx, vy = -40, 330
    px, py = cx + (vx - 400) * k, gy + (vy - 380) * k
    d = ImageDraw.Draw(frame)
    q = t - s["t0"]
    r = 85 + 10 * math.sin(q * 8)
    d.ellipse((px - r, py - r, px + r, py + r), outline=(255, 77, 109), width=12)
    lx, ly = px, py - 260 if py > 500 else py + 260
    d.line((lx, ly + (60 if ly < py else -60), px, py + (-r if ly < py else r)), fill=(255, 77, 109), width=10)
    rt(frame, max(260, min(1660, lx)), ly, s["part"].upper() + "!", int(100 * ease_back(q / 0.3)), colour=(255, 77, 109), maxw=600)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def pothole(frame, fill=0.0, smooth=0.0):
    d = ImageDraw.Draw(frame)
    cx, cy = 820, 900
    if fill < 1:
        d.ellipse((cx - 170, cy - 40, cx + 170, cy + 40), fill=(40, 40, 46), outline=INK, width=5)
    if fill > 0:
        r = 170 * min(1, fill)
        d.ellipse((cx - r, cy - 40 * min(1, fill), cx + r, cy + 40 * min(1, fill)), fill=(140, 120, 100) if smooth < 1 else (92, 96, 112), outline=INK, width=4)
        if smooth >= 1:
            d.rectangle((cx - 170, cy - 8, cx + 170, cy + 8), fill=(92, 96, 112))


def scene_fix(frame, s, t):
    k = s["step"]
    q = t - s["act_t"]
    fill = 0 if k == 0 else (min(1, max(0, q / 1.2)) if k == 1 else 1)
    smooth = 1 if (k == 2 and q > 1.8) else 0
    pothole(frame, fill, smooth)
    x, _ = drive_x(t, s["in_t"], 1260)
    p = act_p(s["act"], t, s["act_t"])
    spin = -(x - 1260) / 40 + (q * 6 if s["act"] == "roll" and q > 0 else 0)
    if s["act"] == "roll" and q > 0:
        x -= 420 * min(1, q / 2.0)
    truck(frame, s["key"], x, 960, 0.85, t, p=p, spin=spin)
    if s["act"] == "dig" and q >= 0:
        dirt_burst(frame, x - 350, 920, q % 1.5, 0.5)
    word(frame, "FIX THE ROAD!", t, s["t0"], size=120, col=(255, 159, 28))
    side_kids(frame, t, xs=(130, 1790), scale=0.26, feet=760)


def scene_fixdone(frame, s, t):
    pothole(frame, 1, 1)
    x = W + 300 - ((t - s["t0"]) * 520) % (W + 900)
    item(frame, "car", x, 880, 300)
    for n, xx in (("gul", 880), ("misheal", 1040)):
        body(frame, n, t, "excited", xx, feet=770, scale=0.36, wave=True, hop=20 * abs(math.sin(t * 5)))
    stars_ring(frame, 960, 620, 420, 200, t, n=8)
    word(frame, "ROAD FIXED!", t, s["done_t"], size=140, col=(59, 193, 74))


def scene_colour(frame, s, t):
    q = t - s["t0"]
    truck(frame, s["key"], 960, 920, 0.9 * ease_back(q / 0.4) + 0.01, t, spin=t * 2)
    if t >= s["answer_t"]:
        word(frame, s["col"].upper() + "!", t, s["answer_t"], size=170, col=COLRGB[s["col"]])
    else:
        word(frame, "WHAT COLOUR?", t, s["t0"], size=120)
    side_kids(frame, t, xs=(130, 1790), scale=0.26, feet=760)


def scene_wheels(frame, s, t):
    key = s["key"]
    k = 1.05
    cx, gy = 980, 900
    truck(frame, key, cx, gy, k, t, spin=t * 2)
    if t >= s["answer_t"]:
        d = ImageDraw.Draw(frame)
        for i, (wx, wy, r) in enumerate(WHEELS[key]):
            x, y = cx + (wx - 400) * k, gy + (wy - 380) * k
            q = t - s["answer_t"] - i * 0.3
            if q < 0:
                continue
            d.ellipse((x - r * k - 14, y - r * k - 14, x + r * k + 14, y + r * k + 14), outline=(59, 193, 74), width=10)
            rt(frame, x, y - r * k - 70, str(i + 1), int(90 * ease_back(q / 0.25)), colour=RAINBOW[i % 6])
        word(frame, f"{s['n']} WHEEL{'S' if s['n'] > 1 else ''}!", t, s["answer_t"], size=140, col=(59, 193, 74))
    else:
        word(frame, "HOW MANY WHEELS?", t, s["t0"], size=120)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_bigsmall(frame, s, t):
    q = t - s["t0"]
    d = ImageDraw.Draw(frame, "RGBA")
    for i, key in enumerate(s["pair"]):
        x = 620 + i * 680
        good = t >= s["answer_t"] and i == s["ans"]
        d.rounded_rectangle((x - 300, 360, x + 300, 860), radius=30, fill=(255, 255, 255, 190), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        if key in G["truck"]:
            truck(frame, key, x, 820, 0.65, t, spin=t * 2)
        else:
            item(frame, key, x, 760, 160 if key == "toytruck" else 230)
    word(frame, "BIG OR SMALL?", t, s["t0"], size=120)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_treasure(frame, s, t):
    p = 0.5 - 0.5 * math.cos((t - s["dig_t"]) * 2 * math.pi / 1.5) if t < s["find_t"] else 0.15
    truck(frame, "excavator", 1250, 930, 0.95, t, p=p)
    if t < s["find_t"]:
        dirt_burst(frame, 860, 930, (t - s["dig_t"]) % 1.5, 0.5)
        item(frame, "dirt", 620, 860, 300)
        rt(frame, 620, 640, "?", int(140 + 12 * math.sin(t * 6)), colour=(255, 255, 255))
    else:
        k = t - s["find_t"]
        item(frame, "dirt", 620, 900, 260)
        item(frame, s["key"], 620, 700 - 60 * ease_back(min(1, k / 0.5)), 260 * ease_back(min(1, k / 0.4)))
        stars_ring(frame, 620, 680, 220, 160, t, n=8, r=18)
        word(frame, s["key"].upper() + "!", t, s["find_t"], size=140, col=(255, 159, 28))
    if t < s["find_t"]:
        word(frame, "DIG FOR TREASURE!", t, s["t0"], size=110)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_load(frame, s, t):
    go = t >= s["go_t"]
    x = 1000 - (900 * min(1, (t - s["go_t"]) / 2.0) ** 2 if go else 0)
    truck(frame, "dumptruck", x, 930, 0.95, t, spin=(x - 1000) / 40)
    n = sum(1 for l in s["lts"] if t >= l + 0.3)
    k = 0.95
    for i in range(n):
        rx, ry = x + (380 + i * 75 - 400) * k, 930 + (150 - 380) * k - (i % 2) * 40
        item(frame, "rock", rx, ry, 120)
        rt(frame, rx, ry - 110, str(i + 1), 70, colour=RAINBOW[i % 6])
    for i, l in enumerate(s["lts"]):
        q = t - l
        if 0 <= q < 0.3:
            item(frame, "rock", 640 + (x + (380 + i * 75 - 400) * k - 640) * q / 0.3, 300 + 200 * q / 0.3, 140)
    word(frame, f"{n} ROCKS!" if n else "LOAD THE TRUCK!", t, s["lts"][n - 1] + 0.3 if n else s["t0"], size=120)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_opps(frame, s, t):
    key = s["key"]
    a_on = t >= s["a_t"]
    b_on = t >= s["b_t"]
    if key == "crane":
        p = 1.0 if a_on and not b_on else (0.0 if b_on else 0.5)
        truck(frame, "crane", 1100, 930, 0.95, t, p=p)
    elif key == "dumptruck":
        p = 0.0 if not b_on else min(1, (t - s["b_t"]) / 1.2)
        truck(frame, "dumptruck", 1060, 930, 0.95, t, p=p)
        if b_on:
            item(frame, "dirt", 1600, 880, 260 * min(1, (t - s["b_t"]) / 1.2))
    else:
        xm = W + 400 - ((t - s["a_t"]) * 1400) % (W + 1600) if a_on else W + 600
        truck(frame, "monster", xm, 690, 0.5, t, spin=t * 12)
        xr = 1700 - (t - s["t0"]) * 60
        truck(frame, "roller", xr, 1010, 0.5, t, spin=t * 2)
    if b_on:
        word(frame, s["w2"].upper() + "!", t, s["b_t"], size=150, col=(46, 140, 255))
    elif a_on:
        word(frame, s["w1"].upper() + "!", t, s["a_t"], size=150, col=(255, 107, 107))
    else:
        word(frame, "OPPOSITES!", t, s["t0"], size=130)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


SCENES = {"intro": scene_intro, "title": scene_title, "team": scene_team, "build": scene_build, "playground": scene_playground, "job": scene_job,
          "city": scene_city, "count": scene_count, "sound": scene_sound, "safety": scene_safety, "dance": scene_dance, "quiz": scene_quiz,
          "outro": scene_outro, "part": scene_part, "fix": scene_fix, "fixdone": scene_fixdone, "colour": scene_colour,
          "wheels": scene_wheels, "bigsmall": scene_bigsmall, "treasure": scene_treasure, "load": scene_load, "opps": scene_opps}


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
    dst = OUT / f"Excavator and Trucks for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=0", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
