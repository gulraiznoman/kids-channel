"""Long video 10: "ABC Phonics". Voices, timeline.json, mix.wav (own music + own sounds).
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

LETTERS = [  # letter, sound (spelled so the voice says it), word 1, word 2 (or None)
    ("A", "ah", "apple", "airplane"), ("B", "buh", "ball", "banana"), ("C", "kuh", "cat", "car"), ("D", "duh", "dog", "dinosaur"),
    ("E", "eh", "elephant", "egg"), ("F", "fuh", "fish", "frog"), ("G", "guh", "grapes", "gift"), ("H", "huh", "hat", "hen"),
    ("I", "ih", "ice cream", None), ("J", "juh", "jellyfish", None), ("K", "kuh", "kite", "kiwi"), ("L", "luh", "lion", "lemon"),
    ("M", "muh", "monkey", "moon"), ("N", "nuh", "nest", "nose"), ("O", "aw", "octopus", "ostrich"), ("P", "puh", "penguin", "pizza"),
    ("Q", "kwuh", "queen", None), ("R", "ruh", "rainbow", "robin"), ("S", "suh", "sun", "snake"), ("T", "tuh", "turtle", "train"),
    ("U", "uh", "umbrella", None), ("V", "vuh", "violin", None), ("W", "wuh", "whale", "watermelon"), ("X", "ks", "xylophone", "box"),
    ("Y", "yuh", "yo-yo", None), ("Z", "zuh", "zebra", None)]
FIRST = [("ball", "B"), ("dog", "D"), ("sun", "S"), ("fish", "F"), ("moon", "M"), ("cat", "C"), ("penguin", "P"), ("turtle", "T"),
         ("apple", "A"), ("zebra", "Z"), ("rainbow", "R"), ("kite", "K")]
PICS = [("S", ["sun", "ball", "snake", "fish"]), ("M", ["cat", "monkey", "egg", "moon"]), ("B", ["ball", "kite", "dog", "banana"]),
        ("D", ["sun", "dog", "dinosaur", "moon"])]
SPELL = [("cat", "CAT"), ("dog", "DOG"), ("sun", "SUN"), ("hen", "HEN"), ("box", "BOX"), ("bus", "BUS"), ("hat", "HAT")]
MATCH = [("A", ["b", "a", "d"]), ("B", ["d", "p", "b"]), ("D", ["d", "b", "q"]), ("G", ["q", "g", "y"]), ("R", ["r", "n", "m"]),
         ("E", ["e", "c", "o"]), ("M", ["n", "w", "m"]), ("T", ["f", "t", "l"])]
HUNT = [("B", "DBPRBEDB"), ("M", "NWMHNMWN"), ("S", "ZSCZOSCS"), ("T", "FTLITFTE")]
TRACE = ["A", "B", "C", "O"]
BODY = [("Y", "Y! Arms up high!"), ("T", "T! Arms out wide!"), ("I", "I! Stand up tall!"), ("O", "O! Arms in a circle!"),
        ("X", "X! Arms and legs out!"), ("C", "C! Bend to the side!")]
QUIZ = [("What sound does B make?", "Buh, buh, ball!", "B"), ("What letter does apple start with?", "A! Ah, ah, apple!", "A"),
        ("Which letter comes after A?", "B!", "B"), ("Which letter makes the suh sound?", "S! Like sun and snake!", "S"),
        ("What is the last letter?", "Z! Zuh, zuh, zebra!", "Z"), ("How many letters are in the alphabet?", "Twenty six letters!", "26")]


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
    # ---------------------------------------------------------------- OPENING: letters rain down, ABC! slam
    sc = T.scene("intro", "abcpark")
    sc["rain_t"] = T.mark("rain")
    T.pause(1.8)
    sc["title_t"] = T.mark("slam")
    T.say("both", "A, B, C!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Let's learn the ABC, and the sound of every letter!", gap=0.2)
    T.say("gul", "From A to Z! Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- ABC PHONICS: A to Z
    T.title("abcpark", "ABC PHONICS!", "gul", "Say the letter, and the sound, with us!")
    for k, (L, snd, w1, w2) in enumerate(LETTERS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("letter", "abcpark", L=L, w1=w1, w2=w2, num=k + 1)
        T.mark("pop")
        T.pause(0.25)
        sc["w1_t"] = T.say(a, f"{L} is for {w1}!", gap=0.1)
        if L == "X":
            sc["snd_t"] = T.say(other(a), "X says ks, like in box!", gap=0.1)
        else:
            sc["snd_t"] = T.say(other(a), f"{snd}, {snd}, {w1}!", gap=0.1)
        if w2 and L != "X":
            sc["w2_t"] = T.say(a, f"And {w2}!", gap=0.1)
        T.prompt(a, f"Your turn! {'ks' if L == 'X' else snd}!", wait=1.1)
        T.end(sc)
    sc = T.scene("allletters", "abcpark")
    T.say("both", "We did the whole alphabet! Hooray!", gap=0.5)
    T.stars.append(round(T.t - 0.8, 3))
    T.end(sc)
    # ---------------------------------------------------------------- FAST ABC
    T.title("abcpark", "FAST ABC!", "mishu", "Now let's say them all, super fast!")
    sc = T.scene("fast", "abcpark")
    ts = []
    for L, *_ in LETTERS:
        ts.append(T.say("both", f"{L}!", gap=-0.05))
    sc["ts"] = ts
    T.pause(0.3)
    T.say("gul", "Wow! So fast!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- SMALL LETTER SOUNDS drill
    T.title("abcpark", "SMALL LETTER SOUNDS!", "gul", "Small letters make the same sounds! Say them with us!")
    sc = T.scene("lower", "abcpark")
    ts = []
    for L, snd, *_ in LETTERS:
        ts.append(T.say("both", f"{snd}!", gap=0.05))
    sc["ts"] = ts
    T.say("mishu", "Wow! You know all the sounds!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- FIRST LETTER GAME
    T.title("board", "FIRST LETTER!", "gul", "Big kids! What letter does it start with?")
    for k, (word, L) in enumerate(FIRST):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("first", "board", word=word, L=L)
        T.mark("pop")
        T.prompt(a, f"{word.capitalize()}! What letter does {word} start with?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        snd = next(x[1] for x in LETTERS if x[0] == L)
        T.say(other(a), f"{L}! {snd}, {snd}, {word}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- WHAT STARTS WITH...?
    T.title("abcpark", "WHAT STARTS WITH...?", "mishu", "Find the pictures that start with the letter!")
    for k, (L, pics) in enumerate(PICS):
        a = "gul" if k % 2 == 0 else "mishu"
        snd = next(x[1] for x in LETTERS if x[0] == L)
        good = [p for p in pics if p[0].upper() == L]
        sc = T.scene("pics", "abcpark", L=L, pics=pics)
        T.mark("pop")
        T.prompt(a, f"What starts with {L}? {snd}, {snd}!", wait=2.2)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{good[0].capitalize()} and {good[1]}!", gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- BIG AND SMALL LETTERS
    T.title("board", "BIG AND SMALL LETTERS!", "mishu", "Every letter has a big one, and a small one!")
    for k, (L, opts) in enumerate(MATCH):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("match", "board", L=L, opts=opts)
        T.mark("pop")
        T.prompt(a, f"Find the small {L}!", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"Here it is! Big {L}, small {L.lower()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- LETTER HUNT
    T.title("abcpark", "LETTER HUNT!", "gul", "Letters are hiding! Can you find them?")
    for k, (L, grid) in enumerate(HUNT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("hunt", "abcpark", L=L, grid=grid)
        T.prompt(a, f"Find all the letter {L}s!", wait=2.4)
        sc["answer_t"] = T.mark("yes")
        n = grid.count(L)
        T.say(other(a), f"I found {['', 'one', 'two', 'three', 'four'][n]} {L}s!", gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- SOUND IT OUT (blending)
    T.title("board", "SOUND IT OUT!", "gul", "Big kids! Put the sounds together, and read a word!")
    for k, (w, letters) in enumerate(SPELL):
        a = "mishu" if k % 2 == 0 else "gul"
        sounds = [next(x[1] for x in LETTERS if x[0] == ch) if ch != "X" else "ks" for ch in letters]
        sc = T.scene("spell", "board", word=w, letters=letters)
        sc["snd_t"] = []
        for snd in sounds:
            T.mark("pop")
            sc["snd_t"].append(T.say(a, f"{snd}!", gap=0.15))
        T.prompt(a, "What word is it?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{w.capitalize()}! {', '.join(letters)}, {w}!", gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- TRACE IN THE AIR
    T.title("board", "DRAW IN THE AIR!", "mishu", "Use your finger, and draw the letters with us!")
    for k, L in enumerate(TRACE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("trace", "board", L=L)
        T.say(a, f"Let's draw {L}!", gap=0.1)
        sc["draw_t"] = T.mark("draw")
        T.prompts.append((round(T.t, 3), round(T.t + 3.2, 3)))
        T.pause(3.2)
        T.say(other(a), f"Great {L}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- BODY LETTERS DANCE x2
    T.title("abcpark", "BODY LETTERS!", "gul", "Stand up! Let's make letters with our body!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "abcpark", title="FASTER!")
            T.mark("riser")
            T.say("mishu", "Again, faster!", gap=0.2)
            T.end(sc)
        for L, text in BODY:
            sc = T.scene("body", "abcpark", L=L, fast=rnd == 1)
            T.mark("pop")
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- QUIZ
    T.title("board", "ABC QUIZ!", "mishu", "Quiz time! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("quiz", "board", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "abcpark")
    T.say("mishu", "Now you know your ABC!", gap=0.2)
    T.say("gul", "What letter does your name start with?", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends! See you next time!", gap=1.8)
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
rng = np.random.default_rng(10)


def marimba(m, d=0.35):
    return A.tone(A.mtof(m), d, ((1, 1), (4, 0.35), (9.2, 0.08)), 0.002, d * 0.35)


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 124
    prog = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]           # C Am F G: bright school-day pop
    hook = [72, 76, 79, 76, 77, 74, 72, 0, 74, 77, 81, 79, 77, 74, 79, 0]
    bar, t0 = 0, 2.0
    while t0 < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = t0 + q * B
            A.add(mus, LS.kick(), b0, 0.48)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.3, 0.05)
                A.add(mus, RV.snare(), b0, 0.14)
            A.add(mus, LS.hat(), b0 + B / 2, 0.45, -0.3)
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):
                A.add(mus, marimba(nt + 12, 0.3), b0 + B / 2, 0.05, -0.25 + 0.25 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, M.toy_piano(mm, 0.4), t0 + i * B / 2, 0.06, 0.2)
        t0 += 4 * B
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
    scale = [72, 74, 76, 77, 79, 81, 83, 84]
    for kind, at in T.fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.35)
        elif kind == "rain":
            for k in range(26):
                A.add(f, marimba(scale[k % 8] + 12 * (k // 8 % 2), 0.25), at + k * 0.065, 0.12, -0.6 + 1.2 * (k % 7) / 6)
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "draw":
            A.add(f, A.sfx_sparkle(), at, 0.3)
            A.add(f, A.sfx_sparkle(), at + 1.4, 0.25)
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
