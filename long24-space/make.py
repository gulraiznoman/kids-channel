"""Long video 24: "Space & Planets for Kids". python make.py
Music: our own tune, code instruments."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
PLANETS = [  # key, name, fact, second fact, word on screen
    ("mercury", "Mercury", "Mercury is the smallest planet!", "And it's the closest to the Sun!", "SMALLEST!"),
    ("venus", "Venus", "Venus is the hottest planet!", "It's covered in thick clouds!", "HOTTEST!"),
    ("earth", "Earth", "Earth is our home!", "It has water, air, and living things!", "OUR HOME!"),
    ("mars", "Mars", "Mars is the red planet!", "It's red, rocky, and dusty!", "RED PLANET!"),
    ("jupiter", "Jupiter", "Jupiter is the biggest planet!", "It has a giant storm, called the red spot!", "BIGGEST!"),
    ("saturn", "Saturn", "Saturn has beautiful rings!", "The rings are made of ice and rock!", "RINGS!"),
    ("uranus", "Uranus", "Uranus spins on its side!", "It's a very cold, blue green planet!", "SIDEWAYS!"),
    ("neptune", "Neptune", "Neptune is the farthest from the Sun!", "It's dark, cold, and very windy!", "FARTHEST!")]
SUIT = [("helmet", "A big round helmet, to help us breathe!"), ("suit", "A thick space suit, to keep us safe!"), ("gloves", "Strong gloves!"), ("boots", "And big moon boots!")]
ROCKET = [("body", "Here's the rocket's tall body!"), ("wings", "Add the fins, to fly straight!"), ("window", "A round window, to see the stars!"), ("fuel", "Fill it with fuel!")]
MOON = [("The Moon goes around the Earth!", "orbit"), ("The Moon is covered in rocks and big round craters!", "craters"),
        ("There is no air on the Moon, so astronauts wear space suits!", "suit"), ("Footprints on the Moon stay there for a long, long time!", "print")]
PHASES = [(0.0, "New moon! We can't see it!"), (0.25, "A thin crescent moon!"), (0.5, "A half moon!"), (1.0, "A big, round full moon!")]
FLOAT = [("hair", "In space, there's almost no gravity, so everything floats!"), ("food", "Astronauts' food floats too! Catch it!"),
         ("sleep", "They strap in to sleep, so they don't float away!")]
SORT = [("rocket", True, "A rocket?", "Yes! Rockets go to space!"), ("car", False, "A car?", "No! Cars stay on the road!"),
        ("astronaut", True, "An astronaut?", "Yes! Astronauts go to space!"), ("fish", False, "A fish?", "No! Fish live in water!"),
        ("comet", True, "A comet?", "Yes! A comet is a ball of ice and dust!"), ("duck", False, "A duck?", "No! Ducks stay near ponds!"),
        ("moon2", True, "The Moon?", "Yes! The Moon is in space!"), ("star", True, "A star?", "Yes! Stars are in space!")]
WHICH = [("Which planet is our home?", "earth", "Earth!"), ("Which planet has rings?", "saturn", "Saturn!"), ("Which planet is the biggest?", "jupiter", "Jupiter!"),
         ("Which planet is red?", "mars", "Mars!"), ("Which is the smallest planet?", "mercury", "Mercury!"),
         ("Which planet is the hottest?", "venus", "Venus!"), ("Which planet is the farthest from the Sun?", "neptune", "Neptune!")]
ORDERQ = [("Mercury, Venus, Earth...", "mars", "Mars!"), ("Mars, Jupiter...", "saturn", "Saturn!"), ("Saturn, Uranus...", "neptune", "Neptune!")]
STARS = [(4, "A kite!"), (5, "A big star!")]
ROCKY = [("earth", True), ("jupiter", False), ("mars", True), ("saturn", False), ("venus", True), ("neptune", False), ("mercury", True), ("uranus", False)]
HOTCOLD = [("venus", True, "Venus! Super hot!"), ("neptune", False, "Neptune! Freezing cold!"), ("mercury", True, "Mercury! Very hot in the sunshine!"), ("uranus", False, "Uranus! Icy cold!")]
PCOL = [("mars", "RED", "Red!"), ("neptune", "BLUE", "Deep blue!"), ("earth", "BLUE AND GREEN", "Blue and green!"), ("venus", "YELLOW", "Yellow!"),
        ("uranus", "LIGHT BLUE", "Light blue!"), ("jupiter", "ORANGE AND BROWN", "Orange and brown!"), ("mercury", "GREY", "Grey!")]
TELE = [("moon2", "Look through the telescope! I can see the Moon!"), ("saturn", "I can see Saturn's rings!"), ("comet", "I can see a comet, with a long, shiny tail!")]
RHYME = ["Mercury, Venus, close to the Sun,", "Earth is our home, and Mars is fun!", "Jupiter, Saturn, giants so wide,", "Uranus, Neptune, on the far side!"]
DANCE = [("Blast off! Jump up!", "jump"), ("Spin like a planet!", "spin"), ("Float like an astronaut!", "sway"), ("Stomp on the Moon!", "stomp"),
         ("Twinkle like a star!", "shake"), ("Fly like a rocket!", "stretch")]
QUIZ = [("Which planet is our home?", "Earth!", "earth"), ("How many planets go around the Sun?", "Eight!", "8"),
        ("Who flies to space?", "Astronauts!", "astronaut"), ("Which planet has rings?", "Saturn!", "saturn")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: rocket countdown
    sc = T.scene("intro", "launch")
    sc["ts"] = []
    for w in ("Five!", "Four!", "Three!", "Two!", "One!"):
        sc["ts"].append(T.mark("ding"))
        T.say("both", w, gap=0.1)
    sc["go_t"] = T.mark("blast")
    T.say("both", "Blast off!", gap=0.8)
    sc["kids_t"] = round(T.t, 3)
    T.end(sc)
    sc = T.scene("arrive", "space")
    sc["title_t"] = T.mark("slam")
    T.say("mishu", "We're going to space! Let's meet all eight planets!", gap=0.2)
    T.say("gul", "And the Sun, the Moon, and the stars! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ GET READY
    T.title("launch", "SPACE SUIT!", "gul", "Before we go to space, we need a space suit!")
    sc = T.scene("suit", "launch")
    sc["ts"] = []
    for k, (key, text) in enumerate(SUIT):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.3)
    sc["done_t"] = T.mark("tada")
    T.say("both", "We're astronauts!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ BUILD ROCKET
    T.title("launch", "BUILD A ROCKET!", "mishu", "Let's get our rocket ready!")
    sc = T.scene("build", "launch")
    sc["ts"] = []
    for k, (key, text) in enumerate(ROCKET):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.3)
    T.pause(0.4)
    T.end(sc)
    # ------------------------------------------------------------ THE SUN
    T.title("space", "THE SUN!", "gul", "First, the Sun! It's right in the middle!")
    sc = T.scene("sun", "space")
    sc["a"] = T.say("mishu", "The Sun is a star! A giant ball of very hot gas!", gap=0.3)
    sc["b"] = T.say("gul", "It gives us light and heat!", gap=0.3)
    sc["c"] = T.say("mishu", "Eight planets go around and around the Sun!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ EIGHT PLANETS
    T.title("space", "EIGHT PLANETS!", "mishu", "Let's meet all eight planets, one by one!")
    for k, (key, name, f1, f2, w) in enumerate(PLANETS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("planet", "space", key=key, name=name.upper(), w=w, num=k + 1)
        T.mark("whoosh")
        T.say(a, f"Planet number {NUM[k + 1]}!", gap=0.1)
        sc["name_t"] = T.say("both", f"{name}!", gap=0.05)
        T.prompts.append((round(T.t, 3), round(T.t + 1.0, 3)))
        T.pause(1.0)
        sc["f1_t"] = T.say(other(a), f1, gap=0.2)
        T.say(a, f2, gap=0.5)
        T.end(sc)
    sc = T.scene("lineup", "space")
    sc["ts"] = []
    for k, (key, name, *_) in enumerate(PLANETS):
        sc["ts"].append(T.mark("pop"))
        T.say("both", f"{name}!", gap=0.15)
    sc["sum_t"] = T.say("gul", "Eight planets! Say them again, faster!", gap=0.2)
    sc["ts2"] = [T.say("both", p[1], gap=0.0) for p in PLANETS]
    T.pause(0.5)
    T.end(sc)
    # ------------------------------------------------------------ BIG OR SMALL
    T.title("space", "BIG AND SMALL!", "gul", "Some planets are giants, and some are tiny!")
    sc = T.scene("sizes", "space")
    sc["a"] = T.say("mishu", "Jupiter is the biggest! More than a thousand Earths could fit inside!", gap=0.3)
    sc["b"] = T.say("gul", "Earth is much smaller!", gap=0.3)
    sc["c"] = T.say("mishu", "And Mercury is the smallest of all!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ ROCKY OR GIANT
    T.title("space", "ROCKY OR GIANT?", "mishu", "Four planets are small and rocky! Four are big giants!")
    for k, (key, rocky) in enumerate(ROCKY):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("rocky", "space", key=key, rocky=rocky)
        T.prompt(a, "Rocky, or giant?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), "Rocky!" if rocky else "Giant!", gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ HOT OR COLD
    T.title("space", "HOT OR COLD?", "gul", "Planets near the Sun can get hot! Far away, they are cold!")
    for k, (key, hot, text) in enumerate(HOTCOLD):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("hotcold", "space", key=key, hot=hot)
        T.prompt(a, "Hot, or cold?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ COLOURS
    T.title("space", "PLANET COLOURS!", "mishu", "Planets are so colourful! What colour is it?")
    for k, (key, col, text) in enumerate(PCOL):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("pcol", "space", key=key, col=col)
        T.prompt(a, "What colour is it?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ DAY AND NIGHT
    T.title("space", "DAY AND NIGHT!", "mishu", "Why do we have day and night? Because the Earth spins!")
    sc = T.scene("daynight", "space")
    sc["a"] = T.say("gul", "When our side faces the Sun, it's day time!", gap=0.3)
    sc["b"] = T.say("mishu", "When our side turns away, it's night time! Good night!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ WHICH PLANET
    T.title("space", "WHICH PLANET?", "gul", "Do you remember? Which planet is it?")
    for k, (q, key, ans) in enumerate(WHICH):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("which", "space", key=key, q=q.upper())
        T.prompt(a, q, wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ------------------------------------------------------------ WHAT COMES NEXT
    T.title("space", "WHAT COMES NEXT?", "mishu", "Big kids! Which planet comes next?")
    for k, (q, key, ans) in enumerate(ORDERQ):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("nextp", "space", key=key)
        T.say(a, q, gap=0.1)
        T.prompt(a, "What comes next?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MOON
    T.title("moonland", "THE MOON!", "gul", "Let's land on the Moon! Touch down!")
    for k, (text, key) in enumerate(MOON):
        sc = T.scene("moon", "space" if key in ("orbit", "craters") else "moonland", key=key)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.6)
        T.end(sc)
    sc = T.scene("walk", "moonland")
    T.say("both", "Let's jump on the Moon! Boing, boing!", gap=0.2)
    sc["b_t"] = T.mark("boing")
    T.say("mishu", "The Moon has less gravity, so you can jump very high!", gap=0.6)
    T.end(sc)
    # ------------------------------------------------------------ MOON SHAPES
    T.title("space", "MOON SHAPES!", "mishu", "The Moon looks different every night!")
    for k, (f, text) in enumerate(PHASES):
        sc = T.scene("phase", "space", f=f)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.6)
        T.end(sc)
    # ------------------------------------------------------------ FLOATING
    T.title("space", "FLOATING IN SPACE!", "gul", "Life in space is so funny!")
    for k, (key, text) in enumerate(FLOAT):
        sc = T.scene("float", "space", key=key)
        T.mark("whoosh")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.6)
        T.end(sc)
    # ------------------------------------------------------------ COUNT THE STARS
    T.title("space", "COUNT THE STARS!", "mishu", "So many stars! Let's count to ten!")
    sc = T.scene("count", "space")
    sc["cts"] = []
    for i in range(1, 11):
        sc["cts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
    sc["sum_t"] = T.say("gul", "Ten stars! There are more stars than we can ever count!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ CONNECT THE STARS
    T.title("space", "STAR PICTURES!", "gul", "Long ago, people joined stars to make pictures!")
    for k, (n, ans) in enumerate(STARS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("connect", "space", n=n)
        T.prompt(a, "Join the stars! What is it?", wait=2.2)
        sc["answer_t"] = T.mark("tada")
        T.say(other(a), ans, gap=0.6)
        T.end(sc)
    # ------------------------------------------------------------ TELESCOPE
    T.title("moonland", "LOOK THROUGH THE TELESCOPE!", "gul", "A telescope makes faraway things look close!")
    for k, (key, text) in enumerate(TELE):
        sc = T.scene("tele", "moonland", key=key)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.7)
        T.end(sc)
    # ------------------------------------------------------------ RHYME
    T.title("space", "PLANET RHYME!", "mishu", "Clap along with our planet rhyme!")
    sc = T.scene("chant", "space")
    sc["l"] = [T.say("both", ln, gap=0.25) for ln in RHYME * 2]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ SPACE OR NOT
    T.title("space", "SPACE OR NOT?", "mishu", "Does it go in space? Yes, or no?")
    for k, (key, good, q, ans) in enumerate(SORT):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sort", "space", key=key, good=good, q=q.upper())
        T.prompt(a, q, wait=1.6)
        sc["answer_t"] = T.mark("yes" if good else "buzz")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("space", "SPACE DANCE!", "gul", "Stand up! Let's do the space dance!")
    T.dance("space", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("space", "SPACE QUIZ!", "mishu", "Quick quiz time! Are you ready?")
    T.quiz("space", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "space")
    T.say("mishu", "Time to fly home to Earth! Thank you for coming to space!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, astronauts!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(24)


def sfx(kind):
    if kind == "buzz":
        t = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t)) * 0.3 * np.minimum(1, (0.4 - t) / 0.05), 0, 0.4)]
    if kind == "blast":
        t = M.tt(2.0)
        n = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
        n = np.convolve(n, np.ones(40) / 40, mode="same")
        return [(n * 7 * np.minimum(1, t / 0.15) * np.minimum(1, (2.0 - t) / 0.8), 0, 0.6)]
    return None


if __name__ == "__main__":
    T = build()
    tune = [72, 76, 79, 84, 83, 79, 76, 0, 74, 77, 81, 86, 84, 81, 77, 0]
    M.finish(T, music=dict(bpm=118, prog=[[60, 64, 67], [57, 60, 64], [65, 69, 72], [55, 59, 62]], hook=tune, start=4.0), sfx=sfx)
