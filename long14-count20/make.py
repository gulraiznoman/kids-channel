"""Long video 14: "Count 1 to 20". Voices, timeline.json, mix.wav (own music + own sounds).
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
PLURAL = {"fish": "fish", "strawberry": "strawberries"}


def plural(w):
    return PLURAL.get(w, w + "s")


PRAISE = ["Great job!", "Yes! You got it!", "Awesome!", "Well done!", "Super!", "You're so smart!"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
TEENS = [(11, "apple"), (12, "star"), (13, "fish"), (14, "duckling"), (15, "strawberry"), (16, "ball"), (17, "cupcake"), (18, "balloon"),
         (19, "flower"), (20, "heart")]
MOVES = [("jump", "Let's jump twenty times! Ready? Jump!"), ("clap", "Now clap twenty times! Clap!"), ("stomp", "Now stomp twenty times! Stomp!")]
HOWMANY = [(13, "star"), (17, "fish"), (15, "apple"), (20, "balloon"), (11, "duckling"), (19, "heart"), (14, "flower"), (16, "cupcake")]
MORE = [((12, "apple"), (18, "apple"), 1), ((16, "star"), (11, "star"), 0), ((14, "fish"), (19, "fish"), 1), ((20, "ball"), (15, "ball"), 0)]
ONEMORE = [12, 15, 17, 19]
AFTER = [(11, 12), (14, 15), (16, 17), (18, 19), (19, 20)]
MISSING = [([11, 12, None, 14, 15], 13), ([15, 16, 17, None, 19], 18), ([10, None, 12, 13, 14], 11), ([16, 17, 18, 19, None], 20)]
QUIZ = [("What comes after nineteen?", "Twenty!", 20), ("How many fingers on two hands?", "Ten!", 10),
        ("Eleven is ten and how many more?", "One more!", 11), ("What comes before fifteen?", "Fourteen!", 14),
        ("Count by twos: two, four, six... what's next?", "Eight!", 8), ("Which is bigger, twelve or twenty?", "Twenty!", 20),
        ("How many fingers and toes do you have?", "Twenty!", 20), ("What is sixteen and one more?", "Seventeen!", 17)]


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


def count_run(T, sc, upto, start=1, step=1, kind="pop", key="ts", gap=0.08):
    ts = []
    for k in range(start, upto + 1, step):
        T.mark(kind)
        ts.append(T.say("both", f"{WORDS[k].capitalize()}!", gap=gap))
    sc[key] = ts


def build():
    T = TL()
    # ---------------------------------------------------------------- OPENING: numbers 1-20 rain down, title
    sc = T.scene("intro", "rainbow")
    sc["rain_t"] = T.mark("rain")
    T.pause(1.8)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Count to twenty!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Let's count, jump, clap, and play, all the way to twenty!", gap=0.2)
    T.say("gul", "Ready? Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- WARM UP 1-10 with claps
    T.title("rainbow", "WARM UP: 1 TO 10!", "gul", "First, let's count to ten, and clap!")
    sc = T.scene("warm", "rainbow")
    count_run(T, sc, 10, kind="clap")
    T.say("mishu", "Easy! Now let's go higher!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- MEET 11-20 (ten and more)
    T.title("board", "MEET 11 TO 20!", "mishu", "After ten come the teen numbers! Let's meet them!")
    for k, (n, art) in enumerate(TEENS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("teen", "board", n=n, art=art)
        T.mark("pop")
        T.pause(0.2)
        sc["name_t"] = T.say(a, f"This is {WORDS[n]}!", gap=0.15)
        if n < 20:
            sc["ten_t"] = T.say(other(a), f"{WORDS[n].capitalize()} is ten, and {WORDS[n - 10]} more!", gap=0.15)
        else:
            sc["ten_t"] = T.say(other(a), "Twenty is two tens! Ten, and ten more!", gap=0.15)
        sc["count_t"] = T.say("both", f"{WORDS[n].capitalize()} {plural(art)}!", gap=0.2)
        T.prompt(a, f"Say {WORDS[n]}!", wait=1.1)
        T.end(sc)
    # ---------------------------------------------------------------- COUNT AND MOVE to 20
    T.title("rainbow", "COUNT AND MOVE!", "gul", "Stand up! Let's count to twenty and move!")
    for k, (move, text) in enumerate(MOVES):
        sc = T.scene("move", "rainbow", move=move)
        T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.1)
        count_run(T, sc, 20, kind="stomp" if move == "stomp" else ("clap" if move == "clap" else "boing"), gap=0.02)
        T.say("both", "Twenty! Phew! Great job!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- FINGERS AND TOES = 20
    T.title("rainbow", "FINGERS AND TOES!", "mishu", "Did you know? You have twenty fingers and toes!")
    sc = T.scene("fingers", "rainbow")
    T.say("gul", "Let's count your fingers!", gap=0.1)
    count_run(T, sc, 10, kind="pop", gap=0.02, key="f_ts")
    T.say("mishu", "Now your toes! Eleven...", gap=0.0)
    count_run(T, sc, 20, start=12, kind="pop", gap=0.02, key="t_ts")
    sc["sum_t"] = T.say("both", "Ten fingers and ten toes make twenty!", gap=0.5)
    T.stars.append(round(T.t - 0.8, 3))
    T.end(sc)
    # ---------------------------------------------------------------- HIDE AND SEEK
    sc = T.scene("hide", "rainbow")
    T.say("mishu", "Let's play hide and seek! Gul, count to twenty!", gap=0.1)
    sc["hide_t"] = round(T.t, 3)
    count_run(T, sc, 20, kind="tick", gap=0.0)
    T.say("gul", "Ready or not, here I come!", gap=0.3)
    sc["found_t"] = T.mark("yes")
    T.say("gul", "Found you, Mishu! Behind the tree!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- HOW MANY?
    T.title("rainbow", "HOW MANY?", "mishu", "Let's count the things! How many are there?")
    for k, (n, art) in enumerate(HOWMANY):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("howmany", "rainbow", n=n, art=art)
        T.say(a, f"How many {plural(art)}? Count with us!", gap=0.1)
        count_run(T, sc, n, kind="pop", gap=0.02)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{WORDS[n].capitalize()}!", gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- WHICH HAS MORE?
    T.title("rainbow", "WHICH HAS MORE?", "gul", "Look at both groups. Which one has more?")
    for k, (g1, g2, ans) in enumerate(MORE):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("more", "rainbow", g1=list(g1), g2=list(g2), ans=ans)
        T.prompt(a, "Which side has more?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        big = g2 if ans else g1
        small = g1 if ans else g2
        T.say(other(a), f"{WORDS[big[0]].capitalize()} is more than {WORDS[small[0]]}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- ONE MORE
    T.title("board", "ONE MORE!", "mishu", "Big kids! What is one more?")
    for k, n in enumerate(ONEMORE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("onemore", "board", n=n)
        T.prompt(a, f"What is {WORDS[n]}, and one more?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{WORDS[n + 1].capitalize()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- WHAT COMES AFTER?
    T.title("board", "WHAT COMES NEXT?", "gul", "Big kids! What number comes after?")
    for k, (n, ans) in enumerate(AFTER):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("after", "board", n=n, ans=ans)
        T.prompt(a, f"What comes after {WORDS[n]}?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{WORDS[ans].capitalize()}!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- MISSING NUMBER
    T.title("board", "MISSING NUMBER!", "mishu", "Oh no! A number is missing! Can you find it?")
    for k, (row, ans) in enumerate(MISSING):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("missing", "board", row=row, ans=ans)
        T.prompt(a, "Which number is missing?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{WORDS[ans].capitalize()}!", gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ---------------------------------------------------------------- COUNT BY TWOS (pairs)
    T.title("rainbow", "COUNT BY TWOS!", "gul", "Big kids! Shoes come in pairs. Let's count by twos!")
    sc = T.scene("twos", "rainbow")
    count_run(T, sc, 20, start=2, step=2, kind="pop", gap=0.15)
    T.say("mishu", "Two, four, six, eight, ten, all the way to twenty!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- COUNT BY FIVES AND TENS (hands)
    sc = T.scene("fives", "rainbow")
    T.say("mishu", "Now, count by fives, with our hands!", gap=0.1)
    count_run(T, sc, 20, start=5, step=5, kind="clap", gap=0.3)
    T.say("gul", "And by tens! Ten, twenty!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- COUNTDOWN FROM 20 (rocket)
    T.title("space", "COUNTDOWN!", "mishu", "Now, count backwards from twenty! Blast off!")
    sc = T.scene("rocket", "space")
    ts = []
    for k in range(20, 0, -1):
        T.mark("tick")
        ts.append(T.say("both", f"{WORDS[k].capitalize()}!", gap=0.02))
    sc["ts"] = ts
    sc["blast_t"] = T.mark("blast")
    T.say("both", "Blast off! Whoosh!", gap=1.0)
    T.end(sc)
    # ---------------------------------------------------------------- QUIZ
    T.title("rainbow", "NUMBER QUIZ!", "gul", "Quiz time! Are you ready?")
    for k, (q, ans, vis) in enumerate(QUIZ):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("quiz", "rainbow", q=q.upper(), vis=vis)
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "rainbow")
    T.say("mishu", "You can count to twenty! Wow!", gap=0.2)
    T.say("gul", "Count your toys today, and see how many you have!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends! One, two, see you!", gap=1.8)
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
rng = np.random.default_rng(14)


def tt_(d):
    return np.arange(int(d * SR)) / SR


def marimba(m, d=0.3):
    return A.tone(A.mtof(m), d, ((1, 1), (4, 0.35), (9.2, 0.08)), 0.002, d * 0.35)


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 126
    prog = [[67, 71, 74], [64, 67, 71], [60, 64, 67], [62, 66, 69]]           # G Em C D: fast, bouncy counting
    hook = [79, 79, 83, 86, 83, 0, 81, 79, 76, 79, 81, 83, 81, 79, 74, 0]
    bar, t0 = 0, 2.0
    while t0 < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = t0 + q * B
            A.add(mus, LS.kick(), b0, 0.5)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.32, 0.05)
                A.add(mus, RV.snare(), b0, 0.14)
            A.add(mus, LS.hat(), b0 + B / 2, 0.45, -0.3)
            A.add(mus, LS.hat(), b0 + B * 0.25, 0.2, 0.3)
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):
                A.add(mus, marimba(nt + 12, 0.28), b0 + B / 2, 0.05, -0.25 + 0.25 * j)
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
            A.add(f, A.sfx_pop(), at, 0.3)
        elif kind == "clap":
            A.add(f, M.clap(), at + 0.05, 0.4)
        elif kind == "stomp":
            A.add(f, M.stomp(), at + 0.05, 0.4)
        elif kind == "boing":
            A.add(f, M.boing(), at + 0.05, 0.25)
        elif kind == "rain":
            for k in range(20):
                A.add(f, marimba(scale[k % 8] + 12 * (k // 8 % 2), 0.25), at + k * 0.08, 0.12, -0.6 + 1.2 * (k % 7) / 6)
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "tick":
            tq = tt_(0.05)
            A.add(f, np.sin(2 * np.pi * 1500 * tq) * np.exp(-tq / 0.01), at, 0.25)
        elif kind == "blast":
            tq = tt_(2.0)
            x = np.convolve(rng.standard_normal(len(tq)), np.ones(40) / 40, mode="same") * 6 * np.minimum(1, tq / 0.1) * np.exp(-tq / 0.9)
            A.add(f, x, at, 0.7)
            A.add(f, A.sfx_whoosh(), at + 0.2, 0.5)
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
