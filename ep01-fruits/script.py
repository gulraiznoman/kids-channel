"""Episode 1: Learn Fruits with Gul & Mishu.

The script is data: a list of beats. Each beat has a speaker line (or a pause) and
optional on-screen events. voices.py turns lines into audio; render.py animates them.
"""

VOICES = {
    # edge/azure settings only; published voices come from voices/kidvoice.py (Kokoro + Praat)
    "gul": dict(voice="en-US-AnaNeural", pitch="-40Hz", rate="+0%"),
    "mishu": dict(voice="en-US-AnaNeural", pitch="+12Hz", rate="-4%"),
}

FRUITS = [
    # key, name, colour words, fun line (speaker, text)
    ("apple", "Apple", "a red, shiny apple", ("mishu", "Crunch, crunch!")),
    ("banana", "Banana", "a long, yellow banana", ("gul", "Monkeys love bananas!")),
    ("orange", "Orange", "a round orange. It's orange too!", ("mishu", "So juicy!")),
    ("lemon", "Lemon", "a yellow lemon. It's sour!", ("gul", "Ooh! Sour face!")),
    ("grapes", "Grapes", "purple grapes. So many!", ("gul", "Let's count them! One, two, three!")),
    ("strawberry", "Strawberry", "a red strawberry with tiny seeds", ("mishu", "Sweet and yummy!")),
    ("watermelon", "Watermelon", "a big watermelon. Green outside, red inside!", ("gul", "It's so big!")),
    ("mango", "Mango", "a mango! The king of fruits!", ("mishu", "My favourite!")),
    ("pineapple", "Pineapple", "a pineapple. It has a spiky crown!", ("gul", "Like a king!")),
    ("cherry", "Cherries", "two little red cherries", ("mishu", "They're twins!")),
    ("kiwi", "Kiwi", "a kiwi. Brown outside, green inside!", ("mishu", "It's fuzzy!")),
    ("pear", "Pear", "a green pear", ("gul", "Yum, yum, yum!")),
]

QUESTIONS = [("mishu", "Gul, look! What's this?"), ("gul", "Mishu, what's this one?"),
             ("mishu", "Ooh! What fruit is this?"), ("gul", "Look, Mishu! What is it?")]
PRAISE = ["Great job!", "Yay! Well done!", "Awesome!", "Super!", "Good job, friends!"]


def beats():
    B = []
    B.append(dict(who="gul", text="Hi friends! I'm Gul!", wave="gul", scene="intro"))
    B.append(dict(who="mishu", text="And I'm Mishu! Today, we're going to learn fruits!", wave="mishu"))
    B.append(dict(who="gul", text="Yummy! Let's go!", eyes_closed="gul"))
    for i, (key, name, desc, fun) in enumerate(FRUITS):
        q_who, q = QUESTIONS[i % len(QUESTIONS)]
        a_who = "mishu" if q_who == "gul" else "gul"
        B.append(dict(pause=0.9, fruit_in=key))
        B.append(dict(who=q_who, text=q))
        B.append(dict(who=a_who, text=f"It's {desc}", label=name))
        B.append(dict(who=q_who, text=f"{name}! Can you say {name.lower()}?", spell=name))
        B.append(dict(pause=3.0, prompt=True))
        B.append(dict(who=a_who, text=PRAISE[i % len(PRAISE)], eyes_closed=a_who, stars=True))
        B.append(dict(who=fun[0], text=fun[1]))
        B.append(dict(pause=0.6, fruit_out=key))
    B.append(dict(pause=0.6, recap=True))
    B.append(dict(who="mishu", text="We learned twelve fruits today!"))
    names = [f[1].lower() for f in FRUITS]
    B.append(dict(who="gul", text=", ".join(names[:-1]) + ", and " + names[-1] + "!", recap_walk=True))
    B.append(dict(who="mishu", text="Which fruit is your favourite? Mine is mango!"))
    B.append(dict(who="gul", text="Eat your fruits and grow big and strong!", eyes_closed="gul"))
    B.append(dict(who="mishu", text="Bye bye, friends!", wave="mishu", scene="outro"))
    B.append(dict(who="gul", text="See you next time!", wave="gul"))
    B.append(dict(pause=2.5, end=True))
    return B
