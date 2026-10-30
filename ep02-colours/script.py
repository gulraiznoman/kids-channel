"""Episode 2: Learn Colours with Gul & Mishu.

Same beat structure as episode 1. Each colour is shown as a big balloon with a familiar
object of the same colour; the label is written in the colour itself.
"""

TOPIC = "Learn Colours!"
NOUN = "COLOUR"                    # Shorts hook: "GUESS THE COLOUR!"
OUTFITS = {"gul": "bluetee", "misheal": "pink"}

VOICES = {
    # edge/azure settings only; published voices come from voices/kidvoice.py (Kokoro + Praat)
    "gul": dict(voice="en-US-AnaNeural", pitch="-40Hz", rate="+0%"),
    "mishu": dict(voice="en-US-AnaNeural", pitch="+12Hz", rate="-4%"),
}

# key, name, label colour, answer line, fun line (speaker, text)
COLOURS = [
    ("red", "Red", (232, 53, 46), "Red! Red, like an apple!", ("mishu", "Red is so bright!")),
    ("orange", "Orange", (255, 148, 32), "Orange! Orange, like an orange!", ("gul", "Orange, orange! That's funny!")),
    ("yellow", "Yellow", (255, 214, 10), "Yellow! Yellow, like a banana!", ("mishu", "Yellow like the sun!")),
    ("green", "Green", (60, 190, 80), "Green! Green, like a leaf!", ("gul", "Green like the grass!")),
    ("blue", "Blue", (46, 140, 255), "Blue! Blue, like a little fish!", ("mishu", "Blue like the sky!")),
    ("purple", "Purple", (142, 68, 201), "Purple! Purple, like grapes!", ("gul", "Purple is so pretty!")),
    ("pink", "Pink", (255, 110, 170), "Pink! Pink, like a flower!", ("mishu", "Pink like my dress!")),
    ("brown", "Brown", (139, 90, 43), "Brown! Brown, like a teddy bear!", ("gul", "A big brown hug!")),
    ("grey", "Grey", (150, 150, 160), "Grey! Grey, like an elephant!", ("gul", "A big grey elephant!")),
    ("black", "Black", (40, 36, 40), "Black! Black, like a kitty cat!", ("mishu", "Meow, meow!")),
    ("white", "White", (255, 255, 255), "White! White, like a fluffy cloud!", ("gul", "Soft and fluffy!")),
]
QUESTIONS = [("mishu", "Gul, look! A balloon! What colour is it?"), ("gul", "Mishu, what colour is this balloon?"),
             ("mishu", "Ooh! What colour is this one?"), ("gul", "Look, Mishu! What colour is it?")]
PRAISE = ["Great job!", "Yay! Well done!", "Awesome!", "Super!", "Good job, friends!"]

# compatibility with the shared engine (render/shorts read FRUITS-style tuples)
FRUITS = [(k, n, a, f) for k, n, _, a, f in COLOURS]
LABEL_COLOURS = {n: c for _, n, c, _, _ in COLOURS}


def beats():
    B = []
    B.append(dict(who="gul", text="Hi friends! I'm Gul!", wave="gul", scene="intro"))
    B.append(dict(who="mishu", text="And I'm Mishu! Today, we're going to learn colours!", wave="mishu"))
    B.append(dict(who="gul", text="Colours are everywhere! Let's go!", eyes_closed="gul"))
    for i, (key, name, col, answer, fun) in enumerate(COLOURS):
        q_who, q = QUESTIONS[i % len(QUESTIONS)]
        a_who = "mishu" if q_who == "gul" else "gul"
        B.append(dict(pause=0.9, fruit_in=key))
        B.append(dict(who=q_who, text=q))
        B.append(dict(who=a_who, text=answer, label=name))
        B.append(dict(who=q_who, text=f"{name}! Can you say {name.lower()}?", spell=name))
        B.append(dict(pause=3.0, prompt=True))
        B.append(dict(who=a_who, text=PRAISE[i % len(PRAISE)], eyes_closed=a_who, stars=True))
        B.append(dict(who=fun[0], text=fun[1]))
        B.append(dict(pause=0.6, fruit_out=key))
    B.append(dict(pause=0.6, recap=True))
    B.append(dict(who="mishu", text="We learned eleven colours today!"))
    names = [c[1].lower() for c in COLOURS]
    B.append(dict(who="gul", text=", ".join(names[:-1]) + ", and " + names[-1] + "!", recap_walk=True))
    B.append(dict(who="mishu", text="What colour are you wearing today? I'm wearing pink!"))
    B.append(dict(who="gul", text="And I'm wearing blue! Look for colours all around you!", eyes_closed="gul"))
    B.append(dict(who="mishu", text="Bye bye, friends!", wave="mishu", scene="outro"))
    B.append(dict(who="gul", text="See you next time!", wave="gul"))
    B.append(dict(pause=2.5, end=True))
    return B
