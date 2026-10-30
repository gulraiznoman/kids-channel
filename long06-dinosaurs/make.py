"""Long video 6: "Dinosaurs for Kids". Voices, timeline.json, mix.wav. Own music + own sounds only.
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
PRAISE = ["Great job!", "Yay! You got it!", "Awesome!", "Well done!", "Super!", "Roar-some!"]

# key, display name, spoken name, fact, size class (big/mid/small), sound
DINOS = [
    ("trex", "T-REX", "T-Rex", "Tyrannosaurus Rex, or T-Rex! It had big, strong teeth and tiny little arms!", "big", "roar"),
    ("triceratops", "TRICERATOPS", "Triceratops", "Triceratops had three horns on its face. Tri means three!", "big", "roar"),
    ("stegosaurus", "STEGOSAURUS", "Stegosaurus", "Stegosaurus had big plates on its back, and spikes on its tail!", "big", "roar"),
    ("brachiosaurus", "BRACHIOSAURUS", "Brachiosaurus", "Brachiosaurus had a super long neck, to eat leaves from tall trees!", "big", "honk"),
    ("pteranodon", "PTERANODON", "Pteranodon", "Pteranodon could fly! It was a flying reptile, not really a dinosaur.", "mid", "screech"),
    ("velociraptor", "VELOCIRAPTOR", "Velociraptor", "Velociraptor was very fast, and it had feathers, like a bird!", "mid", "squeak"),
    ("ankylosaurus", "ANKYLOSAURUS", "Ankylosaurus", "Ankylosaurus had hard armour, like a tank, and a club on its tail!", "big", "roar"),
    ("spinosaurus", "SPINOSAURUS", "Spinosaurus", "Spinosaurus had a big sail on its back, and it loved to eat fish!", "big", "roar"),
    ("parasaurolophus", "PARASAUROLOPHUS", "Parasaurolophus", "Parasaurolophus had a long crest on its head, to make loud honking sounds!", "big", "honk"),
    ("diplodocus", "DIPLODOCUS", "Diplodocus", "Diplodocus had a long neck, and a very, very long tail!", "big", "honk"),
    ("pachycephalosaurus", "PACHYCEPHALOSAURUS", "Pachycephalosaurus", "Pachycephalosaurus had a hard, round dome on its head!", "mid", "roar"),
    ("compsognathus", "COMPSOGNATHUS", "Compsognathus", "Compsognathus was a tiny dinosaur, about as big as a chicken!", "small", "squeak"),
]


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

    def mark(self, kind, extra=None):
        self.fx.append((kind, round(self.t, 3), extra))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("riser")
        self.pause(0.5)
        self.say(who, text, gap=0.3)
        self.end(sc)


def build():
    T = TL()
    # ---------------------------------------------------------------- OPENING: rumble, egg cracks, baby T-Rex ROAR, title slam
    sc = T.scene("intro", "valley")
    T.mark("rumble")
    T.pause(1.3)
    sc["crack_t"] = T.mark("crack")
    T.pause(0.7)
    sc["hatch_t"] = T.mark("pop")
    T.mark("roar", "baby")
    T.pause(1.4)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Dinosaurs!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("gul", "Let's go on a dino adventure!", gap=0.2)
    T.say("mishu", "Let's meet twelve amazing dinosaurs!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- MEET THE DINOSAURS (12)
    T.title("valley", "MEET THE DINOSAURS!", "gul", "Stomp, stomp! Here they come!")
    for k, (key, label, name, fact, size, snd) in enumerate(DINOS):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("dino", "valley", key=key, label=label, num=k + 1, size=size, fact=fact)
        T.mark("stomps", size)
        T.pause(1.0)
        sc["roar_t"] = T.mark(snd, size)
        T.pause(0.9)
        sc["label_t"] = round(T.t, 3)
        T.say(a, fact, gap=0.25)
        T.say(b, {"roar": "Roar! Stomp, stomp!", "honk": "Honk, honk!", "screech": "Whoosh! Up in the sky!",
                  "squeak": "Zoom, zoom!"}[snd], gap=0.2)
        T.prompt(b, f"Can you say {name}?", wait=1.8)
        T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[k % len(PRAISE)], gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- DINO STOMP DANCE (copy along)
    T.title("valley", "DINO DANCE!", "mishu", "Dance time! Move like the dinosaurs!")
    for rnd in range(2):
        if rnd == 1:
            sc = T.scene("title", "valley", title="FASTER!")
            T.mark("riser")
            T.say("gul", "Again, but super fast!", gap=0.3)
            T.end(sc)
        for key, word, who, text in (("trex", "STOMP!", "gul", "Stomp like a T-Rex! Stomp, stomp, stomp!"),
                                     ("brachiosaurus", "STRETCH!", "mishu", "Stretch your neck up high, like a Brachiosaurus!"),
                                     ("pteranodon", "FLAP!", "gul", "Flap your wings, like a Pteranodon!"),
                                     ("stegosaurus", "SWISH!", "mishu", "Swish your tail, like a Stegosaurus!"),
                                     ("velociraptor", "RUN!", "gul", "Run super fast, like a Velociraptor!"),
                                     ("trex", "ROAR!", "both", "Now roar like a dinosaur! ROAR!")):
            sc = T.scene("dance", "valley", key=key, word=word, fast=rnd == 1)
            T.mark("stomp2" if word in ("STOMP!", "RUN!") else "roar" if word == "ROAR!" else "whoosh", "big")
            sc["say_t"] = T.say(who, text, gap=0.1)
            T.prompts.append((round(T.t, 3), round(T.t + (2.4 if rnd == 0 else 1.4), 3)))
            T.pause(2.4 if rnd == 0 else 1.4)
            T.end(sc)
    # ---------------------------------------------------------------- WHO'S MAKING THAT SOUND?
    T.title("valley", "WHO'S THAT SOUND?", "gul", "Listen carefully! Which dinosaur is making that sound?")
    for k, (snd, size, key, ans) in enumerate((("roar", "big", "trex", "A big roar! It's T-Rex!"),
                                              ("honk", None, "parasaurolophus", "Honk, honk! It's Parasaurolophus, with its long crest!"),
                                              ("screech", None, "pteranodon", "Skree! It's Pteranodon, flying in the sky!"),
                                              ("squeak", "small", "compsognathus", "A tiny squeak! It's little Compsognathus!"))):
        sc = T.scene("sound", "valley", key=key)
        T.say("mishu" if k % 2 == 0 else "gul", "Listen!", gap=0.1)
        sc["sound_t"] = T.mark(snd, size)
        T.pause(1.4)
        T.prompts.append((round(T.t, 3), round(T.t + 2.0, 3)))
        T.pause(2.0)
        sc["reveal_t"] = T.mark("yes")
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- COUNT THE DINOSAURS
    T.title("valley", "COUNT THE DINOS!", "mishu", "How many dinosaurs can you see?")
    for k, (key, n) in enumerate((("triceratops", 3), ("stegosaurus", 5), ("compsognathus", 4))):
        sc = T.scene("countd", "valley", key=key, n=n)
        T.mark("stomps", "mid")
        T.prompt("gul" if k % 2 == 0 else "mishu", "How many?", wait=1.8)
        sc["count_t"] = []
        for w in ("One!", "Two!", "Three!", "Four!", "Five!")[:n]:
            T.mark("ding")
            sc["count_t"].append(T.say("both", w, gap=0.05))
        sc["answer_t"] = T.mark("yes")
        T.say("mishu" if k % 2 == 0 else "gul", f"{['One', 'Two', 'Three', 'Four', 'Five'][n - 1]} dinosaurs!", gap=0.5)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- BIG OR SMALL
    T.title("valley", "BIG OR SMALL?", "gul", "Some dinosaurs were huge, and some were tiny!")
    for k, (bigk, smallk, q, ans, extra, extra_line) in enumerate((
            ("brachiosaurus", "compsognathus", "Which dinosaur is bigger?", "Brachiosaurus is big! Compsognathus is small!",
             "building", "Brachiosaurus was as tall as a four floor building!"),
            ("trex", "velociraptor", "Which one is bigger?", "T-Rex is big! Velociraptor is small, about as big as a turkey!", None, None),
            ("diplodocus", "pteranodon", "Who is longer?", "Diplodocus! It was as long as three buses!", None, None))):
        sc = T.scene("size", "valley", big=bigk, small=smallk, flip=k % 2 == 1, extra=extra)
        T.mark("stomps", "big")
        T.pause(0.6)
        T.prompt("mishu" if k % 2 == 0 else "gul", q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.3)
        if extra_line:
            sc["extra_t"] = T.say("mishu", extra_line, gap=0.4)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- PLANTS OR MEAT
    T.title("valley", "PLANTS OR MEAT?", "mishu", "What did dinosaurs eat? Plants, or meat?")
    for k, (key, plant, ans) in enumerate((("triceratops", True, "Triceratops ate plants!"),
                                           ("trex", False, "T-Rex ate meat!"),
                                           ("brachiosaurus", True, "Brachiosaurus ate leaves from tall trees!"),
                                           ("velociraptor", False, "Velociraptor ate meat!"),
                                           ("stegosaurus", True, "Stegosaurus ate plants!"),
                                           ("spinosaurus", False, "Spinosaurus ate fish!"),
                                           ("ankylosaurus", True, "Ankylosaurus ate plants!"))):
        sc = T.scene("eat", "valley", key=key, plant=plant)
        T.mark("stomps", "mid")
        T.pause(0.6)
        T.prompt("gul" if k % 2 == 0 else "mishu", "Plants, or meat?", wait=2.3)
        sc["answer_t"] = T.mark("yes")
        T.say("mishu" if k % 2 == 0 else "gul", ans, gap=0.4)
        T.end(sc)
    sc = T.scene("eatsum", "valley")
    T.say("gul", "Plant eaters are called herbivores!", gap=0.2)
    T.say("mishu", "And meat eaters are called carnivores!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- EGG HATCH GAME
    T.title("valley", "WHO WILL HATCH?", "gul", "Dinosaurs came from eggs! Who will hatch?")
    for k, (key, colour, ans) in enumerate((("triceratops", "#4FA3E0", "A baby Triceratops!"),
                                            ("stegosaurus", "#F2A65A", "A baby Stegosaurus!"),
                                            ("pteranodon", "#FF8FA3", "A baby Pteranodon! It wants to fly!"),
                                            ("trex", "#6CC24A", "A baby T-Rex! Hello, little one!"))):
        sc = T.scene("egg", "valley", key=key, colour=colour)
        T.mark("pop")
        T.pause(0.4)
        T.prompt("mishu" if k % 2 == 0 else "gul", "Crack, crack! Who is inside?", wait=2.2)
        sc["crack_t"] = T.mark("crack")
        T.pause(0.6)
        sc["hatch_t"] = T.mark("pop")
        T.mark("squeak", "small")
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- FOOTPRINTS
    T.title("dig", "DINO FOOTPRINTS!", "mishu", "Look! Giant footprints in the ground!")
    sc = T.scene("foot", "dig")
    T.pause(0.4)
    T.prompt("gul", "How many toes? Let's count!", wait=0.3)
    sc["count_t"] = []
    for w in ("One!", "Two!", "Three!"):
        T.mark("ding")
        sc["count_t"].append(T.say("both", w, gap=0.25))
    T.say("mishu", "Three big toes! Whose footprint is this?", gap=0.1)
    T.prompts.append((round(T.t, 3), round(T.t + 2.2, 3)))
    T.pause(2.2)
    sc["reveal_t"] = T.mark("roar", "big")
    T.say("gul", "It's T-Rex! Stomp, stomp!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- FOSSIL DIG
    T.title("dig", "FOSSIL DIG!", "gul", "Let's dig for dinosaur bones! Brush, brush, brush!")
    sc = T.scene("dig", "dig")
    sc["brush_t"] = T.mark("brush")
    T.say("mishu", "Brush away the sand, very gently.", gap=1.4)
    sc["reveal_t"] = T.mark("sparkle")
    T.say("gul", "Wow! A dinosaur skeleton!", gap=0.3)
    T.say("mishu", "Dinosaurs lived a long, long time ago, before there were any people!", gap=0.3)
    T.say("gul", "Today we find their bones in rocks. They are called fossils!", gap=0.3)
    sc["word_t"] = T.say("mishu", "People who dig up fossils are called paleontologists!", gap=0.1)
    T.prompt("gul", "Big kids, can you say paleontologist?", wait=2.0)
    T.stars.append(round(T.t, 3))
    T.say("mishu", "Wow, you're a dino expert!", gap=0.5)
    T.end(sc)
    # ---------------------------------------------------------------- DINO ABC
    T.title("valley", "DINO ABC!", "mishu", "Dinosaurs have letters too! Let's say the dino ABC!")
    for k, (letter, key, word) in enumerate((("A", "ankylosaurus", "A is for Ankylosaurus!"), ("B", "brachiosaurus", "B is for Brachiosaurus!"),
                                             ("D", "diplodocus", "D is for Diplodocus!"), ("P", "pteranodon", "P is for Pteranodon!"),
                                             ("S", "stegosaurus", "S is for Stegosaurus!"), ("T", "trex", "T is for T-Rex!"))):
        sc = T.scene("abc", "valley", letter=letter, key=key)
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", word, gap=0.2)
        T.say("both", f"{letter}!", gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- AMAZING DINO FACTS (big kids)
    T.title("valley", "AMAZING DINO FACTS!", "gul", "Big kids! Here are some amazing dino facts!")
    for k, (vis, text) in enumerate((("volcano", "Dinosaurs lived on Earth for more than one hundred and sixty million years!"),
                                    ("bird", "Birds are related to dinosaurs! A chicken is a tiny cousin of T-Rex!"),
                                    ("egg", "All dinosaurs hatched from eggs, just like baby birds!"),
                                    ("trex", "T-Rex had about sixty teeth, and some were as big as bananas!"),
                                    ("brachiosaurus", "The biggest dinosaurs were heavier than ten elephants!"))):
        sc = T.scene("fact", "valley", vis=vis, num=k + 1)
        T.mark("pop")
        T.pause(0.3)
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.3)
        T.say("gul" if k % 2 == 0 else "mishu", "Wow!", gap=0.5)
        T.end(sc)
    # ---------------------------------------------------------------- BIG KIDS QUIZ
    T.title("valley", "DINO QUIZ!", "mishu", "Dino quiz time! Are you ready?")
    for k, (q, key, ans) in enumerate((("Which dinosaur had three horns?", "triceratops", "Triceratops!"),
                                       ("Who could fly?", "pteranodon", "Pteranodon!"),
                                       ("Who had a super long neck?", "brachiosaurus", "Brachiosaurus!"),
                                       ("Who had plates on its back?", "stegosaurus", "Stegosaurus!"),
                                       ("Who was tiny, like a chicken?", "compsognathus", "Compsognathus!"),
                                       ("What do we call dinosaur bones in rocks?", "fossil", "Fossils!"),
                                       ("Who had a big sail on its back?", "spinosaurus", "Spinosaurus!"),
                                       ("Who had a club on its tail?", "ankylosaurus", "Ankylosaurus!"))):
        sc = T.scene("quiz", "valley", key=key, q=q.upper())
        T.mark("ding")
        T.prompt("gul" if k % 2 == 0 else "mishu", q, wait=2.5)
        sc["answer_t"] = T.mark("yes")
        T.say("mishu" if k % 2 == 0 else "gul", ans, gap=0.2)
        T.stars.append(round(T.t, 3))
        T.say("gul" if k % 2 == 0 else "mishu", PRAISE[(k + 2) % len(PRAISE)], gap=0.4)
        T.end(sc)
    # ---------------------------------------------------------------- OUTRO
    sc = T.scene("outro", "valley")
    T.mark("stomps", "big")
    T.say("mishu", "Which dinosaur is your favourite?", gap=0.2)
    T.say("gul", "Mine is T-Rex! ROAR!", gap=0.2)
    T.mark("roar", "big")
    sc["bye_t"] = T.say("both", "Bye bye, dino friends!", gap=1.8)
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
    mix = audio_mix(T, tracks, total)
    sf.write(HERE / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s ({total / 60:.1f} min), {len(T.lines)} lines, {len(T.scenes)} scenes")


# ==================================================================== music + dino sounds (all made in code)
rng = np.random.default_rng(31)


def tom(f0):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 + 60 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.14)


def roar(size):
    """Friendly cartoon roar: growly saw + noise with a playful rise at the end (not scary)."""
    d = {"big": 1.3, "mid": 0.9, "small": 0.6, "baby": 0.8}[size]
    base = {"big": 85, "mid": 140, "small": 260, "baby": 210}[size]
    n = int(d * SR)
    t = np.arange(n) / SR
    f = base * (1 + 0.35 * np.sin(np.pi * t / d)) * (1 + 0.03 * np.sin(2 * np.pi * 28 * t))
    ph = np.cumsum(f) / SR
    saw = 2 * (ph % 1) - 1
    nz = np.convolve(rng.standard_normal(n), np.ones(6) / 6, mode="same")
    x = np.convolve(saw * 0.8 + nz * 0.5, np.ones(10) / 10, mode="same")
    return x * np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.25) * 1.6


def honk():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 220 * (1 + 0.15 * np.sin(np.pi * t / 0.9))
    ph = np.cumsum(f) / SR
    x = np.sign(np.sin(2 * np.pi * ph)) * 0.5 + 0.4 * np.sin(4 * np.pi * ph)
    return np.convolve(x, np.ones(14) / 14, mode="same") * np.minimum(1, t / 0.05) * np.minimum(1, (0.9 - t) / 0.2)


def screech():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 900 + 700 * np.sin(np.pi * t / 0.6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.03) * np.exp(-t / 0.35) * 0.7


def squeak():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 700 * 2 ** (1.2 * t / 0.35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.02) * np.exp(-t / 0.15) * 0.8


def crack():
    out = np.zeros(int(0.5 * SR))
    for k in range(3):
        n = int(0.05 * SR)
        x = np.diff(np.concatenate([[0], rng.standard_normal(n)])) * A.env(n, 0.001, 0.012)
        i = int(k * 0.12 * SR)
        out[i:i + n] += x * 1.5
    return out


def rumble(d=1.4):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = np.convolve(rng.standard_normal(n), np.ones(300) / 300, mode="same") * 30
    return x * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.2) + 0.6 * np.sin(2 * np.pi * 40 * t) * np.minimum(1, t / 0.3)


def audio_mix(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 118
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]           # Am F C G: adventure-pop
    hook = [69, 72, 76, 74, 72, 69, 67, 0, 69, 72, 74, 76, 79, 76, 74, 0]
    bar, tt = 0, 3.3                                                     # music kicks in at the title slam
    while tt < total - 1.5:
        ch = prog[bar % 4]
        for q in range(4):
            b0 = tt + q * B
            A.add(mus, LS.kick(), b0, 0.55)
            if q in (1, 3):
                A.add(mus, RV.snare(), b0, 0.33, 0.05)
                A.add(mus, M.clap(), b0, 0.2, -0.05)
            A.add(mus, LS.hat(), b0 + B / 2, 0.55, 0.3)
            for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                A.add(mus, RV.bass(mm, B * 0.42), b0 + e * B, 0.3)
            A.add(mus, M.uke_chord([x + 12 for x in ch], 0.2), b0 + B / 2, 0.05, -0.3)
        if bar % 4 == 3:                                                 # jungle tom fill
            for k, f0 in enumerate((180, 150, 120, 95)):
                A.add(mus, tom(f0), tt + 3 * B + k * B / 4, 0.4, -0.2 + 0.13 * k)
        if bar % 8 >= 4:
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, RV.lead(mm, B * 0.45), tt + i * B / 2, 0.05, 0.2)
                    A.add(mus, M.xylo(mm + 12, 0.3), tt + i * B / 2, 0.03, -0.2)
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
    for kind, at, extra in T.fx:
        if kind == "rumble":
            A.add(f, rumble(), at, 0.5)
        elif kind == "crack":
            A.add(f, crack(), at, 0.6)
        elif kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.4)
            A.add(f, A.sfx_sparkle(), at + 0.05, 0.2)
        elif kind == "roar":
            A.add(f, roar(extra or "big"), at, 0.55)
        elif kind == "honk":
            A.add(f, honk(), at, 0.4)
        elif kind == "screech":
            A.add(f, screech(), at, 0.35)
        elif kind == "squeak":
            A.add(f, squeak(), at, 0.4)
        elif kind == "stomps":
            g = {"big": 0.55, "mid": 0.4, "small": 0.25}.get(extra, 0.4)
            for k in range(3):
                A.add(f, M.stomp(), at + k * 0.33, g)
        elif kind == "stomp2":
            for k in range(3):
                A.add(f, M.stomp(), at + 0.2 + k * 0.4, 0.45)
        elif kind == "slam":
            A.add(f, LS.kick() * 1.3, at, 0.9)
            A.add(f, A.sfx_sparkle(), at, 0.4)
        elif kind == "riser":
            A.add(f, A.sfx_whoosh(), at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.45, 0.4)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.3)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "brush":
            for k in range(8):
                nn = int(0.25 * SR)
                x = np.convolve(rng.standard_normal(nn), np.ones(4) / 4, mode="same") * A.env(nn, 0.05, 0.12)
                A.add(f, x, at + k * 0.3, 0.25)
        elif kind == "sparkle":
            A.add(f, A.sfx_sparkle(), at, 0.35)
        elif kind == "yes":
            A.add(f, A.sfx_ding(79), at, 0.2)
            A.add(f, A.sfx_ding(84), at + 0.12, 0.2)
    for st in T.stars:
        A.add(f, A.sfx_sparkle(), st, 0.15)
    for p0, p1 in T.prompts:
        A.add(f, A.sfx_ding(86), p0, 0.1)
    mix = v + mus * 0.34 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    return mix


if __name__ == "__main__":
    build()
