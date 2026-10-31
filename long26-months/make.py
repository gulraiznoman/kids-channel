"""Long video 26: "Months of the Year & New Year". python make.py
Music: our own tune, code instruments."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ORD = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth"]
YEAR = [  # background, item, line, follow-up, word
    ("northpole", "snowflake", "January is cold! The year begins, and snow may fall!", "Wear your warm hat!", "COLD!"),
    ("northpole", "heart", "February is the shortest month!", "It has only twenty eight days!", "SHORTEST!"),
    ("park", "blossom", "In March, the flowers start to grow!", "Spring is coming!", "FLOWERS!"),
    ("patch", "rainy", "April brings the rain! Splish, splash!", "Rain helps the plants grow!", "RAIN!"),
    ("park", "kite", "May is warm and windy! Let's fly a kite!", "Up, up, up it goes!", "KITE!"),
    ("beach", "sunny", "June is hot! The sun shines all day!", "Summer is here!", "SUNNY!"),
    ("beach", "icecream2", "July is very hot! Let's eat ice cream!", "Yummy and cold!", "ICE CREAM!"),
    ("beach", "watermelon", "August is for juicy watermelon!", "Sweet, and so yummy!", "WATERMELON!"),
    ("board", "schoolbag", "In September, we go back to school!", "Hello, teacher!", "SCHOOL!"),
    ("tree", "autumnleaf", "In October, the leaves turn orange and fall!", "Crunch, crunch, crunch!", "LEAVES!"),
    ("tree", "scarf", "November gets chilly! Wear a warm scarf!", "Brrr! Winter is coming!", "CHILLY!"),
    ("xmasroom", "snowman", "December is the last month! Let's build a snowman!", "The year is ending!", "LAST MONTH!")]
SEASONS = [("spring", "blossom", "Spring! Flowers grow, and baby animals are born!"), ("summer", "sunny", "Summer! It's hot and sunny!"),
           ("autumn", "autumnleaf", "Autumn! Leaves fall from the trees!"), ("winter", "snowman", "Winter! It's cold and frosty!")]
SEASORT = [("snowman", "winter", "A snowman?", "Winter!"), ("watermelon", "summer", "Watermelon?", "Summer!"), ("autumnleaf", "autumn", "Falling leaves?", "Autumn!"),
           ("blossom", "spring", "New flowers?", "Spring!")]
NEXT = [("January", "February"), ("March", "April"), ("June", "July"), ("October", "November"), ("December", "January")]
BEFORE = [("February", "January"), ("May", "April"), ("December", "November"), ("August", "July")]
MISSING = [2, 6, 10]
LETTERS = [("J", ["January", "June", "July"], "Three months start with J!"), ("M", ["March", "May"], "Two months start with M!"), ("A", ["April", "August"], "Two months start with A!")]
HOW = [("A day is one sleep!", "day"), ("A week is seven days!", "week"), ("A month is about four weeks!", "month"), ("And a year is twelve months!", "year")]
BDAY = [("gul", "My birthday is in March!", 2), ("mishu", "My birthday is in August!", 7)]
NEWYEAR = [("party", "It's the last night of the year! Happy New Year's Eve!"), ("clock12", "At twelve o'clock, the new year begins!")]
WISHES = [("Be kind to everyone!", "BE KIND!", "heart"), ("Help at home!", "HELP!", "watering"), ("Read more books!", "READ!", "book"), ("Try new things!", "TRY!", "star")]
RHYME = ["January, February, snow and ice!", "March and April, rain is nice!", "May, June, July, sunny fun!", "August, shining summer sun!",
         "September, school, October leaves!", "November wind blows through the trees!", "December ends the year so bright!", "Happy New Year, day and night!"]
WEAR = [("January", ["scarf", "sunhat"], "scarf", "A warm scarf! It's cold!"), ("April", ["raincoat", "sunglasses"], "raincoat", "A raincoat! It's rainy!"),
        ("July", ["sunhat", "scarf"], "sunhat", "A sun hat! It's hot!"), ("December", ["sunglasses", "boots"], "boots", "Warm boots! It's snowy!")]
WHICHM = [("Which month do we go back to school?", [0, 8, 5], 8, "September!"), ("Which month is the first month?", [11, 0, 6], 0, "January!"),
          ("Which month is cold, with a snowman?", [11, 6, 7], 11, "December!"), ("Which month has falling leaves?", [2, 9, 5], 9, "October!")]
DANCE = [("January, jump!", "jump"), ("March, march, march!", "march"), ("May, sway, sway!", "sway"), ("July, shake it high!", "shake"),
         ("October, spin like a leaf!", "spin"), ("Happy New Year! Hooray!", "jump")]
QUIZ = [("How many months are in a year?", "Twelve!", "12"), ("Which month comes first?", "January!", "JANUARY"),
        ("Which month is the shortest?", "February!", "FEBRUARY"), ("Which month is the last one?", "December!", "DECEMBER")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: fireworks over the city
    sc = T.scene("intro", "city")
    sc["boom_t"] = T.mark("boom")
    T.pause(1.2)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Happy New Year!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "A new year has twelve months! Let's learn them all!", gap=0.2)
    T.say("gul", "From January to December! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ TWELVE MONTHS
    T.title("playroom", "12 MONTHS!", "gul", "Here are the twelve months of the year!")
    sc = T.scene("twelve", "playroom")
    sc["ts"] = []
    for i, m in enumerate(MONTHS):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if i % 2 == 0 else "mishu", f"{m}!", gap=0.15)
    sc["sum_t"] = T.say("both", "Twelve months! That's one year!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ CHANT x3
    T.title("playroom", "SAY THEM WITH US!", "mishu", "Say them with us! Slow, then fast, then super fast!")
    for rnd, (gap, lab) in enumerate(((0.3, "SLOW"), (0.1, "FAST"), (0.0, "SUPER FAST!"))):
        sc = T.scene("chant", "playroom", label=lab)
        if rnd:
            T.say("mishu" if rnd == 1 else "gul", "Faster!" if rnd == 1 else "Super fast!", gap=0.1)
        sc["ts"] = [T.say("both", m, gap=gap) for m in MONTHS]
        sc["end_t"] = T.mark("yes")
        T.pause(0.5)
        T.end(sc)
    # ------------------------------------------------------------ A YEAR STORY
    T.title("playroom", "OUR YEAR!", "gul", "What happens in each month? Let's see!")
    for k, (bg, key, line_, more, w) in enumerate(YEAR):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("month", bg, m=k, key=key, w=w)
        T.mark("riser")
        sc["day_t"] = T.say("both", f"{MONTHS[k]}!", gap=0.1)
        sc["act_t"] = T.say(a, line_, gap=0.1)
        T.say(other(a), more, gap=0.1)
        T.prompt(a, f"Say it! {MONTHS[k]}!", wait=1.2)
        T.end(sc)
    # ------------------------------------------------------------ FIRST TO TWELFTH
    T.title("playroom", "FIRST TO TWELFTH!", "mishu", "Every month has a place in the year!")
    sc = T.scene("ordinal", "playroom")
    sc["ts"] = []
    for i, m in enumerate(MONTHS):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if i % 2 == 0 else "mishu", f"{m} is {ORD[i]}!", gap=0.15)
    T.pause(0.4)
    T.end(sc)
    # ------------------------------------------------------------ FOUR SEASONS
    T.title("park", "FOUR SEASONS!", "mishu", "A year also has four seasons!")
    for k, (name, key, text) in enumerate(SEASONS):
        sc = T.scene("season", "park", name=name, key=key)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    for k, (key, name, q, ans) in enumerate(SEASORT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("seasort", "park", key=key, name=name)
        T.prompt(a, f"{q} Which season?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WHAT DO WE WEAR
    T.title("playroom", "WHAT DO WE WEAR?", "gul", "The weather changes every month! What do we wear?")
    for k, (m, keys, good, ans) in enumerate(WEAR):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("wear", "playroom", m=MONTHS.index(m), keys=keys, good=good)
        T.prompt(a, f"It's {m}! What do we wear?", wait=1.9)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WHICH MONTH
    T.title("playroom", "WHICH MONTH?", "mishu", "Do you remember? Which month is it?")
    for k, (q, ms, good, ans) in enumerate(WHICHM):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("whichm", "playroom", q=q.upper(), ms=ms, good=good)
        T.prompt(a, q, wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WHAT COMES NEXT
    T.title("playroom", "WHAT COMES NEXT?", "gul", "What month comes next? Think hard!")
    for k, (m, ans) in enumerate(NEXT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("seq", "playroom", m=MONTHS.index(m), ans=MONTHS.index(ans), first=False)
        T.prompt(a, f"What comes after {m}?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{ans}!", gap=0.5)
        T.end(sc)
    T.title("playroom", "WHAT COMES BEFORE?", "mishu", "Big kids! Which month comes before?")
    for k, (m, ans) in enumerate(BEFORE):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("seq", "playroom", m=MONTHS.index(m), ans=MONTHS.index(ans), first=True)
        T.prompt(a, f"What comes before {m}?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{ans}! Then {m}!", gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MISSING MONTH
    T.title("playroom", "WHICH MONTH IS MISSING?", "gul", "Oh no! A month is missing!")
    for k, miss in enumerate(MISSING):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("missing", "playroom", miss=miss)
        T.prompt(a, "Which month is missing?", wait=2.4)
        sc["answer_t"] = T.mark("tada")
        T.say(other(a), f"{MONTHS[miss]}!", gap=0.6)
        T.end(sc)
    # ------------------------------------------------------------ FIRST LETTERS
    T.title("playroom", "FIRST LETTERS!", "mishu", "Some months start with the same letter!")
    for k, (L, ms, text) in enumerate(LETTERS):
        sc = T.scene("letters", "playroom", L=L, ms=[MONTHS.index(m) for m in ms])
        T.mark("pop")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.2)
        sc["ts"] = [T.say("both", m, gap=0.2) for m in ms]
        T.pause(0.4)
        T.end(sc)
    # ------------------------------------------------------------ DAY WEEK MONTH YEAR
    T.title("playroom", "HOW LONG IS A YEAR?", "gul", "Days, weeks, months, and a year!")
    for k, (text, key) in enumerate(HOW):
        sc = T.scene("how", "playroom", key=key, k=k)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ BIRTHDAY MONTH
    T.title("playroom", "MY BIRTHDAY MONTH!", "mishu", "Everyone has a birthday month!")
    for who, text, m in BDAY:
        sc = T.scene("bday", "playroom", who=who, m=m)
        T.mark("sparkle")
        sc["say_t"] = T.say(who, text, gap=0.4)
        T.end(sc)
    sc = T.scene("bday", "playroom", who="both", m=-1)
    T.prompt("both", "What month is your birthday?", wait=2.2)
    T.end(sc)
    # ------------------------------------------------------------ RHYME
    T.title("playroom", "MONTHS RHYME!", "gul", "Clap along with our months rhyme!")
    sc = T.scene("rhyme", "playroom")
    sc["l"] = [T.say("both", ln, gap=0.25) for ln in RHYME * 2]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ NEW YEAR'S EVE
    T.title("city", "NEW YEAR'S EVE!", "mishu", "After December, a new year begins!")
    for k, (key, text) in enumerate(NEWYEAR):
        sc = T.scene("eve", "city", key=key)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    sc = T.scene("countdown", "city")
    T.say("mishu", "Let's count down together!", gap=0.1)
    sc["ts"] = []
    for w in ("Ten!", "Nine!", "Eight!", "Seven!", "Six!", "Five!", "Four!", "Three!", "Two!", "One!"):
        sc["ts"].append(T.mark("ding"))
        T.say("both", w, gap=0.14)
    sc["go_t"] = T.mark("boom")
    T.say("both", "Happy New Year!", gap=1.2)
    T.end(sc)
    # ------------------------------------------------------------ WISHES
    T.title("playroom", "NEW YEAR PROMISES!", "gul", "In the new year, we can try to be even better!")
    for k, (text, w, key) in enumerate(WISHES):
        sc = T.scene("wish", "playroom", w=w, key=key)
        T.mark("sparkle")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("playroom", "MONTHS DANCE!", "mishu", "Stand up! Let's do the months dance!")
    T.dance("playroom", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("playroom", "MONTHS QUIZ!", "gul", "Quick quiz time! Are you ready?")
    T.quiz("playroom", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "city")
    T.say("mishu", "Now you know all twelve months!", gap=0.2)
    sc["bye_t"] = T.say("both", "Happy New Year, friends! Bye bye!", gap=1.8)
    T.end(sc)
    return T


rng = np.random.default_rng(26)


def sfx(kind):
    A = M.A
    if kind == "boom":
        out = []
        for i in range(3):
            t = M.tt(0.7)
            n = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
            out.append((np.convolve(n, np.ones(25) / 25, mode="same") * 7 * np.exp(-t / 0.2), i * 0.35, 0.5))
            out.append((A.sfx_sparkle(), i * 0.35 + 0.1, 0.25))
        return out
    return None


if __name__ == "__main__":
    T = build()
    tune = [72, 72, 76, 79, 77, 74, 72, 0, 74, 74, 77, 81, 79, 76, 74, 0]
    M.finish(T, music=dict(bpm=122, prog=[[60, 64, 67], [65, 69, 72], [57, 60, 64], [55, 59, 62]], hook=tune, start=2.0), sfx=sfx)
