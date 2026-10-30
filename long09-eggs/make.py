"""Long video 9: "Who's in the Egg?". Voices, timeline.json, mix.wav (own music + own animal sounds).
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

EGGS = [  # baby, bg, hint, reveal line, fact, sound
    ("chick", "barn", "This egg is in the hay, on the farm!", "A baby chick! Cheep cheep!", "Mama hen sits on her eggs to keep them warm.", "cheep"),
    ("duckling", "pond", "This egg is next to the pond!", "A baby duckling! Quack quack!", "Ducklings can swim on their very first day!", "quack"),
    ("turtle", "beach", "This egg is buried in the sand, on the beach!", "A baby sea turtle!", "Baby sea turtles run to the sea all by themselves!", "flip"),
    ("robin", "tree", "A little blue egg, in a nest!", "A baby robin! Tweet tweet!", "Robin eggs are a pretty sky blue color!", "tweet"),
    ("crocodile", "river", "This egg is by the river. Snap, snap!", "A baby crocodile!", "Mama crocodile carries her babies in her mouth, very gently!", "eep"),
    ("penguin", "ice", "This egg is on the ice. Brrr!", "A baby penguin!", "Penguin daddies keep the egg warm on their feet!", "squawk"),
    ("snake", "jungle", "This egg is hiding in the jungle leaves. Sss!", "A baby snake! Hiss!", "Baby snakes have a tiny egg tooth to cut open the egg!", "hiss"),
    ("ostrich", "savanna", "Wow! This is a giant egg!", "A baby ostrich!", "Ostrich eggs are the biggest bird eggs in the world!", "peep"),
    ("owl", "tree", "This egg is in a hole, up in a tree!", "A baby owl! Hoo hoo!", "Owls sleep in the day, and wake up at night!", "hoot"),
    ("dino", "valley", "A big spotty egg, from long, long ago!", "A baby dinosaur! Rawr!", "Dinosaurs hatched from eggs too, a long time ago!", "roar"),
]
SORT = [("hen", "egg", "A hen lays eggs!"), ("puppy", "baby", "A puppy is born as a baby!"), ("turtle", "egg", "A turtle lays eggs!"),
        ("kitten", "baby", "A kitten is born as a baby!"), ("fish", "egg", "Fish lay eggs!"), ("calf", "baby", "A baby cow is born as a baby!"),
        ("snake", "egg", "A snake lays eggs!"), ("elephant", "baby", "An elephant is born as a baby!")]
SIZES = [("hummingbird", "A hummingbird egg is tiny, like a jelly bean!"), ("chicken", "A chicken egg, like the eggs we eat!"),
         ("ostrich", "An ostrich egg is as big as a melon!")]
LIFE = [("chicken", [("egg", "First, an egg."), ("chick", "Crack! A little chick!"), ("hen", "The chick grows into a big hen!")]),
        ("butterfly", [("leafeggs", "Tiny eggs on a leaf."), ("caterpillar", "Out comes a hungry caterpillar!"),
                       ("cocoon", "It makes a cozy cocoon, and sleeps."), ("butterfly", "Then, a beautiful butterfly!")])]
LIFE.append(("frog", [("frogspawn", "Frogs lay squishy eggs in the water."), ("tadpole", "Out swims a wiggly tadpole!"),
                      ("frog", "It grows legs, and turns into a frog! Ribbit!")]))
HOMES = [("penguin", "ice", ["ice", "jungle", "beach"]), ("crocodile", "river", ["savanna", "river", "ice"]), ("owl", "tree", ["beach", "pond", "tree"]),
         ("turtle", "beach", ["beach", "ice", "tree"]), ("duckling", "pond", ["jungle", "pond", "savanna"]), ("ostrich", "savanna", ["river", "tree", "savanna"])]
HOME_LINE = {"ice": "On the cold ice!", "river": "By the river!", "tree": "Up in a tree!", "beach": "On the sandy beach!", "pond": "In the pond!", "savanna": "On the grassy savanna!"}
FACTS = [("hen", "A hen can lay almost one egg every day!"), ("chick", "Baby birds have a tiny egg tooth, to break out of the shell!"),
         ("platypus", "The platypus is a very special animal. It has fur, but it lays eggs!"),
         ("kiwi", "The kiwi bird lays a giant egg, almost as big as the kiwi!"), ("frogspawn", "Frog eggs have no shell. They are soft, like jelly!"),
         ("ostrich", "An ostrich egg shell is so strong, a grown-up can stand on it!"),
         ("penguin", "Emperor penguin daddies hold the egg on their feet for two whole months!")]
DANCE = [("Curl up small, like an egg!", "curl"), ("Wiggle, wiggle, wiggle!", "wiggle"), ("Knock, knock, knock!", "knock"),
         ("Crack! Pop out!", "pop"), ("Flap your little wings!", "flap"), ("Cheep cheep! Hello world!", "jump")]
SOUNDS = [("quack", "duckling", "Quack quack! A duckling!"), ("hoot", "owl", "Hoo hoo! A baby owl!"), ("hiss", "snake", "Sss! A baby snake!"),
          ("cheep", "chick", "Cheep cheep! A baby chick!"), ("tweet", "robin", "Tweet tweet! A baby robin!"),
          ("squawk", "penguin", "A baby penguin!"), ("roar", "dino", "Rawr! A baby dinosaur!")]
QUIZ = [("Which bird has the biggest egg?", "The ostrich!", "ostrich"), ("Who keeps the penguin egg warm?", "Penguin daddy, on his feet!", "penguin"),
        ("What does a caterpillar turn into?", "A butterfly!", "butterfly"), ("Does a puppy hatch from an egg?", "No! A puppy is born as a baby!", "puppy"),
        ("Where do baby sea turtles run?", "To the sea!", "turtle"), ("What sound does a baby chick make?", "Cheep cheep!", "chick"),
        ("What does a tadpole grow into?", "A frog!", "frog"), ("Where does a baby owl live?", "Up in a tree!", "owl")]


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

    def mark(self, kind, arg=""):
        self.fx.append((kind, round(self.t, 3), arg))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("riser")
        self.pause(0.5)
        self.say(who, text, gap=0.3)
        self.end(sc)


def other(w):
    return "mishu" if w == "gul" else "gul"


def knock_knock(T, sc, who):
    """two knocks on the egg while saying Knock knock"""
    sc["knock_t"] = [T.mark("knock")]
    T.pause(0.35)
    sc["knock_t"].append(T.mark("knock"))
    T.pause(0.35)


def build():
    T = TL()
    # ---------------------------------------------------------------- OPENING: golden egg shakes, knocks, cracks, babies burst out
    sc = T.scene("intro", "barn")
    sc["knock_t"] = []
    for k in range(3):
        sc["knock_t"].append(T.mark("knock"))
        T.pause(0.3)
    sc["crack_t"] = T.mark("crack")
    T.pause(0.5)
    sc["hatch_t"] = T.mark("burst")
    T.pause(0.9)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Who's in the egg?", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Knock, knock! Baby animals are hatching!", gap=0.2)
    T.say("gul", "Let's find out who's inside! Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- KNOCK KNOCK! 10 eggs
    T.title("barn", "KNOCK KNOCK!", "gul", "Knock on the egg, and guess who's inside!")
    for k, (baby, bg, hint, reveal, fact, snd) in enumerate(EGGS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("egg", bg, baby=baby, num=k + 1)
        T.mark("pop")
        T.pause(0.3)
        sc["kk_t"] = round(T.t, 3)
        knock_knock(T, sc, a)
        T.t = sc["kk_t"]
        T.say(a, "Knock, knock!", gap=0.2)
        sc["hint_t"] = T.say(other(a), hint, gap=0.1)
        T.prompt(a, "Who's in the egg?", wait=2.0)
        sc["crack_t"] = T.mark("crack")
        T.pause(0.9)
        sc["hatch_t"] = T.mark("hatch")
        T.mark(snd)
        T.pause(0.5)
        sc["name_t"] = T.say(other(a), reveal, gap=0.2)
        T.say(a, fact, gap=0.2)
        T.say("both", f"Hello, baby {'dino' if baby == 'dino' else baby}!", gap=0.5)
        T.stars.append(sc["hatch_t"])
        T.end(sc)
    # ---------------------------------------------------------------- COUNT THE CHICKS
    T.title("barn", "COUNT THE CHICKS!", "mishu", "Five eggs in the hay! Let's count the chicks!")
    sc = T.scene("count", "barn")
    hatches = []
    for i, w in enumerate(("One chick!", "Two chicks!", "Three chicks!", "Four chicks!", "Five chicks!")):
        hatches.append(T.mark("hatch"))
        T.mark("cheep")
        T.pause(0.4)
        T.say("both", w, gap=0.25)
    sc["hatches"] = hatches
    T.say("gul", "Five baby chicks! Cheep, cheep, cheep!", gap=0.2)
    T.prompt("mishu", "Big kids! Two chicks went to sleep. How many are awake?", wait=2.6)
    sc["sleep_t"] = T.mark("yes")
    T.say("gul", "Three! Five take away two is three!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- FIND THE HIDDEN EGGS
    T.title("barn", "FIND THE EGGS!", "gul", "Oh no! Five eggs are hiding in the barn!")
    sc = T.scene("hidden", "barn")
    T.prompt("mishu", "Can you find all five eggs?", wait=3.0)
    found = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!"):
        found.append(T.mark("yes"))
        T.say("both", w, gap=0.3)
    sc["found"] = found
    T.say("gul", "We found them all! Great job!", gap=0.5)
    T.stars.append(round(T.t - 1.0, 3))
    T.end(sc)
    # ---------------------------------------------------------------- BIG OR SMALL EGGS
    T.title("savanna", "BIG AND SMALL EGGS!", "gul", "Eggs can be tiny, or giant! Look!")
    sc = T.scene("sizes", "savanna")
    shown = []
    for i, (egg, text) in enumerate(SIZES):
        shown.append(T.mark("pop"))
        T.say("mishu" if i % 2 == 0 else "gul", text, gap=0.3)
    sc["shown"] = shown
    T.prompt("gul", "Which egg is the biggest?", wait=2.0)
    sc["big_t"] = T.mark("yes")
    T.say("mishu", "The ostrich egg! It weighs as much as twenty chicken eggs!", gap=0.2)
    T.prompt("mishu", "And which egg is the smallest?", wait=2.0)
    sc["small_t"] = T.mark("yes")
    T.say("gul", "The tiny hummingbird egg!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- WHERE DO THEY LIVE?
    T.title("barn", "WHERE DO THEY LIVE?", "mishu", "Help the babies find their homes!")
    for k, (baby, home, opts) in enumerate(HOMES):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("home", "barn", baby=baby, home=home, opts=opts)
        T.mark("pop")
        T.prompt(a, f"Where does the baby {baby} live?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), HOME_LINE[home], gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- EGGS OR BABIES? sorting
    T.title("barn", "EGG OR BABY?", "mishu", "Some animals hatch from eggs. Some are born as babies. Let's sort!")
    for k, (animal, side, ans) in enumerate(SORT):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sort", "barn", animal=animal, side=side, done=[(x[0], x[1]) for x in SORT[:k]])
        T.mark("pop")
        T.prompt(a, "Egg, or baby?", wait=1.8)
        sc["answer_t"] = T.mark("whoosh")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- LIFE CYCLES (big kids)
    T.title("pond", "HOW THEY GROW!", "gul", "Big kids! Let's see how babies grow up!")
    for name, steps in LIFE:
        sc = T.scene("life", "pond", name=name, steps=[s[0] for s in steps])
        sc["step_t"] = []
        for i, (key, text) in enumerate(steps):
            sc["step_t"].append(T.mark("pop"))
            T.say("mishu" if i % 2 == 0 else "gul", text, gap=0.3)
        sc["cycle_t"] = round(T.t, 3)
        T.say("both", "Round and round! That's a life cycle!", gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- HATCHING DANCE, twice
    T.title("barn", "HATCHING DANCE!", "mishu", "Stand up! Let's hatch like baby chicks! Copy us!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "barn", title="FASTER!")
            T.mark("riser")
            T.say("gul", "Again, faster!", gap=0.2)
            T.end(sc)
        for text, move in DANCE:
            sc = T.scene("dance", "barn", move=move, fast=rnd == 1, word=text.split("!")[0].split(",")[0].upper() + "!")
            T.mark("knock3" if move == "knock" else ("crack" if move == "pop" else "pop"))
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- LISTEN! sound guessing
    T.title("pond", "LISTEN! WHO'S INSIDE?", "gul", "Shh! Listen to the egg. Who's inside?")
    for k, (snd, baby, ans) in enumerate(SOUNDS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("listen", "pond", baby=baby)
        T.pause(0.3)
        sc["sound_t"] = [T.mark(snd)]
        T.pause(1.3)
        sc["sound_t"].append(T.mark(snd))
        T.pause(1.2)
        T.prompt(a, "Who's in the egg?", wait=1.8)
        sc["hatch_t"] = T.mark("hatch")
        T.pause(0.4)
        T.say(other(a), ans, gap=0.5)
        T.stars.append(sc["hatch_t"])
        T.end(sc)
    # ---------------------------------------------------------------- AMAZING EGG FACTS
    T.title("pond", "AMAZING EGG FACTS!", "gul", "Big kids! Here are some amazing egg facts!")
    for k, (vis, text) in enumerate(FACTS):
        sc = T.scene("fact", "pond", vis=vis, num=k + 1)
        T.mark("pop")
        T.pause(0.3)
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.3)
        T.say("gul" if k % 2 == 0 else "mishu", "Wow!", gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- QUIZ
    T.title("barn", "EGG QUIZ!", "mishu", "Big kids quiz! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("quiz", "barn", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- COUNTDOWN FINALE: the golden egg
    sc = T.scene("finale", "barn")
    T.say("gul", "One more egg! The golden egg!", gap=0.2)
    T.say("mishu", "Let's count down together!", gap=0.2)
    nums = []
    for w in ("Five!", "Four!", "Three!", "Two!", "One!"):
        T.mark("knock")
        nums.append(T.say("both", w, gap=0.3))
    sc["nums"] = nums
    T.say("both", "Hatch!", gap=0.0)
    sc["hatch_t"] = T.mark("burst")
    T.pause(0.4)
    T.say("gul", "All our baby friends are here!", gap=0.6)
    T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "barn")
    T.say("mishu", "So many babies hatch from eggs!", gap=0.2)
    T.say("gul", "Which baby animal did you like best?", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends! Cheep cheep!", gap=1.8)
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


# ==================================================================== music + animal sounds (all made in code)
rng = np.random.default_rng(91)


def tt_(d):
    return np.arange(int(d * SR)) / SR


def envd(t, a, d):
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def knock():
    t = tt_(0.18)
    body = np.sin(2 * np.pi * 210 * t) * envd(t, 0.001, 0.03) + 0.5 * np.sin(2 * np.pi * 520 * t) * envd(t, 0.001, 0.015)
    click = np.concatenate([rng.standard_normal(80) * np.linspace(1, 0, 80), np.zeros(len(t) - 80)])
    return body + click * 0.4


def crack():
    out = np.zeros(int(0.7 * SR))
    for k in range(5):
        n = int(0.05 * SR)
        x = np.diff(np.concatenate([[0], rng.standard_normal(n)])) * A.env(n, 0.001, 0.012)
        i = int(k * 0.13 * SR)
        out[i:i + n] += x * 1.5
    return out


def chirp(f0, f1, d, wave="sin"):
    t = tt_(d)
    f = f0 + (f1 - f0) * t / d
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) if wave == "sin" else np.sign(np.sin(ph)) * 0.5
    return x * np.minimum(1, t / 0.008) * np.minimum(1, (d - t) / 0.02)


def seq(parts, gap):
    out = []
    for p in parts:
        out += [p, np.zeros(int(gap * SR))]
    return np.concatenate(out)


def animal(kind):
    if kind == "cheep":
        return seq([chirp(2600, 3600, 0.09), chirp(2700, 3800, 0.09)], 0.07)
    if kind == "tweet":
        return seq([chirp(3800, 2800, 0.06) for _ in range(4)], 0.04)
    if kind == "quack":
        t = tt_(0.22)
        x = np.sign(np.sin(2 * np.pi * np.cumsum(480 - 120 * t / 0.22) / SR))
        x = np.convolve(x, np.ones(6) / 6, mode="same") * np.minimum(1, t / 0.01) * np.minimum(1, (0.22 - t) / 0.05) * 0.6
        return seq([x, x], 0.1)
    if kind == "flip":
        return seq([chirp(900, 300, 0.05) * 0.6 for _ in range(4)], 0.08)
    if kind == "eep":
        return seq([chirp(1100, 1600, 0.12, "sq"), chirp(1200, 1700, 0.12, "sq")], 0.12)
    if kind == "squawk":
        t = tt_(0.35)
        f = 700 + 300 * np.sin(np.pi * t / 0.35)
        x = (2 * ((np.cumsum(f) / SR) % 1) - 1) * 0.5 + rng.standard_normal(len(t)) * 0.15
        return np.convolve(x, np.ones(4) / 4, mode="same") * np.minimum(1, t / 0.02) * np.minimum(1, (0.35 - t) / 0.08)
    if kind == "hiss":
        t = tt_(0.9)
        x = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
        return x * 0.35 * np.minimum(1, t / 0.15) * np.minimum(1, (0.9 - t) / 0.2)
    if kind == "peep":
        return seq([chirp(900, 1300, 0.15), chirp(950, 1350, 0.15)], 0.1)
    if kind == "hoot":
        t = tt_(0.32)
        h = np.sin(2 * np.pi * np.cumsum(420 - 40 * t / 0.32) / SR) * np.sin(np.pi * t / 0.32) * 0.8
        return seq([h, h], 0.12)
    if kind == "roar":
        n = int(0.8 * SR)
        t = np.arange(n) / SR
        f = 210 * (1 + 0.35 * np.sin(np.pi * t / 0.8)) * (1 + 0.03 * np.sin(2 * np.pi * 28 * t))
        saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
        nz = np.convolve(rng.standard_normal(n), np.ones(6) / 6, mode="same")
        x = np.convolve(saw * 0.8 + nz * 0.5, np.ones(10) / 10, mode="same")
        return x * np.minimum(1, t / 0.08) * np.minimum(1, (0.8 - t) / 0.25) * 1.4
    return np.zeros(10)


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 116
    prog = [[58, 62, 65], [55, 58, 62], [51, 55, 58], [53, 57, 60]]           # Bb Gm Eb F: bouncy, warm
    hook = [77, 74, 77, 81, 82, 0, 81, 77, 79, 77, 74, 72, 74, 0, 77, 0]
    bar, t0 = 0, 3.6
    while t0 < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = t0 + q * B
            A.add(mus, LS.kick(), b0, 0.48)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.3, 0.05)
                A.add(mus, RV.snare(), b0, 0.14)
            A.add(mus, LS.hat(), b0 + B / 2, 0.45, -0.3)
            A.add(mus, knock() * 0.5, b0 + B * 0.75, 0.12, 0.35)              # woodblock tick, like a knock on an egg
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):
                A.add(mus, A.tone(A.mtof(nt + 12), 0.3, ((1, 1), (3, 0.25), (5.4, 0.08)), 0.002, 0.11), b0 + B / 2, 0.045, -0.25 + 0.25 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, M.toy_piano(mm, 0.4), t0 + i * B / 2, 0.06, 0.2)
        t0 += 4 * B
        bar += 1
    ts = np.arange(n) / SR
    mus *= np.clip((total - ts) / 1.5, 0, 1)[:, None]
    # music drops out while listening for animal sounds
    g = np.ones(n)
    for s in T.scenes:
        if s["kind"] == "listen":
            a, b = int((s["sound_t"][0] - 0.3) * SR), int((s["sound_t"][-1] + 1.0) * SR)
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
    for kind, at, arg in T.fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.35)
        elif kind == "knock":
            A.add(f, knock(), at, 0.8)
        elif kind == "knock3":
            for k in range(3):
                A.add(f, knock(), at + 0.25 + k * 0.3, 0.6)
        elif kind == "crack":
            A.add(f, crack(), at, 0.8)
        elif kind == "hatch":
            A.add(f, A.sfx_pop(), at, 0.5)
            A.add(f, A.sfx_sparkle(), at + 0.05, 0.3)
        elif kind == "burst":
            A.add(f, LS.kick() * 1.2, at, 0.8)
            A.add(f, A.sfx_sparkle(), at, 0.5)
            for k, s in enumerate(("cheep", "quack", "squawk", "cheep")):
                A.add(f, animal(s), at + 0.15 + k * 0.18, 0.35, -0.4 + 0.27 * k)
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.3)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "yes":
            A.add(f, A.sfx_ding(79), at, 0.2)
            A.add(f, A.sfx_ding(84), at + 0.12, 0.2)
        else:
            A.add(f, animal(kind), at, 0.55)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.15)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(86), p0, 0.1)
    mix = v + mus * 0.33 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    return mix


if __name__ == "__main__":
    build()
