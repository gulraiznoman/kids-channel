"""Long video 18: "Days of the Week". python make.py
Music: our own tune, code instruments."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven"]
WEEK = [  # bg, item, activity line, follow-up
    ("board", "book", "On Monday, we go to school! Hello, teacher!", "We learn letters and numbers!"),
    ("beach", "swimring", "On Tuesday, we go swimming! Splash, splash!", "Kick your legs! Swim like a fish!"),
    ("bedroom", "book", "On Wednesday, we read books at the library! Shh!", "So many stories to read!"),
    ("patch", "watering", "On Thursday, we help in the garden!", "Water the plants, so they grow big and tall!"),
    ("kitchen", "pizza", "On Friday, we have a pizza party! Yummy!", "Pizza with cheese and tomatoes!"),
    ("park", "ball", "On Saturday, we play at the park! Wheee!", "Swings, slides, and a big red ball!"),
    ("street", "house", "On Sunday, we visit Grandma! Hello, Grandma!", "Grandma gives the best hugs!")]
NEXT = [(["Monday", "Tuesday"], "Wednesday"), (["Thursday", "Friday"], "Saturday"), (["Saturday"], "Sunday"),
        (["Tuesday", "Wednesday"], "Thursday"), (["Sunday"], "Monday"), (["Wednesday", "Thursday"], "Friday"), (["Friday"], "Saturday")]
BEFORE = [("Tuesday", "Monday"), ("Saturday", "Friday"), ("Thursday", "Wednesday"), ("Monday", "Sunday")]
MISSING = [2, 5, 0, 4]
LETTERS = [(d, d[0], f"{d} starts with {d[0]}!") for d in DAYS]
FAV = [("gul", "My favourite day is Saturday! Park day!", "Saturday"), ("mishu", "My favourite day is Friday! Pizza day!", "Friday")]
CALENDAR = ["school", "swimming", "books", "garden", "pizza", "park", "Grandma"]
YTT = [("Wednesday", "Yesterday was Tuesday. Today is Wednesday. Tomorrow is Thursday!"),
       ("Friday", "Yesterday was Thursday. Today is Friday. Tomorrow is Saturday!"),
       ("Sunday", "Yesterday was Saturday. Today is Sunday. Tomorrow is Monday!")]
WEATHER = [("sunny", "On Monday, it was sunny! Hello, sun!"), ("rainy", "On Tuesday, it was rainy! Splish, splash!"),
           ("cloudy", "On Wednesday, it was cloudy! Big grey clouds!"), ("windy", "On Thursday, it was windy! Whoosh!"),
           ("snowy", "On Friday, it was snowy! Brrr!"), ("sunny", "On Saturday, it was sunny again!"), ("rainbow", "And on Sunday, a rainbow! Wow!")]
SLEEPS = [("Wednesday", "Saturday", ["Thursday", "Friday", "Saturday"]), ("Friday", "Monday", ["Saturday", "Sunday", "Monday"])]
MIXED = [3, 0, 5, 1, 6, 2, 4]
TIMES = [("morning", "In the morning, we wake up and eat breakfast!"), ("afternoon", "In the afternoon, we play and have lunch!"),
         ("night", "At night, we sleep! Good night! Every day has a morning, an afternoon, and a night!")]
RHYME = ["Monday, Tuesday, hello, hello!", "Wednesday, Thursday, here we go!", "Friday, Saturday, fun and play!", "Sunday is a family day!"]
DANCE = [("Monday, march!", "march"), ("Tuesday, twirl!", "spin"), ("Wednesday, wiggle!", "wiggle"),
         ("Thursday, stomp!", "stomp"), ("Friday, jump!", "jump"), ("Weekend, shake!", "shake")]
QUIZ = [("How many days are in a week?", "Seven!", "7"), ("What day comes after Monday?", "Tuesday!", "TUESDAY"),
        ("What day comes after Saturday?", "Sunday!", "SUNDAY"), ("Which two days are the weekend?", "Saturday and Sunday!", "WEEKEND")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING
    sc = T.scene("intro", "playroom")
    T.pause(0.3)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Days of the week!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "There are seven days in a week! Let's learn them all!", gap=0.2)
    T.say("gul", "Sing, play, and count with us! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ SEVEN DAYS
    T.title("playroom", "7 DAYS!", "gul", "Here are the seven days of the week!")
    sc = T.scene("seven", "playroom")
    sc["ts"] = []
    for i, d in enumerate(DAYS):
        sc["ts"].append(T.mark("pop"))
        T.say("gul" if i % 2 == 0 else "mishu", f"{d}!", gap=0.15)
    sc["sum_t"] = T.say("both", "Seven days! That's one week!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ CHANT x3
    T.title("playroom", "SAY THEM WITH US!", "mishu", "Now say them with us! Slow, then fast, then super fast!")
    for rnd, (gap, lab) in enumerate(((0.35, "SLOW"), (0.12, "FAST"), (0.0, "SUPER FAST!"))):
        sc = T.scene("chant", "playroom", label=lab)
        if rnd:
            T.say("mishu" if rnd == 1 else "gul", "Faster!" if rnd == 1 else "Super fast!", gap=0.1)
        sc["ts"] = [T.say("both", d, gap=gap) for d in DAYS]
        sc["end_t"] = T.mark("yes")
        T.pause(0.5)
        T.end(sc)
    # ------------------------------------------------------------ OUR WEEK STORY
    T.title("playroom", "OUR BUSY WEEK!", "gul", "What do Gul and Mishu do every day? Let's see!")
    for i, (bg, key, line_, more) in enumerate(WEEK):
        a = "mishu" if i % 2 == 0 else "gul"
        sc = T.scene("week", bg, day=i, key=key, chapter=None)
        T.mark("riser")
        sc["day_t"] = T.say("both", f"It's {DAYS[i]}!", gap=0.15)
        sc["act_t"] = T.say(a, line_, gap=0.15)
        T.say(other(a), more, gap=0.1)
        T.prompt(a, f"Say it! {DAYS[i]}!", wait=1.3)
        T.end(sc)
    # ------------------------------------------------------------ FIRST LETTERS
    T.title("playroom", "FIRST LETTERS!", "mishu", "Every day starts with a big letter! Look!")
    for i, (d, L, text) in enumerate(LETTERS):
        sc = T.scene("letter", "playroom", day=i, L=L)
        T.mark("pop")
        sc["say_t"] = T.say("gul" if i % 2 == 0 else "mishu", text, gap=0.4)
        T.end(sc)
    sc = T.scene("twins", "playroom")
    sc["say_t"] = T.say("gul", "Look! Tuesday and Thursday both start with T!", gap=0.2)
    sc["say2_t"] = T.say("mishu", "And Saturday and Sunday both start with S!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ COUNT ON FINGERS
    T.title("playroom", "COUNT THE DAYS!", "gul", "Let's count the days on our fingers!")
    sc = T.scene("fingers", "playroom")
    sc["ts"] = []
    for i, d in enumerate(DAYS):
        sc["ts"].append(T.mark("pop"))
        T.say("both", f"{NUM[i + 1].capitalize()}, {d}!", gap=0.15)
    sc["sum_t"] = T.say("mishu", "Seven fingers! Seven days!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ WHAT COMES NEXT
    T.title("playroom", "WHAT COMES NEXT?", "mishu", "What day comes next? Think hard!")
    for k, (seq, ans) in enumerate(NEXT):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("next", "playroom", seq=seq, ans=ans)
        T.say(a, ", ".join(seq) + "...", gap=0.1)
        T.prompt(a, "What comes next?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{ans}!", gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WHAT COMES BEFORE
    T.title("playroom", "WHAT COMES BEFORE?", "gul", "Big kids! What day comes before?")
    for k, (d, ans) in enumerate(BEFORE):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("before", "playroom", day=d, ans=ans)
        T.prompt(a, f"What day comes before {d}?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), f"{ans}! {ans}, then {d}!", gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MISSING DAY
    T.title("playroom", "WHICH DAY IS MISSING?", "mishu", "Oh no! A day is missing from the train! Which one?")
    for k, miss in enumerate(MISSING):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("missing", "playroom", miss=miss)
        sc["go_t"] = T.mark("whoosh")
        T.prompt(a, "Which day is missing?", wait=2.4)
        sc["answer_t"] = T.mark("tada")
        T.say(other(a), f"{DAYS[miss]}! Welcome back, {DAYS[miss]}!", gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ MIXED UP
    T.title("playroom", "MIXED UP DAYS!", "gul", "Oops! The days are all mixed up! Let's put them in order!")
    sc = T.scene("mixed", "playroom")
    sc["ts"] = []
    for i, d in enumerate(DAYS):
        sc["ts"].append(T.mark("whoosh"))
        T.say("mishu" if i % 2 == 0 else "gul", f"{d}, you go {['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh'][i]}!", gap=0.15)
    sc["done_t"] = T.mark("tada")
    T.say("both", "All in order! Hooray!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ WEEKDAYS AND WEEKEND
    T.title("park", "WEEKDAYS & WEEKEND!", "gul", "Some days are weekdays, and some days are the weekend!")
    sc = T.scene("weekend", "park")
    sc["wd_t"] = T.say("mishu", "Monday, Tuesday, Wednesday, Thursday, Friday. Five weekdays! School days!", gap=0.3)
    sc["ts"] = []
    sc["we_t"] = T.say("gul", "Saturday and Sunday. Two days for the weekend! Family days!", gap=0.3)
    sc["sum_t"] = T.say("both", "Five weekdays, plus two weekend days, makes seven!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    for k, d in enumerate(["Saturday", "Tuesday", "Sunday", "Friday"]):
        a = "mishu" if k % 2 == 0 else "gul"
        we = d in ("Saturday", "Sunday")
        sc = T.scene("sort", "park", day=DAYS.index(d), we=we)
        T.prompt(a, f"{d}! Weekday, or weekend?", wait=1.8)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), "Weekend!" if we else "Weekday!", gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WEATHER WEEK
    T.title("park", "WEATHER WEEK!", "mishu", "Every day the weather can change! What's the weather?")
    for k, (w, text) in enumerate(WEATHER):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("weather", "park", day=k, w=w)
        T.prompt(a, f"{DAYS[k]}! What's the weather?", wait=1.5)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), text, gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ YESTERDAY TODAY TOMORROW
    T.title("playroom", "YESTERDAY, TODAY, TOMORROW!", "mishu", "Yesterday was before. Today is now. Tomorrow comes next!")
    for k, (d, text) in enumerate(YTT):
        sc = T.scene("ytt", "playroom", day=DAYS.index(d))
        T.mark("pop")
        parts = text.split(". ")
        sc["ts"] = [T.say("gul" if (k + j) % 2 == 0 else "mishu", p.rstrip(".!") + "!", gap=0.25) for j, p in enumerate(parts)]
        T.pause(0.3)
        T.end(sc)
    # ------------------------------------------------------------ HOW MANY SLEEPS
    T.title("playroom", "HOW MANY SLEEPS?", "gul", "How many sleeps until the fun day? Let's count!")
    for k, (today, goal, path) in enumerate(SLEEPS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("sleeps", "playroom", today=DAYS.index(today), path=[DAYS.index(p) for p in path])
        T.say(a, f"Today is {today}. How many sleeps until {goal}?", gap=0.2)
        sc["ts"] = []
        for i, p in enumerate(path):
            sc["ts"].append(T.mark("pop"))
            T.say("both", f"{NUM[i + 1].capitalize()}, {p}!", gap=0.15)
        sc["sum_t"] = T.say(other(a), f"Three sleeps until {goal}!", gap=0.5)
        T.stars.append(sc["sum_t"])
        T.end(sc)
    # ------------------------------------------------------------ MORNING AFTERNOON NIGHT
    T.title("bedroom", "MORNING, AFTERNOON, NIGHT!", "mishu", "Every day has three parts! Let's see!")
    for k, (part, text) in enumerate(TIMES):
        sc = T.scene("times", "bedroom", part=part)
        T.mark("sparkle")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ CALENDAR STICKERS
    T.title("playroom", "MY CALENDAR!", "gul", "Let's put a sticker on the calendar for every day!")
    sc = T.scene("calendar", "playroom")
    sc["ts"] = []
    for i, d in enumerate(DAYS):
        sc["ts"].append(T.mark("pop"))
        T.say("mishu" if i % 2 == 0 else "gul", f"{d}, {CALENDAR[i]}!", gap=0.15)
    sc["done_t"] = T.mark("tada")
    T.say("both", "A whole week of fun!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ FAVOURITE DAY
    for who, text, d in FAV:
        sc = T.scene("fav", "playroom", who=who, day=DAYS.index(d))
        T.mark("sparkle")
        sc["say_t"] = T.say(who, text, gap=0.3)
        T.end(sc)
    sc = T.scene("fav", "playroom", who="both", day=-1)
    T.prompt("both", "What's your favourite day?", wait=2.2)
    T.end(sc)
    # ------------------------------------------------------------ RHYME
    T.title("playroom", "DAYS RHYME!", "mishu", "Clap along with our days rhyme!")
    sc = T.scene("rhyme", "playroom")
    sc["l"] = [T.say("both", ln, gap=0.25) for ln in RHYME * 2]
    T.pause(0.3)
    T.end(sc)
    # ------------------------------------------------------------ DAYS TRAIN
    T.title("playroom", "DAYS TRAIN!", "gul", "All aboard the days of the week train! Choo choo!")
    sc = T.scene("train", "playroom")
    sc["ts"] = [T.say("both", d + "!", gap=0.15) for d in DAYS]
    T.say("mishu", "Then back to Monday again! Choo choo!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("playroom", "DAYS DANCE!", "mishu", "Stand up! Let's do the days of the week dance!")
    T.dance("playroom", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("playroom", "DAYS QUIZ!", "gul", "Quick quiz time! Are you ready?")
    T.quiz("playroom", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "playroom")
    T.say("mishu", "Now you know the seven days of the week!", gap=0.2)
    sc["bye_t"] = T.say("both", "See you next week! Bye bye!", gap=1.8)
    T.end(sc)
    return T


def sfx(kind):
    if kind == "choo":
        return [(M.A.sfx_whoosh(), 0, 0.3)]
    return None


if __name__ == "__main__":
    T = build()
    tune = [72, 74, 76, 77, 79, 0, 79, 0, 81, 79, 77, 76, 74, 0, 72, 0]
    M.finish(T, music=dict(bpm=122, prog=[[60, 64, 67], [65, 69, 72], [57, 60, 64], [55, 59, 62]], hook=tune, start=1.4), sfx=sfx)
