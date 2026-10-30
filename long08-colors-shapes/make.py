"""Long video 8: "Colors & Shapes for Kids". Voices, timeline.json, mix.wav (own music + own sounds).
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

COLORS = [  # colour, object art, reveal line, fact line
    ("red", "firetruck", "A red fire truck! Nee naw, nee naw!", "Red means stop at the traffic light!"),
    ("orange", "pumpkinveg", "An orange pumpkin!", "Orange is warm, like the sunset!"),
    ("yellow", "duckling", "A yellow duckling! Quack quack!", "Yellow is bright, like the sunshine!"),
    ("green", "frog", "A green frog! Ribbit!", "Grass and leaves are green too!"),
    ("blue", "whale", "A blue whale! Splash!", "The sky and the sea look blue!"),
    ("purple", "eggplant", "A purple eggplant!", "Purple is a color for kings and queens!"),
    ("pink", "piglet", "A pink piglet! Oink oink!", "Pink is a light, soft red!"),
    ("brown", "cupcake", "A brown chocolate cupcake! Yum!", "Tree trunks are brown too!"),
    ("black", "tophat", "A black magic hat!", "The night sky is black!"),
    ("white", "snowman", "A white snowman! Brrr!", "Snow and clouds are white!"),
]
MIXES = [("red", "yellow", "orange"), ("blue", "yellow", "green"), ("red", "blue", "purple"), ("red", "white", "pink"), ("black", "white", "grey")]
TRAIN = [("tomato", "red", "tomato"), ("corn", "yellow", "corn"), ("broccoli", "green", "broccoli"), ("blueberries", "blue", "blueberries"),
         ("duckling", "yellow", "duckling"), ("strawberry", "red", "strawberry"), ("whale", "blue", "whale"), ("frog", "green", "frog")]
SHAPES = [  # shape, sides to count (0 = none), count line, example art, example line, draw-in-the-air prompt
    ("circle", 0, "A circle is round. It has no corners at all!", "clock", "A clock is a circle!", True),
    ("square", 4, "Four sides, all the same! One, two, three, four!", "window", "This window is a square!", True),
    ("triangle", 3, "Let's count the sides! One, two, three!", "pizza", "A pizza slice is a triangle!", True),
    ("rectangle", 4, "Four sides! Two long, and two short!", "book", "A book is a rectangle!", False),
    ("oval", 0, "An oval is round, and long, like an egg!", "egg", "An egg is an oval!", False),
    ("star", 5, "A star has five points! One, two, three, four, five!", "starfish", "A starfish is a star!", True),
    ("heart", 0, "A heart means love! Two bumps on top!", "heartcookie", "This cookie is a heart! Yum!", False),
    ("diamond", 4, "A diamond has four sides! It stands on its tip!", "kite", "A kite is a diamond!", False),
    ("pentagon", 5, "Five sides! One, two, three, four, five!", "birdhouse", "A birdhouse is a pentagon!", False),
    ("hexagon", 6, "Six sides! One, two, three, four, five, six!", "honeycomb", "Bees make hexagons in their honeycomb!", False),
    ("crescent", 0, "A crescent is a thin curve, like a smile!", "moon", "The moon can look like a crescent!", False),
]
HUNT = [("triangle", "The roof is a triangle!"), ("square", "The window is a square!"), ("rectangle", "The door is a rectangle!"),
        ("circle", "The sun is a circle!"), ("diamond", "The kite is a diamond!"), ("oval", "The pond is an oval!")]
BUILDS = [("house", "A big square, a triangle on top, and a rectangle door.", "A house!"),
          ("rocket", "A long rectangle, three triangles, and a circle window.", "A rocket! Blast off!"),
          ("car", "Two rectangles, and two circles.", "A car! Beep beep!"),
          ("icecream", "A triangle, and three circles on top.", "An ice cream! Yummy!"),
          ("fish", "An oval, a triangle, and a little circle.", "A fish! Swim, swim!")]
SOLIDS = [("sphere", "circle", "ball", "This is a sphere.", "A ball is a sphere! It can roll!"),
          ("cube", "square", "dice", "This is a cube.", "A dice is a cube! It has six square faces!"),
          ("cone", "triangle", "trafficcone", "This is a cone.", "A traffic cone is a cone!"),
          ("cylinder", "rectangle", "drum", "This is a cylinder.", "A drum is a cylinder! Boom boom!"),
          ("pyramid3d", "triangle", "pyramidegypt", "This is a pyramid.", "The big pyramids in Egypt are this shape!")]
PATTERNS = [([("circle", "red"), ("square", "blue"), ("circle", "red"), ("square", "blue")], ("circle", "red"), "Red circle!"),
            ([("star", "yellow"), ("star", "yellow"), ("triangle", "green"), ("star", "yellow"), ("star", "yellow")], ("triangle", "green"), "Green triangle!"),
            ([("circle", "red"), ("triangle", "yellow"), ("square", "blue"), ("circle", "red"), ("triangle", "yellow")], ("square", "blue"), "Blue square!")]
DANCE = [("Make a big circle with your arms!", "circle", "sway"), ("Hands up high, make a triangle!", "triangle", "pop"),
         ("Jump, jump, like a star!", "star", "jump"), ("Draw a square in the air!", "square", "slow"),
         ("Wiggle, wiggle, like a rainbow!", "rainbow", "shake"), ("Make a heart with your hands!", "heart", "sway")]
QUIZ = [("How many sides does a triangle have?", "Three sides!", ("shape", "triangle")),
        ("What do red and yellow make?", "Orange!", ("blob", "orange")),
        ("Which shape has no corners?", "A circle!", ("shape", "circle")),
        ("What shape is a pizza slice?", "A triangle!", ("item", "pizza")),
        ("How many colors are in a rainbow?", "Seven colors!", ("rainbow", "")),
        ("What do blue and yellow make?", "Green!", ("blob", "green")),
        ("What shape is a ball?", "A sphere!", ("item", "sphere"))]


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

    def mark(self, kind, dur=0.0):
        self.fx.append((kind, round(self.t, 3), dur))
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
    # ---------------------------------------------------------------- OPENING: paint splats, shapes rain, title slam
    sc = T.scene("intro", "studio")
    splats = []
    for c in ("red", "yellow", "blue", "green", "pink", "orange"):
        splats.append((T.mark("splat"), c))
        T.pause(0.33)
    sc["splats"] = splats
    sc["title_t"] = T.mark("slam")
    T.say("both", "Colors and shapes!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Today we'll draw, mix, build, and play!", gap=0.2)
    T.say("gul", "Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- CRAYON SURPRISE (10 colours, new objects)
    T.title("studio", "CRAYON SURPRISE!", "gul", "Magic crayons! What will they draw? Let's see!")
    for k, (col, art, reveal, fact) in enumerate(COLORS):
        a = "mishu" if k % 2 else "gul"
        sc = T.scene("crayon", "studio", col=col, art=art, num=k + 1)
        d0 = T.t
        T.mark("scribble", 2.2)
        T.say(a, f"{col.capitalize()} crayon! What will it draw?", gap=0.0)
        T.t = max(T.t, d0 + 2.4)
        sc["pop_t"] = T.mark("reveal")
        T.pause(0.3)
        T.say(other(a), reveal, gap=0.2)
        T.say(a, fact, gap=0.1)
        T.prompt(other(a), f"Say {col}!", wait=1.3)
        T.stars.append(round(T.t - 1.0, 3))
        T.end(sc)
    # ---------------------------------------------------------------- MIXING LAB
    T.title("studio", "MIX THE COLORS!", "mishu", "Now let's be scientists, and mix paint!")
    sc = T.scene("primary", "studio")
    sc["show_t"] = T.mark("pop")
    T.say("gul", "Red, yellow, and blue are primary colors.", gap=0.2)
    T.say("mishu", "We can mix them to make new colors! Watch!", gap=0.4)
    T.end(sc)
    for k, (c1, c2, res) in enumerate(MIXES):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("mix", "studio", c1=c1, c2=c2, res=res)
        sc["pour1_t"] = T.mark("pour")
        T.say(a, f"{c1.capitalize()} paint...", gap=0.5)
        sc["pour2_t"] = T.mark("pour")
        T.say(other(a), f"and {c2} paint!", gap=0.3)
        sc["swirl_t"] = T.mark("swirl")
        T.say("both", "Mix, mix, mix!", gap=0.1)
        T.prompt(a, "What color did we make?", wait=2.0)
        sc["reveal_t"] = T.mark("yes")
        T.say(other(a), f"It's {res}!", gap=0.2)
        T.say(a, f"{c1.capitalize()} and {c2} make {res}!" if k < 4 else "Black and white make grey, like an elephant!", gap=0.5)
        T.stars.append(sc["reveal_t"])
        T.end(sc)
    # ---------------------------------------------------------------- RAINBOW
    sc = T.scene("rainbow", "sky")
    T.mark("riser")
    T.say("gul", "Look up! A rainbow!", gap=0.2)
    T.say("mishu", "Say the rainbow colors with us!", gap=0.2)
    arcs = []
    for c in ("Red!", "Orange!", "Yellow!", "Green!", "Blue!", "Indigo!", "Violet!"):
        T.mark("note")
        arcs.append(T.say("both", c, gap=0.15))
    sc["arcs"] = arcs
    sc["fact_t"] = T.say("mishu", "A rainbow has seven colors!", gap=0.2)
    T.say("gul", "Rainbows come when the sun shines through the rain!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- COLOR TRAIN (sorting game)
    T.title("track", "COLOR TRAIN!", "mishu", "Choo choo! The color train is here!")
    sc = T.scene("train", "track", phase="in")
    T.mark("choo")
    T.say("gul", "Put each thing in the wagon with the same color!", gap=0.5)
    T.end(sc)
    loaded = []
    for k, (art, col, name) in enumerate(TRAIN):
        a = "mishu" if k % 2 else "gul"
        sc = T.scene("train", "track", phase="load", art=art, col=col, loaded=list(loaded))
        T.mark("pop")
        T.prompt(a, f"Where does the {name} go?", wait=1.8)
        sc["answer_t"] = T.mark("whoosh")
        T.say(other(a), f"The {col} wagon!", gap=0.4)
        loaded.append((art, col))
        T.end(sc)
    sc = T.scene("train", "track", phase="out", loaded=list(loaded))
    T.mark("choo")
    T.say("both", "All aboard! Choo choo!", gap=1.2)
    T.end(sc)
    # ---------------------------------------------------------------- MEET THE SHAPES (sides, corners, real things)
    T.title("board", "MEET THE SHAPES!", "gul", "Shapes are everywhere! Let's meet them!")
    for k, (shp, n, count_line, ex, ex_line, air) in enumerate(SHAPES):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("shape", "board", shape=shp, n=n, ex=ex, num=k + 1)
        T.mark("pop")
        T.pause(0.2)
        sc["name_t"] = T.say(a, f"This is a {shp}!", gap=0.2)
        sc["count_t"] = T.say(other(a), count_line, gap=0.2)
        sc["ex_t"] = T.mark("whoosh")
        T.say(a, ex_line, gap=0.2)
        if air:
            sc["air_t"] = round(T.t, 3)
            T.prompt(other(a), f"Draw a {shp} in the air with your finger!", wait=2.0)
        T.end(sc)
    # ---------------------------------------------------------------- SHAPE HUNT
    T.title("street", "SHAPE HUNT!", "mishu", "Shapes are hiding outside! Can you find them?")
    for k, (shp, found) in enumerate(HUNT):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("hunt", "street", shape=shp)
        T.mark("ding")
        T.prompt(a, f"Can you find a {shp}?", wait=2.2)
        sc["found_t"] = T.mark("yes")
        T.say(other(a), found, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BUILD WITH SHAPES
    T.title("studio", "BUILD WITH SHAPES!", "gul", "Let's put shapes together, and make a picture!")
    for k, (thing, pieces, ans) in enumerate(BUILDS):
        a = "mishu" if k % 2 else "gul"
        sc = T.scene("build", "studio", thing=thing)
        sc["build_t"] = T.mark("build", {"house": 5, "rocket": 5, "car": 4, "icecream": 4, "fish": 3}[thing])
        T.say(a, pieces, gap=0.3)
        T.t = max(T.t, sc["build_t"] + 3.2)
        T.prompt(other(a), "What did we make?", wait=1.8)
        sc["reveal_t"] = T.mark("yes")
        T.say(a, ans, gap=0.5)
        T.stars.append(sc["reveal_t"])
        T.end(sc)
    # ---------------------------------------------------------------- 3D SHAPES (big kids)
    T.title("board", "3D SHAPES!", "mishu", "Big kids! Some shapes are flat, and some are 3D, like real things!")
    for k, (solid, flat, ex, name_line, ex_line) in enumerate(SOLIDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("solid", "board", solid=solid, flat=flat, ex=ex)
        sc["pop_t"] = T.mark("boing")
        T.pause(0.6)
        T.say(a, name_line, gap=0.2)
        sc["ex_t"] = T.mark("whoosh")
        T.say(other(a), ex_line, gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- PATTERNS
    T.title("board", "WHAT COMES NEXT?", "gul", "Patterns repeat, again and again. What comes next?")
    for k, (seq, ans, ans_line) in enumerate(PATTERNS):
        a = "mishu" if k % 2 else "gul"
        sc = T.scene("pattern", "board", seq=seq, ans=ans)
        names = ", ".join(f"{c} {s}" for s, c in seq)
        sc["read_t"] = T.say(a, names + "...", gap=0.1)
        T.prompt(other(a), "What comes next?", wait=2.2)
        sc["answer_t"] = T.mark("yes")
        T.say(a, ans_line, gap=0.2)
        T.say(other(a), PRAISE[k], gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- SHAPE DANCE (copy-along), twice
    T.title("sky", "SHAPE DANCE!", "mishu", "Stand up! Let's dance with shapes! Copy us!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "sky", title="FASTER!")
            T.mark("riser")
            T.say("gul", "Now faster!", gap=0.2)
            T.end(sc)
        for text, shp, move in DANCE:
            sc = T.scene("dance", "sky", shape=shp, move=move, fast=rnd == 1)
            T.mark("stomp2" if move == "jump" else "pop")
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- BIG KIDS QUIZ
    T.title("studio", "BIG KIDS QUIZ!", "gul", "Quiz time! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("quiz", "studio", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "sky")
    T.say("mishu", "Look around your home! Can you find a circle? Something red?", gap=0.2)
    T.say("gul", "Colors and shapes are everywhere!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends!", gap=1.8)
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


# ==================================================================== music + sounds (all made in code)
rng = np.random.default_rng(48)


def noise(d, lp):
    return np.convolve(rng.standard_normal(int(d * SR)), np.ones(lp) / lp, mode="same")


def env_t(d, a, dec):
    t = np.arange(int(d * SR)) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)


def splat():
    d = 0.35
    m = int(d * SR)
    t = np.arange(m) / SR
    thump = np.sin(2 * np.pi * (140 - 200 * t) * t) * np.exp(-t / 0.05)
    return thump * 0.9 + noise(d, 10)[:m] * env_t(d, 0.003, 0.06) * 2.5


def scribble(d):
    m = int(d * SR)
    t = np.arange(m) / SR
    x = noise(d, 3)[:m] * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 3.2 * t))) * 0.8
    return x * np.minimum(1, (d - t) / 0.1)


def pour():
    d = 1.1
    m = int(d * SR)
    out = np.zeros(m)
    for j in range(9):
        a = int(j * 0.11 * SR + rng.uniform(0, 0.04) * SR)
        f0 = rng.uniform(300, 700)
        tt = np.arange(int(0.09 * SR)) / SR
        b = np.sin(2 * np.pi * (f0 + 2500 * tt) * tt) * np.exp(-tt / 0.03)
        out[a:a + len(b)] += b[: m - a] * 0.5
    return out + noise(d, 30)[:m] * 1.5 * np.sin(np.linspace(0, np.pi, m))


def swirl():
    d = 1.4
    m = int(d * SR)
    t = np.arange(m) / SR
    return np.sin(2 * np.pi * np.cumsum(500 + 250 * np.sin(2 * np.pi * 3 * t)) / SR) * np.sin(np.linspace(0, np.pi, m)) * 0.35


def choo():
    out = []
    for d in (0.45, 0.8):
        m = int(d * SR)
        t = np.arange(m) / SR
        v = 1 + 0.01 * np.sin(2 * np.pi * 6 * t)
        x = sum(np.sin(2 * np.pi * f * v * t) * g for f, g in ((587, 0.5), (740, 0.4), (880, 0.3)))
        out.append(x * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08) * 0.5)
        out.append(np.zeros(int(0.08 * SR)))
    return np.concatenate(out)


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 122
    prog = [[64, 68, 71], [61, 64, 68], [57, 61, 64], [59, 63, 66]]           # E C#m A B: bright, bouncy pop
    hook = [76, 80, 83, 80, 81, 0, 78, 76, 80, 83, 88, 83, 81, 78, 76, 0]
    bar, tt = 0, 2.3
    while tt < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = tt + q * B
            A.add(mus, LS.kick(), b0, 0.5)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.32, 0.05)
                A.add(mus, RV.snare(), b0, 0.16)
            A.add(mus, LS.hat(), b0 + B / 2, 0.45, -0.3)
            A.add(mus, LS.hat(), b0 + B * 0.75, 0.2, 0.3)
            for e, mm in ((0, ch[0] - 24), (0.5, ch[0] - 12), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm, B * 0.4), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):                                   # plucky marimba-ish chords on the off-beats
                A.add(mus, A.tone(A.mtof(nt + 12), 0.25, ((1, 1), (4, 0.3), (10, 0.06)), 0.002, 0.09), b0 + B / 2, 0.045, -0.25 + 0.25 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, M.toy_piano(mm, 0.4), tt + i * B / 2, 0.06, 0.2)
        tt += 4 * B
        bar += 1
    ts = np.arange(n) / SR
    mus *= np.clip((total - ts) / 1.5, 0, 1)[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.12)
    A.add(v, tracks["mishu"], 0, 1.0, 0.12)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.5 * e)[:, None]
    f = np.zeros((n, 2))
    notes = iter([72, 74, 76, 77, 79, 81, 83])
    for kind, at, dur in T.fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.35)
        elif kind == "boing":
            A.add(f, M.boing(), at, 0.35)
        elif kind == "splat":
            A.add(f, splat(), at, 0.55, float(rng.uniform(-0.5, 0.5)))
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "scribble":
            A.add(f, scribble(dur), at, 0.3)
        elif kind == "reveal":
            A.add(f, A.sfx_pop(), at, 0.45)
            A.add(f, A.sfx_sparkle(), at + 0.05, 0.35)
        elif kind == "pour":
            A.add(f, pour(), at, 0.35)
        elif kind == "swirl":
            A.add(f, swirl(), at, 0.3)
        elif kind == "note":
            A.add(f, A.tone(A.mtof(next(notes, 84)), 0.8, ((1, 1), (2.76, 0.25)), 0.002, 0.4), at, 0.12)
        elif kind == "choo":
            A.add(f, choo(), at, 0.4)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.3)
        elif kind == "build":
            for k in range(int(dur)):
                A.add(f, A.sfx_pop(), at + 0.3 + k * 0.55, 0.3)
        elif kind == "stomp2":
            for k in range(3):
                A.add(f, M.stomp(), at + 0.2 + k * 0.35, 0.4)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "yes":
            A.add(f, A.sfx_ding(79), at, 0.2)
            A.add(f, A.sfx_ding(84), at + 0.12, 0.2)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.15)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(86), p0, 0.1)
    mix = v + mus * 0.33 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    return mix


if __name__ == "__main__":
    build()
