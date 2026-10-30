"""Long video 19: "Santa Claus & Christmas Eve". python make.py
Music hook: Jingle Bells (1857, public domain) played with our own code instruments.
Reindeer names from "A Visit from St. Nicholas" (1823, public domain)."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
PARTS = [("hat", "A red hat with a white fluffy pom-pom!"), ("beard", "A long, white, fluffy beard!"),
         ("coat", "A big red coat!"), ("belt", "A black belt with a shiny gold buckle!"), ("boots", "And big black boots! Stomp, stomp!")]
LETTER = [("dear", "Dear Santa,"), ("kind", "This year, I shared my toys, and I helped my mama."),
          ("wish", "For Christmas, may I please have a teddy bear?"), ("thanks", "Thank you, Santa! Love, Mishu."),
          ("post", "Now, post it to the North Pole! Whoosh!")]
TOYS = [("teddy", "A teddy bear!"), ("car", "A toy car!"), ("ball", "A bouncy ball!"), ("toytrain", "A toy train!"), ("crayons", "Crayons!"),
        ("blocks", "Building blocks!")]
REINDEER = ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donder", "Blitzen"]
DEERFACTS = [("Reindeer have big antlers, like tree branches!"), ("Reindeer live where it's very cold and snowy!"),
             ("Reindeer love to eat carrots! Crunch, crunch!")]
CHIMNEY = [("Santa lands on the roof. Tap, tap, tap!"), ("He climbs down the chimney. Whoosh!"),
           ("He puts presents under the tree, very quietly. Shh!"), ("Then back up the chimney, and away he goes!")]
SNACK = [("cookie", "Let's leave cookies for Santa!"), ("milk", "And a glass of milk!"), ("carrot", "And carrots for the reindeer!")]
BED = [("pyjamas", "Put on your pyjamas!"), ("stocking", "Hang up your stocking!"), ("toothbrush", "Brush your teeth!"),
       ("moon", "Then off to bed! Santa only comes when you're fast asleep. Shh!")]
MORNING = [("present1", "teddy", "It's soft and cuddly!", "A teddy bear! Thank you, Santa!"),
           ("present2", "toytrain", "It goes choo choo!", "A toy train!"), ("present3", "crayons", "You can colour with them!", "Crayons!")]
YESNO = [("reindeer", True, "Does Santa have reindeer?", "Yes! Eight reindeer!"), ("toycar", False, "Does Santa drive a car?", "No! He rides a sleigh!"),
         ("snowflake", True, "Does Santa live where it snows?", "Yes! At the North Pole!"), ("sunny", False, "Does Santa come in summer?", "No! He comes on Christmas Eve!"),
         ("cookie", True, "Does Santa like cookies?", "Yes! Yummy!"), ("sunglasses", False, "Does Santa wear a green suit?", "No! He wears red!"),
         ("letter", True, "Can we write a letter to Santa?", "Yes! Dear Santa!"), ("milk", True, "Do we leave milk for Santa?", "Yes! And cookies!")]
SOUNDS = [("hoho", "santa", "Ho, ho, ho! It's Santa!"), ("jingle", "sleigh", "Sleigh bells! Jingle, jingle!"),
          ("hooves", "reindeer", "Reindeer on the roof! Clip, clop!"), ("whoosh", "chimney", "Down the chimney! Whoosh!")]
DRESS = [("santahat", "First, the red Santa hat!"), ("beard", "Then, a fluffy white beard!"), ("coat", "A big red coat!"),
         ("belt", "A black belt!"), ("boots", "And black boots!")]
KIND = [("Santa's best helpers are kind!"), ("Share your toys, like Santa shares presents!"), ("Say please, and thank you!"),
        ("Give your family a big Christmas hug!")]
CHANT = ["Jingle bells, jingle bells,", "jingle all the way!", "Oh what fun it is to ride", "in a one horse open sleigh! Hey!"]
COLOURS = [("red", "santa", "Santa's coat is red!"), ("white", "santa", "Santa's beard is white!"), ("black", "santa", "Santa's boots are black!"),
           ("gold", "santa", "Santa's buckle is gold!"), ("brown", "reindeer", "The reindeer are brown!")]
COOKIES = [(5, 2, "Santa had five cookies. He ate two. Yum, yum! How many are left?", "Three cookies!"),
           (4, 1, "Four cookies on the plate. Santa ate one. How many are left?", "Three cookies!"),
           (3, 3, "Three cookies. Santa ate all three! How many are left?", "Zero! None left! Ha ha!")]
HIDE = [("santahat", 1, "Santa's hat is under the blue present!"), ("bell", 2, "The sleigh bell is under the green present!"),
        ("letter", 0, "The letter is under the pink present!"), ("carrot", 1, "The reindeer's carrot! Found it!")]
PATTERNS = [(["reindeer", "present1", "reindeer", "present1", "reindeer"], "present1", "A present!"),
            (["santahat", "santahat", "bell", "santahat", "santahat"], "bell", "A bell!"),
            (["cookie", "milk", "cookie", "milk", "cookie"], "milk", "Milk!")]
WARM = [("santahat", "A warm hat!"), ("scarf", "A cosy scarf!"), ("mitt", "Warm mittens!"), ("boots", "And snow boots! Now we're ready for the North Pole!")]
FEEL = [("excited", "gul", "Santa is coming tonight! I feel so excited!"), ("tired", "misheal", "It's late. I feel sleepy. Yawn!"),
        ("surprised", "gul", "Look! Presents! I feel surprised!"), ("happy", "misheal", "A teddy bear from Santa! I feel so happy!")]
DANCE = [("Ho, ho, ho! Hold your belly!", "shake"), ("Fly like a reindeer!", "jump"), ("Ride the sleigh!", "sway"),
         ("Stomp like Santa's boots!", "stomp"), ("Wiggle like an elf!", "wiggle"), ("Merry Christmas! Hooray!", "jump")]
QUIZ = [("What colour is Santa's coat?", "Red!", "santa"), ("Who pulls Santa's sleigh?", "The reindeer!", "reindeer"),
        ("How does Santa get inside?", "Down the chimney!", "chimney"), ("What do we leave for Santa?", "Cookies and milk!", "cookie")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: night, sleigh flies past the moon
    sc = T.scene("intro", "roof")
    T.pause(0.3)
    sc["fly_t"] = T.mark("jingle")
    T.pause(1.6)
    sc["title_t"] = T.mark("slam")
    T.say("both", "It's Christmas Eve!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Tonight, Santa Claus is coming!", gap=0.2)
    T.say("gul", "Let's find out all about Santa! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ MEET SANTA
    T.title("northpole", "MEET SANTA!", "gul", "This is Santa Claus! He lives at the North Pole!")
    sc = T.scene("meet", "northpole")
    sc["ho_t"] = T.mark("hoho")
    T.pause(1.3)
    T.say("mishu", "Santa is kind, and jolly, and he loves to laugh! Ho, ho, ho!", gap=0.5)
    T.end(sc)
    for k, (part, text) in enumerate(PARTS):
        sc = T.scene("part", "northpole", part=part)
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ SANTA COLOURS
    T.title("northpole", "SANTA COLOURS!", "mishu", "Santa is so colourful! What colour is it?")
    for k, (col, key, text) in enumerate(COLOURS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("colour", "northpole", col=col, key=key)
        T.prompt(a, "What colour is it?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ LETTER TO SANTA
    T.title("xmasroom", "LETTER TO SANTA!", "mishu", "Let's write a letter to Santa!")
    sc = T.scene("letter", "xmasroom")
    sc["ts"] = []
    for k, (key, text) in enumerate(LETTER):
        sc["ts"].append(T.mark("whoosh" if key == "post" else "pop"))
        T.say("mishu" if k < 4 else "gul", text, gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ WARM CLOTHES
    T.title("northpole", "BRRR! IT'S COLD!", "gul", "The North Pole is very cold! What do we wear?")
    sc = T.scene("warm", "northpole")
    sc["ts"] = []
    for k, (key, text) in enumerate(WARM):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.3)
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ WORKSHOP
    T.title("northpole", "SANTA'S WORKSHOP!", "gul", "At the North Pole, Santa's helpers make toys all year!")
    sc = T.scene("workshop", "northpole")
    sc["ts"] = []
    for k, (key, text) in enumerate(TOYS):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.2)
    sc["sum_t"] = T.say("both", "Six toys! Tap, tap, all done!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ LOAD THE SLEIGH
    T.title("northpole", "LOAD THE SLEIGH!", "mishu", "Let's load the presents onto the sleigh! Count with us!")
    sc = T.scene("load", "northpole")
    sc["ts"] = []
    for i in range(1, 11):
        sc["ts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
    T.say("gul", "Ten presents! The sleigh is full!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ REINDEER
    T.title("northpole", "SANTA'S REINDEER!", "gul", "Santa's sleigh is pulled by eight reindeer! Let's meet them!")
    sc = T.scene("deer", "northpole")
    sc["ts"] = []
    for i, nm in enumerate(REINDEER):
        sc["ts"].append(T.mark("hooves1"))
        T.say("mishu" if i % 2 == 0 else "gul", f"{NUM[i + 1].capitalize()}, {nm}!", gap=0.15)
    sc["sum_t"] = T.say("both", "Eight reindeer! Ready to fly!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    for k, text in enumerate(DEERFACTS):
        sc = T.scene("deerfact", "northpole", k=k)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ FLYING
    T.title("roof", "UP, UP, AND AWAY!", "mishu", "Santa's sleigh flies all around the world!")
    sc = T.scene("fly", "roof")
    sc["go_t"] = T.mark("jingle")
    T.say("both", "Up, up, and away!", gap=0.2)
    sc["ts"] = []
    for i in range(1, 6):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if i % 2 else "mishu", f"House {NUM[i]}!", gap=0.2)
    T.say("both", "Santa visits every house, all in one night!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ DOWN THE CHIMNEY
    T.title("roof", "DOWN THE CHIMNEY!", "gul", "How does Santa get inside? Let's see!")
    sc = T.scene("chimney", "roof")
    sc["ts"] = []
    for k, text in enumerate(CHIMNEY):
        sc["ts"].append(T.mark(["hooves", "whoosh", "pop", "jingle"][k]))
        T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ COOKIES AND MILK
    T.title("xmasroom", "COOKIES FOR SANTA!", "mishu", "Santa gets hungry! Let's leave him a snack!")
    sc = T.scene("snack", "xmasroom")
    sc["ts"] = []
    for k, (key, text) in enumerate(SNACK):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.3)
    sc["count_t"] = T.say("both", "Three cookies, one milk, two carrots! Thank you, Santa!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ BEDTIME
    T.title("xmasroom", "CHRISTMAS EVE BEDTIME!", "gul", "It's getting late! Time to get ready for bed!")
    for k, (key, text) in enumerate(BED):
        sc = T.scene("bed", "xmasroom", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    sc = T.scene("night", "roof")
    T.pause(0.4)
    sc["land_t"] = T.mark("jingle")
    T.pause(1.4)
    T.say("gul", "Shh! Santa is here! Ho, ho, ho!", gap=0.3)
    sc["away_t"] = T.mark("whoosh")
    T.say("mishu", "Merry Christmas to all, and to all a good night!", gap=0.6)
    T.end(sc)
    # ------------------------------------------------------------ COUNTDOWN
    sc = T.scene("countdown", "roof")
    T.say("mishu", "Let's count down to Christmas morning!", gap=0.1)
    sc["ts"] = []
    for w in ("Ten!", "Nine!", "Eight!", "Seven!", "Six!", "Five!", "Four!", "Three!", "Two!", "One!"):
        sc["ts"].append(T.mark("ding"))
        T.say("both", w, gap=0.12)
    sc["go_t"] = T.mark("tada")
    T.say("both", "Merry Christmas!", gap=0.6)
    T.end(sc)
    # ------------------------------------------------------------ CHRISTMAS MORNING
    T.title("xmasroom", "CHRISTMAS MORNING!", "mishu", "Wake up! It's Christmas morning! Santa came!")
    for k, (box, inside, clue, ans) in enumerate(MORNING):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("open", "xmasroom", box=box, inside=inside)
        sc["shake_t"] = T.mark("shake")
        T.say(a, clue, gap=0.1)
        T.prompt(a, "What's inside?", wait=1.8)
        sc["open_t"] = T.mark("tada")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    sc = T.scene("eaten", "xmasroom")
    T.say("gul", "Look! The cookies are gone!", gap=0.1)
    sc["note_t"] = T.mark("sparkle")
    T.say("mishu", "And Santa left a note! Thank you for the cookies! Love, Santa!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ COOKIE MATHS
    T.title("xmasroom", "COOKIE MATHS!", "gul", "Santa loves cookies! Let's count, and take away!")
    for k, (n, eat, q, ans) in enumerate(COOKIES):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("cookies", "xmasroom", n=n, eat=eat)
        T.say(a, q.rsplit(". ", 1)[0] + ".", gap=0.1)
        sc["eat_t"] = T.mark("crunch")
        T.pause(0.6)
        T.prompt(a, q.rsplit(". ", 1)[1], wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ HIDE AND SEEK
    T.title("xmasroom", "WHERE IS IT?", "mishu", "Something is hiding under a present! Can you find it?")
    for k, (key, pos, text) in enumerate(HIDE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("hide", "xmasroom", key=key, pos=pos)
        T.prompt(a, "Which present is it under?", wait=2.0)
        sc["reveal_t"] = T.mark("tada")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ YES OR NO
    T.title("northpole", "YES OR NO?", "gul", "Santa yes or no game! Shout yes, or no!")
    for k, (key, good, q, ans) in enumerate(YESNO):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("yesno", "northpole", key=key, good=good, q=q.upper())
        T.prompt(a, q, wait=1.6)
        sc["answer_t"] = T.mark("yes" if good else "buzz")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ PATTERNS
    T.title("northpole", "WHAT COMES NEXT?", "gul", "Big kids! Look at the pattern. What comes next?")
    for k, (seq, ans, line_) in enumerate(PATTERNS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("pattern", "northpole", seq=seq, ans=ans)
        T.prompt(a, "What comes next?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), line_, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ SOUNDS
    T.title("roof", "SANTA SOUNDS!", "mishu", "Listen carefully! What is that sound?")
    for k, (snd, key, ans) in enumerate(SOUNDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sound", "roof", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.6)
        T.prompt(a, "What is it?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ FEELINGS
    T.title("xmasroom", "CHRISTMAS FEELINGS!", "mishu", "How does Christmas Eve make you feel?")
    for k2, (emo, who, text) in enumerate(FEEL):
        sc = T.scene("feel", "xmasroom", emo=emo, who=who)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if who == "gul" else "mishu", text, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.3, 3)))
        T.pause(1.3)
        T.end(sc)
    # ------------------------------------------------------------ DRESS UP LIKE SANTA
    T.title("xmasroom", "DRESS UP LIKE SANTA!", "gul", "Let's dress Gul up like Santa!")
    sc = T.scene("dress", "xmasroom")
    sc["ts"] = []
    for k, (key, text) in enumerate(DRESS):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu", text, gap=0.3)
    sc["done_t"] = T.mark("tada")
    T.say("gul", "Ho, ho, ho! I'm Santa Gul!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ KINDNESS
    T.title("xmasroom", "SANTA'S HELPERS!", "mishu", "We can all be Santa's helpers!")
    for k, text in enumerate(KIND):
        sc = T.scene("kind", "xmasroom", k=k)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ JINGLE BELLS
    T.title("roof", "JINGLE BELLS!", "gul", "Let's say Jingle Bells together!")
    sc = T.scene("chant", "roof")
    sc["l"] = [T.say("both", ln, gap=0.2) for ln in CHANT * 2]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("northpole", "SANTA DANCE!", "mishu", "Stand up! Let's do the Santa dance!")
    T.dance("northpole", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("northpole", "SANTA QUIZ!", "gul", "Quick quiz time! Are you ready?")
    T.quiz("northpole", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "roof")
    T.say("mishu", "Thank you for waiting for Santa with us!", gap=0.2)
    sc["bye_t"] = T.say("both", "Merry Christmas, friends! Bye bye!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(19)


def bells():
    t = M.tt(0.12)
    return np.diff(np.concatenate([[0], rng.standard_normal(len(t))])) * np.exp(-t / 0.03) * 0.6


def clop(off, out):
    t2 = M.tt(0.08)
    x = np.sin(2 * np.pi * 900 * t2) * np.exp(-t2 / 0.012) + np.diff(np.concatenate([[0], rng.standard_normal(len(t2))])) * np.exp(-t2 / 0.006) * 0.4
    out.append((x * 0.8, off, 0.5))


def sfx(kind):
    A = M.A
    if kind == "buzz":
        t2 = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t2)) * 0.3 * np.minimum(1, (0.4 - t2) / 0.05), 0, 0.4)]
    if kind == "jingle":
        return [(bells(), i * 0.12, 0.6) for i in range(12)] + [(A.tone(A.mtof(88 + (i % 2) * 4), 0.4, ((1, 1), (2.76, 0.4)), 0.002, 0.2), i * 0.24, 0.2) for i in range(6)]
    if kind == "shake":
        return [(bells(), i * 0.15, 0.5) for i in range(5)]
    if kind in ("hooves", "hooves1"):
        out = []
        for i in range(8 if kind == "hooves" else 2):
            clop(i * 0.17 + (0.05 if i % 2 else 0), out)
        return out
    if kind == "crunch":
        out = []
        for i in range(4):
            t2 = M.tt(0.07)
            out.append((np.diff(np.concatenate([[0], rng.standard_normal(len(t2))])) * np.exp(-t2 / 0.02) * 0.7, i * 0.13, 0.5))
        return out
    if kind == "hoho":
        out = []
        for i in range(3):
            t2 = M.tt(0.3)
            ph = np.cumsum(110 - 20 * t2 / 0.3) / M.SR
            x = np.sin(2 * np.pi * ph) + 0.5 * np.sin(4 * np.pi * ph)
            out.append((x * np.sin(np.pi * t2 / 0.3) * 0.7, i * 0.4, 0.6))
        return out
    return None


if __name__ == "__main__":
    T = build()
    jingle = [76, 76, 76, 0, 76, 76, 76, 0, 76, 79, 72, 74, 76, 0, 0, 0]
    M.finish(T, music=dict(bpm=124, prog=[[60, 64, 67], [65, 69, 72], [60, 64, 67], [55, 59, 62]], hook=jingle, start=2.0, tick=bells()), sfx=sfx)
