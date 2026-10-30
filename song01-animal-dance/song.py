"""Song 1 "Animal Dance": original lyrics and melody (no copyright issues).

Each note: (who, word, beat, beats, midi) or a word with several syllable notes: midi as a list.
Beats count from 0 at the start of the song; 4 beats per bar.
"""
BPM = 120
BEAT = 60 / BPM
TITLE = "Animal Dance"

# (who, animal, action) per verse; art keys from long01-animals-fun/art/fruit_<key>.png
VERSES = [
    ("gul", "elephant", "Elephant", "Stomp"),
    ("mishu", "bunny", "Bunny", "Jump"),
    ("gul", "monkey", "Monkey", "Swing"),
    ("mishu", "duckling", "Duckling", "Quack"),
]
INTRO_BARS = 2          # music + "Animal dance!" shout
SYL = {"Elephant": 3, "Bunny": 2, "Monkey": 2, "Duckling": 2}


def notes():
    out = []
    b = 4.0                                            # bar 2: "Animal dance!" pickup
    out += [("both", "Animal", b + 0, 1.5, [67, 69, 67]), ("both", "dance!", b + 2, 1.5, 72)]
    b = INTRO_BARS * 4
    for k, (who, key, name, act) in enumerate(VERSES):
        n = SYL[name]
        mel = [60, 64, 64] if n == 3 else [60, 64]
        mel2 = [62, 65, 65] if n == 3 else [62, 65]
        out += [(who, name + "!", b + 0, 1.8, mel), (who, name + "!", b + 2, 1.8, mel2)]
        out += [(who, act, b + 4, 0.9, 67), (who, act, b + 5, 0.9, 65), (who, act + "!", b + 6, 1.6, 64 if k % 2 == 0 else 72)]
        b += 8
    # chorus x1: "Dance, dance, dance! Everybody dance!"
    out += [("both", "Dance", b + 0, 0.9, 67), ("both", "dance", b + 1, 0.9, 67), ("both", "dance!", b + 2, 1.6, 69),
            ("both", "Everybody", b + 4, 2.0, [69, 67, 65, 64]), ("both", "dance!", b + 6, 1.8, 72)]
    b += 8
    return out, b + 2                                  # +2 beats tail


def verse_spans():
    """(start_beat, end_beat, who, art_key, action) for the video."""
    b = INTRO_BARS * 4
    s = []
    for who, key, name, act in VERSES:
        s.append((b, b + 8, who, key, act.lower()))
        b += 8
    return s
