"""Short 03: Surprise Box (10 s, seamless loop). A gift box wiggles, pops open, a puppy springs out with a real bark,
Gul and Mishu react, the puppy hops back in and the lid closes (last frame == first frame).

python make.py frames 0,70,110,200   -> preview PNGs
python make.py video                 -> VIDEOS/S03 Surprise Box/Surprise Box - Short v1.mp4
Settings for the next animal: ANIMAL, LABEL, LINES, SOUND below.
"""
import math, os, pathlib, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "voices"))
KIT = ROOT / "characters" / "layers"
ART = ROOT / "long01-animals-fun" / "art"
OUT = ROOT / "VIDEOS" / "S03 Surprise Box"
VER = os.environ.get("VER", "v2")

W, H, FPS, DUR = 1080, 1920, 30, 10.0
N = int(DUR * FPS)
INK = (58, 36, 32)
FONT = "C:/Windows/Fonts/seguibl.ttf"

ANIMAL, LABEL, SOUND = "puppy", "PUPPY!", "puppy"
# (time s, who, text)
LINES = [(0.25, "mishu", "What's inside?"), (3.5, "gul", "Yay!"), (3.55, "mishu", "Yay!"),
         (4.5, "gul", "A puppy!"), (5.7, "mishu", "Hello, puppy!"), (7.25, "gul", "Wow, a flip!")]
T_PEEK0, T_PEEK1 = 1.35, 2.0          # lid lifts a little, eyes peek out, lid slams back
T_POP, T_OUT, T_LAND = 2.45, 2.6, 3.15  # lid flies off, puppy spins out, lands on the box
T_BARK = 3.25
T_FLIP0, T_FLIP1 = 6.85, 7.55         # backflip
T_DIVE = 8.2                          # dives back in (0.6 s)
T_CLOSE = 9.35                        # lid lands, still until the loop restarts

BOX_CX, BOX_TOP, BOX_W, BOX_H = 540, 815, 500, 350
LID_H = 96
PUP_SIZE = 640


def ease_back(x):
    x = min(max(x, 0.0), 1.0)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def ease_in_out(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ assets
def background():
    bg = Image.new("RGBA", (W, H))
    top, bot = np.array([255, 240, 214]), np.array([255, 214, 226])
    g = np.linspace(0, 1, H)[:, None]
    arr = (top * (1 - g) + bot * g).astype(np.uint8)
    bg = Image.fromarray(np.repeat(arr[:, None, :], W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    rnd = np.random.default_rng(3)
    for _ in range(26):                                    # soft confetti dots on the wall
        x, y, r = rnd.uniform(0, W), rnd.uniform(60, 1150), rnd.uniform(10, 20)
        c = [(255, 160, 180), (255, 210, 110), (150, 200, 255), (170, 230, 170), (210, 170, 255)][rnd.integers(5)]
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (150,))
    d.rectangle((0, 1250, W, H), fill=(214, 168, 120))     # wooden floor
    for y in range(1290, H, 90):
        d.line((0, y, W, y), fill=(196, 150, 104), width=4)
    d.ellipse((BOX_CX - 330, BOX_TOP + BOX_H - 40, BOX_CX + 330, BOX_TOP + BOX_H + 70), fill=(120, 190, 255))  # rug
    d.ellipse((BOX_CX - 300, BOX_TOP + BOX_H - 30, BOX_CX + 300, BOX_TOP + BOX_H + 60), fill=(150, 210, 255))
    return bg


def draw_box():
    """Box body (RGBA) and lid (RGBA), drawn at 2x then downsampled."""
    s = 2
    body = Image.new("RGBA", ((BOX_W + 20) * s, (BOX_H + 20) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    d.rounded_rectangle((10 * s, 10 * s, (BOX_W + 10) * s, (BOX_H + 10) * s), radius=22 * s, fill=(232, 60, 80), outline=INK, width=8 * s)
    cx = (BOX_W + 20) * s // 2
    d.rectangle((cx - 34 * s, 14 * s, cx + 34 * s, (BOX_H + 6) * s), fill=(255, 205, 60))
    d.line((cx - 34 * s, 14 * s, cx - 34 * s, (BOX_H + 6) * s), fill=INK, width=5 * s)
    d.line((cx + 34 * s, 14 * s, cx + 34 * s, (BOX_H + 6) * s), fill=INK, width=5 * s)
    for k in range(5):                                     # polka dots
        for j in range(3):
            x, y = (60 + k * 82) * s, (70 + j * 85) * s
            if abs(x - cx) > 60 * s:
                d.ellipse((x - 13 * s, y - 13 * s, x + 13 * s, y + 13 * s), fill=(255, 255, 255, 200))
    body = body.resize((BOX_W + 20, BOX_H + 20), Image.LANCZOS)
    lw = BOX_W + 50
    lid = Image.new("RGBA", ((lw + 20) * s, (LID_H + 150) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lid)
    by = 120 * s
    d.rounded_rectangle((10 * s, by, (lw + 10) * s, by + LID_H * s), radius=18 * s, fill=(240, 72, 92), outline=INK, width=8 * s)
    cx = (lw + 20) * s // 2
    d.rectangle((cx - 34 * s, by + 4 * s, cx + 34 * s, by + (LID_H - 4) * s), fill=(255, 205, 60))
    for side in (-1, 1):                                   # bow loops
        ex = cx + side * 75 * s
        d.ellipse((ex - 70 * s, by - 105 * s, ex + 70 * s, by + 5 * s), fill=(255, 205, 60), outline=INK, width=7 * s)
        d.ellipse((ex - 34 * s, by - 72 * s, ex + 34 * s, by - 26 * s), fill=(240, 170, 30))
    d.ellipse((cx - 36 * s, by - 50 * s, cx + 36 * s, by + 14 * s), fill=(255, 205, 60), outline=INK, width=7 * s)
    lid = lid.resize((lw + 20, LID_H + 150), Image.LANCZOS)
    return body, lid


def char_layers(name, outfit, S=0.4):
    L = {}
    for p in (KIT / name).glob("*.png"):
        im = Image.open(p)
        L[p.stem] = im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS)
    return L


def compose_char(L, girl, outfit, eyes, mouth, wave_ang=None):
    im = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
    for n in (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}"]:
        im.alpha_composite(L[n])
    if wave_ang is None:
        im.alpha_composite(L[f"arm_r_down_{outfit}"])
    else:
        piv = (388 * 0.8, 526 * 0.8) if girl else (396 * 0.8, 526 * 0.8)
        im.alpha_composite(L[f"arm_r_wave_{outfit}"].rotate(wave_ang, center=piv, resample=Image.BICUBIC))
    for n in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if girl else []):
        im.alpha_composite(L[n])
    return im


def envelope(path):
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop = sr // FPS
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
    return np.clip(rms / (np.percentile(rms, 90) + 1e-6), 0, 1.5)


def font(sz):
    return ImageFont.truetype(FONT, sz)


def rainbow_word(img, cx, cy, text, size):
    d = ImageDraw.Draw(img)
    f = font(size)
    cols = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
    widths = [d.textlength(ch, font=f) for ch in text]
    x = cx - (sum(widths) + 6 * (len(text) - 1)) / 2
    for i, ch in enumerate(text):
        y = cy - size * 0.62
        d.text((x, y), ch, font=f, fill=INK, stroke_width=int(size * 0.13), stroke_fill=INK)
        d.text((x, y), ch, font=f, fill=cols[i % 6], stroke_width=int(size * 0.07), stroke_fill=(255, 255, 255))
        x += widths[i] + 6


def star(d, cx, cy, r, col, rot):
    pts = [(cx + (r if k % 2 == 0 else r * 0.45) * math.cos(rot + k * math.pi / 5 - math.pi / 2),
            cy + (r if k % 2 == 0 else r * 0.45) * math.sin(rot + k * math.pi / 5 - math.pi / 2)) for k in range(10)]
    d.polygon(pts, fill=col, outline=INK, width=4)


# ------------------------------------------------------------------ voices + audio
def make_voices():
    import kidvoice
    vdir = HERE / "voice_v2"
    vdir.mkdir(exist_ok=True)
    out = []
    for i, (t, who, text) in enumerate(LINES):
        p = vdir / f"line{i}.wav"
        if not p.exists():
            raw = vdir / f"line{i}.raw.wav"
            kidvoice.say_as(who, text, raw)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                            "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                            "-ac", "1", "-ar", "48000", str(p)], check=True)
            raw.unlink()
        out.append((t, who, p))
    return out


def tone(f, dur, harm=((1, 1),), a=0.003, d=0.25, sr=48000):
    n = int(dur * sr)
    tt = np.arange(n) / sr
    e = np.exp(-tt / d)
    e[:int(a * sr)] *= np.linspace(0, 1, int(a * sr))
    return sum(amp * np.sin(2 * np.pi * f * k * tt) for k, amp in harm) * e


def build_audio(voices, path):
    sr = 48000
    n = int(DUR * sr)
    mix = np.zeros(n)

    def add(x, t, g):
        i = int(t * sr)
        if i >= n:
            return
        x = x[:n - i]
        mix[i:i + len(x)] += x * g

    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    ar = lambda m_: np.arange(int(m_ * sr)) / sr

    def sweep(f0, f1, dur, decay=0.5):
        tt = ar(dur)
        f = f0 + (f1 - f0) * tt / dur
        return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt / decay) * np.minimum(1, tt / 0.01)

    def boing(t0, g=0.22, base=220):
        tt = ar(0.35)
        fr = base + 160 * np.sin(tt * 2 * np.pi * 10) * np.exp(-tt / 0.15)
        add(np.sin(2 * np.pi * np.cumsum(fr) / sr) * np.exp(-tt / 0.12), t0, g)

    # bouncy music: 120 bpm, 5 bars (C F G Am C) = exactly 10 s, so the loop is seamless
    beat = 0.5
    chords = [[60, 64, 67], [53, 57, 60], [55, 59, 62], [57, 60, 64], [60, 64, 67]]
    uke = ((1, 1), (2, 0.45), (3, 0.25), (4, 0.1))
    mel = [76, 79, 81, 79, 76, 72, 74, 76, 77, 76, 74, 72, 71, 74, 79, 77, 76, 72, 74, 76, 72, 74, 76, 79, 77, 76, 74, 71, 72, 76, 79, 84,
           76, 79, 76, 72, 72, 76, 79, 72]
    for bar, ch in enumerate(chords):
        for k in range(4):
            t0 = (bar * 4 + k) * beat
            for j, m in enumerate(ch):
                add(tone(mtof(m), 0.4, uke, 0.002, 0.12), t0 + j * 0.012, 0.035 * (1 if k % 2 == 0 else 0.7))
            if k in (0, 2):
                add(tone(mtof(ch[0] - 24), 0.45, ((1, 1), (2, 0.5)), 0.003, 0.15), t0, 0.16)
            nz = np.random.default_rng(bar * 4 + k).standard_normal(int(0.04 * sr)) * np.exp(-ar(0.04) / 0.01)
            add(np.diff(np.concatenate([[0], nz])), t0 + beat / 2, 0.05)          # shaker off-beat
        for k in range(8):
            add(tone(mtof(mel[(bar * 8 + k) % len(mel)]), 0.5, ((1, 1), (4, 0.2), (10, 0.04)), 0.002, 0.18), (bar * 8 + k) * beat / 2, 0.045)
    # box hops (small thumps), peekaboo creak + blink bloop + thud, rattle
    for t0 in np.arange(0.45, T_PEEK0, 0.5):
        add(tone(140, 0.15, ((1, 1), (2, 0.3)), 0.001, 0.04), t0, 0.25)
    add(sweep(300, 700, 0.25, 0.2), T_PEEK0, 0.12)
    add(sweep(900, 1300, 0.08, 0.05), T_PEEK0 + 0.32, 0.12)
    add(tone(120, 0.25, ((1, 1), (2, 0.4)), 0.001, 0.06), T_PEEK1 - 0.05, 0.5)
    rng = np.random.default_rng(1)
    for t0 in np.arange(T_PEEK1 + 0.05, T_POP - 0.02, 0.07):
        nz = rng.standard_normal(int(0.05 * sr)) * np.exp(-ar(0.05) / 0.012)
        add(np.convolve(nz, np.ones(10) / 10, "same"), t0, 0.22)
    # POP + slide whistle up + sparkles
    add(sweep(300, 1400, 0.2, 0.07), T_POP, 0.45)
    add(sweep(500, 1700, 0.55, 0.6), T_POP + 0.02, 0.16)
    for k, mm in enumerate([84, 88, 91, 96, 100]):
        add(tone(mtof(mm), 0.7, ((1, 1), (2.01, 0.3)), 0.002, 0.25), T_POP + 0.12 + k * 0.06, 0.12)
    boing(T_OUT, 0.22)
    add(tone(90, 0.2, ((1, 1),), 0.001, 0.05), T_LAND, 0.4)                     # plop on landing
    for k, mm in enumerate([79, 83, 86]):                                         # hearts chime
        add(tone(mtof(mm), 0.6, ((1, 1), (2, 0.3)), 0.002, 0.25), T_LAND + 0.25 + k * 0.08, 0.10)
    # real bark (Mixkit, sfxFree)
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / "stock" / "sounds" / f"{SOUND}.mp3"), "-ac", "1",
                          "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    bark = np.frombuffer(raw, np.float32)
    add(bark / max(1e-9, np.abs(bark).max()), T_BARK, 0.55)
    # backflip: whistle up, boing on landing
    add(sweep(450, 1500, 0.6, 0.6), T_FLIP0, 0.13)
    boing(T_FLIP1, 0.22, 260)
    # dive: whistle down + plop; lid thump
    add(sweep(1500, 350, 0.55, 0.6), T_DIVE, 0.14)
    add(tone(80, 0.25, ((1, 1), (2, 0.3)), 0.001, 0.07), T_DIVE + 0.58, 0.45)
    add(tone(110, 0.25, ((1, 1), (2, 0.4)), 0.001, 0.06), T_CLOSE, 0.5)
    for t, who, p in voices:
        with wave.open(str(p)) as w:
            v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        add(v / max(1e-9, np.abs(v).max()), t, 0.8)
    fade = np.ones(n)
    fade[:int(0.03 * sr)] = np.linspace(0, 1, int(0.03 * sr))
    fade[-int(0.03 * sr):] = np.linspace(1, 0, int(0.03 * sr))
    mix *= fade
    mix /= max(1e-9, np.abs(mix).max()) / 0.9
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((mix * 32767).astype("<i2").tobytes())


# ------------------------------------------------------------------ frames
class Scene:
    def __init__(self, voices):
        self.bg = background()
        self.body, self.lid = draw_box()
        pup = Image.open(ART / f"fruit_{ANIMAL}.png")
        self.pup = pup.resize((PUP_SIZE, PUP_SIZE), Image.LANCZOS)
        self.g = char_layers("gul", "tee")
        self.m = char_layers("misheal", "yellow")
        self.voice = [(t, who, envelope(p)) for t, who, p in voices]

    def mouth(self, who, t):
        for t0, w, env in self.voice:
            if w == who and t0 <= t < t0 + len(env) / FPS:
                v = env[min(int((t - t0) * FPS), len(env) - 1)]
                return "closed" if v < 0.15 else ("o" if v < 0.55 else "open"), True
        return None, False

    def frame(self, f):
        t = f / FPS
        im = self.bg.copy()
        d = ImageDraw.Draw(im)
        # --- box shake: grows towards the pop; tiny idle wobble after the lid closes
        if t < T_POP:
            amp = (3 + 9 * (t / T_POP) ** 1.5) * min(1.0, t / 0.3)      # starts still so the loop joins cleanly
            dx = math.sin(t * 2 * math.pi * 7) * amp
            ang = math.sin(t * 2 * math.pi * 7 + 1) * amp * 0.25
        else:
            dx = ang = 0.0
        # --- puppy: springs up out of the box, wags, hops back in
        out = 0.0
        if T_OUT <= t < T_BACK:
            out = ease_back((t - T_OUT) / 0.5)
        elif T_BACK <= t < T_BACK + 0.55:
            out = 1 - ease_in_out((t - T_BACK) / 0.55)
        if out > 0.01:
            bounce = math.sin(max(0, t - T_OUT - 0.5) * 2 * math.pi * 1.6) * 10 if t < T_BACK else 0
            wag = math.sin(t * 2 * math.pi * 2.2) * 4 if t < T_BACK else 0
            p = self.pup.rotate(wag, resample=Image.BICUBIC)
            py = int(BOX_TOP + 60 - out * 560 + bounce)
            # clip so the puppy stays "inside" the box until it rises above the rim
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            layer.alpha_composite(p, (BOX_CX - PUP_SIZE // 2, py))
            mask = Image.new("L", (W, H), 255)
            ImageDraw.Draw(mask).rectangle((0, BOX_TOP + 40, W, H), fill=0)
            im.paste(layer, (0, 0), Image.composite(layer.split()[3], Image.new("L", (W, H), 0), mask))
        # --- box body
        body = self.body.rotate(ang, resample=Image.BICUBIC, expand=False)
        im.alpha_composite(body, (int(BOX_CX - body.width / 2 + dx), BOX_TOP - 10))
        # --- lid: on the box, flies up & spins at the pop, falls back after the puppy goes in
        lid = self.lid
        lx, ly, lrot = BOX_CX + dx, BOX_TOP - 120 - 10, ang
        if T_POP <= t < T_BACK + 0.4:
            k = min(1.0, (t - T_POP) / 0.55)
            lx = BOX_CX + 420 * ease_in_out(k)
            ly = BOX_TOP - 130 - 380 * math.sin(k * math.pi / 2)
            lrot = -38 * ease_in_out(k) + math.sin(t * 3) * 3
        elif T_BACK + 0.4 <= t < T_CLOSE:
            k = ease_in_out((t - T_BACK - 0.4) / (T_CLOSE - T_BACK - 0.4))
            lx = BOX_CX + 420 * (1 - k)
            ly = BOX_TOP - 130 - 380 * (1 - k) ** 1.3
            lrot = -38 * (1 - k)
        elif T_CLOSE <= t < T_CLOSE + 0.25:                 # little squash bounce on landing
            ly += math.sin((t - T_CLOSE) / 0.25 * math.pi) * -14
        lr = lid.rotate(lrot, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(lr, (int(lx - lr.width / 2), int(ly + lid.height / 2 - lr.height / 2)))
        # --- "?" bubble while shaking
        if 0.25 <= t < T_POP - 0.1:
            sc = ease_back((t - 0.25) / 0.35) * (1 + 0.08 * math.sin(t * 2 * math.pi * 2))
            a = 1
            r = max(1, int(70 * sc))
            bx, by = BOX_CX + 250, BOX_TOP - 200
            d.ellipse((bx - r, by - r, bx + r, by + r), fill=(255, 255, 255, int(255 * a)), outline=INK, width=6)
            f_ = font(int(100 * sc))
            tw = d.textlength("?", font=f_)
            d.text((bx - tw / 2, by - 66 * sc), "?", font=f_, fill=(255, 77, 109), stroke_width=4, stroke_fill=INK)
        # --- pop burst
        k = t - T_POP
        if 0 <= k < 1.0:
            cols = [(255, 77, 109), (255, 159, 28), (255, 210, 63), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
            for j in range(12):
                a_ = j / 12 * 2 * math.pi
                rr = 80 + 420 * ease_in_out(k / 0.8)
                sz = int(30 * (1 - max(0, k - 0.6) / 0.4)) + 1
                star(d, BOX_CX + rr * math.cos(a_), BOX_TOP - 60 + rr * math.sin(a_) * 0.7, sz, cols[j % 6], k * 4)
        # --- word label
        if T_BARK - 0.2 <= t < T_BACK:
            sc = ease_back((t - T_BARK + 0.2) / 0.4)
            if t > T_BACK - 0.3:
                sc *= max(0, (T_BACK - t) / 0.3)
            if sc > 0.05:
                rainbow_word(im, BOX_CX, 210, LABEL, int(180 * sc))
        # --- kids at the bottom, reacting
        for name, L, girl, outfit, x in (("gul", self.g, False, "tee", 250), ("mishu", self.m, True, "yellow", 830)):
            mouth, speaking = self.mouth(name, t)
            if mouth is None:
                mouth = "o" if T_POP <= t < T_OUT + 0.8 else "smile"
            eyes = "closed" if (T_BARK + 0.3 <= t < T_BARK + 1.0) else "open"
            if (name == "gul" and int(t * FPS) % 130 in (40, 41, 42)) or (name == "mishu" and int(t * FPS) % 150 in (90, 91, 92)):
                eyes = "blink" if eyes == "open" else eyes
            wave_ang = None
            if name == "mishu" and 5.75 <= t < 7.4:
                wave_ang = -12 * math.sin((t - 5.75) * 2 * math.pi * 1.6)
            c = compose_char(L, girl, outfit, eyes, mouth, wave_ang)
            hop = -abs(math.sin(t * 2 * math.pi * 1.8)) * 14 if speaking else 0
            if T_OUT <= t < T_OUT + 0.6:
                hop -= math.sin((t - T_OUT) / 0.6 * math.pi) * 40          # surprised jump
            im.alpha_composite(c, (int(x - c.width / 2), int(H - 0.93 * c.height - 10 + hop)))
        return im.convert("RGB")


if __name__ == "__main__":
    voices = make_voices()
    sc = Scene(voices)
    if sys.argv[1] == "frames":
        for f in [int(x) for x in sys.argv[2].split(",")]:
            sc.frame(f).save(HERE / f"_f{f:03d}.png")
        print("ok")
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        wav = HERE / "mix.wav"
        build_audio(voices, wav)
        dst = OUT / f"Surprise Box - Short {VER}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                              "-pix_fmt", "yuv420p", "-af", "volume=6dB,alimiter=limit=0.9", "-ar", "48000", "-c:a", "aac",
                              "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(dst)], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(sc.frame(f).tobytes())
        p.stdin.close()
        p.wait()
        print("wrote", dst)
