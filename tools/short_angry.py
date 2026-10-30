"""Short S18: I'M ANGRY! Gul's block tower crashes (hook at 0:00), his face goes angry and red with steam, Mishu helps him
breathe in and out, he calms down, the blocks fly back up, "We did it!".   python tools/short_angry.py frames|video
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
sys.path.insert(0, str(ROOT / "characters"))
from expressions import EMOTIONS

A, M, LS, R, SR = RS.A, RS.M, RS.LS, RS.R, RS.SR
W, H, FPS = 1080, 1920, 30
INK = RS.INK
KIT = ROOT / "characters" / "layers"
OUTFIT = {"gul": "bluetee", "misheal": "yellow"}
TMP = ROOT / "tools" / "_angry"
TMP.mkdir(exist_ok=True)
FLOOR = 1640
BLOCK = 150
COLS = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
TOWER_X = 560
CRASH = 0.5
CLOSE1 = (0.9, 3.0)        # angry close-up
TWO = (3.0, 6.9)           # two-shot, Mishu talks
BREATH = (6.9, 11.4)       # breathing close-up
IN_T, OUT_T = 7.0, 9.0
REBUILD = 13.0
YAY = 16.6
END = 18.8
TOTAL = 21.6

LINES = [("gul", "Grrr! I'm angry!", 1.0, 1.7), ("mishu", "It's okay to feel angry.", 3.2, 1.7), ("mishu", "Let's take a big breath!", 5.1, 1.6),
         ("both", "Breathe in...", IN_T + 0.1, 1.5), ("both", "Breathe out...", OUT_T + 0.1, 1.5), ("gul", "Ahh. I feel calm now.", 11.5, 1.5),
         ("gul", "Let's build it again!", 13.1, 1.5), ("both", "We did it! Yay!", YAY + 0.1, 1.6), ("mishu", "When you're angry, breathe!", END + 0.3, 2.0)]


# ------------------------------------------------------------------ audio
rng = np.random.default_rng(18)


def clack():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 380 * t) * 0.6 + np.sin(2 * np.pi * 900 * t) * 0.3) * np.exp(-t / 0.025) + rng.standard_normal(n) * np.exp(-t / 0.006) * 0.4


def crash():
    out = np.zeros(int(1.2 * SR))
    for k in range(6):
        c = clack() * rng.uniform(0.6, 1.0)
        i = int((0.05 + k * 0.11 + rng.uniform(0, 0.05)) * SR)
        out[i:i + len(c)] += c
    t = np.arange(len(out)) / SR
    return out + np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.2) * 0.8


def breath(d, lp):
    n = int(d * SR)
    x = np.convolve(rng.standard_normal(n), np.ones(lp) / lp, mode="same")
    return x * np.sin(np.linspace(0, np.pi, n)) * 2.0


def audio(path):
    n = int(TOTAL * SR)
    v = np.zeros((n, 2))
    for who, text, t, slot in LINES:
        for w, g, pan in ((("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)) if who == "both" else ((who, 1.0, -0.1 if who == "gul" else 0.1),)):
            A.add(v, RS.chant(w, text, slot), t, g, pan)
    RS.CHORD.setdefault("Am", [57, 60, 64])
    beat = 0.47
    song = {"chords": ["F", "G", "C", "Am"]}
    tune = [72, 74, 76, 79, 76, 74, 72, 0, 74, 76, 77, 79, 81, 79, 76, 0]
    toks = [dict(t=i * beat, dur=beat, notes=[tune[i % 16]]) for i in range(int(TOTAL / beat)) if tune[i % 16]]
    m = RV.exciting_music(song, toks, TOTAL, beat)
    g = np.ones(n)                                            # music almost silent while breathing, back up when calm
    g[int(BREATH[0] * SR):int(BREATH[1] * SR)] = 0.12
    g = np.convolve(g, np.ones(SR // 2) / (SR // 2), mode="same")
    m *= g[:, None]
    fx = np.zeros_like(m)
    A.add(fx, crash(), CRASH, 1.0)
    for k in range(3):
        A.add(fx, M.stomp(), TWO[0] + 0.2 + k * 0.4, 0.6)
    A.add(fx, breath(1.8, 25), IN_T, 0.5)
    A.add(fx, breath(1.8, 8), OUT_T, 0.4)
    for k in range(6):
        A.add(fx, clack(), REBUILD + 0.4 + k * 0.42, 0.7)
    A.add(fx, A.sfx_sparkle(), YAY, 0.6)
    for k in range(4):
        A.add(fx, M.clap(), YAY + 0.2 + k * 0.25, 0.4)
    A.add(fx, A.sfx_ding(84), END + 0.3, 0.3)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    m = m / np.abs(m).max() * (1 - 0.35 * e)[:, None]
    LS.finish_audio(v + m * 0.5 + fx * 0.6, path)


# ------------------------------------------------------------------ pictures
def make_bg():
    y = np.linspace(0, 1, H)[:, None, None]
    wall = np.array([255, 233, 214], float) * (1 - 0.15 * y) + np.array([255, 245, 235], float) * 0.15 * y
    img = Image.fromarray(np.repeat(np.clip(wall, 0, 255).astype(np.uint8), W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for x in range(0, W, 120):
        d.rectangle((x, 0, x + 60, FLOOR - 120), fill=(255, 222, 200))
    d.rectangle((0, FLOOR - 120, W, H), fill=(201, 147, 95))
    d.rectangle((0, FLOOR - 130, W, FLOOR - 112), fill=(255, 255, 255), outline=INK, width=5)
    d.ellipse((60, FLOOR - 40, W - 60, FLOOR + 140), fill=(255, 179, 138))
    d.rounded_rectangle((700, 330, 1000, 640), radius=18, fill=(158, 216, 255), outline=INK, width=8)
    d.line((850, 330, 850, 640), fill=INK, width=8)
    d.line((700, 485, 1000, 485), fill=INK, width=8)
    d.rectangle((90, 520, 400, 545), fill=(192, 138, 85), outline=INK, width=5)
    for i, c in enumerate(COLS):
        d.rounded_rectangle((105 + i * 48, 440, 145 + i * 48, 518), radius=6, fill=c, outline=INK, width=4)
    return img


def block_img(i):
    im = Image.new("RGBA", (BLOCK, BLOCK), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = COLS[i % 6]
    d.rounded_rectangle((3, 3, BLOCK - 3, BLOCK - 3), radius=16, fill=c, outline=INK, width=7)
    d.rounded_rectangle((22, 22, BLOCK - 22, BLOCK - 22), radius=10, fill=tuple(min(255, v + 40) for v in c))
    R.G["fonts"] = R.G.get("fonts", {})
    f = R.font(80)
    ch = "ABCDEF"[i % 6]
    tw = d.textlength(ch, font=f)
    d.text((BLOCK / 2 - tw / 2, BLOCK / 2 - 52), ch, font=f, fill=(255, 255, 255), stroke_width=6, stroke_fill=INK)
    return im


def compose(n, emo, talk_open, wave=False):
    L = KIT / n
    o = OUTFIT[n]
    key = (n, emo, talk_open, wave)
    if key in G["cache"]:
        return G["cache"][key]
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    girl = n == "misheal"
    if emo:
        eyes, brw, mouth, ovs = EMOTIONS[emo]
        mouth_l = f"x_mouth_{mouth}"
    else:
        eyes, brw, ovs = "eyes_open", None, []
        mouth_l = "mouth_open" if talk_open else "mouth_smile"
    for p in (["hair_back"] if girl else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_{'wave' if wave else 'down'}_{o}", "neck", "head", eyes]:
        im.alpha_composite(G["L"][(n, p)] if (n, p) in G["L"] else G["L"].setdefault((n, p), Image.open(L / f"{p}.png").convert("RGBA")))
    def lay(p):
        return G["L"].setdefault((n, p), Image.open(L / f"{p}.png").convert("RGBA"))
    if "lids" in ovs:
        im.alpha_composite(lay("x_over_lids"))
    im.alpha_composite(lay(f"x_brows_{brw}" if brw else "brows"))
    im.alpha_composite(lay(mouth_l))
    im.alpha_composite(lay("hair_front"))
    if girl:
        im.alpha_composite(lay("earrings"))
    for ov in ovs:
        if ov != "lids":
            im.alpha_composite(lay(f"x_over_{ov}"))
    if len(G["cache"]) > 60:
        G["cache"].clear()
    G["cache"][key] = im
    return im


def speaking(who, t):
    for w, text, t0, slot in LINES:
        if (w == who or w == "both") and t0 <= t < t0 + slot * 0.9:
            return ((t - t0) * 7) % 1 < 0.55
    return False


def tint(im, rgb, a):
    if a <= 0:
        return im
    over = Image.new("RGBA", im.size, rgb + (int(255 * a),))
    m = im.getchannel("A")
    out = im.copy()
    over.putalpha(Image.fromarray((np.array(m).astype(float) * a).astype(np.uint8)))
    out.alpha_composite(over)
    return out


def steam(frame, cx, cy, t, s=1.0):
    d = ImageDraw.Draw(frame, "RGBA")
    for side in (-1, 1):
        for j in range(4):
            p = (t * 1.6 + j / 4) % 1
            r = (30 + 50 * p) * s
            x = cx + side * (330 + 120 * p) * s
            y = cy - 60 * s - 260 * p * s
            d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 250, 255, int(230 * (1 - p))))


def face_close(frame, n, emo, t, cy=900, scale=1.15, shake=0.0, red=0.0):
    im = compose(n, emo, speaking("gul" if n == "gul" else "mishu", t))
    crop = im.crop((150, 100, 1050, 1000))
    crop = tint(crop, (255, 40, 40), red)
    crop = crop.resize((int(900 * scale), int(900 * scale)), Image.BICUBIC)
    frame.alpha_composite(crop, (int(540 - crop.width / 2 + shake), int(cy - crop.height / 2 + 6 * math.sin(t * 2))))


def full(frame, n, emo, x, t, scale=0.42, hop=0.0, red=0.0, wave=False, rot=0.0):
    im = compose(n, emo, speaking("gul" if n == "gul" else "mishu", t), wave)
    if red:
        im = tint(im, (255, 40, 40), red)
    sm = im.resize((int(1200 * scale), int(2000 * scale)), Image.BICUBIC)
    if rot:
        sm = sm.rotate(rot, center=(sm.width / 2, sm.height), resample=Image.BICUBIC)
    frame.alpha_composite(sm, (int(x - sm.width / 2), int(FLOOR + 120 - sm.height * 0.93 - hop)))


def tower_pos(i):
    return TOWER_X, FLOOR - BLOCK / 2 - i * (BLOCK - 6)


SCATTER = [(330, FLOOR + 30, 40), (760, FLOOR + 60, -25), (470, FLOOR + 90, 15), (900, FLOOR + 20, 70), (640, FLOOR + 110, -60), (220, FLOOR + 100, 30)]


def blocks(frame, t):
    n = 6
    for i in range(n):
        tx, ty = tower_pos(i)
        if t < CRASH:
            wob = 6 * math.sin(t * 40) * (i / n) * (t / CRASH)
            x, y, r = tx + wob * i, ty, wob
        elif t < REBUILD + 0.4 + i * 0.42:
            k = min(1, (t - CRASH - i * 0.04) / 0.55)
            k = max(0, k)
            sx, sy, sr = SCATTER[i]
            x = tx + (sx - tx) * k
            y = ty + (sy - ty) * (k * k) - 120 * math.sin(math.pi * k) * (i / n)
            r = sr * k
        else:
            k = min(1, (t - (REBUILD + 0.4 + i * 0.42)) / 0.35)
            sx, sy, sr = SCATTER[i]
            e = R.ease_back(k)
            x = sx + (tx - sx) * e
            y = sy + (ty - sy) * e - 200 * math.sin(math.pi * k)
            r = sr * (1 - k)
        b = G["blocks"][i].rotate(r, resample=Image.BICUBIC, expand=True) if r else G["blocks"][i]
        frame.alpha_composite(b, (int(x - b.width / 2), int(y - b.height / 2)))


def text(frame, s, t, t0, y=230, size=170, col=None):
    R.rainbow_text(frame, W / 2, y, s, int(size * R.ease_back((t - t0) / 0.25)), colour=col, maxw=1000)


def frame_at(t):
    fr = G["bg"].copy()
    if t < CLOSE1[0]:
        blocks(fr, t)
        full(fr, "gul", None if t < CRASH else "surprised", 200, t)
        text(fr, "CRASH!" if t >= CRASH else "", t, CRASH, size=200, col=(255, 77, 109)) if t >= CRASH else None
    elif t < CLOSE1[1]:
        q = t - CLOSE1[0]
        sh = 14 * math.sin(t * 55) * max(0.3, 1 - q / 1.5)
        face_close(fr, "gul", "angry", t, shake=sh, red=min(0.28, q * 0.4))
        steam(fr, 540, 820, t)
        text(fr, "ANGRY!", t, CLOSE1[0], size=210, col=(240, 60, 60))
    elif t < TWO[1]:
        blocks(fr, t)
        q = t - TWO[0]
        st = 26 * abs(math.sin(q * 7.8)) if q < 1.4 else 0
        full(fr, "gul", "angry", 250, t, hop=st)
        steam(fr, 250, 950, t, 0.5)
        full(fr, "misheal", None, 830, t, wave=True)
        text(fr, "IT'S OKAY!", t, LINES[1][2], size=170, col=(46, 168, 255))
    elif t < BREATH[1]:
        ph_in = IN_T <= t < OUT_T
        ph_out = t >= OUT_T
        if t < OUT_T + 0.8:
            emo, red = "angry", max(0, 0.25 - (t - BREATH[0]) * 0.08)
        else:
            emo, red = "calm", 0
        d = ImageDraw.Draw(fr, "RGBA")
        if ph_in:
            k = min(1, (t - IN_T) / 1.8)
        elif ph_out:
            k = 1 - min(1, (t - OUT_T) / 1.8)
        else:
            k = 0
        r = 330 + 230 * R.ease_io(k)
        d.ellipse((540 - r, 900 - r, 540 + r, 900 + r), fill=(120, 210, 230, 70), outline=(80, 190, 210, 220), width=14)
        face_close(fr, "gul", emo, t, scale=0.95 + 0.1 * R.ease_io(k), red=red)
        if t < IN_T:
            text(fr, "BIG BREATH!", t, BREATH[0], size=160, col=(80, 190, 210))
        else:
            text(fr, "BREATHE IN..." if ph_in else "BREATHE OUT...", t, IN_T if ph_in else OUT_T, size=130, col=(80, 190, 210))
        d2 = ImageDraw.Draw(fr)
        f = R.font(64)
        for j, lab in enumerate(("YOUR TURN!",)):
            w = d2.textlength(lab, font=f)
            d2.rounded_rectangle((540 - w / 2 - 40, 1560, 540 + w / 2 + 40, 1670), radius=55, fill=(255, 255, 255), outline=INK, width=6)
            d2.text((540 - w / 2, 1575), lab, font=f, fill=(255, 77, 109), stroke_width=4, stroke_fill=(255, 255, 255))
    else:
        blocks(fr, t)
        happy = t >= YAY
        hop = 50 * abs(math.sin((t - YAY) * 5)) if happy else 0
        full(fr, "gul", "excited" if happy else "calm" if t < REBUILD else "happy", 230, t, hop=hop, wave=happy)
        full(fr, "misheal", "happy" if happy else None, 860, t, hop=hop * 0.8, wave=True)
        if t >= END:
            d = ImageDraw.Draw(fr, "RGBA")
            d.rounded_rectangle((70, 140, 1010, 520), radius=50, fill=(255, 255, 255, 225), outline=INK, width=8)
            R.rainbow_text(fr, W / 2, 250, "WHEN YOU'RE ANGRY,", int(80 * R.ease_back((t - END) / 0.3)), maxw=880)
            R.rainbow_text(fr, W / 2, 400, "BREATHE!", int(170 * R.ease_back((t - END - 0.4) / 0.3)), colour=(80, 190, 210), maxw=880)
        elif happy:
            text(fr, "WE DID IT!", t, YAY, size=180)
            d = ImageDraw.Draw(fr)
            for x0, y0, sp, ph, col in G["confetti"]:
                y = y0 + (t - YAY) * sp
                if -30 < y < H:
                    x = x0 + 40 * math.sin(t * 2 + ph)
                    w = 22 * abs(math.cos(t * 5 + ph)) + 4
                    d.rectangle((x - w / 2, y - 12, x + w / 2, y + 12), fill=col)
        elif t >= REBUILD:
            text(fr, "TRY AGAIN!", t, REBUILD, size=170, col=(59, 193, 74))
        else:
            text(fr, "CALM!", t, BREATH[1], size=190, col=(80, 190, 210))
    return fr.convert("RGB")


G = {}


def load():
    R.G["fonts"] = {}
    G.update(bg=make_bg(), blocks=[block_img(i) for i in range(6)], cache={}, L={})
    rng2 = np.random.default_rng(3)
    G["confetti"] = [(rng2.uniform(0, W), rng2.uniform(-H, 0), rng2.uniform(500, 900), rng2.uniform(0, 6.28), R.RAINBOW[int(rng2.integers(6))]) for _ in range(110)]


def main():
    load()
    if _argv and _argv[0] == "frames":
        ts = [float(x) for x in _argv[1].split(",")] if len(_argv) > 1 else [0.0, 0.6, 1.5, 4.0, 6.0, 8.0, 10.0, 12.0, 14.5, 17.2, 20.0]
        sheet = Image.new("RGB", (270 * 6, 480 * ((len(ts) + 5) // 6)))
        for i, t in enumerate(ts):
            sheet.paste(frame_at(t).resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        sheet.save(TMP / "_sheet.png")
        print("sheet", TMP / "_sheet.png")
        return
    audio(TMP / "a.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(TMP / "v.mp4")],
                         stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)):
        p.stdin.write(frame_at(f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    out = ROOT / "VIDEOS" / "S18 Im Angry" / f"I'm Angry - Short {os.environ.get('VER', 'v1')}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "v.mp4"), "-i", str(TMP / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
