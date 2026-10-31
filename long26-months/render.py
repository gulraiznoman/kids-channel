"""Animate L26 "Months of the Year & New Year".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW

A26, L1, L4, L8 = HERE / "art", ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art", ROOT / "long08-colors-shapes/art"
ART = {k: A26 / f"item_{k}.png" for k in ("firework", "party", "clock12", "schoolbag", "autumnleaf", "icecream2", "blossom")}
ART.update({"snowflake": ROOT / "long17-xmastree/art/item_snowflake.png", "heart": ROOT / "long16-sharing/art/item_heart.png", "rainy": L1 / "fruit_rainy.png",
            "kite": L8 / "item_kite.png", "sunny": L1 / "fruit_sunny.png", "watermelon": ROOT / "ep01-fruits/art/fruit_watermelon.png", "scarf": L4 / "item_scarf.png",
            "snowman": L8 / "item_snowman.png", "calendar": ROOT / "long18-days/art/item_calendar.png", "watering": L4 / "item_watering_can.png", "book": L4 / "item_book.png",
            "star": ROOT / "long15-potty/art/item_star.png", "sunhat": L4 / "item_sunhat.png", "raincoat": L4 / "item_raincoat.png",
            "sunglasses": L4 / "item_sunglasses.png", "boots": L4 / "item_boots.png"})
BGS = {"playroom": ROOT / "long18-days/art/bg_wall.png", "northpole": ROOT / "long19-santa/art/bg_northpole.png", "park": ROOT / "long05-body-parts/art/bg_park.png",
       "patch": ROOT / "long03-fruits-veg/art/bg_patch.png", "beach": L1 / "bg_beach.png", "board": L8 / "bg_board.png", "tree": ROOT / "long09-eggs/art/bg_tree.png",
       "xmasroom": ROOT / "long17-xmastree/art/bg_xmasroom.png", "city": A26 / "bg_city.png"}
MON = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
MCOL = [(46, 120, 230), (240, 90, 160), (59, 170, 74), (0, 170, 190), (140, 190, 40), (245, 170, 20), (255, 120, 30), (232, 53, 46), (140, 80, 210), (205, 95, 30), (120, 90, 60), (30, 130, 90)]
SEASCOL = {"spring": (59, 170, 74), "summer": (245, 170, 20), "autumn": (205, 95, 30), "winter": (46, 120, 230)}


def block(frame, x, y, i, w=250, h=100, size=38, hi=False, dim=False, label=None):
    d = ImageDraw.Draw(frame, "RGBA")
    if hi:
        w, h, size = w * 1.15, h * 1.15, size * 1.15
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=int(h / 3), fill=MCOL[i] + ((90,) if dim else (255,)),
                        outline=(255, 255, 255) if hi else INK, width=9 if hi else 5)
    rt(frame, x, y, label or MON[i], int(size), colour=(255, 255, 255), maxw=w - 20)


def grid(i):
    return 280 + (i % 4) * 454, 300 + (i // 4) * 170


def fireworks(frame, t, n=5):
    for j in range(n):
        p = ((t * 0.55 + j * 0.37) % 1)
        x, y = 200 + (j * 397) % 1560, 130 + (j * 173) % 360
        item(frame, "firework", x, y, 60 + 340 * p, alpha=max(0, 1 - p * p), rot=j * 20)


def scene_intro(frame, s, t):
    if t >= s["boom_t"]:
        fireworks(frame, t)
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(280, 1640), scale=0.4)
        rt(frame, 960, 150, "HAPPY NEW YEAR!", int(170 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)


def scene_twelve(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    for i in range(n):
        x, y = grid(i)
        k = ease_back((t - s["ts"][i]) / 0.3)
        block(frame, x, y, i, w=410 * k, h=140 * k, size=48 * k, hi=i == n - 1 and t < s["sum_t"])
    if n:
        rt(frame, 960, 860, str(n), int(120 * ease_back((t - s["ts"][n - 1]) / 0.25)), colour=RAINBOW[n % 6])
    word(frame, "12 MONTHS = 1 YEAR!" if t >= s["sum_t"] else "12 MONTHS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], y=110, size=110)
    side_kids(frame, t, "happy", xs=(90, 1830), scale=0.19)


def scene_chant(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    for i in range(12):
        x, y = grid(i)
        hi = i == n - 1 and t < s["end_t"]
        block(frame, x, y - (16 * abs(math.sin((t - s["ts"][i]) * 8)) if hi else 0), i, w=410, h=140, size=48, hi=hi, dim=i >= n and t < s["end_t"])
    rt(frame, 960, 110, s["label"], 100)
    side_kids(frame, t, "happy", xs=(90, 1830), scale=0.19)


def scene_month(frame, s, t):
    i = s["m"]
    d = ImageDraw.Draw(frame, "RGBA")
    k = ease_back((t - s["t0"]) / 0.4)
    d.rounded_rectangle((960 - 470 * k, 40, 960 + 470 * k, 200), radius=50, fill=MCOL[i] + (255,), outline=INK, width=7)
    if k > 0.3:
        rt(frame, 960, 120, MON[i] + "!", int(100 * k), colour=(255, 255, 255), maxw=860)
    for j in range(12):
        block(frame, 300 + j * 120, 1035, j, w=112, h=56, size=24, dim=j != i, label=MON[j][:3])
    if t >= s["act_t"]:
        kk = ease_back((t - s["act_t"]) / 0.4)
        item(frame, s["key"], 960, 560 - 15 * abs(math.sin(t * 3)), 430 * kk, rot=5 * math.sin(t * 2))
        rt(frame, 960, 870, s["w"], int(90 * kk), colour=MCOL[i], maxw=900)
    side_kids(frame, t, "happy", xs=(300, 1620), scale=0.42, feet=1000)


def scene_season(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 720, 560, 580, 580)
    item(frame, s["key"], 720, 560 + 8 * math.sin(t * 2.5), 430 * k)
    rt(frame, 1350, 540, s["name"].upper() + "!", int(120 * k), colour=SEASCOL[s["name"]], maxw=700)
    side_kids(frame, t, "happy", xs=(160, 1760), scale=0.26)


def scene_seasort(frame, s, t):
    names = ["spring", "summer", "autumn", "winter"]
    for j, n in enumerate(names):
        x = 300 + j * 440
        good = t >= s["answer_t"] and n == s["name"]
        card(frame, x, 860, 390, 170, good=good, dim=t >= s["answer_t"] and not good)
        rt(frame, x, 860, n.upper(), 66, colour=SEASCOL[n])
    item(frame, s["key"], 960, 400, 460)
    word(frame, "WHICH SEASON?", t, s["t0"], y=100, size=100)


def scene_seq(frame, s, t):
    xs = (560, 1360)
    ansp = 0 if s["first"] else 1
    block(frame, xs[1 - ansp], 540, s["m"], w=620, h=240, size=80)
    if t >= s["answer_t"]:
        block(frame, xs[ansp], 540, s["ans"], w=620, h=240, size=80, hi=True)
        stars_ring(frame, xs[ansp], 540, 400, 200, t, n=8, r=18)
    else:
        rt(frame, xs[ansp], 540, "?", int(220 + 12 * math.sin(t * 6)), colour=(255, 77, 109))
    word(frame, "WHAT COMES BEFORE?" if s["first"] else "WHAT COMES NEXT?", t, s["t0"], size=110)
    side_kids(frame, t, xs=(90, 1830), scale=0.19)


def scene_missing(frame, s, t):
    rev = t >= s["answer_t"]
    for i in range(12):
        x, y = grid(i)
        if i == s["miss"] and not rev:
            d = ImageDraw.Draw(frame)
            d.rounded_rectangle((x - 200, y - 70, x + 200, y + 70), radius=46, outline=(255, 77, 109), width=7)
            rt(frame, x, y, "?", 100, colour=(255, 77, 109))
        else:
            block(frame, x, y, i, w=410, h=140, size=48, hi=rev and i == s["miss"])
    word(frame, MON[s["miss"]] + "!" if rev else "WHICH MONTH IS MISSING?", t, s["answer_t"] if rev else s["t0"], y=110, size=100)


def scene_letters(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 460, 540, 520, 560)
    rt(frame, 460, 540, s["L"], int(380 * k), colour=(255, 77, 109))
    n = sum(1 for x in s["ts"] if t >= x)
    for j, m in enumerate(s["ms"][:n]):
        block(frame, 1280, 330 + j * 210, m, w=740, h=170, size=78, hi=j == n - 1)
    side_kids(frame, t, xs=(100, 1820), scale=0.2)


def scene_how(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    key = s["key"]
    if key == "day":
        item(frame, "sunny", 780, 540, 340 * k)
        rt(frame, 1300, 540, "1 DAY", int(130 * k), colour=(245, 170, 20))
    elif key == "week":
        for j in range(7):
            block(frame, 420 + j * 180, 540, j, w=165, h=165, size=64, label=str(j + 1))
        rt(frame, 960, 790, "7 DAYS = 1 WEEK", int(90 * k), colour=(46, 120, 230))
    elif key == "month":
        item(frame, "calendar", 960, 500, 500 * k)
        rt(frame, 960, 860, "4 WEEKS = 1 MONTH", int(90 * k), colour=(59, 170, 74))
    else:
        for i in range(12):
            x, y = grid(i)
            block(frame, x, y, i, w=410, h=120, size=46)
        rt(frame, 960, 860, "12 MONTHS = 1 YEAR", int(90 * k), colour=(232, 53, 46))


def scene_bday(frame, s, t):
    if s["who"] == "both":
        for i in range(12):
            a = i / 12 * 2 * math.pi + t * 0.4
            block(frame, 960 + 680 * math.cos(a), 540 + 320 * math.sin(a), i, w=230, h=86, size=30)
        side_kids(frame, t, "happy", xs=(740, 1180), scale=0.34)
        word(frame, "WHEN IS YOUR BIRTHDAY?", t, s["t0"], size=100)
        return
    n = "gul" if s["who"] == "gul" else "misheal"
    body(frame, n, t, "excited", 620, scale=0.6, hop=18 * abs(math.sin(t * 4)), wave=True)
    block(frame, 1340, 500, s["m"], w=620, h=210, size=74, hi=True)
    item(frame, "party", 1340, 790, 240)
    word(frame, "MY BIRTHDAY!", t, s["t0"], size=110)


def scene_rhyme(frame, s, t):
    n = sum(1 for x in s["l"] if t >= x)
    li = (n - 1) % 8
    gp = [(0, 1), (2, 3), (4, 5, 6), (7,), (8, 9), (10,), (11,), ()]
    for i in range(12):
        a = i / 12 * 2 * math.pi - math.pi / 2 + t * 0.3
        block(frame, 960 + 720 * math.cos(a), 560 + 340 * math.sin(a), i, w=230, h=86, size=30, hi=n > 0 and i in gp[li])
    for nm, x in (("gul", 800), ("misheal", 1120)):
        body(frame, nm, t, "happy", x, scale=0.36, hop=22 * abs(math.sin(t * 4 + (0 if nm == "gul" else 1))), wave=True)
    word(frame, "CLAP ALONG!", t, s["t0"], y=100, size=100)


def scene_eve(frame, s, t):
    item(frame, s["key"], 960, 400, 460 * ease_back((t - s["t0"]) / 0.4), rot=8 * math.sin(t * 2) if s["key"] == "party" else 0)
    side_kids(frame, t, "excited", xs=(300, 1620), scale=0.4)
    word(frame, "NEW YEAR'S EVE!" if s["key"] == "party" else "12 O'CLOCK!", t, s["say_t"], y=100, size=120, col=(255, 225, 90))


def scene_countdown(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    if t >= s["go_t"]:
        fireworks(frame, t, 7)
        confetti(frame, t, s["go_t"])
        rt(frame, 960, 150, "HAPPY NEW YEAR!", int(170 * ease_back((t - s["go_t"]) / 0.35)), maxw=1700)
    elif n:
        rt(frame, 960, 440, str(11 - n), int(400 * ease_back((t - s["ts"][n - 1]) / 0.25)), colour=RAINBOW[n % 6])
    else:
        rt(frame, 960, 440, "COUNTDOWN!", 150, colour=(255, 225, 90))
    side_kids(frame, t, "excited", xs=(260, 1660), scale=0.4)


def scene_wish(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    item(frame, s["key"], 1300, 560, 380 * k)
    body(frame, "misheal" if s["w"] in ("BE KIND!", "READ!") else "gul", t, "happy", 600, scale=0.55, wave=True)
    word(frame, s["w"], t, s["say_t"], y=120, size=130, col=(255, 77, 109))


def quiz_draw(frame, vis, t, k):
    if vis in MON:
        block(frame, 960, 580, MON.index(vis), w=720 * k, h=230 * k, size=86 * k, hi=True)
    else:
        rt(frame, 960, 580, vis, int(300 * k), colour=RAINBOW[2])


def scene_outro(frame, s, t):
    fireworks(frame, t, 4)
    for n, x in (("gul", 620), ("misheal", 1300)):
        body(frame, n, t, "happy", x, scale=0.46, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "HAPPY NEW YEAR!", int(150 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "12 MONTHS!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


ORD = ["1ST", "2ND", "3RD", "4TH", "5TH", "6TH", "7TH", "8TH", "9TH", "10TH", "11TH", "12TH"]


def scene_ordinal(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    for i in range(n):
        x, y = grid(i)
        block(frame, x, y, i, w=410, h=140, size=48, hi=i == n - 1, label=f"{ORD[i]} {MON[i][:3]}")
    if n:
        word(frame, f"{MON[n - 1]} IS {ORD[n - 1]}!", t, s["ts"][n - 1], y=110, size=100, col=MCOL[n - 1])
    side_kids(frame, t, "happy", xs=(90, 1830), scale=0.19)


def scene_wear(frame, s, t):
    block(frame, 960, 190, s["m"], w=620, h=170, size=74, hi=True)
    for j, key in enumerate(s["keys"]):
        x = 620 + j * 680
        ok = t >= s["answer_t"] and key == s["good"]
        card(frame, x, 640, 500, 500, good=ok, dim=t >= s["answer_t"] and not ok)
        item(frame, key, x, 640 - (20 * abs(math.sin(t * 6)) if ok else 0), 370)
    side_kids(frame, t, xs=(120, 1800), scale=0.24)


def scene_whichm(frame, s, t):
    rt(frame, 960, 130, s["q"], int(76 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)
    for j, m in enumerate(s["ms"]):
        ok = t >= s["answer_t"] and m == s["good"]
        block(frame, 960, 340 + j * 220, m, w=720, h=170, size=74, hi=ok, dim=t >= s["answer_t"] and not ok)
        if ok:
            stars_ring(frame, 960, 340 + j * 220, 450, 130, t, n=8, r=16)
    side_kids(frame, t, xs=(200, 1720), scale=0.3)


SCENES = {"intro": scene_intro, "twelve": scene_twelve, "chant": scene_chant, "month": scene_month, "season": scene_season, "seasort": scene_seasort, "seq": scene_seq,
          "missing": scene_missing, "letters": scene_letters, "how": scene_how, "bday": scene_bday, "rhyme": scene_rhyme, "eve": scene_eve, "countdown": scene_countdown,
          "wish": scene_wish, "ordinal": scene_ordinal, "wear": scene_wear, "whichm": scene_whichm, "outro": scene_outro, "quiz": lambda f, s, t: K.scene_quiz(f, s, t, draw=quiz_draw)}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L26 Months and New Year", "Months of the Year for Kids")
K.CFG["title_items"] = ["calendar", "firework", "party", "snowman", "sunny"]

if __name__ == "__main__":
    K.main()
