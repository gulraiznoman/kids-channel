"""Animate L17 "Decorate the Christmas Tree".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW, G

A17 = HERE / "art"
ART = {k: A17 / f"item_{k}.png" for k in ("tree", "topstar", "present1", "present2", "present3", "candycane", "stocking", "gingerbread", "santahat", "bell", "snowflake")}
ART.update({"ball": ROOT / "long04-good-habits/art/item_ball.png", "teddy": ROOT / "long15-potty/art/item_teddy.png",
            "car": ROOT / "long16-sharing/art/item_car.png", "crayons": ROOT / "long16-sharing/art/item_crayons.png",
            "heart": ROOT / "long16-sharing/art/item_heart.png", "snowman": ROOT / "long08-colors-shapes/art/item_snowman.png",
            "bowl": ROOT / "long03-fruits-veg/art/item_bowl.png", "sunny": ROOT / "long01-animals-fun/art/fruit_sunny.png",
            "icecream": ROOT / "long05-body-parts/art/item_icecream.png", "umbrella": ROOT / "long16-sharing/art/item_umbrella.png"})
BGS = {"xmasroom": A17 / "bg_xmasroom.png"}
STAGES = ["lights", "baubles", "bells", "canes", "ginger", "flakes"]
LIGHTCOL = [(232, 53, 46), (255, 140, 26), (255, 210, 40), (59, 193, 74), (46, 140, 255)]
# ornament spots as (u, v): v = 0 top .. 1 bottom of the green part, u = -1 .. 1 across at that height
SPOTS = {"baubles": [(-0.5, 0.45), (0.45, 0.35), (0.0, 0.6), (-0.6, 0.85), (0.6, 0.8)],
         "bells": [(0.2, 0.22), (-0.35, 0.68), (0.35, 0.95)],
         "canes": [(-0.2, 0.3), (0.65, 0.58), (-0.7, 0.6), (0.15, 0.9)],
         "ginger": [(-0.3, 0.98), (0.0, 0.42)],
         "flakes": [(0.0, 0.12), (-0.45, 0.25), (0.3, 0.72), (-0.15, 0.78), (0.75, 0.98), (-0.85, 0.98)]}
ORN = {"bells": ("bell", 0.11), "canes": ("candycane", 0.12), "ginger": ("gingerbread", 0.13), "flakes": ("snowflake", 0.09)}


def spot(cx, top, h, u, v):
    hw = 0.06 * h + v * 0.42 * h
    return cx + u * hw, top + v * 0.82 * h


def bauble(frame, x, y, r, col=(232, 53, 46)):
    d = ImageDraw.Draw(frame)
    d.rectangle((x - r * 0.3, y - r * 1.25, x + r * 0.3, y - r * 0.85), fill=(255, 210, 40), outline=INK, width=3)
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=INK, width=max(3, int(r / 8)))
    d.ellipse((x - r * 0.55, y - r * 0.6, x - r * 0.15, y - r * 0.25), fill=(255, 255, 255))


def tree(frame, cx, by, h, t, upto=6, partial=None, star=True, glow=1.0):
    """by = bottom of trunk; h = tree height. upto = number of finished stages; partial = (stage index, count)"""
    item(frame, "tree", cx, by - h / 2, h)
    top = by - h * 0.93
    d = ImageDraw.Draw(frame)
    for si, st in enumerate(STAGES):
        if si > upto or (si == upto and not partial):
            break
        cnt = partial[1] if (partial and si == partial[0]) else 99
        if st == "lights":
            for row in range(3):
                v0 = 0.25 + row * 0.3
                pts = [spot(cx, top, h, u, v0 + 0.06 * u) for u in [x / 10 for x in range(-10, 11)]]
                d.line(pts, fill=(40, 90, 40), width=4)
                for j, (x, y) in enumerate(pts[::3]):
                    ci = (j + row) % 5
                    if ci >= cnt:
                        continue
                    on = 0.5 + 0.5 * math.sin(t * 5 + j + row * 2)
                    c = tuple(int(v * (0.6 + 0.4 * on * glow)) for v in LIGHTCOL[ci])
                    d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=c, outline=INK, width=2)
        elif st == "baubles":
            for j, (u, v) in enumerate(SPOTS[st][:cnt]):
                x, y = spot(cx, top, h, u, v)
                bauble(frame, x, y, h * 0.045)
        else:
            key, sz = ORN[st]
            for j, (u, v) in enumerate(SPOTS[st][:cnt]):
                x, y = spot(cx, top, h, u, v)
                item(frame, key, x, y, h * sz, rot=6 * math.sin(t * 2 + j))
    if star:
        item(frame, "topstar", cx, top - h * 0.03, h * 0.17, rot=4 * math.sin(t * 2))


def full_tree(frame, t, cx=1500, by=1000, h=640):
    tree(frame, cx, by, h, t)
    for i, p in enumerate(("present1", "present2", "present3")):
        item(frame, p, cx - 170 + i * 170, by - 50, 130)


def scene_intro(frame, s, t):
    tree(frame, 960, 1020, 860, t)
    for i, p in enumerate(("present1", "present2", "present3")):
        item(frame, p, 760 + i * 200, 970, 160)
    if t < s["on_t"]:
        frame.alpha_composite(Image.new("RGBA", frame.size, (10, 10, 40, 200)))
    elif t < s["on_t"] + 0.4:
        frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(220 * (1 - (t - s["on_t"]) / 0.4)))))
    if t >= s["title_t"]:
        k = t - s["title_t"]
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(330, 1590), scale=0.4)
        rt(frame, 960, 150, "CHRISTMAS TREE!", int(190 * ease_back(k / 0.35)), maxw=1600)


def scene_bring(frame, s, t):
    q = t - s["t0"]
    x = 2300 - (2300 - 960) * ease_io(min(1, q / 2.0)) if t < s["set_t"] else 960
    tree(frame, x, 1020, 820, t, upto=0, star=False)
    if t < s["set_t"]:
        body(frame, "gul", t, "excited", x - 360, scale=0.45, hop=12 * abs(math.sin(t * 8)))
        body(frame, "misheal", t, "excited", x + 360, scale=0.45, hop=12 * abs(math.sin(t * 8 + 1)))
    else:
        side_kids(frame, t, "happy", xs=(330, 1590), scale=0.4)
    word(frame, "HERE COMES THE TREE!", t, s["t0"], size=120)


def scene_decor(frame, s, t):
    k = s["stage"]
    n = sum(1 for x in s["cts"] if t >= x)
    tree(frame, 960, 1030, 880, t, upto=k, partial=(k, n), star=False)
    side_kids(frame, t, "happy", xs=(250, 1670), scale=0.38)
    if n:
        rt(frame, 1520, 300, str(n), int(200 * ease_back((t - s["cts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    lab = {"lights": "LIGHTS!", "baubles": "RED BALLS!", "bells": "GOLDEN BELLS!", "canes": "CANDY CANES!", "ginger": "GINGERBREAD!", "flakes": "SNOWFLAKES!"}[s["key"]]
    word(frame, f"{s['n']} {lab}" if t >= s["sum_t"] else lab, t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=120)


def scene_star(frame, s, t):
    up = t >= s["star_t"]
    tree(frame, 960, 1030, 880, t, star=up, glow=1.0 if up else 0.4)
    if not up:
        n = sum(1 for x in s["cd"] if t >= x)
        item(frame, "topstar", 960, 120 + 10 * math.sin(t * 3), 160)
        if n:
            rt(frame, 1520, 400, str(4 - n), 220, colour=RAINBOW[n])
        side_kids(frame, t, "excited", xs=(250, 1670), scale=0.38)
    else:
        stars_ring(frame, 960, 200, 260, 120, t * 2, n=10, r=22)
        confetti(frame, t, s["star_t"])
        side_kids(frame, t, "excited", xs=(250, 1670), scale=0.38)
        word(frame, "BEAUTIFUL!", t, s["star_t"], y=1000 - 880, size=140)


def shape_pic(frame, shp, x, y, sz, t):
    if shp == "circle":
        bauble(frame, x, y, sz * 0.4)
    elif shp == "triangle":
        item(frame, "tree", x, y, sz)
    elif shp == "star":
        item(frame, "topstar", x, y, sz)
    elif shp == "rectangle":
        item(frame, "present2", x, y, sz)
    else:
        item(frame, "heart", x, y, sz)


def scene_shape(frame, s, t):
    full_tree(frame, t, cx=560, by=1020, h=760)
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 1340, 520, 560, 560)
    shape_pic(frame, s["shape"], 1340, 520, 380 * k, t)
    word(frame, s["shape"].upper() + "!", t, s["say_t"], x=1340, y=880, size=120)


COLRGB = {"red": (232, 53, 46), "green": (59, 193, 74), "gold": (240, 180, 20), "white": (255, 255, 255), "brown": (150, 95, 50)}


def scene_colour(frame, s, t):
    full_tree(frame, t, cx=1560, by=1020, h=600)
    key = {"stocking": "stocking", "tree": "tree", "bell": "bell", "snowflake": "snowflake", "gingerbread": "gingerbread"}[s["key"]]
    item(frame, key, 760, 540 + 10 * math.sin(t * 3), 420 * ease_back((t - s["t0"]) / 0.4))
    if t >= s["answer_t"]:
        word(frame, s["col"].upper() + "!", t, s["answer_t"], x=760, y=150, size=160, col=COLRGB[s["col"]])
    else:
        word(frame, "WHAT COLOUR?", t, s["t0"], x=760, y=150, size=120)
    side_kids(frame, t, xs=(150, 1100), scale=0.28)


def scene_present(frame, s, t):
    full_tree(frame, t, cx=1560, by=1020, h=600)
    x, y = 800, 640
    if t < s["open_t"]:
        sh = 12 * math.sin(t * 30) if (t - s["shake_t"]) % 2.0 < 0.8 else 0
        item(frame, s["box"], x + sh, y, 380, rot=sh * 0.5)
        rt(frame, x + 300, y - 260, "?", int(150 + 12 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "WHAT'S INSIDE?", t, s["t0"], x=800, size=120)
    else:
        k = min(1, (t - s["open_t"]) / 0.6)
        item(frame, s["box"], x, y + 60, 360)
        item(frame, s["inside"], x, y - 80 - 160 * ease_back(k), 280 * max(0.1, ease_back(k)))
        confetti(frame, t, s["open_t"])
        word(frame, s["inside"].upper() + "!", t, s["open_t"], x=800, size=140)
    side_kids(frame, t, xs=(150, 1100), scale=0.28)


def scene_stockings(frame, s, t):
    full_tree(frame, t, cx=1500, by=1020, h=640)
    for i, name in enumerate(("GUL", "MISHU", "MAMA", "PAPA")):
        if t >= s["ts"][i]:
            k = ease_back((t - s["ts"][i]) / 0.35)
            x = 135 + i * 110
            item(frame, "stocking", x, 500 + 6 * math.sin(t * 2 + i), 140 * k)
            rt(frame, x, 600, name, 30, colour=(255, 255, 255), maxw=110)
    side_kids(frame, t, "happy", xs=(820, 1060), scale=0.34)
    word(frame, "4 STOCKINGS!" if t >= s["count_t"] else "HANG THE STOCKINGS!", t, s["count_t"] if t >= s["count_t"] else s["t0"], size=110)


def quiz_draw(frame, vis, t, k):
    if vis == "bauble":
        bauble(frame, 960, 580, 170 * k)
    elif vis == "tree":
        item(frame, "tree", 960, 580, 460 * k)
    else:
        item(frame, vis, 960, 580, 400 * k)


def scene_outro(frame, s, t):
    tree(frame, 960, 1030, 860, t)
    for n, x in (("gul", 420), ("misheal", 1500)):
        body(frame, n, t, "happy", x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "MERRY CHRISTMAS!", int(170 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "THANK YOU!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


def scene_cword(frame, s, t):
    badge(frame, 160, 90, f"{s['num']}/10", (232, 53, 46))
    k = ease_back((t - s["t0"]) / 0.4)
    K.card(frame, 760, 540, 560, 560)
    if s["key"] == "tree":
        item(frame, "tree", 760, 540, 440 * k)
    else:
        item(frame, s["key"], 760, 540 + 8 * math.sin(t * 2.5), 400 * k)
    rt(frame, 1350, 540, s["w"] + "!", int(110 * k), colour=RAINBOW[s["num"] % 6], maxw=620)
    side_kids(frame, t, xs=(150, 1770), scale=0.28)


def scene_count(frame, s, t):
    tree(frame, 960, 760, 560, t)
    n = sum(1 for x in s["cts"] if t >= x)
    keys = ("present1", "present2", "present3")
    for i in range(n):
        x = 340 + (i % 5) * 310
        y = 860 + (i // 5) * 120 - (40 if i < 5 else 0)
        item(frame, keys[i % 3], x, y, 130)
        rt(frame, x, y - 80, str(i + 1), 60, colour=RAINBOW[i % 6])
    word(frame, f"{n} PRESENTS!" if n else "COUNT THE PRESENTS!", t, s["cts"][n - 1] if n else s["t0"], size=110)


def scene_bake(frame, s, t):
    key = s["key"]
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((420, 700, 1500, 780), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    q = t - s["t0"]
    if key == "bowl":
        item(frame, "bowl", 960, 600, 360, rot=6 * math.sin(t * 8))
    elif key == "roll":
        d.ellipse((700, 640, 1220, 720), fill=(200, 140, 80), outline=INK, width=5)
        x = 760 + 400 * (0.5 + 0.5 * math.sin(t * 3))
        d.rounded_rectangle((x - 160, 590, x + 160, 640), radius=25, fill=(230, 190, 140), outline=INK, width=5)
    elif key == "cut":
        d.ellipse((700, 640, 1220, 720), fill=(200, 140, 80), outline=INK, width=5)
        for i in range(min(3, int(q * 1.5) + 1)):
            item(frame, "gingerbread", 820 + i * 140, 640, 150)
    elif key == "oven":
        d.rounded_rectangle((760, 300, 1160, 700), radius=24, fill=(190, 195, 210), outline=INK, width=8)
        d.rounded_rectangle((800, 400, 1120, 650), radius=16, fill=(255, 160, 60) if int(t * 2) % 2 else (255, 190, 90), outline=INK, width=6)
        for i in range(3):
            item(frame, "gingerbread", 880 + i * 80, 560, 110)
    else:
        for i in range(3):
            item(frame, "gingerbread", 760 + i * 200, 600 - 15 * abs(math.sin(t * 4 + i)), 220)
        stars_ring(frame, 960, 600, 420, 160, t, n=8, r=18)
    badge(frame, 160, 90, f"STEP {s['num']}", (200, 120, 60))
    word(frame, {"bowl": "MIX!", "roll": "ROLL!", "cut": "CUT!", "oven": "BAKE!", "decorate": "DECORATE!"}[key], t, s["say_t"], size=150, col=(200, 120, 60))
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.32)


COLRGB2 = {"red": (232, 53, 46), "green": (59, 193, 74), "gold": (240, 180, 20)}


def pat_thing(frame, v, x, y, sz):
    if v in COLRGB2:
        bauble(frame, x, y, sz * 0.4, COLRGB2[v])
    elif v == "star":
        item(frame, "topstar", x, y, sz)
    else:
        item(frame, v, x, y, sz)


def scene_pattern(frame, s, t):
    n = len(s["seq"]) + 1
    x0 = 960 - (n - 1) * 130
    d = ImageDraw.Draw(frame)
    d.line((x0 - 120, 330, x0 + (n - 1) * 260 + 120, 330), fill=(46, 158, 74), width=14)
    for i, v in enumerate(s["seq"]):
        pat_thing(frame, v, x0 + i * 260, 480, 200)
    x = x0 + (n - 1) * 260
    if t >= s["answer_t"]:
        pat_thing(frame, s["ans"], x, 480, 200)
        stars_ring(frame, x, 480, 150, 130, t, n=6, r=16)
    else:
        d.rounded_rectangle((x - 110, 370, x + 110, 590), radius=24, outline=(255, 255, 255), width=8)
        rt(frame, x, 480, "?", 150, colour=(255, 255, 255))
    word(frame, "WHAT COMES NEXT?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(150, 1770), scale=0.28)


def scene_bigsmall(frame, s, t):
    kinds = {"ball": "ball", "present": "present2", "star": "topstar"}
    big_left = s["kind2"] != "present"
    for j in range(2):
        x = 620 + j * 680
        big = (j == 0) == big_left
        good = t >= s["answer_t"] and big == (s["ans"] == "big")
        K.card(frame, x, 540, 520, 520, good=good)
        sz = 380 if big else 170
        if s["kind2"] == "ball":
            bauble(frame, x, 540, sz * 0.42)
        else:
            item(frame, kinds[s["kind2"]], x, 540, sz)
    word(frame, "BIGGER?" if s["ans"] == "big" else "SMALLER?", t, s["t0"], size=130)


def scene_sound(frame, s, t):
    full_tree(frame, t, cx=1560, by=1020, h=560)
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.6:
            for j in range(3):
                r = 120 + 100 * j + 120 * (q % 0.7)
                d.arc((760 - r, 520 - r, 760 + r, 520 + r), -50, 50, fill=(255, 255, 255, 210), width=10)
                d.arc((760 - r, 520 - r, 760 + r, 520 + r), 130, 230, fill=(255, 255, 255, 210), width=10)
        rt(frame, 760, 520, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], x=760, size=130)
    else:
        k = ease_back((t - s["answer_t"]) / 0.4)
        if s["key"] == "fire":
            d = ImageDraw.Draw(frame)
            d.ellipse((160, 660, 420, 760), outline=(255, 200, 40), width=12)
            word(frame, "FIRE!", t, s["answer_t"], x=760, size=150, col=(255, 140, 26))
        else:
            item(frame, s["key"], 760, 540, 380 * k)
            word(frame, {"bell": "BELLS!", "present1": "WRAPPING PAPER!", "santahat": "SANTA!"}[s["key"]], t, s["answer_t"], x=760, size=130)
    side_kids(frame, t, xs=(150, 1120), scale=0.28)


def scene_kindness(frame, s, t):
    full_tree(frame, t, cx=1560, by=1020, h=560)
    k = ease_back((t - s["t0"]) / 0.4)
    if s["key"] == "tree":
        item(frame, "tree", 760, 540, 400 * k)
    else:
        item(frame, s["key"], 760, 540 + 8 * math.sin(t * 2.5), 340 * k)
    item(frame, "heart", 980, 330 - 15 * abs(math.sin(t * 3)), 140)
    word(frame, "BE KIND!", t, s["say_t"], x=760, size=140, col=(255, 77, 109))
    side_kids(frame, t, "happy", xs=(150, 1120), scale=0.28)


def scene_snowman(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    d = ImageDraw.Draw(frame)
    cx = 960
    d.ellipse((560, 900, 1360, 1010), fill=(245, 250, 255))
    balls = [(cx, 800, 150), (cx, 590, 110), (cx, 430, 80)]
    for i in range(min(3, n)):
        x, y, r = balls[i]
        k = ease_back(min(1, (t - s["ts"][i]) / 0.4))
        d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), fill=(255, 255, 255), outline=INK, width=7)
    if n >= 4:
        for ex in (-28, 28):
            d.ellipse((cx + ex - 10, 410, cx + ex + 10, 430), fill=INK)
        d.polygon([(cx, 440), (cx + 70, 452), (cx, 462)], fill=(255, 138, 31), outline=INK)
        for yy in (560, 620, 760, 830):
            d.ellipse((cx - 10, yy - 10, cx + 10, yy + 10), fill=INK)
    if n >= 5:
        d.line((cx - 100, 580, cx - 230, 500), fill=(138, 90, 43), width=12)
        d.line((cx + 100, 580, cx + 230, 500), fill=(138, 90, 43), width=12)
    if n >= 6:
        item(frame, "santahat", cx + 10, 345, 170, rot=-10)
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "HELLO, SNOWMAN!", t, s["done_t"], size=130)
    else:
        word(frame, "BUILD A SNOWMAN!", t, s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(260, 1660), scale=0.36)


def scene_wrap(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    d = ImageDraw.Draw(frame)
    cx, cy = 960, 620
    if n <= 1:
        d.rectangle((cx - 180, cy - 120, cx + 180, cy + 130), fill=(210, 160, 110), outline=INK, width=7)
        item(frame, "teddy", cx, cy - 150 + (60 * min(1, (t - s["ts"][0]) / 0.8) if n else 0), 170)
    else:
        item(frame, "present2" if n < 4 else "present1", cx, cy, 380)
        if n >= 3:
            d.rectangle((cx - 30, cy - 140, cx + 30, cy + 120), fill=(255, 255, 255, 120))
        if n >= 5:
            d.rounded_rectangle((cx + 170, cy - 40, cx + 330, cy + 40), radius=12, fill=(255, 255, 255), outline=INK, width=5)
            rt(frame, cx + 250, cy, "GRANDMA", 30, colour=(255, 77, 109), maxw=150)
    labels = ["IN THE BOX!", "WRAP IT!", "TAPE IT!", "ADD A BOW!", "NAME TAG!"]
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "TA-DA!", t, s["done_t"], size=160)
    elif n:
        word(frame, labels[n - 1], t, s["ts"][n - 1], size=130)
    side_kids(frame, t, "happy", xs=(260, 1660), scale=0.36)


def scene_xornot(frame, s, t):
    rt(frame, 960, 150, s["q"], int(72 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)
    item(frame, s["key"], 960, 520, 320)
    if t >= s["answer_t"]:
        d = ImageDraw.Draw(frame)
        k = ease_back((t - s["answer_t"]) / 0.3)
        if s["good"]:
            d.line((800, 520, 920, 640, 1140, 380), fill=(59, 193, 74), width=int(40 * k) + 1, joint="curve")
            word(frame, "CHRISTMAS!", t, s["answer_t"], y=840, size=140, col=(59, 193, 74))
        else:
            r = 230 * k
            d.ellipse((960 - r, 520 - r, 960 + r, 520 + r), outline=(232, 53, 46), width=24)
            d.line((960 - r * 0.7, 520 + r * 0.7, 960 + r * 0.7, 520 - r * 0.7), fill=(232, 53, 46), width=24)
            word(frame, "NOT CHRISTMAS!", t, s["answer_t"], y=840, size=140, col=(232, 53, 46))
    side_kids(frame, t, xs=(170, 1750))


def scene_feel(frame, s, t):
    full_tree(frame, t, cx=1560, by=1020, h=560)
    body(frame, s["who"], t, s["emo"], 720, scale=0.6, hop=20 * abs(math.sin(t * 4)), wave=True)
    word(frame, s["emo"].upper() + "!", t, s["say_t"], x=720, size=150, col=(255, 77, 109))


def scene_hide(frame, s, t):
    tree(frame, 960, 640, 420, t)
    rev = t >= s["reveal_t"]
    for i, p in enumerate(("present1", "present2", "present3")):
        x = 560 + i * 400
        if rev and i == s["pos"]:
            k = min(1, (t - s["reveal_t"]) / 0.5)
            item(frame, s["key"], x, 820 - 60 * ease_back(k), 180)
            item(frame, p, x + 240 * k, 860 - 200 * k, 220, rot=40 * k)
            stars_ring(frame, x, 800, 180, 120, t, n=6, r=16)
        else:
            item(frame, p, x, 860, 220, rot=(6 * math.sin(t * 8 + i) if not rev else 0))
    word(frame, "FOUND IT!" if rev else "WHERE IS IT?", t, s["reveal_t"] if rev else s["t0"], size=130)
    side_kids(frame, t, xs=(150, 1770), scale=0.28)


def scene_chant(frame, s, t):
    tree(frame, 960, 1030, 760, t)
    for n, x in (("gul", 420), ("misheal", 1500)):
        body(frame, n, t, "happy", x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    word(frame, "JINGLE, JINGLE!", t, s["t0"], size=130)


SCENES = {"intro": scene_intro, "bring": scene_bring, "decor": scene_decor, "star": scene_star, "shape": scene_shape, "colour": scene_colour,
          "present": scene_present, "stockings": scene_stockings, "outro": scene_outro, "cword": scene_cword, "count": scene_count, "bake": scene_bake,
          "pattern": scene_pattern, "bigsmall": scene_bigsmall, "sound": scene_sound, "kindness": scene_kindness, "snowman": scene_snowman, "wrap": scene_wrap, "xornot": scene_xornot, "feel": scene_feel, "hide": scene_hide, "chant": scene_chant,
          "quiz": lambda f, s, t: K.scene_quiz(f, s, t, draw=quiz_draw),
          "dance": lambda f, s, t: (full_tree(f, t, cx=960, by=1060, h=420), K.scene_dance(f, s, t))}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L17 Christmas Tree", "Decorate the Christmas Tree for Kids")
K.CFG["title_items"] = ["topstar", "present1", "candycane", "bell", "gingerbread"]

if __name__ == "__main__":
    K.main()
