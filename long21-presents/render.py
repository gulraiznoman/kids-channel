"""Animate L21 "Christmas Presents".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW

A21, A17, L1, L4, L8 = HERE / "art", ROOT / "long17-xmastree/art", ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art", ROOT / "long08-colors-shapes/art"
ART = {k: A21 / f"item_{k}.png" for k in ("basketball", "rocket", "robot", "jackbox", "card", "paperchain", "bone")}
ART.update({k: A17 / f"item_{k}.png" for k in ("present1", "present2", "present3", "tree", "bell")})
ART.update({"firetruck": L1 / "fruit_firetruck.png", "piglet": L1 / "fruit_piglet.png", "puppy": L1 / "fruit_puppy.png", "kitten": L1 / "fruit_kitten.png",
            "bunny": L1 / "fruit_bunny.png", "monkey": L1 / "fruit_monkey.png", "fish": L1 / "fruit_fish.png",
            "duck": ROOT / "long11-bath/art/item_duck.png", "frog": L8 / "item_frog.png", "kite": L8 / "item_kite.png", "snowman": L8 / "item_snowman.png",
            "car": ROOT / "long16-sharing/art/item_car.png", "teddy": L4 / "item_teddy.png", "ball": L4 / "item_ball.png", "blocks": L4 / "item_blocks.png",
            "book": L4 / "item_book.png", "drum": ROOT / "long05-body-parts/art/item_drum.png", "flower": ROOT / "long05-body-parts/art/item_flower.png",
            "xylophone": ROOT / "long10-abc/art/item_xylophone.png", "balloons": ROOT / "long07-feelings/art/item_balloons.png",
            "crayons": ROOT / "long16-sharing/art/item_crayons.png", "heart": ROOT / "long16-sharing/art/item_heart.png",
            "carrot": ROOT / "long03-fruits-veg/art/item_carrot.png", "banana": ROOT / "ep01-fruits/art/fruit_banana.png"})
BGS = {"xmasroom": A17 / "bg_xmasroom.png", "northpole": ROOT / "long19-santa/art/bg_northpole.png"}
COL = {"red": (232, 53, 46), "orange": (255, 140, 26), "yellow": (245, 200, 30), "green": (59, 170, 74), "blue": (46, 130, 235), "purple": (140, 80, 210),
       "pink": (240, 110, 170), "brown": (150, 95, 50), "white": (245, 245, 250), "grey": (150, 155, 170), "gold": (240, 180, 20)}
ORDER = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "grey"]
TOYS = ["firetruck", "basketball", "duck", "frog", "car", "rocket", "piglet", "teddy", "snowman", "robot"]


def gbox(frame, x, y, w, col, rib=(255, 255, 255), lid=0.0, rot_dx=0):
    """gift box centred on x,y. lid 0 = closed, 1 = lid off"""
    d = ImageDraw.Draw(frame)
    h = w * 0.8
    d.rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), fill=col, outline=INK, width=max(3, int(w / 60)))
    d.rectangle((x - w * 0.08, y - h / 2, x + w * 0.08, y + h / 2), fill=rib, outline=INK, width=max(2, int(w / 90)))
    if lid < 0:
        return
    ly = y - h / 2 + lid * h * 0.95
    lx = x + lid * w * 1.05 + rot_dx
    d.rectangle((lx - w * 0.56, ly - w * 0.13, lx + w * 0.56, ly + w * 0.05), fill=col, outline=INK, width=max(3, int(w / 60)))
    d.rectangle((lx - w * 0.08, ly - w * 0.13, lx + w * 0.08, ly + w * 0.05), fill=rib, outline=INK, width=max(2, int(w / 90)))
    for s in (-1, 1):
        d.ellipse((lx + s * w * 0.14 - w * 0.13, ly - w * 0.28, lx + s * w * 0.14 + w * 0.13, ly - w * 0.13), fill=rib, outline=INK, width=max(2, int(w / 80)))


def rib(c):
    return (255, 215, 60) if c != "yellow" else (232, 53, 46)


def scene_intro(frame, s, t):
    q = t - s["shake_t"]
    for j, c in enumerate(("red", "blue", "green", "yellow", "purple", "pink")):
        x, y = 560 + (j % 3) * 400, 480 + (j // 3) * 260
        sh = 10 * math.sin(t * 30 + j) if q < 1.0 else 3 * math.sin(t * 8 + j)
        gbox(frame, x + sh, y, 280, COL[c], rib(c))
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(190, 1730), scale=0.36)
        rt(frame, 960, 130, "CHRISTMAS PRESENTS!", int(140 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)


def progress(frame, upto):
    for i, c in enumerate(ORDER):
        x = 330 + i * 140
        if i < upto:
            d = ImageDraw.Draw(frame)
            d.rounded_rectangle((x - 60, 930, x + 60, 1050), radius=16, fill=(255, 255, 255), outline=INK, width=4)
            item(frame, TOYS[i], x, 990, 100)
        else:
            gbox(frame, x, 1000, 96, COL[c], rib(c))


def scene_surprise(frame, s, t):
    c = s["col"]
    x, y = 960, 620
    progress(frame, s["num"] - 1)
    if t < s["open_t"]:
        sh = 12 * math.sin(t * 30) if (t - s["shake_t"]) % 2.0 < 0.8 else 0
        gbox(frame, x + sh, y, 400, COL[c], rib(c), rot_dx=sh)
        rt(frame, x + 320, y - 240, "?", int(150 + 12 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, c.upper() + " PRESENT!", t, s["t0"], size=120, col=COL[c] if c != "white" else None)
    else:
        q = t - s["open_t"]
        gbox(frame, x, y + 110, 400, COL[c], rib(c), lid=min(1, q / 0.5))
        k = ease_back(q / 0.6)
        item(frame, s["key"], x, y - 170 * k, 420 * max(0.1, k))
        confetti(frame, t, s["open_t"])
        word(frame, s["w"] + "!", t, s["open_t"], size=120, col=COL[c] if c != "white" else None)
    badge(frame, 160, 90, f"{s['num']}/10", COL[c])
    side_kids(frame, t, "excited" if t >= s["open_t"] else None, xs=(190, 1730), scale=0.3)


def scene_allten(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    for i in range(n):
        x, y = 360 + (i % 5) * 300, 400 + (i // 5) * 310
        k = ease_back((t - s["ts"][i]) / 0.3)
        gbox(frame, x, y + 110, 180, COL[ORDER[i]], rib(ORDER[i]), lid=-1)
        item(frame, TOYS[i], x, y, 190 * k)
    word(frame, "10 TOYS!" if t >= s["sum_t"] else "10 COLOURS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=120)


def scene_parcel(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    cols = ["red", "green", "blue", "yellow", "purple"]
    x, y = 960, 600
    if t < s["open_t"]:
        for i in range(n, 5):
            sz = 560 - i * 70
            if i == n:
                d = ImageDraw.Draw(frame)
                gbox(frame, x, y, sz, COL[cols[i]], rib(cols[i]))
        if n and t - s["ts"][n - 1] < 0.6:
            q = (t - s["ts"][n - 1]) / 0.6
            for j in range(8):
                a = j * 0.8
                ImageDraw.Draw(frame).rectangle((x + 500 * q * math.cos(a) - 20, y + 300 * q * math.sin(a) - 30, x + 500 * q * math.cos(a) + 20, y + 300 * q * math.sin(a) + 30), fill=COL[cols[n - 1]], outline=INK)
        if n:
            badge(frame, 160, 90, f"{n}/5", COL[cols[n - 1]])
        word(frame, "RIP, RIP!" if n else "PASS THE PARCEL!", t, s["ts"][n - 1] if n else s["t0"], size=120)
    else:
        q = t - s["open_t"]
        item(frame, "jackbox", x, y - 10 * abs(math.sin(q * 8)) * max(0, 1 - q / 3), 620 * ease_back(q / 0.3))
        confetti(frame, t, s["open_t"])
        word(frame, "BOING!", t, s["open_t"], size=150)
    side_kids(frame, t, "excited" if t >= s["open_t"] else "happy", xs=(200, 1720), scale=0.32)


def scene_size(frame, s, t):
    ok = {"big": 0, "mid": 1, "small": 2}[s["ans"]]
    xs, ws, cs = (520, 1040, 1420), (460, 300, 170), ("red", "blue", "green")
    for j in range(3):
        good = t >= s["answer_t"] and j == ok
        bob = 25 * abs(math.sin((t - s["answer_t"]) * 6)) if good else 0
        gbox(frame, xs[j], 860 - ws[j] * 0.4 - bob, ws[j], COL[cs[j]], rib(cs[j]))
        if good:
            stars_ring(frame, xs[j], 860 - ws[j] * 0.4, ws[j] * 0.75, ws[j] * 0.6, t, n=8, r=18)
    word(frame, {"big": "BIGGEST!", "mid": "MEDIUM!", "small": "SMALLEST!"}[s["ans"]] if t >= s["answer_t"] else "WHICH ONE?", t, s["answer_t"] if t >= s["answer_t"] else s["t0"], size=120)
    side_kids(frame, t, xs=(150, 1770), scale=0.26)


def scene_tower(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    fell = t >= s["fall_t"]
    q = t - s["fall_t"]
    for i in range(n):
        c = ORDER[i]
        x, y = 960 + (18 if i % 2 else -18), 1000 - i * 82
        if fell:
            k = min(1, q / 0.8)
            a = (i - 4.5) * 0.45
            x, y = x + (i - 4.5) * 170 * k + 30 * math.sin(a), y + (960 - y) * k * k
            gbox(frame, x, y, 120, COL[c], rib(c))
        else:
            k = ease_back((t - s["ts"][i]) / 0.3)
            gbox(frame, x, y - 60 * (1 - k), 110, COL[c], rib(c))
    if n and not fell:
        rt(frame, 1480, 400, str(n), int(220 * ease_back((t - s["ts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    word(frame, "OH NO!" if fell else "PRESENT TOWER!", t, s["fall_t"] if fell else s["t0"], size=120)
    side_kids(frame, t, "surprised" if fell else "happy", xs=(240, 1680), scale=0.34)


def tie(frame, x, y, sz):
    d = ImageDraw.Draw(frame)
    u = sz / 10
    d.polygon([(x - u, y - 5 * u), (x + u, y - 5 * u), (x + u * 0.6, y - 3.4 * u), (x + 2 * u, y + 4 * u), (x, y + 5 * u), (x - 2 * u, y + 4 * u), (x - u * 0.6, y - 3.4 * u)],
              fill=(46, 130, 235), outline=INK)


def scene_family(frame, s, t):
    x, y = 860, 620
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((1240, 300, 1680, 460), radius=20, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, 1460, 335, "TO:", 44, colour=(120, 120, 140))
    rt(frame, 1460, 405, s["who"].upper(), 70, colour=(232, 53, 46), maxw=400)
    if t < s["open_t"]:
        gbox(frame, x, y, 400, COL["green"], (255, 215, 60))
    else:
        q = t - s["open_t"]
        gbox(frame, x, y + 110, 400, COL["green"], (255, 215, 60), lid=min(1, q / 0.5))
        k = max(0.1, ease_back(q / 0.6))
        if s["key"] == "tie":
            tie(frame, x, y - 170 * k, 340 * k)
        else:
            item(frame, s["key"], x, y - 170 * k, 340 * k)
    word(frame, "WHO IS IT FOR?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(200, 1740), scale=0.3)


def scene_pet(frame, s, t):
    item(frame, s["pet"], 620, 640 - 10 * abs(math.sin(t * 4)), 460)
    x, y = 1300, 640
    if t < s["open_t"]:
        gbox(frame, x, y, 340, COL["pink"], (255, 255, 255))
        rt(frame, x + 240, y - 200, "?", 130, colour=(232, 53, 46))
    else:
        q = t - s["open_t"]
        gbox(frame, x, y + 100, 340, COL["pink"], (255, 255, 255), lid=min(1, q / 0.5))
        k = max(0.1, ease_back(q / 0.6))
        item(frame, s["key"], x, y - 130 * k, 300 * k)
        stars_ring(frame, 620, 640, 280, 260, t, n=8, r=18)
    word(frame, "PRESENTS FOR PETS!", t, s["t0"], size=110)


def shape_box(frame, shp, x, y, r, good=False):
    d = ImageDraw.Draw(frame)
    o = (59, 193, 74) if good else INK
    wd = 14 if good else 7
    f = (255, 225, 160)
    if shp == "circle":
        d.ellipse((x - r, y - r, x + r, y + r), fill=f, outline=o, width=wd)
    elif shp == "square":
        d.rectangle((x - r, y - r, x + r, y + r), fill=f, outline=o, width=wd)
    else:
        d.polygon([(x, y - r * 1.2), (x + r, y), (x, y + r * 1.2), (x - r, y)], fill=f, outline=o)


def scene_boxfit(frame, s, t):
    q = t - s["answer_t"]
    sp = {"circle": 480, "square": 960, "diamond": 1440}
    for shp, x in sp.items():
        shape_box(frame, shp, x, 760, 170, good=t >= s["answer_t"] and shp == s["shp"])
    if t >= s["answer_t"]:
        k = ease_io(min(1, q / 0.6))
        item(frame, s["key"], 960 + (sp[s["shp"]] - 960) * k, 330 + 430 * k, 300 - 100 * k)
    else:
        item(frame, s["key"], 960, 340 + 10 * math.sin(t * 3), 300)
    word(frame, "WHICH BOX FITS?", t, s["t0"], size=100)


def scene_heavy(frame, s, t):
    d = ImageDraw.Draw(frame)
    k = ease_io(min(1, max(0, t - s["answer_t"]) / 0.8))
    dy = 110 * k
    d.polygon([(960, 640), (900, 880), (1020, 880)], fill=(190, 140, 90), outline=INK)
    d.line((460, 640 - dy * -1, 1460, 640 - dy), fill=(120, 80, 50), width=24)
    item(frame, s["h"], 520, 500 + dy, 280)
    item(frame, s["l"], 1400, 500 - dy, 280)
    if k >= 1:
        rt(frame, 520, 880, "HEAVY!", 90, colour=(232, 53, 46))
        rt(frame, 1400, 230, "LIGHT!", 90, colour=(46, 130, 235))
    word(frame, "HEAVY OR LIGHT?", t, s["t0"], size=100)


def scene_bows(frame, s, t):
    n = sum(1 for x in s["cts"] if t >= x)
    d0 = COL[s["col"]]
    for i in range(s["n"]):
        x = 960 + (i - (s["n"] - 1) / 2) * 280
        gbox(frame, x, 640, 220, (255, 255, 255), d0 if i < n else (225, 225, 235))
        if i < n:
            rt(frame, x, 800, str(i + 1), 70, colour=RAINBOW[i % 6])
    word(frame, f"{s['n']} {s['col'].upper()} BOWS!" if t >= s["sum_t"] else "COUNT THE BOWS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(140, 1780), scale=0.26)


def scene_sound(frame, s, t):
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.5:
            for j in range(3):
                r = 120 + 100 * j + 120 * (q % 0.7)
                d.arc((960 - r, 520 - r, 960 + r, 520 + r), -50, 50, fill=(255, 255, 255, 220), width=10)
                d.arc((960 - r, 520 - r, 960 + r, 520 + r), 130, 230, fill=(255, 255, 255, 220), width=10)
        gbox(frame, 960, 560, 340, COL["blue"], (255, 215, 60), rot_dx=6 * math.sin(t * 20))
        word(frame, "LISTEN!", t, s["t0"], size=130)
    else:
        item(frame, s["key"], 960, 560, 440 * ease_back((t - s["answer_t"]) / 0.4))
        word(frame, s["key"].upper() + "!", t, s["answer_t"], size=130)
    side_kids(frame, t, xs=(170, 1750), scale=0.3)


def scene_odd(frame, s, t):
    for i, key in enumerate(s["keys"]):
        x = 960 + (i - 1.5) * 400
        bad = t >= s["answer_t"] and i == s["bad"]
        card(frame, x, 580, 350, 350, good=bad, dim=t >= s["answer_t"] and not bad)
        item(frame, key, x, 580 - (25 * abs(math.sin((t - s["answer_t"]) * 6)) if bad else 0), 260)
    word(frame, "WHICH ONE IS DIFFERENT?", t, s["t0"], size=100)
    side_kids(frame, t, xs=(100, 1820), scale=0.22)


def scene_make(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 760, 540, 560, 560)
    item(frame, s["key"], 760, 540 + 8 * math.sin(t * 2.5), 400 * k)
    badge(frame, 160, 90, f"STEP {s['num']}", (255, 77, 109))
    rt(frame, 1350, 540, {"card": "DRAW!", "crayons": "COLOUR!", "paperchain": "LOOP!", "heart": "I LOVE YOU!"}[s["key"]], int(110 * k), colour=(255, 77, 109), maxw=620)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.28)


def scene_manner(frame, s, t):
    if s["k"] == 2:
        body(frame, "gul", t, "happy", 800, scale=0.55)
        body(frame, "misheal", t, "happy", 1120, scale=0.55)
    else:
        n = "gul" if s["k"] % 2 == 0 else "misheal"
        body(frame, n, t, "happy", 620, scale=0.58, hop=15 * abs(math.sin(t * 4)), wave=True)
        item(frame, ("card", "heart", "", "teddy")[s["k"]], 1320, 560, 340 * ease_back((t - s["t0"]) / 0.4))
    item(frame, "heart", 960, 330 - 15 * abs(math.sin(t * 3)), 130) if s["k"] == 2 else None
    word(frame, s["w"], t, s["say_t"], size=130, col=(255, 77, 109))


def scene_giving(frame, s, t):
    item(frame, "tree", 960, 620, 620)
    body(frame, "gul", t, "happy", 460, scale=0.5, wave=True)
    body(frame, "misheal", t, "happy", 1460, scale=0.5, wave=True)
    gbox(frame, 710, 880, 170, COL["red"], (255, 215, 60))
    gbox(frame, 1210, 880, 170, COL["blue"], (255, 215, 60))
    word(frame, "GIVING IS FUN!", t, s["t0"], size=120)


def scene_gone(frame, s, t):
    n = len(s["keys"])
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((220, 640, 1700, 690), radius=12, fill=(200, 140, 90), outline=INK, width=6)
    for i, key in enumerate(s["keys"]):
        x = 960 + (i - (n - 1) / 2) * 400
        if t >= s["open_t"] and i == s["gone"]:
            if t >= s["answer_t"]:
                item(frame, key, x, 500, 280 * ease_back((t - s["answer_t"]) / 0.4))
                stars_ring(frame, x, 500, 190, 170, t, n=6, r=16)
            else:
                rt(frame, x, 500, "?", int(170 + 12 * math.sin(t * 6)), colour=(255, 77, 109))
        else:
            item(frame, key, x, 500, 280)
    if s["close_t"] <= t < s["open_t"]:
        frame.alpha_composite(Image.new("RGBA", frame.size, (30, 30, 70, 255)))
        rt(frame, 960, 520, "CLOSE YOUR EYES!", 130, colour=(255, 230, 120), maxw=1500)
        return
    word(frame, "WHICH TOY IS GONE?", t, s["t0"], size=100)
    side_kids(frame, t, xs=(120, 1800), scale=0.24)


def scene_more(frame, s, t):
    for j, (nm, n, who) in enumerate((("gul", s["g"], "gul"), ("misheal", s["m"], "mishu"))):
        cx = 540 + j * 840
        good = t >= s["answer_t"] and s["ans"] in (who, "same")
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((cx - 330, 330, cx + 330, 790), radius=30, fill=(255, 255, 255), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        for i in range(n):
            gbox(frame, cx - 200 + (i % 3) * 200, 440 + (i // 3) * 210, 130, COL[ORDER[i]], rib(ORDER[i]))
        rt(frame, cx, 730, str(n), 90, colour=RAINBOW[n % 6])
        body(frame, nm, t, "excited" if good else None, 90 if j == 0 else 1830, scale=0.24)
    lab = "THE SAME!" if s["ans"] == "same" else "MORE!"
    word(frame, lab if t >= s["answer_t"] else "WHO HAS MORE?", t, s["answer_t"] if t >= s["answer_t"] else s["t0"], size=120)


def scene_tidy(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, lab in enumerate(("ANIMAL", "VEHICLE")):
        x = 430 + j * 1060
        good = t >= s["answer_t"] and lab == s["ans"]
        d.rounded_rectangle((x - 300, 600, x + 300, 960), radius=30, fill=(150, 95, 50, 255), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        rt(frame, x, 880, lab, 76, colour=(255, 255, 255))
    if t >= s["answer_t"]:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x = 960 + ((430 if s["ans"] == "ANIMAL" else 1490) - 960) * k
        y, sz = 360 + 340 * k, 340 - 120 * k
    else:
        x, y, sz = 960, 360 + 10 * math.sin(t * 3), 340
    item(frame, s["key"], x, y, sz)
    word(frame, "TIDY UP!", t, s["t0"], y=100, size=110)


def quiz_draw(frame, vis, t, k):
    item(frame, vis, 960, 580, 400 * k)


def scene_outro(frame, s, t):
    item(frame, "tree", 960, 660, 680)
    for j, c in enumerate(("red", "blue", "green")):
        gbox(frame, 760 + j * 200, 950, 150, COL[c], rib(c))
    for n, x in (("gul", 420), ("misheal", 1500)):
        body(frame, n, t, "happy", x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "MERRY CHRISTMAS!", int(160 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "THANK YOU!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


SCENES = {"intro": scene_intro, "surprise": scene_surprise, "allten": scene_allten, "parcel": scene_parcel, "size": scene_size, "tower": scene_tower,
          "family": scene_family, "pet": scene_pet, "boxfit": scene_boxfit, "heavy": scene_heavy, "bows": scene_bows, "sound": scene_sound,
          "gone": scene_gone, "more": scene_more, "tidy": scene_tidy, "odd": scene_odd, "make": scene_make, "manner": scene_manner, "giving": scene_giving, "outro": scene_outro,
          "quiz": lambda f, s, t: K.scene_quiz(f, s, t, draw=quiz_draw),
          "dance": lambda f, s, t: (gbox(f, 1720, 860, 220, COL["red"], (255, 215, 60)), K.scene_dance(f, s, t))}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L21 Christmas Presents", "Christmas Presents for Kids")
K.CFG["title_items"] = ["present1", "present2", "teddy", "rocket", "firetruck"]

if __name__ == "__main__":
    K.main()
