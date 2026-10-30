"""Long video 5: "Body Parts for Kids". Opens with a hook (Gul lost his nose!), then a new thing every 20-30 s.
Voices, timeline.json, mix.wav. Own words + the traditional public-domain rhyme "Head, Shoulders, Knees and Toes"
(spoken chant, our own rhythm). All sounds made in code.  python make.py
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
PRAISE = ["Great job!", "Yay! You got it!", "Awesome!", "Well done!", "Super!", "You're so smart!"]


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
        self.t, self.lines, self.scenes, self.voc, self.prompts, self.stars, self.fx = 0.4, [], [], {"gul": [], "mishu": []}, [], [], []

    def say(self, who, text, gap=0.4):
        singers = ["gul", "mishu"] if who == "both" else [who]
        d = 0
        for s in singers:
            x = line(s, text)
            self.voc[s].append((self.t, x * ((0.9 if s == "mishu" else 0.45) if who == "both" else 1.0)))
            d = max(d, len(x) / SR)
        start = round(self.t, 3)
        self.lines.append(dict(who=who, text=text, t=start, dur=round(d, 3)))
        self.t += d + gap + 0.2
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

    def mark(self, kind):
        self.fx.append((kind, round(self.t, 3)))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("whoosh")
        self.pause(0.5)
        self.say(who, text, gap=0.5)
        self.end(sc)


def build():
    T = TL()
    # ---------------------------------------------------------------- HOOK (first seconds): Gul lost his nose!
    sc = T.scene("hook", "playroom", who="gul")
    T.mark("boing")
    T.say("gul", "Oh no! Where is my nose?!", gap=0.3)
    T.say("mishu", "Gul! Your nose is gone! Let's find it!", gap=0.3)
    sc["search_t"] = T.mark("whoosh")
    T.pause(1.2)
    T.say("mishu", "Found it! It was in the toy box!", gap=0.2)
    sc["found_t"] = T.mark("pop")
    T.pause(0.7)
    T.say("gul", "Phew! Thank you, Mishu! Boop!", gap=0.3)
    T.say("mishu", "Let's learn all about our body!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- my face
    T.title("playroom", "MY FACE!", "gul", "First, let's look at my face!")
    for k, (part, label, what, copy) in enumerate((
            ("eyes", "EYES", "My eyes help me see!", "Blink, blink, blink your eyes!"),
            ("nose", "NOSE", "My nose helps me smell! Sniff, sniff!", "Touch your nose!"),
            ("mouth", "MOUTH", "My mouth helps me eat and talk!", "Give a big smile!"),
            ("ears", "EARS", "My ears help me hear!", "Wiggle your ears!"),
            ("hair", "HAIR", "This is my hair! Soft and shiny!", "Pat your head!"),
            ("brows", "EYEBROWS", "These are my eyebrows! Up and down!", "Can you move your eyebrows?"))):
        sc = T.scene("face", "playroom", who="gul", part=part, label=label)
        T.mark("pop")
        T.pause(0.4)
        sc["label_t"] = T.say("mishu" if k % 2 else "gul", f"These are my {label.lower()}!" if part not in ("nose", "mouth", "hair") else f"This is my {label.lower()}!", gap=0.2)
        T.say("gul", what, gap=0.2)
        T.prompt("mishu", copy, wait=2.2)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- my body (Mishu, move along)
    T.title("playroom", "MY BODY!", "mishu", "Now my whole body! Move along with me!")
    for k, (part, label, line_, action) in enumerate((
            ("shoulders", "SHOULDERS", "These are my shoulders!", "Shrug your shoulders, up and down!"),
            ("arms", "ARMS", "These are my arms!", "Shake your arms!"),
            ("hands", "HANDS", "These are my hands! I have ten fingers!", "Clap your hands! Clap, clap, clap!"),
            ("tummy", "TUMMY", "This is my tummy!", "Pat your tummy! Yum, yum!"),
            ("knees", "KNEES", "These are my knees!", "Bend your knees, up and down!"),
            ("feet", "FEET", "These are my feet!", "Stamp your feet! Stamp, stamp!"),
            ("neck", "NECK", "This is my neck!", "Turn your head, left and right!"),
            ("elbows", "ELBOWS", "These are my elbows!", "Bend your elbows, like a chicken! Cluck, cluck!"),
            ("legs", "LEGS", "These are my legs! Long and strong!", "March your legs! Left, right, left, right!"),
            ("fingers", "FINGERS", "These are my fingers!", "Wiggle your fingers! Wiggle, wiggle!"))):
        sc = T.scene("body", "playroom", who="misheal", part=part, label=label)
        T.mark("pop")
        T.pause(0.4)
        sc["label_t"] = T.say("mishu", line_, gap=0.2)
        sc["act_t"] = T.mark("clap" if part == "hands" else "stomp" if part == "feet" else "pop")
        T.say("gul", action, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 2.4, 3)))
        T.pause(2.4)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- five senses (older kids)
    T.title("park", "MY FIVE SENSES!", "gul", "Big kids! Our body has five senses!")
    for k, (icon, objs, label, l1, l2) in enumerate((
            ("eye", ["rainbow"], "SEE", "I can see a rainbow! What colours do you see?", "We see with our eyes!"),
            ("ear", ["bell", "drum"], "HEAR", "Ding, ding! Boom, boom! I hear a bell and a drum!", "We hear with our ears!"),
            ("nose", ["flower"], "SMELL", "Sniff, sniff! The flower smells so nice!", "We smell with our nose!"),
            ("mouth", ["lemon", "icecream"], "TASTE", "The lemon is sour! Ewww! The ice cream is sweet! Yum!", "We taste with our tongue!"),
            ("hand", ["teddy", "cactus"], "TOUCH", "The teddy is soft! The cactus is spiky! Ouch!", "We touch with our hands!"))):
        sc = T.scene("sense", "park", icon=icon, objs=objs, label=label)
        T.mark("pop")
        T.pause(0.5)
        sc["label_t"] = T.say("mishu", f"Sense number {k + 1}: {label.lower()}!", gap=0.2)
        sc["objs_t"] = T.mark({"HEAR": "bell", "TASTE": "sour", "TOUCH": "boing"}.get(label, "sparkle"))
        T.say("gul", l1, gap=0.3)
        T.say("mishu", l2, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- quiz (older kids)
    T.title("playroom", "BODY QUIZ!", "mishu", "Quiz time! Can you answer?")
    for k, (q, ans, icon) in enumerate((("What do we hear with?", "Our ears!", "ear"), ("What do we see with?", "Our eyes!", "eye"),
                                        ("What do we smell with?", "Our nose!", "nose"), ("What do we clap with?", "Our hands!", "hand"),
                                        ("What do we taste with?", "Our tongue, in our mouth!", "mouth"),
                                        ("What do we walk with?", "Our feet!", "shoes"),
                                        ("What do we think with?", "Our brain, inside our head!", "eye"))):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("quiz", "playroom", icon=icon, q=q.upper())
        T.mark("ding")
        T.pause(0.3)
        T.prompt(a, q, wait=2.6)
        sc["answer_t"] = T.mark("yes")
        T.say(b, ans, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[k % len(PRAISE)], gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- Mishu says (listening game)
    T.title("park", "MISHU SAYS!", "mishu", "Let's play Mishu Says! Only do it if I say, Mishu says!")
    for k, (said, action, icon) in enumerate(((True, "touch your head!", None), (True, "touch your nose!", "nose"),
                                              (False, "touch your toes!", None), (True, "clap your hands!", "hand"),
                                              (True, "wiggle your ears!", "ear"), (False, "jump up high!", None),
                                              (True, "blink your eyes!", "eye"), (True, "give a big hug!", None),
                                              (False, "touch your tummy!", None), (True, "stamp your feet!", None),
                                              (True, "pat your head!", None), (False, "sit down!", None))):
        sc = T.scene("says", "park", said=said, action=action.upper().rstrip("!"), icon=icon)
        T.mark("ding")
        sc["say_t"] = T.say("mishu", ("Mishu says, " if said else "") + action, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 2.2, 3)))
        T.pause(2.2)
        sc["result_t"] = T.mark("yes" if said else "no")
        T.say("gul", "Yay! Well done!" if said else "Oops! Mishu didn't say! Don't move!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- what's missing? (callback to the hook)
    T.title("playroom", "WHAT'S MISSING?", "gul", "Uh oh! Something is missing from my face again!")
    for k, (part, ans) in enumerate((("ears", "Your ears are missing!"), ("mouth", "Your mouth! Your smile is missing!"),
                                     ("hair", "Your hair is missing! Ha ha!"), ("brows", "Your eyebrows are missing!"),
                                     ("nose", "Your nose! Again, Gul?!"))):
        a, b = ("gul", "mishu")
        sc = T.scene("missing", "playroom", who="gul", part=part)
        T.mark("boing")
        T.pause(0.4)
        T.prompt(a, "What's missing?", wait=2.8)
        sc["back_t"] = T.mark("pop")
        T.say(b, ans, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- animal body parts
    T.title("park", "ANIMAL BODIES!", "mishu", "Animals have body parts too!")
    for k, (q, key, ans) in enumerate((("Who has a long trunk?", "elephant", "The elephant! Toot, toot!"),
                                       ("Who has long, floppy ears?", "bunny", "The bunny! Hop, hop!"),
                                       ("Who has fins to swim?", "fish", "The fish! Swim, swim!"),
                                       ("Who has a long tail to swing?", "monkey", "The monkey! Ooh, ooh, aah!"),
                                       ("Who has wings and a beak?", "duckling", "The duckling! Quack, quack!"),
                                       ("Who has a big fluffy mane?", "cub", "The lion! Roar!"),
                                       ("Who has a hard shell on its back?", "turtle", "The turtle! Slow and steady!"),
                                       ("Who has eight wiggly arms?", "octopus", "The octopus! Wiggle, wiggle!"))):
        a, b = ("gul", "mishu") if k % 2 == 0 else ("mishu", "gul")
        sc = T.scene("animal", "park", key=key, q=q.upper().rstrip("?") + "?")
        T.mark("ding")
        T.pause(0.3)
        T.prompt(a, q, wait=2.4)
        sc["reveal_t"] = T.mark("pop")
        T.say(b, ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- count with your body
    T.title("playroom", "COUNT YOUR BODY!", "gul", "How many? Let's count with our body!")
    for k, (part, q, ans, num) in enumerate((("eyes", "How many eyes do we have?", "Two eyes!", 2),
                                            ("nose", "How many noses?", "Just one nose!", 1),
                                            ("ears", "How many ears?", "Two ears!", 2),
                                            ("hands", "How many fingers?", "Ten fingers! Five on each hand!", 10),
                                            ("feet", "How many feet?", "Two feet!", 2))):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("count", "playroom", who="gul", part=part, num=num, q=q.upper())
        T.mark("ding")
        T.pause(0.3)
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(b, ans, gap=0.4)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- what do we use? (thinking game)
    T.title("park", "WHAT DO WE USE?", "mishu", "Big kids, think! What body part do we use?")
    for k, (obj, q, ans, icon) in enumerate((("icecream", "To eat an ice cream, I use my...", "Mouth! Yum!", "mouth"),
                                            ("ball", "To kick a ball, I use my...", "Feet! Kick!", None),
                                            ("drum", "To hear the drum, I use my...", "Ears! Boom, boom!", "ear"),
                                            ("flower", "To smell a flower, I use my...", "Nose! Sniff, sniff!", "nose"),
                                            ("book", "To read a book, I use my...", "Eyes!", "eye"),
                                            ("crayon", "To draw a picture, I use my...", "Hands!", "hand"))):
        a, b = ("gul", "mishu") if k % 2 == 0 else ("mishu", "gul")
        sc = T.scene("use", "park", obj=obj, icon=icon, q=q.upper().rstrip(".") + "...")
        T.mark("pop")
        T.pause(0.3)
        T.prompt(a, q, wait=2.6)
        sc["answer_t"] = T.mark("yes")
        T.say(b, ans, gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- who's peeking? (guess the animal from one body part)
    T.title("park", "WHO'S PEEKING?", "gul", "Someone is peeking through the window! Who is it?")
    for k, (key, focus, ans) in enumerate((("elephant", (0.25, 0.62), "It's the elephant! I saw his long trunk!"),
                                          ("bunny", (0.55, 0.12), "The bunny! I saw her long ears!"),
                                          ("monkey", (0.82, 0.72), "The monkey! I saw his curly tail!"),
                                          ("puppy", (0.5, 0.42), "The puppy! I saw his wet nose!"),
                                          ("foal", (0.48, 0.86), "A horse! I saw his long legs!"),
                                          ("fish", (0.86, 0.5), "The fish! I saw its tail fin!"),
                                          ("cub", (0.5, 0.25), "The lion! I saw his fluffy mane!"))):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("peek", "park", key=key, focus=list(focus))
        T.mark("pop")
        T.pause(0.4)
        T.prompt(a, "Who's peeking? Can you guess?", wait=2.8)
        sc["reveal_t"] = T.mark("sparkle")
        T.say(b, ans, gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- If you're happy and you know it (traditional)
    T.title("park", "IF YOU'RE HAPPY!", "mishu", "Let's sing a happy song and move our body!")
    sc = T.scene("happy", "park")
    acts = []
    for verse, act, icon in (("clap your hands!", "CLAP!", "hand"), ("stamp your feet!", "STAMP!", None), ("shout hooray!", "HOORAY!", "mouth")):
        acts.append((T.say("both", f"If you're happy and you know it, {verse}", gap=0.1), act, icon, verse))
        T.mark("clap" if act == "CLAP!" else "stomp2" if act == "STAMP!" else "yes")
        T.pause(1.4)
        T.say("both", f"If you're happy and you know it, {verse}", gap=0.1)
        T.mark("clap" if act == "CLAP!" else "stomp2" if act == "STAMP!" else "yes")
        T.pause(1.4)
    sc["acts"] = acts
    T.end(sc)
    # ---------------------------------------------------------------- Head, shoulders, knees and toes (traditional rhyme), slow then fast
    T.title("park", "HEAD, SHOULDERS, KNEES AND TOES!", "gul", "Now let's sing and touch! First slow, then super fast!")
    for rep, gap in ((0, 0.25), (1, 0.02)):
        sc = T.scene("song", "park", who="gul", fast=bool(rep))
        words = []
        for verse in (("Head!", "Shoulders!", "Knees!", "and toes!", "Knees!", "and toes!"),
                      ("Head!", "Shoulders!", "Knees!", "and toes!", "Knees!", "and toes!"),
                      ("And eyes!", "and ears!", "and mouth!", "and nose!")):
            for w in verse:
                T.mark("clap")
                words.append((T.say("both", w, gap=gap - 0.2), w))
            T.pause(0.2 if rep else 0.4)
        sc["words"] = words
        T.pause(0.6)
        T.say("mishu", "Wow, so fast! Phew!" if rep else "Great! Now super fast!", gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- outro
    sc = T.scene("outro", "playroom", who="gul")
    T.say("mishu", "We learned all about our body today!")
    T.say("gul", "And I will never lose my nose again! Boop!", gap=0.3)
    sc["bye_t"] = T.say("both", "Bye bye, friends!", gap=0.3)
    T.say("mishu", "See you next time!", gap=1.8)
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

    # ---------------------------------------------------------------- music: A major, 108 BPM, marimba bass + claps (new for this video)
    mus = np.zeros((n, 2))
    B = 60 / 108
    prog = [[69, 73, 76], [74, 78, 81], [76, 80, 83], [69, 73, 76]]
    tune = [81, 85, 88, 85, 86, 83, 81, 0, 83, 86, 88, 90, 88, 85, 81, 0]
    i, tt = 0, 0.0
    while tt < total:
        ch = prog[(i // 8) % 4]
        if i % 2 == 0:
            A.add(mus, M.xylo(ch[0] - 24, 0.4), tt, 0.16)
        if i % 4 == 2:
            A.add(mus, M.clap(), tt, 0.08, 0.15)
        if i % 2 == 1:
            A.add(mus, M.uke_chord(ch, 0.22), tt, 0.035, -0.25)
        if (i // 16) % 2 == 1 and tune[i % 16]:
            A.add(mus, M.xylo(tune[i % 16], 0.35), tt, 0.05, 0.3)
        tt += B / 2
        i += 1
    ts = np.arange(n) / SR
    mus *= (np.clip(ts / 0.4, 0, 1) * np.clip((total - ts) / 2.0, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.15)
    A.add(v, tracks["mishu"], 0, 1.0, 0.15)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.4 * e)[:, None]

    def bell():
        out = np.zeros(int(1.6 * SR))
        for k in range(2):
            x = A.tone(A.mtof(88), 0.9, ((1, 1), (2.7, 0.5), (5.4, 0.2)), 0.001, 0.35)
            out[int(k * 0.45 * SR): int(k * 0.45 * SR) + len(x)] += x
        return out

    def drum():
        n2 = int(0.3 * SR)
        t2 = np.arange(n2) / SR
        return np.sin(2 * np.pi * np.cumsum(60 + 80 * np.exp(-t2 / 0.03)) / SR) * np.exp(-t2 / 0.12)

    f = np.zeros((n, 2))
    for kind, at in T.fx:
        if kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.3)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.15)
        elif kind == "boing":
            A.add(f, M.boing(), at, 0.3)
        elif kind == "clap":
            A.add(f, M.clap(), at, 0.3)
        elif kind == "stomp":
            for k in range(3):
                A.add(f, M.stomp(), at + 1.2 + k * 0.35, 0.4)
        elif kind == "stomp2":
            for k in range(2):
                A.add(f, M.stomp(), at + 0.1 + k * 0.4, 0.45)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.12)
        elif kind == "bell":
            A.add(f, bell(), at + 0.1, 0.25)
            for k in range(2):
                A.add(f, drum(), at + 0.9 + k * 0.3, 0.5)
        elif kind == "sparkle":
            A.add(f, A.sfx_sparkle(), at, 0.2)
        elif kind == "sour":
            A.add(f, A.tone(A.mtof(60), 0.5, ((1, 1), (2, 0.5)), 0.01, 0.3) * np.linspace(1, 0.5, int(0.5 * SR)), at + 1.2, 0.15)
        elif kind == "yes":
            A.add(f, A.sfx_ding(79), at, 0.2)
            A.add(f, A.sfx_ding(84), at + 0.12, 0.2)
        elif kind == "no":
            A.add(f, A.tone(A.mtof(58), 0.25, ((1, 1), (2, 0.4)), 0.005, 0.1), at, 0.25)
            A.add(f, A.tone(A.mtof(55), 0.35, ((1, 1), (2, 0.4)), 0.005, 0.15), at + 0.22, 0.25)
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
