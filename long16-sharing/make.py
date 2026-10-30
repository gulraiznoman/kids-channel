"""Long video 16: "Sharing is Caring". python make.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other, PRAISE

M = Maker(__file__)
STORIES = [  # key, setup (Gul or Mishu has it), problem, solution, ending
    ("cookie", "Gul has one big cookie.", "Mishu has no cookie. She feels sad.", "Gul breaks the cookie in half. One for you, one for me!", "Yummy! Sharing is caring!"),
    ("crayons", "Mishu is drawing with all the crayons.", "Gul wants to draw too.", "Mishu shares her crayons. You take blue, I take red!", "Now we can draw together!"),
    ("swing", "There is only one swing.", "Gul and Mishu both want to swing!", "Let's take turns! Ten swings each. One, two, three...", "Taking turns is fair!"),
    ("umbrella", "Oh no! It's raining!", "Mishu forgot her umbrella.", "Gul shares his umbrella. Come under, Mishu!", "Now we both stay dry!"),
    ("sandcastle", "Gul has the bucket and the spade.", "Mishu wants to build a sandcastle too.", "Let's build it together! You dig, and I fill the bucket!", "Wow! A big sandcastle! Teamwork!"),
    ("car", "Mishu is playing with the toy car.", "Gul asks: Can I have a turn, please?", "Mishu says: Sure! Here you go! Vroom vroom!", "Asking nicely works!"),
    ("ball", "Gul is playing with his new ball.", "Mishu is sitting all alone.", "Gul says: Let's play catch together! Catch!", "Playing together is more fun!"),
    ("teddy", "Mishu has her favourite teddy.", "Gul fell down, and he is crying.", "Mishu says: Here, hug my teddy. You'll feel better!", "Sharing makes friends feel better!"),
    ("pizza", "Gul has a big pizza.", "Mishu is very hungry.", "Gul says: Let's share! Two slices for you, two for me!", "Pizza party for two!"),
    ("apple", "Mishu has two shiny apples.", "Gul has no snack today.", "Mishu says: One for you, and one for me!", "Crunch, crunch! Thank you, Mishu!")]
FAIR = [("cookie", 6, 2), ("apple", 4, 2), ("crayons1", 10, 2), ("strawberry", 8, 4), ("cookie", 8, 4), ("apple", 6, 3)]
FAMILY = [("plate", "At dinner, Gul shares his food with Papa. Here you go, Papa!"), ("crayons", "Mishu shares her crayons with her baby cousin."),
          ("cookie", "Gul shares his cookies with Grandma. Grandma smiles!"), ("teddy", "Mishu lets her little brother hold her teddy.")]
CHANT = ["Sharing, sharing, it's so nice!", "One for you, and one for me!", "Taking turns, and playing fair!", "Sharing is caring, everywhere!"]
TURNS = ["Gul's turn! Whee!", "Mishu's turn! Whee!", "Gul's turn again!", "Mishu's turn again!"]
THANKS = [("cookie", "Mishu shares a cookie with Gul."), ("crayons", "Gul shares his crayons with Mishu."),
          ("umbrella", "Mishu shares her umbrella."), ("ball", "Gul shares his ball.")]
KIND = [("share", True, "Sharing your toys with a friend?", "Kind! That's sharing!"),
        ("grab", False, "Grabbing a toy away from a friend?", "Unkind! Ask nicely instead."),
        ("wait", True, "Waiting for your turn on the slide?", "Kind! Taking turns!"),
        ("mine", False, "Shouting, Mine! Mine! Mine!", "Unkind! We can share."),
        ("help", True, "Helping a friend build a tower?", "Kind! Teamwork!"),
        ("thanks", True, "Saying thank you when a friend shares?", "Kind! Thank you!"),
        ("push", False, "Pushing to be first on the slide?", "Unkind! Wait in line."),
        ("invite", True, "Asking a lonely friend to play?", "Kind! Everyone can play!"),
        ("hide", False, "Hiding all the cookies for yourself?", "Unkind! Let's share them."),
        ("sorry", True, "Saying sorry when you bump a friend?", "Kind! Sorry helps.")]
ASK = [("ball", "Can I play with the ball too, please?", "Yes! Let's play together!"),
       ("swing", "Can I have a turn on the swing, please?", "Sure! After ten swings, it's your turn!"),
       ("crayons", "May I use the green crayon, please?", "Here you go! You're welcome!"),
       ("car", "Can we play with the car together, please?", "Yes! You push, and I'll catch!"),
       ("cookie", "May I have some cookie, please?", "Of course! Half for you!")]
DANCE = [("Share with your friend! Give, give, give!", "sway"), ("Take turns! You go, I go!", "hop"), ("Give a big hug!", "wiggle"),
         ("High five! Teamwork!", "jump"), ("Hearts so happy! Jump, jump!", "jump"), ("Sharing is caring! Hooray!", "spin")]
QUIZ = [("What do we say when we want a turn?", "Can I have a turn, please?", "heart"), ("What do we say when a friend shares?", "Thank you!", "heart"),
        ("Six cookies, two friends. How many each?", "Three each!", "cookie"), ("There is one swing. What do we do?", "Take turns!", "swing"),
        ("Is grabbing kind or unkind?", "Unkind! Ask nicely.", "car"), ("How does sharing make us feel?", "Happy!", "heart"),
        ("Your friend forgot her umbrella. What can you do?", "Share yours!", "umbrella"), ("Sharing is...?", "Caring!", "heart"),
        ("Eight cookies, four friends. How many each?", "Two each!", "cookie"), ("A friend is sitting alone. What can you do?", "Ask them to play!", "ball"),
        ("Who can we share with at home?", "Our family!", "heart"), ("Two friends want the swing. What do we do?", "Take turns!", "swing")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: tug of war over the teddy, MINE!
    sc = T.scene("intro", "room")
    sc["tug_t"] = T.mark("boing")
    T.say("gul", "Mine!", gap=0.0)
    T.say("mishu", "No, mine!", gap=0.1)
    sc["stop_t"] = T.mark("slam")
    T.say("both", "Sharing is caring!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Let's learn how to share, take turns, and be kind!", gap=0.2)
    T.say("gul", "Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ WHAT IS SHARING?
    T.title("room", "WHAT IS SHARING?", "gul", "What does sharing mean?")
    sc = T.scene("what", "room")
    sc["l1"] = T.say("mishu", "Sharing means letting a friend use or have some of what you have.", gap=0.2)
    sc["l2"] = T.say("gul", "When we share, our friends feel happy.", gap=0.2)
    sc["l3"] = T.say("mishu", "And we feel happy too! Our hearts grow big!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ SHARING STORIES
    T.title("park", "SHARING STORIES!", "mishu", "Let's watch Gul and Mishu learn to share!")
    for k, (key, setup, problem, solution, ending) in enumerate(STORIES):
        bg = "park" if key in ("swing", "sandcastle", "umbrella") else "room"
        sc = T.scene("story", bg, key=key, num=k + 1)
        sc["setup_t"] = T.say("gul" if k % 2 == 0 else "mishu", setup, gap=0.2)
        sc["prob_t"] = T.say("mishu" if k % 2 == 0 else "gul", problem, gap=0.1)
        T.prompt("gul" if k % 2 == 0 else "mishu", "What can we do?", wait=1.8)
        sc["sol_t"] = T.mark("sparkle")
        T.say("mishu" if k % 2 == 0 else "gul", solution, gap=0.2)
        sc["end_t"] = T.say("both", ending, gap=0.5)
        T.stars.append(sc["end_t"])
        T.end(sc)
    # ------------------------------------------------------------ FAIR SHARE (math)
    T.title("room", "FAIR SHARE!", "gul", "Big kids! Let's share fairly, so everyone gets the same!")
    for k, (key, n, people) in enumerate(FAIR):
        a = "mishu" if k % 2 == 0 else "gul"
        name = {"cookie": "cookies", "apple": "apples", "crayons1": "crayons", "strawberry": "strawberries"}[key]
        sc = T.scene("fair", "room", key=key, n=n, people=people)
        T.say(a, f"{n} {name}, for {people} friends.", gap=0.1)
        T.prompt(other(a), "How many does each friend get?", wait=1.8)
        sc["deal_t"] = T.mark("pop")
        T.say(a, f"One for you, one for me...", gap=0.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{['zero', 'one', 'two', 'three', 'four', 'five'][n // people].capitalize()} each! That's fair!", gap=0.4)
        T.stars.append(sc["answer_t"])
        T.end(sc)
    # ------------------------------------------------------------ MY TURN, YOUR TURN (slide)
    T.title("park", "MY TURN, YOUR TURN!", "gul", "There is one slide. Let's take turns!")
    sc = T.scene("turns", "park")
    sc["ts"] = []
    for k, text in enumerate(TURNS):
        sc["ts"].append(T.mark("whoosh"))
        T.say("mishu" if k % 2 else "gul", text, gap=1.0)
    T.say("both", "Taking turns is fun, and fair!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ HOW TO ASK NICELY
    T.title("park", "ASK NICELY!", "mishu", "When you want a turn, ask nicely!")
    for k, (key, ask, ans) in enumerate(ASK):
        sc = T.scene("ask", "park", key=key)
        sc["ask_t"] = T.say("gul" if k % 2 == 0 else "mishu", ask, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.8, 3)))
        T.say("both", "Your turn! Say it with us!", gap=1.6)
        sc["ans_t"] = T.mark("sparkle")
        T.say("mishu" if k % 2 == 0 else "gul", ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ KIND OR UNKIND?
    T.title("room", "KIND OR UNKIND?", "gul", "Is it kind, or unkind? You decide!")
    for k, (key, good, q, ans) in enumerate(KIND):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("kind", "room", key=key, good=good, q=q.upper())
        T.prompt(a, q, wait=1.8)
        sc["answer_t"] = T.mark("yes" if good else "buzz")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ SAY THANK YOU
    T.title("room", "SAY THANK YOU!", "mishu", "When a friend shares, what do we say?")
    for k, (key, text) in enumerate(THANKS):
        sc = T.scene("thanks", "room", key=key)
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.6, 3)))
        T.pause(1.6)
        sc["ty_t"] = T.mark("sparkle")
        T.say("both", "Thank you!", gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ SHARING AT HOME
    T.title("room", "SHARING AT HOME!", "gul", "We can share with our family too!")
    for k, (key, text) in enumerate(FAMILY):
        sc = T.scene("family", "room", key=key, num=k + 1)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ SHARING CHANT
    sc = T.scene("chant", "room")
    sc["l"] = [T.say("both", ln, gap=0.25) for ln in CHANT * 3]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ THE HAPPY HEART
    sc = T.scene("heart", "room")
    sc["l1"] = T.say("mishu", "Every time we share, our heart grows bigger!", gap=0.1)
    sc["grow"] = []
    for w in ("Share a toy!", "Take a turn!", "Say thank you!", "Help a friend!"):
        sc["grow"].append(T.mark("sparkle"))
        T.say("both", w, gap=0.25)
    T.say("gul", "A big, happy heart!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ SHARING DANCE
    T.title("park", "SHARING DANCE!", "mishu", "Stand up! Let's do the sharing dance!")
    T.dance("park", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("room", "SHARING QUIZ!", "gul", "Quiz time! Are you ready?")
    T.quiz("room", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "park")
    T.say("mishu", "Today, share something with a friend, or your family!", gap=0.2)
    T.say("gul", "Remember: sharing is caring!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, kind friends!", gap=1.8)
    T.end(sc)
    return T


def sfx(kind):
    if kind == "buzz":
        import numpy as np
        t = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t)) * 0.3 * np.minimum(1, (0.4 - t) / 0.05), 0, 0.4)]
    return None


if __name__ == "__main__":
    T = build()
    M.finish(T, music=dict(bpm=110, prog=[[65, 69, 72], [62, 65, 69], [58, 62, 65], [60, 64, 67]]), sfx=sfx)
