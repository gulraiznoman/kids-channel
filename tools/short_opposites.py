"""Short: OPPOSITES (big/small, hot/cold, fast/slow, day/night). Gul & Mishu talk over exciting kids music.
Hook at 0:00: the elephant slams in with BIG! and a drum hit.  python tools/short_opposites.py [frames]
"""
import math, os, subprocess, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
_argv = sys.argv[1:]
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(ROOT / "tools"))
import rhyme_shorts as RS
import rhyme_v4 as RV

A, M, LS, R, SR = RS.A, RS.M, RS.LS, RS.R, RS.SR
W, H, FPS = 1080, 1920, 30
ART = ROOT / "long01-animals-fun" / "art"
PAIRS = [  # word A, art A, colour A, word B, art B, colour B, summary
    ("BIG", ART / "fruit_elephant.png", (255, 200, 120), "SMALL", ART / "fruit_chick.png", (255, 240, 170), "Big and small!"),
    ("HOT", ART / "fruit_sunny.png", (255, 150, 90), "COLD", ART / "fruit_snowy.png", (170, 220, 255), "Hot and cold!"),
    ("FAST", ART / "fruit_car.png", (255, 120, 140), "SLOW", ART / "fruit_turtle.png", (170, 235, 170), "Fast and slow!"),
    ("DAY", ART / "fruit_sunny.png", (130, 200, 255), "NIGHT", ROOT / "long04-good-habits/art/item_moon.png", (70, 70, 150), "Day and night!"),
]
SEG = 5.0
INTRO = 0.0
TOTAL = SEG * len(PAIRS) + 2.0         # + outro "Opposites!"


def plan():
    lines = []
    for i, (a, _, _, b, _, _, summ) in enumerate(PAIRS):
        t0 = i * SEG
        lines += [("mishu", a.title() + "!", t0 + 0.05, 1.3), ("gul", b.title() + "!", t0 + 1.7, 1.3), ("both", summ, t0 + 3.3, 1.5)]
    lines.append(("both", "Opposites! Yay!", SEG * len(PAIRS) + 0.1, 1.7))
    return lines


def audio(path):
    lines = plan()
    n = int(TOTAL * SR)
    v = np.zeros((n, 2))
    for who, text, t, slot in lines:
        for w, g, pan in ((("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)) if who == "both" else ((who, 1.0, 0.0),)):
            A.add(v, RS.chant(w, text, slot), t, g, pan)
    beat = 0.5
    song = {"chords": ["C", "F", "G", "C"]}
    tune = [72, 76, 79, 76, 77, 74, 72, 0, 74, 77, 79, 81, 79, 76, 74, 0]
    toks = [dict(t=i * beat, dur=beat, notes=[tune[i % 16]]) for i in range(int(TOTAL / beat)) if tune[i % 16]]
    m = RV.exciting_music(song, toks, TOTAL, beat)
    fx = np.zeros_like(m)
    for i in range(len(PAIRS)):
        A.add(fx, LS.kick() * 1.2, i * SEG, 0.9)               # slam on A
        A.add(fx, A.sfx_whoosh(), i * SEG, 0.4)
        A.add(fx, A.sfx_pop(), i * SEG + 1.65, 0.5)            # pop on B
        A.add(fx, A.sfx_sparkle(), i * SEG + 3.3, 0.3)
    A.add(fx, A.sfx_sparkle(), SEG * len(PAIRS), 0.5)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    m = m / np.abs(m).max() * (1 - 0.35 * e)[:, None]
    LS.finish_audio(v + m * 0.6 + fx * 0.5, path)


def panel_bg(c1, c2):
    y = np.linspace(0, 1, H)[:, None, None]
    top = np.array(c1, float)
    bot = np.array(c2, float)
    img = np.where(y < 0.5, top * (1 - y) + 255 * y * 0.3, bot * (0.7 + 0.3 * y))
    return Image.fromarray(np.repeat(np.clip(img, 0, 255).astype(np.uint8), W, axis=1)).convert("RGBA")


def frame(G, t):
    i = min(len(PAIRS) - 1, int(t // SEG))
    u = t - i * SEG
    a, _, ca, b, _, cb, summ = PAIRS[i]
    if t >= SEG * len(PAIRS):                                    # outro: all pairs small, "OPPOSITES!"
        fr = G["bgs"][0].copy()
        q = t - SEG * len(PAIRS)
        for j in range(len(PAIRS)):
            LS.paste(fr, G["imgA"][j], 300, 520 + j * 250 - 15 * abs(math.sin(t * 5 + j)), scale=0.42)
            LS.paste(fr, G["imgB"][j], 780, 520 + j * 250 - 15 * abs(math.sin(t * 5 + j + 1)), scale=0.42)
        R.rainbow_text(fr, W / 2, 230, "OPPOSITES!", int(170 * R.ease_back(q / 0.3)), maxw=1000)
    else:
        fr = G["bgs"][i].copy()
        d = ImageDraw.Draw(fr)
        d.rectangle((0, 948, W, 972), fill=(255, 255, 255))
        # A slams in (hook), B pops in
        ka = R.ease_back(u / 0.35)
        sq = 1 + 0.15 * max(0, 1 - u / 0.25)
        if a == "FAST":
            xa = 540 + (1 - min(1, u / 0.35)) * 900
        else:
            xa = 540
        bob = 12 * math.sin(t * 6)
        LS.paste(fr, G["imgA"][i], xa, 540 + bob, scale=ka, sx=sq, sy=2 - sq)
        R.rainbow_text(fr, W / 2, 150, a + "!", int(170 * R.ease_back(u / 0.25)), maxw=1000)
        if u >= 1.65:
            kb = R.ease_back((u - 1.65) / 0.35)
            xb = 540 + (60 * math.sin((u - 1.65) * 1.2) if b == "SLOW" else 0)
            LS.paste(fr, G["imgB"][i], xb, 1330 + bob * 0.5, scale=kb)
            R.rainbow_text(fr, W / 2, 1060, b + "!", int(150 * R.ease_back((u - 1.65) / 0.25)), maxw=1000)
        if u >= 3.3:
            R.plain_text(fr, W / 2, 900, summ.upper(), 70, fill=(255, 255, 255))
    for name, outfit, x, off in (("gul", "tee", 150, 0.0), ("misheal", "yellow", 930, 0.5)):
        im = LS.character(name, outfit, mouth="open" if ((t * 2 + off) % 1) < 0.5 else "smile", wave=18 * math.sin(t * 6.28 + off * 3))
        LS.paste(fr, im, x, 1910 - 25 * abs(math.sin((t * 2 + off) * math.pi)), scale=0.27, bottom=True)
    return fr.convert("RGB")


def main():
    R.G["fonts"] = {}
    if not hasattr(R, "plain_text"):
        def plain_text(img, cx, cy, text, size, fill=(255, 255, 255)):
            d = ImageDraw.Draw(img)
            f = R.font(size)
            w = d.textlength(text, font=f)
            d.text((cx - w / 2, cy - size * 0.62), text, font=f, fill=fill, stroke_width=int(size * 0.13), stroke_fill=RS.INK)
        R.plain_text = plain_text
    G = {"bgs": [panel_bg(p[2], p[5]) for p in PAIRS],
         "imgA": [LS.load(p[1], 640) for p in PAIRS], "imgB": [LS.load(p[4], 640) for p in PAIRS]}
    G["imgB"][0] = LS.load(PAIRS[0][4], 240)                     # the chick is SMALL
    G["imgA"][0] = LS.load(PAIRS[0][1], 760)                     # the elephant is BIG
    tmp = ROOT / "tools" / "_opp"
    tmp.mkdir(exist_ok=True)
    if _argv and _argv[0] == "frames":
        for t in (0.15, 2.5, 4.0, 6.0, 12.0, 17.5, 21.0):
            frame(G, t).save(tmp / f"f{t:05.2f}.png")
        print("frames", tmp)
        return
    audio(tmp / "a.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp / "v.mp4")],
                         stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)):
        p.stdin.write(frame(G, f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    out = ROOT / "VIDEOS" / "S16 Opposites" / f"Opposites - Short {os.environ.get('VER', 'v1')}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "v.mp4"), "-i", str(tmp / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
