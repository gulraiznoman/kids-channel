"""Animate L18 "Days of the Week".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW

A18 = HERE / "art"
ART = {k: A18 / f"item_{k}.png" for k in ("calendar", "swimring", "house", "paint")}
ART.update({"book": ROOT / "long04-good-habits/art/item_book.png", "watering": ROOT / "long04-good-habits/art/item_watering_can.png",
            "pizza": ROOT / "long08-colors-shapes/art/item_pizza.png", "ball": ROOT / "long04-good-habits/art/item_ball.png",
            "star": ROOT / "long15-potty/art/item_star.png", "moon": ROOT / "long04-good-habits/art/item_moon.png",
            "bed": ROOT / "long04-good-habits/art/item_bed_neat.png", "toast": ROOT / "long04-good-habits/art/item_toast.png"})
ART.update({w: ROOT / f"long01-animals-fun/art/fruit_{w}.png" for w in ("sunny", "rainy", "cloudy", "windy", "snowy", "rainbow")})
BGS = {"playroom": ROOT / "long05-body-parts/art/bg_playroom.png", "board": ROOT / "long08-colors-shapes/art/bg_board.png",
       "beach": ROOT / "long01-animals-fun/art/bg_beach.png", "bedroom": ROOT / "long04-good-habits/art/bg_bedroom.png",
       "patch": ROOT / "long03-fruits-veg/art/bg_patch.png", "kitchen": ROOT / "long03-fruits-veg/art/bg_kitchen.png",
       "park": ROOT / "long05-body-parts/art/bg_park.png", "street": ROOT / "long08-colors-shapes/art/bg_street.png"}
DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
DCOL = [(232, 53, 46), (255, 140, 26), (240, 190, 20), (59, 170, 74), (46, 120, 230), (140, 80, 210), (240, 90, 160)]
WEEK_KEYS = ["book", "swimring", "book", "watering", "pizza", "ball", "house"]


def block(frame, x, y, i, w=230, h=110, size=44, hi=False, dim=False, label=None):
    d = ImageDraw.Draw(frame, "RGBA")
    c = DCOL[i]
    if hi:
        w, h, size = w * 1.18, h * 1.18, size * 1.18
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=int(h / 3), fill=c + ((90,) if dim else (255,)),
                        outline=(255, 255, 255) if hi else INK, width=10 if hi else 5)
    rt(frame, x, y, label or DAYS[i], int(size), colour=(255, 255, 255), maxw=w - 20)


def latest(ts, t):
    return sum(1 for x in ts if t >= x)


def scene_intro(frame, s, t):
    q = t - s["t0"]
    item(frame, "calendar", 960, 600, 460 * ease_back(q / 0.5), rot=4 * math.sin(t * 2))
    for i in range(7):
        a = i / 7 * 2 * math.pi + t * 0.6
        k = ease_back((q - 0.1 * i) / 0.4)
        if k > 0.05:
            block(frame, 960 + 620 * math.cos(a), 610 + 300 * math.sin(a), i, w=230 * k, h=100 * k, size=40 * k)
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(190, 1730), scale=0.36)
        rt(frame, 960, 140, "DAYS OF THE WEEK!", int(150 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)


def grid(frame, t, ts, hi_last=True):
    n = latest(ts, t)
    pos = [(960 + (i - 1.5) * 330, 400) if i < 4 else (960 + (i - 5) * 330, 600) for i in range(7)]
    for i in range(n):
        k = ease_back((t - ts[i]) / 0.35)
        block(frame, pos[i][0], pos[i][1] - 40 * (1 - k), i, w=290, h=140 * max(0.2, k), size=52, hi=hi_last and i == n - 1)
    return n


def scene_seven(frame, s, t):
    n = grid(frame, t, s["ts"], hi_last=t < s["sum_t"])
    if n:
        rt(frame, 960, 820, str(n), int(140 * ease_back((t - s["ts"][n - 1]) / 0.25)), colour=RAINBOW[n % 6])
    word(frame, "7 DAYS = 1 WEEK!" if t >= s["sum_t"] else "7 DAYS!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=120)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.3)


def scene_chant(frame, s, t):
    n = latest(s["ts"], t)
    for i in range(7):
        x = 960 + (i - 3) * 255
        hi = i == n - 1 and t < s["end_t"]
        bob = 20 * abs(math.sin((t - s["ts"][i]) * 8)) if hi else 0
        block(frame, x, 560 - bob, i, w=235, h=150, size=40, hi=hi, dim=t >= s["t0"] + 0.2 and i >= n and t < s["end_t"])
    if t >= s["end_t"]:
        stars_ring(frame, 960, 560, 900, 160, t, n=12, r=20)
    badge(frame, 960, 300, s["label"].rstrip("!"), (255, 77, 109)) if len(s["label"]) < 6 else rt(frame, 960, 300, s["label"], 80, colour=(255, 77, 109))
    word(frame, "SAY IT WITH US!", t, s["t0"], size=110)
    side_kids(frame, t, "happy", xs=(160, 1760), scale=0.3)


def scene_week(frame, s, t):
    i = s["day"]
    q = t - s["t0"]
    d = ImageDraw.Draw(frame, "RGBA")
    k = ease_back(q / 0.4)
    d.rounded_rectangle((960 - 420 * k, 60, 960 + 420 * k, 220), radius=50, fill=DCOL[i] + (255,), outline=INK, width=7)
    if k > 0.3:
        rt(frame, 960, 140, DAYS[i] + "!", int(100 * k), colour=(255, 255, 255), maxw=780)
    for j in range(7):
        block(frame, 520 + j * 145, 290, j, w=130, h=50, size=20, hi=False, dim=j != i, label=DAYS[j][:3])
    if t >= s["act_t"]:
        kk = ease_back((t - s["act_t"]) / 0.4)
        item(frame, WEEK_KEYS[i], 960, 600 - 20 * abs(math.sin(t * 3)), 380 * kk, rot=6 * math.sin(t * 2))
    body(frame, "gul", t, "happy", 360, scale=0.48, hop=10 * abs(math.sin(t * 3)))
    body(frame, "misheal", t, "happy", 1560, scale=0.48, hop=10 * abs(math.sin(t * 3 + 1)))


def scene_letter(frame, s, t):
    i = s["day"]
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 620, 540, 520, 560, fill=DCOL[i])
    rt(frame, 620, 540, s["L"], int(420 * k), colour=(255, 255, 255))
    rt(frame, 1340, 480, DAYS[i], int(120 * k), colour=DCOL[i], maxw=760)
    rt(frame, 1340, 640, f"{s['L']} is for {DAYS[i].capitalize()}", int(56 * k), colour=(255, 255, 255), maxw=760)
    badge(frame, 160, 90, f"{i + 1}/7", DCOL[i])
    side_kids(frame, t, xs=(150, 1770), scale=0.26)


def scene_twins(frame, s, t):
    second = t >= s["say2_t"]
    pair = (5, 6) if second else (1, 3)
    for j, i in enumerate(pair):
        x = 620 + j * 680
        k = ease_back((t - (s["say2_t"] if second else s["t0"])) / 0.4)
        card(frame, x, 480, 460, 420, good=True)
        rt(frame, x, 430, DAYS[i][0], int(260 * k), colour=DCOL[i])
        rt(frame, x, 620, DAYS[i], int(70 * k), colour=DCOL[i], maxw=420)
    word(frame, "BOTH START WITH S!" if second else "BOTH START WITH T!", t, s["say2_t"] if second else s["t0"], y=850, size=110)
    side_kids(frame, t, "happy", xs=(150, 1770), scale=0.28)


def hand(frame, cx, cy, up, t):
    """a cartoon hand; up = how many fingers are raised (0..5), thumb first"""
    d = ImageDraw.Draw(frame)
    skin, sk2 = (242, 194, 155), (214, 160, 120)
    fingers = [(-130, -10, -160, -110), (-85, -80, -95, -270), (-30, -85, -30, -300), (25, -85, 30, -285), (80, -75, 95, -240)]
    for f, (bx, by, tx, ty) in enumerate(fingers):
        raised = f < up
        if not raised:
            tx, ty = bx + (tx - bx) * 0.3, by + (ty - by) * 0.3
        for col, wd in ((INK, 60), (skin if raised else sk2, 48)):
            d.line((cx + bx, cy + by, cx + tx, cy + ty), fill=col, width=wd)
            d.ellipse((cx + tx - wd / 2, cy + ty - wd / 2, cx + tx + wd / 2, cy + ty + wd / 2), fill=col)
    d.rounded_rectangle((cx - 125, cy - 100, cx + 115, cy + 130), radius=60, fill=skin, outline=INK, width=6)


def scene_fingers(frame, s, t):
    n = latest(s["ts"], t)
    hand(frame, 640, 640, min(5, n), t)
    hand(frame, 1280, 640, max(0, n - 5), t)
    if n:
        i = n - 1
        block(frame, 960, 240, i, w=520, h=150, size=80)
        rt(frame, 960, 960, str(n), int(130 * ease_back((t - s["ts"][i]) / 0.25)), colour=RAINBOW[n % 6])
    if t >= s["sum_t"]:
        word(frame, "7 DAYS!", t, s["sum_t"], y=240, size=150)


def seq_row(frame, t, names, q_at, ans=None, ans_t=None, ans_first=False):
    items = list(names)
    n = len(items) + 1
    x0 = 960 - (n - 1) * 170
    slot = 0 if ans_first else n - 1
    j = 0
    for p in range(n):
        x = x0 + p * 340
        if p == slot:
            if ans_t is not None and t >= ans_t:
                block(frame, x, 540, DAYS.index(ans.upper()), w=320, h=160, size=48, hi=True)
                stars_ring(frame, x, 540, 210, 120, t, n=6, r=16)
            else:
                d = ImageDraw.Draw(frame)
                d.rounded_rectangle((x - 160, 460, x + 160, 620), radius=50, outline=(255, 255, 255), width=8, fill=(255, 255, 255, 0))
                rt(frame, x, 540, "?", int(120 + 10 * math.sin(t * 6)), colour=(255, 255, 255))
        else:
            block(frame, x, 540, DAYS.index(items[j].upper()), w=320, h=160, size=48)
            j += 1


def scene_next(frame, s, t):
    seq_row(frame, t, s["seq"], s["t0"], s["ans"], s["answer_t"])
    word(frame, "WHAT COMES NEXT?", t, s["t0"], size=110)
    side_kids(frame, t, "happy" if t >= s["answer_t"] else None, xs=(150, 1770), scale=0.28)


def scene_before(frame, s, t):
    seq_row(frame, t, [s["day"]], s["t0"], s["ans"], s["answer_t"], ans_first=True)
    word(frame, "WHAT COMES BEFORE?", t, s["t0"], size=110)
    side_kids(frame, t, "happy" if t >= s["answer_t"] else None, xs=(150, 1770), scale=0.28)


def train(frame, x0, y, t, labels, gap_i=None, filled=True, w=210):
    """engine at the right end, carriages to the left. labels: list of day indexes in order"""
    d = ImageDraw.Draw(frame)
    n = len(labels)
    ex = x0 + n * (w + 20) + 60
    d.rounded_rectangle((ex - 110, y - 150, ex + 120, y + 70), radius=20, fill=(232, 53, 46), outline=INK, width=6)
    d.rectangle((ex + 40, y - 230, ex + 90, y - 150), fill=(43, 43, 51), outline=INK, width=5)
    d.rectangle((ex - 80, y - 120, ex + 10, y - 50), fill=(158, 216, 255), outline=INK, width=5)
    for wx in (ex - 60, ex + 70):
        d.ellipse((wx - 40, y + 30, wx + 40, y + 110), fill=(43, 43, 51), outline=INK, width=5)
    for k in range(3):
        r = 25 + k * 14
        sx, sy = ex + 65 + k * 30, y - 260 - k * 50 - (t * 40 % 30)
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(235, 235, 240))
    for j, i in enumerate(labels):
        x = x0 + j * (w + 20) + w / 2
        d.line((x + w / 2 - 10, y, x + w / 2 + 30, y), fill=INK, width=8)
        for wx in (x - w / 3, x + w / 3):
            d.ellipse((wx - 28, y + 40, wx + 28, y + 96), fill=(43, 43, 51), outline=INK, width=5)
        if j == gap_i and not filled:
            d.rounded_rectangle((x - w / 2, y - 110, x + w / 2, y + 60), radius=18, outline=(255, 255, 255), width=7)
            rt(frame, x, y - 25, "?", int(100 + 8 * math.sin(t * 6)), colour=(255, 255, 255))
        else:
            block(frame, x, y - 25, i, w=w, h=170, size=34)


def scene_missing(frame, s, t):
    q = t - s["go_t"]
    x0 = -1900 + 1950 * ease_io(min(1, q / 1.5))
    rev = t >= s["answer_t"]
    train(frame, x0, 640, t, list(range(7)), gap_i=s["miss"], filled=rev)
    if rev:
        x = x0 + s["miss"] * 230 + 105
        stars_ring(frame, x, 615, 150, 120, t, n=6, r=16)
    word(frame, DAYS[s["miss"]] + "!" if rev else "WHICH DAY IS MISSING?", t, s["answer_t"] if rev else s["t0"], size=110)
    side_kids(frame, t, xs=(150, 1770), scale=0.26) if q > 1.6 else None


def scene_weekend(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    if t >= s["wd_t"]:
        d.rounded_rectangle((90, 300, 1150, 820), radius=40, fill=(255, 255, 255, 200), outline=INK, width=6)
        rt(frame, 620, 360, "WEEKDAYS: 5", 70, colour=(46, 120, 230))
        for i in range(5):
            k = ease_back((t - s["wd_t"] - i * 0.45) / 0.35)
            if k > 0.05:
                block(frame, 300 + (i % 3) * 320, 520 + (i // 3) * 170, i, w=280 * k, h=130 * k, size=40 * k)
    if t >= s["we_t"]:
        d.rounded_rectangle((1220, 300, 1830, 820), radius=40, fill=(255, 240, 200, 220), outline=INK, width=6)
        rt(frame, 1525, 360, "WEEKEND: 2", 70, colour=(240, 90, 160))
        for j, i in enumerate((5, 6)):
            k = ease_back((t - s["we_t"] - j * 0.5) / 0.35)
            if k > 0.05:
                block(frame, 1525, 520 + j * 170, i, w=320 * k, h=130 * k, size=44 * k)
    word(frame, "5 + 2 = 7!" if t >= s["sum_t"] else "WEEKDAYS & WEEKEND!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)
    if t >= s["sum_t"]:
        side_kids(frame, t, "happy", xs=(160, 1760), scale=0.22)


def scene_sort(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, (lab, col) in enumerate((("WEEKDAY", (46, 120, 230)), ("WEEKEND", (240, 90, 160)))):
        x = 520 + j * 880
        good = t >= s["answer_t"] and (j == 1) == s["we"]
        d.rounded_rectangle((x - 300, 560, x + 300, 900), radius=40, fill=(255, 255, 255, 220), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        rt(frame, x, 620, lab, 70, colour=col)
        if good:
            stars_ring(frame, x, 760, 330, 180, t, n=8, r=18)
    if t >= s["answer_t"]:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x = 960 + ((1400 if s["we"] else 520) - 960) * k
        y = 330 + (760 - 330) * k
    else:
        x, y = 960, 330 + 12 * math.sin(t * 3)
    block(frame, x, y, s["day"], w=400, h=170, size=60)
    word(frame, "WEEKDAY OR WEEKEND?", t, s["t0"], size=100)


def scene_ytt(frame, s, t):
    i = s["day"]
    n = latest(s["ts"], t)
    for j, (lab, di) in enumerate((("YESTERDAY", (i - 1) % 7), ("TODAY", i), ("TOMORROW", (i + 1) % 7))):
        x = 420 + j * 540
        on = n > j
        card(frame, x, 560, 480, 440, good=on and j == 1, dim=not on)
        rt(frame, x, 420, lab, 64, colour=(255, 77, 109) if j == 1 else (80, 80, 100), maxw=440)
        if on:
            k = ease_back((t - s["ts"][j]) / 0.35)
            block(frame, x, 600, di, w=400 * k, h=170 * k, size=54 * k, hi=j == 1)
    d = ImageDraw.Draw(frame)
    for j in range(2):
        x = 690 + j * 540
        d.polygon([(x - 25, 540), (x + 25, 560), (x - 25, 580)], fill=INK)
    side_kids(frame, t, xs=(150, 1770), scale=0.24)


def scene_calendar(frame, s, t):
    n = latest(s["ts"], t)
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((70, 230, 1850, 900), radius=40, fill=(255, 255, 255, 235), outline=INK, width=8)
    d.rounded_rectangle((70, 230, 1850, 330), radius=40, fill=(255, 77, 109), outline=INK, width=8)
    rt(frame, 960, 280, "MY WEEK", 64, colour=(255, 255, 255))
    for i in range(7):
        x = 200 + i * 253
        block(frame, x, 400, i, w=230, h=90, size=30, label=DAYS[i][:3])
        item(frame, WEEK_KEYS[i], x, 600, 170)
        if i < n:
            k = ease_back((t - s["ts"][i]) / 0.35)
            item(frame, "star", x + 70, 760, 110 * k, rot=15 * math.sin(t * 3 + i))
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
    word(frame, "STICKER TIME!", t, s["t0"], size=110)


def scene_fav(frame, s, t):
    if s["who"] == "both":
        side_kids(frame, t, "happy", xs=(400, 1520), scale=0.5)
        for i in range(7):
            a = i / 7 * 2 * math.pi + t * 0.5
            block(frame, 960 + 380 * math.cos(a), 520 + 260 * math.sin(a), i, w=230, h=90, size=32)
        rt(frame, 960, 520, "?", int(200 + 15 * math.sin(t * 5)), colour=(255, 255, 255))
        word(frame, "YOUR FAVOURITE DAY?", t, s["t0"], size=110)
        return
    n = "gul" if s["who"] == "gul" else "misheal"
    body(frame, n, t, "excited", 620, scale=0.62, hop=20 * abs(math.sin(t * 4)), wave=True)
    k = ease_back((t - s["say_t"]) / 0.4)
    block(frame, 1340, 520, s["day"], w=560 * k, h=200 * k, size=70 * k, hi=True)
    item(frame, WEEK_KEYS[s["day"]], 1340, 790, 220 * k)
    word(frame, "MY FAVOURITE DAY!", t, s["t0"], size=100)


def scene_train(frame, s, t):
    q = t - s["t0"]
    x0 = 1950 - q * 260
    train(frame, x0, 640, t, list(range(7)))
    n = latest(s["ts"], t)
    if n:
        word(frame, DAYS[n - 1] + "!", t, s["ts"][n - 1], size=120, col=DCOL[n - 1])
    else:
        word(frame, "CHOO CHOO!", t, s["t0"], size=120)


def scene_outro(frame, s, t):
    for i in range(7):
        a = i / 7 * 2 * math.pi + t * 0.6
        block(frame, 960 + 520 * math.cos(a), 560 + 230 * math.sin(a), i, w=220, h=90, size=32)
    for n, x in (("gul", 760), ("misheal", 1160)):
        body(frame, n, t, "happy", x, scale=0.42, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "GREAT JOB!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


def quiz_draw(frame, vis, t, k):
    if vis == "WEEKEND":
        block(frame, 760, 580, 5, w=360 * k, h=160 * k, size=50 * k)
        block(frame, 1160, 580, 6, w=360 * k, h=160 * k, size=50 * k)
    elif vis in DAYS:
        block(frame, 960, 580, DAYS.index(vis), w=620 * k, h=230 * k, size=90 * k, hi=True)
    else:
        rt(frame, 960, 580, vis, int(300 * k), colour=RAINBOW[2])


def scene_weather(frame, s, t):
    i = s["day"]
    block(frame, 960, 180, i, w=560, h=150, size=74, hi=True)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        item(frame, s["w"], 960, 580, 400 * k, rot=4 * math.sin(t * 2))
        word(frame, s["w"].upper() + "!", t, s["answer_t"], y=880, size=120, col=DCOL[i])
    else:
        rt(frame, 960, 560, "?", int(240 + 15 * math.sin(t * 6)), colour=(255, 255, 255))
    for j in range(7):
        block(frame, 300 + j * 220, 1010, j, w=200, h=60, size=24, dim=j != i, label=DAYS[j][:3])
    side_kids(frame, t, xs=(170, 1750), scale=0.28, feet=950)


def scene_sleeps(frame, s, t):
    n = latest(s["ts"], t)
    seq = [s["today"]] + s["path"]
    for j, di in enumerate(seq):
        x = 300 + j * 440
        block(frame, x, 380, di, w=380, h=150, size=50, hi=(j == len(seq) - 1 and t >= s["sum_t"]), dim=j > n)
        if j == 0:
            rt(frame, x, 250, "TODAY", 56, colour=(255, 77, 109))
        elif j <= n:
            k = ease_back((t - s["ts"][j - 1]) / 0.35)
            item(frame, "moon", x, 600, 160 * k)
            rt(frame, x, 760, str(j), int(90 * k), colour=RAINBOW[j % 6])
    word(frame, "3 SLEEPS!" if t >= s["sum_t"] else "HOW MANY SLEEPS?", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], size=110)


def scene_times(frame, s, t):
    p = s["part"]
    tint = {"morning": (255, 220, 120, 40), "afternoon": (255, 255, 255, 0), "night": (20, 20, 70, 140)}[p]
    if tint[3]:
        from PIL import Image
        frame.alpha_composite(Image.new("RGBA", frame.size, tint))
    k = ease_back((t - s["t0"]) / 0.4)
    if p == "morning":
        item(frame, "sunny", 1450, 300, 300 * k)
        item(frame, "toast", 1450, 650, 260 * k)
    elif p == "afternoon":
        item(frame, "sunny", 1450, 220, 220 * k)
        item(frame, "ball", 1450, 620, 280 * k)
    else:
        item(frame, "moon", 1450, 300, 280 * k)
        item(frame, "bed", 1450, 700, 380 * k)
    body(frame, "gul", t, "tired" if p == "night" else "happy", 520, scale=0.48)
    body(frame, "misheal", t, "tired" if p == "night" else "happy", 880, scale=0.48)
    word(frame, p.upper() + "!", t, s["say_t"], size=140, col=(255, 210, 40) if p == "night" else (255, 140, 26))


def scene_mixed(frame, s, t):
    n = latest(s["ts"], t)
    # unsorted spots for days not yet placed
    from longkit import G as KG
    MIX = [3, 0, 5, 1, 6, 2, 4]
    for i in range(7):
        home = (960 + (i - 3) * 255, 760)
        mess = (300 + MIX.index(i) * 220, 360 + 60 * ((i * 3) % 2))
        if i < n:
            k = ease_io(min(1, (t - s["ts"][i]) / 0.5))
            x, y = mess[0] + (home[0] - mess[0]) * k, mess[1] + (home[1] - mess[1]) * k
            block(frame, x, y, i, w=235, h=130, size=36, hi=i == n - 1 and t < s["done_t"])
        else:
            block(frame, mess[0], mess[1] + 10 * math.sin(t * 3 + i), i, w=200, h=110, size=30, )
    if t >= s["done_t"]:
        confetti(frame, t, s["done_t"])
        word(frame, "IN ORDER!", t, s["done_t"], size=130)
    else:
        word(frame, "MIXED UP!", t, s["t0"], size=120)


def scene_rhyme(frame, s, t):
    n = latest(s["l"], t)
    li = (n - 1) % 4 if n else 0
    groups = [(0, 1), (2, 3), (4, 5), (6,)]
    for i in range(7):
        a = i / 7 * 2 * math.pi - math.pi / 2 + t * 0.4
        hi = n and i in groups[li]
        block(frame, 960 + 640 * math.cos(a), 520 + 300 * math.sin(a), i, w=240, h=100, size=34, hi=hi)
    for nm, x in (("gul", 800), ("misheal", 1120)):
        body(frame, nm, t, "happy", x, scale=0.4, hop=25 * abs(math.sin(t * 4 + (0 if nm == "gul" else 1))), wave=True)
    word(frame, "CLAP ALONG!", t, s["t0"], size=110)


SCENES = {"intro": scene_intro, "seven": scene_seven, "chant": scene_chant, "week": scene_week, "letter": scene_letter, "twins": scene_twins,
          "fingers": scene_fingers, "next": scene_next, "before": scene_before, "missing": scene_missing, "weekend": scene_weekend,
          "sort": scene_sort, "ytt": scene_ytt, "calendar": scene_calendar, "fav": scene_fav, "train": scene_train, "outro": scene_outro, "weather": scene_weather, "sleeps": scene_sleeps,
          "times": scene_times, "mixed": scene_mixed, "rhyme": scene_rhyme,
          "quiz": lambda f, s, t: K.scene_quiz(f, s, t, draw=quiz_draw)}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L18 Days of the Week", "Days of the Week for Kids")
K.CFG["title_items"] = ["calendar", "book", "pizza", "ball", "house"]

if __name__ == "__main__":
    K.main()
