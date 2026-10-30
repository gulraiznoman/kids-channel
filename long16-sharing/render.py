"""Animate L16 "Sharing is Caring".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW, G

A16 = HERE / "art"
ART = {k: A16 / f"item_{k}.png" for k in ("cookie", "bucket", "spade", "sandcastle", "crayons", "plate", "swing", "car", "umbrella", "heart")}
ART.update({"pizza": ROOT / "long08-colors-shapes/art/item_pizza.png", "plate2": A16 / "item_plate.png", "teddy": ROOT / "long15-potty/art/item_teddy.png", "apple": ROOT / "ep01-fruits/art/fruit_apple.png",
            "strawberry": ROOT / "ep01-fruits/art/fruit_strawberry.png", "ball": ROOT / "long04-good-habits/art/item_ball.png",
            "crayon1": ROOT / "long04-good-habits/art/item_crayon.png", "slide": ROOT / "long12-trucks/art/item_slide.png"})
BGS = {"room": ROOT / "long07-feelings/art/bg_room.png", "park": ROOT / "long05-body-parts/art/bg_park.png"}


def pair(frame, t, emo_g=None, emo_m=None, xg=640, xm=1280, scale=0.5, wave_g=False, wave_m=False, hop=0.0):
    body(frame, "gul", t, emo_g, xg, scale=scale, wave=wave_g, hop=hop * abs(math.sin(t * 5)))
    body(frame, "misheal", t, emo_m, xm, scale=scale, wave=wave_m, hop=hop * abs(math.sin(t * 5 + 1)))


def scene_intro(frame, s, t):
    if t < s["stop_t"]:
        q = t - s["tug_t"]
        pull = 40 * math.sin(q * 9)
        pair(frame, t, "angry", "angry", 700 + pull, 1220 + pull)
        item(frame, "teddy", 960 + pull, 640, 260, rot=10 * math.sin(q * 9))
        word(frame, "MINE!", t, s["tug_t"], size=170, col=(232, 53, 46))
    else:
        k = t - s["stop_t"]
        pair(frame, t, "happy" if t < s["kids_t"] else None, "happy" if t < s["kids_t"] else None, 700, 1220, wave_g=True, wave_m=True, hop=25)
        item(frame, "teddy", 960, 720, 240)
        item(frame, "heart", 960, 440 - 20 * abs(math.sin(t * 3)), 260 * ease_back(k / 0.4))
        rt(frame, 960, 160, "SHARING IS CARING!", int(170 * ease_back(k / 0.35)), maxw=1700)
        if k < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k / 0.3)))))


def scene_what(frame, s, t):
    pair(frame, t, "happy", "happy", 640, 1280, wave_g=t >= s["l2"])
    if t >= s["l3"]:
        sz = 200 + 120 * ease_back((t - s["l3"]) / 0.6)
        item(frame, "heart", 960, 420, sz)
    else:
        item(frame, "ball", 960 - 150 * math.cos(t * 1.5), 600 - 120 * abs(math.sin(t * 3)), 160)
    word(frame, "SHARING!", t, s["t0"], size=140)


def scene_story(frame, s, t):
    key = s["key"]
    solved = t >= s["sol_t"]
    happy = t >= s["end_t"]
    badge(frame, 160, 90, f"{s['num']}/10")
    g_has = s["num"] % 2 == 1
    sad_emo = "sad" if t >= s["prob_t"] and not solved else None
    emo_g = "happy" if happy else (None if g_has else sad_emo)
    emo_m = "happy" if happy else (sad_emo if g_has else None)
    xg, xm = 600, 1320
    if solved and key in ("umbrella",):
        xm = 1000
    pair(frame, t, emo_g, emo_m, xg, xm, wave_g=solved and g_has, wave_m=solved and not g_has, hop=20 if happy else 0)
    if key == "cookie":
        if solved:
            k = min(1, (t - s["sol_t"]) / 0.8)
            item(frame, "cookie", 900 - 200 * k, 560, 170)
            item(frame, "cookie", 1020 + 200 * k, 560, 170)
        else:
            item(frame, "cookie", 820, 560, 240)
    elif key == "crayons":
        item(frame, "plate", 960, 860, 380)
        item(frame, "crayons", 960 if solved else 1180, 640, 240)
    elif key == "swing":
        item(frame, "swing", 960, 640, 520)
        if solved:
            k = int((t - s["sol_t"]) / 2.5) % 2
            body(frame, "gul" if k == 0 else "misheal", t, "excited", 960 + 120 * math.sin(t * 3), feet=980, scale=0.3)
    elif key == "umbrella":
        ux = 820 if solved else 600
        item(frame, "umbrella", ux, 380, 360 if solved else 240)
        d = ImageDraw.Draw(frame, "RGBA")
        for j in range(40):
            p = (t * 1.3 + j / 40) % 1
            x = (j * 53) % 1920
            if solved and 560 < x < 1080:
                continue
            d.line((x, 200 + p * 800, x - 8, 230 + p * 800), fill=(110, 170, 255, 220), width=5)
    elif key == "sandcastle":
        if solved:
            item(frame, "sandcastle", 960, 820, 300 * min(1, (t - s["sol_t"]) / 2.5) + 40)
        item(frame, "bucket", 800, 900, 150)
        item(frame, "spade", 1120, 880, 170, rot=20 * math.sin(t * 6) if solved else 0)
    elif key == "car":
        cx = 1100 if not solved else 820 - 60 * math.sin(t * 2)
        item(frame, "car", cx, 900, 220)
    elif key == "ball":
        if solved:
            ph = (t * 0.8) % 1
            item(frame, "ball", 640 + 680 * (ph if int(t * 0.8) % 2 == 0 else 1 - ph), 500 - 220 * math.sin(math.pi * ph), 150)
        else:
            item(frame, "ball", 760, 860 - 60 * abs(math.sin(t * 4)), 150)
    elif key in ("pizza", "apple"):
        if solved:
            k = min(1, (t - s["sol_t"]) / 0.8)
            item(frame, key, 900 - 200 * k, 560, 170)
            item(frame, key, 1020 + 200 * k, 560, 170)
        else:
            item(frame, key, 820, 560, 240)
    elif key == "teddy":
        item(frame, "teddy", 1150 if not solved else 760, 760, 200)
    if happy:
        stars_ring(frame, 960, 560, 520, 260, t, n=10)
        word(frame, "SHARING IS CARING!", t, s["end_t"], size=120)
    elif solved:
        word(frame, {"swing": "TAKE TURNS!", "car": "ASK NICELY!", "sandcastle": "TEAMWORK!"}.get(key, "LET'S SHARE!"), t, s["sol_t"], size=130, col=(59, 193, 74))
    elif t >= s["prob_t"]:
        word(frame, "WHAT CAN WE DO?", t, s["prob_t"], size=120)


FAIR_ART = {"cookie": "cookie", "apple": "apple", "crayons1": "crayon1", "strawberry": "strawberry"}


def scene_fair(frame, s, t):
    n, p = s["n"], s["people"]
    art = FAIR_ART[s["key"]]
    each = n // p
    xs = [400 + i * (1120 / max(1, p - 1)) for i in range(p)] if p > 1 else [960]
    if p == 4:
        xs = [330, 750, 1170, 1590]
    if p == 3:
        xs = [480, 960, 1440]
    for i, x in enumerate(xs):
        nm = "gul" if i % 2 == 0 else "misheal"
        body(frame, nm, t, "happy", x, scale=0.3, feet=800)
        item(frame, "plate", x, 880, 260 if p == 2 else 200)
    dealt = 0
    if t >= s["deal_t"]:
        dealt = min(n, int((t - s["deal_t"]) / 0.18) + 1)
    for j in range(n):
        if j < dealt:
            who = j % p
            slot = j // p
            x = xs[who] + (slot - (each - 1) / 2) * (55 if p == 2 else 40)
            item(frame, art, x, 860, 80 if p == 2 else 60)
        else:
            x = 960 + ((j - dealt) - (n - dealt - 1) / 2) * 70
            item(frame, art, x, 300, 80)
    if t >= s["answer_t"]:
        word(frame, f"{each} EACH! FAIR!", t, s["answer_t"], size=130, col=(59, 193, 74))
    else:
        word(frame, f"{n} FOR {p} FRIENDS", t, s["t0"], size=120)


def scene_ask(frame, s, t):
    asker = "gul" if s["key"] != "swing" else "misheal"
    pair(frame, t, None, None, 640, 1280, wave_g=t >= s["ans_t"], wave_m=t >= s["ans_t"])
    item(frame, s["key"], 960, 640, 260)
    if t >= s["ans_t"]:
        item(frame, "heart", 960, 330, 200)
        word(frame, "YES! HERE YOU GO!", t, s["ans_t"], size=120, col=(59, 193, 74))
    else:
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((420, 150, 1500, 320), radius=60, fill=(255, 255, 255), outline=INK, width=6)
        rt(frame, 960, 235, "CAN I HAVE A TURN, PLEASE?", 70, colour=(255, 107, 139), maxw=1000)


KIND_PIC = {"share": "ball", "grab": "car", "wait": "slide", "mine": "teddy", "help": "sandcastle", "thanks": "heart",
            "push": "slide", "invite": "ball", "hide": "cookie", "sorry": "heart"}


def scene_kind(frame, s, t):
    rt(frame, 960, 150, s["q"], int(70 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)
    item(frame, KIND_PIC[s["key"]], 960, 520, 320)
    if t >= s["answer_t"]:
        d = ImageDraw.Draw(frame)
        k = ease_back((t - s["answer_t"]) / 0.3)
        if s["good"]:
            item(frame, "heart", 1300, 500, 200 * k)
            word(frame, "KIND!", t, s["answer_t"], y=840, size=160, col=(59, 193, 74))
        else:
            r = 230 * k
            d.ellipse((960 - r, 520 - r, 960 + r, 520 + r), outline=(232, 53, 46), width=24)
            d.line((960 - r * 0.7, 520 + r * 0.7, 960 + r * 0.7, 520 - r * 0.7), fill=(232, 53, 46), width=24)
            word(frame, "UNKIND!", t, s["answer_t"], y=840, size=160, col=(232, 53, 46))
    side_kids(frame, t, xs=(170, 1750))


def scene_heart(frame, s, t):
    n = sum(1 for x in s["grow"] if t >= x)
    item(frame, "heart", 960, 520, 160 + 90 * n + 10 * math.sin(t * 4))
    labels = ["SHARE!", "TAKE TURNS!", "THANK YOU!", "HELP!"]
    for i in range(n):
        x = 470 + i * 330
        rt(frame, x, 870, labels[i], 54, colour=RAINBOW[i % 6], maxw=310)
    side_kids(frame, t, "happy", xs=(160, 1760))
    word(frame, "HAPPY HEART!", t, s["t0"], size=130, col=(255, 77, 109))


def scene_outro(frame, s, t):
    for i, k in enumerate(("cookie", "ball", "crayons", "car", "umbrella", "heart", "teddy")):
        item(frame, k, (i * 300 + t * 120) % 2200 - 140, 980 - 20 * abs(math.sin(t * 4 + i)), 150)
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, scale=0.5, feet=900, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE, KIND FRIENDS!", int(130 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 140, "SHARING IS CARING!", int(120 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


def scene_turns(frame, s, t):
    item(frame, "slide", 960, 640, 560)
    n = sum(1 for x in s["ts"] if t >= x)
    if n:
        who = "gul" if (n - 1) % 2 == 0 else "misheal"
        q = min(1, (t - s["ts"][n - 1]) / 1.4)
        x = 1140 - 420 * q
        y = 420 + 520 * q
        body(frame, who, t, "excited", x, feet=y, scale=0.28, wave=True)
        waiting = "misheal" if who == "gul" else "gul"
        body(frame, waiting, t, "happy", 1500, scale=0.4, wave=True)
        word(frame, ("GUL'S TURN!" if who == "gul" else "MISHU'S TURN!"), t, s["ts"][n - 1], size=130)
    else:
        side_kids(frame, t, "happy", xs=(300, 1620), scale=0.4)
        word(frame, "MY TURN, YOUR TURN!", t, s["t0"], size=120)


def scene_thanks(frame, s, t):
    k = min(1, (t - s["t0"]) / 1.0)
    giver_g = s["key"] in ("crayons", "ball")
    x = 640 + 640 * ease_io(k) if giver_g else 1280 - 640 * ease_io(k)
    pair(frame, t, "happy", "happy", 640, 1280, wave_g=t >= s["ty_t"], wave_m=t >= s["ty_t"])
    item(frame, s["key"], x, 600, 200)
    if t >= s["ty_t"]:
        item(frame, "heart", 960, 330 - 15 * abs(math.sin(t * 4)), 200)
        word(frame, "THANK YOU!", t, s["ty_t"], size=150, col=(255, 77, 109))
    else:
        word(frame, "WHAT DO WE SAY?", t, s["t0"], size=120)


def scene_family(frame, s, t):
    who = "gul" if s["num"] % 2 == 1 else "misheal"
    body(frame, who, t, "happy", 640, scale=0.5, wave=True)
    d = ImageDraw.Draw(frame)
    # simple grown-up / little one: a bigger or smaller Gul-family silhouette is not available, so show a heart family card
    K.card(frame, 1300, 560, 520, 520)
    rt(frame, 1300, 380, {1: "PAPA", 2: "BABY COUSIN", 3: "GRANDMA", 4: "LITTLE BROTHER"}[s["num"]], 64, colour=(255, 107, 139), maxw=470)
    item(frame, "heart", 1300, 600, 220)
    k = min(1, (t - s["t0"]) / 1.2)
    item(frame, s["key"], 760 + 540 * ease_io(k), 620 - 120 * math.sin(math.pi * k), 160)
    word(frame, "SHARE WITH FAMILY!", t, s["t0"], size=110)


def scene_chant(frame, s, t):
    i = max([j for j, x in enumerate(s["l"]) if t >= x] or [0])
    pair(frame, t, "happy", "happy", 640, 1280, wave_g=True, wave_m=True, hop=25)
    item(frame, ["heart", "cookie", "swing", "heart"][i % 4], 960, 560, 260)
    word(frame, "SHARING IS CARING!", t, s["t0"], size=120)


SCENES = {"intro": scene_intro, "what": scene_what, "story": scene_story, "fair": scene_fair, "ask": scene_ask, "kind": scene_kind,
          "heart": scene_heart, "outro": scene_outro, "turns": scene_turns, "thanks": scene_thanks, "family": scene_family, "chant": scene_chant}
K.configure(__file__, {"gul": "polo", "misheal": "yellow"}, ART, BGS, SCENES, "L16 Sharing is Caring", "Sharing is Caring for Kids")
K.CFG["title_items"] = ["heart", "cookie", "ball", "crayons", "teddy"]

if __name__ == "__main__":
    K.main()
