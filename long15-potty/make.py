"""Long video 15: "Potty Training for Toddlers". python make.py"""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other, PRAISE

M = Maker(__file__)
MEET = [("potty", "This is a potty! It's just your size."), ("toilet", "This is a big toilet, for big kids and grown-ups."),
        ("stool", "A step stool helps you climb up!"), ("paper", "Toilet paper, for wiping."), ("soap", "Soap, to wash your hands."),
        ("towel", "A towel, to dry your hands."), ("undies", "And big kid underwear! Yay!"), ("chart", "A sticker chart, to collect stars!")]
SIGNS = [("wiggle", "Your tummy feels funny, and you wiggle and dance!"), ("hold", "You hold your tummy, or cross your legs."),
         ("stop", "You stop playing, because you need to go."), ("tell", "Then, tell a grown-up: I need to go potty!")]
STEPS = [("tell", "Tell a grown-up: I need to go!"), ("walk", "Go to the bathroom."), ("pants", "Pull your pants down."),
         ("sit", "Sit on the potty."), ("go", "Pee or poop. Relax, and take your time."), ("wipe", "Wipe with toilet paper."),
         ("up", "Pull your pants up."), ("flush", "Flush! Bye bye!"), ("wash", "Wash your hands with soap."), ("dry", "Dry your hands. All done!")]
STEP_SHORT = {"tell": "Tell!", "walk": "Go!", "pants": "Pants down!", "sit": "Sit!", "go": "Pee or poop!", "wipe": "Wipe!",
              "up": "Pants up!", "flush": "Flush!", "wash": "Wash!", "dry": "Dry!"}
RIGHTWRONG = [("wash", True, "Wash your hands after the potty?", "Yes! Always wash your hands!"),
              ("play", False, "Play with the toilet paper?", "No! Toilet paper is for wiping."),
              ("tell", True, "Tell a grown-up when you need to go?", "Yes! Good job!"),
              ("wait", False, "Wait and wait until it's too late?", "No! Go as soon as you feel it."),
              ("flush", True, "Flush when you're done?", "Yes! Flush, flush!"),
              ("toys", False, "Put toys in the toilet?", "No, no! Toys stay out of the toilet!"),
              ("stool", True, "Use a step stool to climb up?", "Yes! It helps you reach!"),
              ("rush", False, "Run out without pulling your pants up?", "No! Pants up first!"),
              ("try", True, "Try the potty before bedtime?", "Yes! Great idea!"),
              ("scared", True, "Tell a grown-up if you feel scared?", "Yes! Grown-ups can help!"),
              ("lid", True, "Close the lid before you flush?", "Yes! Close it, then flush!"),
              ("climb", False, "Climb on the sink?", "No! Use your step stool safely."),
              ("relax", True, "Sit and relax on the potty?", "Yes! Take your time."),
              ("hide", False, "Hide when you need to go?", "No! Tell a grown-up right away.")]
WHEN = [("sunny", "When you wake up in the morning!"), ("plate", "After you eat lunch!"), ("car", "Before a ride in the car!"),
        ("bathtub", "Before your bath!"), ("clock", "After your nap!"), ("ball", "Before you go out to play!"), ("moon", "And before you go to bed!")]
WORDS = [("potty", "Potty!"), ("toilet", "Toilet!"), ("paper", "Wipe!"), ("flushw", "Flush!"), ("pee", "Pee!"), ("poop", "Poop!")]
WHERE = [("bedroom", "At home!"), ("hall", "At school!"), ("park", "At the park! Ask a grown-up to find the bathroom."), ("kitchen", "At Grandma's house!")]
ANIMALS = [("puppy", "A puppy goes potty on the grass, outside!"), ("kitten", "A kitty goes potty in her litter box!"),
           ("duckling", "A duckling goes potty in the pond! Quack!"), ("elephant", "An elephant does a giant potty! Wow!")]
THISWAY = ["This is the way we sit on the potty,", "sit on the potty, sit on the potty!", "This is the way we flush the toilet,",
           "flush, flush, flush!", "This is the way we wash our hands,", "wash our hands, wash our hands!"]
DANCE = [("Wiggle, wiggle, potty dance!", "wiggle"), ("Hop to the bathroom!", "hop"), ("Sit down on the potty!", "sit"),
         ("Flush! Whoosh, whoosh!", "spin"), ("Wash, wash, wash your hands!", "shake"), ("Hooray! I did it!", "jump")]
QUIZ = [("What do you say when you need to go?", "I need to go potty!", "potty"), ("What do we use to wipe?", "Toilet paper!", "paper"),
        ("What do we do after we flush?", "Wash our hands!", "soap"), ("What helps you climb up?", "A step stool!", "stool"),
        ("Is it okay to have an accident?", "Yes! Just try again next time!", "heart"), ("What do big kids wear?", "Big kid underwear!", "undies"),
        ("What do we get on the sticker chart?", "A shiny star!", "star"), ("How long do we wash our hands?", "Count to twenty!", "soap"),
        ("Where does a puppy go potty?", "Outside, on the grass!", "puppy"), ("When should we try the potty?", "Before bed!", "moon"),
        ("What do we pull up after the potty?", "Our pants!", "undies"), ("Who can help us at the potty?", "A grown-up!", "heart"),
        ("Where do big kids wash their hands?", "At the sink!", "soap"), ("Is the hand dryer scary?", "No! It's just loud!", "heart"),
        ("What does a kitty use?", "A litter box!", "kitten"), ("What do we do before the car ride?", "Try the potty!", "car")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: Gul wiggles, "I need to go!", title
    sc = T.scene("intro", "bathroom2")
    sc["wiggle_t"] = T.mark("boing")
    T.say("gul", "Uh oh! I need to go! I need to go!", gap=0.2)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Potty time!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Let's learn how to use the potty, like a big kid!", gap=0.2)
    T.say("gul", "You can do it! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ MEET THE POTTY
    T.title("bathroom2", "MEET THE POTTY!", "mishu", "Let's look at everything in the bathroom!")
    for k, (key, text) in enumerate(MEET):
        sc = T.scene("meet", "bathroom2", key=key, num=k + 1, done=[m[0] for m in MEET[:k]])
        T.mark("pop")
        T.pause(0.2)
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ HOW DO I KNOW?
    T.title("bathroom2", "HOW DO I KNOW?", "gul", "How do you know when you need to go?")
    for k, (key, text) in enumerate(SIGNS):
        sc = T.scene("sign", "bathroom2", key=key)
        T.mark("boing" if k < 3 else "ding")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ POTTY STEPS (Gul), then quick recap (Mishu)
    T.title("bathroom2", "POTTY STEPS!", "mishu", "Let's do it step by step! Gul, your turn!")
    for k, (key, text) in enumerate(STEPS):
        sc = T.scene("step", "bathroom2", key=key, num=k + 1, who="gul")
        T.mark({"flush": "flush", "wash": "water", "go": "sparkle"}.get(key, "pop"))
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.2)
        T.prompt("gul" if k % 2 == 0 else "mishu", f"Step {k + 1}!", wait=0.9)
        T.end(sc)
    sc = T.scene("celebrate", "bathroom2", who="gul")
    sc["t_t"] = T.mark("tada")
    T.say("both", "Hooray! Gul did it all by himself!", gap=0.5)
    T.stars.append(sc["t_t"])
    T.end(sc)
    T.title("bathroom2", "NOW MISHU!", "gul", "Now Mishu's turn! Say the steps with us!")
    for k, (key, text) in enumerate(STEPS):
        sc = T.scene("step", "bathroom2", key=key, num=k + 1, who="misheal")
        T.mark({"flush": "flush", "wash": "water"}.get(key, "pop"))
        sc["say_t"] = T.say("both", text, gap=0.25)
        T.end(sc)
    # ------------------------------------------------------------ FAST RECAP
    T.title("bathroom2", "SUPER FAST!", "mishu", "Now let's say all the steps, super fast!")
    for k, (key, text) in enumerate(STEPS):
        sc = T.scene("step", "bathroom2", key=key, num=k + 1, who="gul" if k % 2 else "misheal")
        T.mark("pop")
        sc["say_t"] = T.say("both", STEP_SHORT[key], gap=0.05)
        T.end(sc)
    # ------------------------------------------------------------ WASH HANDS, COUNT TO 20
    sc = T.scene("wash", "bathroom2")
    T.say("mishu", "Wash your hands while we count to twenty! Scrub, scrub!", gap=0.1)
    sc["water_t"] = T.mark("water")
    ts = []
    for w in ("One", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
              "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"):
        ts.append(T.say("both", f"{w.capitalize()}!", gap=0.0))
    sc["ts"] = ts
    T.say("gul", "Clean hands! Germs, go away!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ THIS IS THE WAY (traditional rhyme, spoken)
    sc = T.scene("thisway", "bathroom2")
    sc["l"] = [T.say("both", ln, gap=0.15) for ln in THISWAY]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ WHEN DO WE TRY?
    T.title("bathroom2", "WHEN DO WE TRY?", "gul", "When is a good time to try the potty?")
    for k, (key, text) in enumerate(WHEN):
        sc = T.scene("when", "bathroom2", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WHERE CAN WE GO?
    T.title("bathroom2", "WHERE CAN WE GO?", "mishu", "Big kids can use the potty everywhere!")
    for k, (bg, text) in enumerate(WHERE):
        sc = T.scene("where", "bathroom2", place=bg)
        T.mark("whoosh")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ EVEN ANIMALS GO POTTY
    T.title("bathroom2", "ANIMALS GO POTTY TOO!", "gul", "Guess what? Everybody goes potty! Even animals!")
    for k, (key, text) in enumerate(ANIMALS):
        sc = T.scene("animal", "bathroom2", key=key)
        T.mark("boing")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.4)
        T.end(sc)
    sc = T.scene("animal", "bathroom2", key="potty")
    sc["say_t"] = T.say("both", "And you go on the potty, like a big kid!", gap=0.6)
    T.end(sc)
    # ------------------------------------------------------------ POTTY WORDS
    T.title("bathroom2", "POTTY WORDS!", "mishu", "Let's learn some potty words! Say them with us!")
    for k, (key, w) in enumerate(WORDS):
        sc = T.scene("pword", "bathroom2", key=key, w=w.rstrip("!").upper())
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", w, gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.3, 3)))
        T.pause(1.3)
        T.say("both", w, gap=0.3)
        T.end(sc)
    # ------------------------------------------------------------ THE LOUD HAND DRYER
    sc = T.scene("dryer", "bathroom2")
    sc["l1"] = T.say("gul", "Some bathrooms have a hand dryer.", gap=0.1)
    sc["whoosh_t"] = T.mark("dryer")
    T.pause(1.6)
    sc["scared_t"] = T.say("mishu", "Whoa! It's so loud!", gap=0.2)
    sc["ok_t"] = T.say("gul", "It's okay! It's just warm air. You can cover your ears!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ MISHU'S FIRST TIME
    sc = T.scene("mishu1", "bathroom2")
    sc["l1"] = T.say("mishu", "I need to go! I'll try the potty!", gap=0.2)
    sc["sit_t"] = T.say("gul", "Mishu sits on the potty, and waits.", gap=0.6)
    sc["done_t"] = T.mark("tada")
    T.say("mishu", "I did it! I went in the potty!", gap=0.2)
    T.say("gul", "Hooray, Mishu! High five!", gap=0.5)
    T.stars.append(sc["done_t"])
    T.end(sc)
    # ------------------------------------------------------------ OOPS! ACCIDENTS HAPPEN
    T.title("bathroom2", "OOPS!", "mishu", "Sometimes, we have an accident.")
    sc = T.scene("oops", "bathroom2")
    sc["sad_t"] = T.say("gul", "Oh no. I didn't make it in time.", gap=0.2)
    sc["ok_t"] = T.say("mishu", "That's okay, Gul! Everybody has accidents.", gap=0.2)
    T.say("mishu", "Let's change into dry clothes, and try again next time.", gap=0.2)
    sc["happy_t"] = T.say("gul", "Okay! Next time, I'll go sooner!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ TEDDY'S TURN (pretend play)
    T.title("bathroom2", "TEDDY'S TURN!", "gul", "Teddy wants to learn too! Let's help him!")
    sc = T.scene("teddy", "bathroom2")
    sc["l1"] = T.say("mishu", "Teddy says, I need to go!", gap=0.2)
    sc["l2"] = T.say("gul", "Teddy sits on the potty.", gap=0.3)
    sc["flush_t"] = T.mark("flush")
    T.say("mishu", "Flush! And now, wash your paws, Teddy!", gap=0.2)
    sc["yay_t"] = T.mark("tada")
    T.say("both", "Good job, Teddy!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ STICKER CHART
    T.title("bathroom2", "STICKER CHART!", "mishu", "Every time you use the potty, you get a star!")
    sc = T.scene("chart", "bathroom2")
    ts = []
    for w in ("One star!", "Two stars!", "Three stars!", "Four stars!", "Five stars!", "Six stars!", "Seven stars!"):
        ts.append(T.mark("sparkle"))
        T.say("both", w, gap=0.2)
    sc["ts"] = ts
    T.say("gul", "Seven stars! A whole week! I'm a potty star!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ BIG KID UNDERWEAR
    sc = T.scene("undies", "bathroom2")
    sc["in_t"] = T.mark("whoosh")
    T.say("mishu", "Now you can wear big kid underwear!", gap=0.2)
    sc["yay_t"] = T.mark("tada")
    T.say("both", "Bye bye, diapers! We're big kids now!", gap=0.6)
    T.end(sc)
    # ------------------------------------------------------------ YES OR NO?
    T.title("bathroom2", "YES OR NO?", "gul", "Big kids! Is it a good idea? Yes, or no?")
    for k, (key, good, q, ans) in enumerate(RIGHTWRONG):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("yesno", "bathroom2", key=key, good=good, q=q.upper())
        T.prompt(a, q, wait=1.8)
        sc["answer_t"] = T.mark("yes" if good else "buzz")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ POTTY STAR CHANT
    sc = T.scene("thisway", "bathroom2")
    sc["l"] = [T.say("both", ln, gap=0.2) for ln in ["Tell a grown-up, sit on the potty,", "wipe, and flush, and wash your hands!",
                                                     "I'm a potty star! I'm a potty star!", "Tell a grown-up, sit on the potty,",
                                                     "wipe, and flush, and wash your hands!", "I'm a potty star! Hooray!"]]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ POTTY DANCE
    T.title("bathroom2", "POTTY DANCE!", "mishu", "Stand up! It's time for the potty dance!")
    T.dance("bathroom2", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("bathroom2", "POTTY QUIZ!", "gul", "Quiz time! Are you ready?")
    T.quiz("bathroom2", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "bathroom2")
    T.say("mishu", "You're doing great! Keep practising, every day.", gap=0.2)
    T.say("gul", "Remember: tell a grown-up, sit, flush, and wash!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, potty stars!", gap=1.8)
    T.end(sc)
    return T


def sfx(kind):
    if kind == "flush":
        t = M.tt(1.8)
        nz = np.convolve(np.random.default_rng(1).standard_normal(len(t)), np.ones(25) / 25, mode="same")
        swirl = 0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)
        return [(nz * 4 * swirl * np.minimum(1, t / 0.1) * np.minimum(1, (1.8 - t) / 0.6), 0, 0.6)]
    if kind == "water":
        t = M.tt(1.6)
        nz = np.convolve(np.random.default_rng(2).standard_normal(len(t)), np.ones(4) / 4, mode="same")
        return [(nz * 0.35 * np.minimum(1, t / 0.1) * np.minimum(1, (1.6 - t) / 0.3), 0, 0.5)]
    if kind == "dryer":
        t = M.tt(1.5)
        nz = np.convolve(np.random.default_rng(3).standard_normal(len(t)), np.ones(3) / 3, mode="same")
        return [(nz * 0.5 * np.minimum(1, t / 0.1) * np.minimum(1, (1.5 - t) / 0.2), 0, 0.6)]
    if kind == "buzz":
        t = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t)) * 0.3 * np.minimum(1, (0.4 - t) / 0.05), 0, 0.4)]
    return None


if __name__ == "__main__":
    T = build()
    M.finish(T, music=dict(bpm=114, prog=[[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]), sfx=sfx)
