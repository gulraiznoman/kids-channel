"""Long video 2: "Count 1 to 10 for Toddlers" (~10-11 min). Builds voices, timeline.json and mix.wav.

Formats (so it is not one template on repeat): number intro with count-along, "how many?" rounds
(fruits, farm, vehicles, pumpkins), a traditional counting rhyme, and a rocket countdown.
python make.py
"""
import hashlib, json, subprocess, sys, pathlib
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
NUM = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
PRAISE = ["Great job!", "Yay! Well done!", "Awesome!", "Super counting!", "You did it!", "Good job, friends!"]

# number, art key, phrase, fun line
NUMBERS = [
    (1, "elephant", "One big elephant!", "Toot, toot!"),
    (2, "bunny", "Two little bunnies!", "Hop, hop!"),
    (3, "duckling", "Three ducklings!", "Quack, quack!"),
    (4, "chick", "Four chicks!", "Cheep, cheep!"),
    (5, "fish", "Five fish!", "Blub, blub!"),
    (6, "star", "Six stars!", "Twinkle, twinkle!"),
    (7, "heart", "Seven hearts!", "I love you!"),
    (8, "apple", "Eight apples!", "Crunch, crunch!"),
    (9, "strawberry", "Nine strawberries!", "Yummy!"),
    (10, "car", "Ten little cars!", "Beep, beep!"),
]
# section title, background, intro line, rounds (art key, plural word, count)
ROUNDS = [
    ("COUNT THE FRUITS!", "garden", ("mishu", "Now let's count some yummy fruits!"),
     [("orange", "oranges", 2), ("banana", "bananas", 5), ("grapes", "bunches of grapes", 3), ("pear", "pears", 4),
      ("watermelon", "watermelons", 6), ("cherry", "cherries", 7), ("lemon", "lemons", 8), ("kiwi", "kiwis", 9)]),
    ("COUNT THE ANIMALS!", "farm", ("gul", "Let's go to the farm and count the animals!"),
     [("calf", "cows", 2), ("piglet", "piglets", 3), ("lamb", "lambs", 5), ("puppy", "puppies", 4),
      ("kitten", "kittens", 6), ("duckling", "ducklings", 7), ("chick", "chicks", 9), ("bunny", "bunnies", 10)]),
    ("COUNT THE VEHICLES!", "road", ("mishu", "Beep, beep! Let's count the vehicles!"),
     [("bus", "buses", 2), ("firetruck", "fire trucks", 3), ("tractor", "tractors", 4), ("police", "police cars", 5),
      ("train", "trains", 1), ("car", "cars", 6)]),
    ("COUNT THE PUMPKINS!", "halloween", ("gul", "It's almost Halloween! Let's count!"),
     [("pumpkin", "pumpkins", 3), ("bat", "bats", 5), ("ghost", "friendly ghosts", 2), ("jackolantern", "jack-o'-lanterns", 4),
      ("blackcat", "black cats", 6)]),
]

# adding: art key, singular, plural, left count, right count
ADDS = [("apple", "apple", "apples", 1, 1), ("banana", "banana", "bananas", 2, 1), ("duckling", "duckling", "ducklings", 2, 2),
        ("star", "star", "stars", 3, 2), ("car", "car", "cars", 4, 2), ("strawberry", "strawberry", "strawberries", 3, 4)]


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
        start = self.t
        self.lines.append(dict(who=who, text=text, t=round(start, 3), dur=round(d, 3)))
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

    def count(self, who, n, step_gap=0.22):
        times = []
        for i in range(n):
            times.append(round(self.say(who, NUM[i] + "!", gap=step_gap), 3))
            self.fx.append(("ding", self.t - step_gap, i))
        return times

    def prompt(self, who, text, wait=2.6):
        self.say(who, text, gap=0.2)
        self.prompts.append((round(self.t, 3), round(self.t + wait, 3)))
        self.pause(wait)


def build():
    T = TL()
    other = lambda w: "mishu" if w == "gul" else "gul"
    # ---------------------------------------------------------------- intro
    sc = T.scene("intro", "rainbow")
    T.say("gul", "Hi friends! I'm Gul!")
    T.say("mishu", "And I'm Mishu! Today let's count from one to ten!")
    T.say("gul", "Ready? Let's count together!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- numbers 1 to 10
    sc = T.scene("title", "rainbow", title="NUMBERS 1 TO 10!")
    T.pause(0.6)
    T.say("mishu", "First, let's meet the numbers!", gap=0.6)
    T.end(sc)
    for k, (n, key, phrase, fun) in enumerate(NUMBERS):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("number", "rainbow", n=n, key=key)
        T.pause(0.7)
        sc["numeral_t"] = round(T.t, 3)
        T.say(a, f"This is number {NUM[n - 1].lower()}!", gap=0.5)
        sc["count_t"] = T.count("both", n)
        T.pause(0.3)
        sc["phrase_t"] = T.say(b, phrase)
        T.say(a, fun, gap=0.4)
        T.prompt(b, "Can you show one finger?" if n == 1 else f"Can you show {NUM[n - 1].lower()} fingers?",
                 wait=2.2 if n < 6 else 2.8)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[k % len(PRAISE)], gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- how many? rounds
    r = 0
    for title, bg, intro, rounds in ROUNDS:
        sc = T.scene("title", bg, title=title)
        T.pause(0.6)
        T.say(*intro, gap=0.6)
        T.end(sc)
        for key, plural, n in rounds:
            a, b = ("mishu", "gul") if r % 2 == 0 else ("gul", "mishu")
            sc = T.scene("count", bg, n=n, key=key)
            T.pause(0.9)
            T.prompt(a, f"How many {plural}?", wait=2.4)
            T.say(b, "Let's count!", gap=0.4)
            sc["count_t"] = T.count(b, n)
            T.pause(0.3)
            sc["answer_t"] = round(T.t, 3)
            T.say(a, f"{NUM[n - 1]} {plural if n > 1 else plural.rstrip('s')}!", gap=0.3)
            T.stars.append(round(T.t, 3))
            T.say(b, PRAISE[r % len(PRAISE)], gap=0.7)
            T.end(sc)
            r += 1
    # ---------------------------------------------------------------- adding (for the older kids)
    sc = T.scene("title", "garden", title="LET'S ADD!")
    T.pause(0.6)
    T.say("gul", "Big kids, this one is for you! Let's add!", gap=0.4)
    T.say("mishu", "Adding means putting things together!", gap=0.6)
    T.end(sc)
    for k, (key, word, plural, a_n, b_n) in enumerate(ADDS):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("add", "garden", key=key, a=a_n, b=b_n)
        T.pause(0.8)
        sc["left_t"] = T.say(a, f"{NUM[a_n - 1]} {word if a_n == 1 else plural}...", gap=0.3)
        sc["right_t"] = T.say(a, f"and {NUM[b_n - 1].lower()} more!", gap=0.3)
        T.prompt(a, "How many altogether?", wait=2.6)
        T.say(b, "Let's count them all!", gap=0.4)
        sc["count_t"] = T.count(b, a_n + b_n)
        T.pause(0.3)
        sc["answer_t"] = T.say(a, f"{NUM[a_n - 1]} plus {NUM[b_n - 1].lower()} is {NUM[a_n + b_n - 1].lower()}!", gap=0.3)
        T.stars.append(round(T.t, 3))
        T.say(b, PRAISE[(k + 2) % len(PRAISE)], gap=0.7)
        T.end(sc)
    # ---------------------------------------------------------------- traditional rhyme (public domain, 18th century)
    sc = T.scene("title", "beach", title="COUNTING RHYME!")
    T.pause(0.6)
    T.say("gul", "Let's say a counting rhyme together!", gap=0.7)
    T.end(sc)
    for rep in range(2):
        sc = T.scene("song", "beach")
        T.pause(0.5)
        sc["count_t"] = T.count("both" if rep else "mishu", 5, step_gap=0.15)
        sc["line1_t"] = T.say("gul" if rep == 0 else "both", "Once I caught a fish alive!", gap=0.4)
        sc["count2_t"] = T.count("both" if rep else "mishu", 10, step_gap=0.15)[5:]
        sc["line2_t"] = T.say("gul" if rep == 0 else "both", "Then I let it go again!", gap=0.8)
        T.end(sc)
    sc = T.scene("rhyme_end", "beach")
    T.say("mishu", "Why did you let it go?")
    T.say("gul", "Because it bit my finger so!", gap=0.4)
    T.say("mishu", "Oh no! Silly fish!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- rocket countdown
    sc = T.scene("title", "space", title="ROCKET COUNTDOWN!")
    T.pause(0.6)
    T.say("mishu", "Now let's count backwards! Ten to one!", gap=0.4)
    T.say("gul", "Get ready for blast off!", gap=0.6)
    T.end(sc)
    sc = T.scene("rocket", "space")
    T.pause(0.5)
    times = []
    for i in range(9, -1, -1):
        times.append(round(T.say("both", NUM[i] + "!", gap=0.3), 3))
    sc["count_t"] = times
    sc["launch_t"] = T.say("both", "Blast off!", gap=2.6)
    T.fx.append(("launch", sc["launch_t"], 0))
    T.say("mishu", "Up, up and away!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- outro
    sc = T.scene("outro", "rainbow")
    T.say("gul", "We counted so many things today!")
    T.say("mishu", "What is your favourite number? Mine is five!", gap=0.5)
    sc["bye_t"] = T.say("both", "Bye bye, friends!", gap=0.4)
    T.say("gul", "See you next time!", gap=2.0)
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
    json.dump(dict(lines=T.lines, scenes=T.scenes, prompts=T.prompts, stars=T.stars, total=total),
              open(HERE / "timeline.json", "w"), indent=1)
    # ---------------------------------------------------------------- audio mix
    mus = np.zeros((n, 2))
    B = 60 / 104
    prog = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]
    tune = [72, 76, 79, 76, 77, 74, 72, 0, 72, 74, 76, 79, 81, 79, 76, 0]
    i, tt = 0, 0.0
    while tt < total:
        ch = prog[(i // 4) % 4]
        if i % 2 == 0:
            A.add(mus, M.tuba(ch[0] - 24, B * 0.8), tt, 0.18)
        else:
            A.add(mus, M.uke_chord([x + 12 for x in ch]), tt, 0.045, -0.25)
        if (i // 16) % 2 == 0 and tune[i % 16]:
            A.add(mus, M.toy_piano(tune[i % 16] + 12), tt, 0.03, 0.25)
        tt += B
        i += 1
    ts = np.arange(n) / SR
    mus *= (np.clip(ts / 1.0, 0, 1) * np.clip((total - ts) / 2.0, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.15)
    A.add(v, tracks["mishu"], 0, 1.0, 0.15)
    v /= np.abs(v).max() / 0.9
    e = np.abs(v).mean(axis=1)                              # duck music under speech
    win = int(0.1 * SR)
    e = np.convolve(e, np.ones(win) / win, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.4 * e)[:, None]
    f = np.zeros((n, 2))
    for kind, at, k in T.fx:
        if kind == "ding":
            A.add(f, A.sfx_ding(72 + [0, 2, 4, 5, 7, 9, 11, 12, 14, 16][k]), at, 0.08)
        elif kind == "launch":
            A.add(f, A.sfx_whoosh(), at + 0.3, 0.6)
            rng = np.random.default_rng(9)
            rum = np.convolve(rng.standard_normal(int(2.2 * SR)), np.ones(200) / 200, mode="same")
            rum *= np.minimum(1, np.arange(len(rum)) / (0.2 * SR)) * np.linspace(1, 0, len(rum))
            A.add(f, rum * 6, at + 0.2, 0.5)
    for sc in T.scenes:
        if sc["kind"] in ("number", "count"):
            A.add(f, A.sfx_pop(), sc["t0"] + 0.2, 0.2)
        if sc["kind"] == "title":
            A.add(f, A.sfx_whoosh(), sc["t0"], 0.15)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.18)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(84), p0, 0.12)
    mix = v + mus * 0.22 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    sf.write(HERE / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s ({total / 60:.1f} min), {len(T.lines)} lines, {len(T.scenes)} scenes")


if __name__ == "__main__":
    build()
