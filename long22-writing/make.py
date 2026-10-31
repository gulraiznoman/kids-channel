"""Long video 22: "Learn to Write ABC". python make.py
Music: our own tune, code instruments."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
LETTERS = [  # letter, how to write it, word, picture key
    ("A", "Slant down. Slant down. Line across!", "apple", "apple"), ("B", "Line down. Bump, bump!", "ball", "ball"),
    ("C", "One big curve!", "cat", "cat"), ("D", "Line down. One big bump!", "dog", "dog"),
    ("E", "Line down. Three lines across!", "elephant", "elephant"), ("F", "Line down. Two lines across!", "fish", "fish"),
    ("G", "Big curve, up, and in!", "grapes", "grapes"), ("H", "Line down. Line down. Line across!", "hat", "hat"),
    ("I", "Line down. Top line. Bottom line!", "ice cream", "ice cream"), ("J", "Line down, and hook!", "jellyfish", "jellyfish"),
    ("K", "Line down. Slant in. Slant out!", "kite", "kite"), ("L", "Line down. Line across!", "lion", "lion"),
    ("M", "Down. Slant down. Slant up. Down!", "monkey", "monkey"), ("N", "Line down. Slant down. Line up!", "nest", "nest"),
    ("O", "Round and round! A circle!", "octopus", "octopus"), ("P", "Line down. One bump at the top!", "pizza", "pizza"),
    ("Q", "A circle, and a little tail!", "queen", "queen"), ("R", "Line down. Bump. Slant out!", "rainbow", "rainbow"),
    ("S", "Curve around, and curve back!", "sun", "sun"), ("T", "Line down. Line across the top!", "train", "train"),
    ("U", "Down, around, and up!", "umbrella", "umbrella"), ("V", "Slant down. Slant up!", "violin", "violin"),
    ("W", "Slant down, up, down, up!", "whale", "whale"), ("X", "Slant, and slant across!", "xylophone", "xylophone"),
    ("Y", "Slant in. Slant in. Line down!", "yo-yo", "yo-yo"), ("Z", "Across. Slant down. Across!", "zebra", "zebra")]
WARM = [("down", "Lines going down! Top to bottom!"), ("across", "Lines going across! Left to right!"), ("slant", "Slanting lines! Like a slide!"),
        ("zigzag", "Zig zag, zig zag! Like mountains!"), ("wave", "Wavy lines! Like the sea!"), ("circle", "Round and round! Big circles!")]
PENCIL = [("pencil", "Pick up your pencil!"), ("grip", "Hold it with your thumb and two fingers!"), ("paper", "Put your paper flat on the table!"),
          ("sit", "Sit up nice and tall!")]
LOWER = [("a", "Small a! Round, and a line down!"), ("b", "Small b! Line down, and a tummy!"), ("c", "Small c! A little curve!"),
         ("d", "Small d! Round, and a tall line!"), ("e", "Small e! Across, and curve around!"), ("o", "Small o! A little circle!"),
         ("i", "Small i! Line down, and a dot!"), ("t", "Small t! Line down, and a little cross!"), ("n", "Small n! Line down, and a hump!"),
         ("u", "Small u! Down, around, up, and down!")]
NUMS = [("1", "Number one! One line down!"), ("2", "Number two! Curve around, and across!"), ("3", "Number three! Bump, bump!"),
        ("4", "Number four! Slant, across, and down!"), ("5", "Number five! Down, big bump, and a hat on top!")]
TOOLS = [("crayon", "You can write with a crayon!"), ("chalk", "You can write with chalk, on a board!"), ("sand", "You can even write with your finger, in the sand!")]
WORDS = [("CAT", "cat", "C, A, T! Cat!"), ("SUN", "sun", "S, U, N! Sun!"), ("DOG", "dog", "D, O, G! Dog!"), ("HAT", "hat", "H, A, T! Hat!"), ("FISH", "fish", "F, I, S, H! Fish!"), ("BALL", "ball", "B, A, L, L! Ball!")]
NAMES = [("GUL", "gul", "G, U, L! That's my name! Gul!"), ("MISHU", "misheal", "M, I, S, H, U! That's my name! Mishu!")]
SORT = [("L", True), ("O", False), ("T", True), ("S", False), ("E", True), ("C", False), ("H", True), ("U", False)]
RIGHT = [("B", 0), ("S", 1), ("E", 0), ("N", 1)]
MISSING = [(list("ABCD"), 2), (list("KLMN"), 1), (list("PQRS"), 3), (list("WXYZ"), 0)]
DANCE = [("Write a big A in the air!", "reach"), ("Draw a circle! Round and round!", "spin"), ("Zig zag, zig zag!", "wiggle"),
         ("Stand tall, like letter I!", "stretch"), ("Jump like letter J!", "jump"), ("Well done, writers!", "jump")]
QUIZ = [("Lines go down, from top to...?", "Bottom!", "pencil"), ("Which letter is a circle?", "O!", "O"),
        ("Which letter is for apple?", "A!", "A"), ("How do we hold a pencil?", "Thumb and two fingers!", "pencil")]


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING: pencil writes ABC by itself
    sc = T.scene("intro", "studio")
    sc["write_t"] = T.mark("scribble")
    T.pause(1.6)
    sc["title_t"] = T.mark("slam")
    T.say("both", "Let's learn to write A B C!", gap=0.2)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Every letter, from A to Z, step by step!", gap=0.2)
    T.say("gul", "Get your pencil! Let's go!", gap=0.4)
    T.end(sc)
    # ------------------------------------------------------------ GET READY
    T.title("studio", "GET READY!", "gul", "Before we write, let's get ready!")
    for k, (key, text) in enumerate(PENCIL):
        sc = T.scene("ready", "studio", key=key, num=k + 1)
        T.mark("pop")
        sc["say_t"] = T.say("mishu" if k % 2 == 0 else "gul", text, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ WARM UP
    T.title("studio", "WARM UP LINES!", "mishu", "Let's warm up our fingers! Draw lines with us!")
    for k, (kind2, text) in enumerate(WARM):
        sc = T.scene("warm", "studio", line=kind2)
        sc["go_t"] = T.mark("scribble")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.2)
        T.prompts.append((round(T.t, 3), round(T.t + 1.4, 3)))
        T.pause(1.4)
        T.end(sc)
    # ------------------------------------------------------------ A TO Z
    T.title("studio", "WRITE A TO Z!", "gul", "Now, every letter! Watch the pencil, then trace with your finger!")
    for k, (L, how, w, key) in enumerate(LETTERS):
        if k and k % 6 == 0:
            sc = T.scene("cheer", "studio", done=k)
            T.mark("sparkle")
            T.say("both", f"{k} letters! Keep going!", gap=0.4)
            T.end(sc)
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("trace", "studio", L=L, key=key, w=w.upper(), num=k + 1)
        T.mark("pop")
        T.say(a, f"Letter {L}!", gap=0.1)
        sc["draw_t"] = T.mark("scribble")
        T.say(a, how, gap=0.05)
        sc["draw_end"] = round(T.t, 3)
        T.prompts.append((round(T.t, 3), round(T.t + 2.3, 3)))
        T.pause(2.3)
        sc["word_t"] = T.mark("yes")
        T.say(other(a), f"{L} is for {w}!", gap=0.3)
        T.end(sc)
    sc = T.scene("allabc", "studio")
    sc["ts"] = []
    for L, *_ in LETTERS:
        sc["ts"].append(T.mark("pop"))
        T.say("both", L, gap=0.02)
    sc["sum_t"] = T.say("gul", "A to Z! You wrote all 26 letters!", gap=0.5)
    T.stars.append(sc["sum_t"])
    T.end(sc)
    # ------------------------------------------------------------ STRAIGHT OR CURVY
    T.title("studio", "STRAIGHT OR CURVY?", "mishu", "Some letters have straight lines, and some are curvy!")
    for k, (L, straight) in enumerate(SORT):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sort", "studio", L=L, straight=straight)
        T.prompt(a, f"Letter {L}! Straight, or curvy?", wait=1.6)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), "Straight lines!" if straight else "Curvy!", gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ WHICH IS RIGHT
    T.title("studio", "WHICH ONE IS RIGHT?", "gul", "Oops! One letter is backwards! Which one is right?")
    for k, (L, pos) in enumerate(RIGHT):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("right", "studio", L=L, pos=pos)
        T.prompt(a, f"Which {L} is right?", wait=2.0)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), "This one! Good eyes!", gap=0.4)
        T.end(sc)
    # ------------------------------------------------------------ MISSING LETTER
    T.title("studio", "WHICH LETTER IS MISSING?", "mishu", "A letter is missing! Can you write it?")
    for k, (seq, miss) in enumerate(MISSING):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("missing", "studio", seq=seq, miss=miss)
        T.prompt(a, "Which letter is missing?", wait=2.0)
        sc["answer_t"] = T.mark("scribble")
        T.say(other(a), f"{seq[miss]}!", gap=0.8)
        T.end(sc)
    # ------------------------------------------------------------ SMALL LETTERS
    T.title("studio", "SMALL LETTERS!", "gul", "Letters can be small too! Let's write some!")
    for k, (L, how) in enumerate(LOWER):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("lower", "studio", L=L, num=k + 1, of=len(LOWER))
        sc["draw_t"] = T.mark("scribble")
        T.say(a, how, gap=0.05)
        sc["draw_end"] = round(T.t, 3)
        T.prompts.append((round(T.t, 3), round(T.t + 1.5, 3)))
        T.pause(1.5)
        T.end(sc)
    # ------------------------------------------------------------ NUMBERS
    T.title("studio", "WRITE NUMBERS!", "gul", "We can write numbers too! One to five!")
    for k, (L, how) in enumerate(NUMS):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("lower", "studio", L=L, num=k + 1, of=len(NUMS))
        sc["draw_t"] = T.mark("scribble")
        T.say(a, how, gap=0.05)
        sc["draw_end"] = round(T.t, 3)
        T.prompts.append((round(T.t, 3), round(T.t + 1.6, 3)))
        T.pause(1.6)
        T.end(sc)
    # ------------------------------------------------------------ WRITE WITH
    T.title("studio", "WHAT CAN WE WRITE WITH?", "mishu", "Pencils are not the only way to write!")
    for k, (key, text) in enumerate(TOOLS):
        sc = T.scene("tool", "studio", key=key)
        sc["draw_t"] = T.mark("scribble")
        sc["say_t"] = T.say("gul" if k % 2 == 0 else "mishu", text, gap=0.6)
        sc["draw_end"] = round(T.t, 3)
        T.end(sc)
    # ------------------------------------------------------------ WRITE WORDS
    T.title("studio", "WRITE A WORD!", "mishu", "Letters make words! Let's write some words!")
    for k, (word, key, text) in enumerate(WORDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("wordw", "studio", word=word, key=key)
        sc["draw_t"] = T.mark("scribble")
        T.say(a, text, gap=0.2)
        sc["draw_end"] = round(T.t, 3)
        sc["pic_t"] = T.mark("tada")
        T.pause(1.2)
        T.end(sc)
    # ------------------------------------------------------------ WRITE YOUR NAME
    T.title("studio", "WRITE YOUR NAME!", "gul", "The best word to write is your name!")
    for who, body_, text in NAMES:
        sc = T.scene("name", "studio", word=who, who=body_)
        sc["draw_t"] = T.mark("scribble")
        T.say("gul" if body_ == "gul" else "mishu", text, gap=0.2)
        sc["draw_end"] = round(T.t, 3)
        T.mark("tada")
        T.pause(1.0)
        T.end(sc)
    sc = T.scene("yourname", "studio")
    T.prompt("both", "Now, can you write your name?", wait=2.5)
    T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("studio", "LETTER DANCE!", "mishu", "Stand up! Let's write in the air!")
    T.dance("studio", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("studio", "WRITING QUIZ!", "gul", "Quick quiz time! Are you ready?")
    T.quiz("studio", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "studio")
    T.say("mishu", "Great writing! Keep practising every day!", gap=0.2)
    sc["bye_t"] = T.say("both", "Bye bye, little writers!", gap=1.8)
    T.end(sc)
    return T


def sfx(kind):
    if kind == "scribble":
        import numpy as np
        t = M.tt(0.9)
        rng = np.random.default_rng(22)
        n = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
        return [(n * 0.18 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)) * np.minimum(1, (0.9 - t) / 0.2), 0, 0.35)]
    return None


if __name__ == "__main__":
    T = build()
    tune = [76, 76, 79, 79, 81, 81, 79, 0, 77, 77, 76, 76, 74, 74, 72, 0]
    M.finish(T, music=dict(bpm=116, prog=[[60, 64, 67], [65, 69, 72], [55, 59, 62], [60, 64, 67]], hook=tune, start=1.8), sfx=sfx)
