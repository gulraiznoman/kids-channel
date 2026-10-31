"""Animate L23 "Bugs & Insects for Kids".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW

A23 = HERE / "art"
BUGS = ["bee", "ladybug", "ant", "butterfly", "caterpillar", "grasshopper", "dragonfly", "firefly", "beetle", "spider", "worm", "snail"]
ART = {k: A23 / f"item_{k}.png" for k in ("bee", "ladybug", "ant", "grasshopper", "dragonfly", "firefly", "beetle", "spider", "worm", "snail",
                                           "magnifier", "hive", "honey", "web", "soil")}
ART.update({f"sil_{k}": A23 / f"item_sil_{k}.png" for k in BUGS})
ART.update({"butterfly": ROOT / "long09-eggs/art/item_butterfly.png", "caterpillar": ROOT / "long09-eggs/art/item_caterpillar.png",
            "flower": ROOT / "long05-body-parts/art/item_flower.png", "leaf": ROOT / "long11-bath/art/item_leaf.png",
            "egg": ROOT / "long06-dinosaurs/art/item_egg.png"})


def night():
    im = Image.open(ROOT / "long05-body-parts/art/bg_park.png").convert("RGBA")
    im.alpha_composite(Image.new("RGBA", im.size, (10, 15, 60, 185)))
    return im


BGS = {"patch": ROOT / "long03-fruits-veg/art/bg_patch.png", "park": ROOT / "long05-body-parts/art/bg_park.png", "tree": ROOT / "long09-eggs/art/bg_tree.png",
       "pond": ROOT / "long09-eggs/art/bg_pond.png", "underground": A23 / "bg_underground.png", "night": night}
COLRGB = {"red": (232, 53, 46), "yellow": (245, 200, 30), "green": (59, 170, 74), "brown": (140, 85, 45), "pink": (240, 100, 150)}


def scene_intro(frame, s, t):
    q = t - s["sweep_t"]
    for j, k in enumerate(("ladybug", "bee", "butterfly", "ant", "snail", "grasshopper")):
        x, y = 330 + j * 250, 520 + 120 * math.sin(j * 2.1)
        item(frame, k, x, y + 8 * math.sin(t * 3 + j), 170)
    mx = 300 + (q * 700) % 1320
    item(frame, "magnifier", mx, 520 + 90 * math.sin(q * 2), 300)
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(170, 1750), scale=0.34)
        rt(frame, 960, 140, "BUGS AND INSECTS!", int(150 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)


def scene_hunt(frame, s, t):
    key = s["key"]
    if t < s["reveal_t"]:
        item(frame, "sil_" + key, 960, 560 + 8 * math.sin(t * 3), 520)
        item(frame, "magnifier", 1420 + 80 * math.cos(t * 2), 380 + 60 * math.sin(t * 2), 280)
        rt(frame, 960, 150, "WHO IS IT?", int(120 * ease_back((t - s["t0"]) / 0.3)), colour=(255, 255, 255))
    else:
        q = t - s["reveal_t"]
        item(frame, key, 960, 570 + 10 * math.sin(t * 4), 560 * ease_back(q / 0.4), rot=4 * math.sin(t * 3))
        if t >= s["fact_t"]:
            word(frame, s["verb"], t, s["fact_t"], y=150, size=130)
        else:
            word(frame, s["name"] + "!", t, s["reveal_t"], y=150, size=130)
            stars_ring(frame, 960, 570, 380, 310, t, n=8, r=20)
    badge(frame, 160, 90, f"{s['num']}/12", (255, 140, 26))
    side_kids(frame, t, "excited" if t >= s["reveal_t"] else None, xs=(190, 1730), scale=0.32)


ANT = (960, 560, 980)
LEGS = [(90, 350), (175, 365), (315, 350), (85, 170), (180, 120), (320, 170)]


def ant_pt(sx, sy):
    cx, cy, S = ANT
    return cx + (sx - 197) * S / 367, cy + (sy - 228) * S / 367


def scene_anatomy(frame, s, t):
    cx, cy, S = ANT
    item(frame, "ant", cx, cy, S)
    d = ImageDraw.Draw(frame)
    n = sum(1 for x in s["ts"] if t >= x)
    spots = [(295, 205, 110, "HEAD", RAINBOW[0]), (195, 230, 75, "MIDDLE", RAINBOW[2]), (85, 235, 110, "BACK", RAINBOW[4])]
    if t < s["legs_say"]:
        if n:
            sx, sy, r0, lab, col = spots[n - 1]
            x, y = ant_pt(sx, sy)
            r = r0 * S / 367 + 8 * math.sin(t * 6)
            d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=14)
            word(frame, lab + "!", t, s["ts"][n - 1], size=130, col=col)
        else:
            word(frame, "3 BODY PARTS!", t, s["t0"], size=120)
    elif t < s["ant_t"]:
        m = sum(1 for x in s["legs"] if t >= x)
        for i in range(m):
            x, y = ant_pt(*LEGS[i])
            d.ellipse((x - 40, y - 40, x + 40, y + 40), fill=(255, 255, 255), outline=(255, 77, 109), width=7)
            rt(frame, x, y, str(i + 1), 56, colour=(255, 77, 109))
        word(frame, f"{m} LEGS!" if m else "6 LEGS!", t, s["legs"][m - 1] if m else s["legs_say"], size=130)
    elif t < s["sum_t"]:
        for sx, sy in ((285, 148), (320, 148)):
            x, y = ant_pt(sx, sy - 40)
            d.ellipse((x - 80, y - 80, x + 80, y + 80), outline=(255, 210, 40), width=12)
        word(frame, "2 ANTENNAS!", t, s["ant_t"], size=130)
    else:
        rt(frame, 960, 150, "3 PARTS + 6 LEGS = INSECT!", int(110 * ease_back((t - s["sum_t"]) / 0.3)), maxw=1700)


def scene_isnot(frame, s, t):
    rt(frame, 960, 150, s["q"], int(90 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)
    item(frame, s["key"], 960, 540, 400)
    if t >= s["answer_t"]:
        d = ImageDraw.Draw(frame)
        k = ease_back((t - s["answer_t"]) / 0.3)
        if s["good"]:
            d.line((1180, 520, 1280, 620, 1480, 380), fill=(59, 193, 74), width=int(40 * k) + 1, joint="curve")
            word(frame, "INSECT!", t, s["answer_t"], y=860, size=140, col=(59, 193, 74))
        else:
            r = 240 * k
            d.ellipse((960 - r, 540 - r, 960 + r, 540 + r), outline=(232, 53, 46), width=24)
            d.line((960 - r * 0.7, 540 + r * 0.7, 960 + r * 0.7, 540 - r * 0.7), fill=(232, 53, 46), width=24)
            word(frame, "NOT AN INSECT!", t, s["answer_t"], y=860, size=120, col=(232, 53, 46))
    side_kids(frame, t, xs=(170, 1750))


def scene_spots(frame, s, t):
    n = sum(1 for x in s["cts"] if t >= x)
    d = ImageDraw.Draw(frame)
    cx, cy, r = 960, 590, 340
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(232, 53, 46), outline=INK, width=9)
    d.line((cx, cy - r, cx, cy + r), fill=INK, width=9)
    d.pieslice((cx - 240, cy - r - 120, cx + 240, cy - r + 200), 0, 180, fill=(50, 50, 60), outline=INK, width=7)
    for ex in (-80, 80):
        d.ellipse((cx + ex - 26, cy - r + 50, cx + ex + 26, cy - r + 102), fill=(255, 255, 255))
        d.ellipse((cx + ex - 11, cy - r + 62, cx + ex + 11, cy - r + 84), fill=INK)
    pos = [(-170, 40), (170, 40), (-180, 200), (180, 200), (-90, 110), (90, 110), (-70, 260)]
    for i in range(n):
        x, y = pos[i]
        k = ease_back((t - s["cts"][i]) / 0.3)
        d.ellipse((cx + x - 52 * k, cy + y - 52 * k - 40, cx + x + 52 * k, cy + y + 52 * k - 40), fill=(45, 45, 55))
    if n:
        rt(frame, 1560, 500, str(n), int(240 * ease_back((t - s["cts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    word(frame, f"{s['n']} SPOTS!" if t >= s["sum_t"] else "COUNT THE SPOTS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(200, 1740), scale=0.28)


def scene_honey(frame, s, t):
    key = s["key"]
    q = min(1, (t - s["t0"]) / 2.2)
    if key == "jar":
        item(frame, "honey", 960, 560, 520 * ease_back((t - s["t0"]) / 0.4))
        confetti(frame, t, s["t0"])
    else:
        item(frame, "flower", 460, 620, 460)
        item(frame, "hive", 1440, 480, 460)
        if key == "fly":
            x, y = 1200 - 740 * ease_io(q), 480 + 40 * math.sin(t * 6)
        elif key == "sip":
            x, y = 460, 490 + 8 * math.sin(t * 8)
        elif key == "home":
            x, y = 460 + 860 * ease_io(q), 500 + 40 * math.sin(t * 6)
        else:
            x, y = 1320, 520
            for j in range(4):
                item(frame, "bee", 1440 + 300 * math.cos(t * 2 + j * 1.6), 480 + 220 * math.sin(t * 2 + j * 1.6), 110)
        item(frame, "bee", x, y, 200, flip=key == "fly")
    badge(frame, 160, 90, f"STEP {s['num']}", (245, 170, 30))
    word(frame, {"fly": "FLY TO A FLOWER!", "sip": "SIP THE NECTAR!", "home": "BACK TO THE HIVE!", "make": "MAKE HONEY!", "jar": "HONEY!"}[key], t, s["say_t"], size=110)


TUNNEL = [(960, 300), (960, 440), (860, 500), (420, 500)]


def on_path(f):
    pts, seg = TUNNEL, [440 - 300, 117, 440]
    L = sum(seg) * f
    for i, s0 in enumerate(seg):
        if L <= s0:
            k = L / s0
            return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k
        L -= s0
    return pts[-1]


def scene_march(frame, s, t):
    n = sum(1 for x in s["cts"] if t >= x)
    for i in range(n):
        f = min(1, (t - s["cts"][i]) * 0.14)
        x, y = on_path(1 - i * 0.09 if f >= 1 else f)
        item(frame, "ant", x, y, 86, flip=True)
    if n:
        rt(frame, 1450, 560, str(n), int(210 * ease_back((t - s["cts"][n - 1]) / 0.2)), colour=(255, 230, 120))
    rt(frame, 960, 90, f"{n} ANTS!" if n else "COUNT THE ANTS!", 100)


def scene_room(frame, s, t):
    d = ImageDraw.Draw(frame)
    x, y, lab = {"food": (360, 500, "FOOD ROOM!"), "baby": (1620, 520, "BABY ROOM!"), "queen": (960, 860, "QUEEN ANT!")}[s["room"]]
    r = 170 + 8 * math.sin(t * 5)
    d.ellipse((x - r, y - r * 0.68, x + r, y + r * 0.68), outline=(255, 215, 60), width=12)
    if s["room"] == "food":
        for j in range(3):
            item(frame, "leaf", x - 60 + j * 60, y, 90, rot=j * 30)
    elif s["room"] == "baby":
        for j in range(5):
            d.ellipse((x - 90 + j * 38, y - 16, x - 62 + j * 38, y + 22), fill=(255, 250, 235), outline=INK, width=3)
    else:
        item(frame, "ant", x, y, 200, flip=True)
        pts = [(x + 45, y - 100), (x + 60, y - 60), (x + 120, y - 60), (x + 135, y - 100), (x + 110, y - 80), (x + 90, y - 110), (x + 70, y - 80)]
        d.polygon(pts, fill=(255, 215, 60), outline=INK)
    rt(frame, 960, 90, lab, int(110 * ease_back((t - s["t0"]) / 0.3)))


def scene_home(frame, s, t):
    item(frame, s["key"], 560, 560, 400)
    d = ImageDraw.Draw(frame)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        card(frame, 1320, 560, 520, 520, good=True, fill=(90, 110, 140) if s["home"] == "web" else (255, 255, 255))
        item(frame, s["home"], 1320, 560, 420 * k)
        word(frame, {"hive": "A HIVE!", "web": "A WEB!", "soil": "THE SOIL!", "snail": "ITS SHELL!"}[s["home"]], t, s["answer_t"], size=120)
    else:
        card(frame, 1320, 560, 520, 520)
        rt(frame, 1320, 560, "?", int(220 + 12 * math.sin(t * 6)), colour=(255, 77, 109))
        word(frame, "WHERE DOES IT LIVE?", t, s["t0"], size=100)


def scene_move(frame, s, t):
    q = t - s["t0"]
    mv = s["mv"]
    ax = t >= s["answer_t"]
    x, y = 960, 400
    if ax:
        x += 60 * math.sin(t * 3) if mv != "jump" else 0
        y += {"fly": -30 * abs(math.sin(t * 4)), "crawl": 0, "jump": -110 * abs(math.sin(t * 5))}[mv]
    item(frame, s["key"], x, y, 340)
    for j, m in enumerate(("fly", "crawl", "jump")):
        cx = 480 + j * 480
        good = ax and m == mv
        card(frame, cx, 790, 400, 180, good=good, dim=ax and not good)
        rt(frame, cx, 790, m.upper(), 76, colour=RAINBOW[j])
    word(frame, "HOW DOES IT MOVE?", t, s["t0"], size=100)


def scene_colour(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    item(frame, s["key"], 720, 560, 480 * k)
    if t >= s["answer_t"]:
        word(frame, s["col"].upper() + "!", t, s["answer_t"], x=1420, y=540, size=150, col=COLRGB[s["col"]])
    else:
        word(frame, "WHAT COLOUR?", t, s["t0"], x=1420, y=540, size=100)
    side_kids(frame, t, xs=(140, 1800), scale=0.24)


def scene_size(frame, s, t):
    for j, (key, sz) in enumerate(((s["big"], 420), (s["small"], 200))):
        x = 620 + j * 680
        want = (j == 0) == (s["want"] == "big")
        good = t >= s["answer_t"] and want
        card(frame, x, 560, 540, 540, good=good, dim=t >= s["answer_t"] and not want)
        item(frame, key, x, 560, sz)
    word(frame, "WHICH IS BIGGER?" if s["want"] == "big" else "WHICH IS SMALLER?", t, s["t0"], size=100)
    side_kids(frame, t, xs=(120, 1800), scale=0.24)


def scene_sound(frame, s, t):
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.5:
            for j in range(3):
                r = 120 + 100 * j + 120 * (q % 0.7)
                d.arc((960 - r, 520 - r, 960 + r, 520 + r), -50, 50, fill=(255, 255, 255, 220), width=10)
                d.arc((960 - r, 520 - r, 960 + r, 520 + r), 130, 230, fill=(255, 255, 255, 220), width=10)
        rt(frame, 960, 520, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], size=130)
    else:
        item(frame, s["key"], 960, 560, 460 * ease_back((t - s["answer_t"]) / 0.4))
        word(frame, s["key"].upper() + "!", t, s["answer_t"], size=130)
    side_kids(frame, t, xs=(170, 1750), scale=0.3)


def scene_hide(frame, s, t):
    rev = t >= s["reveal_t"]
    for i in range(3):
        x = 500 + i * 460
        if rev and i == s["pos"]:
            k = min(1, (t - s["reveal_t"]) / 0.5)
            item(frame, s["key"], x, 640, 240)
            item(frame, "leaf", x + 220 * k, 640 - 200 * k, 360, rot=40 * k)
            stars_ring(frame, x, 640, 200, 180, t, n=6, r=16)
        else:
            item(frame, "leaf", x, 640, 360, rot=4 * math.sin(t * 3 + i))
    word(frame, "FOUND IT!" if rev else "WHERE IS IT?", t, s["reveal_t"] if rev else s["t0"], size=130)
    side_kids(frame, t, xs=(130, 1790), scale=0.26)


def scene_rule(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    item(frame, ("magnifier", "bee", "ladybug", "butterfly")[s["k"]], 1300, 560, 400 * k)
    n = "gul" if s["k"] % 2 == 0 else "misheal"
    body(frame, n, t, "happy", 620, scale=0.55, hop=12 * abs(math.sin(t * 4)), wave=True)
    word(frame, s["w"], t, s["say_t"], size=120, col=(59, 170, 74))


def scene_chant(frame, s, t):
    for j, k in enumerate(("bee", "ladybug", "ant", "grasshopper", "butterfly")):
        item(frame, k, 300 + j * 330, 330 + 20 * math.sin(t * 4 + j), 200)
    for n, x in (("gul", 620), ("misheal", 1300)):
        body(frame, n, t, "happy", x, scale=0.42, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    word(frame, "BUSY BUGS!", t, s["t0"], size=120)


def scene_outro(frame, s, t):
    for j, k in enumerate(("butterfly", "bee", "ladybug", "dragonfly")):
        a = j * 1.57 + t * 0.6
        item(frame, k, 960 + 640 * math.cos(a), 450 + 240 * math.sin(a), 190)
    for n, x in (("gul", 720), ("misheal", 1200)):
        body(frame, n, t, "happy", x, scale=0.42, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "GREAT BUG HUNT!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


SPIDER = (960, 570, 620)
SLEGS = [(25, 150), (15, 255), (35, 350), (95, 385), (375, 150), (385, 255), (365, 350), (305, 385)]


def scene_spiderlegs(frame, s, t):
    cx, cy, S = SPIDER
    item(frame, "spider", cx, cy, S)
    d = ImageDraw.Draw(frame)
    n = sum(1 for x in s["cts"] if t >= x)
    for i in range(n):
        x, y = cx + (SLEGS[i][0] - 200) * S / 372, cy + (SLEGS[i][1] - 202) * S / 372
        d.ellipse((x - 38, y - 38, x + 38, y + 38), fill=(255, 255, 255), outline=(255, 77, 109), width=6)
        rt(frame, x, y, str(i + 1), 52, colour=(255, 77, 109))
    word(frame, "8 LEGS!" if t >= s["sum_t"] else "COUNT THE LEGS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], y=110, size=120)


def scene_webbuild(frame, s, t):
    q = min(1, (t - s["t0"]) / max(1, s["t1"] - s["t0"] - 0.8))
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((430, 180, 1490, 980), radius=30, fill=(50, 70, 110, 255), outline=INK, width=6)
    item(frame, "web", 960, 580, 200 + 520 * q, rot=q * 30)
    item(frame, "spider", 960 + 300 * math.cos(q * 18) * q, 580 + 300 * math.sin(q * 18) * q, 170)
    word(frame, "SPIN A WEB!", t, s["say_t"], y=100, size=120)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.3)


def scene_glow(frame, s, t):
    n = sum(1 for x in s["cts"] if t >= x)
    pos = [(420, 420), (760, 300), (1120, 460), (1480, 330), (640, 640), (1280, 660)]
    for i in range(n):
        x, y = pos[i]
        a = 0.45 + 0.55 * abs(math.sin(t * 2.5 + i))
        d = ImageDraw.Draw(frame, "RGBA")
        for r, al in ((120, 50), (80, 90), (50, 130)):
            d.ellipse((x - r, y + 40 - r, x + r, y + 40 + r), fill=(255, 240, 120, int(al * a)))
        item(frame, "firefly", x + 16 * math.sin(t * 1.5 + i), y + 12 * math.cos(t * 1.8 + i), 170)
        rt(frame, x + 110, y - 90, str(i + 1), 62, colour=(255, 240, 120))
    rt(frame, 960, 110, "6 FIREFLIES!" if t >= s["sum_t"] else "COUNT THE FIREFLIES!", 100, colour=(255, 240, 120), maxw=1500)
    side_kids(frame, t, "happy", xs=(160, 1760), scale=0.3)


SCENES = {"intro": scene_intro, "hunt": scene_hunt, "anatomy": scene_anatomy, "isnot": scene_isnot, "spots": scene_spots, "honey": scene_honey, "march": scene_march,
          "room": scene_room, "home": scene_home, "move": scene_move, "colour": scene_colour, "size": scene_size, "sound": scene_sound, "hide": scene_hide,
          "rule": scene_rule, "spiderlegs": scene_spiderlegs, "webbuild": scene_webbuild, "glow": scene_glow, "chant": scene_chant, "outro": scene_outro,
          "dance": lambda f, s, t: (item(f, "butterfly", 1720, 500 + 30 * math.sin(t * 3), 240), K.scene_dance(f, s, t))}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L23 Bugs and Insects", "Bugs and Insects for Kids")
K.CFG["title_items"] = ["bee", "ladybug", "butterfly", "ant", "grasshopper"]

if __name__ == "__main__":
    K.main()
