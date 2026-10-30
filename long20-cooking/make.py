"""Long video 20: "Cooking for Kids: Let's Make Pizza!". python make.py
Music: our own tune, code instruments."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
CHEF = [("hands", "First, wash your hands with soap! Scrub, scrub!"), ("apron", "Put on your apron!"), ("chefhat", "And a chef hat! Now we're real chefs!")]
SAFETY = [("hands", "Always cook with a grown-up!", True), ("oven", "The oven is hot! Don't touch!", False),
          ("mitt", "Grown-ups use oven mitts for hot things!", True), ("knife", "Only grown-ups use sharp knives!", False)]
TOOLS = [("rollingpin", "Rolling pin!", "It rolls dough flat!"), ("whisk", "Whisk!", "It mixes things fast! Whisk, whisk!"),
         ("bowl", "Bowl!", "We mix things in it!"), ("spoon", "Spoon!", "Stir, stir, stir!"), ("mitt", "Oven mitt!", "It keeps hands safe from hot things!"),
         ("blender", "Blender!", "It blends fruit into a smoothie! Vrrrr!"), ("oven", "Oven!", "It bakes food nice and hot!")]
INGRED = [("flour", "Flour, to make the dough!"), ("sauce", "Tomato sauce! Red and yummy!"), ("cheese", "Cheese! Lots of cheese!"),
          ("olive", "Olives!"), ("pepper", "Green peppers!"), ("mushroom", "Mushrooms!")]
STEPS = [("mix", "Mix the flour and water in a bowl. Stir, stir, stir!"), ("knead", "Squish the dough with your hands! Push and squish!"),
         ("roll", "Roll it flat with the rolling pin. Roll, roll, roll!"), ("sauce", "Spread the red tomato sauce! Round and round!"),
         ("cheese", "Sprinkle the cheese! Sprinkle, sprinkle!"), ("bake", "A grown-up puts it in the hot oven. Bake, bake, bake!")]
TOPS = [("olive", 5, "olives"), ("pepper", 4, "green peppers"), ("mushroom", 3, "mushrooms")]
SLICE = [(2, "Cut it in half! Two pieces! One for Gul, one for Mishu!"), (4, "Cut it again! Four pieces! For the whole family!"),
         (8, "And again! Eight slices! Let's count them!")]
SMOOTHIE = [("strawberry", "Add red strawberries!"), ("banana", "Add a yellow banana!"), ("milk", "Pour in some milk!"),
            ("blend", "A grown-up turns on the blender! Vrrrr!"), ("pour", "Pour it in a cup! A pink smoothie!")]
KEBAB = [("strawberry", "red", "Red strawberry!"), ("orange", "orange", "Orange orange!"), ("pineapple", "yellow", "Yellow pineapple!"),
         ("kiwi", "green", "Green kiwi!"), ("grapes", "purple", "Purple grapes!")]
TASTE = [("banana", "sweet", "Bananas taste sweet!"), ("carrot", "crunchy", "Carrots are crunchy! Crunch, crunch!"),
         ("watermelon", "juicy", "Watermelon is juicy!"), ("chips", "salty", "Chips are salty!"), ("cheese", "yummy", "Cheese is soft and yummy!"), ("icecream", "creamy", "Ice cream is cold and creamy!"), ("pizza", "cheesy", "Pizza is warm and cheesy!")]
HOTCOLD = [("pizza", True, "Pizza from the oven!"), ("icecream", False, "Ice cream!"), ("pot", True, "Soup in a pot!"),
           ("smoothie", False, "A smoothie!"), ("oven", True, "The oven!"), ("milk", False, "Milk from the fridge!"), ("toast", True, "Toast from the toaster!"), ("icepop", False, "Frozen fruit pops!")]
NEED = [("To make pizza, we need...", ["cheese", "teddy", "ball"], "cheese", "Cheese!"),
        ("To make a smoothie, we need...", ["shoes", "blender", "book"], "blender", "A blender!"),
        ("To roll the dough, we need...", ["rollingpin", "toothbrush", "car"], "rollingpin", "A rolling pin!"),
        ("To flip the pancake, we need...", ["ball", "teddy", "pan"], "pan", "A pan!")]
CLEAN = [("Put the food away.", "fridge"), ("Wash the dishes. Splash, splash!", "plates"), ("Wipe the table.", "sponge"),
         ("Wash your hands again!", "hands")]
PANCAKE = [("egg", "Crack an egg into the bowl. Crack!"), ("flour", "Add flour!"), ("milk", "Pour in milk!"),
           ("whisk", "Whisk, whisk, whisk! Nice and smooth!"), ("pan", "A grown-up cooks it in a hot pan. Sizzle!"),
           ("flip", "Flip the pancake! Up, and over!"), ("stack", "Add strawberries and banana on top! Yummy pancakes!")]
SANDWICH = [("bread", "A slice of bread!"), ("cheese", "A slice of cheese!"), ("tomato", "Red tomato!"), ("lettuce", "Green lettuce!"),
            ("bread", "And bread on top!")]
KSOUNDS = [("sizzle", "pan", "Sizzle, sizzle! Something cooking in the pan!"), ("chop", "knife", "Chop, chop! A grown-up is chopping!"),
           ("blend", "blender", "Vrrrr! The blender!"), ("ovending", "oven", "Ding! The oven! Food is ready!")]
HEALTHY = [("broccoli", True, "Broccoli?", "Healthy! Makes you strong!"), ("donut", False, "A donut?", "A treat! Just a little bit!"),
           ("apple", True, "An apple?", "Healthy! Crunch!"), ("cupcake", False, "A cupcake?", "A treat! Yummy, but just sometimes!"),
           ("carrot", True, "A carrot?", "Healthy! Good for your eyes!"), ("chips", False, "Chips?", "A treat! Just a few!")]
TABLE = [("plate", "A plate!"), ("spoon", "A spoon!"), ("cup", "A cup!"), ("napkin", "And a napkin! The table is ready! Let's eat!")]
FULLEMPTY = [("full", "This cup is full!"), ("empty", "This cup is empty!"), ("half", "And this cup is half full!")]
POPS = [("pour", "Pour fruit juice into the moulds."), ("stick", "Put in the sticks."), ("freeze", "Put them in the freezer. Brrr! Wait, wait, wait!"),
        ("done", "Ta-da! Frozen fruit pops! Cold and yummy!")]
DANCE = [("Stir the pot!", "spin"), ("Squish the dough!", "jump"), ("Roll it flat!", "sway"),
         ("Sprinkle the cheese!", "shake"), ("Chop, chop, chop!", "stomp"), ("Yummy in my tummy!", "wiggle")]
QUIZ = [("What do we wash before cooking?", "Our hands!", "hands"), ("What rolls the dough flat?", "A rolling pin!", "rollingpin"),
        ("Is the oven hot or cold?", "Hot! Don't touch!", "oven"), ("What red sauce goes on pizza?", "Tomato sauce!", "sauce")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: pizza zooms in
    sc = T.scene("intro", "kitchen")
    T.pause(0.3)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Let's cook!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Today, we're making yummy pizza, a smoothie, and rainbow fruit sticks!", gap=0.2)
    T.say("gul", "Come and cook with us! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ BE A CHEF
    T.title("kitchen", "LITTLE CHEFS!", "gul", "First, let's get ready to be chefs!")
    for k, (key, text) in enumerate(CHEF):
        sc = T.scene("chef", "kitchen", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ SAFETY
    T.title("kitchen", "KITCHEN SAFETY!", "mishu", "Kitchens can be hot! Let's learn the safety rules!")
    for k, (key, text, ok) in enumerate(SAFETY):
        sc = T.scene("safety", "kitchen", key=key, ok=ok)
        T.mark("yes" if ok else "buzz")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ TOOLS
    T.title("kitchen", "KITCHEN TOOLS!", "gul", "Let's learn the kitchen tools! Say them with us!")
    for k, (key, name, use) in enumerate(TOOLS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("tool", "kitchen", key=key, w=name.rstrip("!").upper(), num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say(a, name, gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.0, 3)))
        T.pause(1.0)
        T.say(other(a), use, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ INGREDIENTS
    T.title("kitchen", "PIZZA INGREDIENTS!", "mishu", "What do we need to make pizza? Let's see!")
    sc = T.scene("ingred", "kitchen")
    sc["ts"] = []
    for k, (key, text) in enumerate(INGRED):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.25)
    sc["sum_t"] = T.say("both", "Six things! Let's make pizza!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ PIZZA STEPS
    T.title("kitchen", "LET'S MAKE PIZZA!", "gul", "Step by step! Let's make pizza!")
    for k, (key, text) in enumerate(STEPS):
        sc = T.scene("step", "kitchen", key=key, num=k + 1)
        T.mark("whoosh" if key == "bake" else "pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.6)
        T.end(sc)
    # ------------------------------------------------------------ TOPPINGS COUNT
    T.title("kitchen", "COUNT THE TOPPINGS!", "mishu", "Let's put toppings on our pizza! Count with us!")
    for si, (key, n, plural) in enumerate(TOPS):
        a = "gul" if si % 2 == 0 else "mishu"
        sc = T.scene("tops", "kitchen", stage=si, n=n)
        T.say(a, f"Now, {plural}!", gap=0.1)
        sc["cts"] = []
        for i in range(1, n + 1):
            sc["cts"].append(T.mark("pop"))
            T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
        sc["sum_t"] = T.say(other(a), f"{NUM[n].capitalize()} {plural}!", gap=0.5)
        T.stars.append(sc["sum_t"])
        T.end(sc)
    sc = T.scene("baked", "kitchen")
    sc["ding_t"] = T.mark("ovending")
    T.pause(1.0)
    T.say("gul", "Ding! The pizza is ready!", gap=0.2)
    sc["out_t"] = T.mark("tada")
    T.say("mishu", "A grown-up takes it out, with oven mitts! Ta-da! Hot pizza!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ SLICE
    T.title("kitchen", "SLICE THE PIZZA!", "gul", "Let's cut the pizza into slices!")
    for k, (n, text) in enumerate(SLICE):
        sc = T.scene("slice", "kitchen", n=n)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.2)
        if n == 8:
            sc["cts"] = []
            for i in range(1, 9):
                sc["cts"].append(T.mark("pop"))
                T.say("both", f"{NUM[i].capitalize()}!", gap=0.1)
        T.pause(0.4)
        T.end(sc)
    sc = T.scene("pizzaface", "kitchen")
    T.say("mishu", "Let's make a silly pizza face!", gap=0.1)
    sc["ts"] = []
    for text in ("Two olive eyes!", "A mushroom nose!", "And a pepper smile!"):
        sc["ts"].append(T.mark("pop"))
        T.say("gul", text, gap=0.25)
    sc["done_t"] = T.mark("tada")
    T.say("both", "Hello, Mister Pizza! Ha ha!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ PANCAKES
    T.title("kitchen", "LET'S MAKE PANCAKES!", "gul", "Next recipe! Fluffy pancakes!")
    for k, (key, text) in enumerate(PANCAKE):
        sc = T.scene("pancake", "kitchen", key=key, num=k + 1)
        T.mark({"egg": "crack", "pan": "sizzle", "flip": "whoosh"}.get(key, "pop"))
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ COOKIE TRAY
    sc = T.scene("tray", "kitchen")
    T.say("mishu", "We baked cookies too! Let's count them!", gap=0.1)
    sc["cts"] = []
    for i in range(1, 11):
        sc["cts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i].capitalize()}!", gap=0.12)
    sc["sum_t"] = T.say("gul", "Ten cookies! Let's share them!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ SMOOTHIE
    T.title("kitchen", "MAKE A SMOOTHIE!", "mishu", "Now let's make a cold, yummy smoothie!")
    sc = T.scene("smoothie", "kitchen")
    sc["ts"] = []
    for k, (key, text) in enumerate(SMOOTHIE):
        sc["ts"].append(T.mark("blend" if key == "blend" else "pop"))
        T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5 if key == "blend" else 0.3)
    sc["done_t"] = T.mark("tada")
    T.say("both", "Slurp! Yummy!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ SANDWICH
    T.title("kitchen", "BUILD A SANDWICH!", "mishu", "Let's build a sandwich! Count the layers!")
    sc = T.scene("sandwich", "kitchen")
    sc["ts"] = []
    for k, (key, text) in enumerate(SANDWICH):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if k % 2 == 0 else "mishu", f"{NUM[k + 1].capitalize()}! {text}", gap=0.3)
    sc["done_t"] = T.mark("tada")
    T.say("both", "Five layers! A yummy sandwich!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ RAINBOW FRUIT STICK
    T.title("kitchen", "RAINBOW FRUIT STICKS!", "gul", "Let's make a rainbow with fruit! What colour is it?")
    sc = T.scene("kebab", "kitchen")
    sc["ts"] = []
    for k, (key, col, text) in enumerate(KEBAB):
        a = "mishu" if k % 2 == 0 else "gul"
        T.prompt(a, "What colour?", wait=1.3)
        sc["ts"].append(T.mark("pop"))
        T.say(other(a), text, gap=0.3)
    sc["done_t"] = T.mark("tada")
    T.say("both", "A rainbow fruit stick! So healthy!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ FRUIT POPS
    T.title("kitchen", "FROZEN FRUIT POPS!", "gul", "It's hot outside! Let's make frozen fruit pops!")
    for k2, (key, text) in enumerate(POPS):
        sc = T.scene("pops", "kitchen", key=key, num=k2 + 1)
        T.mark("tada" if key == "done" else "pop")
        sc["say_t"] = T.say("mishu" if k2 % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ FULL EMPTY
    T.title("kitchen", "FULL OR EMPTY?", "mishu", "Chefs measure things! Is the cup full, or empty?")
    for k2, (kind2, text) in enumerate(FULLEMPTY):
        a = "gul" if k2 % 2 == 0 else "mishu"
        sc = T.scene("fullempty", "kitchen", lvl=kind2)
        T.prompt(a, "Full, or empty?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ TASTE WORDS
    T.title("kitchen", "TASTE WORDS!", "mishu", "How does it taste? Let's learn taste words!")
    for k, (key, w, text) in enumerate(TASTE):
        sc = T.scene("taste", "kitchen", key=key, w=w.upper())
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 1.0, 3)))
        T.pause(1.0)
        T.end(sc)
    # ------------------------------------------------------------ KITCHEN SOUNDS
    T.title("kitchen", "KITCHEN SOUNDS!", "gul", "Listen! What's that kitchen sound?")
    for k, (snd, key, ans) in enumerate(KSOUNDS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("ksound", "kitchen", key=key)
        T.pause(0.3)
        sc["snd_t"] = T.mark(snd)
        T.pause(1.6)
        T.prompt(a, "What is it?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ HEALTHY OR TREAT
    T.title("kitchen", "HEALTHY OR TREAT?", "mishu", "Is it a healthy food, or a treat?")
    for k, (key, good, q, ans) in enumerate(HEALTHY):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("healthy", "kitchen", key=key, good=good)
        T.prompt(a, f"{q} Healthy, or a treat?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ HOT OR COLD
    T.title("kitchen", "HOT OR COLD?", "gul", "Is it hot, or cold? You tell us!")
    for k, (key, hot, q) in enumerate(HOTCOLD):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("hotcold", "kitchen", key=key, hot=hot)
        T.prompt(a, f"{q} Hot, or cold?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), "Hot! Don't touch!" if hot else "Cold! Brrr!", gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ WHAT DO WE NEED
    T.title("kitchen", "WHAT DO WE NEED?", "mishu", "Silly chef game! Which one do we need?")
    for k, (q, keys, good, ans) in enumerate(NEED):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("need", "kitchen", keys=keys, good=good)
        T.prompt(a, q, wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ SET THE TABLE
    T.title("kitchen", "SET THE TABLE!", "gul", "Food is ready! Let's set the table!")
    sc = T.scene("table", "kitchen")
    sc["ts"] = []
    for k2, (key, text) in enumerate(TABLE):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu" if k2 % 2 == 0 else "gul", text, gap=0.3)
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ CLEAN UP
    T.title("kitchen", "CLEAN UP TIME!", "gul", "Good chefs always clean up!")
    for k, (text, key) in enumerate(CLEAN):
        sc = T.scene("clean", "kitchen", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("kitchen", "COOKING DANCE!", "mishu", "Stand up! Let's do the cooking dance!")
    T.dance("kitchen", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("kitchen", "CHEF QUIZ!", "gul", "Quick quiz time! Are you ready?")
    T.quiz("kitchen", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "kitchen")
    T.say("mishu", "Thank you for cooking with us, little chefs!", gap=0.2)
    sc["bye_t"] = T.say("both", "Yummy! Bye bye!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(20)


def sfx(kind):
    A = M.A
    if kind == "buzz":
        t2 = M.tt(0.4)
        return [(np.sign(np.sin(2 * np.pi * 140 * t2)) * 0.3 * np.minimum(1, (0.4 - t2) / 0.05), 0, 0.4)]
    if kind == "blend":
        t2 = M.tt(1.6)
        nz = np.diff(np.concatenate([[0], rng.standard_normal(len(t2))]))
        x = (0.5 * np.sign(np.sin(2 * np.pi * 95 * t2)) + nz) * np.minimum(1, t2 / 0.1) * np.minimum(1, (1.6 - t2) / 0.2)
        return [(x * 0.25, 0, 0.5)]
    if kind == "sizzle":
        t2 = M.tt(1.5)
        nz = np.diff(np.concatenate([[0], rng.standard_normal(len(t2))]))
        crack = (rng.random(len(t2)) < 0.002) * 3.0
        return [((nz * 0.3 + crack * nz) * np.minimum(1, t2 / 0.1) * np.minimum(1, (1.5 - t2) / 0.3), 0, 0.4)]
    if kind in ("chop", "crack"):
        out = []
        for i in range(4 if kind == "chop" else 1):
            t2 = M.tt(0.08)
            x = np.sin(2 * np.pi * 300 * t2) * np.exp(-t2 / 0.015) + np.diff(np.concatenate([[0], rng.standard_normal(len(t2))])) * np.exp(-t2 / 0.01)
            out.append((x * 0.7, i * 0.3, 0.6))
        return out
    if kind == "ovending":
        return [(A.sfx_ding(91), 0, 0.4), (A.sfx_ding(91), 0.05, 0.2)]
    return None


if __name__ == "__main__":
    T = build()
    tune = [72, 0, 76, 79, 81, 79, 76, 0, 77, 76, 74, 72, 74, 0, 72, 0]
    M.finish(T, music=dict(bpm=120, prog=[[60, 64, 67], [57, 60, 64], [65, 69, 72], [55, 59, 62]], hook=tune, start=1.4), sfx=sfx)
