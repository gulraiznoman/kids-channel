"""Nursery-rhyme loop Shorts (1080x1920). COPYRIGHT-SAFE: traditional public-domain tunes and words only
(Old MacDonald: traditional, 1917 and earlier; Twinkle Twinkle: 1761 French tune + 1806 Jane Taylor poem),
played by OUR OWN instruments made in code and chanted by Gul & Mishu (Kokoro voices). No outside recordings.

python tools/rhyme_shorts.py macdonald|twinkle [frames]
"""
import hashlib, math, os, subprocess, sys, pathlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "voices"))
sys.path.insert(0, str(ROOT / "long02-counting"))
import loop_shorts as LS
import importlib.util
_spec = importlib.util.spec_from_file_location("l02render", ROOT / "long02-counting" / "render.py")
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
import kidvoice

A, M = LS.A, LS.M
W, H, FPS, SR = 1080, 1920, 30, 48000
INK, RAINBOW = LS.INK, LS.RAINBOW
CACHE = ROOT / "tools" / "_rhyme_words"
CACHE.mkdir(exist_ok=True)
N = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71, "C5": 72, "G3": 55, "A3": 57, "B3": 59}

# token = (words, beats, notes)  notes = melody per syllable, spread evenly over the token
MACDONALD = {
    "bpm": 132,
    "tokens": [
        ("Old", 1, "C"), ("MacDonald", 3, "C C G"), ("had a", 2, "A A"), ("farm", 2, "G"),
        ("E", 1, "E"), ("I", 1, "E"), ("E", 1, "D"), ("I", 1, "D"), ("O", 4, "C"),
        ("And on that farm", 4, "G3 C C C"), ("he had a cow", 4, "G A A G"),
        ("E", 1, "E"), ("I", 1, "E"), ("E", 1, "D"), ("I", 1, "D"), ("O", 4, "C"),
        ("With a moo moo here", 2, "G3 G3 C C C"), ("and a moo moo there", 2, "G3 G3 C C C"),
        ("Here a moo", 1, "C C C"), ("there a moo", 1, "C C C"), ("everywhere a moo moo", 2, "C C C C C C"),
        ("Old", 1, "C"), ("MacDonald", 3, "C C G"), ("had a", 2, "A A"), ("farm", 2, "G"),
        ("E", 1, "E"), ("I", 1, "E"), ("E", 1, "D"), ("I", 1, "D"), ("O", 4, "C")],
    "chords": ["C", "C", "F", "C", "C", "C", "G", "C", "C", "C", "F", "C", "C", "G", "C", "C"],
}
TWINKLE = {
    "bpm": 104,
    "tokens": [
        ("Twinkle", 2, "C C"), ("twinkle", 2, "G G"), ("little", 2, "A A"), ("star", 2, "G"),
        ("How", 1, "F"), ("I", 1, "F"), ("wonder", 2, "E E"), ("what", 1, "D"), ("you", 1, "D"), ("are", 2, "C"),
        ("Up", 1, "G"), ("above", 2, "G F"), ("the", 1, "F"), ("world", 1, "E"), ("so", 1, "E"), ("high", 2, "D"),
        ("Like", 1, "G"), ("a", 1, "G"), ("diamond", 2, "F F"), ("in", 1, "E"), ("the", 1, "E"), ("sky", 2, "D")],
    "chords": ["C", "C", "F", "C", "F", "C", "G", "C", "C", "F", "C", "G", "C", "F", "C", "G"],
}
CHORD = {"C": [60, 64, 67], "F": [65, 69, 72], "G": [67, 71, 74]}


def timeline(song):
    beat = 60 / song["bpm"]
    t, out = 0.0, []
    for words, beats, notes in song["tokens"]:
        ns = [N[x] for x in notes.split()]
        out.append(dict(words=words, t=round(t, 4), dur=beats * beat, notes=ns))
        t += beats * beat
    return out, t, beat


# ------------------------------------------------------------------ voices: chant each word group on its beat
def say(who, text, speed=None):
    c = dict(kidvoice.CHARACTERS[who])
    if speed:
        c["speed"] = speed
    p = CACHE / f"{who}_{hashlib.md5((who + text + str(c)).encode()).hexdigest()[:10]}.wav"
    if not p.exists():
        kidvoice.say(text + "!", p, **c)
    x, sr = sf.read(p)
    idx = np.where(np.abs(x) > 0.03 * np.abs(x).max())[0]
    return x[max(0, idx[0] - int(0.005 * sr)): idx[-1] + int(0.03 * sr)]


SPOKEN = {"E": "Ee", "I": "Eye", "O": "Oh"}       # say letters the way they sound (displayed as E-I-E-I-O)


def chant(who, text, slot):
    text = SPOKEN.get(text, text)
    x = say(who, text)
    if len(x) > slot * SR * 1.05:
        x = say(who, text, round(min(1.6, kidvoice.CHARACTERS[who]["speed"] * len(x) / (slot * SR) * 1.08), 2))
    x = x[: int(slot * SR * 1.1)].copy()
    f = min(len(x) // 3, int(0.03 * SR))
    if f:
        x[-f:] *= np.linspace(1, 0, f)
    return x


def vocals(toks, total):
    n = int(total * SR)
    v = np.zeros((n, 2))
    for tk in toks:
        for who, g, pan in (("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)):
            x = chant(who, tk["words"], tk["dur"])
            A.add(v, x, tk["t"], g, pan)
    return v


def music(song, toks, total, beat, style):
    n = int(total * SR)
    m = np.zeros((n, 2))
    bars = int(round(total / (4 * beat)))
    for b in range(bars):
        ch = CHORD[song["chords"][b % len(song["chords"])]]
        for q in range(4):
            tt = b * 4 * beat + q * beat
            if style == "farm":
                A.add(m, LS.kick(), tt, 0.45)
                if q in (1, 3):
                    A.add(m, M.clap(), tt, 0.25)
                A.add(m, LS.hat(), tt + beat / 2, 0.5, 0.3)
                A.add(m, M.tuba(ch[0] - 24 + (7 if q % 2 else 0), beat * 0.7), tt, 0.3)
                A.add(m, M.uke_chord([x + 12 for x in ch], 0.2), tt + beat / 2, 0.05, -0.3)
            else:                                              # night: soft music-box arpeggio + warm pad
                for j, nt in enumerate((ch[0], ch[1], ch[2], ch[1])):
                    A.add(m, A.tone(A.mtof(nt + 12), 0.9, ((1, 1), (3, 0.25), (5.2, 0.08)), 0.002, 0.5), tt + j * beat / 4, 0.025, 0.25)
                if q == 0:
                    A.add(m, A.tone(A.mtof(ch[0] - 12), 4 * beat, ((1, 1), (2, 0.3)), 0.2, 2.5), tt, 0.12)
    for tk in toks:                                            # the TUNE, played by our instruments (carries the melody)
        k = len(tk["notes"])
        for i, nt in enumerate(tk["notes"]):
            at = tk["t"] + i * tk["dur"] / k
            if style == "farm":
                A.add(m, M.toy_piano(nt + 12, 0.45), at, 0.11, 0.2)
                A.add(m, M.xylo(nt + 12, 0.3), at, 0.07, -0.2)
            else:
                A.add(m, A.tone(A.mtof(nt + 12), 1.2, ((1, 1), (2.76, 0.3), (5.4, 0.1)), 0.001, 0.6), at, 0.12, 0.0)
    return m


def moo():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 150 - 40 * t / 0.9
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    x = np.convolve(saw, np.ones(18) / 18, mode="same") * np.minimum(1, t / 0.08) * np.minimum(1, (0.9 - t) / 0.2)
    return x * (1 + 0.3 * np.sin(2 * np.pi * 5 * t)) * 1.5


def build_audio(song, style, path):
    toks, total, beat = timeline(song)
    v = vocals(toks, total)
    m = music(song, toks, total, beat, style)
    fx = np.zeros_like(m)
    if style == "farm":
        for tk in toks:
            if tk["words"] == "he had a cow":
                A.add(fx, moo(), tk["t"] + tk["dur"] * 0.85, 0.5)
            if tk["words"] == "O":
                A.add(fx, A.sfx_sparkle(), tk["t"], 0.2)
    else:
        for tk in toks:
            if tk["words"] in ("star", "high", "sky", "are"):
                A.add(fx, A.sfx_sparkle(), tk["t"], 0.25)
    v /= np.abs(v).max() / 0.9
    m /= np.abs(m).max()
    mix = v + m * (0.5 if style == "farm" else 0.55) + fx * 0.5
    LS.finish_audio(mix, path)
    return toks, total, beat


# ------------------------------------------------------------------ visuals
def karaoke(frame, toks, t, y, size=150):
    cur = next((tk for tk in toks if tk["t"] <= t < tk["t"] + tk["dur"]), toks[-1])
    k = (t - cur["t"]) / 0.18
    R.rainbow_text(frame, W / 2, y, cur["words"].upper() + ("" if cur["words"] in ("E", "I") else ""), int(size * R.ease_back(k)) or 1,
                   maxw=1000)
    return cur


def dancer(name, outfit, t, beat, eyes="open"):
    lb = t / beat
    singing = (lb % 1) < 0.55
    return LS.character(name, outfit, eyes=eyes, mouth="open" if singing else "smile", wave=16 * math.sin(lb * math.pi))


def farm_frame(G, t):
    toks, beat = G["toks"], G["beat"]
    fr = G["bg"].copy()
    d = ImageDraw.Draw(fr, "RGBA")
    lb = t / beat
    cur = karaoke(fr, toks, t, 300)
    # E-I-E-I-O letters build up across the row
    eio = [tk for tk in toks if tk["words"] in ("E", "I", "O")]
    groups = [eio[i:i + 5] for i in range(0, len(eio), 5)]
    for g in groups:
        if g[0]["t"] <= t < g[-1]["t"] + g[-1]["dur"]:
            for j, tk in enumerate(g):
                if t >= tk["t"]:
                    q = t - tk["t"]
                    R.rainbow_text(fr, 170 + j * 185, 520 - 30 * abs(math.sin(q * 6)) * max(0, 1 - q), tk["words"],
                                   int(130 * R.ease_back(q / 0.2)), colour=RAINBOW[j % 6])
    # the cow: bounces on the beat, big jump on "he had a cow", squash + MOO bubble on every "moo"
    cy, sx, sy = 1700, 1.0, 1.0
    cy -= 40 * abs(math.sin(lb * math.pi))
    w = cur["words"]
    if w == "he had a cow":
        q = (t - cur["t"]) / cur["dur"]
        cy -= 220 * math.sin(min(1, q * 1.4) * math.pi)
    if "moo" in w:
        q = ((t - cur["t"]) / (cur["dur"] / max(1, w.count("moo")))) % 1
        if q < 0.3:
            sx, sy = 1.1, 0.9
        bx, by = 800, 980
        d.ellipse((bx - 150, by - 85, bx + 150, by + 85), fill=(255, 255, 255, 240), outline=INK, width=7)
        d.polygon([(bx - 70, by + 70), (bx - 140, by + 160), (bx - 10, by + 80)], fill=(255, 255, 255, 240))
        R.rainbow_text(fr, bx, by + 8, "MOO!", 95, colour=(150, 90, 50))
    LS.paste(fr, G["cow"], 540, cy, sx=sx, sy=sy, bottom=True)
    # Gul & Mishu dancing at the sides
    for name, outfit, x, off in (("gul", "tee", 150, 0.0), ("misheal", "yellow", 930, 0.5)):
        im = dancer(name, outfit, t + off * beat, beat)
        hop = 30 * abs(math.sin((lb + off) * math.pi))
        LS.paste(fr, im, x, 1900 - hop, scale=0.33, bottom=True)
    for j in range(4):
        p = (t * 0.25 + j / 4) % 1
        LS.note(d, 120 + j * 270, 1100 - p * 380, 22, RAINBOW[(j + 1) % 6], int(200 * math.sin(p * math.pi)))
    return fr.convert("RGB")


def night_bg():
    y = np.linspace(0, 1, H)[:, None, None]
    img = (np.array((25, 30, 90), float) * (1 - y) + np.array((120, 70, 160), float) * y).astype(np.uint8)
    im = Image.fromarray(np.repeat(img, W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.ellipse((780, 120, 960, 300), fill=(255, 240, 180))
    d.ellipse((830, 100, 1010, 280), fill=(35, 38, 100))
    d.polygon([(0, 1500), (350, 1430), (700, 1480), (1080, 1420), (1080, 1920), (0, 1920)], fill=(60, 120, 90))
    d.polygon([(0, 1600), (500, 1560), (1080, 1620), (1080, 1920), (0, 1920)], fill=(80, 150, 100))
    return im


def smiley_star(r):
    s = int(r * 2.6)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = s / 2
    pts = [(c + (r if k % 2 == 0 else r * 0.48) * math.cos(-math.pi / 2 + k * math.pi / 5),
            c + (r if k % 2 == 0 else r * 0.48) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    d.polygon(pts, fill=(255, 220, 70), outline=INK, width=10)
    for ex in (-0.22, 0.22):
        d.ellipse((c + ex * r - 0.09 * r, c - 0.12 * r - 0.12 * r, c + ex * r + 0.09 * r, c - 0.12 * r + 0.12 * r), fill=INK)
        d.ellipse((c + ex * r - 0.05 * r, c - 0.2 * r, c + ex * r, c - 0.15 * r), fill=(255, 255, 255))
    d.arc((c - 0.2 * r, c - 0.05 * r, c + 0.2 * r, c + 0.25 * r), 20, 160, fill=INK, width=10)
    for ex in (-0.34, 0.34):
        d.ellipse((c + ex * r - 0.08 * r, c + 0.04 * r, c + ex * r + 0.08 * r, c + 0.14 * r), fill=(255, 150, 160))
    return im


def twinkle_frame(G, t):
    toks, beat = G["toks"], G["beat"]
    fr = G["bg"].copy()
    d = ImageDraw.Draw(fr, "RGBA")
    rng = G["stars"]
    for i, (x, y, s, ph) in enumerate(rng):                          # twinkling little stars
        a = 0.5 + 0.5 * math.sin(t * 3 + ph)
        R.star(d, x, y, s * (0.6 + 0.4 * a), (255, 250, 200), rot=t * 0.5 + ph)
    cur = next((tk for tk in toks if tk["t"] <= t < tk["t"] + tk["dur"]), toks[-1])
    w = cur["words"]
    rise = 0
    if w in ("Up", "above", "the", "world", "so", "high"):
        rise = 90 * math.sin(min(1, (t - [tk for tk in toks if tk["words"] == "Up"][0]["t"]) / 2.0) * math.pi / 2)
    glow = 1 + 0.08 * max(0, math.cos((t / beat % 1) * math.pi)) ** 2
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for r, a in ((330, 40), (260, 60), (200, 80)):
        ld.ellipse((540 - r * glow, 640 - rise - r * glow, 540 + r * glow, 640 - rise + r * glow), fill=(255, 240, 160, a))
    fr.alpha_composite(lay)
    big = G["star"].rotate(6 * math.sin(t * 1.5), resample=Image.BICUBIC)
    LS.paste(fr, big, 540, 640 - rise + 12 * math.sin(t * 2), scale=glow)
    if w == "diamond":                                                # a sparkly diamond appears
        q = (t - cur["t"]) / cur["dur"]
        LS.paste(fr, G["diamond"], 850, 360, scale=R.ease_back(q / 0.3), rot=10 * math.sin(t * 4))
    R.rainbow_text(fr, W / 2, 1060, w.upper(), int(140 * R.ease_back((t - cur["t"]) / 0.18)), maxw=1000)
    for name, outfit, x in (("gul", "bluetee", 300), ("misheal", "pink", 780)):
        im = LS.character(name, outfit, mouth="open" if (t / beat % 1) < 0.55 else "smile", wave=20 * math.sin(t * 2.2))
        LS.paste(fr, im, x, 1890 - 10 * abs(math.sin(t * 1.6)), scale=0.33, bottom=True)
    return fr.convert("RGB")


def build(key):
    song, style = (MACDONALD, "farm") if key == "macdonald" else (TWINKLE, "night")
    name = ("S14 Old MacDonald", "Old MacDonald - Short") if key == "macdonald" else ("S15 Twinkle Twinkle", "Twinkle Twinkle - Short")
    tmp = ROOT / "tools" / f"_rhyme_{key}"
    tmp.mkdir(exist_ok=True)
    R.G["fonts"] = {}
    toks, total, beat = timeline(song)
    G = {"toks": toks, "beat": beat}
    if style == "farm":
        G["bg"] = LS.bg_farm()
        G["cow"] = LS.load(ROOT / "long01-animals-fun" / "art" / "fruit_calf.png", 700)
        fn = farm_frame
    else:
        G["bg"] = night_bg()
        G["star"] = smiley_star(230)
        G["diamond"] = LS.load(ROOT / "long01-animals-fun" / "art" / "fruit_diamond.png", 220)
        r = np.random.default_rng(4)
        G["stars"] = [(r.uniform(40, 1040), r.uniform(60, 1350), r.uniform(10, 24), r.uniform(0, 6.28)) for _ in range(40)
                      if True]
        G["stars"] = [s for s in G["stars"] if not (300 < s[0] < 780 and 380 < s[1] < 900)]
        fn = twinkle_frame
    if len(sys.argv) > 2 and sys.argv[2] == "frames":
        for t in (0.0, total * 0.25, total * 0.5, total * 0.62, total * 0.9):
            fn(G, t).save(tmp / f"f{t:05.2f}.png")
        print("frames", tmp)
        return
    build_audio(song, style, tmp / "a.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp / "v.mp4")],
                         stdin=subprocess.PIPE)
    for f in range(int(round(total * FPS))):
        p.stdin.write(fn(G, f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    out = ROOT / "VIDEOS" / name[0] / f"{name[1]} {os.environ.get('VER', 'v1')}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "v.mp4"), "-i", str(tmp / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    build(sys.argv[1])
