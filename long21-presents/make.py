"""Long video 21: "Christmas Presents: Surprise Toys". python make.py
Music hook: Deck the Halls (traditional Welsh, public domain) played with our own code instruments."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
COLOURS = [  # colour, toy key, toy word, clue, fact
    ("red", "firetruck", "fire truck", "It goes nee naw, nee naw!", "A red fire truck! It helps put out fires!"),
    ("orange", "basketball", "basketball", "It's round, and it bounces!", "An orange basketball! Bounce, bounce!"),
    ("yellow", "duck", "rubber duck", "It floats in the bath! Quack!", "A yellow duck! Quack, quack!"),
    ("green", "frog", "toy frog", "It jumps, and says ribbit!", "A green frog! Ribbit, ribbit!"),
    ("blue", "car", "toy car", "It has four wheels! Vroom!", "A blue car! Vroom, vroom!"),
    ("purple", "rocket", "toy rocket", "It zooms up to the moon!", "A purple rocket! Three, two, one, blast off!"),
    ("pink", "piglet", "toy pig", "It says oink, oink!", "A pink pig! Oink, oink!"),
    ("brown", "teddy", "teddy bear", "It's soft and cuddly!", "A brown teddy bear! Big hug!"),
    ("white", "snowman", "toy snowman", "It has a carrot nose!", "A white snowman! Brrr!"),
    ("grey", "robot", "robot", "It goes beep, boop, beep!", "A grey robot! Beep, boop!")]
SIZES = [("big", "Which present is the biggest?", "This one! The big one!"), ("small", "Which present is the smallest?", "This tiny one!"),
         ("mid", "Which one is in the middle?", "The medium one!")]
FAMILY = [("Grandma", "book", "Grandma loves to read! A book for Grandma!"), ("Papa", "tie", "A blue tie for Papa! So smart!"),
          ("Mama", "flower", "Mama loves flowers! A pretty flower!"), ("Baby", "duck", "A little duck for the baby! Quack!")]
PETS = [("puppy", "bone", "What present for the puppy?", "A bone! Woof, woof!"), ("kitten", "fish", "What present for the kitten?", "A fish! Meow!"),
        ("bunny", "carrot", "What present for the bunny?", "A crunchy carrot!"), ("monkey", "banana", "What present for the monkey?", "A yummy banana!")]
PARCEL = ["Unwrap layer one! Rip, rip!", "Layer two! More paper!", "Layer three! Keep going!", "Layer four! Almost there!", "Layer five! Last one!"]
SHAPES = [("ball", "circle", "A ball is round. It fits in the round box!"), ("blocks", "square", "Blocks go in the square box!"),
          ("kite", "diamond", "The kite goes in the diamond box!"), ("drum", "circle", "The drum is round too! Round box!")]
HEAVY = [("basketball", "balloons", "Which is heavy, and which is light?", "The basketball is heavy! The balloons are light!"),
         ("robot", "kite", "Which is heavy?", "The robot is heavy! The kite is light!")]
SOUNDS = [("drumsnd", "drum", "Boom, boom! A drum!"), ("xylo", "xylophone", "Ding, ding, ding! A xylophone!"),
          ("beep", "robot", "Beep, boop! A robot!"), ("quack", "duck", "Quack, quack! A duck!")]
MAKE = [("card", "Fold some paper, and draw a big heart!"), ("crayons", "Colour it with crayons!"), ("paperchain", "Make a paper chain! Loop, loop, loop!"),
        ("heart", "Write, I love you! Gifts we make are the best gifts!")]
MANNERS = [("Say thank you, when you get a present!", "THANK YOU!"), ("Smile, even if it's not what you wanted!", "SMILE!"),
           ("Give the person a big hug!", "BIG HUG!"), ("Share your new toy with a friend!", "SHARE!")]
GIVING = ["Giving makes other people happy!", "And it makes us happy too!", "Who will you give a present to?"]
STACK = list(range(1, 11))
BOWS = [("red", 3), ("gold", 5), ("blue", 4)]
ODD = [(["present1", "present1", "bell", "present1"], 2, "The bell! It's not a present!"), (["teddy", "car", "ball", "banana"], 3, "The banana! It's not a toy!"),
       (["duck", "frog", "piglet", "present2"], 3, "The present! It's not an animal!")]
GONE = [(["teddy", "car", "duck", "drum"], 2, "The duck is gone!"), (["rocket", "ball", "frog", "kite"], 0, "The rocket is gone!"),
        (["robot", "piglet", "firetruck", "blocks"], 3, "The blocks are gone!"),
        (["basketball", "teddy", "kite", "snowman"], 1, "The teddy bear is gone!")]
MORE = [(3, 5, "mishu", "Mishu has more! Five is more than three!"), (6, 2, "gul", "Gul has more! Six is more than two!"),
        (4, 4, "same", "The same! Four and four!")]
AV = [("duck", "ANIMAL", "An animal!"), ("car", "VEHICLE", "A vehicle!"), ("frog", "ANIMAL", "An animal!"), ("firetruck", "VEHICLE", "A vehicle!"),
      ("piglet", "ANIMAL", "An animal!"), ("rocket", "VEHICLE", "A vehicle!")]
DANCE = [("Shake the present!", "shake"), ("Rip the paper!", "wiggle"), ("Bounce the ball!", "jump"), ("Spin the top!", "spin"),
         ("March like a toy soldier!", "march"), ("Merry Christmas! Hooray!", "jump")]
QUIZ = [("What colour was the fire truck?", "Red!", "firetruck"), ("What do we say when we get a present?", "Thank you!", "card"),
        ("What present did the puppy get?", "A bone!", "bone"), ("How many presents in the tower?", "Ten!", "present2")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: a pile of presents shakes
    sc = T.scene("intro", "xmasroom")
    sc["shake_t"] = T.mark("shake")
    T.pause(1.0)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Christmas presents!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "So many surprises under the tree!", gap=0.2)
    T.say("gul", "Let's open them, and see what's inside!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ COLOUR SURPRISES
    T.title("xmasroom", "COLOUR SURPRISES!", "gul", "Ten colour presents! Guess the toy, and say the colour!")
    for k, (col, key, w, clue, fact) in enumerate(COLOURS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("surprise", "xmasroom", col=col, key=key, w=w.upper(), num=k + 1)
        sc["shake_t"] = T.mark("shake")
        T.say(a, f"The {col} present! {clue}", gap=0.1)
        T.prompt(a, "What's inside?", wait=1.7)
        sc["open_t"] = T.mark("tada")
        T.say(other(a), fact, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.0, 3)))
        T.pause(1.0)
        T.end(sc)
    sc = T.scene("allten", "xmasroom")
    sc["ts"] = []
    for k, (col, *_) in enumerate(COLOURS):
        sc["ts"].append(T.mark("pop"))
        T.say("both", f"{col.capitalize()}!", gap=0.12)
    sc["sum_t"] = T.say("gul", "Ten colours! Ten toys! Wow!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ PASS THE PARCEL
    T.title("xmasroom", "PASS THE PARCEL!", "mishu", "One present, with five layers of paper! What's in the middle?")
    sc = T.scene("parcel", "xmasroom")
    sc["ts"] = []
    for k, text in enumerate(PARCEL):
        sc["ts"].append(T.mark("rip"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
    sc["open_t"] = T.mark("tada")
    T.say("both", "Boing! A jack in the box! Ha ha!", gap=0.6)
    T.end(sc)
    # ------------------------------------------------------------ BIG MEDIUM SMALL
    T.title("xmasroom", "BIG AND SMALL!", "gul", "Big, medium, small! Look at the presents!")
    for k, (ans, q, a_text) in enumerate(SIZES):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("size", "xmasroom", ans=ans)
        T.prompt(a, q, wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), a_text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ PRESENT TOWER
    T.title("xmasroom", "PRESENT TOWER!", "mishu", "Let's build a tall present tower! Count with us!")
    sc = T.scene("tower", "xmasroom")
    sc["ts"] = []
    for i in STACK:
        sc["ts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.14)
    sc["fall_t"] = T.mark("crash")
    T.say("gul", "Oh no! The tower fell down! Ha ha!", gap=0.3)
    T.say("mishu", "Ten presents! Let's build it again!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ WHO IS IT FOR
    T.title("xmasroom", "WHO IS IT FOR?", "gul", "Presents for the whole family! Who is it for?")
    for k, (who, key, text) in enumerate(FAMILY):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("family", "xmasroom", who=who, key=key)
        T.mark("pop")
        T.prompt(a, f"This tag says {who}!", wait=1.2)
        sc["open_t"] = T.mark("tada")
        T.say(other(a), text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ PRESENTS FOR PETS
    T.title("northpole", "PRESENTS FOR PETS!", "mishu", "Animals want presents too! What does each animal like?")
    for k, (pet, key, q, ans) in enumerate(PETS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("pet", "northpole", pet=pet, key=key)
        T.prompt(a, q, wait=2.0)
        sc["open_t"] = T.mark("tada")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ BOX SHAPES
    T.title("xmasroom", "WHICH BOX FITS?", "gul", "Toys need the right box! Which box fits?")
    for k, (key, shp, text) in enumerate(SHAPES):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("boxfit", "xmasroom", key=key, shp=shp)
        T.prompt(a, "Which box fits?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ HEAVY OR LIGHT
    T.title("xmasroom", "HEAVY OR LIGHT?", "mishu", "Some presents are heavy, and some are light!")
    for k, (h, l, q, ans) in enumerate(HEAVY):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("heavy", "xmasroom", h=h, l=l)
        T.prompt(a, q, wait=1.8)
        sc["answer_t"] = T.mark("boing")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ COUNT THE BOWS
    T.title("xmasroom", "COUNT THE BOWS!", "gul", "Every present needs a bow! Let's count them!")
    for k, (col, n) in enumerate(BOWS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("bows", "xmasroom", col=col, n=n)
        T.say(a, f"How many {col} bows?", gap=0.1)
        sc["cts"] = []
        for i in range(1, n + 1):
            sc["cts"].append(T.mark("pop"))
            T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
        sc["sum_t"] = T.say(other(a), f"{NUM[n].capitalize()} {col} bows!", gap=0.5)
        T.stars.append(sc["sum_t"])
        T.end(sc)
    # ------------------------------------------------------------ WHICH TOY IS GONE
    T.title("xmasroom", "WHICH TOY IS GONE?", "gul", "Look at the toys! Now close your eyes! Which toy is gone?")
    for k, (keys, gone, text) in enumerate(GONE):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("gone", "xmasroom", keys=keys, gone=gone)
        T.say(a, "Look carefully!", gap=1.0)
        sc["close_t"] = T.mark("whoosh")
        T.say(a, "Close your eyes!", gap=0.8)
        sc["open_t"] = T.mark("whoosh")
        T.prompt(a, "Which toy is gone?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WHO HAS MORE
    T.title("xmasroom", "WHO HAS MORE?", "mishu", "Gul and Mishu are counting presents! Who has more?")
    for k, (g, m, ans, text) in enumerate(MORE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("more", "xmasroom", g=g, m=m, ans=ans)
        T.prompt(a, "Who has more?", wait=2.2)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ ANIMAL OR VEHICLE
    T.title("xmasroom", "TIDY UP THE TOYS!", "gul", "Time to tidy up! Animal, or vehicle?")
    for k, (key, ans, text) in enumerate(AV):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("tidy", "xmasroom", key=key, ans=ans)
        T.prompt(a, "Animal, or vehicle?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ TOY SOUNDS
    T.title("xmasroom", "WHAT'S THAT SOUND?", "mishu", "Listen! Which toy makes this sound?")
    for k, (snd, key, ans) in enumerate(SOUNDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sound", "xmasroom", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.5)
        T.prompt(a, "Which toy is it?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ ODD ONE OUT
    T.title("xmasroom", "WHICH ONE IS DIFFERENT?", "gul", "One of these is different! Can you find it?")
    for k, (keys, bad, text) in enumerate(ODD):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("odd", "xmasroom", keys=keys, bad=bad)
        T.prompt(a, "Which one is different?", wait=2.2)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MAKE A PRESENT
    T.title("xmasroom", "MAKE A PRESENT!", "mishu", "You can make a present yourself! Let's try!")
    for k, (key, text) in enumerate(MAKE):
        sc = T.scene("make", "xmasroom", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MANNERS
    T.title("xmasroom", "SAY THANK YOU!", "gul", "What do we do, when we get a present?")
    for k, (text, w) in enumerate(MANNERS):
        sc = T.scene("manner", "xmasroom", w=w, k=k)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    sc = T.scene("giving", "xmasroom")
    sc["ts"] = [T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.4) for k, text in enumerate(GIVING[:2])]
    T.prompt("both", GIVING[2], wait=2.2)
    T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("xmasroom", "PRESENT DANCE!", "mishu", "Stand up! Let's do the present dance!")
    T.dance("xmasroom", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("xmasroom", "PRESENT QUIZ!", "gul", "Quick quiz time! Are you ready?")
    T.quiz("xmasroom", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "xmasroom")
    T.say("mishu", "Thank you for opening presents with us!", gap=0.2)
    sc["bye_t"] = T.say("both", "Merry Christmas, friends! Bye bye!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(21)


def noise(d):
    t = M.tt(d)
    return t, np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))


def sfx(kind):
    A = M.A
    if kind == "shake":
        out = []
        for i in range(6):
            t, n = noise(0.06)
            out.append((n * np.exp(-t / 0.02) * 0.6, i * 0.12, 0.5))
        return out
    if kind == "rip":
        t, n = noise(0.7)
        return [(n * 0.4 * np.minimum(1, t / 0.03) * np.minimum(1, (0.7 - t) / 0.3), 0, 0.6)]
    if kind == "crash":
        return [(A.tone(A.mtof(60 - i * 3), 0.2, ((1, 1), (2, 0.4)), 0.002, 0.1), i * 0.1, 0.35) for i in range(6)]
    if kind == "drumsnd":
        return [(A.tone(70, 0.3, ((1, 1), (1.6, 0.4)), 0.002, 0.15), i * 0.32, 0.8) for i in range(4)]
    if kind == "xylo":
        return [(A.tone(A.mtof(m), 0.4, ((1, 1), (4, 0.3)), 0.002, 0.2), i * 0.22, 0.4) for i, m in enumerate((72, 76, 79, 84))]
    if kind == "beep":
        return [(A.tone(f, 0.16, ((1, 1), (3, 0.3)), 0.002, 0.14), i * 0.24, 0.3) for i, f in enumerate((880, 660, 880))]
    if kind == "quack":
        out = []
        for i in range(2):
            t = M.tt(0.2)
            x = np.sign(np.sin(2 * np.pi * (420 - 300 * t) * t)) * np.sin(np.pi * t / 0.2)
            out.append((x * 0.3, i * 0.32, 0.5))
        return out
    return None


if __name__ == "__main__":
    T = build()
    deck = [72, 71, 69, 67, 65, 67, 69, 65, 67, 69, 71, 67, 69, 67, 65, 64]
    M.finish(T, music=dict(bpm=126, prog=[[60, 64, 67], [65, 69, 72], [60, 64, 67], [55, 59, 62]], hook=deck, start=1.4), sfx=sfx)
