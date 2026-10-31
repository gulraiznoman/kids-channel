"""Long video 25: "First Words for Toddlers". python make.py
Slower pace than the other videos: each word is said twice with a long pause for the child to answer.
Music: our own gentle tune, code instruments."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from longkit import Maker, other

M = Maker(__file__)
GROUPS = [  # title, intro, background, words (word, picture key, short sentence)
    ("MY FAMILY!", "Let's say our family words!", "bedroom", [("Mama", "mama", "I love Mama!"), ("Papa", "papa", "Hello, Papa!"), ("Baby", "baby", "A happy baby!")]),
    ("ANIMAL WORDS!", "Let's say animal words!", "farm", [("Dog", "dog", "Woof, woof! A dog!"), ("Cat", "cat", "Meow! A cat!"), ("Duck", "duck", "Quack, quack! A duck!"),
                                                         ("Bird", "bird", "Tweet, tweet! A bird!"), ("Fish", "fish", "Splash! A fish!"), ("Pig", "pig", "Oink, oink! A pig!")]),
    ("FOOD WORDS!", "Are you hungry? Let's say food words!", "kitchen", [("Milk", "bottle", "Yummy milk!"), ("Water", "water", "Drink your water!"), ("Apple", "apple", "A red apple!"),
                                                                         ("Banana", "banana", "A yellow banana!"), ("Egg", "egg", "An egg! Yum!"), ("Bread", "toast", "Warm bread!")]),
    ("MY THINGS!", "Let's say words for our things!", "bedroom", [("Ball", "ball", "Bounce the ball!"), ("Car", "car", "Vroom, vroom! A car!"), ("Book", "book", "Read a book!"),
                                                                  ("Shoes", "shoes", "Put on your shoes!"), ("Hat", "hat", "A hat for my head!"), ("Cup", "cupkid", "A blue cup!"),
                                                                  ("Bed", "bed", "Time for bed!"), ("Teddy", "teddy", "Hug your teddy!"), ("Socks", "socks", "Socks on my feet!"), ("Spoon", "spoon", "Eat with a spoon!")]),
    ("MY BODY!", "Let's point to our body!", "playroom2", [("Nose", "nose", "Touch your nose!"), ("Eyes", "eye", "Blink your eyes!"), ("Mouth", "mouth", "Open your mouth!"),
                                                          ("Ear", "ear", "Touch your ear!"), ("Hand", "hand", "Wave your hand!")]),
    ("OUTSIDE WORDS!", "Let's go outside! What can we see?", "park", [("Sun", "sun", "The sun is hot!"), ("Tree", "tree", "A big green tree!"), ("Flower", "flower", "Smell the flower!"),
                                                                      ("Bus", "bus", "Beep, beep! A bus!"), ("Moon", "moon", "The moon comes out at night!"),
                                                                      ("Star", "star", "A shiny star!")])]
ACTIONS = [("Up", "up", "Up, up, up!"), ("Down", "down", "Down, down, down!"), ("Go", "go", "Ready, go!"), ("Stop", "stop", "Stop!"),
           ("Jump", "jump", "Jump, jump!"), ("Clap", "clap", "Clap your hands!"), ("Sleep", "sleep", "Shh! Sleep!"), ("Eat", "eat", "Yum, yum! Eat!")]
MAGIC = [("Hi", "wave", "Hi! Wave your hand!"), ("Bye bye", "wave", "Bye bye!"), ("Please", "happy", "More milk, please!"), ("Thank you", "happy", "Thank you, Mama!"),
         ("More", "more", "More, please!"), ("All done", "done", "All done!"), ("Yes", "yes", "Yes! Nod your head!"), ("No", "no", "No! Shake your head!")]
PHRASES = [("Big ball", "ball", "Big ball!"), ("Red apple", "apple", "Red apple!"), ("More milk", "bottle", "More milk!"), ("Bye bye, Papa", "papa", "Bye bye, Papa!"),
           ("Baby sleep", "baby", "Baby sleep!"), ("Go car", "car", "Go car!")]
WHERE = [("ball", ["ball", "apple", "dog"], "Where is the ball?", "There it is! Ball!"), ("dog", ["cat", "car", "dog"], "Where is the dog?", "There it is! Dog!"),
         ("apple", ["apple", "shoes", "duck"], "Where is the apple?", "There it is! Apple!"), ("book", ["hat", "book", "bus"], "Where is the book?", "There it is! Book!"),
         ("shoes", ["teddy", "shoes", "banana"], "Where are the shoes?", "There they are! Shoes!")]
PEEK = [("baby", "Baby!"), ("cat", "Cat!"), ("teddy", "Teddy!"), ("duck", "Duck!")]
SOUNDS = [("dog", "What does the dog say?", "Woof, woof!"), ("cat", "What does the cat say?", "Meow!"), ("duck", "What does the duck say?", "Quack, quack!"),
          ("car", "What does the car say?", "Vroom, vroom!"), ("bus", "What does the bus say?", "Beep, beep!")]
DANCE = [("Clap, clap, clap!", "shake"), ("Up, up, up!", "stretch"), ("Stomp, stomp, stomp!", "stomp"), ("Jump, jump, jump!", "jump"),
         ("Spin around!", "spin"), ("Wave bye bye!", "sway")]
QUIZ = [("What's this?", "Ball!", "ball"), ("What's this?", "Dog!", "dog"), ("What's this?", "Apple!", "apple"), ("What's this?", "Book!", "book")]


def word_scene(T, w, key, line_, a, bg, kind="word", **extra):
    sc = T.scene(kind, bg, key=key, w=w.upper(), **extra)
    T.mark("pop")
    sc["say_t"] = T.say(a, f"{w}.", gap=0.5)
    T.say(a, f"{w}!", gap=0.1)
    T.prompts.append((round(T.t, 3), round(T.t + 2.3, 3)))
    T.pause(2.3)
    sc["line_t"] = T.mark("yes")
    T.say(other(a), line_, gap=0.5)
    T.end(sc)


def build():
    T = M.TL()
    # ------------------------------------------------------------ OPENING
    sc = T.scene("intro", "playroom2")
    T.pause(0.2)
    sc["title_t"] = T.mark("slam")
    T.say("both", "First words!", gap=0.3)
    sc["kids_t"] = round(T.t, 3)
    T.say("mishu", "Hello, baby! Hello, toddler! Let's learn to talk!", gap=0.3)
    T.say("gul", "We say a word. Then it's your turn! Ready?", gap=0.5)
    T.end(sc)
    sc = T.scene("hello", "playroom2")
    T.say("mishu", "Say hi! Hi!", gap=0.1)
    T.prompts.append((round(T.t, 3), round(T.t + 2.2, 3)))
    T.pause(2.2)
    T.say("gul", "Good job! Hi!", gap=0.5)
    T.end(sc)
    # ------------------------------------------------------------ WORD GROUPS (first half)
    n = 0

    def group(title, intro, bg, words):
        nonlocal n
        T.title(bg, title, "gul" if n % 2 == 0 else "mishu", intro)
        for k, (w, key, line_) in enumerate(words):
            word_scene(T, w, key, line_, "mishu" if k % 2 == 0 else "gul", bg)
        n += 1

    for g in GROUPS[:3]:
        group(*g)
    # ------------------------------------------------------------ ANIMAL AND CAR SOUNDS
    T.title("farm", "WHAT DOES IT SAY?", "mishu", "Sounds are first words too!")
    for k, (key, q, ans) in enumerate(SOUNDS):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("sound", "farm", key=key, ans=ans.upper())
        T.prompt(a, q, wait=2.3)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ PEEKABOO
    T.title("bedroom", "PEEKABOO!", "gul", "Who is hiding? Peekaboo!")
    for k, (key, ans) in enumerate(PEEK):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("peek", "bedroom", key=key)
        T.say(a, "Who's that? Peek...", gap=0.8)
        sc["boo_t"] = T.mark("tada")
        T.say("both", "A boo!", gap=0.4)
        T.say(other(a), ans, gap=0.3)
        T.prompts.append((round(T.t, 3), round(T.t + 1.8, 3)))
        T.pause(1.8)
        T.end(sc)
    for g in GROUPS[3:]:
        group(*g)
    # ------------------------------------------------------------ ACTION WORDS
    T.title("park", "ACTION WORDS!", "gul", "Let's do it, and say it!")
    for k, (w, act, line_) in enumerate(ACTIONS):
        word_scene(T, w, act, line_, "mishu" if k % 2 == 0 else "gul", "park", kind="action")
    # ------------------------------------------------------------ MAGIC WORDS
    T.title("playroom2", "SPECIAL WORDS!", "mishu", "These words help us every day!")
    for k, (w, act, line_) in enumerate(MAGIC):
        word_scene(T, w, act, line_, "gul" if k % 2 == 0 else "mishu", "playroom2", kind="action")
    # ------------------------------------------------------------ WHERE IS IT
    T.title("playroom2", "WHERE IS IT?", "gul", "Can you point to it?")
    for k, (good, keys, q, ans) in enumerate(WHERE):
        a = "mishu" if k % 2 == 0 else "gul"
        sc = T.scene("where", "playroom2", keys=keys, good=good, w=good.upper())
        T.prompt(a, q, wait=2.4)
        sc["answer_t"] = T.mark("yes")
        T.say(other(a), ans, gap=0.5)
        T.end(sc)
    # ------------------------------------------------------------ TWO WORDS
    T.title("playroom2", "TWO WORDS!", "mishu", "Big kids can say two words together!")
    for k, (p, key, line_) in enumerate(PHRASES):
        a = "gul" if k % 2 == 0 else "mishu"
        sc = T.scene("phrase", "playroom2", key=key, w=p.upper())
        T.mark("pop")
        sc["say_t"] = T.say(a, f"{p}.", gap=0.5)
        T.say(a, line_, gap=0.1)
        T.prompts.append((round(T.t, 3), round(T.t + 2.5, 3)))
        T.pause(2.5)
        T.end(sc)
    # ------------------------------------------------------------ DANCE
    T.title("playroom2", "WORD DANCE!", "gul", "Stand up! Let's move and say the words!")
    T.dance("playroom2", DANCE)
    # ------------------------------------------------------------ QUIZ
    T.title("playroom2", "WHAT'S THIS?", "mishu", "Your turn! Say the word!")
    T.quiz("playroom2", QUIZ)
    # ------------------------------------------------------------ OUTRO
    sc = T.scene("outro", "playroom2")
    T.say("mishu", "Great talking! Keep saying your words every day!", gap=0.3)
    sc["bye_t"] = T.say("both", "Bye bye!", gap=2.2)
    T.end(sc)
    return T


if __name__ == "__main__":
    T = build()
    tune = [72, 0, 76, 0, 79, 0, 76, 0, 77, 0, 74, 0, 72, 0, 0, 0]
    M.finish(T, music=dict(bpm=96, prog=[[60, 64, 67], [65, 69, 72], [60, 64, 67], [55, 59, 62]], hook=tune, start=2.0))
