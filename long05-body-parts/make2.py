"""Body Parts v2: big impressive opening, 30 body parts with what they do, INSIDE MY BODY (brain, heart, lungs,
stomach, bones, muscles), five senses, games, energetic dance-beat music. Voices, timeline2.json, mix2.wav.
python make2.py
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
from make import line, PRAISE                                   # same voice cache as v1

SR = A.SR


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
        self.t += d + gap + 0.1
        return start

    def pause(self, s):
        self.t += s

    def scene(self, kind, bg, **data):
        sc = dict(kind=kind, bg=bg, t0=round(self.t, 3), **data)
        self.scenes.append(sc)
        return sc

    def end(self, sc):
        sc["t1"] = round(self.t, 3)

    def prompt(self, who, text, wait=2.2):
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


FACE = [  # part, label, line (what it does)
    ("head", "HEAD", "This is my head! My brain lives inside!"), ("hair", "HAIR", "My hair keeps my head warm!"),
    ("forehead", "FOREHEAD", "My forehead is above my eyes!"), ("brows", "EYEBROWS", "My eyebrows go up when I'm surprised!"),
    ("lashes", "EYELASHES", "My eyelashes keep dust out of my eyes!"), ("eyes", "EYES", "My eyes help me see!"),
    ("nose", "NOSE", "My nose helps me smell and breathe!"), ("cheeks", "CHEEKS", "Puff up your cheeks, like a balloon!"),
    ("ears", "EARS", "My ears help me hear!"), ("lips", "LIPS", "My lips can smile and blow kisses!"),
    ("teeth", "TEETH", "My teeth help me chew my food!"), ("tongue", "TONGUE", "My tongue helps me taste and talk!"),
    ("chin", "CHIN", "This is my chin, at the bottom of my face!")]
BODY = [
    ("neck", "NECK", "My neck holds up my head!"), ("shoulders", "SHOULDERS", "My shoulders can shrug!"),
    ("chest", "CHEST", "My chest goes up and down when I breathe!"), ("tummy", "TUMMY", "My tummy is where my food goes!"),
    ("arms", "ARMS", "My arms can give big hugs!"), ("elbows", "ELBOWS", "My elbows help my arms bend!"),
    ("wrists", "WRISTS", "My wrists help my hands wave!"), ("hands", "HANDS", "My hands can hold and clap!"),
    ("thumbs", "THUMBS", "Thumbs up! Thumbs help us hold things!"), ("fingers", "FINGERS", "I have ten fingers to wiggle!"),
    ("hips", "HIPS", "My hips help me dance! Wiggle, wiggle!"), ("legs", "LEGS", "My legs help me walk and run!"),
    ("knees", "KNEES", "My knees help my legs bend!"), ("ankles", "ANKLES", "My ankles help my feet move!"),
    ("feet", "FEET", "My feet help me stand and jump!"), ("toes", "TOES", "I have ten toes! Wiggle your toes!")]
COPY = {"cheeks": "Puff your cheeks with me!", "tongue": "Stick out your tongue! Bleh!", "chin": "Touch your chin!",
        "shoulders": "Shrug your shoulders!", "hands": "Clap your hands!", "hips": "Wiggle your hips!", "toes": "Stamp your feet!"}
INSIDE = [  # organ art, window, label, lines, sfx
    ("brain", "head", "BRAIN", ["Inside my head is my brain!", "My brain helps me think, learn and remember!"], "ding"),
    ("heart_organ", "chest", "HEART", ["Inside my chest is my heart! Thump, thump!", "My heart pumps blood all around my body!",
                                       "Put your hand on your chest. Can you feel it beating?"], "heart"),
    ("lungs", "chest", "LUNGS", ["These are my lungs!", "Lungs help me breathe. Breathe in... and breathe out!"], "breath"),
    ("stomach", "tummy", "STOMACH", ["This is my stomach!", "When I eat, my food goes down into my stomach!"], "gurgle"),
    ("bone", "leg", "BONES", ["Under my skin, I have bones!", "Bones make me strong. A grown-up has two hundred and six bones!"], "ding"),
    ("muscle", "arm", "MUSCLES", ["And these are muscles!", "Muscles help me move, run and jump! I'm so strong!"], "boing"),
    ("hand", "arm", "SKIN", ["My skin covers my whole body, like a cozy coat!", "Skin keeps germs out, and feels hot and cold!"], "sparkle"),
    ("mouth", "head", "TEETH", ["Kids have twenty baby teeth!", "Grown-ups have thirty two teeth! Brush them every day!"], "ding")]


def build():
    T = TL()
    # ---------------------------------------------------------------- BIG OPENING (0-7 s)
    sc = T.scene("intro", "stage")
    T.mark("drumroll")
    T.pause(1.6)
    sc["crash_t"] = T.mark("crash")
    T.pause(0.4)
    sc["logo_t"] = round(T.t, 3)
    T.pause(1.0)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Body Parts!", gap=0.2)
    T.say("gul", "Let's go!", gap=0.3)
    T.end(sc)
    # ---------------------------------------------------------------- hook: Gul lost his nose
    sc = T.scene("hook", "stage", who="gul")
    T.mark("boing")
    T.say("gul", "Oh no! Where is my nose?!", gap=0.2)
    sc["search_t"] = T.mark("whoosh")
    T.say("mishu", "Here it is! Catch!", gap=0.1)
    sc["found_t"] = T.mark("pop")
    T.pause(0.6)
    T.say("gul", "Boop! Thank you, Mishu!", gap=0.2)
    T.say("mishu", "Let's learn thirty body parts! Ready?", gap=0.3)
    T.end(sc)
    # ---------------------------------------------------------------- my face (13 parts, Mishu close-up)
    T.title("stage", "MY FACE!", "mishu", "Let's start with my face!")
    for k, (part, label, ln) in enumerate(FACE):
        sc = T.scene("face", "stage", who="misheal", part=part, label=label, num=k + 1, fact=ln)
        T.mark("pop")
        sc["label_t"] = round(T.t, 3)
        T.say("mishu" if k % 2 == 0 else "gul", ln, gap=0.2)
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", f"{label.title()}! Say it with me!", gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.3, 3)))
        T.pause(1.3)
        if part in COPY:
            T.prompt("gul" if k % 2 == 0 else "mishu", COPY[part], wait=1.8)
        T.end(sc)
    # ---------------------------------------------------------------- song break: head shoulders knees toes (beat)
    for rep, gp in ((0, -0.12), (1, -0.22)):
        sc = T.scene("song", "stage", who="gul", fast=bool(rep))
        words = []
        for w in ("Head!", "Shoulders!", "Knees!", "and toes!", "Knees!", "and toes!", "Head!", "Shoulders!", "Knees!", "and toes!", "Knees!", "and toes!",
                  "And eyes!", "and ears!", "and mouth!", "and nose!", "Head!", "Shoulders!", "Knees!", "and toes!", "Knees!", "and toes!"):
            T.mark("clap")
            words.append((T.say("both", w, gap=gp), w))
        sc["words"] = words
        T.pause(0.3)
        T.say("mishu", "Now super fast!" if rep == 0 else "Wow! So fast!", gap=0.3)
        T.end(sc)
    # ---------------------------------------------------------------- my body (16 parts, Gul full body)
    T.title("stage", "MY BODY!", "gul", "Now my whole body! Move with me!")
    for k, (part, label, ln) in enumerate(BODY):
        sc = T.scene("body", "stage", who="gul", part=part, label=label, num=len(FACE) + k + 1, fact=ln)
        T.mark("pop")
        sc["label_t"] = round(T.t, 3)
        sc["act_t"] = sc["label_t"]
        T.say("gul" if k % 2 == 0 else "mishu", ln, gap=0.2)
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", f"{label.title()}! Say it with me!", gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.3, 3)))
        T.pause(1.3)
        if part in COPY:
            T.mark("clap" if part == "hands" else "stomp2" if part == "toes" else "pop")
            T.prompt("mishu" if k % 2 == 0 else "gul", COPY[part], wait=1.8)
        T.end(sc)
    sc = T.scene("thirty", "stage")
    T.mark("crash")
    T.say("both", "Thirty body parts! Hooray!", gap=0.3)
    T.say("mishu", "Let's say them all, super fast!", gap=0.3)
    T.end(sc)
    for k, (part, label, ln) in enumerate(FACE + BODY):
        kind = "face" if k < len(FACE) else "body"
        sc = T.scene(kind, "stage", who="misheal" if kind == "face" else "gul", part=part, label=label, num=k + 1, fact="", quick=True)
        T.mark("clap")
        sc["label_t"] = round(T.t, 3)
        sc["act_t"] = sc["label_t"]
        T.say("both", label.title() + "!", gap=0.0)
        T.end(sc)
    # ---------------------------------------------------------------- left and right (older kids)
    T.title("stage", "LEFT AND RIGHT!", "gul", "Big kids! Let's learn left and right!")
    for k, (part, side, label, ln) in enumerate((("hands", 1, "RIGHT HAND", "Raise your right hand! Wave, wave!"),
                                                ("hands", 0, "LEFT HAND", "Now your left hand! Wave, wave!"),
                                                ("feet", 1, "RIGHT FOOT", "Stamp your right foot!"),
                                                ("feet", 0, "LEFT FOOT", "Stamp your left foot!"),
                                                ("ears", 1, "RIGHT EAR", "Touch your right ear!"),
                                                ("eyes", 0, "LEFT EYE", "Wink your left eye!"))):
        sc = T.scene("leftright", "stage", who="gul", part=part, side=side, label=label)
        T.mark("pop")
        sc["label_t"] = round(T.t, 3)
        T.prompt("mishu" if k % 2 == 0 else "gul", ln, wait=1.8)
        T.end(sc)
    # ---------------------------------------------------------------- zoom in! guess the body part
    T.title("stage", "ZOOM IN!", "mishu", "Zoom in game! What body part is this?")
    for k, (part, ans) in enumerate((("ears", "An ear!"), ("eyes", "An eye!"), ("hands", "A hand!"), ("nose", "A nose!"),
                                     ("knees", "A knee!"), ("hair", "Hair!"))):
        sc = T.scene("zoom", "stage", who="gul", part=part)
        T.mark("scan")
        T.prompt("gul" if k % 2 == 0 else "mishu", "What is it?", wait=2.2)
        sc["reveal_t"] = T.mark("whoosh")
        T.say("mishu" if k % 2 == 0 else "gul", ans, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- inside my body (x-ray)
    T.title("stage", "INSIDE MY BODY!", "mishu", "Now let's look inside! X-ray vision, on!")
    for k, (art, win, label, lines_, fx) in enumerate(INSIDE):
        sc = T.scene("xray", "stage", who="gul", art=art, win=win, label=label)
        T.mark("scan")
        T.pause(0.5)
        sc["label_t"] = round(T.t, 3)
        T.mark(fx)
        for j, ln in enumerate(lines_):
            T.say("mishu" if (k + j) % 2 == 0 else "gul", ln, gap=0.25)
        if art == "lungs":
            sc["breath_t"] = round(T.t, 3)
            T.prompts.append((round(T.t, 3), round(T.t + 3.2, 3)))
            T.pause(3.2)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- five senses
    T.title("park", "FIVE SENSES!", "gul", "Our body has five senses!")
    for k, (icon, objs, label, l1, l2) in enumerate((
            ("eye", ["rainbow"], "SEE", "I see a rainbow!", "We see with our eyes!"),
            ("ear", ["bell", "drum"], "HEAR", "Ding, ding! Boom, boom!", "We hear with our ears!"),
            ("nose", ["flower"], "SMELL", "Sniff, sniff! A sweet flower!", "We smell with our nose!"),
            ("mouth", ["lemon", "icecream"], "TASTE", "Lemon is sour! Ice cream is sweet!", "We taste with our tongue!"),
            ("hand", ["teddy", "cactus"], "TOUCH", "Teddy is soft! Cactus is spiky! Ouch!", "We touch with our skin!"))):
        sc = T.scene("sense", "park", icon=icon, objs=objs, label=label)
        T.mark("pop")
        sc["label_t"] = round(T.t, 3)
        sc["objs_t"] = T.mark({"HEAR": "bell", "TASTE": "sour", "TOUCH": "boing"}.get(label, "sparkle"))
        T.say("mishu", l1, gap=0.25)
        T.say("gul", l2, gap=0.3)
        T.end(sc)
    sc = T.scene("listen", "park")
    T.say("mishu", "Let's use our ears! Close your eyes...", gap=0.2)
    T.say("gul", "What can you hear?", gap=0.1)
    sc["sound_t"] = T.mark("bell")
    T.prompts.append((round(T.t, 3), round(T.t + 2.4, 3)))
    T.pause(2.4)
    T.say("mishu", "A bell! Ding, ding! Open your eyes!", gap=0.4)
    T.end(sc)
    # ---------------------------------------------------------------- Mishu says
    T.title("park", "MISHU SAYS!", "mishu", "Mishu Says! Only move if I say, Mishu says!")
    for k, (said, action) in enumerate(((True, "touch your head!"), (True, "puff your cheeks!"), (False, "touch your toes!"),
                                        (True, "wiggle your hips!"), (True, "thumbs up!"), (False, "jump!"),
                                        (True, "flex your muscles!"), (False, "sit down!"), (True, "wink your eye!"),
                                        (True, "wiggle your fingers!"), (False, "clap your hands!"), (True, "give a big hug!"))):
        sc = T.scene("says", "park", said=said, action=action.upper().rstrip("!"), icon=None)
        T.mark("ding")
        sc["say_t"] = T.say("mishu", ("Mishu says, " if said else "") + action, gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.8, 3)))
        T.pause(1.8)
        sc["result_t"] = T.mark("yes" if said else "no")
        T.say("gul", "Yes!" if said else "Oops! Mishu didn't say!", gap=0.3)
        T.end(sc)
    # ---------------------------------------------------------------- who's peeking
    T.title("park", "WHO'S PEEKING?", "gul", "Who's peeking through the window?")
    for k, (key, focus, ans) in enumerate((("elephant", (0.25, 0.62), "The elephant! Long trunk!"),
                                          ("bunny", (0.55, 0.12), "The bunny! Long ears!"),
                                          ("monkey", (0.82, 0.72), "The monkey! Curly tail!"),
                                          ("fish", (0.86, 0.5), "The fish! Tail fin!"),
                                          ("puppy", (0.5, 0.42), "The puppy! Wet nose!"), ("cub", (0.5, 0.25), "The lion! Fluffy mane!"))):
        sc = T.scene("peek", "park", key=key, focus=list(focus))
        T.mark("pop")
        T.prompt("mishu" if k % 2 == 0 else "gul", "Who is it?", wait=2.4)
        sc["reveal_t"] = T.mark("sparkle")
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.3)
        T.end(sc)
    # ---------------------------------------------------------------- If you're happy (traditional)
    sc = T.scene("happy", "park")
    acts = []
    for verse, act in (("clap your hands!", "CLAP!"), ("stamp your feet!", "STAMP!"), ("shout hooray!", "HOORAY!")):
        for rep in range(2):
            acts.append((T.say("both", f"If you're happy and you know it, {verse}", gap=0.0), act, None, verse))
            T.mark("clap" if act == "CLAP!" else "stomp2" if act == "STAMP!" else "crash")
            T.pause(1.2)
    sc["acts"] = acts
    T.end(sc)
    # ---------------------------------------------------------------- animal body parts
    T.title("park", "ANIMAL BODIES!", "gul", "Animals have special body parts too!")
    for k, (q, key, ans) in enumerate((("Who has a long trunk?", "elephant", "The elephant! Its trunk is its nose!"),
                                       ("Who has fins to swim?", "fish", "The fish!"),
                                       ("Who has wings and a beak?", "duckling", "The duckling! Quack!"),
                                       ("Who has a hard shell?", "turtle", "The turtle! Its shell is its house!"),
                                       ("Who has eight arms?", "octopus", "The octopus!"),
                                       ("Who has a long tail to swing?", "monkey", "The monkey!"))):
        sc = T.scene("animal", "park", key=key, q=q.upper())
        T.mark("ding")
        T.prompt("mishu" if k % 2 == 0 else "gul", q, wait=2.2)
        sc["reveal_t"] = T.mark("pop")
        T.say("gul" if k % 2 == 0 else "mishu", ans, gap=0.3)
        T.end(sc)
    # ---------------------------------------------------------------- big kids quiz
    T.title("stage", "BIG KIDS QUIZ!", "mishu", "Big kids quiz! Are you ready?")
    for k, (q, ans, icon) in enumerate((("What pumps blood around our body?", "Our heart!", "heart_organ"),
                                        ("What helps us breathe?", "Our lungs!", "lungs"),
                                        ("What helps us think?", "Our brain!", "brain"),
                                        ("What makes our body strong?", "Our bones and muscles!", "muscle"),
                                        ("Where does our food go?", "Into our stomach!", "stomach"),
                                        ("What covers our whole body?", "Our skin!", "hand"),
                                        ("What do we chew with?", "Our teeth!", "mouth"),
                                        ("How many bones does a grown-up have?", "Two hundred and six!", "bone"))):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("quiz", "stage", icon=icon, q=q.upper())
        T.mark("ding")
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(b, ans, gap=0.3)
        T.stars.append(round(T.t, 3))
        T.end(sc)
    # ---------------------------------------------------------------- outro
    sc = T.scene("outro", "stage", who="gul")
    T.mark("crash")
    T.say("mishu", "Your body is amazing!", gap=0.2)
    T.say("gul", "And I will never lose my nose again! Boop!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, friends!", gap=1.6)
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
        sf.write(HERE / f"vocal2_{s}.wav", (y / max(1e-9, np.abs(y).max()) * 0.9).astype(np.float32), SR, subtype="PCM_16")
    json.dump(dict(lines=T.lines, scenes=T.scenes, prompts=T.prompts, stars=T.stars, total=total), open(HERE / "timeline2.json", "w"), indent=1)
    mix = dance_music_mix(T, tracks, total)
    sf.write(HERE / "mix2.wav", mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"total {total}s ({total / 60:.1f} min), {len(T.lines)} lines, {len(T.scenes)} scenes")


# ==================================================================== exciting music + sounds
rng = np.random.default_rng(12)


def noise(d):
    return rng.standard_normal(int(d * SR))


def env(n, a, dcy):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dcy)


def kick():
    n2 = int(0.35 * SR)
    t = np.arange(n2) / SR
    return np.sin(2 * np.pi * np.cumsum(48 + 150 * np.exp(-t / 0.035)) / SR) * np.exp(-t / 0.16) * 1.2


def snare():
    n2 = int(0.22 * SR)
    t = np.arange(n2) / SR
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5
    nz = np.diff(np.concatenate([[0], noise(0.22)[:n2]])) * np.exp(-t / 0.07)
    return body + nz * 0.8


def hat(open_=False):
    n2 = int((0.18 if open_ else 0.05) * SR)
    x = np.diff(np.diff(np.concatenate([[0, 0], noise(n2 / SR)[:n2]])))
    return x * env(n2, 0.001, 0.06 if open_ else 0.012) * 0.35


def pluck_bass(m, d):
    f = A.mtof(m)
    n2 = int(d * SR)
    t = np.arange(n2) / SR
    saw = 2 * ((f * t) % 1) - 1
    sub = np.sin(2 * np.pi * f * t)
    lp = np.convolve(saw, np.ones(12) / 12, mode="same")
    return (0.6 * sub + 0.5 * lp) * env(n2, 0.004, 0.18)


def lead(m, d):
    f = A.mtof(m)
    n2 = int(d * SR)
    t = np.arange(n2) / SR
    sq = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * 2 * f * t) * 0.2
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f * vib) / SR)) * 0.5 + 0.25 * np.sin(2 * np.pi * np.cumsum(2 * f * vib) / SR)
    return np.convolve(sq, np.ones(6) / 6, mode="same") * env(n2, 0.01, 0.35)


def brass(chord, d):
    n2 = int(d * SR)
    t = np.arange(n2) / SR
    x = sum(2 * ((A.mtof(m) * t) % 1) - 1 for m in chord) / len(chord)
    return np.convolve(x, np.ones(8) / 8, mode="same") * np.minimum(1, t / 0.03) * np.exp(-t / 0.5)


def dance_music_mix(T, tracks, total):
    n = int(total * SR)
    mus = np.zeros((n, 2))
    B = 60 / 124
    prog = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]      # Am F C G (bouncy pop)
    hook = [76, 76, 79, 76, 74, 72, 74, 0, 72, 72, 74, 76, 79, 76, 74, 0]
    bar = 0
    tt = 2.6                                                         # music kicks in after the drum roll + crash
    while tt < total - 1.0:
        root, ch = prog[bar % 4]
        for q in range(4):
            b0 = tt + q * B
            A.add(mus, kick(), b0, 0.55)
            if q in (1, 3):
                A.add(mus, snare(), b0, 0.35, 0.05)
                A.add(mus, M.clap(), b0, 0.18, -0.05)
            for e in (0, 0.5):
                A.add(mus, hat(open_=(e == 0.5 and q == 3)), b0 + e * B, 0.5, 0.3)
            for e, mm in ((0, root - 12), (0.5, root), (0.75, root - 12)):
                A.add(mus, pluck_bass(mm, B * 0.45), b0 + e * B, 0.3)
            A.add(mus, A.tone(A.mtof(ch[q % 3] + 12), 0.25, ((1, 1), (2, 0.4), (3, 0.2)), 0.002, 0.08), b0 + 0.5 * B, 0.05, -0.3)
        if bar % 8 >= 4:                                             # catchy lead hook on alternate phrases
            for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                if mm:
                    A.add(mus, lead(mm, B * 0.48), tt + i * B / 2, 0.06, 0.2)
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
    for kind, at in T.fx:
        if kind == "drumroll":
            m2 = int(1.6 * SR)
            roll = np.zeros(m2)
            for k in range(40):
                s2 = snare() * (0.3 + 0.7 * k / 40)
                i0 = int(k * 0.04 * SR)
                roll[i0:i0 + len(s2)] += s2[: m2 - i0]
            A.add(f, roll, at, 0.5)
        elif kind == "crash":
            m2 = int(1.6 * SR)
            x = np.diff(np.concatenate([[0], noise(1.6)[:m2]])) * env(m2, 0.002, 0.5)
            A.add(f, x, at, 0.5)
            A.add(f, brass([60, 64, 67, 72], 1.0), at, 0.45)
            A.add(f, kick(), at, 0.6)
        elif kind == "slam":
            A.add(f, kick(), at, 0.8)
            A.add(f, brass([65, 69, 72, 77], 0.8), at, 0.4)
        elif kind == "riser":
            m2 = int(0.6 * SR)
            t2 = np.arange(m2) / SR
            sw = np.sin(2 * np.pi * np.cumsum(300 * 2 ** (3 * t2 / 0.6)) / SR) * (t2 / 0.6) * 0.5
            A.add(f, sw + np.diff(np.concatenate([[0], noise(0.6)[:m2]])) * (t2 / 0.6) * 0.3, at - 0.1, 0.35)
            A.add(f, M.clap(), at + 0.5, 0.4)
        elif kind == "pop":
            A.add(f, A.sfx_pop(), at, 0.3)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.25)
        elif kind == "boing":
            A.add(f, M.boing(), at, 0.35)
        elif kind == "clap":
            A.add(f, M.clap(), at, 0.35)
        elif kind == "stomp2":
            for k in range(2):
                A.add(f, M.stomp(), at + 0.1 + k * 0.4, 0.45)
        elif kind == "ding":
            A.add(f, A.sfx_ding(84), at, 0.15)
        elif kind == "scan":
            m2 = int(0.5 * SR)
            t2 = np.arange(m2) / SR
            A.add(f, np.sin(2 * np.pi * np.cumsum(600 + 900 * t2 / 0.5) / SR) * 0.4 * np.exp(-t2 / 0.4), at, 0.25)
        elif kind == "heart":
            for k in range(8):
                A.add(f, kick() * 0.8, at + k * 0.8, 0.6)
                A.add(f, kick() * 0.5, at + k * 0.8 + 0.22, 0.45)
        elif kind == "breath":
            m2 = int(4.0 * SR)
            t2 = np.arange(m2) / SR
            x = np.convolve(noise(4.0)[:m2], np.ones(30) / 30, mode="same") * np.abs(np.sin(np.pi * t2 / 2.0)) * 3
            A.add(f, x, at + 3.0, 0.2)
        elif kind == "gurgle":
            for k in range(5):
                A.add(f, M.boing() * 0.6, at + 1.0 + k * 0.18, 0.25)
        elif kind == "bell":
            for k in range(2):
                x = A.tone(A.mtof(88), 0.9, ((1, 1), (2.7, 0.5), (5.4, 0.2)), 0.001, 0.35)
                A.add(f, x, at + k * 0.45, 0.25)
        elif kind == "sour":
            A.add(f, A.tone(A.mtof(60), 0.5, ((1, 1), (2, 0.5)), 0.01, 0.3), at + 1.0, 0.15)
        elif kind == "sparkle":
            A.add(f, A.sfx_sparkle(), at, 0.25)
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
    mix = v + mus * 0.34 + f * 0.6
    mix /= np.abs(mix).max() / 0.9
    return mix


if __name__ == "__main__":
    build()
