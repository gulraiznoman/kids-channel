"""Long video 11: "Bath Time & Sink or Float". Voices, timeline.json, mix.wav (own music + own water sounds).
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

NEED = [("towel", "A soft towel, to dry off!"), ("soap", "Soap, to wash our body!"), ("shampoo", "Shampoo, to wash our hair!"),
        ("sponge", "A squishy sponge!"), ("duck", "And a rubber duck! Squeak squeak!"), ("pyjamas", "Cozy pyjamas, for after the bath!")]
WASH = [("hand", "hands"), ("arm", "arms"), ("leg", "legs"), ("foot", "feet"), ("ear", "ears"), ("face", "face"), ("hair", "hair")]
SINK = [("duck", "float", "The rubber duck floats! It's light, and full of air."), ("rock", "sink", "The rock sinks! It's heavy."),
        ("apple", "float", "Surprise! The apple floats! It has air inside."), ("key", "sink", "The key sinks! Metal is heavy."),
        ("sponge", "float", "The sponge floats! It has lots of tiny air holes."), ("coin", "sink", "The coin sinks, all the way down!"),
        ("ball", "float", "The ball floats! It's full of air."), ("spoon", "sink", "The spoon sinks!"),
        ("leaf", "float", "The leaf floats, like a little boat!"), ("egg", "sink", "The egg sinks!"),
        ("orange", "float", "Wow! The orange floats! Its peel is full of air."), ("grapes", "sink", "The grapes sink!"),
        ("banana", "float", "The banana floats!"), ("carrot", "sink", "The carrot sinks!")]
SWIM = [("duckling", "A duckling can swim! Quack quack!"), ("fish", "A fish swims all day! Blub blub!"), ("frog", "A frog can swim, and jump! Ribbit!"),
        ("turtle", "A sea turtle swims in the sea!"), ("penguin", "A penguin swims super fast!"), ("dolphin", "A dolphin jumps and splashes!"),
        ("octopus", "An octopus swims with eight arms!"), ("crab", "A crab walks sideways in the water!"), ("whale", "And a big whale! Splash!")]
OPP = [("hot", "cold", "sunny", "snowy", "Hot and cold! Bath water should be warm, in the middle!"), ("wet", "dry", "drop", "towel", "Wet and dry!"),
       ("dirty", "clean", "dirt", "soap", "Dirty and clean!"), ("big", "small", "bigbubble", "smallbubble", "Big and small bubbles!")]
SURPRISE = [("fish", "A fish!"), ("boat", "A boat!"), ("apple", "An apple!"), ("whale", "A whale!"), ("ball", "A ball!"),
            ("duckling", "A duckling!"), ("starfish", "A starfish!"), ("frog", "A frog! Ribbit!")]
SIZES = [("big", "Which bubble is bigger?"), ("small", "Which bubble is smaller?"), ("big", "Which bubble is the biggest?")]
POPCOL = [("red", "Pop the red bubble!"), ("blue", "Pop the blue bubble!"), ("yellow", "Pop the yellow bubble!"),
          ("green", "Pop the green bubble!"), ("purple", "Pop the purple bubble!"), ("orange", "Pop the orange bubble!"), ("pink", "Pop the pink bubble!")]
TOYS = [("squeak", "duck", "Squeak squeak! The rubber duck!"), ("toot", "boat", "Toot toot! The boat!"),
        ("spray", "whale", "Psssh! The whale sprays water!"), ("blub", "fish", "Blub blub! The fish!")]
DANCE = [("Scrub your arms! Scrub, scrub, scrub!", "scrub"), ("Splash, splash, splash!", "splash"), ("Shake like a wet puppy!", "shake"),
         ("Pop the bubbles! Pop, pop, pop!", "pop"), ("Wiggle your toes!", "wiggle"), ("Dry off with your towel!", "dry")]
QUIZ = [("Does a rock sink or float?", "It sinks!", "rock"), ("Who should be with you at bath time?", "A grown-up!", "grownup"),
        ("What do we use to wash our hair?", "Shampoo!", "shampoo"), ("Does a rubber duck sink or float?", "It floats!", "duck"),
        ("What do we use to dry off?", "A towel!", "towel"), ("Why does an apple float?", "It has air inside!", "apple"),
        ("Does a banana sink or float?", "It floats!", "banana"), ("Why do we take a bath?", "To wash away dirt and germs!", "soap"),
        ("Should bath water be hot or warm?", "Just warm!", "sunny"), ("Does an orange sink or float?", "It floats!", "orange"),
        ("Who can swim, a fish or a rock?", "A fish!", "fish"), ("What makes lots of bubbles?", "Soap!", "soap")]


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

    def title(self, title, who, text):
        sc = self.scene("title", "bath", title=title)
        self.mark("riser")
        self.pause(0.5)
        self.say(who, text, gap=0.3)
        self.end(sc)


def other(w):
    return "mishu" if w == "gul" else "gul"


def build():
    T = TL()
    # ---------------------------------------------------------------- OPENING: bubbles burst out of the tub, duck squeaks
    sc = T.scene("intro", "bath")
    sc["burst_t"] = T.mark("burst")
    T.pause(1.0)
    sc["duck_t"] = T.mark("squeak")
    T.pause(0.6)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Bath time!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Bubbles, splashes, and a big science test!", gap=0.2)
    T.say("gul", "Will it sink, or float? Let's find out!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- MUDDY GUL (why we take a bath)
    sc = T.scene("muddy", "bath")
    sc["mud_t"] = T.mark("splash")
    T.say("mishu", "Oh no, Gul! You're all muddy!", gap=0.2)
    T.say("gul", "I jumped in the mud puddles! Splash, splash!", gap=0.2)
    sc["germ_t"] = T.say("mishu", "Baths wash away dirt and germs, and keep us healthy.", gap=0.2)
    T.say("gul", "Then it's bath time! Yay!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- WHAT DO WE NEED?
    T.title("WHAT DO WE NEED?", "gul", "Let's get ready for bath time! What do we need?")
    for k, (key, text) in enumerate(NEED):
        sc = T.scene("need", "bath", key=key, done=[n[0] for n in NEED[:k]], num=k + 1)
        T.mark("pop")
        T.pause(0.2)
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- FILL THE BATH (safety)
    sc = T.scene("fill", "bath")
    sc["tap_t"] = T.mark("tap")
    T.say("gul", "Turn on the water. Splish, splash!", gap=0.2)
    sc["check_t"] = T.say("mishu", "Always have a grown-up check the water.", gap=0.2)
    T.say("gul", "Not too hot, not too cold. Just warm!", gap=0.2)
    sc["rule_t"] = T.say("both", "And never play in water alone!", gap=0.4)
    sc["jump_t"] = T.mark("splash")
    T.say("mishu", "Now, hop in! Splash!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- THIS IS THE WAY (traditional rhyme, spoken)
    sc = T.scene("thisway", "bath")
    sc["l"] = []
    for text in ("This is the way we wash our hands,", "wash our hands, wash our hands!", "This is the way we wash our hands,", "so early in the morning!"):
        sc["l"].append(T.say("both", text, gap=0.15))
    T.pause(0.3)
    T.end(sc)
    # ---------------------------------------------------------------- WASH WASH chant
    T.title("WASH, WASH, WASH!", "mishu", "Let's wash from top to toes! Copy us!")
    for k, (key, part) in enumerate(WASH):
        sc = T.scene("wash", "bath", key=key, part=part)
        T.mark("scrub")
        if part == "hair":
            sc["say_t"] = T.say("both", "Wash, wash, wash your hair! Close your eyes!", gap=0.1)
        else:
            sc["say_t"] = T.say("both", f"Wash, wash, wash your {part}!", gap=0.1)
        T.say("gul" if k % 2 == 0 else "mishu", "Scrub, scrub, scrub!" if k % 2 == 0 else "Rub, rub, rub!", gap=0.4)
        T.end(sc)
    sc = T.scene("rinse", "bath")
    sc["pour_t"] = T.mark("pour")
    T.say("gul", "Now rinse off all the bubbles. Whoosh!", gap=0.2)
    T.say("mishu", "Squeaky clean!", gap=0.5)
    T.stars.append(round(T.t - 0.6, 3))
    T.end(sc)
    # ---------------------------------------------------------------- POP AND COUNT BUBBLES
    T.title("POP THE BUBBLES!", "gul", "So many bubbles! Let's pop them and count!")
    sc = T.scene("bubbles", "bath")
    pops = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!", "Six!", "Seven!", "Eight!", "Nine!", "Ten!"):
        pops.append(T.mark("bubblepop"))
        T.say("both", w, gap=0.1)
    sc["pops"] = pops
    T.say("mishu", "Ten bubbles! Pop, pop, pop!", gap=0.5)
    T.end(sc)
    for k, (col, text) in enumerate(POPCOL):
        sc = T.scene("popcol", "bath", col=col)
        T.prompt("gul" if k % 2 == 0 else "mishu", text, wait=1.6)
        sc["pop_t"] = T.mark("bubblepop")
        T.say("mishu" if k % 2 == 0 else "gul", f"Pop! {col.capitalize()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BIG OR SMALL BUBBLE
    for k, (ans, q) in enumerate(SIZES):
        sc = T.scene("bubsize", "bath", ans=ans, n=3 if k == 2 else 2)
        T.prompt("mishu" if k % 2 == 0 else "gul", q, wait=1.6)
        sc["answer_t"] = T.mark("bubblepop")
        T.say("gul" if k % 2 == 0 else "mishu", "This one!" if k < 2 else "The giant one! Wow!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- COUNT THE DUCKS
    sc = T.scene("ducks", "bath")
    T.say("gul", "Let's count the rubber ducks!", gap=0.1)
    dts = []
    for w in ("One!", "Two!", "Three!", "Four!", "Five!"):
        dts.append(T.mark("squeak"))
        T.say("both", w, gap=0.2)
    sc["dts"] = dts
    T.say("mishu", "Five little ducks, squeak, squeak!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- RUB-A-DUB-DUB (our version of the traditional rhyme)
    sc = T.scene("rubadub", "bath")
    sc["l1"] = T.say("both", "Rub-a-dub-dub, three ducks in a tub!", gap=0.3)
    sc["l2"] = T.say("both", "Rub-a-dub-dub, splash, splash, splash!", gap=0.3)
    sc["l3"] = T.say("both", "Rub-a-dub-dub, three ducks in a tub!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- BUBBLE SURPRISE
    T.title("BUBBLE SURPRISE!", "gul", "Something is hiding in the bubbles! Pop them!")
    for k, (key, ans) in enumerate(SURPRISE):
        sc = T.scene("surprise", "bath", key=key)
        T.prompt("mishu" if k % 2 == 0 else "gul", "Pop! What's inside?", wait=1.4)
        sc["pop_t"] = T.mark("bubblepop")
        T.pause(0.3)
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- SINK OR FLOAT (science)
    T.title("SINK OR FLOAT?", "mishu", "Science time! Will it sink to the bottom, or float on top?")
    sc = T.scene("sinkintro", "bath")
    T.say("gul", "Things that float stay on top of the water.", gap=0.2)
    T.say("mishu", "Things that sink go down, down, down!", gap=0.4)
    T.end(sc)
    for k, (key, res, text) in enumerate(SINK):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sink", "bath", key=key, res=res, done=[(x[0], x[1]) for x in SINK[:k]])
        T.mark("pop")
        T.prompt(a, f"Will the {key} sink or float?", wait=2.0)
        sc["drop_t"] = T.mark("plop" if res == "sink" else "splash")
        T.pause(1.1)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    sc = T.scene("sinksum", "bath", done=[(x[0], x[1]) for x in SINK])
    T.say("gul", "Light things with air inside float.", gap=0.2)
    T.say("mishu", "Heavy things sink! You're a scientist!", gap=0.5)
    T.stars.append(round(T.t - 0.8, 3))
    T.end(sc)
    # ---------------------------------------------------------------- WHO CAN SWIM?
    T.title("WHO CAN SWIM?", "mishu", "Look! Friends who love water are visiting our bath!")
    for k, (animal, text) in enumerate(SWIM):
        sc = T.scene("swim", "bath", animal=animal)
        T.mark("splash")
        T.pause(0.3)
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BATH TOY SOUNDS
    T.title("WHICH BATH TOY?", "gul", "Listen! Which bath toy makes this sound?")
    for k, (snd, toy, ans) in enumerate(TOYS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("toy", "bath", toy=toy)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.4)
        T.prompt(a, "Which toy is it?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BATH OPPOSITES
    T.title("BATH OPPOSITES!", "mishu", "Big kids! Let's find opposites in the bath!")
    for k, (w1, w2, i1, i2, text) in enumerate(OPP):
        sc = T.scene("opp", "bath", w1=w1, w2=w2, i1=i1, i2=i2)
        T.mark("pop")
        sc["a_t"] = T.say("gul" if k % 2 == 0 else "mishu", f"{w1.capitalize()}!", gap=0.3)
        sc["b_t"] = T.mark("pop")
        T.say("mishu" if k % 2 == 0 else "gul", f"{w2.capitalize()}!", gap=0.2)
        T.say("both", text, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- DOWN THE DRAIN
    sc = T.scene("drain", "bath")
    sc["drain_t"] = T.mark("drain")
    T.say("mishu", "Bath time is over. Pull the plug!", gap=0.2)
    T.say("both", "Glug, glug, glug! Bye bye, bubbles!", gap=0.6)
    T.end(sc)
    # ---------------------------------------------------------------- WHAT COMES FIRST? (order)
    T.title("WHAT COMES FIRST?", "mishu", "Big kids! What do we do after the bath?")
    sc = T.scene("order", "bath")
    T.prompt("gul", "Towel, pyjamas, or brushing teeth? What comes first?", wait=2.4)
    sc["o1"] = T.say("mishu", "First, dry off with a towel!", gap=0.2)
    sc["o2"] = T.say("gul", "Next, put on cozy pyjamas!", gap=0.2)
    sc["o3"] = T.say("mishu", "Last, brush your teeth!", gap=0.3)
    T.say("both", "First, next, last! Great job!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- BATH DANCE x2
    T.title("BATH DANCE!", "gul", "Stand up! Let's do the bath dance! Copy us!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "bath", title="FASTER!")
            T.mark("riser")
            T.say("mishu", "Again, faster!", gap=0.2)
            T.end(sc)
        for text, move in DANCE:
            sc = T.scene("dance", "bath", move=move, fast=rnd == 1, word=text.split("!")[0].upper() + "!")
            T.mark("splash" if move == "splash" else "pop")
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- QUIZ
    T.title("BATH QUIZ!", "mishu", "Big kids quiz! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("quiz", "bath", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "bath")
    T.say("mishu", "Bath time is so much fun! Now we're squeaky clean!", gap=0.2)
    T.say("gul", "Next bath time, try sink or float with a grown-up!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends! Squeak squeak!", gap=1.8)
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


# ==================================================================== music + water sounds (all made in code)
rng = np.random.default_rng(11)


def tt_(d):
    return np.arange(int(d * SR)) / SR


def noise(d, lp=1):
    x = rng.standard_normal(int(d * SR))
    return np.convolve(x, np.ones(lp) / lp, mode="same") if lp > 1 else x


def bubblepop():
    t = tt_(0.12)
    return np.sin(2 * np.pi * np.cumsum(500 + 2500 * t / 0.12) / SR) * np.exp(-t / 0.03) * 0.8


def splash():
    d = 0.9
    t = tt_(d)
    x = noise(d, 3) * np.exp(-t / 0.25) * 0.8
    for k in range(6):
        a = int(rng.uniform(0.05, 0.5) * SR)
        b = bubblepop()
        x[a:a + len(b)] += b[: len(x) - a] * 0.5
    return x


def plop():
    t = tt_(0.35)
    return np.sin(2 * np.pi * np.cumsum(300 - 200 * t / 0.35) / SR) * np.exp(-t / 0.08) + noise(0.35, 6)[:len(t)] * np.exp(-t / 0.05) * 0.6


def tap(d=2.5):
    t = tt_(d)
    return noise(d, 4) * 0.35 * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.4)


def drain(d=3.0):
    t = tt_(d)
    x = np.zeros(len(t))
    for k in range(int(d * 6)):
        a = int(k / 6 * SR + rng.uniform(0, 0.08) * SR)
        f0 = rng.uniform(150, 260)
        tb = tt_(0.12)
        b = np.sin(2 * np.pi * np.cumsum(f0 + 400 * tb / 0.12) / SR) * np.exp(-tb / 0.04)
        x[a:a + len(b)] += b[: len(x) - a] * 0.7
    return x + noise(d, 60)[:len(t)] * 3 * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.5)


def squeak():
    out = []
    for k in range(2):
        t = tt_(0.18)
        out += [np.sin(2 * np.pi * np.cumsum(1300 + 500 * np.sin(np.pi * t / 0.18)) / SR) * np.minimum(1, t / 0.01) * np.minimum(1, (0.18 - t) / 0.03) * 0.6,
                np.zeros(int(0.1 * SR))]
    return np.concatenate(out)


def toot():
    out = []
    for d in (0.3, 0.6):
        t = tt_(d)
        out += [(np.sign(np.sin(2 * np.pi * 330 * t)) * 0.3 + np.sin(2 * np.pi * 660 * t) * 0.2) * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05),
                np.zeros(int(0.12 * SR))]
    return np.concatenate(out)


def spray():
    t = tt_(1.0)
    return np.diff(np.concatenate([[0], noise(1.0)])) * 0.35 * np.minimum(1, t / 0.05) * np.minimum(1, (1.0 - t) / 0.3)


def blub():
    out = np.zeros(int(0.8 * SR))
    for k in range(3):
        b = bubblepop() * 0.8
        a = int(k * 0.22 * SR)
        out[a:a + len(b)] += b
    return out


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 112
    prog = [[63, 67, 70], [60, 63, 67], [56, 60, 63], [58, 62, 65]]           # Eb Cm Ab Bb: splashy, warm
    hook = [75, 79, 82, 79, 80, 77, 75, 0, 77, 80, 82, 84, 82, 79, 77, 0]
    bar, t0 = 0, 3.4
    while t0 < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = t0 + q * B
            A.add(mus, LS.kick(), b0, 0.46)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.28, 0.05)
                A.add(mus, RV.snare(), b0, 0.13)
            A.add(mus, LS.hat(), b0 + B / 2, 0.42, -0.3)
            A.add(mus, bubblepop() * 0.4, b0 + B * 0.75, 0.08, 0.4)                # little bubble tick on the off-beat
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):
                A.add(mus, A.tone(A.mtof(nt + 12), 0.3, ((1, 1), (2, 0.3), (3, 0.15)), 0.004, 0.12), b0 + B / 2, 0.045, -0.25 + 0.25 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, M.toy_piano(mm, 0.4), t0 + i * B / 2, 0.06, 0.2)
        t0 += 4 * B
        bar += 1
    ts = np.arange(n) / SR
    mus *= np.clip((total - ts) / 1.5, 0, 1)[:, None]
    g = np.ones(n)                                                     # quiet while listening for toy sounds
    for s in T.scenes:
        if s["kind"] == "toy":
            a, b = int((s["snd_t"] - 0.3) * SR), int((s["snd_t"] + 1.5) * SR)
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
        elif kind == "burst":
            A.add(f, LS.kick() * 1.2, at, 0.8)
            for k in range(14):
                A.add(f, bubblepop(), at + k * 0.06, 0.35, float(rng.uniform(-0.6, 0.6)))
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "bubblepop":
            A.add(f, bubblepop(), at + 0.1, 0.6)
        elif kind == "splash":
            A.add(f, splash(), at, 0.6)
        elif kind == "plop":
            A.add(f, plop(), at + 0.5, 0.7)
        elif kind == "tap":
            A.add(f, tap(), at, 0.5)
        elif kind == "pour":
            A.add(f, tap(1.6), at, 0.5)
        elif kind == "drain":
            A.add(f, drain(), at, 0.6)
        elif kind == "scrub":
            m2 = int(1.6 * SR)
            A.add(f, noise(1.6, 3)[:m2] * (0.5 + 0.5 * np.abs(np.sin(np.linspace(0, 16, m2)))) * 0.25, at + 0.2, 0.35)
        elif kind == "squeak":
            A.add(f, squeak(), at, 0.6)
        elif kind == "toot":
            A.add(f, toot(), at, 0.6)
        elif kind == "spray":
            A.add(f, spray(), at, 0.6)
        elif kind == "blub":
            A.add(f, blub(), at, 0.6)
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
