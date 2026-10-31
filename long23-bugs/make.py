"""Long video 23: "Bugs & Insects for Kids". python make.py
Music: our own tune, code instruments."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
BUGS = [  # key, name, background, clue, fact, verb word on screen
    ("bee", "Bee", "patch", "It says buzz, buzz!", "Bees visit flowers, and make sweet honey!", "BUZZ!"),
    ("ladybug", "Ladybug", "patch", "It's red, with black spots!", "Ladybugs eat tiny bugs, and help our gardens!", "SPOTS!"),
    ("ant", "Ant", "park", "It's tiny, and it walks in a long line!", "Ants are very strong! They carry big, big food!", "STRONG!"),
    ("butterfly", "Butterfly", "patch", "It has big, colourful wings!", "Butterflies taste with their feet! Yummy flowers!", "FLUTTER!"),
    ("caterpillar", "Caterpillar", "tree", "It's long, and it loves to eat leaves!", "Caterpillars eat and eat, and grow into butterflies!", "MUNCH!"),
    ("grasshopper", "Grasshopper", "park", "It jumps very, very high!", "Grasshoppers have long back legs! Jump, jump!", "JUMP!"),
    ("dragonfly", "Dragonfly", "pond", "It zooms over the pond!", "Dragonflies have four wings, and can fly backwards!", "ZOOM!"),
    ("firefly", "Firefly", "night", "It glows in the dark!", "Fireflies light up at night! Blink, blink!", "GLOW!"),
    ("beetle", "Beetle", "tree", "It has a hard, shiny back!", "Beetles have a hard shell, to keep their wings safe!", "SHINY!"),
    ("spider", "Spider", "tree", "It has eight long legs!", "Spiders spin sticky webs, to catch their food!", "SPIN!"),
    ("worm", "Worm", "patch", "It wiggles in the soil!", "Worms have no legs! They help plants grow!", "WIGGLE!"),
    ("snail", "Snail", "patch", "It's very slow, with a shell on its back!", "Snails carry their home everywhere they go!", "SLOW!")]
PARTS = [("head", "An insect has three body parts! First, the head!"), ("thorax", "Next, the middle!"), ("abdomen", "And the back part!")]
ISNOT = [("ladybug", True, "A ladybug?", "Yes! Six legs! An insect!"), ("spider", False, "A spider?", "No! Eight legs! Not an insect!"),
         ("bee", True, "A bee?", "Yes! Six legs! An insect!"), ("worm", False, "A worm?", "No! No legs at all!"),
         ("ant", True, "An ant?", "Yes! Six legs! An insect!"), ("snail", False, "A snail?", "No! Not an insect!"),
         ("butterfly", True, "A butterfly?", "Yes! An insect with wings!")]
SPOTS = [2, 5, 7]
HONEY = [("fly", "The bee flies to a flower."), ("sip", "She sips the sweet nectar."), ("home", "She flies back to the hive."),
         ("make", "The bees turn it into honey!"), ("jar", "Sweet, yummy honey! Thank you, bees!")]
ROOMS = [("food", "This room is for food!"), ("baby", "This room is for baby ants!"), ("queen", "And here's the queen ant! She lays the eggs!")]
HOMES = [("bee", "hive", "The bee lives in a hive!"), ("spider", "web", "The spider lives on a web!"), ("worm", "soil", "The worm lives in the soil!"),
         ("snail", "snail", "The snail's home is its shell!")]
SOUNDS = [("buzz", "bee", "Buzz, buzz! A bee!"), ("chirp", "grasshopper", "Chirp, chirp! A grasshopper!"), ("crunch", "caterpillar", "Munch, munch! A hungry caterpillar!")]
MOVE = [("bee", "fly", "Bees fly!"), ("ant", "crawl", "Ants crawl!"), ("grasshopper", "jump", "Grasshoppers jump!"), ("dragonfly", "fly", "Dragonflies fly!"),
        ("caterpillar", "crawl", "Caterpillars crawl!"), ("butterfly", "fly", "Butterflies fly!"), ("worm", "crawl", "Worms wiggle and crawl!"), ("firefly", "fly", "Fireflies fly!")]
COLOURS = [("ladybug", "red", "Red!"), ("bee", "yellow", "Yellow and black!"), ("grasshopper", "green", "Green!"), ("ant", "brown", "Brown!"), ("worm", "pink", "Pink!"), ("beetle", "green", "Shiny green!")]
HIDE = [("ladybug", 1, "The ladybug is under the middle leaf!"), ("bee", 2, "The bee is under the last leaf!"),
        ("ant", 0, "The little ant! Found you!"), ("snail", 1, "The snail! Slowly, slowly!")]
SIZES = [("beetle", "ant", "Which one is bigger?", "The beetle is bigger!"), ("bee", "dragonfly", "Which one is smaller?", "The bee is smaller!")]
RULES = [("Look at bugs, but don't touch!", "LOOK!"), ("Bees can sting, so stay calm and walk away!", "STAY CALM!"),
         ("Be gentle! Bugs are little!", "BE GENTLE!"), ("Bugs help our world! Thank you, bugs!", "THANK YOU!")]
CHANT = ["Buzzy bee and ladybug,", "little ant and big black bug,", "wiggle, jiggle, hop and fly,", "bugs are busy, you and I!"]
DANCE = [("Buzz like a bee!", "shake"), ("Flutter like a butterfly!", "sway"), ("March like an ant!", "march"), ("Jump like a grasshopper!", "jump"),
         ("Wiggle like a worm!", "wiggle"), ("Spin like a spider!", "spin")]
QUIZ = [("How many legs does an insect have?", "Six!", "6"), ("Which insect makes honey?", "The bee!", "bee"),
        ("How many legs does a spider have?", "Eight!", "spider"), ("Which insect glows at night?", "The firefly!", "firefly")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: magnifier sweeps the garden
    sc = T.scene("intro", "patch")
    sc["sweep_t"] = T.mark("buzz")
    T.pause(1.4)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Bugs and insects!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Tiny little animals are hiding in the garden!", gap=0.2)
    T.say("gul", "Get your magnifying glass! Let's go on a bug hunt!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ BUG HUNT
    T.title("patch", "BUG HUNT!", "gul", "Twelve bugs are hiding! Look closely! Who is it?")
    for k, (key, name, bg, clue, fact, verb) in enumerate(BUGS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("hunt", bg, key=key, name=name.upper(), verb=verb, num=k + 1)
        T.mark("whoosh")
        T.say(a, clue, gap=0.05)
        T.prompt(a, "Who is it?", wait=1.5)
        sc["reveal_t"] = T.mark("tada")
        T.say(other(a), f"{name}!", gap=0.05)
        T.prompts.append((round(T.t, 3), round(T.t + 0.9, 3)))
        T.pause(0.9)
        sc["fact_t"] = T.say(a, fact, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ WHAT IS AN INSECT
    T.title("park", "WHAT IS AN INSECT?", "mishu", "How do we know a bug is an insect? Let's look closely!")
    sc = T.scene("anatomy", "park")
    sc["ts"] = []
    for k, (part, text) in enumerate(PARTS):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.3)
    sc["legs_say"] = T.say("gul", "Insects have six legs! Count with us!", gap=0.1)
    sc["legs"] = []
    for i in range(1, 7):
        sc["legs"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
    sc["ant_t"] = T.say("mishu", "And two antennas, to feel and smell!", gap=0.3)
    sc["sum_t"] = T.say("both", "Three parts! Six legs! That's an insect!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ INSECT OR NOT
    T.title("park", "INSECT OR NOT?", "gul", "Is it an insect? Yes, or no?")
    for k, (key, good, q, ans) in enumerate(ISNOT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("isnot", "park", key=key, good=good, q=q.upper())
        T.prompt(a, q + " Is it an insect?", wait=1.6)
        sc["answer_t"] = T.mark("yes" if good else "buzzer")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ COUNT THE SPOTS
    T.title("patch", "COUNT THE SPOTS!", "mishu", "Ladybugs have spots! Let's count them!")
    for k, n in enumerate(SPOTS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("spots", "patch", n=n)
        T.say(a, "How many spots?", gap=0.1)
        sc["cts"] = []
        for i in range(1, n + 1):
            sc["cts"].append(T.mark("pop"))
            T.say("both", f"{NUM[i].capitalize()}!", gap=0.1)
        sc["sum_t"] = T.say(other(a), f"{NUM[n].capitalize()} spots!", gap=0.5)
        T.stars.append(sc["sum_t"])
        T.end(sc)
    # ------------------------------------------------------------ HOW BEES MAKE HONEY
    T.title("patch", "HOW BEES MAKE HONEY!", "gul", "How do bees make honey? Let's follow the bee!")
    for k, (key, text) in enumerate(HONEY):
        sc = T.scene("honey", "patch", key=key, num=k + 1)
        T.mark("buzz" if key in ("fly", "home") else "pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.6)
        T.end(sc)
    # ------------------------------------------------------------ ANT TUNNELS
    T.title("underground", "UNDER THE GROUND!", "mishu", "Ants live in tunnels, under the ground! Let's look!")
    sc = T.scene("march", "underground")
    T.say("gul", "Count the ants! Marching in a line!", gap=0.1)
    sc["cts"] = []
    for i in range(1, 11):
        sc["cts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.1)
    T.pause(0.3)
    T.end(sc)
    for k, (room, text) in enumerate(ROOMS):
        sc = T.scene("room", "underground", room=room)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ SPIDER LEGS
    T.title("tree", "SPIDER LEGS!", "gul", "Spiders are not insects! Let's count the legs!")
    sc = T.scene("spiderlegs", "tree")
    sc["cts"] = []
    for i in range(1, 9):
        sc["cts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
    sc["sum_t"] = T.say("mishu", "Eight legs! Insects have six, but spiders have eight!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    sc = T.scene("webbuild", "tree")
    sc["say_t"] = T.say("gul", "The spider spins a web, round and round, with sticky silk!", gap=0.8)
    T.end(sc)
    # ------------------------------------------------------------ FIREFLY NIGHT
    T.title("night", "FIREFLY NIGHT!", "mishu", "It's dark outside! Let's count the fireflies!")
    sc = T.scene("glow", "night")
    sc["cts"] = []
    for i in range(1, 7):
        sc["cts"].append(T.mark("sparkle"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.2)
    sc["sum_t"] = T.say("gul", "Six fireflies! Blink, blink, blink!", gap=0.6)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ BUG HOMES
    T.title("patch", "WHERE DO BUGS LIVE?", "gul", "Every bug has a home! Where does it live?")
    for k, (key, home, text) in enumerate(HOMES):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("home", "patch", key=key, home=home)
        T.prompt(a, "Where does it live?", wait=1.7)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MOVE
    T.title("park", "FLY, CRAWL, OR JUMP?", "mishu", "How does it move? Fly, crawl, or jump?")
    for k, (key, mv, text) in enumerate(MOVE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("move", "park", key=key, mv=mv)
        T.prompt(a, "How does it move?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ COLOURS
    T.title("patch", "BUG COLOURS!", "gul", "Bugs are so colourful! What colour is it?")
    for k, (key, col, text) in enumerate(COLOURS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("colour", "patch", key=key, col=col)
        T.prompt(a, "What colour is it?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ BIG OR SMALL
    for k, (big, small, q, ans) in enumerate(SIZES):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("size", "patch", big=big, small=small, want="big" if k == 0 else "small")
        T.prompt(a, q, wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ SOUNDS
    T.title("tree", "BUG SOUNDS!", "mishu", "Listen carefully! Which bug is it?")
    for k, (snd, key, ans) in enumerate(SOUNDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sound", "tree", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.5)
        T.prompt(a, "Which bug is it?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ HIDE AND SEEK
    T.title("patch", "WHERE IS IT HIDING?", "gul", "Bugs love to hide! Which leaf is it under?")
    for k, (key, pos, text) in enumerate(HIDE):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("hide", "patch", key=key, pos=pos)
        T.prompt(a, "Where is it hiding?", wait=2.0)
        sc["reveal_t"] = T.mark("tada")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ BUG RULES
    T.title("park", "BE KIND TO BUGS!", "mishu", "When you see a bug, remember these rules!")
    for k, (text, w) in enumerate(RULES):
        sc = T.scene("rule", "park", w=w, k=k)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ CHANT
    sc = T.scene("chant", "patch")
    sc["l"] = [T.say("both", ln, gap=0.2) for ln in CHANT * 2]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("park", "BUG DANCE!", "gul", "Stand up! Let's do the bug dance!")
    T.dance("park", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("patch", "BUG QUIZ!", "mishu", "Quick quiz time! Are you ready?")
    T.quiz("patch", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "patch")
    T.say("mishu", "Thank you for hunting bugs with us!", gap=0.2)
    sc["bye_t"] = T.say("both", "Buzz, buzz! Bye bye!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(23)


def sfx(kind):
    A = M.A
    if kind == "buzz":
        t = M.tt(1.4)
        x = np.sign(np.sin(2 * np.pi * (190 + 18 * np.sin(2 * np.pi * 3 * t)) * t))
        return [(x * 0.16 * np.minimum(1, t / 0.1) * np.minimum(1, (1.4 - t) / 0.2), 0, 0.5)]
    if kind == "buzzer":
        t = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t)) * 0.3 * np.minimum(1, (0.4 - t) / 0.05), 0, 0.4)]
    if kind == "chirp":
        return [(A.tone(4200, 0.07, ((1, 1), (1.5, 0.4)), 0.003, 0.03), i * 0.13 + (i // 3) * 0.2, 0.2) for i in range(9)]
    if kind == "crunch":
        out = []
        for i in range(5):
            t = M.tt(0.07)
            out.append((np.diff(np.concatenate([[0], rng.standard_normal(len(t))])) * np.exp(-t / 0.02) * 0.7, i * 0.28, 0.5))
        return out
    return None


if __name__ == "__main__":
    T = build()
    tune = [79, 76, 79, 76, 81, 79, 76, 0, 77, 74, 77, 74, 79, 77, 74, 0]
    M.finish(T, music=dict(bpm=120, prog=[[60, 64, 67], [57, 60, 64], [62, 65, 69], [55, 59, 62]], hook=tune, start=1.6), sfx=sfx)
