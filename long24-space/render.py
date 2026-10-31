"""Animate L24 "Space & Planets for Kids".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW

A24 = HERE / "art"
PLANETS = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
SIZE = {"mercury": 70, "venus": 110, "earth": 115, "mars": 90, "jupiter": 260, "saturn": 250, "uranus": 150, "neptune": 145}
ART = {k: A24 / f"item_{k}.png" for k in PLANETS + ["sun", "moon2", "astronaut", "comet", "telescope", "footprint"]}
ART.update({"rocket": ROOT / "long21-presents/art/item_rocket.png", "car": ROOT / "long16-sharing/art/item_car.png", "fish": ROOT / "long01-animals-fun/art/fruit_fish.png",
            "duck": ROOT / "long11-bath/art/item_duck.png", "star": ROOT / "long15-potty/art/item_star.png"})
BGS = {k: A24 / f"bg_{k}.png" for k in ("space", "moonland", "launch")}
YEL = (255, 225, 90)


def kids_astro(frame, t, n=2):
    item(frame, "astronaut", 190, 860 + 12 * math.sin(t * 1.5), 330, rot=5 * math.sin(t))
    item(frame, "astronaut", 1730, 860 + 12 * math.sin(t * 1.5 + 1), 330, rot=-5 * math.sin(t), flip=True)


def scene_intro(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    q = t - s["go_t"]
    y = 560 if q < 0 else 560 - 900 * ease_io(min(1, q / 1.5))
    sh = 6 * math.sin(t * 40) if q >= 0 else 0
    d = ImageDraw.Draw(frame)
    if q >= 0:
        for j in range(5):
            d.ellipse((960 - 90 - j * 30 + sh, y + 300 + j * 40, 960 + 90 + j * 30 + sh, y + 460 + j * 40), fill=(255, 150 + j * 18, 40))
    item(frame, "rocket", 960 + sh, y, 640)
    if n and q < 0:
        rt(frame, 1480, 460, str(6 - n), int(320 * ease_back((t - s["ts"][n - 1]) / 0.25)), colour=(232, 53, 46))
    if q >= 0:
        rt(frame, 960, 200, "BLAST OFF!", int(180 * ease_back(q / 0.3)))
    side_kids(frame, t, "excited", xs=(240, 1680), scale=0.34)


def scene_arrive(frame, s, t):
    q = t - s["t0"]
    for j, k in enumerate(("mars", "earth", "saturn", "jupiter", "neptune")):
        a = j * 1.26 + t * 0.35
        item(frame, k, 960 + 620 * math.cos(a), 590 + 300 * math.sin(a), SIZE[k] * 1.1)
    item(frame, "rocket", 960, 590 + 14 * math.sin(t * 2), 300, rot=20)
    rt(frame, 960, 130, "SPACE & PLANETS!", int(150 * ease_back(q / 0.35)), maxw=1700)
    kids_astro(frame, t)


def scene_suit(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    labs = ["HELMET!", "SUIT!", "GLOVES!", "BOOTS!"]
    spots = [(960, 300), (960, 620), (690, 700), (960, 890)]
    item(frame, "astronaut", 960, 600, 800, alpha=1.0 if t >= s["done_t"] else 0.35)
    d = ImageDraw.Draw(frame)
    if n and t < s["done_t"]:
        x, y = spots[n - 1]
        r = 150 + 8 * math.sin(t * 6)
        d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 215, 60), width=14)
        word(frame, labs[n - 1], t, s["ts"][n - 1], x=1520, y=500, size=120, col=(46, 120, 230))
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "ASTRONAUTS!", t, s["done_t"], y=110, size=130)
    side_kids(frame, t, "happy", xs=(240, 1700), scale=0.3)


def scene_build(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    item(frame, "rocket", 800, 500, 800, alpha=0.3 + 0.175 * n)
    if n >= 4:
        d = ImageDraw.Draw(frame)
        for j in range(4):
            yy = 900 - ((t * 200 + j * 60) % 240)
            d.ellipse((1350, yy, 1380, yy + 40), fill=(255, 170, 50))
    labs = ["BODY!", "FINS!", "WINDOW!", "FUEL!"]
    word(frame, labs[n - 1] if n else "BUILD A ROCKET!", t, s["ts"][n - 1] if n else s["t0"], x=1500 if n else 960, y=460 if n else 120, size=120, col=(140, 80, 210))
    side_kids(frame, t, "happy", xs=(240, 1740), scale=0.3)


def scene_sun(frame, s, t):
    ph = t >= s["c"]
    item(frame, "sun", 960, 560, 460 + (0 if ph else 80), rot=t * 8)
    if ph:
        for j, k in enumerate(PLANETS):
            r = 280 + j * 75
            a = t * (0.9 - j * 0.08) + j
            item(frame, k, 960 + r * 1.5 * math.cos(a), 560 + r * 0.55 * math.sin(a), SIZE[k] * 0.55)
    word(frame, "8 PLANETS GO AROUND!" if ph else ("LIGHT AND HEAT!" if t >= s["b"] else "THE SUN IS A STAR!"), t, s["c"] if ph else (s["b"] if t >= s["b"] else s["a"]), y=100, size=110, col=YEL)


def strip(frame, upto):
    for i, k in enumerate(PLANETS):
        x = 330 + i * 180
        if i < upto:
            item(frame, k, x, 1000, 86)
        else:
            d = ImageDraw.Draw(frame)
            d.ellipse((x - 34, 966, x + 34, 1034), outline=(150, 160, 200), width=4)


def scene_planet(frame, s, t):
    k = ease_back((t - s["name_t"]) / 0.4) if t >= s["name_t"] else 0
    if t >= s["name_t"]:
        item(frame, s["key"], 960, 540 + 10 * math.sin(t * 2), 620 * k)
    else:
        rt(frame, 960, 540, str(s["num"]), int(330 * ease_back((t - s["t0"]) / 0.3)), colour=YEL)
    if t >= s["f1_t"]:
        word(frame, s["w"], t, s["f1_t"], y=110, size=130, col=YEL)
    elif t >= s["name_t"]:
        word(frame, s["name"] + "!", t, s["name_t"], y=110, size=140)
    badge(frame, 160, 90, f"{s['num']}/8", (46, 120, 230))
    strip(frame, s["num"] if t >= s["name_t"] else s["num"] - 1)
    kids_astro(frame, t)


def scene_lineup(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    item(frame, "sun", -60, 540, 560, rot=t * 8)
    x = 300
    for i, k in enumerate(PLANETS[:n]):
        sz = SIZE[k] * 1.05
        x += sz / 2
        hi = i == n - 1 and t < s["sum_t"]
        item(frame, k, x, 560 - (24 if hi else 0), sz)
        rt(frame, x, 800 + (i % 2) * 70, k.upper(), 38, colour=(255, 255, 255), maxw=240)
        x += sz / 2 + 12
    word(frame, "8 PLANETS!", t, s["t0"], y=110, size=130, col=YEL)


def scene_sizes(frame, s, t):
    item(frame, "jupiter", 620, 560, 760)
    if t >= s["b"]:
        item(frame, "earth", 1250, 660, 110 * ease_back((t - s["b"]) / 0.4))
        rt(frame, 1250, 780, "EARTH", 52, colour=(255, 255, 255))
    if t >= s["c"]:
        item(frame, "mercury", 1520, 680, 56 * ease_back((t - s["c"]) / 0.4))
        rt(frame, 1520, 780, "MERCURY", 52, colour=(255, 255, 255))
    word(frame, "SMALLEST!" if t >= s["c"] else ("SMALLER!" if t >= s["b"] else "JUPITER IS BIGGEST!"), t, s["c"] if t >= s["c"] else (s["b"] if t >= s["b"] else s["a"]), x=1250, y=240, size=90, col=YEL, maxw=1100)


def scene_daynight(frame, s, t):
    item(frame, "sun", 240, 540, 460, rot=t * 8)
    d = ImageDraw.Draw(frame, "RGBA")
    night = t >= s["b"]
    d.polygon([(420, 420), (800, 380), (800, 700), (420, 660)], fill=(255, 235, 120, 70))
    item(frame, "earth", 1040, 540, 520, rot=-t * 25)
    d = ImageDraw.Draw(frame, "RGBA")
    d.pieslice((1040 - 240, 540 - 240, 1040 + 240, 540 + 240), -90, 90, fill=(5, 8, 40, 170))
    rt(frame, 720, 860, "DAY", 90, colour=YEL)
    rt(frame, 1340, 860, "NIGHT", 90, colour=(170, 190, 255))
    word(frame, "NIGHT TIME!" if night else "DAY TIME!", t, s["b"] if night else s["a"], y=110, size=130, col=YEL)


def scene_which(frame, s, t):
    keys = [s["key"]] + [p for p in ("venus", "neptune", "mars", "earth") if p != s["key"]][:2]
    keys = sorted(keys, key=lambda k: (PLANETS.index(k) * 3 + 1) % 7)
    for i, k in enumerate(keys):
        x = 460 + i * 500
        ok = t >= s["answer_t"] and k == s["key"]
        dim = t >= s["answer_t"] and not ok
        item(frame, k, x, 560 - (20 * abs(math.sin(t * 5)) if ok else 0), 340, alpha=0.3 if dim else 1)
        if ok:
            stars_ring(frame, x, 560, 240, 230, t, n=8, r=18)
    rt(frame, 960, 130, s["q"], int(82 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)
    kids_astro(frame, t)


def scene_nextp(frame, s, t):
    i = PLANETS.index(s["key"])
    show = PLANETS[max(0, i - 3):i]
    for j, k in enumerate(show):
        item(frame, k, 400 + j * 370, 540, 280)
    x = 400 + len(show) * 370
    if t >= s["answer_t"]:
        item(frame, s["key"], x, 540, 320 * ease_back((t - s["answer_t"]) / 0.4))
        stars_ring(frame, x, 540, 210, 200, t, n=8, r=16)
    else:
        rt(frame, x, 540, "?", int(240 + 12 * math.sin(t * 6)), colour=YEL)
    word(frame, "WHAT COMES NEXT?", t, s["t0"], size=110, col=YEL)


def scene_moon(frame, s, t):
    key = s["key"]
    if key == "orbit":
        a = t * 1.2
        item(frame, "earth", 960, 500, 280)
        item(frame, "moon2", 960 + 500 * math.cos(a), 500 + 240 * math.sin(a), 130)
        word(frame, "AROUND THE EARTH!", t, s["say_t"], y=860, size=110, col=YEL)
    elif key == "craters":
        item(frame, "moon2", 960, 460, 560)
        word(frame, "CRATERS!", t, s["say_t"], y=860, size=130, col=YEL)
    elif key == "suit":
        item(frame, "astronaut", 960, 540, 640, rot=4 * math.sin(t * 2))
        word(frame, "NO AIR!", t, s["say_t"], y=110, size=130, col=YEL)
    else:
        q = min(6, int((t - s["t0"]) * 2))
        for i in range(q):
            item(frame, "footprint", 300 + i * 230, 840 - (i % 2) * 70, 130, rot=-80)
        item(frame, "astronaut", 300 + q * 230, 640, 380)
        word(frame, "FOOTPRINTS!", t, s["say_t"], y=110, size=130, col=YEL)


def scene_walk(frame, s, t):
    q = t - s["t0"]
    x = 200 + (q * 170) % 1500
    item(frame, "astronaut", x, 650 - 300 * abs(math.sin(q * 1.3)), 380)
    word(frame, "BOING, BOING!", t, s["t0"], y=110, size=130, col=YEL)


def scene_phase(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    f = s["f"]
    cx, cy, r = 960, 540, 300
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 34, 70, 255), outline=(120, 130, 180), width=5)
    if f >= 1:
        item(frame, "moon2", cx, cy, 2 * r)
    elif f > 0:
        m = Image.new("L", frame.size, 0)
        md = ImageDraw.Draw(m)
        md.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        if f <= 0.25:
            md.ellipse((cx - r - 150, cy - r, cx + r - 150, cy + r), fill=0)
        else:
            md.rectangle((0, 0, cx, 1080), fill=0)
        light = Image.new("RGBA", frame.size, (235, 238, 245, 255))
        frame.paste(light, (0, 0), m)
    word(frame, {0.0: "NEW MOON!", 0.25: "CRESCENT!", 0.5: "HALF MOON!", 1.0: "FULL MOON!"}[f], t, s["say_t"], y=110, size=130, col=YEL)
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.3)


def scene_float(frame, s, t):
    key = s["key"]
    q = t - s["t0"]
    if key == "hair":
        item(frame, "astronaut", 960, 540 + 90 * math.sin(q), 520, rot=q * 30)
        for j, k in enumerate(("star", "duck", "car")):
            item(frame, k, 400 + j * 560, 400 + 100 * math.sin(q + j), 150, rot=q * 40)
        word(frame, "FLOATING!", t, s["say_t"], size=130, col=YEL)
    elif key == "food":
        item(frame, "astronaut", 1250, 560, 520)
        d = ImageDraw.Draw(frame)
        for j in range(5):
            x, y = 500 + 60 * math.sin(q + j * 2) + j * 80, 360 + j * 70 + 40 * math.cos(q * 1.3 + j)
            d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=RAINBOW[j], outline=INK, width=4)
        word(frame, "FLOATING FOOD!", t, s["say_t"], size=120, col=YEL)
    else:
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((640, 240, 1280, 900), radius=60, fill=(90, 100, 170), outline=INK, width=7)
        item(frame, "astronaut", 960, 570, 560)
        d.rectangle((690, 560, 1230, 620), fill=(255, 210, 40), outline=INK, width=5)
        word(frame, "ZZZ!", t, s["say_t"], x=1500, y=300, size=160, col=YEL)


def scene_count(frame, s, t):
    n = sum(1 for x in s["cts"] if t >= x)
    pos = [(300, 300), (700, 220), (1120, 300), (1560, 240), (480, 560), (900, 500), (1340, 560), (270, 800), (800, 820), (1560, 790)]
    for i in range(n):
        x, y = pos[i]
        item(frame, "star", x, y, 170 * ease_back((t - s["cts"][i]) / 0.3), rot=10 * math.sin(t * 2 + i))
        rt(frame, x, y + 120, str(i + 1), 56, colour=(255, 255, 255))
    word(frame, f"{n} STARS!" if n else "COUNT THE STARS!", t, s["cts"][n - 1] if n else s["t0"], size=110, col=YEL)


CONS = {4: [(960, 200), (1380, 520), (960, 900), (540, 520), (960, 200)], 5: [(960, 180), (1200, 880), (560, 430), (1360, 430), (720, 880), (960, 180)]}


def scene_connect(frame, s, t):
    pts = CONS[s["n"]]
    d = ImageDraw.Draw(frame)
    if t >= s["answer_t"]:
        f = min(1, (t - s["answer_t"]) / 1.0) * (len(pts) - 1)
        for i in range(int(f)):
            d.line((*pts[i], *pts[i + 1]), fill=(255, 225, 90), width=12)
        i = int(f)
        if i < len(pts) - 1:
            k = f - i
            d.line((*pts[i], pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k), fill=(255, 225, 90), width=12)
    for p in pts[:-1]:
        item(frame, "star", p[0], p[1], 90 + 10 * math.sin(t * 4))
    side_kids(frame, t, xs=(170, 1750), scale=0.3)


def scene_sort(frame, s, t):
    rt(frame, 960, 150, s["q"], int(100 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)
    item(frame, s["key"], 960, 540, 420)
    if t >= s["answer_t"]:
        d = ImageDraw.Draw(frame)
        k = ease_back((t - s["answer_t"]) / 0.3)
        if s["good"]:
            d.line((1210, 520, 1310, 620, 1510, 380), fill=(59, 193, 74), width=int(40 * k) + 1, joint="curve")
            word(frame, "SPACE!", t, s["answer_t"], y=860, size=140, col=(90, 225, 110))
        else:
            r = 250 * k
            d.ellipse((960 - r, 540 - r, 960 + r, 540 + r), outline=(232, 53, 46), width=24)
            d.line((960 - r * 0.7, 540 + r * 0.7, 960 + r * 0.7, 540 - r * 0.7), fill=(232, 53, 46), width=24)
            word(frame, "NOT IN SPACE!", t, s["answer_t"], y=860, size=120, col=(255, 110, 100))
    side_kids(frame, t, xs=(170, 1750))


def scene_outro(frame, s, t):
    item(frame, "earth", 960, 620, 420)
    item(frame, "rocket", 1450 - (t - s["t0"]) * 30, 300, 260, rot=70)
    for n, x in (("gul", 420), ("misheal", 1500)):
        body(frame, n, t, "happy", x, scale=0.42, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "BACK TO EARTH!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


def two_bins(frame, t, s, labs, cols, first, key):
    d = ImageDraw.Draw(frame, "RGBA")
    for j in range(2):
        x = 430 + j * 1060
        good = t >= s["answer_t"] and (j == 0) == first
        d.rounded_rectangle((x - 300, 640, x + 300, 960), radius=36, fill=cols[j] + (70,), outline=(90, 225, 110) if good else (255, 255, 255), width=14 if good else 6)
        rt(frame, x, 880, labs[j], 76, colour=cols[j])
    if t >= s["answer_t"]:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x, y, sz = 960 + ((430 if first else 1490) - 960) * k, 380 + 370 * k, 380 - 180 * k
    else:
        x, y, sz = 960, 380 + 10 * math.sin(t * 3), 380
    item(frame, key, x, y, sz)


def scene_rocky(frame, s, t):
    two_bins(frame, t, s, ("ROCKY", "GIANT"), ((205, 130, 90), (150, 190, 255)), s["rocky"], s["key"])
    word(frame, "ROCKY OR GIANT?", t, s["t0"], y=100, size=100, col=YEL)


def scene_hotcold(frame, s, t):
    two_bins(frame, t, s, ("HOT", "COLD"), ((255, 110, 80), (120, 200, 255)), s["hot"], s["key"])
    word(frame, "HOT OR COLD?", t, s["t0"], y=100, size=100, col=YEL)


def scene_pcol(frame, s, t):
    item(frame, s["key"], 960, 480, 560)
    if t >= s["answer_t"]:
        word(frame, s["col"] + "!", t, s["answer_t"], y=860, size=110, col=YEL, maxw=1500)
    else:
        word(frame, "WHAT COLOUR?", t, s["t0"], y=860, size=110)
    kids_astro(frame, t)


def scene_tele(frame, s, t):
    item(frame, "telescope", 380, 620, 560)
    d = ImageDraw.Draw(frame)
    d.ellipse((800, 110, 1560, 870), fill=(14, 17, 64), outline=(255, 215, 60), width=18)
    item(frame, s["key"], 1180, 490, 460 * ease_back((t - s["t0"]) / 0.4), rot=3 * math.sin(t * 2))
    word(frame, {"moon2": "THE MOON!", "saturn": "SATURN!", "comet": "A COMET!"}[s["key"]], t, s["say_t"], y=960, x=1180, size=100, col=YEL)


def scene_chant(frame, s, t):
    n = sum(1 for x in s["l"] if t >= x)
    gp = [(0, 1), (2, 3), (4, 5), (6, 7)]
    lit = gp[(n - 1) % 4] if n else ()
    for i, k in enumerate(PLANETS):
        a = i / 8 * 2 * math.pi + t * 0.3
        item(frame, k, 960 + 680 * math.cos(a), 520 + 300 * math.sin(a), (SIZE[k] * 0.8 + 50) * (1.3 if i in lit else 1))
    for nm, x in (("gul", 820), ("misheal", 1100)):
        body(frame, nm, t, "happy", x, scale=0.36, hop=22 * abs(math.sin(t * 4 + (0 if nm == "gul" else 1))), wave=True)
    word(frame, "CLAP ALONG!", t, s["t0"], y=90, size=100, col=YEL)


SCENES = {"intro": scene_intro, "arrive": scene_arrive, "suit": scene_suit, "build": scene_build, "sun": scene_sun, "planet": scene_planet, "lineup": scene_lineup,
          "sizes": scene_sizes, "daynight": scene_daynight, "which": scene_which, "nextp": scene_nextp, "moon": scene_moon, "walk": scene_walk, "phase": scene_phase,
          "float": scene_float, "count": scene_count, "connect": scene_connect, "sort": scene_sort, "outro": scene_outro,
          "rocky": scene_rocky, "hotcold": scene_hotcold, "pcol": scene_pcol, "tele": scene_tele, "chant": scene_chant,
          "dance": lambda f, s, t: (item(f, "saturn", 1730, 330, 280), K.scene_dance(f, s, t))}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L24 Space and Planets", "Space and Planets for Kids")
K.CFG["title_items"] = ["rocket", "saturn", "earth", "astronaut", "jupiter"]

if __name__ == "__main__":
    K.main()
