"""Animate L15 "Potty Training for Toddlers".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, ease_io, side_kids, stars_ring, confetti, badge, card, INK, RAINBOW, G

A15, L4 = HERE / "art", ROOT / "long04-good-habits/art"
ART = {k: A15 / f"item_{k}.png" for k in ("potty", "toilet", "paper", "stool", "undies", "chart", "star", "teddy")}
L1 = ROOT / "long01-animals-fun/art"
ART.update({"soap": L4 / "item_soap.png", "towel": L4 / "item_towel.png", "heart": ROOT / "long16-sharing/art/item_heart.png",
            "sunny": L1 / "fruit_sunny.png", "plate": ROOT / "long16-sharing/art/item_plate.png", "car": ROOT / "long16-sharing/art/item_car.png",
            "bathtub": L4 / "item_bathtub.png", "moon": L4 / "item_moon.png", "puppy": L1 / "fruit_puppy.png", "kitten": L1 / "fruit_kitten.png",
            "duckling": L1 / "fruit_duckling.png", "elephant": L1 / "fruit_elephant.png", "clock": L4 / "item_clock.png", "ball": L4 / "item_ball.png"})
PLACES = {"bedroom": L4 / "bg_bedroom.png", "hall": L4 / "bg_hall.png", "park": ROOT / "long05-body-parts/art/bg_park.png",
          "kitchen": ROOT / "long03-fruits-veg/art/bg_kitchen.png"}
BGS = {"bathroom2": A15 / "bg_bathroom2.png"}
STEP_WORD = {"tell": "TELL A GROWN-UP!", "walk": "GO TO THE BATHROOM", "pants": "PANTS DOWN", "sit": "SIT ON THE POTTY", "go": "PEE OR POOP",
             "wipe": "WIPE", "up": "PANTS UP", "flush": "FLUSH!", "wash": "WASH HANDS", "dry": "DRY HANDS"}


def on_potty(frame, n, t, emo, cx, scale=0.42):
    """kid sitting: body drawn lower, the potty covers the legs"""
    body(frame, n, t, emo, cx, feet=1075 + 2000 * scale * 0.2, scale=scale)
    item(frame, "potty", cx, 1000, 2000 * scale * 0.28)


def scene_intro(frame, s, t):
    if t < s["title_t"]:
        q = t - s["wiggle_t"]
        body(frame, "gul", t, "scared", 960 + 30 * math.sin(q * 14), scale=0.6, rot=8 * math.sin(q * 10), hop=20 * abs(math.sin(q * 8)))
        word(frame, "I NEED TO GO!", t, s["wiggle_t"] + 0.2, size=150, col=(255, 107, 139))
    else:
        k = t - s["title_t"]
        item(frame, "potty", 960, 820, 380 * ease_back(k / 0.4))
        for n, x in (("gul", 560), ("misheal", 1360)):
            body(frame, n, t, "excited" if t < s["kids_t"] else None, x, scale=0.46, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
        rt(frame, 960, 180, "POTTY TIME!", int(220 * ease_back(k / 0.35)), maxw=1500)
        if k < 0.3:
            frame.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - k / 0.3)))))


def scene_meet(frame, s, t):
    q = t - s["t0"]
    badge(frame, 160, 90, f"{s['num']}/8")
    for i, k in enumerate(s["done"]):
        item(frame, k, 560 + i * 130, 230, 110)
    item(frame, s["key"], 960, 580 + 8 * math.sin(t * 2.5), 400 * ease_back(q / 0.4))
    word(frame, {"undies": "UNDERWEAR!", "paper": "TOILET PAPER!", "stool": "STEP STOOL!", "chart": "STICKER CHART!"}.get(s["key"], s["key"].upper() + "!"),
         t, s["say_t"], y=880, size=110)
    side_kids(frame, t, xs=(170, 1750))


def scene_sign(frame, s, t):
    key = s["key"]
    q = t - s["t0"]
    if key == "wiggle":
        body(frame, "gul", t, "scared", 960 + 25 * math.sin(q * 14), scale=0.6, rot=8 * math.sin(q * 10))
    elif key == "hold":
        body(frame, "gul", t, "shy", 960, scale=0.6, rot=3 * math.sin(q * 6))
    elif key == "stop":
        item(frame, "teddy", 1300, 860, 220, rot=20)
        body(frame, "gul", t, "surprised", 900, scale=0.6)
    else:
        body(frame, "gul", t, None, 760, scale=0.55, wave=True)
        body(frame, "misheal", t, "happy", 1180, scale=0.55)
    word(frame, {"wiggle": "WIGGLE, WIGGLE!", "hold": "HOLD YOUR TUMMY", "stop": "STOP PLAYING", "tell": "TELL A GROWN-UP!"}[key], t, s["t0"], size=120,
         col=(255, 107, 139))


def scene_step(frame, s, t):
    key, n = s["key"], s["who"]
    q = t - s["t0"]
    badge(frame, 160, 90, f"STEP {s['num']}", (46, 168, 255))
    item(frame, "toilet", 1450, 760, 380)
    if key in ("tell",):
        body(frame, n, t, None, 760, scale=0.5, wave=True)
        body(frame, "misheal" if n == "gul" else "gul", t, "happy", 1150, scale=0.5)
    elif key == "walk":
        body(frame, n, t, "happy", 400 + 400 * ease_io(min(1, q / 2)), scale=0.5, hop=15 * abs(math.sin(q * 8)))
    elif key in ("pants", "up"):
        body(frame, n, t, "happy", 800, scale=0.5)
    elif key in ("sit", "go", "wipe"):
        on_potty(frame, n, t, "calm" if key == "go" else "happy", 800)
        if key == "wipe":
            item(frame, "paper", 1050, 760, 160)
        if key == "go":
            stars_ring(frame, 800, 700, 260, 160, t * 0.5, n=6, r=16)
    elif key == "flush":
        body(frame, n, t, "excited", 900, scale=0.5, wave=True)
        d = ImageDraw.Draw(frame, "RGBA")
        for j in range(4):
            a0 = (t * 500 + j * 90) % 360
            d.arc((1360, 680, 1540, 760), a0, a0 + 90, fill=(60, 140, 210, 255), width=8)
    elif key in ("wash", "dry"):
        body(frame, n, t, "happy", 800, scale=0.5)
        item(frame, "soap" if key == "wash" else "towel", 1100, 640 + 10 * math.sin(t * 6), 200, rot=10 * math.sin(t * 6))
    word(frame, STEP_WORD[key], t, s["t0"], size=110, col=(46, 168, 255))


def scene_celebrate(frame, s, t):
    body(frame, "gul", t, "proud", 960, scale=0.6, hop=40 * abs(math.sin(t * 5)), wave=True)
    confetti(frame, t, s["t_t"])
    word(frame, "HOORAY! GUL DID IT!", t, s["t_t"], size=130)


def scene_wash(frame, s, t):
    n = 0
    for i, x in enumerate(s["ts"]):
        if t >= x:
            n = i + 1
    body(frame, "misheal", t, "happy", 560, scale=0.5)
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((820, 620, 1300, 720), radius=30, fill=(255, 255, 255), outline=INK, width=6)
    if t >= s["water_t"]:
        for j in range(5):
            x = 1040 + (j - 2) * 8
            d.line((x, 420, x + 4 * math.sin(t * 20 + j), 640), fill=(120, 200, 245, 200), width=8)
    item(frame, "soap", 1060 + 60 * math.cos(t * 6), 560 + 30 * math.sin(t * 6), 140)
    for j in range(8):
        x, y = 940 + (j * 53) % 260, 470 + (j * 37) % 120 - 10 * math.sin(t * 3 + j)
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(225, 245, 255, 150), outline=(150, 200, 235, 220), width=3)
    if n:
        rt(frame, 1560, 520, str(n), 220, colour=RAINBOW[n % 6])
    word(frame, "COUNT TO 20!", t, s["t0"], size=120, col=(46, 168, 255))


def scene_oops(frame, s, t):
    happy = t >= s["happy_t"]
    body(frame, "gul", t, "happy" if happy else ("sad" if t < s["ok_t"] + 1 else "calm"), 760, scale=0.55)
    body(frame, "misheal", t, "happy", 1200, scale=0.55, wave=t >= s["ok_t"])
    if t >= s["ok_t"]:
        item(frame, "heart", 980, 420 - 15 * abs(math.sin(t * 3)), 200)
        word(frame, "IT'S OKAY! TRY AGAIN!", t, s["ok_t"], size=110, col=(255, 107, 139))
    else:
        word(frame, "OOPS!", t, s["sad_t"], size=150)


def scene_teddy(frame, s, t):
    item(frame, "potty", 960, 900, 300)
    if t >= s["l2"]:
        item(frame, "teddy", 960, 760, 260)
    else:
        item(frame, "teddy", 960 + 20 * math.sin(t * 12), 760, 260, rot=8 * math.sin(t * 10))
    side_kids(frame, t, "happy", xs=(400, 1520), scale=0.4)
    if t >= s["yay_t"]:
        confetti(frame, t, s["yay_t"])
        word(frame, "GOOD JOB, TEDDY!", t, s["yay_t"], size=120)
    else:
        word(frame, "TEDDY'S TURN!", t, s["t0"], size=120)


def scene_chart(frame, s, t):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((560, 230, 1360, 830), radius=30, fill=(255, 255, 255), outline=INK, width=8)
    for i, day in enumerate(("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")):
        x = 640 + i * 108
        rt(frame, x, 300, day, 40, colour=RAINBOW[i % 6])
        d.rounded_rectangle((x - 45, 360, x + 45, 450), radius=14, fill=(242, 244, 248), outline=INK, width=4)
        if i < len(s["ts"]) and t >= s["ts"][i]:
            item(frame, "star", x, 405, 80 * ease_back((t - s["ts"][i]) / 0.3) + 1)
    n = sum(1 for x in s["ts"] if t >= x)
    if n:
        rt(frame, 960, 640, f"{n} STARS!", 120, colour=(255, 200, 40))
    side_kids(frame, t, "excited", xs=(250, 1670), scale=0.36)


def scene_undies(frame, s, t):
    k = min(1, (t - s["in_t"]) / 0.8)
    item(frame, "undies", 960, 300 + 200 * (1 - ease_back(k)), 300)
    body(frame, "gul", t, "proud", 700, scale=0.5, hop=30 * abs(math.sin(t * 5)) if t >= s["yay_t"] else 0, wave=t >= s["yay_t"])
    body(frame, "misheal", t, "excited", 1220, scale=0.5, hop=30 * abs(math.sin(t * 5 + 1)) if t >= s["yay_t"] else 0, wave=True)
    if t >= s["yay_t"]:
        confetti(frame, t, s["yay_t"])
        word(frame, "BIG KIDS!", t, s["yay_t"], size=150)
    else:
        word(frame, "BIG KID UNDERWEAR!", t, s["in_t"], size=110)


def scene_yesno(frame, s, t):
    rt(frame, 960, 150, s["q"], int(72 * ease_back((t - s["t0"]) / 0.35)), maxw=1600)
    pic = {"wash": "soap", "play": "paper", "tell": "heart", "wait": "teddy", "flush": "toilet", "toys": "teddy", "stool": "stool",
           "rush": "undies", "try": "moon", "scared": "heart", "lid": "toilet", "climb": "stool", "relax": "potty", "hide": "heart"}[s["key"]]
    item(frame, pic, 960, 520, 320)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.3)
        d = ImageDraw.Draw(frame)
        if s["good"]:
            d.line((800, 520, 920, 640, 1140, 380), fill=(59, 193, 74), width=int(40 * k) + 1, joint="curve")
            word(frame, "YES!", t, s["answer_t"], y=840, size=160, col=(59, 193, 74))
        else:
            r = 230 * k
            d.ellipse((960 - r, 520 - r, 960 + r, 520 + r), outline=(232, 53, 46), width=24)
            d.line((960 - r * 0.7, 520 + r * 0.7, 960 + r * 0.7, 520 - r * 0.7), fill=(232, 53, 46), width=24)
            word(frame, "NO!", t, s["answer_t"], y=840, size=160, col=(232, 53, 46))
    side_kids(frame, t, xs=(170, 1750))


def scene_outro(frame, s, t):
    for i, k in enumerate(("potty", "star", "soap", "undies", "chart", "teddy")):
        item(frame, k, (i * 330 + t * 120) % 2200 - 140, 980 - 20 * abs(math.sin(t * 4 + i)), 150)
    for n, x in (("gul", 700), ("misheal", 1220)):
        body(frame, n, t, "happy" if t >= s["bye_t"] else None, x, scale=0.5, feet=900, hop=30 * abs(math.sin(t * 4 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 140, "BYE BYE, POTTY STARS!", int(130 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 140, "TELL, SIT, FLUSH, WASH!", int(110 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


def scene_thisway(frame, s, t):
    i = max([j for j, x in enumerate(s["l"]) if t >= x] or [0])
    if i < 2:
        on_potty(frame, "gul", t, "happy", 800)
    elif i < 4:
        body(frame, "gul", t, "excited", 800, scale=0.5, wave=True)
        item(frame, "toilet", 1200, 760, 360)
    else:
        body(frame, "gul", t, "happy", 800, scale=0.5)
        item(frame, "soap", 1100, 620 + 10 * math.sin(t * 6), 200, rot=10 * math.sin(t * 6))
    body(frame, "misheal", t, "happy", 1550, scale=0.45, hop=15 * abs(math.sin(t * 4)), wave=True)
    word(frame, "THIS IS THE WAY!", t, s["t0"], size=120)


def scene_when(frame, s, t):
    badge(frame, 160, 90, f"{s['num']}/7", (46, 168, 255))
    item(frame, s["key"], 760, 560 + 8 * math.sin(t * 2.5), 340 * ease_back((t - s["t0"]) / 0.4))
    item(frame, "potty", 1250, 760, 300)
    rt(frame, 1000, 560, "+", 120, colour=(255, 255, 255))
    lab = {"sunny": "WAKE UP!", "plate": "AFTER LUNCH!", "car": "BEFORE THE CAR!", "bathtub": "BEFORE BATH!", "moon": "BEFORE BED!",
           "clock": "AFTER YOUR NAP!", "ball": "BEFORE PLAYTIME!"}[s["key"]]
    word(frame, lab, t, s["say_t"], size=130, col=(46, 168, 255))
    side_kids(frame, t, xs=(170, 1750))


def scene_where(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    if s["place"] not in G.get("places", {}):
        G.setdefault("places", {})[s["place"]] = Image.open(PLACES[s["place"]]).convert("RGBA").resize((960, 540))
    im = G["places"][s["place"]].resize((max(2, int(960 * k)), max(2, int(540 * k))))
    frame.alpha_composite(im, (int(960 - im.width / 2), int(520 - im.height / 2)))
    ImageDraw.Draw(frame).rounded_rectangle((960 - im.width / 2, 520 - im.height / 2, 960 + im.width / 2, 520 + im.height / 2), radius=20, outline=INK, width=8)
    item(frame, "toilet", 1360, 700, 240)
    lab = {"bedroom": "AT HOME!", "hall": "AT SCHOOL!", "park": "AT THE PARK!", "kitchen": "AT GRANDMA'S!"}[s["place"]]
    word(frame, lab, t, s["say_t"], y=900, size=120)
    side_kids(frame, t, xs=(170, 1750))


def scene_animal(frame, s, t):
    key = s["key"]
    k = ease_back((t - s["t0"]) / 0.4)
    if key == "potty":
        on_potty(frame, "gul", t, "proud", 960, scale=0.5)
        confetti(frame, t, s["t0"])
        word(frame, "AND YOU!", t, s["say_t"], size=150)
        return
    item(frame, key, 960, 600 + 10 * math.sin(t * 3), 420 * k)
    d = ImageDraw.Draw(frame)
    if key == "puppy":
        d.ellipse((560, 760, 1360, 900), fill=(93, 187, 70))
    elif key == "kitten":
        d.rounded_rectangle((680, 760, 1240, 880), radius=20, fill=(120, 190, 240), outline=INK, width=6)
    elif key == "duckling":
        d.ellipse((560, 760, 1360, 900), fill=(110, 195, 245))
    word(frame, {"puppy": "ON THE GRASS!", "kitten": "LITTER BOX!", "duckling": "IN THE POND!", "elephant": "GIANT POTTY!"}[key], t, s["say_t"], size=120)
    side_kids(frame, t, "happy", xs=(170, 1750))


def scene_pword(frame, s, t):
    key = s["key"]
    k = ease_back((t - s["t0"]) / 0.4)
    if key in ("pee", "poop"):
        on_potty(frame, "gul", t, "calm", 760, scale=0.42)
    elif key == "flushw":
        item(frame, "toilet", 760, 600, 380 * k)
    else:
        item(frame, key, 760, 600 + 8 * math.sin(t * 2.5), 380 * k)
    rt(frame, 1300, 560, s["w"] + "!", int(150 * k), colour=RAINBOW[len(s["w"]) % 6], maxw=700)
    side_kids(frame, t, xs=(170, 1750))
    word(frame, "POTTY WORDS!", t, s["t0"], size=110)


def scene_dryer(frame, s, t):
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((900, 300, 1140, 520), radius=30, fill=(220, 225, 235), outline=INK, width=8)
    d.rectangle((960, 500, 1080, 540), fill=(160, 165, 180), outline=INK, width=5)
    on = s["whoosh_t"] <= t < s["whoosh_t"] + 1.6
    if on:
        for j in range(6):
            p = (t * 3 + j / 6) % 1
            d.line((960 + j * 24, 545 + p * 160, 970 + j * 24, 575 + p * 160), fill=(150, 200, 255, int(220 * (1 - p))), width=6)
    scared = s["scared_t"] <= t < s["ok_t"] + 0.8
    body(frame, "misheal", t, "scared" if scared else "happy", 640, scale=0.5, hop=8 * abs(math.sin(t * 20)) if scared else 0)
    body(frame, "gul", t, "happy", 1400, scale=0.5, wave=t >= s["ok_t"])
    if t >= s["ok_t"]:
        word(frame, "IT'S JUST LOUD!", t, s["ok_t"], size=120, col=(46, 168, 255))
    elif on or scared:
        word(frame, "WHOOSH!", t, s["whoosh_t"], size=160)
    else:
        word(frame, "HAND DRYER", t, s["t0"], size=120)


def scene_mishu1(frame, s, t):
    if t < s["sit_t"]:
        body(frame, "misheal", t, "scared", 960 + 25 * math.sin(t * 14), scale=0.55, rot=6 * math.sin(t * 10))
        word(frame, "I NEED TO GO!", t, s["l1"], size=130, col=(255, 107, 139))
    elif t < s["done_t"]:
        on_potty(frame, "misheal", t, "calm", 960, scale=0.48)
        word(frame, "WAIT AND RELAX...", t, s["sit_t"], size=110)
    else:
        body(frame, "misheal", t, "proud", 760, scale=0.5, hop=40 * abs(math.sin(t * 5)), wave=True)
        body(frame, "gul", t, "excited", 1200, scale=0.5, hop=40 * abs(math.sin(t * 5 + 1)), wave=True)
        confetti(frame, t, s["done_t"])
        word(frame, "MISHU DID IT!", t, s["done_t"], size=140)


SCENES = {"intro": scene_intro, "meet": scene_meet, "sign": scene_sign, "step": scene_step, "celebrate": scene_celebrate, "wash": scene_wash,
          "oops": scene_oops, "teddy": scene_teddy, "chart": scene_chart, "undies": scene_undies, "yesno": scene_yesno, "outro": scene_outro, "thisway": scene_thisway, "when": scene_when, "where": scene_where, "animal": scene_animal, "pword": scene_pword, "dryer": scene_dryer, "mishu1": scene_mishu1,
          "dance": lambda f, s, t: K.scene_dance(f, s, t, pics={"sit": "potty", "spin": "toilet", "shake": "soap", "jump": "star"})}
K.configure(__file__, {"gul": "tee", "misheal": "pink"}, ART, BGS, SCENES, "L15 Potty Training", "Potty Training for Toddlers")
K.CFG["title_items"] = ["potty", "star", "soap", "undies", "teddy"]

if __name__ == "__main__":
    K.main()
