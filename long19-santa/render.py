"""Animate L19 "Santa Claus & Christmas Eve".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW

A19, A17 = HERE / "art", ROOT / "long17-xmastree/art"
ART = {k: A19 / f"item_{k}.png" for k in ("santa", "greensanta", "reindeer", "sleigh", "letter", "chimney", "milk", "toytrain")}
ART.update({k: A17 / f"item_{k}.png" for k in ("present1", "present2", "present3", "stocking", "santahat", "snowflake", "topstar", "tree", "bell")})
ART.update({"teddy": ROOT / "long15-potty/art/item_teddy.png", "car": ROOT / "long16-sharing/art/item_car.png",
            "ball": ROOT / "long04-good-habits/art/item_ball.png", "crayons": ROOT / "long16-sharing/art/item_crayons.png",
            "blocks": ROOT / "long04-good-habits/art/item_blocks.png", "cookie": ROOT / "long16-sharing/art/item_cookie.png",
            "plate": ROOT / "long16-sharing/art/item_plate.png", "carrot": ROOT / "long03-fruits-veg/art/item_carrot.png",
            "pyjamas": ROOT / "long11-bath/art/item_pyjamas.png", "toothbrush": ROOT / "long04-good-habits/art/item_toothbrush.png",
            "moon": ROOT / "long04-good-habits/art/item_moon.png", "sunny": ROOT / "long01-animals-fun/art/fruit_sunny.png",
            "heart": ROOT / "long16-sharing/art/item_heart.png", "house": ROOT / "long18-days/art/item_house.png",
            "scarf": ROOT / "long04-good-habits/art/item_scarf.png", "boots": ROOT / "long04-good-habits/art/item_boots.png",
            "mitt": ROOT / "long20-cooking/art/item_mitt.png", "gingerbread": A17 / "item_gingerbread.png"})
BGS = {"northpole": A19 / "bg_northpole.png", "roof": A19 / "bg_roof.png", "xmasroom": A17 / "bg_xmasroom.png"}
KEYMAP = {"toycar": "car", "sunglasses": "greensanta"}
NAMES = ["DASHER", "DANCER", "PRANCER", "VIXEN", "COMET", "CUPID", "DONDER", "BLITZEN"]


def team(frame, x, y, t, s=1.0, deer=2):
    """sleigh with reindeer in front (to the right); x, y = sleigh centre"""
    d = ImageDraw.Draw(frame)
    for j in range(deer):
        dx = x + (200 + j * 190) * s
        dy = y - 30 * s + 12 * s * math.sin(t * 8 + j)
        d.line((x + 120 * s, y, dx - 60 * s, dy + 20 * s), fill=(200, 160, 64), width=max(2, int(6 * s)))
        item(frame, "reindeer", dx, dy, 200 * s, flip=True)
    item(frame, "santa", x + 10 * s, y - 95 * s, 150 * s)
    item(frame, "sleigh", x, y, 260 * s)


def santa_pt(cx, cy, S, sx, sy):
    return cx + (sx - 210) * S / 358, cy + (sy - 201) * S / 358


def scene_intro(frame, s, t):
    q = t - s["fly_t"]
    if q >= 0:
        x = -400 + q * 900
        team(frame, x, 300 - 80 * math.sin(min(x, 2400) / 2400 * math.pi), t, s=0.7, deer=3)
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(260, 1660), scale=0.4)
        rt(frame, 960, 140, "CHRISTMAS EVE!", int(170 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)
        item(frame, "santa", 960, 640, 420 * ease_back((t - s["title_t"] - 0.3) / 0.4))


def scene_meet(frame, s, t):
    item(frame, "santa", 960, 600 - 20 * abs(math.sin(t * 4)), 640)
    if t >= s["ho_t"]:
        for j, w in enumerate(("HO!", "HO!", "HO!")):
            k = ease_back((t - s["ho_t"] - j * 0.4) / 0.3)
            if k > 0.05:
                rt(frame, 520 + j * 440, 170 - j * 20, w, int(130 * k), colour=(232, 53, 46))
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.32)


SPOTS = {"hat": (205, 60), "beard": (200, 200), "coat": (150, 240), "belt": (200, 287), "boots": (200, 350)}


def scene_part(frame, s, t):
    S, cx, cy = 760, 760, 600
    item(frame, "santa", cx, cy, S)
    x, y = santa_pt(cx, cy, S, *SPOTS[s["part"]])
    k = ease_back((t - s["t0"]) / 0.4)
    d = ImageDraw.Draw(frame)
    r = 120 * k + 8 * math.sin(t * 6)
    d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 210, 40), width=14)
    d.line((x + r, y, 1300, y), fill=(255, 210, 40), width=8)
    rt(frame, 1550, y, s["part"].upper() + "!", int(110 * k), colour=(232, 53, 46), maxw=520)
    badge(frame, 160, 90, f"{list(SPOTS).index(s['part']) + 1}/5", (232, 53, 46))


def scene_letter(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    lines = ["Dear Santa,", "I shared my toys,", "and I helped my mama.", "May I please have", "a teddy bear?", "Thank you!", "Love, Mishu"]
    upto = {0: 0, 1: 1, 2: 3, 3: 5, 4: 7, 5: 7}[n]
    if n < 5:
        card(frame, 820, 560, 860, 820)
        for j in range(upto):
            rt(frame, 820, 220 + j * 100, lines[j], 56, colour=(232, 53, 46) if j in (0, 6) else (60, 60, 90), maxw=780)
        if upto < 7:
            x = 640 + 200 * math.sin(t * 7)
            d = ImageDraw.Draw(frame)
            d.line((x, 240 + upto * 100, x + 60, 160 + upto * 100), fill=INK, width=14)
        body(frame, "misheal", t, "happy", 1550, scale=0.5)
    else:
        q = t - s["ts"][4]
        item(frame, "letter", 820 + q * 900, 560 - q * 500, 380 * max(0.2, 1 - q * 0.4), rot=q * 40)
        word(frame, "TO THE NORTH POLE!", t, s["ts"][4], size=110)
        body(frame, "misheal", t, "excited", 1550, scale=0.5, wave=True)


def scene_workshop(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    toys = ["teddy", "car", "ball", "toytrain", "crayons", "blocks"]
    card(frame, 1100, 560, 1300, 760)
    for i in range(n):
        x, y = 650 + (i % 3) * 450, 380 + (i // 3) * 350
        k = ease_back((t - s["ts"][i]) / 0.35)
        item(frame, toys[i], x, y, 260 * k, rot=5 * math.sin(t * 2 + i))
        rt(frame, x - 150, y - 120, str(i + 1), 60, colour=RAINBOW[i % 6])
    item(frame, "santa", 200, 760, 360)
    word(frame, "6 TOYS!" if t >= s["sum_t"] else "SANTA'S WORKSHOP!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)


def scene_load(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    item(frame, "sleigh", 860, 720, 760)
    keys = ("present1", "present2", "present3")
    for i in range(n):
        x = 720 + (i % 4) * 110 - (i // 4) * 40
        y = 540 - (i // 4) * 105
        k = ease_back((t - s["ts"][i]) / 0.3)
        item(frame, keys[i % 3], x, y - 80 * (1 - k), 120)
    if n:
        rt(frame, 1520, 380, str(n), int(220 * ease_back((t - s["ts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    word(frame, f"{n} PRESENTS!" if n else "LOAD THE SLEIGH!", t, s["ts"][n - 1] if n else s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(170, 1750), scale=0.3)


def scene_deer(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    for i in range(n):
        x, y = 300 + (i % 4) * 440, 420 + (i // 4) * 360
        k = ease_back((t - s["ts"][i]) / 0.35)
        item(frame, "reindeer", x, y - 10 * abs(math.sin(t * 4 + i)), 260 * k, flip=i % 2 == 1)
        rt(frame, x, y + 150, NAMES[i], int(48 * k), colour=(232, 53, 46), maxw=400)
        rt(frame, x - 150, y - 120, str(i + 1), int(56 * k), colour=RAINBOW[i % 6])
    word(frame, "8 REINDEER!" if t >= s["sum_t"] else "MEET THE REINDEER!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)


def scene_deerfact(frame, s, t):
    k = s["k"]
    item(frame, "reindeer", 760, 600, 640)
    if k == 0:
        d = ImageDraw.Draw(frame)
        r = 150 + 8 * math.sin(t * 6)
        d.ellipse((560 - r, 300 - r, 560 + r, 300 + r), outline=(255, 210, 40), width=14)
        word(frame, "ANTLERS!", t, s["say_t"], x=1450, y=500, size=130)
    elif k == 1:
        for j in range(14):
            item(frame, "snowflake", (j * 157) % 1920, ((t * 120 + j * 140) % 1200) - 100, 60)
        word(frame, "SNOWY!", t, s["say_t"], x=1450, y=500, size=150, col=(46, 120, 230))
    else:
        item(frame, "carrot", 1400, 560, 300, rot=20 * math.sin(t * 3))
        word(frame, "CRUNCH!", t, s["say_t"], x=1400, y=250, size=130, col=(255, 140, 26))
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.24)


def scene_fly(frame, s, t):
    q = t - s["go_t"]
    n = sum(1 for x in s["ts"] if t >= x)
    for i in range(n):
        x = 220 + i * 370
        k = ease_back((t - s["ts"][i]) / 0.35)
        stars_ring(frame, x, 560, 80, 40, t, n=5, r=14)
        rt(frame, x, 470, str(i + 1), int(90 * k), colour=(255, 230, 120))
    x = -300 + (q * 330) % 2600
    team(frame, x, 300 + 40 * math.sin(t * 2), t, s=0.6, deer=3)
    word(frame, f"HOUSE {n}!" if n else "UP, UP, AND AWAY!", t, s["ts"][n - 1] if n else s["t0"], y=110, size=110)


def scene_chimney(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    cx, top = 960, 380
    q = t - s["ts"][n - 1] if n else 0
    if n == 1:
        item(frame, "santa", cx, top - 150 + 10 * abs(math.sin(t * 6)), 300)
    elif n == 2:
        item(frame, "santa", cx, top - 150 + min(1, q / 1.2) * 330, 300)
    elif n == 3:
        card(frame, 960, 560, 900, 620, fill=(70, 50, 110))
        item(frame, "tree", 760, 560, 480)
        for i, p in enumerate(("present1", "present2", "present3")):
            k = ease_back((q - i * 0.5) / 0.35)
            item(frame, p, 1060 + i * 120, 760, 150 * k)
        rt(frame, 1180, 400, "SHH!", 110, colour=(255, 255, 255))
        return
    elif n >= 4:
        item(frame, "santa", cx, top - 150 - min(1, q / 0.8) * 200, 300)
        if q > 0.8:
            team(frame, 960 + (q - 0.8) * 900, 180, t, s=0.5, deer=2)
    if n != 3:
        item(frame, "chimney", cx, 820, 700)
    labels = ["TAP, TAP, TAP!", "WHOOSH!", "SHH!", "AWAY HE GOES!"]
    word(frame, labels[n - 1] if n else "DOWN THE CHIMNEY!", t, s["ts"][n - 1] if n else s["t0"], size=120)


def scene_snack(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((360, 720, 1560, 800), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    if n >= 1:
        item(frame, "plate", 700, 690, 360)
        for i in range(3):
            item(frame, "cookie", 620 + i * 80, 660 - 10 * (i % 2), 130 * ease_back((t - s["ts"][0] - i * 0.2) / 0.3))
    if n >= 2:
        item(frame, "milk", 1060, 600, 300 * ease_back((t - s["ts"][1]) / 0.3))
    if n >= 3:
        for i in range(2):
            item(frame, "carrot", 1320 + i * 90, 640, 220 * ease_back((t - s["ts"][2] - i * 0.2) / 0.3), rot=-30 + i * 20)
    word(frame, "FOR SANTA!" if t < s["count_t"] else "THANK YOU, SANTA!", t, s["count_t"] if t >= s["count_t"] else s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(170, 1750), scale=0.32)


def scene_bed(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 760, 540, 560, 560)
    item(frame, s["key"], 760, 540 + 8 * math.sin(t * 2.5), 400 * k)
    badge(frame, 160, 90, f"STEP {s['num']}", (90, 90, 200))
    lab = {"pyjamas": "PYJAMAS!", "stocking": "STOCKING!", "toothbrush": "BRUSH!", "moon": "SLEEP!"}[s["key"]]
    rt(frame, 1350, 540, lab, int(110 * k), colour=(90, 90, 200), maxw=620)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.28)
    if s["key"] == "moon":
        frame.alpha_composite(Image.new("RGBA", frame.size, (10, 10, 50, int(120 * min(1, (t - s["t0"]) / 2)))))


def scene_night(frame, s, t):
    if t < s["away_t"]:
        q = t - s["land_t"]
        x = -500 + 1400 * ease_io(min(1, max(0, q) / 1.4))
        y = 200 + 420 * ease_io(min(1, max(0, q) / 1.4))
        team(frame, x, y, t, s=0.6, deer=3)
    else:
        q = t - s["away_t"]
        team(frame, 900 + q * 700, 620 - q * 300, t, s=0.6, deer=3)
    word(frame, "SHH! SANTA IS HERE!" if t < s["away_t"] else "GOOD NIGHT!", t, s["land_t"] if t < s["away_t"] else s["away_t"], size=110)


def full_tree(frame, t, cx=1560, by=1020, h=600):
    item(frame, "tree", cx, by - h / 2, h)
    for i, p in enumerate(("present1", "present2", "present3")):
        item(frame, p, cx - 170 + i * 170, by - 50, 130)


def scene_open(frame, s, t):
    full_tree(frame, t)
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
        word(frame, {"teddy": "TEDDY BEAR!", "toytrain": "TOY TRAIN!", "crayons": "CRAYONS!"}[s["inside"]], t, s["open_t"], x=800, size=130)
    side_kids(frame, t, "excited", xs=(150, 1100), scale=0.28)


def scene_eaten(frame, s, t):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((360, 720, 1560, 800), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    item(frame, "plate", 700, 690, 360)
    for i in range(6):
        d.ellipse((620 + i * 30, 680 - (i % 2) * 14, 632 + i * 30, 692 - (i % 2) * 14), fill=(190, 130, 60))
    if t >= s["note_t"]:
        k = ease_back((t - s["note_t"]) / 0.4)
        card(frame, 1200, 480, 600 * k, 400 * k)
        if k > 0.5:
            rt(frame, 1200, 400, "THANK YOU!", 70, colour=(232, 53, 46))
            rt(frame, 1200, 520, "LOVE, SANTA", 60, colour=(46, 158, 74))
        stars_ring(frame, 1200, 480, 340, 230, t, n=8, r=16)
    word(frame, "THE COOKIES ARE GONE!", t, s["t0"], size=110)
    side_kids(frame, t, "surprised", xs=(170, 1750), scale=0.3)


def scene_yesno(frame, s, t):
    rt(frame, 960, 150, s["q"], int(72 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)
    item(frame, KEYMAP.get(s["key"], s["key"]), 960, 520, 340)
    if t >= s["answer_t"]:
        d = ImageDraw.Draw(frame)
        k = ease_back((t - s["answer_t"]) / 0.3)
        if s["good"]:
            d.line((800, 520, 920, 640, 1140, 380), fill=(59, 193, 74), width=int(40 * k) + 1, joint="curve")
            word(frame, "YES!", t, s["answer_t"], y=860, size=160, col=(59, 193, 74))
        else:
            r = 230 * k
            d.ellipse((960 - r, 520 - r, 960 + r, 520 + r), outline=(232, 53, 46), width=24)
            d.line((960 - r * 0.7, 520 + r * 0.7, 960 + r * 0.7, 520 - r * 0.7), fill=(232, 53, 46), width=24)
            word(frame, "NO!", t, s["answer_t"], y=860, size=160, col=(232, 53, 46))
    side_kids(frame, t, xs=(170, 1750))


def scene_sound(frame, s, t):
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.6:
            for j in range(3):
                r = 120 + 100 * j + 120 * (q % 0.7)
                d.arc((960 - r, 520 - r, 960 + r, 520 + r), -50, 50, fill=(255, 255, 255, 210), width=10)
                d.arc((960 - r, 520 - r, 960 + r, 520 + r), 130, 230, fill=(255, 255, 255, 210), width=10)
        rt(frame, 960, 520, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], size=130)
    else:
        k = ease_back((t - s["answer_t"]) / 0.4)
        item(frame, s["key"], 960, 560, 440 * k)
        word(frame, {"santa": "SANTA!", "sleigh": "SLEIGH BELLS!", "reindeer": "REINDEER!", "chimney": "CHIMNEY!"}[s["key"]], t, s["answer_t"], size=130)
    side_kids(frame, t, xs=(170, 1750), scale=0.3)


def dressed(frame, t, n, cx, feet, sc, hop):
    """Gul with santa pieces; n pieces worn (hat, beard, coat, belt, boots)"""
    top = feet - 1860 * sc - hop
    P = lambda x, y: (cx + (x - 600) * sc, top + y * sc)
    d = ImageDraw.Draw(frame)
    body(frame, "gul", t, "happy", cx, feet=feet, scale=sc, hop=hop)
    if n >= 3:
        a, b = P(355, 985), P(845, 1440)
        d.rounded_rectangle((*a, *b), radius=int(60 * sc), fill=(232, 53, 46), outline=INK, width=5)
        d.rectangle((P(570, 985)[0], a[1], P(630, 985)[0], b[1]), fill=(255, 255, 255))
        d.rounded_rectangle((a[0] - 6, P(0, 1390)[1], b[0] + 6, b[1] + 10), radius=20, fill=(255, 255, 255), outline=INK, width=4)
    if n >= 4:
        d.rectangle((P(355, 1300)[0], P(0, 1300)[1], P(845, 0)[0], P(0, 1360)[1]), fill=(43, 43, 51), outline=INK, width=4)
        d.rectangle((P(560, 0)[0], P(0, 1290)[1], P(640, 0)[0], P(0, 1370)[1]), fill=(255, 210, 40), outline=INK, width=4)
    if n >= 5:
        for x in (480, 720):
            d.rounded_rectangle((*P(x - 85, 1740), *P(x + 85, 1860)), radius=int(40 * sc), fill=(43, 43, 51), outline=INK, width=4)
    if n >= 2:
        d.ellipse((*P(420, 830), *P(780, 1120)), fill=(255, 255, 255), outline=INK, width=4)
        d.ellipse((*P(500, 870), *P(700, 930)), fill=(120, 60, 50))
    if n >= 1:
        x, y = P(620, 150)
        item(frame, "santahat", x, y, 640 * sc, rot=-12)


def scene_dress(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    dressed(frame, t, n, 960, 1060, 0.5, 0)
    labs = ["HAT!", "BEARD!", "COAT!", "BELT!", "BOOTS!"]
    for i in range(5):
        x = 260 if i < 3 else 1660
        y = 300 + (i % 3) * 220
        card(frame, x, y, 300, 160, good=i < n, dim=i >= n)
        rt(frame, x, y, labs[i], 56, colour=(232, 53, 46))
    body(frame, "misheal", t, "happy", 1660, scale=0.3) if n < 4 else None
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "SANTA GUL!", t, s["done_t"], size=140)
    else:
        word(frame, "DRESS UP!", t, s["t0"], size=120)


def scene_kind(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    vis = ["santa", "teddy", "present2", "heart"][s["k"]]
    item(frame, vis, 760, 540, 400 * k)
    item(frame, "heart", 1000, 300 - 15 * abs(math.sin(t * 3)), 140)
    word(frame, ["BE KIND!", "SHARE!", "PLEASE & THANK YOU!", "BIG HUG!"][s["k"]], t, s["say_t"], x=1300, y=540, size=110, col=(255, 77, 109), maxw=900)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.28)


def scene_chant(frame, s, t):
    q = t - s["t0"]
    team(frame, -300 + (q * 400) % 2600, 330 + 40 * math.sin(t * 2), t, s=0.55, deer=3)
    for n, x in (("gul", 560), ("misheal", 1360)):
        body(frame, n, t, "happy", x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    word(frame, "JINGLE BELLS!", t, s["t0"], y=130, size=130)


def scene_outro(frame, s, t):
    q = t - s["t0"]
    team(frame, -300 + q * 420, 330, t, s=0.55, deer=3)
    for n, x in (("gul", 560), ("misheal", 1360)):
        body(frame, n, t, "happy", x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "MERRY CHRISTMAS!", int(150 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)


COLRGB = {"red": (232, 53, 46), "white": (255, 255, 255), "black": (43, 43, 51), "gold": (240, 180, 20), "brown": (150, 95, 50)}
CSPOT = {"red": (150, 240), "white": (200, 200), "black": (200, 350), "gold": (200, 287)}


def scene_colour(frame, s, t):
    S, cx, cy = 680, 760, 600
    item(frame, s["key"], cx, cy, S)
    if t >= s["answer_t"]:
        if s["col"] in CSPOT:
            x, y = santa_pt(cx, cy, S, *CSPOT[s["col"]])
            r = 90 + 8 * math.sin(t * 6)
            ImageDraw.Draw(frame).ellipse((x - r, y - r, x + r, y + r), outline=(255, 210, 40), width=12)
        word(frame, s["col"].upper() + "!", t, s["answer_t"], x=1450, y=500, size=160, col=COLRGB[s["col"]])
    else:
        word(frame, "WHAT COLOUR?", t, s["t0"], x=1450, y=500, size=110)
    side_kids(frame, t, xs=(1300, 1700), scale=0.26)


def scene_warm(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    keys = ["santahat", "scarf", "mitt", "boots"]
    labs = ["HAT!", "SCARF!", "MITTENS!", "BOOTS!"]
    for i in range(n):
        x = 330 + i * 420
        k = ease_back((t - s["ts"][i]) / 0.35)
        card(frame, x, 520, 360, 360, good=True)
        item(frame, keys[i], x, 520, 260 * k)
        rt(frame, x, 780, labs[i], int(64 * k), colour=(46, 120, 230))
    for j in range(10):
        item(frame, "snowflake", (j * 197) % 1920, ((t * 100 + j * 120) % 1200) - 100, 50)
    word(frame, "BRRR! WRAP UP WARM!", t, s["t0"], size=110)


def scene_cookies(frame, s, t):
    n, eat = s["n"], s["eat"]
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((360, 720, 1560, 800), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    item(frame, "plate", 860, 680, 700)
    eaten = t >= s["eat_t"]
    for i in range(n):
        x = 860 + (i - (n - 1) / 2) * 120
        if eaten and i >= n - eat:
            k = min(1, (t - s["eat_t"]) / 0.6)
            if k < 1:
                item(frame, "cookie", x, 650 - 200 * k, 120 * (1 - k))
            continue
        item(frame, "cookie", x, 650, 120)
    item(frame, "santa", 1550, 560, 380)
    if t >= s["answer_t"]:
        left = n - eat
        word(frame, f"{n} - {eat} = {left}", t, s["answer_t"], y=200, size=150, col=(232, 53, 46))
    elif eaten:
        word(frame, f"{n} - {eat} = ?", t, s["eat_t"], y=200, size=150)
    else:
        word(frame, f"{n} COOKIES", t, s["t0"], y=200, size=130)


def scene_hide(frame, s, t):
    rev = t >= s["reveal_t"]
    full = ("present1", "present2", "present3")
    for i, p in enumerate(full):
        x = 560 + i * 400
        if rev and i == s["pos"]:
            k = min(1, (t - s["reveal_t"]) / 0.5)
            item(frame, s["key"], x, 760 - 60 * ease_back(k), 220)
            item(frame, p, x + 240 * k, 800 - 200 * k, 280, rot=40 * k)
            stars_ring(frame, x, 740, 200, 130, t, n=6, r=16)
        else:
            item(frame, p, x, 800, 280, rot=(6 * math.sin(t * 8 + i) if not rev else 0))
    word(frame, "FOUND IT!" if rev else "WHERE IS IT?", t, s["reveal_t"] if rev else s["t0"], size=130)
    side_kids(frame, t, xs=(150, 1770), scale=0.28)


def scene_pattern(frame, s, t):
    n = len(s["seq"]) + 1
    x0 = 960 - (n - 1) * 130
    for i, v in enumerate(s["seq"]):
        item(frame, v, x0 + i * 260, 520, 210)
    x = x0 + (n - 1) * 260
    if t >= s["answer_t"]:
        item(frame, s["ans"], x, 520, 210)
        stars_ring(frame, x, 520, 150, 130, t, n=6, r=16)
    else:
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((x - 110, 410, x + 110, 630), radius=24, outline=(255, 255, 255), width=8)
        rt(frame, x, 520, "?", 150, colour=(255, 255, 255))
    word(frame, "WHAT COMES NEXT?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(150, 1770), scale=0.28)


def scene_countdown(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    if t >= s["go_t"]:
        confetti(frame, t, s["go_t"])
        item(frame, "santa", 960, 600, 460 * ease_back((t - s["go_t"]) / 0.4))
        word(frame, "MERRY CHRISTMAS!", t, s["go_t"], size=140)
    elif n:
        rt(frame, 960, 520, str(11 - n), int(380 * ease_back((t - s["ts"][n - 1]) / 0.25)), colour=RAINBOW[n % 6])
    else:
        word(frame, "COUNTDOWN!", t, s["t0"], size=140)
    side_kids(frame, t, "excited", xs=(250, 1670), scale=0.4)


def scene_feel(frame, s, t):
    full_tree(frame, t)
    body(frame, s["who"], t, s["emo"], 720, scale=0.6, hop=20 * abs(math.sin(t * 4)) if s["emo"] != "tired" else 0, wave=s["emo"] != "tired")
    word(frame, {"tired": "SLEEPY!"}.get(s["emo"], s["emo"].upper() + "!"), t, s["say_t"], x=720, size=150, col=(255, 77, 109))


SCENES = {"intro": scene_intro, "meet": scene_meet, "part": scene_part, "letter": scene_letter, "workshop": scene_workshop, "load": scene_load,
          "deer": scene_deer, "deerfact": scene_deerfact, "fly": scene_fly, "chimney": scene_chimney, "snack": scene_snack, "bed": scene_bed,
          "night": scene_night, "open": scene_open, "eaten": scene_eaten, "yesno": scene_yesno, "sound": scene_sound, "dress": scene_dress,
          "kind": scene_kind, "chant": scene_chant, "outro": scene_outro,
          "colour": scene_colour, "warm": scene_warm, "cookies": scene_cookies, "hide": scene_hide, "pattern": scene_pattern,
          "countdown": scene_countdown, "feel": scene_feel,
          "dance": lambda f, s, t: (item(f, "santa", 1700, 640, 340), K.scene_dance(f, s, t))}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L19 Santa Christmas Eve", "Santa Claus for Kids")
K.CFG["title_items"] = ["santa", "reindeer", "sleigh", "present1", "cookie"]

if __name__ == "__main__":
    K.main()
