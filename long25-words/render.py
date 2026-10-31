"""Animate L25 "First Words for Toddlers".  python render.py frames auto | video"""
import math, sys, pathlib
from PIL import ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import longkit as K
from longkit import item, body, word, rt, ease_back, side_kids, stars_ring, confetti, badge, card, choice_row, INK, RAINBOW

A25, L1, L4, L5, E1 = HERE / "art", ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art", ROOT / "long05-body-parts/art", ROOT / "ep01-fruits/art"
ART = {k: A25 / f"item_{k}.png" for k in ("cupkid", "baby", "mama", "papa", "bottle", "spoonfood")}
ART.update({"dog": L1 / "fruit_puppy.png", "cat": L1 / "fruit_kitten.png", "duck": ROOT / "long11-bath/art/item_duck.png", "bird": ROOT / "long09-eggs/art/item_robin.png",
            "fish": L1 / "fruit_fish.png", "pig": L1 / "fruit_piglet.png", "water": L4 / "item_water.png", "apple": E1 / "fruit_apple.png", "banana": E1 / "fruit_banana.png",
            "egg": L4 / "item_egg.png", "toast": L4 / "item_toast.png", "ball": L4 / "item_ball.png", "car": ROOT / "long16-sharing/art/item_car.png", "book": L4 / "item_book.png",
            "shoes": L4 / "item_shoes.png", "hat": ROOT / "long08-colors-shapes/art/item_tophat.png", "bed": L4 / "item_bed_neat.png", "teddy": L4 / "item_teddy.png",
            "nose": L5 / "item_nose.png", "eye": L5 / "item_eye.png", "mouth": L5 / "item_mouth.png", "ear": L5 / "item_ear.png", "hand": L5 / "item_hand.png",
            "moon": L4 / "item_moon.png", "star": ROOT / "long15-potty/art/item_star.png", "socks": L4 / "item_socks.png", "spoon": ROOT / "long11-bath/art/item_spoon.png", "sun": L1 / "fruit_sunny.png", "tree": ROOT / "long17-xmastree/art/item_tree.png", "flower": L5 / "item_flower.png", "bus": L1 / "fruit_bus.png"})
BGS = {"bedroom": L4 / "bg_bedroom.png", "farm": L1 / "bg_farm.png", "kitchen": ROOT / "long03-fruits-veg/art/bg_kitchen.png", "park": L5 / "bg_park.png",
       "playroom2": ROOT / "long08-colors-shapes/art/bg_studio.png"}


def scene_intro(frame, s, t):
    for j, k in enumerate(("ball", "dog", "apple", "car", "duck", "book")):
        a = j * 1.05 + t * 0.4
        item(frame, k, 960 + 560 * math.cos(a), 560 + 280 * math.sin(a), 200)
    if t >= s["title_t"]:
        side_kids(frame, t, "excited" if t < s["kids_t"] else None, xs=(170, 1750), scale=0.36)
        rt(frame, 960, 150, "FIRST WORDS!", int(170 * ease_back((t - s["title_t"]) / 0.35)), maxw=1600)


def scene_hello(frame, s, t):
    body(frame, "misheal", t, "happy", 960, scale=0.62, wave=True, hop=10 * abs(math.sin(t * 3)))
    word(frame, "HI!", t, s["t0"], size=190)


def scene_word(frame, s, t):
    k = ease_back((t - s["t0"]) / 0.4)
    card(frame, 960, 480, 720, 660)
    item(frame, s["key"], 960, 480 + 8 * math.sin(t * 2), 540 * k)
    rt(frame, 960, 80, s["w"], int(120 * ease_back((t - s["say_t"]) / 0.3)), colour=(255, 77, 109), maxw=1000)
    if t >= s["line_t"]:
        stars_ring(frame, 960, 480, 420, 390, t, n=8, r=18)
    side_kids(frame, t, "happy", xs=(240, 1680), scale=0.36)


def scene_sound(frame, s, t):
    card(frame, 960, 520, 680, 620)
    item(frame, s["key"], 960, 520 - (20 * abs(math.sin(t * 6)) if t >= s["answer_t"] else 0), 500)
    if t >= s["answer_t"]:
        word(frame, s["ans"], t, s["answer_t"], y=100, size=120, col=(255, 77, 109))
    else:
        word(frame, "WHAT DOES IT SAY?", t, s["t0"], y=100, size=90)
    side_kids(frame, t, xs=(240, 1680), scale=0.34)


def scene_peek(frame, s, t):
    d = ImageDraw.Draw(frame)
    k = min(1, max(0, (t - s["boo_t"]) / 0.4))
    item(frame, s["key"], 960, 540, 540)
    w = 560 * (1 - k)
    if w > 2:
        d.rectangle((960 - 40 - w, 200, 960, 880), fill=(255, 150, 190), outline=INK, width=6)
        d.rectangle((960, 200, 960 + 40 + w, 880), fill=(255, 150, 190), outline=INK, width=6)
    d.rounded_rectangle((340, 170, 1580, 210), radius=16, fill=(170, 110, 60), outline=INK, width=5)
    if k > 0:
        word(frame, "PEEKABOO!", t, s["boo_t"], y=100, size=120, col=(255, 77, 109))
    side_kids(frame, t, "excited" if k else None, xs=(200, 1720), scale=0.32)


def scene_action(frame, s, t):
    act = s["key"]
    q = t - s["t0"]
    n, hop, emo, wave, rot = "gul", 0, "happy", False, 0
    if act in ("up", "jump"):
        hop = 130 * abs(math.sin(q * 2.6))
    elif act == "down":
        hop = 120 * (1 - min(1, (q % 2) / 1.5))
    elif act == "go":
        hop = 40 * abs(math.sin(q * 8))
    elif act in ("sleep",):
        emo = "tired"
    elif act in ("wave", "yes"):
        wave = True
    elif act == "no":
        rot = 7 * math.sin(q * 7)
    elif act == "done":
        emo = "proud"
    x = 960
    if act == "go":
        x = 300 + (q * 200) % 1000
    body(frame, n, t, emo, x, scale=0.62, hop=hop, wave=wave, rot=rot)
    body(frame, "misheal", t, "happy", 1640, scale=0.32)
    if act == "stop":
        d = ImageDraw.Draw(frame)
        pts = [(350 + 170 * math.cos(math.pi / 8 + i * math.pi / 4), 540 + 170 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
        d.polygon(pts, fill=(232, 53, 46), outline=(255, 255, 255), width=12)
        rt(frame, 350, 540, "STOP", 80, colour=(255, 255, 255))
    elif act == "eat":
        item(frame, "spoonfood", 400, 620, 340)
    elif act == "more":
        for j in range(3):
            item(frame, "banana", 330 + j * 90, 600 - (j % 2) * 60, 170)
    elif act == "clap":
        rt(frame, 400, 520, "CLAP!", 90, colour=(255, 140, 26))
    elif act == "sleep":
        item(frame, "bed", 380, 720, 420)
    word(frame, s["w"] + "!", t, s["say_t"], y=110, size=150, col=(255, 77, 109))


def scene_where(frame, s, t):
    choice_row(frame, t, s["keys"], s["good"], s["answer_t"], y=580, size=300)
    word(frame, "WHERE IS THE " + s["w"] + "?" if s["w"] != "SHOES" else "WHERE ARE THE SHOES?", t, s["t0"], size=100)


def scene_phrase(frame, s, t):
    card(frame, 960, 500, 640, 600)
    item(frame, s["key"], 960, 500, 460)
    word(frame, s["w"] + "!", t, s["say_t"], y=95, size=120, col=(255, 77, 109), maxw=1500)
    side_kids(frame, t, "happy", xs=(240, 1680), scale=0.34)


def scene_outro(frame, s, t):
    for n, x in (("gul", 600), ("misheal", 1320)):
        body(frame, n, t, "happy", x, scale=0.5, hop=30 * abs(math.sin(t * 3 + (0 if n == "gul" else 1))), wave=True)
    if t >= s["bye_t"]:
        confetti(frame, t, s["bye_t"])
        rt(frame, 960, 130, "BYE BYE!", int(180 * ease_back((t - s["bye_t"]) / 0.35)), maxw=1700)
    else:
        rt(frame, 960, 130, "GREAT TALKING!", int(150 * ease_back((t - s["t0"]) / 0.35)), maxw=1700)


SCENES = {"intro": scene_intro, "hello": scene_hello, "word": scene_word, "sound": scene_sound, "peek": scene_peek, "action": scene_action, "where": scene_where,
          "phrase": scene_phrase, "outro": scene_outro}
K.configure(__file__, {"gul": "bluetee", "misheal": "pink"}, ART, BGS, SCENES, "L25 First Words", "First Words for Toddlers")
K.CFG["title_items"] = ["ball", "dog", "apple", "car", "book"]

if __name__ == "__main__":
    K.main()
