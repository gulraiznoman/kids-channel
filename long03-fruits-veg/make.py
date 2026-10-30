"""Long video 3: "Learn Fruits and Vegetables Names for Kids" (market trip). Voices, timeline.json, mix.wav.

Formats (all different from Ep1 flashcards): cut-it-open reveal, pull-it-from-the-ground reveal,
fruit-or-vegetable sorting game, find-the-colour plate game, an original fruit rhyme, a cooking story.
All sounds are made in code. python make.py
"""
import hashlib, json, sys, pathlib
import numpy as np, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "voices"))
sys.path.insert(0, str(ROOT / "ep02-colours"))
sys.path.insert(0, str(ROOT / "song01-animal-dance"))
import kidvoice
import audio_mix as A
import music as M

SR = A.SR
CACHE = HERE / "words"
CACHE.mkdir(exist_ok=True)
PRAISE = ["Great job!", "Yay! You got it!", "Awesome!", "Well done!", "Super!", "You're so smart!", "Good job, friends!"]
QUESTIONS = ["Ooh, what fruit is this?", "What's this fruit?", "Do you know this fruit?", "Look! What fruit is it?"]

# key, name, article, fact after cutting (None = no cut)
FRUITS = [
    ("guava", "guava", "a", "Green outside, and pink inside!"),
    ("pomegranate", "pomegranate", "a", "So many juicy red seeds!"),
    ("papaya", "papaya", "a", "Orange inside, with little black seeds!"),
    ("peach", "peach", "a", "Soft and sweet, with a big seed in the middle!"),
    ("coconut", "coconut", "a", "Hard outside, white inside, with coconut water!"),
    ("blueberries", "blueberries", "", None),
    ("plum", "plum", "a", None),
    ("avocado", "avocado", "an", "Green inside, with a big brown seed!"),
]
FRUIT_EXTRA = {"blueberries": "Tiny, round, and blue!", "plum": "A purple plum! Sweet and juicy!"}
# key, name, grows (under = pull from soil, plant = pick), fact
VEG = [
    ("carrot", "carrot", "under", "Carrots grow under the ground!"),
    ("tomato", "tomato", "plant", "Tomatoes grow on a plant!"),
    ("potato", "potato", "under", "Potatoes hide under the ground too!"),
    ("corn", "corn", "plant", "Corn grows on a tall plant!"),
    ("onion", "onion", "under", "An onion! It grows under the ground!"),
    ("peas", "peas", "plant", "Little green peas live inside a pod!"),
    ("broccoli", "broccoli", "plant", "Broccoli looks like a little tree!"),
    ("cucumber", "cucumber", "plant", "A long, green cucumber! Crunch, crunch!"),
    ("eggplant", "eggplant", "plant", "A shiny purple eggplant!"),
    ("cabbage", "cabbage", "plant", "A big round cabbage, with lots of leaves!"),
    ("pumpkinveg", "pumpkin", "plant", "A big orange pumpkin grows on a vine!"),
]
# big or small: big key, small key, big word, small word
SIZES = [("watermelon", "grapes", "watermelon", "grapes"), ("pumpkinveg", "peas", "pumpkin", "peas"),
         ("coconut", "blueberries", "coconut", "blueberries"), ("pineapple", "cherry", "pineapple", "cherries"),
         ("cabbage", "tomato", "cabbage", "tomato")]
# mystery shadows: key, answer line
SHADOWS = [("pineapple", "A pineapple! It has a spiky crown!"), ("broccoli", "Broccoli! Like a little tree!"),
           ("banana", "A banana! Long and yellow!"), ("corn", "Corn! Pop, pop, popcorn!"),
           ("watermelon", "A watermelon slice! Red and juicy!"), ("eggplant", "An eggplant! Shiny and purple!"),
           ("coconut", "A coconut! Round and hairy!"), ("carrot", "A carrot! Crunchy and orange!")]
# sorting game: key, word, is_fruit
SORT = [("apple", "apple", True), ("carrot", "carrot", False), ("banana", "banana", True), ("broccoli", "broccoli", False),
        ("grapes", "grapes", True), ("potato", "potato", False), ("strawberry", "strawberry", True), ("corn", "corn", False)]
# rainbow plate: colour word, rgb, targets, distractor
PLATE = [
    ("red", (232, 53, 46), ["apple", "tomato", "strawberry"], "banana"),
    ("orange", (255, 148, 32), ["carrot", "orange", "papaya_half"], "peas"),
    ("yellow", (255, 214, 10), ["banana", "corn", "lemon"], "eggplant"),
    ("green", (60, 190, 80), ["broccoli", "peas", "cucumber"], "strawberry"),
    ("purple", (142, 68, 201), ["grapes", "eggplant", "plum"], "carrot"),
]
RHYME = [("mishu", "Apple, apple, red and round!", "apple"), ("gul", "Banana, banana, yellow and long!", "banana"),
         ("mishu", "Grapes, grapes, purple and sweet!", "grapes"), ("gul", "Orange, orange, a juicy treat!", "orange"),
         ("mishu", "Carrot, carrot, crunchy and bright!", "carrot"), ("gul", "Broccoli, broccoli, green and right!", "broccoli"),
         ("both", "Fruits and veggies, yummy and good!", None), ("both", "Eat them up, like we should!", None)]


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
        self.t, self.lines, self.scenes, self.voc, self.prompts, self.stars, self.fx = 1.0, [], [], {"gul": [], "mishu": []}, [], [], []

    def say(self, who, text, gap=0.4):
        singers = ["gul", "mishu"] if who == "both" else [who]
        d = 0
        for s in singers:
            x = line(s, text)
            self.voc[s].append((self.t, x * ((0.9 if s == "mishu" else 0.45) if who == "both" else 1.0)))
            d = max(d, len(x) / SR)
        start = round(self.t, 3)
        self.lines.append(dict(who=who, text=text, t=start, dur=round(d, 3)))
        self.t += d + gap
        return start

    def pause(self, s):
        self.t += s

    def scene(self, kind, bg, **data):
        sc = dict(kind=kind, bg=bg, t0=round(self.t, 3), **data)
        self.scenes.append(sc)
        return sc

    def end(self, sc):
        sc["t1"] = round(self.t, 3)

    def prompt(self, who, text, wait=2.4):
        self.say(who, text, gap=0.2)
        self.prompts.append((round(self.t, 3), round(self.t + wait, 3)))
        self.pause(wait)

    def mark(self, kind, extra=0):
        self.fx.append((kind, round(self.t, 3), extra))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("whoosh")
        self.pause(0.6)
        self.say(who, text, gap=0.6)
        self.end(sc)


def build():
    T = TL()
    # ---------------------------------------------------------------- intro: going to the market
    sc = T.scene("intro", "market")
    T.say("gul", "Hi friends! I'm Gul!")
    T.say("mishu", "And I'm Mishu! Today we're going to the market!")
    T.say("gul", "Let's fill our basket with fruits and vegetables!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- fruit stall: cut it open
    T.title("market", "FRUIT STALL!", "mishu", "First, the fruit stall! So many fruits!")
    basket = []
    for k, (key, name, art, fact) in enumerate(FRUITS):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("fruit", "market", key=key, name=name.upper(), basket=list(basket))
        T.mark("pop")
        T.pause(0.8)
        T.prompt(a, QUESTIONS[k % len(QUESTIONS)], wait=2.6)
        sc["label_t"] = T.say(b, f"It's {art} {name}!" if art else f"They're {name}!", gap=0.3)
        T.say(a, f"Can you say {name}?", gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.8, 3)))
        T.pause(1.8)
        if fact:
            T.say(b, "Let's cut it open!", gap=0.2)
            sc["cut_t"] = T.mark("chop")
            T.pause(0.9)
            T.say(a, fact, gap=0.4)
        else:
            T.say(b, FRUIT_EXTRA[key], gap=0.4)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[k % len(PRAISE)], gap=0.3)
        sc["drop_t"] = T.mark("drop")
        T.pause(1.0)
        basket.append(key)
        T.end(sc)
    # ---------------------------------------------------------------- vegetable patch: pull it out
    T.title("patch", "VEGETABLE PATCH!", "gul", "Now let's pick vegetables from the garden!")
    for k, (key, name, grows, fact) in enumerate(VEG):
        a, b = ("gul", "mishu") if k % 2 == 0 else ("mishu", "gul")
        sc = T.scene("veg", "patch", key=key, name=name.upper(), grows=grows)
        T.pause(0.7)
        T.prompt(a, "What's growing here?" if k % 2 == 0 else "Ooh, what is this one?", wait=2.6)
        T.say(b, "Let's pull it out!" if grows == "under" else "Let's pick it!", gap=0.2)
        sc["pull_t"] = T.mark("pull")
        T.pause(1.0)
        sc["label_t"] = T.say(a, f"{'Peas' if key == 'peas' else 'Corn' if key == 'corn' else 'Broccoli' if key == 'broccoli' else ('An ' if name[0] in 'aeiou' else 'A ') + name}!", gap=0.3)
        T.say(b, f"Can you say {name}?", gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.8, 3)))
        T.pause(1.8)
        T.say(a, fact, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.say(b, PRAISE[(k + 3) % len(PRAISE)], gap=0.3)
        sc["drop_t"] = T.mark("drop")
        T.pause(0.9)
        T.end(sc)
    # ---------------------------------------------------------------- mystery shadows (guess the shape)
    T.title("market", "MYSTERY SHADOWS!", "gul", "Can you guess the food from its shadow?")
    for k, (key, ans) in enumerate(SHADOWS):
        a, b = ("gul", "mishu") if k % 2 == 0 else ("mishu", "gul")
        sc = T.scene("shadow", "market", key=key)
        T.mark("pop")
        T.pause(0.7)
        T.prompt(a, "Whose shadow is this?" if k % 2 == 0 else "Hmm, what could it be?", wait=2.8)
        sc["reveal_t"] = T.mark("sparkle")
        T.pause(0.5)
        T.say(b, ans, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[(k + 2) % len(PRAISE)], gap=0.7)
        T.end(sc)
    # ---------------------------------------------------------------- fruit or vegetable? (sorting game)
    T.title("market", "FRUIT OR VEGETABLE?", "mishu", "Let's play a game! Is it a fruit, or a vegetable?")
    for k, (key, word, is_fruit) in enumerate(SORT):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("sort", "market", key=key, fruit=is_fruit, done=[(s[0], s[2]) for s in SORT[:k]])
        T.mark("pop")
        T.pause(0.7)
        T.prompt(a, f"The {word}! Fruit, or vegetable?", wait=2.8)
        sc["answer_t"] = T.say(b, f"{'It is' if word != 'grapes' else 'They are'} a fruit!" if is_fruit else
                               f"{'It is' if word != 'grapes' else 'They are'} a vegetable!", gap=0.2)
        sc["fly_t"] = T.mark("drop")
        T.pause(1.0)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[(k + 1) % len(PRAISE)], gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- big or small? (comparing sizes)
    T.title("market", "BIG OR SMALL?", "gul", "Big kids, which one is bigger? Let's compare!")
    for k, (big, small, bw, sw) in enumerate(SIZES):
        a, b = ("gul", "mishu") if k % 2 == 0 else ("mishu", "gul")
        flip = k % 2 == 1                                   # big one sometimes on the right
        sc = T.scene("size", "market", big=big, small=small, flip=flip)
        T.mark("pop")
        T.pause(0.7)
        T.prompt(a, f"The {bw}, or the {sw}? Which one is bigger?", wait=2.6)
        sc["answer_t"] = T.say(b, f"The {bw} is big!", gap=0.2)
        sc["small_t"] = T.say(b, f"The {sw} {'are' if sw.endswith('s') else 'is'} small!", gap=0.3)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[(k + 4) % len(PRAISE)], gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- rainbow plate (find the colour)
    T.title("kitchen", "RAINBOW PLATE!", "gul", "Fruits and vegetables come in every colour! Let's make a rainbow plate!")
    plate = []
    for k, (cname, rgb, targets, other) in enumerate(PLATE):
        a, b = ("gul", "mishu") if k % 2 == 0 else ("mishu", "gul")
        items = targets[:2] + [other] + targets[2:]
        sc = T.scene("plate", "kitchen", colour=cname, rgb=rgb, items=items, other=other, plate=list(plate))
        T.pause(0.8)
        T.prompt(a, f"Can you find the {cname} ones?", wait=3.0)
        sc["show_t"] = T.mark("ding")
        T.say(b, f"{', '.join(t.replace('_half', '').replace('papaya', 'papaya') for t in targets[:-1])}, and {targets[-1].replace('_half', '')}!", gap=0.3)
        sc["move_t"] = T.mark("drop")
        T.pause(1.0)
        T.say(a, f"{cname.capitalize()} foods! {PRAISE[k % len(PRAISE)]}", gap=0.6)
        T.stars.append(round(T.t - 0.6, 3))
        plate += [(t, cname) for t in targets]
        T.end(sc)
    sc = T.scene("plate_done", "kitchen", plate=list(plate))
    T.say("mishu", "Look! A whole rainbow on our plate!", gap=0.4)
    T.say("gul", "Eating the rainbow makes us strong!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- our own fruit rhyme
    T.title("market", "FRUIT RHYME!", "mishu", "Now let's say our fruit rhyme! Clap along!")
    sc = T.scene("rhyme", "market", items=[])
    T.pause(0.4)
    times = []
    for who, text, key in RHYME:
        T.mark("clap")
        times.append((T.say(who, text, gap=0.45), key, text))
    sc["lines"] = times
    T.pause(0.4)
    T.say("gul", "Yay! Great clapping, friends!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- cooking story
    T.title("kitchen", "LET'S COOK!", "gul", "Let's use our basket and cook something yummy!")
    sc = T.scene("cook", "kitchen", dish="bowl", items=["guava_half", "banana", "blueberries", "pomegranate_half", "peach_half"])
    T.say("mishu", "First, a fruit salad!", gap=0.3)
    drops = []
    for key, word in (("guava_half", "Guava"), ("banana", "banana"), ("blueberries", "blueberries"), ("pomegranate_half", "pomegranate"), ("peach_half", "and peach!")):
        drops.append(T.mark("plop"))
        T.say("gul" if len(drops) % 2 else "mishu", word + ("!" if not word.endswith("!") else ""), gap=0.35)
    sc["drops"] = drops
    sc["stir_t"] = T.say("mishu", "Stir, stir, stir!", gap=0.3)
    T.mark("sparkle")
    T.say("gul", "Mmm! A yummy fruit salad!", gap=0.8)
    T.end(sc)
    sc = T.scene("cook", "kitchen", dish="pot", items=["carrot", "potato", "peas", "corn", "tomato"])
    T.say("gul", "Now, vegetable soup!", gap=0.3)
    drops = []
    for key, word in (("carrot", "Carrot"), ("potato", "potato"), ("peas", "peas"), ("corn", "corn"), ("tomato", "and tomato!")):
        drops.append(T.mark("splash"))
        T.say("mishu" if len(drops) % 2 else "gul", word + ("!" if not word.endswith("!") else ""), gap=0.35)
    sc["drops"] = drops
    sc["stir_t"] = T.say("gul", "Bubble, bubble, bubble!", gap=0.3)
    T.mark("sparkle")
    T.say("mishu", "Hot and healthy soup! Yum!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- outro
    sc = T.scene("outro", "market", basket=[f[0] for f in FRUITS])
    T.say("mishu", "We learned so many fruits and vegetables today!")
    T.say("gul", "Which one is your favourite? Mine is the coconut!", gap=0.5)
    sc["bye_t"] = T.say("both", "Bye bye, friends!", gap=0.4)
    T.say("mishu", "See you next time!", gap=2.0)
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

    # ---------------------------------------------------------------- music: new key (F), slower 96 BPM, marimba-led (different from L01/L02)
    mus = np.zeros((n, 2))
    B = 60 / 96
    prog = [[65, 69, 72], [62, 65, 69], [70, 74, 77], [72, 76, 79]]          # F, Dm, Bb, C
    tune = [77, 81, 84, 81, 79, 77, 74, 0, 74, 77, 79, 81, 79, 77, 72, 0]
    i, tt = 0, 0.0
    while tt < total:
        ch = prog[(i // 4) % 4]
        if i % 4 == 0:
            A.add(mus, M.tuba(ch[0] - 24, B * 1.6), tt, 0.15)
        A.add(mus, M.xylo(ch[i % 3] + 12, 0.3), tt + B / 2, 0.035, -0.3)
        if (i // 16) % 2 == 1 and tune[i % 16]:
            A.add(mus, M.toy_piano(tune[i % 16]), tt, 0.028, 0.3)
        A.add(mus, M.shaker(), tt + B / 2, 0.03, 0.4)
        tt += B
        i += 1
    ts = np.arange(n) / SR
    mus *= (np.clip(ts / 1.0, 0, 1) * np.clip((total - ts) / 2.0, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.15)
    A.add(v, tracks["mishu"], 0, 1.0, 0.15)
    v /= np.abs(v).max() / 0.9
    e = np.abs(v).mean(axis=1)
    win = int(0.1 * SR)
    e = np.convolve(e, np.ones(win) / win, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.4 * e)[:, None]
    rng = np.random.default_rng(4)

    def noise(d, lp):
        x = rng.standard_normal(int(d * SR))
        return np.convolve(x, np.ones(lp) / lp, mode="same")

    def chop():
        n2 = int(0.25 * SR)
        t = np.arange(n2) / SR
        thud = np.sin(2 * np.pi * np.cumsum(140 * np.exp(-t / 0.04) + 60) / SR) * np.exp(-t / 0.06)
        return thud + noise(0.25, 3)[:n2] * np.exp(-t / 0.015) * 0.6

    def splash():
        n2 = int(0.6 * SR)
        t = np.arange(n2) / SR
        return noise(0.6, 6)[:n2] * np.exp(-t / 0.15) * np.minimum(1, t / 0.01) * 1.5

    def clap():
        return M.clap()

    f = np.zeros((n, 2))
    for kind, at, _ in T.fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.25)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.15)
        elif kind == "chop":
            A.add(f, chop(), at + 0.25, 0.6)
            A.add(f, A.sfx_sparkle(), at + 0.35, 0.12)
        elif kind == "pull":
            A.add(f, M.boing(), at + 0.2, 0.35)
            A.add(f, A.sfx_pop(), at + 0.45, 0.3)
        elif kind == "drop":
            A.add(f, M.xylo(79), at + 0.5, 0.2)
            A.add(f, M.xylo(84), at + 0.62, 0.2)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "clap":
            A.add(f, clap(), at, 0.4)
            A.add(f, clap(), at + 0.3, 0.3)
        elif kind == "plop":
            A.add(f, A.sfx_pop(), at + 0.3, 0.3)
        elif kind == "splash":
            A.add(f, splash(), at + 0.35, 0.4)
        elif kind == "sparkle":
            A.add(f, A.sfx_sparkle(), at, 0.25)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.15)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(86), p0, 0.1)
    mix = v + mus * 0.22 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    sf.write(HERE / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s ({total / 60:.1f} min), {len(T.lines)} lines, {len(T.scenes)} scenes")


if __name__ == "__main__":
    build()
