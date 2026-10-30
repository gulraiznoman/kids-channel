"""Long video 4: "Good Habits for Kids | Morning Routine" (a story morning with Gul & Mishu).
Voices, timeline.json, mix.wav. All songs are our own words; all sounds are made in code.  python make.py
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
        self.t += d + gap + 0.25                     # calmer pace for young kids
        return start

    def pause(self, s):
        self.t += s

    def scene(self, kind, bg, **data):
        sc = dict(kind=kind, bg=bg, t0=round(self.t, 3), **data)
        self.scenes.append(sc)
        return sc

    def end(self, sc):
        sc["t1"] = round(self.t, 3)

    def prompt(self, who, text, wait=2.6):
        self.say(who, text, gap=0.2)
        self.prompts.append((round(self.t, 3), round(self.t + wait + 0.4, 3)))
        self.pause(wait + 0.4)

    def mark(self, kind):
        self.fx.append((kind, round(self.t, 3)))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("whoosh")
        self.pause(0.6)
        self.say(who, text, gap=0.6)
        self.end(sc)


def build():
    T = TL()
    # ---------------------------------------------------------------- wake up!
    sc = T.scene("wake", "bedroom")
    T.pause(1.4)                                      # snoring "Zzz"
    sc["ring_t"] = T.mark("ring")
    T.pause(1.6)
    T.say("mishu", "Ring, ring! Wake up, Gul!")
    sc["wake_t"] = round(T.t, 3)
    T.say("gul", "Good morning, Mishu! Good morning, friends!", gap=0.4)
    T.say("mishu", "Today we'll learn good habits for the morning!", gap=0.4)
    T.say("gul", "Let's start our day!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- make the bed
    T.title("bedroom", "MAKE THE BED!", "mishu", "First, let's make our bed!")
    sc = T.scene("bed", "bedroom")
    T.say("gul", "Oh no, my bed is so messy!", gap=0.3)
    T.prompt("mishu", "What should we do?", wait=2.0)
    T.say("gul", "Pull up the blanket...", gap=0.2)
    T.say("gul", "and fluff the pillow!", gap=0.2)
    sc["fix_t"] = T.mark("sparkle")
    T.pause(0.8)
    T.stars.append(round(T.t, 3))
    T.say("mishu", "Wow! Nice and neat!", gap=0.4)
    sc["stretch_t"] = T.say("gul", "Now a big morning stretch! Reach up high!", gap=0.3)
    T.say("mishu", "Touch your toes! Up, and down!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- morning exercise (copy along)
    T.title("bedroom", "MORNING EXERCISE!", "mishu", "Let's wake up our bodies! Move with us!")
    sc = T.scene("exercise", "bedroom")
    moves = []
    for word, who, text in (("JUMP!", "gul", "Jump, jump, jump!"), ("CLAP!", "mishu", "Clap, clap, clap!"),
                            ("SPIN!", "gul", "Spin around!"), ("STOMP!", "mishu", "Stomp your feet!"),
                            ("WIGGLE!", "both", "Wiggle, wiggle, wiggle!")):
        moves.append((round(T.t, 3), word))
        T.mark("clap" if word == "CLAP!" else "pop")
        T.say(who, text, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 2.2, 3)))
        T.pause(2.2)
    sc["moves"] = moves
    T.stars.append(round(T.t, 3))
    T.say("gul", "Phew! Exercise makes us strong and happy!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- brush your teeth (own chant)
    T.title("bathroom", "BRUSH YOUR TEETH!", "gul", "Next, the bathroom! Time to brush our teeth!")
    sc = T.scene("brush", "bathroom")
    T.say("mishu", "First, a little bit of toothpaste. Just a pea size!", gap=0.3)
    sc["paste_t"] = T.mark("squeeze")
    T.pause(0.8)
    sc["brush_t"] = round(T.t, 3)
    chant = []
    for who, text in (("both", "Brush, brush, brush your teeth!"), ("gul", "Up and down, and round and round!"),
                      ("mishu", "Brush the front, and brush the back!"), ("gul", "Don't forget your tongue! Ahh!"),
                      ("both", "Brush, brush, brush your teeth!"), ("both", "Now our teeth are shiny bright!")):
        T.mark("clap")
        chant.append(T.say(who, text, gap=0.45))
    sc["chant"] = chant
    T.say("gul", "Your turn! Pretend to brush with us!", gap=0.2)
    T.prompts.append((round(T.t, 3), round(T.t + 4.0, 3)))
    T.pause(4.0)
    sc["rinse_t"] = T.say("mishu", "Now rinse, and spit!", gap=0.2)
    T.mark("splash")
    T.pause(0.8)
    sc["shine_t"] = T.mark("sparkle")
    T.stars.append(round(T.t, 3))
    T.say("gul", "Ta-da! Sparkly clean teeth!", gap=0.3)
    T.say("mishu", "Brush your teeth two times a day, morning and night!", gap=0.8)
    sc["brush_end"] = round(T.t, 3)
    T.end(sc)
    # ---------------------------------------------------------------- wash your hands (own chant, 20 seconds)
    T.title("bathroom", "WASH YOUR HANDS!", "mishu", "Now let's wash our hands! Germs, go away!")
    sc = T.scene("wash", "bathroom")
    steps = []
    for word, icon, who, text in (("WATER", "water", "gul", "Step one: wet your hands with water."),
                                  ("SOAP", "soap", "mishu", "Step two: take some soap."),
                                  ("SCRUB", "bubbles", "both", "Step three: scrub, scrub, scrub!")):
        steps.append((round(T.t, 3), word, icon))
        T.mark("pop")
        T.say(who, text, gap=0.4)
    sc["scrub_t"] = round(T.t, 3)
    chant = []
    for who, text in (("both", "Scrub, scrub, scrub your hands!"), ("gul", "Front and back, and in between!"),
                      ("mishu", "Thumbs and fingers, nails too!"), ("both", "Bubbles, bubbles, wash the germs!"),
                      ("gul", "Scrub, scrub, scrub your hands!"), ("mishu", "Now they're clean and shiny too!")):
        T.mark("bubble")
        chant.append(T.say(who, text, gap=0.5))
    sc["chant"] = chant
    T.say("mishu", "Rub your hands with us! Scrub, scrub, scrub!", gap=0.2)
    T.prompts.append((round(T.t, 3), round(T.t + 4.0, 3)))
    T.pause(4.0)
    for word, icon, who, text in (("RINSE", "water", "gul", "Step four: rinse off the bubbles."),
                                  ("DRY", "towel", "mishu", "Step five: dry with a towel!")):
        steps.append((round(T.t, 3), word, icon))
        T.mark("splash" if word == "RINSE" else "pop")
        T.say(who, text, gap=0.4)
    sc["steps"] = steps
    T.stars.append(round(T.t, 3))
    T.say("gul", "Wash your hands before you eat, and after the toilet!", gap=0.8)
    sc["scrub_end"] = steps[3][0]
    T.end(sc)
    # ---------------------------------------------------------------- get dressed
    T.title("bedroom", "GET DRESSED!", "gul", "Now let's get dressed for school!")
    sc = T.scene("dress", "bedroom")
    items = []
    for key, who, text in (("shirt", "mishu", "A shirt!"), ("shorts", "gul", "Shorts!"), ("socks", "mishu", "Socks!")):
        items.append((round(T.t, 3), key))
        T.mark("pop")
        T.say(who, text, gap=0.4)
    sc["q_t"] = round(T.t, 3)
    T.prompt("gul", "Big kids! What goes on first, socks or shoes?", wait=2.8)
    T.say("mishu", "Socks first! Then shoes!", gap=0.3)
    items.append((round(T.t, 3), "shoes"))
    T.mark("pop")
    T.say("gul", "Shoes!", gap=0.4)
    sc["items"] = items
    sc["change_gul"] = T.mark("poof")
    T.say("gul", "I'm all dressed!", gap=0.3)
    sc["change_mishu"] = T.mark("poof")
    T.say("mishu", "Me too! We look great!", gap=0.8)
    T.stars.append(round(T.t - 0.8, 3))
    T.end(sc)
    # ---------------------------------------------------------------- dress for the weather
    T.title("bedroom", "DRESS FOR THE WEATHER!", "gul", "Let's look outside! What should we wear today?")
    for k, (weather, items, who_q, q, who_a, a) in enumerate((
            ("rainy", ["umbrella", "boots", "raincoat"], "mishu", "It's raining! What do we need?", "gul", "An umbrella, rain boots, and a raincoat!"),
            ("cold", ["jacket", "scarf"], "gul", "Brrr, it's cold! What do we wear?", "mishu", "A warm jacket, and a scarf!"),
            ("sunny", ["sunhat", "sunglasses", "water"], "mishu", "It's hot and sunny! What do we need?", "gul", "A sun hat, sunglasses, and lots of water!"))):
        sc = T.scene("weather", "bedroom", weather=weather, items=items)
        T.mark("whoosh")
        T.pause(0.6)
        T.prompt(who_q, q, wait=2.6)
        sc["answer_t"] = T.mark("pop")
        T.say(who_a, a, gap=0.4)
        T.stars.append(round(T.t, 3))
        T.say(who_q, PRAISE[(k + 2) % len(PRAISE)], gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- healthy breakfast
    T.title("kitchen", "HEALTHY BREAKFAST!", "mishu", "Yum! Time for a healthy breakfast!")
    sc = T.scene("breakfast", "kitchen")
    food = []
    for key, who, text in (("milk", "gul", "Milk makes our bones strong!"), ("egg", "mishu", "An egg helps us grow big!"),
                           ("toast", "gul", "Toast gives us energy!"), ("oatmeal", "mishu", "Oatmeal with blueberries! Yummy!"),
                           ("banana", "gul", "A banana for our tummy!"), ("water", "mishu", "And a glass of water!")):
        food.append((round(T.t, 3), key))
        T.mark("pop")
        T.say(who, text, gap=0.5)
    sc["food"] = food
    T.say("gul", "Eat slowly, and chew, chew, chew!", gap=0.3)
    sc["eat_t"] = T.mark("munch")
    T.pause(1.0)
    T.say("mishu", "Mmm! All finished! Thank you for breakfast!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- healthy food or junk food?
    T.title("kitchen", "HEALTHY OR JUNK FOOD?", "gul", "Some food makes us strong. Some food is just a treat!")
    for k, (key, healthy, ans) in enumerate((
            ("apple", True, "An apple! Healthy food!"), ("soda", False, "Soda? Junk food! Too much sugar!"),
            ("carrot", True, "A carrot! Healthy and crunchy!"), ("chips", False, "Chips? Junk food! Just a little, sometimes."),
            ("milk", True, "Milk! Healthy for strong bones!"), ("donut", False, "A donut? Junk food! It's a treat."),
            ("broccoli", True, "Broccoli! Super healthy!"), ("cake", False, "Cake is a treat for special days!"),
            ("egg", True, "An egg! Healthy food!"), ("candy", False, "Candy? Junk food! Just a little!"))):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("junk", "kitchen", key=key, healthy=healthy)
        T.mark("pop")
        T.pause(0.6)
        T.prompt(a, "Healthy food, or junk food?", wait=2.4)
        sc["answer_t"] = T.mark("yes" if healthy else "no")
        T.say(b, ans, gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- pack the school bag
    T.title("hall", "PACK YOUR BAG!", "gul", "Now let's pack our school bag!")
    sc = T.scene("bag", "hall")
    packed = []
    for key, who, text in (("book", "mishu", "A book? Check!"), ("pencil", "gul", "A pencil? Check!"),
                           ("crayon", "mishu", "Crayons? Check!"), ("lunchbox", "gul", "Lunch box? Check!")):
        packed.append((round(T.t, 3), key))
        T.mark("pop")
        T.say(who, text, gap=0.5)
    sc["q_t"] = round(T.t, 3)
    T.prompt("mishu", "Hmm, did we forget something?", wait=2.6)
    packed.append((round(T.t, 3), "bottle"))
    T.mark("pop")
    T.say("gul", "Our water bottle! Check!", gap=0.4)
    sc["packed"] = packed
    sc["zip_t"] = T.mark("zip")
    T.pause(0.7)
    T.stars.append(round(T.t, 3))
    T.say("mishu", "Zip it up! We're ready for school!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- walk to school safely
    T.title("road", "SAFE ON THE ROAD!", "gul", "Now we walk to school. Let's be safe on the road!")
    sc = T.scene("road", "road")
    T.say("mishu", "Look! The light is red.", gap=0.3)
    sc["red_t"] = round(T.t, 3)
    T.prompt("gul", "Red light! What do we do?", wait=2.6)
    T.say("mishu", "We stop, and we wait!", gap=0.5)
    sc["left_t"] = T.say("gul", "Look left...", gap=0.3)
    sc["right_t"] = T.say("mishu", "Look right...", gap=0.3)
    sc["hold_t"] = T.say("gul", "And hold a grown-up's hand!", gap=0.5)
    sc["green_t"] = T.mark("yes")
    T.say("mishu", "Green light! Now we can cross. Let's go!", gap=0.4)
    sc["walk_t"] = round(T.t, 3)
    T.pause(1.6)
    T.stars.append(round(T.t, 3))
    T.say("gul", "Stop, look, and hold hands! Safe and sound!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- tidy up time
    T.title("bedroom", "TIDY UP TIME!", "mishu", "After school, we play. And then we tidy up!")
    sc = T.scene("tidy", "bedroom")
    toys = []
    for key, who, text in (("ball", "gul", "The ball goes in the box!"), ("blocks", "mishu", "The blocks go in the box!"),
                           ("teddy", "gul", "Teddy goes in the box!"), ("crayon", "mishu", "Crayons go in the box too!"),
                           ("car", "gul", "The toy car goes in the box!"), ("book", "mishu", "And books go on the shelf!")):
        toys.append((round(T.t, 3), key))
        T.mark("pop")
        T.say(who, text, gap=0.3)
        T.mark("drop")
        T.pause(0.5)
    sc["toys"] = toys
    T.say("both", "Tidy up, tidy up, put your toys away!", gap=0.4)
    sc["done_t"] = T.mark("sparkle")
    T.stars.append(round(T.t, 3))
    T.say("gul", "Our room is clean! Now we can find our toys again!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- helping at home
    T.title("hall", "HELPING AT HOME!", "mishu", "Good kids help at home! Let's help!")
    sc = T.scene("help", "hall")
    jobs = []
    for keys, word, who, text in ((("watering_can", "plant"), "WATER THE PLANTS", "gul", "I water the plants. Drink up, flowers!"),
                                  (("pet_bowl", "puppy"), "FEED THE PUPPY", "mishu", "I feed the puppy. Here you go, puppy!"),
                                  (("plates", "water"), "SET THE TABLE", "gul", "I set the table for dinner!")):
        jobs.append((round(T.t, 3), keys, word))
        T.mark("pop")
        T.say(who, text, gap=0.4)
        T.pause(0.8)
    sc["jobs"] = jobs
    T.prompt("mishu", "How do you help at home?", wait=2.8)
    T.stars.append(round(T.t, 3))
    T.say("gul", "Helping makes everyone happy!", gap=0.8)
    T.end(sc)
    # ---------------------------------------------------------------- magic words (role play)
    T.title("hall", "MAGIC WORDS!", "mishu", "Let's use our magic words!")
    sc = T.scene("polite", "hall")
    words = []
    words.append((T.say("mishu", "Gul, may I have the red crayon, please?", gap=0.3), "PLEASE", "mishu"))
    sc["give_t"] = T.mark("pop")
    T.say("gul", "Here you go, Mishu!", gap=0.3)
    words.append((T.say("mishu", "Thank you, Gul!", gap=0.3), "THANK YOU", "mishu"))
    words.append((T.say("gul", "You're welcome!", gap=0.6), "YOU'RE WELCOME", "gul"))
    sc["bump_t"] = T.mark("bonk")
    T.pause(0.6)
    words.append((T.say("gul", "Oops! I bumped you. Sorry, Mishu!", gap=0.3), "SORRY", "gul"))
    T.say("mishu", "That's okay, Gul!", gap=0.6)
    sc["sneeze_t"] = T.mark("sneeze")
    T.pause(0.9)
    words.append((T.say("mishu", "Achoo! Excuse me!", gap=0.4), "EXCUSE ME", "mishu"))
    T.say("gul", "Bless you!", gap=0.5)
    sc["share_t"] = T.mark("pop")
    words.append((T.say("gul", "Mishu, can I play with the ball too?", gap=0.3), "CAN I PLAY?", "gul"))
    words.append((T.say("mishu", "Yes! Let's take turns! You go first!", gap=0.4), "TAKE TURNS", "mishu"))
    T.stars.append(round(T.t, 3))
    T.say("both", "Please, thank you, sorry, excuse me! Magic words!", gap=0.8)
    sc["words"] = words
    T.end(sc)
    # ---------------------------------------------------------------- bedtime routine
    T.title("night", "BEDTIME!", "mishu", "The sun goes down. It's bedtime!")
    sc = T.scene("bedtime", "night")
    steps = []
    for key, word, who, text in (("bathtub", "BATH TIME", "gul", "First, a warm bath! Splish, splash!"),
                                 ("pyjamas", "PYJAMAS", "mishu", "Then we put on our pyjamas!"),
                                 ("toothbrush", "BRUSH AGAIN", "gul", "We brush our teeth again, before bed!"),
                                 ("book", "STORY TIME", "mishu", "Now, a bedtime story!"),
                                 ("moon", "GOOD NIGHT", "both", "Lights off. Good night, moon!")):
        steps.append((round(T.t, 3), key, word))
        T.mark("splash" if key == "bathtub" else "pop")
        T.say(who, text, gap=0.6)
    sc["steps"] = steps
    T.prompt("gul", "Big kids! What do we do before bed?", wait=2.8)
    T.say("mishu", "Bath, pyjamas, brush our teeth, and a story!", gap=0.4)
    sc["sleep_t"] = round(T.t, 3)
    T.say("gul", "Sleep helps us grow big and strong!", gap=0.4)
    T.say("both", "Good night!", gap=1.4)
    T.end(sc)
    # ---------------------------------------------------------------- game: good habit or bad habit?
    T.title("bedroom", "GOOD OR BAD HABIT?", "gul", "Game time! Is it a good habit, or a bad habit?")
    for k, (key, good, ans) in enumerate((
            ("toothbrush", True, "Brushing your teeth is a good habit!"),
            ("messy_toys", False, "Leaving toys everywhere? Bad habit! Let's tidy up!"),
            ("soap", True, "Washing your hands is a good habit!"),
            ("tv_late", False, "Watching TV all night? Bad habit! We need sleep!"),
            ("sharing", True, "Sharing with friends is a good habit!"),
            ("candy", False, "Eating lots of candy? Bad habit! Just a little, sometimes!"),
            ("water", True, "Drinking water is a good habit!"),
            ("bed_neat", True, "Making your bed is a good habit!"),
            ("traffic_red", True, "Stopping at the red light is a good habit!"),
            ("teddy", True, "Putting your toys away is a good habit!"),
            ("donut", False, "A donut for breakfast every day? Bad habit!"),
            ("plates", True, "Helping set the table is a good habit!"))):
        a, b = ("mishu", "gul") if k % 2 == 0 else ("gul", "mishu")
        sc = T.scene("habit", "bedroom", key=key, good=good)
        T.mark("pop")
        T.pause(0.7)
        T.prompt(a, "Good habit, or bad habit?", wait=2.6)
        sc["answer_t"] = T.mark("yes" if good else "no")
        T.say(b, ans, gap=0.3)
        if good:
            T.stars.append(round(T.t, 3))
        T.say(a, PRAISE[k % len(PRAISE)], gap=0.6)
        T.end(sc)
    # ---------------------------------------------------------------- goodbye chant
    sc = T.scene("outro", "bedroom")
    chant = []
    for who, text in (("both", "Good habits, every day!"), ("gul", "Brush and wash, and tidy away!"),
                      ("mishu", "Eat good food, and drink your water!"), ("both", "Please and thank you, that's the way!")):
        T.mark("clap")
        chant.append(T.say(who, text, gap=0.5))
    sc["chant"] = chant
    sc["bye_t"] = T.say("both", "Bye bye, friends! Have a happy day!", gap=2.0)
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

    # ---------------------------------------------------------------- music: D major, 100 BPM, bright ukulele + glockenspiel
    mus = np.zeros((n, 2))
    B = 60 / 100
    prog = [[62, 66, 69], [67, 71, 74], [69, 73, 76], [62, 66, 69]]
    tune = [74, 78, 81, 78, 79, 76, 74, 0, 76, 79, 81, 83, 81, 78, 74, 0]
    i, tt = 0, 0.0
    while tt < total:
        ch = prog[(i // 8) % 4]
        if i % 4 == 0:
            A.add(mus, M.tuba(ch[0] - 24, B * 1.6), tt, 0.14)
        if i % 2 == 1:
            A.add(mus, M.uke_chord([x + 12 for x in ch], 0.25), tt, 0.04, -0.25)
        if (i // 16) % 2 == 0 and tune[i % 16]:
            A.add(mus, A.tone(A.mtof(tune[i % 16] + 12), 0.6, ((1, 1), (2.76, 0.3), (5.4, 0.1)), 0.002, 0.3), tt, 0.03, 0.3)
        tt += B / 2
        i += 1
    ts = np.arange(n) / SR
    mus *= (np.clip(ts / 1.0, 0, 1) * np.clip((total - ts) / 2.0, 0, 1))[:, None]
    v = np.zeros((n, 2))
    A.add(v, tracks["gul"], 0, 1.0, -0.15)
    A.add(v, tracks["mishu"], 0, 1.0, 0.15)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.4 * e)[:, None]
    rng = np.random.default_rng(8)

    def noise(d, lp):
        return np.convolve(rng.standard_normal(int(d * SR)), np.ones(lp) / lp, mode="same")

    def ring():                                     # alarm bell: fast alternating metal tones
        out = np.zeros(int(1.5 * SR))
        for k in range(14):
            x = A.tone(A.mtof(88 if k % 2 else 91), 0.12, ((1, 1), (2.7, 0.5), (5.1, 0.25)), 0.001, 0.06)
            i0 = int(k * 0.1 * SR)
            out[i0:i0 + len(x)] += x
        return out

    def env_t(d, a, dec):
        t = np.arange(int(d * SR)) / SR
        return np.minimum(1, t / a) * np.exp(-t / dec)

    f = np.zeros((n, 2))
    for kind, at in T.fx:
        if kind == "ring":
            A.add(f, ring(), at, 0.35)
        elif kind in ("pop", "poof"):
            A.add(f, A.sfx_pop(), at, 0.3)
            if kind == "poof":
                A.add(f, A.sfx_sparkle(), at + 0.05, 0.25)
        elif kind == "whoosh":
            A.add(f, A.sfx_whoosh(), at, 0.15)
        elif kind == "sparkle":
            A.add(f, A.sfx_sparkle(), at, 0.25)
        elif kind == "clap":
            A.add(f, M.clap(), at, 0.35)
            A.add(f, M.clap(), at + 0.3, 0.25)
        elif kind == "squeeze":
            A.add(f, noise(0.4, 20)[: int(0.4 * SR)] * env_t(0.4, 0.05, 0.15) * 3, at, 0.3)
        elif kind == "splash":
            A.add(f, noise(0.6, 6)[: int(0.6 * SR)] * env_t(0.6, 0.01, 0.15) * 1.5, at, 0.35)
        elif kind == "bubble":
            for k in range(3):
                A.add(f, A.sfx_pop(), at + k * 0.12, 0.12)
        elif kind == "munch":
            for k in range(4):
                A.add(f, noise(0.08, 2)[: int(0.08 * SR)] * env_t(0.08, 0.002, 0.02), at + k * 0.22, 0.4)
        elif kind == "zip":
            A.add(f, noise(0.5, 2)[: int(0.5 * SR)] * env_t(0.5, 0.05, 0.4) * (1 + np.sin(np.arange(int(0.5 * SR)) / SR * 2 * np.pi * 60)), at, 0.25)
        elif kind == "bonk":
            A.add(f, M.boing(), at, 0.3)
        elif kind == "sneeze":
            A.add(f, noise(0.3, 4)[: int(0.3 * SR)] * env_t(0.3, 0.02, 0.08) * 1.2, at + 0.3, 0.3)
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
