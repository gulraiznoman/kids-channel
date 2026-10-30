"""Long video 1: Baby Animals & Fun Learning with Gul & Mishu (~12-13 min).

Six sections, each with its own background and title card. Same beat structure as the episodes
(item pops in, question, answer + label, "can you say", pause, praise, fun line).
"""

TOPIC = "Fun Learning!"
NOUN = "THING"
OUTFITS = {"gul": "tee", "misheal": "yellow"}
VOICES = {
    "gul": dict(voice="en-US-AnaNeural", pitch="-40Hz", rate="+0%"),
    "mishu": dict(voice="en-US-AnaNeural", pitch="+12Hz", rate="-4%"),
}

# (section title, background, intro line (speaker, text), question lines, items)
# item: key, label, answer line, "say" word, fun line (speaker, text) or None
SECTIONS = [
    ("BABY ANIMALS!", "bg_farm.png", ("mishu", "Let's go to the farm and meet some baby animals!"),
     ["Who is this?", "Ooh, who is this?", "Look! Who is it?"],
     [("puppy", "Puppy", "It's a puppy! A puppy says woof, woof!", "puppy", ("gul", "Woof, woof!")),
      ("kitten", "Kitten", "It's a kitten! A kitten says meow!", "kitten", ("mishu", "Meow, meow!")),
      ("duckling", "Duckling", "It's a duckling! A duckling says quack, quack!", "duckling", ("gul", "Quack, quack!")),
      ("chick", "Chick", "It's a little chick! A chick says cheep, cheep!", "chick", ("mishu", "Cheep, cheep!")),
      ("lamb", "Lamb", "It's a lamb! A lamb says baa!", "lamb", ("gul", "Baa, baa!")),
      ("piglet", "Piglet", "It's a piglet! A piglet says oink, oink!", "piglet", ("mishu", "Oink, oink!")),
      ("calf", "Calf", "It's a calf! A baby cow says moo!", "calf", ("gul", "Moo, moo!")),
      ("bunny", "Bunny", "It's a bunny! Bunnies go hop, hop, hop!", "bunny", ("mishu", "Hop, hop, hop!")),
      ("foal", "Foal", "It's a foal! A baby horse says neigh!", "foal", ("gul", "Neigh!")),
      ("cub", "Lion Cub", "It's a lion cub! A lion says roar!", "lion cub", ("mishu", "Roar!")),
      ("elephant", "Baby Elephant", "It's a baby elephant! It has a long trunk!", "elephant", ("gul", "Toot, toot!")),
      ("monkey", "Monkey", "It's a little monkey! Ooh, ooh, aah, aah!", "monkey", ("mishu", "Ooh, ooh, aah, aah!"))]),
    ("SHAPES!", "bg.png", ("gul", "Now let's learn shapes!"),
     ["What shape is this?", "Ooh, what shape is it?", "Look! What shape?"],
     [("circle", "Circle", "It's a circle! Round like a ball!", "circle", ("mishu", "Round and round!")),
      ("square", "Square", "It's a square! It has four sides!", "square", ("gul", "Four sides!")),
      ("triangle", "Triangle", "It's a triangle! It has three sides!", "triangle", ("mishu", "One, two, three!")),
      ("star", "Star", "It's a star! Twinkle, twinkle!", "star", ("gul", "A shiny star!")),
      ("heart", "Heart", "It's a heart! I love you!", "heart", ("mishu", "Love you too!")),
      ("rectangle", "Rectangle", "It's a rectangle! Like a door!", "rectangle", ("gul", "Knock, knock!")),
      ("oval", "Oval", "It's an oval! Like an egg!", "oval", ("mishu", "An egg shape!")),
      ("diamond", "Diamond", "It's a diamond! Like a kite!", "diamond", ("gul", "Fly, kite, fly!"))]),
    ("VEHICLES!", "bg_road.png", ("mishu", "Beep, beep! Let's see some vehicles!"),
     ["What is this?", "Ooh, what's this one?", "Look! What is it?"],
     [("car", "Car", "It's a car! Beep, beep!", "car", ("gul", "Beep, beep!")),
      ("bus", "Bus", "It's a big yellow bus!", "bus", ("mishu", "The wheels go round and round!")),
      ("firetruck", "Fire Truck", "It's a fire truck! Nee naw, nee naw!", "fire truck", ("gul", "Nee naw, nee naw!")),
      ("police", "Police Car", "It's a police car! Wee woo, wee woo!", "police car", ("mishu", "Wee woo!")),
      ("ambulance", "Ambulance", "It's an ambulance! It helps people!", "ambulance", ("gul", "Help is coming!")),
      ("train", "Train", "It's a train! Choo, choo!", "train", ("mishu", "Choo, choo!")),
      ("airplane", "Airplane", "It's an airplane! It flies in the sky!", "airplane", ("gul", "Zoom!")),
      ("boat", "Boat", "It's a boat! It floats on water!", "boat", ("mishu", "Splish, splash!")),
      ("tractor", "Tractor", "It's a tractor! It works on the farm!", "tractor", ("gul", "Chug, chug!")),
      ("helicopter", "Helicopter", "It's a helicopter! Whirr, whirr!", "helicopter", ("mishu", "Up, up, up!"))]),
    ("OCEAN ANIMALS!", "bg_beach.png", ("gul", "Splash! Let's go to the ocean!"),
     ["Who lives in the ocean?", "Ooh, who is swimming?", "Look! Who is this?"],
     [("fish", "Fish", "It's a little fish! Swim, swim!", "fish", ("mishu", "Blub, blub!")),
      ("octopus", "Octopus", "It's an octopus! It has eight arms!", "octopus", ("gul", "Eight wiggly arms!")),
      ("whale", "Whale", "It's a whale! A very big whale!", "whale", ("mishu", "Splash!")),
      ("crab", "Crab", "It's a crab! Snap, snap!", "crab", ("gul", "Snap, snap!")),
      ("turtle", "Turtle", "It's a turtle! Slow and steady!", "turtle", ("mishu", "Hello, turtle!")),
      ("starfish", "Starfish", "It's a starfish! A star in the sea!", "starfish", ("gul", "Twinkle, starfish!")),
      ("dolphin", "Dolphin", "It's a dolphin! It loves to jump!", "dolphin", ("mishu", "Jump, jump!")),
      ("jellyfish", "Jellyfish", "It's a jellyfish! Wiggly and wobbly!", "jellyfish", ("gul", "Wiggle, wobble!"))]),
    ("LET'S COUNT!", "bg_rainbow.png", ("gul", "Now let's count with yummy fruits!"),
     ["How many?", "Let's count! How many?", "How many can you see?"],
     [("n1", "One", "One! One apple!", "one", None),
      ("n2", "Two", "One, two! Two bananas!", "two", None),
      ("n3", "Three", "One, two, three! Three oranges!", "three", None),
      ("n4", "Four", "One, two, three, four! Four strawberries!", "four", None),
      ("n5", "Five", "One, two, three, four, five! Five lemons!", "five", ("mishu", "High five!")),
      ("n6", "Six", "One, two, three, four, five, six! Six cherries!", "six", None),
      ("n7", "Seven", "One, two, three, four, five, six, seven! Seven pears!", "seven", None),
      ("n8", "Eight", "One, two, three, four, five, six, seven, eight! Eight kiwis!", "eight", None),
      ("n9", "Nine", "One, two, three, four, five, six, seven, eight, nine! Nine pineapples!", "nine", None),
      ("n10", "Ten", "One, two, three, four, five, six, seven, eight, nine, ten! Ten mangoes!", "ten", ("gul", "We counted to ten!"))]),
    ("WEATHER!", "bg.png", ("mishu", "Let's look at the weather!"),
     ["What's the weather?", "Ooh, what's the weather now?", "Look at the sky! What's the weather?"],
     [("sunny", "Sunny", "It's sunny! The sun is shining!", "sunny", ("gul", "Let's play outside!")),
      ("rainy", "Rainy", "It's rainy! Pitter, patter!", "rainy", ("mishu", "Put on your boots!")),
      ("cloudy", "Cloudy", "It's cloudy! Big grey clouds!", "cloudy", ("gul", "Where is the sun?")),
      ("windy", "Windy", "It's windy! Whoosh!", "windy", ("mishu", "Hold your hat!")),
      ("snowy", "Snowy", "It's snowy! Cold, white snow!", "snowy", ("gul", "Let's make a snowman!")),
      ("rainbow", "Rainbow", "It's a rainbow! So many colours!", "rainbow", ("mishu", "So pretty!"))]),
]
PRAISE = ["Great job!", "Yay! Well done!", "Awesome!", "Super!", "Good job, friends!", "You did it!"]

import json as _json, pathlib as _pl
_man = _pl.Path(__file__).resolve().parent.parent / "stock" / "manifest.json"
SOUNDS = {k for k, v in (_json.load(open(_man)) if _man.exists() else {}).items() if v.get("sound")}

FRUITS = [(it[0], it[1], it[2], it[4]) for s in SECTIONS for it in s[4]]


def beats():
    B = [dict(who="gul", text="Hi friends! I'm Gul!", wave="gul", scene="intro", bg="bg.png"),
         dict(who="mishu", text="And I'm Mishu! Today is a big fun learning day!", wave="mishu"),
         dict(who="gul", text="Animals, shapes, vehicles, ocean friends, numbers, and the weather! Let's go!", eyes_closed="gul")]
    n = 0
    for si, (title, bg, intro, questions, items) in enumerate(SECTIONS):
        B.append(dict(pause=0.4, section=title, bg=bg))
        B.append(dict(who=intro[0], text=intro[1], section_hold=title))
        for k, (key, name, answer, say, fun) in enumerate(items):
            q_who = "mishu" if n % 2 == 0 else "gul"
            a_who = "gul" if q_who == "mishu" else "mishu"
            B.append(dict(pause=0.8, fruit_in=key))
            B.append(dict(who=q_who, text=questions[k % len(questions)]))
            B.append(dict(who=a_who, text=answer, label=name))
            if key in SOUNDS:
                B.append(dict(pause=1.7, sfx=key))           # the real animal / vehicle sound
            B.append(dict(who=q_who, text=f"{name}! Can you say {say}?", spell=name))
            B.append(dict(pause=2.6, prompt=True))
            B.append(dict(who=a_who, text=PRAISE[n % len(PRAISE)], eyes_closed=a_who, stars=True))
            if fun:
                B.append(dict(who=fun[0], text=fun[1]))
            B.append(dict(pause=0.5, fruit_out=key))
            n += 1
    B += [dict(pause=0.5, bg="bg_rainbow.png"),
          dict(who="mishu", text="Wow! We learned so many things today!"),
          dict(who="gul", text="Which one was your favourite? Mine was the fire truck!", eyes_closed="gul"),
          dict(who="mishu", text="Bye bye, friends!", wave="mishu", scene="outro"),
          dict(who="gul", text="See you next time!", wave="gul"),
          dict(pause=2.5, end=True)]
    return B
