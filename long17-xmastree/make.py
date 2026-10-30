"""Long video 17: "Decorate the Christmas Tree". python make.py
Music hook: Jingle Bells (1857, public domain) played with our own code instruments."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other, PRAISE

M = Maker(__file__)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
DECOR = [  # stage key, how many, intro line, plural name, colour/fact
    ("lights", 5, "First, the twinkly lights! Let's count the colours!", "lights", "Red, orange, yellow, green, blue!"),
    ("baubles", 5, "Now, shiny red balls! Count them with us!", "red balls", "They're round, like circles!"),
    ("bells", 3, "Next, golden bells! Ding, ding, ding!", "golden bells", "Jingle, jingle!"),
    ("canes", 4, "Candy canes! Red and white stripes!", "candy canes", "They look like the letter J!"),
    ("ginger", 2, "Two gingerbread friends!", "gingerbread friends", "Run, run, as fast as you can!"),
    ("flakes", 6, "And sparkly snowflakes!", "snowflakes", "Every snowflake is different!")]
SHAPES = [("circle", "The red ball is a circle!"), ("triangle", "The tree is a big triangle!"), ("star", "The star on top is a star shape!"),
          ("rectangle", "The present is a rectangle!"), ("heart", "And look, a heart! We love Christmas!")]
COLOURS = [("red", "stocking", "The stocking is red!"), ("green", "tree", "The tree is green!"), ("gold", "bell", "The bell is gold!"),
           ("white", "snowflake", "The snowflake is white!"), ("brown", "gingerbread", "The gingerbread man is brown!")]
PRESENTS = [("present1", "ball", "It's round, and it bounces!", "A ball!"), ("present2", "teddy", "It's soft and cuddly!", "A teddy bear!"),
            ("present3", "car", "It has four wheels! Vroom!", "A toy car!"), ("present1", "crayons", "You can draw with them!", "Crayons!")]
STOCKINGS = ["Gul", "Mishu", "Mama", "Papa"]
WORDS = [("tree", "Christmas tree"), ("topstar", "Star"), ("present1", "Present"), ("stocking", "Stocking"), ("candycane", "Candy cane"),
         ("bell", "Bell"), ("gingerbread", "Gingerbread man"), ("snowman", "Snowman"), ("santahat", "Santa hat"), ("snowflake", "Snowflake")]
BAKE = [("bowl", "First, mix flour, sugar, and spices. Stir, stir, stir!"), ("roll", "Roll the dough, nice and flat."),
        ("cut", "Cut out gingerbread shapes!"), ("oven", "Bake them in the oven. Ask a grown-up to help!"),
        ("decorate", "Decorate with icing and sweets! Yummy!")]
PATTERNS = [(["red", "green", "red", "green", "red"], "green", "Green!"), (["star", "bell", "star", "bell", "star"], "bell", "A bell!"),
            (["red", "red", "gold", "red", "red"], "gold", "Gold!")]
BIGSMALL = [("big", "Which ball is bigger?"), ("small", "Which present is smaller?"), ("big", "Which star is bigger?")]
SOUNDS = [("jingle", "bell", "Jingle bells!"), ("crackle", "fire", "The fire! Crackle, crackle!"),
          ("rustle", "present1", "Wrapping paper! Rip, rip!"), ("hoho", "santahat", "Ho, ho, ho! It's Santa!")]
SNOWMAN = [("big", "First, a big snowball for the bottom!"), ("mid", "A middle snowball on top!"), ("small", "A small snowball for the head!"),
           ("eyes", "Two eyes, and a carrot nose!"), ("arms", "Stick arms! Hello, snowman!"), ("hat", "And a warm Santa hat!")]
WRAP = [("box", "Put the toy in the box."), ("paper", "Wrap it in shiny paper."), ("tape", "Tape it, so it stays closed."),
        ("bow", "Add a big bow on top!"), ("tag", "Write a name tag: To Grandma, with love!")]
XORNOT = [("bell", True, "A jingle bell?", "Yes! Christmas!"), ("sunny", False, "A hot sunny beach?", "No! Christmas is in winter!"),
          ("snowman", True, "A snowman?", "Yes! Christmas!"), ("icecream", False, "An ice cream cone?", "No, that's for summer!"),
          ("candycane", True, "A candy cane?", "Yes! Christmas!"), ("umbrella", False, "A rain umbrella?", "No, not Christmas!")]
FEEL = [("excited", "gul", "Presents! I feel so excited!"), ("surprised", "misheal", "A new teddy? Wow! I feel surprised!"),
        ("happy", "gul", "Christmas with my family makes me feel happy!"), ("proud", "misheal", "I made a card for Grandma! I feel proud!")]
HIDE = [("topstar", 1, "The star is under the blue present!"), ("bell", 2, "The bell is under the green present!"),
        ("candycane", 0, "The candy cane is under the pink present!"), ("gingerbread", 1, "Gingerbread man, found you!")]
CHANT = ["Jingle, jingle, little bell,", "lights so bright, and snow so white!", "Presents, cookies, stockings too,", "Merry Christmas, me and you!"]
KINDNESS = [("present2", "Make a present for someone you love!"), ("heart", "Make a Christmas card for Grandma!"),
            ("tree", "Help your family decorate the tree!")]
DANCE = [("Stand tall like a Christmas tree!", "stretch"), ("Twinkle, twinkle, little lights!", "wiggle"), ("Jingle like a bell!", "shake"),
         ("Spin like a snowflake!", "spin"), ("Jump for presents!", "jump"), ("Merry Christmas! Hooray!", "jump")]
QUIZ = [("What goes on top of the tree?", "A star!", "topstar"), ("What colour is a Christmas tree?", "Green!", "tree"),
        ("What shape is a Christmas ball?", "A circle!", "bauble"), ("How many golden bells did we hang?", "Three!", "bell"),
        ("What shape is the tree?", "A triangle!", "tree"), ("What has red and white stripes?", "A candy cane!", "candycane"),
        ("What do we hang by the fireplace?", "Stockings!", "stocking"), ("What do we say at Christmas?", "Merry Christmas!", "present1"),
        ("What do we bake at Christmas?", "Gingerbread cookies!", "gingerbread"), ("What makes a jingle sound?", "Bells!", "bell"),
        ("What is made of snow, with a carrot nose?", "A snowman!", "snowman"), ("Red, green, red, green... what's next?", "Red!", "bauble")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: dark room, lights switch on
    sc = T.scene("intro", "xmasroom")
    T.pause(0.4)
    sc["on_t"] = T.mark("lightson")
    T.pause(1.0)
    sc["title_t"] = T.mark("slam")
    T.say("both", "It's Christmas time!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Let's decorate the Christmas tree together!", gap=0.2)
    T.say("gul", "Count, colours, and shapes! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ BRING IN THE TREE
    sc = T.scene("bring", "xmasroom")
    T.say("gul", "Here comes our Christmas tree! Heave, ho!", gap=0.2)
    sc["set_t"] = T.mark("boing")
    T.say("mishu", "It's so big and green! Now it needs decorations!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ DECORATE STAGE BY STAGE
    T.title("xmasroom", "DECORATE THE TREE!", "gul", "Let's decorate, and count!")
    for k, (key, n, intro, plural, fact) in enumerate(DECOR):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("decor", "xmasroom", key=key, n=n, stage=k)
        sc["intro_t"] = T.say(a, intro, gap=0.1)
        cts = []
        for i in range(1, n + 1):
            cts.append(T.mark("ornament"))
            T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
        sc["cts"] = cts
        sc["sum_t"] = T.say(other(a), f"{NUM[n].capitalize()} {plural}! {fact}", gap=0.5)
        T.stars.append(sc["sum_t"])
        T.end(sc)
    # ------------------------------------------------------------ STAR ON TOP, countdown
    sc = T.scene("star", "xmasroom")
    T.say("mishu", "Now, the most important part! The star on top!", gap=0.1)
    cd = []
    for w in ("Three!", "Two!", "One!"):
        cd.append(T.mark("ding"))
        T.say("both", w, gap=0.25)
    sc["cd"] = cd
    sc["star_t"] = T.mark("lightson")
    T.say("both", "Wow! Our Christmas tree is beautiful!", gap=0.8)
    T.end(sc)
    # ------------------------------------------------------------ SHAPES ON THE TREE
    T.title("xmasroom", "CHRISTMAS SHAPES!", "gul", "Can you find shapes on our tree?")
    for k, (shp, text) in enumerate(SHAPES):
        sc = T.scene("shape", "xmasroom", shape=shp)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS COLOURS
    T.title("xmasroom", "CHRISTMAS COLOURS!", "mishu", "Christmas is so colourful! What colour is it?")
    for k, (col, key, text) in enumerate(COLOURS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("colour", "xmasroom", col=col, key=key)
        T.prompt(a, "What colour is it?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ PRESENTS: GUESS WHAT'S INSIDE
    T.title("xmasroom", "WHAT'S INSIDE?", "gul", "Presents under the tree! Let's guess what's inside!")
    for k, (box, inside, clue, ans) in enumerate(PRESENTS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("present", "xmasroom", box=box, inside=inside)
        sc["shake_t"] = T.mark("shake")
        T.say(a, clue, gap=0.1)
        T.prompt(a, "What's inside?", wait=1.8)
        sc["open_t"] = T.mark("tada")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ STOCKINGS
    T.title("xmasroom", "HANG THE STOCKINGS!", "mishu", "Let's hang a stocking for everyone in the family!")
    sc = T.scene("stockings", "xmasroom")
    ts = []
    for i, name in enumerate(STOCKINGS):
        ts.append(T.mark("pop"))
        T.say("gul" if i % 2 == 0 else "mishu", f"One for {name}!", gap=0.2)
    sc["ts"] = ts
    sc["count_t"] = T.say("both", "Four stockings! One, two, three, four!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS WORDS
    T.title("xmasroom", "CHRISTMAS WORDS!", "gul", "Let's learn Christmas words! Say them with us!")
    for k, (key, w) in enumerate(WORDS):
        sc = T.scene("cword", "xmasroom", key=key, w=w.upper(), num=k + 1)
        T.mark("ornament")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", f"{w}!", gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.1, 3)))
        T.pause(1.1)
        T.end(sc)
    # ------------------------------------------------------------ COUNT THE PRESENTS
    sc = T.scene("count", "xmasroom")
    T.say("mishu", "So many presents under the tree! Let's count them!", gap=0.1)
    cts = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!", "Six!", "Seven!", "Eight!", "Nine!", "Ten!"):
        cts.append(T.mark("ornament"))
        T.say("both", w, gap=0.15)
    sc["cts"] = cts
    T.say("gul", "Ten presents! Wow!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ BAKE GINGERBREAD
    T.title("xmasroom", "BAKE GINGERBREAD!", "mishu", "Let's bake gingerbread cookies!")
    for k, (key, text) in enumerate(BAKE):
        sc = T.scene("bake", "xmasroom", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ BUILD A SNOWMAN
    T.title("xmasroom", "BUILD A SNOWMAN!", "gul", "Let's build a snowman, step by step!")
    sc = T.scene("snowman", "xmasroom")
    sc["ts"] = []
    for k, (key, text) in enumerate(SNOWMAN):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.4)
    sc["done_t"] = T.mark("tada")
    T.say("both", "Our snowman is ready! Brrr!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ WRAP A PRESENT
    T.title("xmasroom", "WRAP A PRESENT!", "mishu", "Let's wrap a present for someone we love!")
    sc = T.scene("wrap", "xmasroom")
    sc["ts"] = []
    for k, (key, text) in enumerate(WRAP):
        sc["ts"].append(T.mark("shake" if key == "paper" else "pop"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.4)
    sc["done_t"] = T.mark("tada")
    T.say("both", "Ta-da! A beautiful present!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS OR NOT?
    T.title("xmasroom", "CHRISTMAS OR NOT?", "gul", "Is it a Christmas thing? Yes, or no?")
    for k, (key, good, q, ans) in enumerate(XORNOT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("xornot", "xmasroom", key=key, good=good, q=q.upper())
        T.prompt(a, q, wait=1.6)
        sc["answer_t"] = T.mark("yes" if good else "buzz")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ PATTERNS
    T.title("xmasroom", "WHAT COMES NEXT?", "gul", "Big kids! Look at the pattern. What comes next?")
    for k, (seq, ans, line_) in enumerate(PATTERNS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("pattern", "xmasroom", seq=seq, ans=ans)
        T.prompt(a, "What comes next?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), line_, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ BIG OR SMALL
    for k, (ans, q) in enumerate(BIGSMALL):
        sc = T.scene("bigsmall", "xmasroom", ans=ans, kind2=["ball", "present", "star"][k])
        T.prompt("gul" if k % 2 == 0 else "mishu", q, wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say("mishu" if k % 2 == 0 else "gul", "This one!", gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS SOUNDS
    T.title("xmasroom", "CHRISTMAS SOUNDS!", "mishu", "Listen! What makes this Christmas sound?")
    for k, (snd, key, ans) in enumerate(SOUNDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sound", "xmasroom", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.6)
        T.prompt(a, "What is it?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS KINDNESS
    T.title("xmasroom", "CHRISTMAS KINDNESS!", "gul", "Christmas is about love, and being kind!")
    for k, (key, text) in enumerate(KINDNESS):
        sc = T.scene("kindness", "xmasroom", key=key)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS FEELINGS
    T.title("xmasroom", "CHRISTMAS FEELINGS!", "mishu", "How does Christmas make you feel?")
    for k, (emo, who, text) in enumerate(FEEL):
        sc = T.scene("feel", "xmasroom", emo=emo, who=who)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if who == "gul" else "mishu", text, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.4, 3)))
        T.pause(1.4)
        T.end(sc)
    # ------------------------------------------------------------ FIND THE HIDDEN ORNAMENT
    T.title("xmasroom", "WHERE IS IT HIDING?", "gul", "Something is hiding under a present! Can you find it?")
    for k, (key, pos, text) in enumerate(HIDE):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("hide", "xmasroom", key=key, pos=pos)
        T.prompt(a, "Which present is it under?", wait=2.0)
        sc["reveal_t"] = T.mark("tada")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS CHANT
    sc = T.scene("chant", "xmasroom")
    sc["l"] = [T.say("both", ln, gap=0.2) for ln in CHANT * 2]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS DANCE
    T.title("xmasroom", "CHRISTMAS DANCE!", "gul", "Stand up! Let's do the Christmas dance!")
    T.dance("xmasroom", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("xmasroom", "CHRISTMAS QUIZ!", "mishu", "Quiz time! Are you ready?")
    T.quiz("xmasroom", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "xmasroom")
    T.say("mishu", "Thank you for decorating the tree with us!", gap=0.2)
    sc["bye_t"] = T.say("both", "Merry Christmas, friends! Bye bye!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(17)


def sleigh():
    t = M.tt(0.12)
    x = np.diff(np.concatenate([[0], rng.standard_normal(len(t))])) * np.exp(-t / 0.03)
    return x * 0.6


def sfx(kind):
    A = M.A
    if kind == "ornament":
        return [(A.tone(A.mtof(88), 0.6, ((1, 1), (2.76, 0.3), (5.4, 0.1)), 0.002, 0.3), 0.05, 0.25)]
    if kind == "lightson":
        return [(A.sfx_sparkle(), 0, 0.6)] + [(A.tone(A.mtof(m), 0.8, ((1, 1), (2.76, 0.3)), 0.002, 0.4), 0.1 + i * 0.08, 0.15)
                                          for i, m in enumerate((84, 88, 91, 96))]
    if kind == "buzz":
        t2 = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t2)) * 0.3 * np.minimum(1, (0.4 - t2) / 0.05), 0, 0.4)]
    if kind == "jingle":
        return [(sleigh(), i * 0.12, 0.6) for i in range(10)] + [(M.A.tone(M.A.mtof(88 + (i % 2) * 4), 0.4, ((1, 1), (2.76, 0.4)), 0.002, 0.2), i * 0.24, 0.2) for i in range(6)]
    if kind == "crackle":
        out = []
        for i in range(14):
            t2 = M.tt(0.05)
            out.append((np.diff(np.concatenate([[0], rng.standard_normal(len(t2))])) * np.exp(-t2 / 0.01) * 0.8, rng.uniform(0, 1.4), 0.5))
        return out
    if kind == "rustle":
        t2 = M.tt(1.2)
        nz = np.diff(np.concatenate([[0], rng.standard_normal(len(t2))])) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 5 * t2)))
        return [(nz * 0.35 * np.minimum(1, (1.2 - t2) / 0.2), 0, 0.6)]
    if kind == "hoho":
        out = []
        for i in range(3):
            t2 = M.tt(0.3)
            x = np.sin(2 * np.pi * np.cumsum(110 - 20 * t2 / 0.3) / M.SR) + 0.5 * np.sin(4 * np.pi * np.cumsum(110 - 20 * t2 / 0.3) / M.SR)
            out.append((x * np.sin(np.pi * t2 / 0.3) * 0.7, i * 0.4, 0.6))
        return out
    if kind == "shake":
        return [(sleigh(), i * 0.15, 0.5) for i in range(5)]
    return None


if __name__ == "__main__":
    T = build()
    jingle = [76, 76, 76, 0, 76, 76, 76, 0, 76, 79, 72, 74, 76, 0, 0, 0]
    M.finish(T, music=dict(bpm=120, prog=[[60, 64, 67], [65, 69, 72], [60, 64, 67], [55, 59, 62]], hook=jingle, start=1.6, tick=sleigh()), sfx=sfx)
