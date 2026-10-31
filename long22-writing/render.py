"""Animate L22 "Learn to Write ABC".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW
from strokes import UP, LOW, partial, arc

A22 = HERE / "art"
E1, L1, L4, L5, L8, L9 = (ROOT / "ep01-fruits/art", ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art", ROOT / "long05-body-parts/art",
                          ROOT / "long08-colors-shapes/art", ROOT / "long09-eggs/art")
A10 = ROOT / "long10-abc/art"
ART = {k: A22 / f"item_{k}.png" for k in ("pencil", "crayon", "eraser", "paper")}
ART.update({"apple": E1 / "fruit_apple.png", "ball": L4 / "item_ball.png", "cat": L1 / "fruit_kitten.png", "dog": L1 / "fruit_puppy.png",
            "elephant": L1 / "fruit_elephant.png", "fish": L1 / "fruit_fish.png", "grapes": E1 / "fruit_grapes.png", "hat": L8 / "item_tophat.png",
            "ice cream": L5 / "item_icecream.png", "jellyfish": L1 / "fruit_jellyfish.png", "kite": L8 / "item_kite.png", "lion": L1 / "fruit_cub.png",
            "monkey": L1 / "fruit_monkey.png", "nest": L9 / "item_nest.png", "octopus": L1 / "fruit_octopus.png", "pizza": L8 / "item_pizza.png",
            "queen": A10 / "item_queen.png", "rainbow": L1 / "fruit_rainbow.png", "sun": L1 / "fruit_sunny.png", "train": L1 / "fruit_train.png",
            "umbrella": L4 / "item_umbrella.png", "violin": A10 / "item_violin.png", "whale": L1 / "fruit_whale.png", "xylophone": A10 / "item_xylophone.png",
            "yo-yo": A10 / "item_yoyo.png", "zebra": A10 / "item_zebra.png", "hand": L5 / "item_hand.png"})
BGS = {"studio": L8 / "bg_studio.png"}
ST = {**UP, **LOW}
BLUE = (157, 216, 255)


def paper(frame, x0, y0, x1, y1, lines=6):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x0 + 10, y0 + 12, x1 + 10, y1 + 12), radius=26, fill=(0, 0, 0, 40))
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=(255, 255, 255), outline=INK, width=6)
    for i in range(1, lines):
        y = y0 + (y1 - y0) * i / lines
        d.line((x0 + 24, y, x1 - 24, y), fill=BLUE, width=4)


def mp(p, box, flip=False):
    x, y, w, h = box
    return (x + (1 - p[0] if flip else p[0]) * w, y + p[1] * h)


def dots(d, strokes, box, step=26, r=6, col=(205, 210, 222), flip=False):
    for poly in strokes:
        pts = [mp(p, box, flip) for p in poly]
        run = 0
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
            while run <= L:
                x, y = a[0] + (b[0] - a[0]) * run / L, a[1] + (b[1] - a[1]) * run / L
                d.ellipse((x - r, y - r, x + r, y + r), fill=col)
                run += step
            run -= L


def ink(d, strokes, box, col, wd=26, flip=False):
    for poly in strokes:
        pts = [mp(p, box, flip) for p in poly]
        if len(pts) > 1:
            d.line(pts, fill=col, width=wd, joint="curve")
        for x, y in (pts[0], pts[-1]):
            d.ellipse((x - wd / 2, y - wd / 2, x + wd / 2, y + wd / 2), fill=col)


def letter(frame, L, cx, cy, h, col, f=1.0, wd=None, guide=False, pencil=False, nums=False, flip=False):
    """L drawn in a box h tall; f = fraction written. returns tip position"""
    d = ImageDraw.Draw(frame)
    w = h * 0.82
    box = (cx - w / 2, cy - h / 2, w, h)
    wd = wd or max(8, int(h / 15))
    strokes = ST[L]
    if guide:
        dots(d, strokes, box, step=max(14, h / 24), r=max(3, h / 90), flip=flip)
    tip = mp(strokes[0][0], box, flip)
    if f > 0:
        part, tp = partial(strokes, min(1, f))
        ink(d, part, box, col, wd, flip)
        tip = mp(tp, box, flip)
    if nums:
        for i, poly in enumerate(strokes):
            x, y = mp(poly[0], box, flip)
            d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(255, 77, 109), outline=INK, width=3)
            rt(frame, x, y, str(i + 1), 34, colour=(255, 255, 255))
    if pencil and 0 < f < 1:
        item(frame, "pencil", tip[0] + 75, tip[1] - 75, 210)
    return tip


def scene_intro(frame, s, t):
    paper(frame, 420, 300, 1500, 900)
    q = t - s["write_t"]
    for j, L in enumerate("ABC"):
        letter(frame, L, 640 + j * 320, 600, 420, RAINBOW[j], f=min(1, max(0, (q - j * 0.55) / 0.5)), pencil=True)
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(190, 1730), scale=0.36)
        rt(frame, 960, 150, "LEARN TO WRITE ABC!", int(140 * ease_back((t - s["title_t"]) / 0.35)), maxw=1700)


def scene_ready(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    key = s["key"]
    if key == "sit":
        body(frame, "gul", t, "proud", 760, scale=0.6)
        rt(frame, 1350, 540, "SIT UP TALL!", int(100 * k), colour=(46, 130, 235), maxw=640)
        return
    card(frame, 720, 540, 560, 560)
    if key == "grip":
        item(frame, "hand", 720, 600, 400 * k)
        item(frame, "pencil", 790, 420, 300 * k)
    else:
        item(frame, key, 720, 540, 400 * k)
    rt(frame, 1340, 540, {"pencil": "PENCIL!", "grip": "HOLD IT LIKE THIS!", "paper": "PAPER FLAT!"}[key], int(100 * k), colour=(46, 130, 235), maxw=680)
    badge(frame, 160, 90, f"STEP {s['num']}", (46, 130, 235))
    side_kids(frame, t, xs=(150, 1770), scale=0.26)


def warm_strokes(kind):
    if kind == "down":
        return [[(x, .05), (x, .95)] for x in (.08, .22, .36, .5, .64, .78, .92)]
    if kind == "across":
        return [[(.05, y), (.95, y)] for y in (.1, .36, .62, .9)]
    if kind == "slant":
        return [[(x, .05), (x + .14, .95)] for x in (.03, .2, .37, .54, .71)]
    if kind == "zigzag":
        return [[(.04 + i * .092, (y if i % 2 == 0 else y + .26)) for i in range(11)] for y in (.05, .62)]
    if kind == "wave":
        return [[(.03 + i * .94 / 40, y + .09 * math.sin(i * .62)) for i in range(41)] for y in (.2, .72)]
    return [arc(x, .5, .085, .3, -90, -450) for x in (.12, .31, .5, .69, .88)]


def scene_warm(frame, s, t):
    paper(frame, 260, 260, 1660, 900, lines=5)
    q = (t - s["go_t"]) / max(0.5, s["t1"] - s["go_t"] - 1.4)
    strokes = warm_strokes(s["line"])
    box = (320, 310, 1280, 540)
    d = ImageDraw.Draw(frame)
    dots(d, strokes, box, step=26, r=5)
    part, tp = partial(strokes, min(1, max(0.001, q)))
    ink(d, part, box, (255, 77, 109), wd=16)
    if q < 1:
        x, y = mp(tp, box)
        item(frame, "pencil", x + 75, y - 75, 210)
    word(frame, {"down": "DOWN!", "across": "ACROSS!", "slant": "SLANT!", "zigzag": "ZIG ZAG!", "wave": "WAVY!", "circle": "CIRCLES!"}[s["line"]], t, s["say_t"], size=120)
    side_kids(frame, t, xs=(120, 1800), scale=0.24)


def scene_trace(frame, s, t):
    n = s["num"]
    col = RAINBOW[n % 6]
    paper(frame, 180, 110, 1110, 980)
    f = min(1, max(0, (t - s["draw_t"]) / max(0.6, s["draw_end"] - s["draw_t"])))
    letter(frame, s["L"], 645, 545, 640, col, f=f, guide=True, pencil=True, nums=t < s["draw_t"])
    if s["draw_end"] <= t < s["word_t"]:
        f2 = min(1, (t - s["draw_end"]) / (s["word_t"] - s["draw_end"] - 0.15))
        h, w = 640, 640 * 0.82
        part, tp = partial(ST[s["L"]], f2)
        x, y = mp(tp, (645 - w / 2, 545 - h / 2, w, h))
        item(frame, "hand", x + 40, y + 60, 190)
    badge(frame, 160, 70, f"{n}/26", col)
    if t >= s["word_t"]:
        k = ease_back((t - s["word_t"]) / 0.4)
        item(frame, s["key"], 1500, 370, 380 * k)
        rt(frame, 1500, 640, s["w"], int(84 * k), colour=col, maxw=640)
    else:
        rt(frame, 1500, 460, s["L"], int(330 * ease_back((t - s["t0"]) / 0.3)), colour=col)
    side_kids(frame, t, xs=(1250, 1790), scale=0.2)


def scene_cheer(frame, s, t):
    side_kids(frame, t, "excited", xs=(420, 1500), scale=0.45)
    rt(frame, 960, 190, f"{s['done']} LETTERS!", int(170 * ease_back((t - s["t0"]) / 0.35)), maxw=1300)
    stars_ring(frame, 960, 240, 720, 170, t, n=10, r=24)


def scene_allabc(frame, s, t):
    n = sum(1 for x in s["ts"] if t >= x)
    paper(frame, 100, 170, 1820, 960, lines=4)
    for i, L in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:n]):
        x, y = 200 + (i % 9) * 190, 300 + (i // 9) * 250
        letter(frame, L, x, y, 170, RAINBOW[i % 6], f=min(1, (t - s["ts"][i]) / 0.35))
    word(frame, "26 LETTERS!" if t >= s["sum_t"] else "A TO Z!", t, s["sum_t"] if t >= s["sum_t"] else s["t0"], y=90, size=120)


def scene_sort(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    for j, (lab, col) in enumerate((("STRAIGHT", (46, 130, 235)), ("CURVY", (255, 77, 109)))):
        x = 430 + j * 1060
        good = t >= s["answer_t"] and (j == 0) == s["straight"]
        d.rounded_rectangle((x - 300, 620, x + 300, 960), radius=40, fill=(255, 255, 255, 225), outline=(59, 193, 74) if good else INK, width=14 if good else 6)
        rt(frame, x, 655, lab, 62, colour=col)
    if t >= s["answer_t"]:
        k = ease_io(min(1, (t - s["answer_t"]) / 0.6))
        x = 960 + ((430 if s["straight"] else 1490) - 960) * k
        y, h = 400 + 420 * k, 460 - 280 * k
    else:
        x, y, h = 960, 400, 460
    letter(frame, s["L"], x, y, h, (140, 80, 210))
    word(frame, "STRAIGHT OR CURVY?", t, s["t0"], y=90, size=100)


def scene_right(frame, s, t):
    for j in range(2):
        x = 620 + j * 680
        ok = j == s["pos"]
        good = t >= s["answer_t"] and ok
        card(frame, x, 560, 520, 620, good=good, dim=t >= s["answer_t"] and not ok)
        letter(frame, s["L"], x, 560, 420, RAINBOW[j + 1], flip=not ok)
        if good:
            stars_ring(frame, x, 560, 300, 340, t, n=8, r=18)
    word(frame, "WHICH ONE IS RIGHT?", t, s["t0"], y=110, size=100)
    side_kids(frame, t, xs=(130, 1790), scale=0.24)


def scene_missing(frame, s, t):
    n = len(s["seq"])
    for i, L in enumerate(s["seq"]):
        x = 960 + (i - (n - 1) / 2) * 340
        card(frame, x, 540, 300, 380)
        if i == s["miss"]:
            f = min(1, max(0, (t - s["answer_t"]) / 0.8))
            if f > 0:
                letter(frame, L, x, 540, 240, (255, 77, 109), f=f, pencil=True)
            else:
                rt(frame, x, 540, "?", int(170 + 12 * math.sin(t * 6)), colour=(255, 77, 109))
        else:
            letter(frame, L, x, 540, 240, RAINBOW[i])
    word(frame, "WHICH LETTER IS MISSING?", t, s["t0"], size=100)
    side_kids(frame, t, xs=(130, 1790), scale=0.24)


def scene_lower(frame, s, t):
    paper(frame, 460, 140, 1460, 960)
    f = min(1, max(0, (t - s["draw_t"]) / max(0.6, s["draw_end"] - s["draw_t"])))
    letter(frame, s["L"], 960, 550, 620, RAINBOW[s["num"] % 6], f=f, guide=True, pencil=True)
    badge(frame, 160, 90, f"{s['num']}/{s['of']}", RAINBOW[s["num"] % 6])
    side_kids(frame, t, xs=(200, 1720), scale=0.3)


def scene_tool(frame, s, t):
    key = s["key"]
    d = ImageDraw.Draw(frame)
    fill, col, wd = {"crayon": ((255, 255, 255), (255, 77, 109), 34), "chalk": ((46, 92, 74), (245, 245, 245), 26), "sand": ((240, 215, 150), (190, 150, 90), 40)}[key]
    d.rounded_rectangle((430, 190, 1490, 930), radius=26, fill=fill, outline=(150, 100, 60) if key == "chalk" else INK, width=14 if key == "chalk" else 6)
    f = min(1, max(0, (t - s["draw_t"]) / max(0.6, s["draw_end"] - s["draw_t"] - 0.5)))
    for j, L in enumerate("ABC"):
        tip = letter(frame, L, 640 + j * 320, 560, 420, col, f=min(1, max(0, f * 3 - j)), wd=wd)
        if 0 < f * 3 - j < 1:
            x, y = tip
            if key == "sand":
                item(frame, "hand", x + 45, y + 70, 200)
            elif key == "chalk":
                d.rectangle((x, y - 90, x + 34, y), fill=(255, 255, 255), outline=INK, width=4)
            else:
                item(frame, "crayon", x + 70, y - 70, 200)
    word(frame, {"crayon": "CRAYON!", "chalk": "CHALK!", "sand": "SAND!"}[key], t, s["say_t"], size=120)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.3)


def write_word(frame, s, t, cy=560, h=340):
    w = s["word"]
    n = len(w)
    gap = min(420, 1400 / n)
    h = min(h, gap * 0.95 / 0.82)
    f = min(1, max(0, (t - s["draw_t"]) / max(0.6, s["draw_end"] - s["draw_t"]))) * n
    for i, L in enumerate(w):
        letter(frame, L, 960 + (i - (n - 1) / 2) * gap, cy, h, RAINBOW[i], f=min(1, max(0, f - i)), guide=True, pencil=True)


def scene_wordw(frame, s, t):
    paper(frame, 180, 250, 1740, 870)
    write_word(frame, s, t)
    if t >= s["pic_t"]:
        item(frame, s["key"], 1690, 300, 250 * ease_back((t - s["pic_t"]) / 0.4))
    word(frame, "WRITE A WORD!", t, s["t0"], y=120, size=110)
    side_kids(frame, t, xs=(110, 1810), scale=0.22)


def scene_name(frame, s, t):
    paper(frame, 180, 230, 1740, 830)
    write_word(frame, s, t, cy=530)
    body(frame, s["who"], t, "excited", 1830, scale=0.24, wave=True)
    word(frame, "MY NAME!", t, s["t0"], y=120, size=120)


def scene_yourname(frame, s, t):
    paper(frame, 300, 240, 1620, 760)
    d = ImageDraw.Draw(frame)
    d.line((420, 620, 1500, 620), fill=(255, 77, 109), width=8)
    item(frame, "pencil", 1360, 500 + 15 * math.sin(t * 5), 260)
    word(frame, "YOUR NAME!", t, s["t0"], y=120, size=120)
    side_kids(frame, t, "happy", xs=(170, 1750), scale=0.32)


def scene_outro(frame, s, t):
    paper(frame, 540, 280, 1380, 800)
    for j, L in enumerate("ABC"):
        letter(frame, L, 690 + j * 270, 540, 320, RAINBOW[j])
    for n, x in (("gul", 300), ("misheal", 1620)):
        body(frame, n, t, "happy", x, scale=0.45, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "GREAT WRITING!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


SCENES = {"intro": scene_intro, "ready": scene_ready, "warm": scene_warm, "trace": scene_trace, "cheer": scene_cheer, "allabc": scene_allabc, "sort": scene_sort,
          "right": scene_right, "missing": scene_missing, "lower": scene_lower, "tool": scene_tool, "wordw": scene_wordw, "name": scene_name, "yourname": scene_yourname, "outro": scene_outro}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L22 Learn to Write ABC", "Learn to Write ABC for Kids")
K.CFG["title_items"] = ["pencil", "crayon", "paper", "eraser", "apple"]

if __name__ == "__main__":
    K.main()
