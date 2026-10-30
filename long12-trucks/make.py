"""Long video 12: "Excavator & Construction Trucks". Voices, timeline.json, mix.wav (own music + own truck sounds).
python make.py
"""
import hashlib, json, sys, pathlib
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "voices"))
sys.path.insert(0, str(ROOT / "tools"))
_argv = sys.argv
import kidvoice
import loop_shorts as LS
import rhyme_v4 as RV
sys.argv = _argv

A, M = LS.A, LS.M
SR = A.SR
CACHE = HERE / "words"
CACHE.mkdir(exist_ok=True)
PRAISE = ["Great job!", "Yes! You got it!", "Awesome!", "Well done!", "Super!", "You're so smart!"]

TEAM = [  # truck, name, job, fact, action sound
    ("excavator", "excavator", "It digs big holes with its bucket. Dig, dig, dig!", "Excavators have tracks instead of wheels, so they never get stuck!", "dig"),
    ("dumptruck", "dump truck", "It carries dirt, and dumps it out. Dump!", "The biggest dump trucks have wheels taller than a grown-up!", "dump"),
    ("bulldozer", "bulldozer", "It pushes dirt with its big blade. Push, push, push!", "A bulldozer is super strong. It can push a giant pile of rocks!", "push"),
    ("mixer", "cement mixer", "Its drum spins round and round, to mix cement!", "The drum keeps spinning, so the cement doesn't get hard!", "spin"),
    ("crane", "crane truck", "It lifts heavy things, way up high!", "Cranes use a strong rope and a hook to lift things!", "lift"),
    ("roller", "road roller", "It rolls the ground flat and smooth. Roll, roll, roll!", "Its heavy drum makes new roads nice and flat!", "roll")]
BUILD = [("excavator", "First, the excavator digs the ground!", "dig"), ("dumptruck", "The dump truck takes the dirt away!", "dump"),
         ("bulldozer", "The bulldozer pushes the ground flat!", "push"), ("mixer", "The cement mixer pours the cement!", "spin"),
         ("crane", "The crane lifts the slide into place!", "lift"), ("roller", "The road roller makes a smooth path!", "roll")]
JOBS = [("Which truck digs big holes?", "excavator", ["bulldozer", "excavator", "mixer"], "The excavator!"),
        ("Which truck spins round and round?", "mixer", ["mixer", "roller", "dumptruck"], "The cement mixer!"),
        ("Which truck pushes dirt with a blade?", "bulldozer", ["crane", "excavator", "bulldozer"], "The bulldozer!"),
        ("Which truck lifts things up high?", "crane", ["crane", "dumptruck", "roller"], "The crane truck!"),
        ("Which truck dumps the dirt?", "dumptruck", ["roller", "dumptruck", "excavator"], "The dump truck!"),
        ("Which truck makes the road flat?", "roller", ["mixer", "bulldozer", "roller"], "The road roller!")]
CITY = [("garbage", "The garbage truck picks up all the trash! Crunch, crunch!", "crunch"),
        ("firetruck", "The fire truck rushes to put out fires! Nee naw, nee naw!", "siren"),
        ("towtruck", "The tow truck pulls broken cars to the garage!", "winch"),
        ("monster", "And the monster truck has giant wheels! It can jump! Wow!", "jump")]
SOUNDS = [("beep", "towtruck", "Beep, beep, beep! A truck backing up!"), ("siren", "firetruck", "Nee naw! The fire truck!"),
          ("crunch", "garbage", "Crunch! The garbage truck!"), ("horn", "dumptruck", "Honk honk! The dump truck!"),
          ("spin", "mixer", "Swish, swish! The cement mixer!"), ("jump", "monster", "Vroom! Boing! The monster truck!")]
PARTS = [("dumptruck", "cab", (150, 190), "This is the cab. The driver sits inside!"), ("dumptruck", "wheels", (560, 340), "These are wheels. They go round and round!"),
         ("excavator", "bucket", (-60, 300), "This is the bucket. It scoops up dirt!"), ("excavator", "tracks", (370, 340), "These are tracks. They roll over bumpy ground!"),
         ("bulldozer", "blade", (100, 270), "This is the blade. It pushes big piles!"), ("mixer", "drum", (480, 215), "This is the drum. It spins to mix cement!"),
         ("crane", "hook", (308, 40), "This is the hook. It holds heavy things!")]
TREASURE = [("fossil", "A dinosaur fossil! Wow!"), ("coin", "A shiny gold coin!"), ("ball", "A lost ball!"), ("key", "An old key!"),
            ("bone", "A big bone! Woof woof!"), ("egg", "A spotty dinosaur egg!")]
OPPS = [("crane", "up", "down", "The crane lifts things up, and puts them down!"), ("dumptruck", "full", "empty", "The dump truck is full, then empty!"),
        ("monster", "fast", "slow", "The monster truck is fast! The road roller is slow!")]
SAY = {"excavator": "excavator", "firetruck": "fire truck", "garbage": "garbage truck", "towtruck": "tow truck", "monster": "monster truck", "roller": "road roller", "crane": "crane truck"}
COLOURS = [("excavator", "yellow"), ("firetruck", "red"), ("garbage", "green"), ("towtruck", "blue"), ("monster", "purple"), ("roller", "green"), ("crane", "orange")]
WHEELS_Q = [("dumptruck", 3, "Three wheels!"), ("monster", 2, "Two giant wheels!"), ("towtruck", 3, "Three wheels!"), ("roller", 1, "One wheel, and one big drum!")]
BIGSMALL = [("Which truck is bigger?", ("dumptruck", "toytruck"), 0, "The dump truck is bigger!"),
            ("Which wheels are bigger?", ("monster", "car"), 0, "The monster truck wheels!"),
            ("Which one is smaller?", ("crane", "toytruck"), 1, "The toy truck is smaller!")]
FIX = [("excavator", "Oh no! A big hole in the road! The excavator digs out the broken bits.", "dig"),
       ("dumptruck", "The dump truck brings new gravel. Dump!", "dump"),
       ("roller", "The road roller makes it flat and smooth. Roll, roll!", "roll")]
COUNT = ["excavator", "dumptruck", "bulldozer", "mixer", "crane", "roller", "garbage", "towtruck", "monster", "firetruck"]
DANCE = [("Dig, dig, dig like an excavator!", "dig"), ("Push, push like a bulldozer!", "push"), ("Spin around like a mixer!", "spin"),
         ("Lift up high like a crane!", "lift"), ("Beep, beep, back up!", "back"), ("Honk, honk! Jump!", "honk")]
QUIZ = [("Which truck digs big holes?", "The excavator!", "excavator"), ("What does a cement mixer do?", "It mixes cement!", "mixer"),
        ("What do builders wear on their heads?", "A hard hat!", "hardhat"), ("Which truck lifts heavy things?", "The crane!", "crane"),
        ("Which truck pushes dirt with a big blade?", "The bulldozer!", "bulldozer"), ("Should we play near big trucks?", "No! Stay far away, with a grown-up!", "cone"),
        ("Where does the driver sit?", "In the cab!", "dumptruck"), ("What colour is the fire truck?", "Red!", "firetruck"),
        ("Which truck has giant wheels?", "The monster truck!", "monster"), ("What does a road roller make?", "Flat, smooth roads!", "roller")]


def line(who, text):
    c = kidvoice.CHARACTERS[who]
    p = CACHE / f"{who}_{hashlib.md5((who + text + str(c)).encode()).hexdigest()[:10]}.wav"
    if not p.exists():
        kidvoice.say_as(who, text, p)
    x, sr = sf.read(p)
    idx = np.where(np.abs(x) > 0.03 * np.abs(x).max())[0]
    return x[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.05 * sr)]


class TL:
    def __init__(self):
        self.t, self.lines, self.scenes, self.voc, self.prompts, self.stars, self.fx = 0.0, [], [], {"gul": [], "mishu": []}, [], [], []

    def say(self, who, text, gap=0.3):
        singers = ["gul", "mishu"] if who == "both" else [who]
        d = 0
        for s in singers:
            x = line(s, text)
            self.voc[s].append((self.t, x * ((0.9 if s == "mishu" else 0.45) if who == "both" else 1.0)))
            d = max(d, len(x) / SR)
        start = round(self.t, 3)
        self.lines.append(dict(who=who, text=text, t=start, dur=round(d, 3)))
        self.t += d + gap + 0.15
        return start

    def pause(self, s):
        self.t += s

    def scene(self, kind, bg, **data):
        sc = dict(kind=kind, bg=bg, t0=round(self.t, 3), **data)
        self.scenes.append(sc)
        return sc

    def end(self, sc):
        sc["t1"] = round(self.t, 3)

    def prompt(self, who, text, wait=2.3):
        self.say(who, text, gap=0.1)
        self.prompts.append((round(self.t, 3), round(self.t + wait, 3)))
        self.pause(wait)

    def mark(self, kind):
        self.fx.append((kind, round(self.t, 3)))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("riser")
        self.pause(0.5)
        self.say(who, text, gap=0.3)
        self.end(sc)


def other(w):
    return "mishu" if w == "gul" else "gul"


def build():
    T = TL()
    # ---------------------------------------------------------------- OPENING: excavator SMASHES into the dirt
    sc = T.scene("intro", "site")
    sc["engine_t"] = T.mark("engine")
    T.pause(0.5)
    sc["smash_t"] = T.mark("smash")
    T.pause(1.0)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Big trucks!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Put on your hard hat! Let's build something!", gap=0.2)
    T.say("gul", "Dig, dump, push, and lift! Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- MEET THE TEAM
    T.title("site", "MEET THE TRUCKS!", "gul", "Here comes the construction team!")
    for k, (key, name, job, fact, snd) in enumerate(TEAM):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("team", "site", key=key, name=name, act=snd, num=k + 1)
        sc["in_t"] = T.mark("engine")
        T.pause(1.0)
        sc["name_t"] = T.say(a, f"This is {'an' if name[0] in 'aeiou' else 'a'} {name}!", gap=0.1)
        sc["act_t"] = T.mark(snd)
        T.say(other(a), job, gap=0.2)
        T.say(a, fact, gap=0.1)
        T.prompt(other(a), f"Say {name}!", wait=1.3)
        T.end(sc)
    # ---------------------------------------------------------------- BUILD A PLAYGROUND (story)
    T.title("site", "LET'S BUILD A PLAYGROUND!", "mishu", "The trucks work together! Let's build a playground!")
    for k, (key, text, snd) in enumerate(BUILD):
        sc = T.scene("build", "site", key=key, step=k, act=snd)
        sc["in_t"] = T.mark("engine")
        T.pause(0.8)
        sc["act_t"] = T.mark(snd)
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=1.0)
        T.end(sc)
    sc = T.scene("playground", "park")
    sc["reveal_t"] = T.mark("tada")
    T.say("both", "Ta-da! A brand new playground!", gap=0.2)
    T.say("mishu", "Thank you, trucks! Let's play!", gap=0.6)
    T.stars.append(sc["reveal_t"])
    T.end(sc)
    # ---------------------------------------------------------------- TRUCK PARTS
    T.title("site", "TRUCK PARTS!", "mishu", "Let's look closely! What are the parts of a truck?")
    for k, (key, part, xy, text) in enumerate(PARTS):
        sc = T.scene("part", "site", key=key, part=part, xy=list(xy))
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.2)
        T.say("both", f"{part.capitalize()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- DIG FOR TREASURE
    T.title("site", "DIG FOR TREASURE!", "gul", "The excavator is digging! What will it find?")
    for k, (key, text) in enumerate(TREASURE):
        sc = T.scene("treasure", "site", key=key)
        sc["dig_t"] = T.mark("dig")
        T.prompt("mishu" if k % 2 == 0 else "gul", "Dig, dig! What did it find?", wait=1.4)
        sc["find_t"] = T.mark("yes")
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.4)
        T.stars.append(sc["find_t"])
        T.end(sc)
    # ---------------------------------------------------------------- LOAD THE DUMP TRUCK (count)
    sc = T.scene("load", "site")
    T.say("mishu", "Let's load the dump truck with rocks! Count with us!", gap=0.1)
    lts = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!"):
        lts.append(T.mark("dirtdrop"))
        T.say("both", w, gap=0.25)
    sc["lts"] = lts
    sc["go_t"] = T.mark("engine")
    T.say("gul", "Five rocks! The dump truck is full! Vroom!", gap=0.6)
    T.end(sc)
    # ---------------------------------------------------------------- WHO DOES THIS JOB?
    T.title("site", "WHICH TRUCK?", "gul", "Big kids! Which truck does this job?")
    for k, (q, ans, opts, line_) in enumerate(JOBS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("job", "site", q=q.upper(), ans=ans, opts=opts)
        T.mark("ding")
        T.prompt(a, q, wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), line_, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- CITY TRUCKS
    T.title("city", "CITY TRUCKS!", "mishu", "Now let's meet the trucks in the city!")
    for k, (key, text, snd) in enumerate(CITY):
        sc = T.scene("city", "city", key=key, act=snd)
        sc["in_t"] = T.mark("engine")
        T.pause(0.9)
        sc["act_t"] = T.mark(snd)
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- FIX THE ROAD (story 2)
    T.title("city", "FIX THE ROAD!", "gul", "Uh oh! The cars can't drive. Trucks to the rescue!")
    for k, (key, text, snd) in enumerate(FIX):
        sc = T.scene("fix", "city", key=key, step=k, act=snd)
        sc["in_t"] = T.mark("engine")
        T.pause(0.8)
        sc["act_t"] = T.mark(snd)
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.8)
        T.end(sc)
    sc = T.scene("fixdone", "city")
    sc["done_t"] = T.mark("horn_short")
    T.say("both", "The road is fixed! Beep beep! Cars can drive again!", gap=0.6)
    T.stars.append(sc["done_t"])
    T.end(sc)
    # ---------------------------------------------------------------- WHAT COLOUR?
    T.title("city", "WHAT COLOUR?", "mishu", "Trucks come in lots of colours! What colour is it?")
    for k, (key, col) in enumerate(COLOURS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("colour", "city", key=key, col=col)
        T.mark("pop")
        T.prompt(a, f"What colour is the {SAY[key]}?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{col.capitalize()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- COUNT THE WHEELS
    T.title("site", "COUNT THE WHEELS!", "gul", "How many wheels can you see?")
    for k, (key, n, ans) in enumerate(WHEELS_Q):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("wheels", "site", key=key, n=n)
        T.prompt(a, "How many wheels?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BIG OR SMALL
    for k, (q, pair, ans, text) in enumerate(BIGSMALL):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("bigsmall", "site", pair=list(pair), ans=ans)
        T.prompt(a, q, wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- COUNT THE TRUCKS
    T.title("city", "COUNT THE TRUCKS!", "gul", "Here comes a truck parade! Let's count!")
    sc = T.scene("count", "city")
    cts = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!", "Six!", "Seven!", "Eight!", "Nine!", "Ten!"):
        cts.append(T.mark("horn_short"))
        T.say("both", w, gap=0.25)
    sc["cts"] = cts
    T.say("mishu", "Ten trucks! What a big parade!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- TRUCK SOUNDS
    T.title("city", "WHICH TRUCK IS IT?", "mishu", "Listen carefully! Which truck makes this sound?")
    for k, (snd, key, ans) in enumerate(SOUNDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sound", "city", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.6)
        T.prompt(a, "Which truck is it?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- TRUCK OPPOSITES
    T.title("site", "TRUCK OPPOSITES!", "mishu", "Big kids! Trucks can show us opposites!")
    for k, (key, w1, w2, text) in enumerate(OPPS):
        sc = T.scene("opps", "site", key=key, w1=w1, w2=w2)
        sc["a_t"] = T.say("gul" if k % 2 == 0 else "mishu", f"{w1.capitalize()}!", gap=0.6)
        sc["b_t"] = T.say("mishu" if k % 2 == 0 else "gul", f"{w2.capitalize()}!", gap=0.3)
        T.say("both", text, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- SAFETY
    sc = T.scene("safety", "city")
    sc["s1"] = T.say("gul", "Big trucks are so cool! But drivers can't always see little kids.", gap=0.2)
    sc["s2"] = T.say("mishu", "So stay far away from big trucks, and hold a grown-up's hand.", gap=0.2)
    sc["s3"] = T.say("both", "And wave to the driver from the sidewalk! Hello!", gap=0.6)
    T.end(sc)
    # ---------------------------------------------------------------- TRUCK DANCE x2
    T.title("site", "TRUCK DANCE!", "gul", "Stand up! Let's move like trucks! Copy us!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "site", title="FASTER!")
            T.mark("riser")
            T.say("mishu", "Again, faster!", gap=0.2)
            T.end(sc)
        for text, move in DANCE:
            sc = T.scene("dance", "site", move=move, fast=rnd == 1, word=text.split("!")[0].split(" like")[0].upper() + "!")
            T.mark("horn_short" if move == "honk" else ("beep" if move == "back" else "pop"))
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- QUIZ
    T.title("site", "TRUCK QUIZ!", "mishu", "Big kids quiz! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("quiz", "site", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "park")
    T.say("mishu", "Which truck is your favourite?", gap=0.2)
    T.say("gul", "Mine is the excavator! Dig, dig, dig!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends! Beep beep!", gap=1.8)
    T.end(sc)

    total = round(T.t, 2)
    n = int(total * SR)
    tracks = {}
    for s, items in T.voc.items():
        y = np.zeros(n)
        for at, x in items:
            i = int(at * SR)
            y[i:i + len(x)] += x[: n - i]
        tracks[s] = y
        sf.write(HERE / f"vocal_{s}.wav", (y / max(1e-9, np.abs(y).max()) * 0.9).astype(np.float32), SR, subtype="PCM_16")
    json.dump(dict(lines=T.lines, scenes=T.scenes, prompts=T.prompts, stars=T.stars, total=total), open(HERE / "timeline.json", "w"), indent=1)
    sf.write(HERE / "mix.wav", mixdown(T, tracks, total).astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s ({total / 60:.1f} min), {len(T.lines)} lines, {len(T.scenes)} scenes")


# ==================================================================== music + truck sounds (all made in code)
rng = np.random.default_rng(12)


def tt_(d):
    return np.arange(int(d * SR)) / SR


def noise(d, lp=1):
    x = rng.standard_normal(int(d * SR))
    return np.convolve(x, np.ones(lp) / lp, mode="same") if lp > 1 else x


def engine(d=1.4):
    t = tt_(d)
    f = 45 + 20 * np.minimum(1, t / 0.6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sign(np.sin(2 * np.pi * np.cumsum(f * 2) / SR)) * 0.3
    return x * (0.7 + 0.3 * np.sin(2 * np.pi * 11 * t)) * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.4) * 0.6


def clank():
    t = tt_(0.25)
    return sum(np.sin(2 * np.pi * f * t) * g for f, g in ((620, 0.5), (1430, 0.3), (2100, 0.2))) * np.exp(-t / 0.05)


def dirt(d=0.8):
    t = tt_(d)
    return noise(d, 12) * 2.5 * np.exp(-t / 0.25)


def whirr(d=1.4, f0=180, f1=260):
    t = tt_(d)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * t / d) / SR)) * 0.2 + noise(d, 20)[:len(t)] * 0.8
    return np.convolve(x, np.ones(16) / 16, mode="same") * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.2)


def beep():
    out = []
    for k in range(3):
        t = tt_(0.22)
        out += [np.sign(np.sin(2 * np.pi * 1040 * t)) * 0.3 * np.minimum(1, (0.22 - t) / 0.02), np.zeros(int(0.22 * SR))]
    return np.concatenate(out)


def horn(d=0.5):
    t = tt_(d)
    x = sum(np.sign(np.sin(2 * np.pi * f * t)) * g for f, g in ((311, 0.25), (392, 0.2)))
    return np.convolve(x, np.ones(6) / 6, mode="same") * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)


def siren(d=1.6):
    t = tt_(d)
    f = np.where((t * 2.5) % 1 < 0.5, 740, 990)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.1)


def crunch():
    out = np.zeros(int(0.9 * SR))
    for k in range(8):
        n = int(0.06 * SR)
        x = np.diff(np.concatenate([[0], rng.standard_normal(n)])) * np.exp(-np.arange(n) / SR / 0.02)
        a = int(rng.uniform(0, 0.6) * SR)
        out[a:a + n] += x * 1.2
    return out


def act_sound(kind):
    if kind == "dig":
        return whirr(0.6), [(clank(), 0.6), (dirt(), 0.65)]
    if kind == "dump":
        return whirr(1.0, 140, 200), [(dirt(1.2) * 1.2, 0.9)]
    if kind == "push":
        return engine(1.6), [(dirt(1.0), 0.4)]
    if kind == "spin":
        t = tt_(1.8)
        return noise(1.8, 30) * 1.8 * (0.6 + 0.4 * np.sin(2 * np.pi * 2 * t)) * np.minimum(1, t / 0.2) * np.minimum(1, (1.8 - t) / 0.3), []
    if kind == "lift":
        return whirr(1.6, 300, 420), [(clank(), 1.5)]
    if kind == "roll":
        return engine(1.8), []
    if kind == "crunch":
        return crunch(), []
    if kind == "siren":
        return siren(), []
    if kind == "winch":
        return whirr(1.4, 220, 160), [(clank(), 1.3)]
    if kind == "jump":
        t = tt_(0.5)
        return engine(0.8), [(M.boing(), 0.7), (np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.1), 1.4)]
    return np.zeros(10), []


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 120
    prog = [[65, 69, 72], [62, 65, 69], [58, 62, 65], [60, 64, 67]]           # F Dm Bb C: strong, sunny
    hook = [77, 77, 81, 84, 81, 0, 79, 77, 76, 79, 84, 0, 81, 79, 77, 0]
    bar, t0 = 0, 3.3
    while t0 < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = t0 + q * B
            A.add(mus, LS.kick() * 1.1, b0, 0.5)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.3, 0.05)
                A.add(mus, RV.snare(), b0, 0.18)
            A.add(mus, LS.hat(), b0 + B / 2, 0.45, -0.3)
            A.add(mus, clank() * 0.25, b0 + B * 0.75, 0.08, 0.35)                   # little metal clank, like a tool
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.3)
            for j, nt in enumerate(ch):
                A.add(mus, A.tone(A.mtof(nt + 12), 0.28, ((1, 1), (3, 0.3), (5, 0.12)), 0.004, 0.1), b0 + B / 2, 0.045, -0.25 + 0.25 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, RV.lead(mm, B * 0.45), t0 + i * B / 2, 0.05, 0.2)
        t0 += 4 * B
        bar += 1
    ts = np.arange(n) / SR
    mus *= np.clip((total - ts) / 1.5, 0, 1)[:, None]
    g = np.ones(n)
    for s in T.scenes:
        if s["kind"] == "sound":
            a, b = int((s["snd_t"] - 0.3) * SR), int((s["snd_t"] + 1.8) * SR)
            g[a:b] = 0.15
    g = np.convolve(g, np.ones(SR // 3) / (SR // 3), mode="same")
    mus *= g[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.12)
    A.add(v, tracks["mishu"], 0, 1.0, 0.12)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.5 * e)[:, None]
    f = np.zeros((n, 2))
    for kind, at in T.fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.35)
        elif kind == "engine":
            A.add(f, engine(), at, 0.5)
        elif kind == "smash":
            A.add(f, LS.kick() * 1.4, at, 0.9)
            A.add(f, clank(), at, 0.6)
            A.add(f, dirt(1.0), at + 0.02, 0.8)
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "tada":
            A.add(f, A.sfx_sparkle(), at, 0.6)
            for k in range(4):
                A.add(f, M.clap(), at + 0.2 + k * 0.25, 0.4)
        elif kind == "beep":
            A.add(f, beep(), at, 0.45)
        elif kind == "horn":
            A.add(f, horn(0.4), at, 0.55)
            A.add(f, horn(0.7), at + 0.55, 0.55)
        elif kind == "horn_short":
            A.add(f, horn(0.25), at, 0.35)
        elif kind == "dirtdrop":
            A.add(f, clank(), at + 0.3, 0.4)
            A.add(f, dirt(0.4), at + 0.32, 0.4)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "yes":
            A.add(f, A.sfx_ding(79), at, 0.2)
            A.add(f, A.sfx_ding(84), at + 0.12, 0.2)
        else:
            main, extra = act_sound(kind)
            A.add(f, main, at, 0.5)
            for x, off in extra:
                A.add(f, x, at + off, 0.55)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.15)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(86), p0, 0.1)
    mix = v + mus * 0.33 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    return mix


if __name__ == "__main__":
    build()
