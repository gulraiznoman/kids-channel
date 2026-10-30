"""Long video 7: "Feelings & Emotions for Kids". Voices, timeline.json, mix.wav (own music + own sounds).
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

FEELINGS = [  # feeling, who shows it, lines
    ("happy", "gul", ["I feel happy!", "When I'm happy, I smile and laugh! Ha ha ha!"]),
    ("sad", "misheal", ["I feel sad.", "When I'm sad, I might cry, and tears come out."]),
    ("angry", "gul", ["I feel angry!", "When I'm angry, my face feels hot, and I want to stomp!"]),
    ("scared", "misheal", ["I feel scared!", "When I'm scared, my heart beats fast, and I want a hug."]),
    ("surprised", "gul", ["Oh! I feel surprised!", "My eyes go big, and my mouth makes an O!"]),
    ("excited", "misheal", ["I feel excited!", "I can't wait! I want to jump up and down!"]),
    ("tired", "gul", ["Yawn! I feel tired.", "My eyes are sleepy. I need some rest."]),
    ("shy", "misheal", ["I feel shy.", "When I'm shy, I want to hide a little bit."]),
    ("proud", "gul", ["I feel proud!", "I did it all by myself!"]),
    ("calm", "misheal", ["I feel calm.", "Nice and quiet, like a soft, sleepy cloud."]),
]
SPEAK = {"gul": "gul", "misheal": "mishu"}
OTHER = {"gul": "mishu", "misheal": "gul"}


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


def build():
    T = TL()
    # ---------------------------------------------------------------- OPENING: Gul's face flips through feelings, title slam
    sc = T.scene("intro", "room")
    flips = []
    for emo in ("happy", "sad", "angry", "surprised", "scared", "excited"):
        flips.append((round(T.t, 3), emo))
        T.mark("boing" if emo in ("surprised", "scared") else "pop")
        T.pause(0.4)
    sc["flips"] = flips
    sc["title_t"] = T.mark("slam")
    T.say("both", "Big feelings!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Today we'll learn all about our feelings!", gap=0.2)
    T.say("gul", "Happy, sad, angry, and more! Let's go!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- HOW DO YOU FEEL TODAY? (check-in)
    sc = T.scene("checkin", "room")
    T.say("gul", "Before we start, how do YOU feel today?", gap=0.2)
    T.say("mishu", "Happy? Sad? Excited? Point to your face!", gap=0.1)
    T.prompts.append((round(T.t, 3), round(T.t + 3.0, 3)))
    T.pause(3.0)
    T.say("gul", "Great! Every feeling is okay!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- MEET THE FEELINGS (10)
    T.title("room", "MEET THE FEELINGS!", "gul", "Let's look at our faces! Can you copy us?")
    for k, (emo, who, ls) in enumerate(FEELINGS):
        sc = T.scene("feeling", "room", emo=emo, who=who, num=k + 1)
        T.mark("pop")
        T.pause(0.3)
        sc["label_t"] = T.say(SPEAK[who], ls[0], gap=0.2)
        T.say(SPEAK[who], ls[1], gap=0.2)
        T.prompt(OTHER[who], f"Show me your {emo} face!", wait=2.0)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- WHY DO WE FEEL? little stories
    T.title("room", "HOW DO THEY FEEL?", "mishu", "Things happen, and we get feelings! Watch and guess!")
    for k, (who, prop, setup, event, sfx, emo, answer, help_) in enumerate((
            ("gul", "icecream", "Gul has a yummy ice cream.", "Oh no! It fell on the floor!", "splat", "sad",
             "Gul feels sad.", "It's okay to feel sad. Let's share mine!"),
            ("misheal", "gift", "Look! Mishu got a present!", "What's inside? A new teddy bear!", "sparkle", "excited",
             "Mishu feels excited!", "Yay! Excited feels like popcorn inside!"),
            ("gul", "ball", "Gul is playing with his ball.", "Oh no! Someone broke it!", "crash", "angry",
             "Gul feels angry.", "It's okay to feel angry. Let's take a big breath."),
            ("misheal", "thunder", "It's a rainy night.", "BOOM! Loud thunder!", "thunder", "scared",
             "Mishu feels scared.", "A big hug helps us feel safe."),
            ("gul", "balloons", "Gul opens the door.", "SURPRISE! A party for Gul!", "party", "surprised",
             "Gul feels surprised!", "Wow! What a nice surprise!"),
            ("misheal", "puzzle", "Mishu is doing a hard puzzle.", "She finished it all by herself!", "sparkle", "proud",
             "Mishu feels proud!", "Great job, Mishu! You did it!"),
            ("gul", "teddy", "Gul can't find his teddy anywhere.", "Where is it? It's lost!", "crash", "sad",
             "Gul feels sad and worried.", "Let's look together. Found it! Now Gul feels happy!"),
            ("misheal", "dog", "Mishu is walking in the park.", "WOOF WOOF! A big dog barks!", "bark", "scared",
             "Mishu feels scared.", "Hold a grown-up's hand. The dog is friendly!"),
            ("gul", "friend", "A new friend says hello to Gul.", "Gul doesn't know what to say.", "pop", "shy",
             "Gul feels shy.", "It's okay to feel shy. Just say hello, and smile!"),
            ("misheal", "medal", "Mishu runs in a race.", "She ran so fast! She won!", "party", "proud",
             "Mishu feels proud!", "Hooray, Mishu! Well done!"))):
        sc = T.scene("story", "room", who=who, prop=prop, emo=emo)
        T.say(SPEAK[who] if k % 2 else OTHER[who], setup, gap=0.2)
        sc["event_t"] = T.mark(sfx)
        T.say(OTHER[who], event, gap=0.1)
        T.prompt(SPEAK[who] if k % 2 == 0 else OTHER[who], f"How does {'Gul' if who == 'gul' else 'Mishu'} feel?", wait=2.2)
        sc["answer_t"] = T.mark("yes")
        T.say(OTHER[who], answer, gap=0.2)
        T.say(OTHER[who], help_, gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- GUESS THE FEELING
    T.title("room", "GUESS THE FEELING!", "gul", "Look at the face. How does it feel?")
    for k, (who, emo) in enumerate((("misheal", "happy"), ("gul", "scared"), ("misheal", "angry"), ("gul", "tired"),
                                    ("misheal", "surprised"), ("gul", "sad"), ("misheal", "shy"), ("gul", "excited"),
                                    ("misheal", "proud"), ("gul", "calm"))):
        sc = T.scene("guess", "room", who=who, emo=emo)
        T.mark("ding")
        T.pause(0.3)
        T.prompt("gul" if k % 2 == 0 else "mishu", "How does this face feel?", wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say("mishu" if k % 2 == 0 else "gul", f"{emo.capitalize()}!", gap=0.2)
        T.say("gul" if k % 2 == 0 else "mishu", PRAISE[k % len(PRAISE)], gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- WHAT MAKES YOU HAPPY?
    T.title("room", "WHAT MAKES YOU HAPPY?", "mishu", "What makes us happy? Let's see!")
    for k, (prop, text) in enumerate((("sun", "A sunny day makes me happy!"), ("hearthug", "Big hugs make me happy!"),
                                      ("ball", "Playing with my friends makes me happy!"), ("music", "Music and dancing make me happy!"),
                                      ("puppy", "A cuddly puppy makes me happy!"), ("icecream", "And ice cream! Yummy!"))):
        sc = T.scene("happy", "room", prop=prop, who="gul" if k % 2 else "misheal")
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 else "mishu", text, gap=0.4)
        T.end(sc)
    sc = T.scene("happy", "room", prop="question", who="gul")
    T.prompt("gul", "What makes YOU happy?", wait=2.6)
    T.end(sc)
    # ---------------------------------------------------------------- MIRROR GAME
    T.title("room", "COPY MY FACE!", "gul", "Mirror game! Quick, copy our faces!")
    for rnd, emos in enumerate((("happy", "angry", "surprised", "sad", "scared", "excited", "tired", "proud"),
                                ("sad", "happy", "angry", "calm", "surprised", "shy"))):
        if rnd == 1:
            sc = T.scene("title", "room", title="FASTER!")
            T.mark("riser")
            T.say("mishu", "Now faster!", gap=0.2)
            T.end(sc)
        for emo in emos:
            sc = T.scene("mirror", "room", emo=emo)
            T.mark("pop")
            sc["say_t"] = T.say("both", f"{emo.capitalize()} face!", gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.5 if rnd == 0 else 0.8), 3)))
            T.pause(1.5 if rnd == 0 else 0.8)
            T.end(sc)
    # ---------------------------------------------------------------- CALM DOWN TOOLS
    T.title("room", "BIG FEELINGS? TRY THIS!", "mishu", "When feelings are big, these help us feel calm!")
    sc = T.scene("breathe", "room", calm=True)
    T.say("gul", "Smell the flower, and blow out the candle. Do it with us!", gap=0.3)
    breaths = []
    for i in range(3):
        b_in = T.say("mishu", "Smell the flower...", gap=0.0)
        T.mark("breath_in")
        T.pause(1.6)
        b_out = T.say("gul", "Blow the candle...", gap=0.0)
        T.mark("breath_out")
        T.pause(1.6)
        breaths.append((b_in, b_out))
    sc["breaths"] = breaths
    T.say("mishu", "Ahh. I feel calm now.", gap=0.5)
    T.end(sc)
    for k, (prop, word, who, text) in enumerate((("count", "COUNT TO FIVE", "gul", "Count to five, slowly. One, two, three, four, five."),
                                                ("teddy", "HUG", "mishu", "Hug your teddy, or a grown-up you love."),
                                                ("speech", "TALK ABOUT IT", "gul", "Tell a grown-up how you feel. Talking helps!"),
                                                ("pillow", "QUIET CORNER", "mishu", "Take a little rest in a quiet, cozy corner."),
                                                ("water", "DRINK WATER", "gul", "Have a drink of cool water."))):
        sc = T.scene("tool", "room", prop=prop, word=word, num=k + 1, calm=True)
        T.mark("chime")
        sc["say_t"] = T.say(who, text, gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- FEELINGS DANCE (own chant), twice
    T.title("room", "FEELINGS DANCE!", "gul", "Now let's dance our feelings! Copy us!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "room", title="FASTER!")
            T.mark("riser")
            T.say("mishu", "Again, faster!", gap=0.2)
            T.end(sc)
        for emo, text, move in (("happy", "Happy face! Jump, jump, jump!", "jump"), ("angry", "Angry face! Stomp, stomp, stomp!", "stomp"),
                                ("sad", "Sad face! Boo hoo hoo!", "sway"), ("surprised", "Surprised face! Oh, oh, oh!", "pop"),
                                ("scared", "Scared face! Shake, shake, shake!", "shake"), ("calm", "Calm face! Breathe in, and out.", "slow")):
            sc = T.scene("dance", "room", emo=emo, move=move, fast=rnd == 1)
            T.mark("stomp2" if move in ("stomp", "jump") else "pop")
            sc["say_t"] = T.say("both", text, gap=0.0)
            T.prompts.append((round(T.t, 3), round(T.t + (1.6 if rnd == 0 else 0.9), 3)))
            T.pause(1.6 if rnd == 0 else 0.9)
            T.end(sc)
    # ---------------------------------------------------------------- BE A KIND FRIEND
    T.title("room", "BE A KIND FRIEND!", "mishu", "When a friend is sad, we can help!")
    for k, (who, problem, helper_line, prop) in enumerate((
            ("misheal", "Oh no, Mishu fell down. Her knee hurts.", "Are you okay, Mishu? Here's a big hug!", "hearthug"),
            ("gul", "Gul has no toy to play with. He feels sad.", "Gul, let's share my teddy! We can play together!", "teddy"),
            ("misheal", "Mishu's drawing got wet. She feels sad.", "Don't worry, Mishu! Let's draw a new one together!", "drawing"),
            ("gul", "Gul feels scared of the dark.", "Here's a little light, Gul. I'll stay with you!", "candle"),
            ("misheal", "Mishu feels angry. Her tower fell down.", "Let's breathe together, and build it again!", "puzzle"))):
        sc = T.scene("kind", "room", who=who, prop=prop)
        T.say("gul" if who == "misheal" else "mishu", problem, gap=0.1)
        T.prompt("mishu" if who == "misheal" else "gul", "How can we help?", wait=2.2)
        sc["help_t"] = T.mark("sparkle")
        T.say("gul" if who == "misheal" else "mishu", helper_line, gap=0.2)
        sc["happy_t"] = T.say(SPEAK[who], "Thank you! I feel happy now!", gap=0.5)
        T.stars.append(round(sc["happy_t"] + 0.5, 3))
        T.end(sc)
    # ---------------------------------------------------------------- BIG KIDS QUIZ
    T.title("room", "FEELINGS QUIZ!", "gul", "Big kids quiz! Are you ready?")
    for k, (q, ans, emo) in enumerate((("What can you do when you feel angry?", "Take deep breaths, and count to five!", "calm"),
                                       ("How does a surprised face look?", "Big eyes, and an O mouth!", "surprised"),
                                       ("Is it okay to feel sad?", "Yes! All feelings are okay!", "sad"),
                                       ("When do we feel proud?", "When we do something all by ourselves!", "proud"),
                                       ("What can you do when a friend is sad?", "Give a hug, or say kind words!", "happy"),
                                       ("How does a tired face look?", "Sleepy eyes, and a big yawn!", "tired"),
                                       ("Who can you talk to about big feelings?", "A grown-up who loves you!", "calm"))):
        sc = T.scene("quiz", "room", q=q.upper(), emo=emo, who="gul" if k % 2 else "misheal")
        T.mark("ding")
        T.prompt("mishu" if k % 2 == 0 else "gul", q, wait=2.5)
        sc["answer_t"] = T.mark("yes")
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "room")
    T.say("mishu", "Remember, all feelings are okay!", gap=0.2)
    T.say("gul", "Tell a grown-up how you feel. They love you!", gap=0.2)
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
rng = np.random.default_rng(41)


def noise(d, lp):
    return np.convolve(rng.standard_normal(int(d * SR)), np.ones(lp) / lp, mode="same")


def env_t(d, a, dec):
    t = np.arange(int(d * SR)) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)


def mixdown(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 114
    prog = [[67, 71, 74], [64, 67, 71], [60, 64, 67], [62, 66, 69]]           # G Em C D: warm, happy pop
    hook = [79, 83, 86, 83, 84, 81, 79, 0, 81, 84, 86, 88, 86, 83, 81, 0]
    bar, tt = 0, 2.6
    while tt < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = tt + q * B
            A.add(mus, LS.kick(), b0, 0.5)
            if q in (1, 3):
                A.add(mus, M.clap(), b0, 0.3, 0.05)
                A.add(mus, RV.snare(), b0, 0.18)
            A.add(mus, LS.hat(), b0 + B / 2, 0.5, 0.3)
            for e, mm in ((0, ch[0] - 24), (0.5, ch[0] - 12), (0.75, ch[0] - 24)):
                A.add(mus, RV.bass(mm, B * 0.42), b0 + e * B, 0.28)
            for j, nt in enumerate(ch):                                   # bright piano chord stabs on the off-beat
                A.add(mus, A.tone(A.mtof(nt), 0.35, ((1, 1), (2, 0.45), (3, 0.2), (4, 0.1)), 0.003, 0.18), b0 + B / 2, 0.05, -0.2 + 0.2 * j)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, M.toy_piano(mm, 0.45), tt + i * B / 2, 0.06, 0.2)
        tt += 4 * B
        bar += 1
    # quieter music during the calm-down part
    g = np.ones(n)
    for s in T.scenes:
        if s.get("calm"):
            a, b = int(s["t0"] * SR), int(s["t1"] * SR)
            g[a:b] = 0.35
    g = np.convolve(g, np.ones(SR) / SR, mode="same")
    ts = np.arange(n) / SR
    mus *= (g * np.clip((total - ts) / 1.5, 0, 1))[:, None]
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
        elif kind == "boing":
            A.add(f, M.boing(), at, 0.35)
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.35)
        elif kind == "splat":
            A.add(f, noise(0.3, 8)[: int(0.3 * SR)] * env_t(0.3, 0.005, 0.07) * 3, at + 1.2, 0.5)
        elif kind == "crash":
            A.add(f, noise(0.5, 2)[: int(0.5 * SR)] * env_t(0.5, 0.002, 0.15) * 1.5, at + 1.0, 0.45)
        elif kind == "thunder":
            m2 = int(1.8 * SR)
            x = noise(1.8, 400)[:m2] * 40 * env_t(1.8, 0.02, 0.6)
            A.add(f, x, at + 0.2, 0.6)
        elif kind == "party":
            A.add(f, A.sfx_sparkle(), at + 0.3, 0.4)
            for k in range(3):
                A.add(f, A.sfx_pop(), at + 0.3 + k * 0.12, 0.35)
        elif kind == "sparkle":
            A.add(f, A.sfx_sparkle(), at + 0.3, 0.35)
        elif kind == "breath_in":
            m2 = int(1.5 * SR)
            A.add(f, noise(1.5, 20)[:m2] * np.sin(np.linspace(0, np.pi, m2)) * 2.5, at, 0.25)
        elif kind == "breath_out":
            m2 = int(1.5 * SR)
            A.add(f, noise(1.5, 6)[:m2] * np.sin(np.linspace(0, np.pi, m2)) * 1.5, at, 0.25)
        elif kind == "chime":
            for k, mm in enumerate((84, 88, 91)):
                A.add(f, A.tone(A.mtof(mm), 1.2, ((1, 1), (2.76, 0.25)), 0.002, 0.6), at + k * 0.08, 0.1)
        elif kind == "stomp2":
            for k in range(3):
                A.add(f, M.stomp(), at + 0.2 + k * 0.35, 0.4)
        elif kind == "bark":
            for k in range(2):
                nn = int(0.22 * SR)
                tt2 = np.arange(nn) / SR
                x = np.sign(np.sin(2 * np.pi * np.cumsum(260 - 120 * tt2 / 0.22) / SR)) * env_t(0.22, 0.005, 0.08) * 0.6
                A.add(f, np.convolve(x, np.ones(8) / 8, mode="same"), at + 1.0 + k * 0.3, 0.45)
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
