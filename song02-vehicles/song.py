"""Song 2 "Vehicle Sounds": original lyrics and tune (no copyright issues).

All song-specific settings live here; sing/music/render/thumb read them.
Each note: (who, word, beat, beats, midi) or a word with several syllable notes: midi as a list.
Beats count from 0 at the start of the song; 4 beats per bar.
"""
BPM = 120
BEAT = 60 / BPM
TITLE = "Vehicle Sounds"
SLUG = "S02 Vehicle Sounds"                 # VIDEOS folder; file names start with TITLE
TITLE_LINES = ("BEEP BEEP", "GO GO!")        # big intro title + thumbnail
INTRO_WORDS = ("Beep beep", "Let's go!")    # shouted by both in bar 2
CHORUS = ("Go", "Everybody go!")             # "Go, go, go! Everybody go!"
BG = "bg_road.png"

# (who, art key, name sung twice, sound sung three times, animation)
# art keys from long01-animals-fun/art/fruit_<key>.png
VERSES = [
    ("gul", "car", "Little car", "Beep", "drive"),
    ("mishu", "train", "Choo-choo train", "Choo-choo", "chug"),
    ("gul", "police", "Police car", "Woo-woo", "siren"),
    ("mishu", "firetruck", "Fire truck", "Ding ding", "siren"),
]
RAY_COL = {"car": (255, 120, 120), "train": (130, 200, 255), "firetruck": (255, 200, 80), "police": (140, 160, 255)}
INTRO_BARS = 2


def notes():
    out = []
    b = 4.0                                            # bar 2: intro shout
    out += [("both", INTRO_WORDS[0], b + 0, 1.5, [67, 69]), ("both", INTRO_WORDS[1], b + 2, 1.5, [72, 72])]
    b = INTRO_BARS * 4
    for k, (who, key, name, snd, anim) in enumerate(VERSES):
        out += [(who, name + "!", b + 0, 1.8, [60, 64]), (who, name + "!", b + 2, 1.8, [62, 65])]
        out += [(who, snd, b + 4, 0.9, 67), (who, snd, b + 5, 0.9, 65), (who, snd + "!", b + 6, 1.6, 64 if k % 2 == 0 else 72)]
        b += 8
    w, line = CHORUS
    out += [("both", w, b + 0, 0.9, 67), ("both", w.lower(), b + 1, 0.9, 67), ("both", w.lower() + "!", b + 2, 1.6, 69),
            ("both", line, b + 4, 3.6, [69, 67, 65, 64, 72])]
    b += 8
    return out, b + 2                                  # +2 beats tail


def verse_spans():
    """(start_beat, end_beat, who, art_key, animation) for the video."""
    b = INTRO_BARS * 4
    s = []
    for who, key, name, snd, anim in VERSES:
        s.append((b, b + 8, who, key, anim))
        b += 8
    return s


def cast():
    return [v[1] for v in VERSES]

FACES_RIGHT = {"car": True, "train": False, "firetruck": True, "police": True}   # which way the art points
STAGE_Y = 1120                              # vehicles drive on the road
LIGHTS = {"police": (0.0, -0.36), "firetruck": (0.33, -0.22)}   # siren light spot, as a share of art size (art facing right)
