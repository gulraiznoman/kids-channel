"""Animate L20 "Cooking for Kids".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, choice_row, INK, RAINBOW

A20, L4, F = HERE / "art", ROOT / "long04-good-habits/art", ROOT / "ep01-fruits/art"
ART = {k: A20 / f"item_{k}.png" for k in ("chefhat", "apron", "rollingpin", "whisk", "mitt", "flour", "cheese", "sauce", "olive", "pepper",
                                           "mushroom", "blender", "smoothie", "skewer", "oven", "knife", "fridge")}
ART.update({k: L4 / f"item_{k}.png" for k in ("hands", "soap", "milk", "chips", "teddy", "shoes", "book", "plates", "ball", "toothbrush")})
ART.update({k: F / f"fruit_{k}.png" for k in ("strawberry", "banana", "orange", "pineapple", "kiwi", "grapes", "watermelon")})
ART.update({"bowl": ROOT / "long03-fruits-veg/art/item_bowl.png", "pot": ROOT / "long03-fruits-veg/art/item_pot.png",
            "carrot": ROOT / "long03-fruits-veg/art/item_carrot.png", "spoon": ROOT / "long11-bath/art/item_spoon.png",
            "sponge": ROOT / "long11-bath/art/item_sponge.png", "pizza": ROOT / "long08-colors-shapes/art/item_pizza.png",
            "icecream": ROOT / "long05-body-parts/art/item_icecream.png", "car": ROOT / "long16-sharing/art/item_car.png",
            "egg": L4 / "item_egg.png", "toast": L4 / "item_toast.png", "donut": L4 / "item_donut.png", "cup": L4 / "item_water.png",
            "broccoli": ROOT / "long03-fruits-veg/art/item_broccoli.png", "apple": F / "fruit_apple.png",
            "cupcake": ROOT / "long08-colors-shapes/art/item_cupcake.png", "cookie": ROOT / "long16-sharing/art/item_cookie.png",
            "plate": ROOT / "long16-sharing/art/item_plate.png"})
BGS = {"kitchen": ROOT / "long03-fruits-veg/art/bg_kitchen.png"}
CRUST, SAUCE, CHEESE = (232, 180, 110), (214, 58, 40), (255, 214, 80)
TOPKEYS = ["olive", "pepper", "mushroom"]


def top_spots(n_each, r):
    out, k = [], 0
    for ti, n in enumerate(n_each):
        for i in range(n):
            a = k * 2.399
            rr = r * (0.18 + 0.55 * ((k * 0.37) % 1))
            out.append((TOPKEYS[ti], rr * math.cos(a), rr * math.sin(a), k))
            k += 1
    return out


def pizza(frame, cx, cy, r, sauce=1.0, cheese=1.0, tops=(0, 0, 0), new_t=None, t=0, slices=0, face=0):
    d = ImageDraw.Draw(frame)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CRUST, outline=INK, width=8)
    if sauce > 0:
        s = r * 0.86 * sauce
        d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=SAUCE)
    if cheese > 0:
        for j in range(int(40 * cheese)):
            a, rr = j * 2.399, r * 0.75 * math.sqrt((j * 0.61) % 1)
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            b = r * 0.19
            d.ellipse((x - b, y - b * 0.7, x + b, y + b * 0.7), fill=CHEESE)
    if face:
        if face >= 1:
            for ex in (-0.3, 0.3):
                item(frame, "olive", cx + ex * r, cy - 0.25 * r, r * 0.28)
        if face >= 2:
            item(frame, "mushroom", cx, cy + 0.05 * r, r * 0.3)
        if face >= 3:
            for j in range(5):
                a = math.radians(30 + j * 30)
                item(frame, "pepper", cx + 0.45 * r * math.cos(a), cy + 0.1 * r + 0.35 * r * math.sin(a), r * 0.16)
    else:
        for key, x, y, k in top_spots(tops, r):
            item(frame, key, cx + x, cy + y, r * 0.17, rot=k * 37)
    for j in range(slices):
        a = j / slices * 2 * math.pi - math.pi / 2
        d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)), fill=INK, width=7)


def scene_intro(frame, s, t):
    q = t - s["t0"]
    pizza(frame, 960, 600, 330 * ease_back(q / 0.6), tops=(5, 4, 3))
    for j, key in enumerate(("rollingpin", "whisk", "cheese", "smoothie", "chefhat", "skewer")):
        a = j / 6 * 2 * math.pi + t * 0.5
        item(frame, key, 960 + 640 * math.cos(a), 600 + 300 * math.sin(a), 190 * ease_back((q - 0.2 - j * 0.08) / 0.4))
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(170, 1750), scale=0.34)
        rt(frame, 960, 130, "LET'S COOK!", int(180 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)


def chef_body(frame, n, t, x, scale=0.55, hat=True, emo="happy", hop=0):
    body(frame, n, t, emo, x, scale=scale, hop=hop)
    if hat:
        top = 1075 - 1860 * scale - hop
        item(frame, "chefhat", x + 10 * scale, top + 130 * scale, 520 * scale)


def scene_chef(frame, s, t):
    k = s["num"]
    key = s["key"]
    card(frame, 1320, 520, 560, 560)
    item(frame, key, 1320, 520 + 8 * math.sin(t * 2.5), 380 * ease_back((t - s["t0"]) / 0.4))
    if key == "hands":
        for j in range(8):
            a = t * 2 + j
            ImageDraw.Draw(frame).ellipse((1320 + 220 * math.cos(a) - 20, 520 + 200 * math.sin(a) - 20, 1320 + 220 * math.cos(a) + 20, 520 + 200 * math.sin(a) + 20), outline=(150, 200, 255), width=5)
    chef_body(frame, "gul", t, 600, hat=k >= 3)
    if k >= 2:
        top = 1075 - 1860 * 0.55
        item(frame, "apron", 600, top + 1250 * 0.55, 560 * 0.55)
    badge(frame, 160, 90, f"STEP {k}", (255, 140, 26))
    word(frame, {"hands": "WASH HANDS!", "apron": "APRON!", "chefhat": "CHEF HAT!"}[key], t, s["say_t"], x=1320, y=900, size=110)


def scene_safety(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 760, 540, 600, 600, good=s["ok"])
    item(frame, s["key"], 760, 540, 420 * k)
    d = ImageDraw.Draw(frame)
    if s["ok"]:
        d.line((1240, 540, 1320, 620, 1480, 440), fill=(59, 193, 74), width=int(36 * k) + 1, joint="curve")
    else:
        r = 300 * k
        d.ellipse((760 - r, 540 - r, 760 + r, 540 + r), outline=(232, 53, 46), width=22)
        d.line((760 - r * 0.7, 540 + r * 0.7, 760 + r * 0.7, 540 - r * 0.7), fill=(232, 53, 46), width=22)
        rt(frame, 1400, 540, "HOT!" if s["key"] == "oven" else "SHARP!", int(130 * k), colour=(232, 53, 46))
    if s["ok"] and s["key"] == "hands":
        body(frame, "misheal", t, "happy", 1520, scale=0.5)
        rt(frame, 760, 900, "WITH A GROWN-UP!", 70, colour=(46, 120, 230), maxw=700)
    word(frame, "SAFETY RULE!", t, s["t0"], size=100)


def scene_tool(frame, s, t):
    badge(frame, 160, 90, f"{s['num']}/7", (255, 140, 26))
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 700, 540, 560, 560)
    rot = 0
    if s["key"] == "rollingpin":
        rot = 0
        dx = 60 * math.sin(t * 4)
    else:
        dx = 0
        rot = 8 * math.sin(t * (12 if s["key"] in ("whisk", "spoon") else 2))
    item(frame, s["key"], 700 + dx, 540, 400 * k, rot=rot)
    rt(frame, 1340, 540, s["w"] + "!", int(100 * k), colour=RAINBOW[s["num"] % 6], maxw=700)
    side_kids(frame, t, xs=(150, 1770), scale=0.26)


def scene_ingred(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    keys = ["flour", "sauce", "cheese", "olive", "pepper", "mushroom"]
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((180, 760, 1740, 830), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    for i in range(n):
        x = 330 + i * 252
        k = ease_back((t - s["ts"][i]) / 0.35)
        item(frame, keys[i], x, 640 - 10 * abs(math.sin(t * 3 + i)), 220 * k)
        rt(frame, x, 450, str(i + 1), int(70 * k), colour=RAINBOW[i % 6])
    word(frame, "6 INGREDIENTS!" if t >= s["sum_t"] else "PIZZA INGREDIENTS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(170, 1750), scale=0.24)


def scene_step(frame, s, t):
    key = s["key"]
    q = t - s["t0"]
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((360, 760, 1560, 840), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    if key == "mix":
        item(frame, "bowl", 960, 620, 440)
        item(frame, "spoon", 960 + 60 * math.cos(t * 6), 470 + 20 * math.sin(t * 6), 260, rot=30 * math.sin(t * 6))
        item(frame, "flour", 1380, 600, 220)
    elif key == "knead":
        sq = 1 + 0.18 * math.sin(t * 6)
        d.ellipse((960 - 200 * sq, 680 - 110 / sq, 960 + 200 * sq, 760), fill=(245, 225, 180), outline=INK, width=6)
        for x in (840, 1080):
            item(frame, "hands", x, 600 - 30 * abs(math.sin(t * 6)), 200)
    elif key == "roll":
        r = 160 + 140 * min(1, q / 3)
        d.ellipse((960 - r, 720 - r * 0.25, 960 + r, 720 + r * 0.25), fill=(245, 225, 180), outline=INK, width=6)
        item(frame, "rollingpin", 960 + 160 * math.sin(t * 3), 650, 420)
    elif key in ("sauce", "cheese"):
        pizza(frame, 960, 560, 300, sauce=min(1, q / 2.5) if key == "sauce" else 1, cheese=min(1, q / 2.5) if key == "cheese" else 0)
        if key == "sauce":
            item(frame, "spoon", 960 + 180 * math.cos(t * 3), 560 + 180 * math.sin(t * 3), 200)
        else:
            for j in range(10):
                y = 250 + ((t * 300 + j * 70) % 300)
                d.rectangle((800 + j * 35, y, 812 + j * 35, y + 24), fill=CHEESE, outline=INK)
    else:
        item(frame, "oven", 960, 540, 560)
        if int(t * 2) % 2:
            stars_ring(frame, 960, 600, 300, 200, t, n=6, r=14)
    badge(frame, 160, 90, f"STEP {s['num']}", (255, 140, 26))
    word(frame, {"mix": "MIX!", "knead": "SQUISH!", "roll": "ROLL!", "sauce": "SAUCE!", "cheese": "CHEESE!", "bake": "BAKE!"}[key],
         t, s["say_t"], size=150, col=(255, 140, 26))
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.3)


def scene_tops(frame, s, t):
    si = s["stage"]
    n = sum(1 for x in s["cts"] if t >= x)
    tops = [(5, 4, 3)[j] if j < si else 0 for j in range(3)]
    tops[si] = n
    pizza(frame, 960, 560, 380, tops=tuple(tops))
    item(frame, TOPKEYS[si], 1560, 300, 200)
    if n:
        rt(frame, 1560, 560, str(n), int(220 * ease_back((t - s["cts"][n - 1]) / 0.2)), colour=RAINBOW[n % 6])
    side_kids(frame, t, "happy", xs=(240, 1700), scale=0.32)
    lab = {0: "OLIVES!", 1: "PEPPERS!", 2: "MUSHROOMS!"}[si]
    word(frame, f"{s['n']} {lab}" if t >= s["sum_t"] else lab, t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)


def scene_baked(frame, s, t):
    if t < s["out_t"]:
        item(frame, "oven", 960, 560, 560)
        if t >= s["ding_t"]:
            rt(frame, 1400, 260, "DING!", int(140 * ease_back((t - s["ding_t"]) / 0.3)), colour=(255, 140, 26))
    else:
        k = ease_back((t - s["out_t"]) / 0.5)
        pizza(frame, 960, 600, 380 * k, tops=(5, 4, 3))
        item(frame, "mitt", 520, 620, 260)
        item(frame, "mitt", 1400, 620, 260, flip=True)
        for j in range(3):
            y = 260 - ((t * 60 + j * 40) % 120)
            ImageDraw.Draw(frame).arc((880 + j * 60, y, 920 + j * 60, y + 80), 90, 270, fill=(255, 255, 255), width=8)
        confetti(frame, t, s["out_t"])
        word(frame, "HOT PIZZA!", t, s["out_t"], size=140)


def scene_slice(frame, s, t):
    pizza(frame, 960, 580, 380, tops=(5, 4, 3), slices=s["n"])
    if s.get("cts"):
        n = sum(1 for x in s["cts"] if t >= x)
        for i in range(n):
            a = (i + 0.5) / 8 * 2 * math.pi - math.pi / 2
            rt(frame, 960 + 470 * math.cos(a), 580 + 440 * math.sin(a), str(i + 1), 70, colour=RAINBOW[i % 6])
    word(frame, {2: "HALVES! 2 PIECES", 4: "QUARTERS! 4 PIECES", 8: "8 SLICES!"}[s["n"]], t, s["say_t"], size=100)
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.3)


def scene_pizzaface(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    pizza(frame, 960, 580, 380, face=n)
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "MISTER PIZZA!", t, s["done_t"], size=130)
    else:
        word(frame, "PIZZA FACE!", t, s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.32)


def scene_smoothie(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    q = t - s["ts"][n - 1] if n else 0
    shake = 8 * math.sin(t * 40) if n == 4 and q < 1.6 else 0
    if n < 5:
        item(frame, "blender", 960 + shake, 560, 520)
        for i, key in enumerate(("strawberry", "banana")[:min(n, 2)]):
            if n < 4:
                item(frame, key, 900 + i * 120, 480, 140)
        side = ["strawberry", "banana", "milk", "blender"][n - 1] if n else None
        if side and side != "blender":
            item(frame, side, 1450, 520, 240 * ease_back(q / 0.3))
    else:
        item(frame, "smoothie", 960, 560, 520 * ease_back(q / 0.4))
    labs = ["STRAWBERRIES!", "BANANA!", "MILK!", "VRRRR!", "SMOOTHIE!"]
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "SLURP!", t, s["done_t"], size=150)
    else:
        word(frame, labs[n - 1] if n else "MAKE A SMOOTHIE!", t, s["ts"][n - 1] if n else s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.32)


KCOL = {"red": (232, 53, 46), "orange": (255, 140, 26), "yellow": (240, 190, 20), "green": (59, 170, 74), "purple": (140, 80, 210)}
KEBAB = [("strawberry", "red"), ("orange", "orange"), ("pineapple", "yellow"), ("kiwi", "green"), ("grapes", "purple")]


def scene_kebab(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    d = ImageDraw.Draw(frame)
    d.line((260, 540, 1660, 540), fill=(200, 150, 74), width=16)
    for i in range(n):
        key, col = KEBAB[i]
        x = 420 + i * 270
        k = ease_back((t - s["ts"][i]) / 0.35)
        item(frame, key, x, 540, 230 * k)
        rt(frame, x, 720, col.upper(), int(44 * k), colour=KCOL[col], maxw=250)
    if n < 5:
        key, _ = KEBAB[n]
        x = 420 + n * 270
        item(frame, key, x, 300 + 10 * math.sin(t * 4), 180)
        rt(frame, x, 540, "?", 120, colour=(255, 255, 255))
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "RAINBOW!", t, s["done_t"], size=140)
    else:
        word(frame, "WHAT COLOUR?", t, s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.26)


def scene_taste(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 700, 540, 560, 560)
    item(frame, s["key"], 700, 540 + 8 * math.sin(t * 2.5), 400 * k)
    rt(frame, 1340, 540, s["w"] + "!", int(130 * k), colour=(255, 77, 109), maxw=700)
    body(frame, "gul" if s["key"] in ("banana", "watermelon", "cheese") else "misheal", t, "happy", 220, scale=0.36)


def scene_hotcold(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, (lab, col) in enumerate((("HOT", (232, 53, 46)), ("COLD", (46, 140, 255)))):
        x = 420 + j * 1080
        good = t >= s["answer_t"] and (j == 0) == s["hot"]
        d.rounded_rectangle((x - 230, 560, x + 230, 880), radius=40, fill=col + (60,), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        rt(frame, x, 720, lab, 110, colour=col)
        if good:
            stars_ring(frame, x, 720, 260, 170, t, n=8, r=18)
    if t >= s["answer_t"]:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x = 960 + ((420 if s["hot"] else 1500) - 960) * k
        y = 460 + (520 - 460) * k
        sz = 340 - 120 * k
    else:
        x, y, sz = 960, 460 + 10 * math.sin(t * 3), 340
    if s["key"] == "icepop":
        icepop(frame, x, y, sz)
    else:
        item(frame, s["key"], x, y, sz)
    word(frame, "HOT OR COLD?", t, s["t0"], size=110)


def scene_need(frame, s, t):
    choice_row(frame, t, s["keys"], s["good"], s["answer_t"], y=580, size=300,
               draw=lambda f, k, x, y, sz: pan(f, x - 60, y, sz * 0.4) if k == "pan" else item(f, k, x, y, sz))
    word(frame, "WHAT DO WE NEED?", t, s["t0"], size=100)


def scene_clean(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 760, 540, 560, 560)
    item(frame, s["key"], 760 + (20 * math.sin(t * 8) if s["key"] == "sponge" else 0), 540, 400 * k)
    badge(frame, 160, 90, f"STEP {s['num']}", (46, 140, 255))
    rt(frame, 1350, 540, {"fridge": "PUT AWAY!", "plates": "WASH!", "sponge": "WIPE!", "hands": "WASH HANDS!"}[s["key"]], int(100 * k), colour=(46, 140, 255), maxw=620)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.28)


def scene_outro(frame, s, t):
    pizza(frame, 960, 640, 260, tops=(5, 4, 3), slices=8)
    for n, x in (("gul", 480), ("misheal", 1440)):
        chef_body(frame, n, t, x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))))
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "YUMMY! BYE BYE!", int(150 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "GREAT COOKING!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


def pan(frame, x, y, r, t=0, cake=None, flip=0.0):
    d = ImageDraw.Draw(frame)
    d.line((x + r * 0.9, y, x + r * 2.0, y - r * 0.2), fill=INK, width=int(r * 0.22))
    d.line((x + r * 0.9, y, x + r * 2.0, y - r * 0.2), fill=(60, 60, 70), width=int(r * 0.14))
    d.ellipse((x - r, y - r * 0.35, x + r, y + r * 0.35), fill=(70, 72, 82), outline=INK, width=6)
    if cake:
        cy = y - flip * r * 1.6
        h = r * 0.22 * max(0.45, abs(math.cos(flip * math.pi)))
        d.ellipse((x - r * 0.7, cy - max(6, h), x + r * 0.7, cy + max(6, h)), fill=cake, outline=INK, width=5)


def icepop(frame, x, y, sz):
    d = ImageDraw.Draw(frame)
    w, h = sz * 0.36, sz * 0.62
    d.rectangle((x - sz * 0.05, y + h * 0.4, x + sz * 0.05, y + h * 0.8), fill=(230, 190, 130), outline=INK, width=4)
    for j, c in enumerate(((232, 53, 46), (255, 140, 26), (255, 210, 40))):
        d.rounded_rectangle((x - w / 2, y - h / 2 + j * h / 3, x + w / 2, y - h / 2 + (j + 1) * h / 3 + (20 if j < 2 else 0)),
                            radius=int(w / 2) if j in (0, 2) else 0, fill=c)
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=int(w / 2), outline=INK, width=5)


def scene_pancake(frame, s, t):
    key = s["key"]
    q = t - s["t0"]
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((360, 760, 1560, 840), radius=20, fill=(200, 140, 90), outline=INK, width=6)
    if key in ("egg", "flour", "milk", "whisk"):
        item(frame, "bowl", 960, 640, 420)
        item(frame, key, 960 + (60 * math.cos(t * 8) if key == "whisk" else 0), 430 + (0 if key == "whisk" else 40 * min(1, q / 0.8)), 230,
             rot=(20 * math.sin(t * 8) if key == "whisk" else 0))
    elif key == "pan":
        pan(frame, 860, 640, 260, t, cake=(250, 220, 150))
        for j in range(4):
            y = 520 - ((t * 80 + j * 30) % 120)
            d.arc((740 + j * 70, y, 780 + j * 70, y + 70), 90, 270, fill=(255, 255, 255), width=7)
    elif key == "flip":
        f = (q % 1.6) / 1.6
        pan(frame, 860, 640, 260, t, cake=(225, 170, 90), flip=math.sin(f * math.pi) * 0.999)
    else:
        for j in range(4):
            d.ellipse((760, 640 - j * 40, 1160, 700 - j * 40), fill=(225, 170, 90), outline=INK, width=5)
        for j, kk in enumerate(("strawberry", "banana", "strawberry")):
            item(frame, kk, 880 + j * 80, 500, 110)
    badge(frame, 160, 90, f"STEP {s['num']}", (255, 140, 26))
    word(frame, {"egg": "CRACK!", "flour": "FLOUR!", "milk": "MILK!", "whisk": "WHISK!", "pan": "SIZZLE!", "flip": "FLIP!", "stack": "PANCAKES!"}[key],
         t, s["say_t"], size=150, col=(255, 140, 26))
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.3)


def scene_tray(frame, s, t):
    n = sum(1 for x in s["cts"] if t >= x)
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((380, 380, 1540, 820), radius=30, fill=(170, 175, 190), outline=INK, width=8)
    for i in range(n):
        x, y = 520 + (i % 5) * 220, 500 + (i // 5) * 200
        item(frame, "cookie", x, y, 170 * ease_back((t - s["cts"][i]) / 0.3))
        rt(frame, x, y, str(i + 1), 54, colour=(255, 255, 255))
    word(frame, f"{n} COOKIES!" if n else "COUNT THE COOKIES!", t, s["cts"][n - 1] if n else s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.3)


LAYER = {"bread": ((235, 190, 120), 46), "cheese": ((255, 210, 60), 22), "tomato": ((220, 50, 40), 26), "lettuce": ((110, 200, 70), 24)}


def scene_sandwich(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    d = ImageDraw.Draw(frame)
    item(frame, "plate", 960, 860, 700)
    y = 830
    order = ["bread", "cheese", "tomato", "lettuce", "bread"]
    for i in range(n):
        col, h = LAYER[order[i]]
        k = min(1, (t - s["ts"][i]) / 0.35)
        yy = y - h - 300 * (1 - k)
        if order[i] == "lettuce":
            pts = [(700 + j * 40, yy + (0 if j % 2 else h)) for j in range(14)] + [(1220, yy + h), (700, yy + h)]
            d.polygon(pts, fill=col, outline=INK)
        else:
            d.rounded_rectangle((690, yy, 1230, yy + h), radius=int(h / 2), fill=col, outline=INK, width=5)
        y -= h
        rt(frame, 1420, yy + h / 2, str(i + 1), 50, colour=RAINBOW[i % 6])
    labs = ["BREAD!", "CHEESE!", "TOMATO!", "LETTUCE!", "BREAD!"]
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "5 LAYERS!", t, s["done_t"], size=140)
    else:
        word(frame, labs[n - 1] if n else "BUILD A SANDWICH!", t, s["ts"][n - 1] if n else s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.3)


def scene_ksound(frame, s, t):
    if t < s["answer_t"]:
        q = t - s["snd_t"]
        d = ImageDraw.Draw(frame, "RGBA")
        if 0 <= q < 1.6:
            for j in range(3):
                r = 120 + 100 * j + 120 * (q % 0.7)
                d.arc((960 - r, 540 - r, 960 + r, 540 + r), -50, 50, fill=(255, 255, 255, 210), width=10)
                d.arc((960 - r, 540 - r, 960 + r, 540 + r), 130, 230, fill=(255, 255, 255, 210), width=10)
        rt(frame, 960, 540, "?", int(220 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
        word(frame, "LISTEN!", t, s["t0"], size=130)
    else:
        k = ease_back((t - s["answer_t"]) / 0.4)
        if s["key"] == "pan":
            pan(frame, 900, 580, 240 * k, t, cake=(250, 220, 150))
        else:
            item(frame, s["key"], 960, 560, 420 * k)
        word(frame, {"pan": "SIZZLE!", "knife": "CHOP!", "blender": "VRRRR!", "oven": "DING!"}[s["key"]], t, s["answer_t"], size=140)
    side_kids(frame, t, xs=(170, 1750), scale=0.3)


def scene_healthy(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, (lab, col) in enumerate((("HEALTHY", (59, 170, 74)), ("TREAT", (240, 90, 160)))):
        x = 420 + j * 1080
        good = t >= s["answer_t"] and (j == 0) == s["good"]
        d.rounded_rectangle((x - 250, 560, x + 250, 880), radius=40, fill=col + (60,), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        rt(frame, x, 720, lab, 90, colour=col, maxw=460)
        if good:
            stars_ring(frame, x, 720, 280, 170, t, n=8, r=18)
    if t >= s["answer_t"]:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x = 960 + ((420 if s["good"] else 1500) - 960) * k
        y = 460 + (520 - 460) * k
        sz = 340 - 120 * k
    else:
        x, y, sz = 960, 460 + 10 * math.sin(t * 3), 340
    item(frame, s["key"], x, y, sz)
    word(frame, "HEALTHY OR TREAT?", t, s["t0"], size=110)


POPCOL = [(232, 53, 46), (255, 140, 26), (255, 210, 40)]


def scene_pops(frame, s, t):
    key = s["key"]
    q = t - s["t0"]
    d = ImageDraw.Draw(frame)
    if key == "freeze":
        item(frame, "fridge", 960, 560, 640)
        stars_ring(frame, 960, 560, 380, 300, t, n=10, r=16)
        rt(frame, 1450, 400, "BRRR!", 110, colour=(46, 140, 255))
    else:
        for j in range(3):
            x = 760 + j * 200
            if key == "pour":
                lvl = min(1, max(0, (q - j * 0.6) / 0.8))
                d.rounded_rectangle((x - 60, 420, x + 60, 700), radius=50, outline=INK, width=6, fill=(255, 255, 255))
                if lvl > 0:
                    d.rounded_rectangle((x - 54, 694 - 270 * lvl, x + 54, 694), radius=40, fill=POPCOL[j])
            elif key == "stick":
                d.rounded_rectangle((x - 60, 420, x + 60, 700), radius=50, outline=INK, width=6, fill=POPCOL[j])
                yy = 280 + 140 * min(1, max(0, (q - j * 0.4) / 0.5))
                d.rectangle((x - 12, yy, x + 12, yy + 200), fill=(230, 190, 130), outline=INK, width=4)
            else:
                icepop(frame, x, 560 - 15 * abs(math.sin(t * 4 + j)), 380)
        if key == "done":
            confetti(frame, t, s["t0"])
    badge(frame, 160, 90, f"STEP {s['num']}", (232, 53, 46))
    word(frame, {"pour": "POUR!", "stick": "STICKS!", "freeze": "FREEZE!", "done": "FRUIT POPS!"}[key], t, s["say_t"], size=140, col=(232, 53, 46))
    side_kids(frame, t, "happy", xs=(200, 1720), scale=0.3)


def scene_fullempty(frame, s, t):
    d = ImageDraw.Draw(frame)
    lvl = {"full": 1.0, "empty": 0.0, "half": 0.5}[s["lvl"]]
    x, top, bot, w = 960, 300, 820, 300
    d.polygon([(x - w / 2, top), (x + w / 2, top), (x + w / 2 - 40, bot), (x - w / 2 + 40, bot)], fill=(235, 245, 255))
    if lvl:
        yy = bot - (bot - top - 20) * lvl
        f = (yy - top) / (bot - top)
        d.polygon([(x - w / 2 + 40 * f, yy), (x + w / 2 - 40 * f, yy), (x + w / 2 - 40, bot), (x - w / 2 + 40, bot)], fill=(255, 150, 60))
    d.polygon([(x - w / 2, top), (x + w / 2, top), (x + w / 2 - 40, bot), (x - w / 2 + 40, bot)], outline=INK, width=8)
    if t >= s["answer_t"]:
        word(frame, "HALF FULL!" if s["lvl"] == "half" else s["lvl"].upper() + "!", t, s["answer_t"], x=1450, y=540, size=130, col=(255, 140, 26))
    else:
        word(frame, "FULL OR EMPTY?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(200, 1720), scale=0.3)


def scene_table(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((300, 600, 1620, 860), radius=30, fill=(255, 245, 230), outline=INK, width=6)
    if n >= 1:
        item(frame, "plate", 960, 720, 360 * ease_back((t - s["ts"][0]) / 0.35))
        if n >= 4:
            pizza(frame, 960, 700, 110, tops=(5, 4, 3), slices=8)
    if n >= 2:
        item(frame, "spoon", 1220, 720, 260 * ease_back((t - s["ts"][1]) / 0.35), rot=-80)
    if n >= 3:
        item(frame, "cup", 1420, 620, 230 * ease_back((t - s["ts"][2]) / 0.35))
    if n >= 4:
        d.polygon([(640, 650), (760, 650), (780, 800), (620, 800)], fill=(255, 140, 180), outline=INK)
    labs = ["PLATE!", "SPOON!", "CUP!", "NAPKIN!"]
    word(frame, labs[n - 1] if n else "SET THE TABLE!", t, s["ts"][n - 1] if n else s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(170, 1750), scale=0.3)


SCENES = {"intro": scene_intro, "chef": scene_chef, "safety": scene_safety, "tool": scene_tool, "ingred": scene_ingred, "step": scene_step,
          "tops": scene_tops, "baked": scene_baked, "slice": scene_slice, "pizzaface": scene_pizzaface, "smoothie": scene_smoothie,
          "kebab": scene_kebab, "taste": scene_taste, "hotcold": scene_hotcold, "need": scene_need, "clean": scene_clean, "outro": scene_outro,
          "pancake": scene_pancake, "tray": scene_tray, "sandwich": scene_sandwich, "ksound": scene_ksound, "healthy": scene_healthy,
          "pops": scene_pops, "fullempty": scene_fullempty, "table": scene_table,
          "dance": lambda f, s, t: (pizza(f, 1700, 640, 170, tops=(5, 4, 3)), K.scene_dance(f, s, t))}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L20 Cooking for Kids", "Cooking for Kids")
K.CFG["title_items"] = ["chefhat", "rollingpin", "cheese", "whisk", "smoothie"]

if __name__ == "__main__":
    K.main()
