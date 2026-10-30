"""Long video 13: "Wild Animals Safari". Voices, timeline.json, mix.wav (own music + own animal sounds).
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

SAFARI = [  # habitat bg, title, intro line, animals (key, name, sound, fact)
    ("savanna", "THE SAVANNA!", "First stop, the grassy savanna!", [
        ("lion", "lion", "roar", "Lions live in big families called prides!"),
        ("elephant", "elephant", "trumpet", "Elephants are the biggest animals on land!"),
        ("giraffe", "giraffe", "hum", "Giraffes are the tallest animals in the world!"),
        ("zebra", "zebra", "whinny", "Every zebra has its very own stripes!"),
        ("hippo", "hippo", "grunt", "Hippos stay in the water all day, to keep cool!"),
        ("rhino", "rhino", "snort", "A rhino's horn is made of the same stuff as your fingernails!"),
        ("cheetah", "cheetah", "chirp", "Cheetahs are the fastest runners! And they chirp like birds!")]),
    ("jungle", "THE JUNGLE!", "Next stop, the green jungle!", [
        ("tiger", "tiger", "roar", "Tigers have stripes, and they love to swim!"),
        ("monkey", "monkey", "ooh", "Monkeys swing from tree to tree!"),
        ("gorilla", "gorilla", "beat", "Gorillas beat their chests! But they're very gentle."),
        ("parrot", "parrot", "squawk", "Some parrots can copy words! Hello! Hello!"),
        ("snake", "snake", "hiss", "Snakes smell with their tongues!")]),
    ("forest", "THE FOREST!", "Now, into the forest!", [
        ("bear", "bear", "growl", "Bears love honey, and sleep all winter long!"),
        ("wolf", "wolf", "howl", "Wolves howl to talk to their family!"),
        ("owl", "owl", "hoot", "Owls can turn their heads almost all the way around!"),
        ("panda", "panda", "munch", "Pandas eat bamboo, almost all day long!")]),
    ("desert", "THE DESERT!", "Phew! It's hot in the desert!", [
        ("camel", "camel", "groan", "Camels can walk for days in the hot sand!")]),
    ("outback", "THE OUTBACK!", "Hop hop! Welcome to the outback!", [
        ("kangaroo", "kangaroo", "thump", "Baby kangaroos ride in their mum's pouch!"),
        ("koala", "koala", "snore", "Koalas sleep about twenty hours a day!")]),
    ("ice", "THE ICE!", "Brrr! It's cold on the ice!", [
        ("penguin", "penguin", "squawk2", "Penguins can't fly, but they swim super fast!")]),
    ("pond", "THE RIVER!", "Last stop, the river!", [
        ("flamingo", "flamingo", "honk", "Flamingos are pink because of the food they eat!"),
        ("crocodile", "crocodile", "snap", "Crocodiles lived at the time of the dinosaurs!")]),
]
RECORDS = [("Which animal is the biggest on land?", "elephant", ["giraffe", "elephant", "lion"], "The elephant!"),
           ("Which animal is the tallest?", "giraffe", ["giraffe", "zebra", "camel"], "The giraffe!"),
           ("Which animal runs the fastest?", "cheetah", ["hippo", "bear", "cheetah"], "The cheetah!"),
           ("Which animal sleeps the most?", "koala", ["koala", "monkey", "wolf"], "The koala! Zzz!")]
SOUNDS = [("roar", "lion", "Roar! The lion!"), ("trumpet", "elephant", "The elephant!"), ("hoot", "owl", "Hoo hoo! The owl!"),
          ("howl", "wolf", "Awoooo! The wolf!"), ("hiss", "snake", "Sss! The snake!"), ("ooh", "monkey", "Ooh ooh ah ah! The monkey!")]
HOMES = [("penguin", "ice", ["ice", "desert", "jungle"]), ("camel", "desert", ["forest", "desert", "ice"]),
         ("kangaroo", "outback", ["pond", "jungle", "outback"]), ("monkey", "jungle", ["jungle", "ice", "desert"]),
         ("bear", "forest", ["savanna", "forest", "pond"]), ("lion", "savanna", ["outback", "pond", "savanna"])]
HOME_SAY = {"ice": "On the cold ice!", "desert": "In the hot desert!", "outback": "In the outback!", "jungle": "In the jungle!",
            "forest": "In the forest!", "savanna": "On the savanna!", "pond": "By the river!"}
BABIES = [("lion", "cub", "A baby lion is called a cub!"), ("kangaroo", "joey", "A baby kangaroo is called a joey!"),
          ("elephant", "calf", "A baby elephant is called a calf!"), ("owl", "owlet", "A baby owl is called an owlet!")]
EAT = [("lion", "meat", ["meat", "banana", "bamboo"], "Lions eat meat!"), ("panda", "bamboo", ["fish", "bamboo", "meat"], "Pandas eat bamboo!"),
       ("monkey", "banana", ["leaves", "fish", "banana"], "Monkeys love bananas!"), ("koala", "leaves", ["leaves", "meat", "fish"], "Koalas eat eucalyptus leaves!"),
       ("penguin", "fish", ["banana", "fish", "bamboo"], "Penguins eat fish!"), ("giraffe", "leaves", ["meat", "banana", "leaves"], "Giraffes eat leaves from tall trees!")]
HIDE = [("zebra", "I see black and white stripes!", "A zebra!"), ("elephant", "I see a long trunk!", "An elephant!"),
        ("giraffe", "I see a very long neck!", "A giraffe!"), ("lion", "I see a fluffy mane!", "A lion!"),
        ("kangaroo", "I see big, long ears!", "A kangaroo!"), ("flamingo", "I see a pink, curly neck!", "A flamingo!")]
PATTERN = [("zebra", "stripes"), ("cheetah", "spots"), ("tiger", "stripes"), ("giraffe", "spots")]
DANCE = [("Stomp like an elephant!", "stomp"), ("Jump like a kangaroo!", "jump"), ("Swing like a monkey!", "swing"),
         ("Stretch tall like a giraffe!", "stretch"), ("Roar like a lion! Roar!", "roar"), ("Waddle like a penguin!", "waddle")]
QUIZ = [("Which animal is the tallest?", "The giraffe!", "giraffe"), ("What do pandas eat?", "Bamboo!", "panda"),
        ("Where does a camel live?", "In the desert!", "camel"), ("What is a baby kangaroo called?", "A joey!", "kangaroo"),
        ("Which animal is the fastest?", "The cheetah!", "cheetah"), ("What sound does a wolf make?", "It howls! Awoooo!", "wolf"),
        ("Why are flamingos pink?", "Because of the food they eat!", "flamingo"), ("Which animal has a long trunk?", "The elephant!", "elephant")]


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
    # ---------------------------------------------------------------- OPENING: a lion leaps in, ROAR, title
    sc = T.scene("intro", "savanna")
    T.pause(0.3)
    sc["roar_t"] = T.mark("roar")
    T.pause(1.4)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Wild animals!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Hop in the safari jeep! Let's meet animals from all over the world!", gap=0.2)
    T.say("gul", "Roar! Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- SAFARI: 7 habitats, 22 animals
    n = 0
    for bg, ttl, intro, animals in SAFARI:
        sc = T.scene("habitat", bg, title=ttl)
        T.mark("engine")
        T.pause(0.6)
        T.say("gul" if n % 2 == 0 else "mishu", intro, gap=0.3)
        T.end(sc)
        for key, name, snd, fact in animals:
            n += 1
            a = "gul" if n % 2 == 0 else "mishu"
            sc = T.scene("animal", bg, key=key, name=name, num=n)
            T.mark("pop")
            T.pause(0.3)
            sc["name_t"] = T.say(a, f"Look! {'An' if name[0] in 'aeiou' else 'A'} {name}!", gap=0.1)
            sc["snd_t"] = T.mark(snd)
            T.pause(1.3)
            T.say(other(a), fact, gap=0.1)
            T.prompt(a, f"Say {name}!", wait=1.2)
            T.end(sc)
    sc = T.scene("allanimals", "savanna")
    T.say("both", "We met so many wild animals! Hooray!", gap=0.5)
    T.stars.append(round(T.t - 0.8, 3))
    T.end(sc)
    # ---------------------------------------------------------------- ANIMAL RECORDS
    T.title("savanna", "ANIMAL RECORDS!", "mishu", "Who is the biggest? Who is the fastest? Let's find out!")
    for k, (q, ans, opts, line_) in enumerate(RECORDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("record", "savanna", ans=ans, opts=opts)
        T.prompt(a, q, wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), line_, gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- WHO'S THAT SOUND?
    T.title("jungle", "WHO'S THAT SOUND?", "gul", "Listen carefully! Which animal is it?")
    for k, (snd, key, ans) in enumerate(SOUNDS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("sound", "jungle", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.6)
        T.prompt(a, "Who is it?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- WHERE DO THEY LIVE?
    T.title("savanna", "WHERE DO THEY LIVE?", "mishu", "Help the animals find their homes!")
    for k, (key, home, opts) in enumerate(HOMES):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("home", "savanna", key=key, home=home, opts=opts)
        T.mark("pop")
        T.prompt(a, f"Where does the {key} live?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), HOME_SAY[home], gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- WHAT DO THEY EAT?
    T.title("jungle", "WHAT DO THEY EAT?", "gul", "Animals are hungry! What do they eat?")
    for k, (key, food, opts, line_) in enumerate(EAT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("eat", "jungle", key=key, food=food, opts=opts)
        T.mark("pop")
        T.prompt(a, f"What does the {key} eat?", wait=1.8)
        sc["answer_t"] = T.mark("munch")
        T.say(other(a), line_, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- WHO'S HIDING?
    T.title("forest", "WHO'S HIDING?", "mishu", "Someone is hiding behind the bush! Who is it?")
    for k, (key, clue, ans) in enumerate(HIDE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("hide", "forest", key=key)
        T.mark("pop")
        T.say(a, clue, gap=0.1)
        T.prompt(a, "Who is it?", wait=1.8)
        sc["reveal_t"] = T.mark("yes")
        T.say(other(a), f"Peekaboo! {ans}", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- SPOTS OR STRIPES?
    T.title("savanna", "SPOTS OR STRIPES?", "gul", "Some animals have spots. Some have stripes!")
    for k, (key, pat) in enumerate(PATTERN):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("pattern", "savanna", key=key, pat=pat)
        T.mark("pop")
        T.prompt(a, f"Does the {key} have spots, or stripes?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{pat.capitalize()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BABY ANIMAL NAMES
    T.title("outback", "BABY ANIMALS!", "gul", "Big kids! Baby animals have special names!")
    for k, (key, baby, line_) in enumerate(BABIES):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("baby", "outback", key=key, baby=baby)
        T.prompt(a, f"What is a baby {key} called?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), line_, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- COUNT THE ZEBRAS
    sc = T.scene("count", "savanna")
    T.say("mishu", "Here come the zebras! Let's count them!", gap=0.1)
    cts = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!", "Six!", "Seven!", "Eight!", "Nine!", "Ten!"):
        cts.append(T.mark("gallop"))
        T.say("both", w, gap=0.25)
    sc["cts"] = cts
    T.say("gul", "Ten zebras! Run, zebras, run!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- ANIMAL MOVES DANCE x2
    T.title("savanna", "ANIMAL MOVES!", "mishu", "Stand up! Move like the animals! Copy us!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "savanna", title="FASTER!")
            T.mark("riser")
            T.say("gul", "Again, faster!", gap=0.2)
            T.end(sc)
        for text, move in DANCE:
            sc = T.scene("dance", "savanna", move=move, fast=rnd == 1, word=text.split("!")[0].upper() + "!")
            T.mark("roar_small" if move == "roar" else ("stomp2" if move in ("stomp", "jump") else "pop"))
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- QUIZ
    T.title("jungle", "ANIMAL QUIZ!", "gul", "Big kids quiz! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("quiz", "jungle", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "savanna")
    T.say("mishu", "Which wild animal is your favourite?", gap=0.2)
    T.say("gul", "Mine is the lion! Roar!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends! See you on the next safari!", gap=1.8)
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
rng = np.random.default_rng(13)


def tt_(d):
    return np.arange(int(d * SR)) / SR


def noise(d, lp=1):
    x = rng.standard_normal(int(d * SR))
    return np.convolve(x, np.ones(lp) / lp, mode="same") if lp > 1 else x


def env(t, d, a=0.03, r=0.2):
    return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, d - t) / r)


def growl(d, f0, f1, rough=0.6, vib=28):
    t = tt_(d)
    f = (f0 + (f1 - f0) * np.sin(np.pi * t / d)) * (1 + 0.03 * np.sin(2 * np.pi * vib * t))
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    x = np.convolve(saw * 0.8 + noise(d, 6)[:len(t)] * rough, np.ones(10) / 10, mode="same")
    return x * env(t, d, 0.06, 0.25) * 1.4


def tone(f0, f1, d, wave="sin", a=0.02, r=0.1):
    t = tt_(d)
    ph = 2 * np.pi * np.cumsum(f0 + (f1 - f0) * t / d) / SR
    x = np.sin(ph) if wave == "sin" else (np.sign(np.sin(ph)) * 0.5 if wave == "sq" else (2 * ((ph / 6.283) % 1) - 1) * 0.6)
    return x * env(t, d, a, r)


def seq(parts, gap):
    out = []
    for p in parts:
        out += [p, np.zeros(int(gap * SR))]
    return np.concatenate(out)


def animal(kind):
    if kind == "roar":
        return growl(1.3, 90, 140)
    if kind == "roar_small":
        return growl(0.7, 160, 230)
    if kind == "trumpet":
        x = tone(420, 650, 0.9, "saw")
        return np.convolve(x, np.ones(4) / 4, mode="same") * 1.2
    if kind == "hum":
        return tone(110, 120, 1.0) * 0.6
    if kind == "whinny":
        t = tt_(0.8)
        return tone(700, 500, 0.8, "sq") * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t))
    if kind == "grunt":
        return seq([growl(0.25, 70, 90, 0.9) for _ in range(3)], 0.12)
    if kind == "snort":
        return seq([noise(0.25, 3)[:int(0.25 * SR)] * env(tt_(0.25), 0.25, 0.01, 0.1) * 0.8 for _ in range(2)], 0.15)
    if kind == "chirp":
        return seq([tone(1800, 2400, 0.1) for _ in range(3)], 0.08)
    if kind == "ooh":
        return seq([tone(500, 800, 0.18), tone(520, 820, 0.18), tone(900, 1200, 0.12), tone(950, 1250, 0.12)], 0.06)
    if kind == "beat":
        t = tt_(0.12)
        thump = np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.04)
        return seq([thump] * 6, 0.07) * 1.2
    if kind == "squawk":
        t = tt_(0.35)
        return (tone(900, 1300, 0.35, "saw") + noise(0.35)[:len(t)] * 0.2) * 0.8
    if kind == "squawk2":
        return seq([tone(700, 900, 0.25, "saw") * 0.7, tone(700, 950, 0.3, "saw") * 0.7], 0.1)
    if kind == "hiss":
        t = tt_(0.9)
        return np.diff(np.concatenate([[0], noise(0.9)]))[:len(t)] * 0.35 * env(t, 0.9, 0.15, 0.2)
    if kind == "growl":
        return growl(1.0, 80, 110, 0.9)
    if kind == "howl":
        x = np.concatenate([tone(350, 650, 0.8, a=0.2, r=0.05), tone(650, 450, 0.8, a=0.05, r=0.4)])
        t = np.arange(len(x)) / SR
        return x * (1 + 0.04 * np.sin(2 * np.pi * 6 * t))
    if kind == "hoot":
        t = tt_(0.32)
        h = np.sin(2 * np.pi * np.cumsum(420 - 40 * t / 0.32) / SR) * np.sin(np.pi * t / 0.32) * 0.8
        return seq([h, h], 0.12)
    if kind == "munch":
        return seq([noise(0.08, 2)[:int(0.08 * SR)] * np.exp(-tt_(0.08) / 0.02) * 1.5 for _ in range(5)], 0.12)
    if kind == "groan":
        return growl(0.9, 140, 110, 0.4, vib=8) * 0.8
    if kind == "thump":
        t = tt_(0.2)
        th = np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.05)
        return seq([th] * 3, 0.3) * 1.3
    if kind == "snore":
        return seq([noise(0.5, 40)[:int(0.5 * SR)] * env(tt_(0.5), 0.5, 0.15, 0.2) * 4, tone(200, 160, 0.4) * 0.3], 0.3)
    if kind == "honk":
        return seq([tone(500, 560, 0.2, "sq"), tone(520, 580, 0.2, "sq")], 0.12)
    if kind == "snap":
        t = tt_(0.1)
        return seq([np.sin(2 * np.pi * 200 * t) * np.exp(-t / 0.02) + noise(0.1)[:len(t)] * np.exp(-t / 0.01)], 0.1) * 1.2
    if kind == "gallop":
        t = tt_(0.08)
        c = np.sin(2 * np.pi * 300 * t) * np.exp(-t / 0.02)
        return seq([c, c, c], 0.07) * 0.8
    return np.zeros(10)


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 116
    prog = [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]           # D Bm G A: adventure, sunny
    hook = [74, 78, 81, 78, 79, 76, 74, 0, 76, 79, 81, 83, 81, 78, 76, 0]
    bar, t0 = 0, 2.5
    while t0 < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = t0 + q * B
            A.add(mus, LS.kick(), b0, 0.48)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.28, 0.05)
                A.add(mus, RV.snare(), b0, 0.13)
            A.add(mus, LS.hat(), b0 + B / 2, 0.42, -0.3)
            for e in (0.25, 0.75):                                          # little bongo pattern, safari feel
                tb = tt_(0.12)
                A.add(mus, np.sin(2 * np.pi * (300 if e < 0.5 else 220) * tb) * np.exp(-tb / 0.05), b0 + e * B, 0.12, 0.3)
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):
                A.add(mus, A.tone(A.mtof(nt + 12), 0.3, ((1, 1), (3, 0.3), (5, 0.1)), 0.003, 0.1), b0 + B / 2, 0.045, -0.25 + 0.25 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, M.toy_piano(mm, 0.4), t0 + i * B / 2, 0.06, 0.2)
        t0 += 4 * B
        bar += 1
    ts = np.arange(n) / SR
    mus *= np.clip((total - ts) / 1.5, 0, 1)[:, None]
    g = np.ones(n)
    for s in T.scenes:
        if s["kind"] in ("sound", "animal") and "snd_t" in s:
            a, b = int((s["snd_t"] - 0.2) * SR), int((s["snd_t"] + 1.6) * SR)
            g[a:b] = np.minimum(g[a:b], 0.2 if s["kind"] == "sound" else 0.45)
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
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "engine":
            tq = tt_(1.2)
            x = np.sin(2 * np.pi * np.cumsum(55 + 15 * np.minimum(1, tq / 0.5)) / SR) * (0.7 + 0.3 * np.sin(2 * np.pi * 10 * tq)) * env(tq, 1.2, 0.1, 0.4)
            A.add(f, x, at, 0.45)
        elif kind == "stomp2":
            for k in range(3):
                A.add(f, M.stomp(), at + 0.2 + k * 0.35, 0.4)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "yes":
            A.add(f, A.sfx_ding(79), at, 0.2)
            A.add(f, A.sfx_ding(84), at + 0.12, 0.2)
        else:
            A.add(f, animal(kind), at, 0.6)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.15)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(86), p0, 0.1)
    mix = v + mus * 0.33 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    return mix


if __name__ == "__main__":
    build()
