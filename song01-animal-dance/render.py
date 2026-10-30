"""Animate the sing-along Short (1080x1920, 30 fps).

python render.py frames 30,200,...  -> preview PNGs
python render.py video              -> "VIDEOS/S01 Animal Dance/Animal Dance - Short.mp4"
"""
import json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
import song

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
KIT = ROOT / "characters" / "layers"
ART = ROOT / "long01-animals-fun" / "art"
OUT = ROOT / "VIDEOS" / "S01 Animal Dance"
W, H, FPS = 1080, 1920, 30
S = 0.31
FONT = "C:/Windows/Fonts/seguibl.ttf"
INK = (58, 36, 32)
RAINBOW = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
B = song.BEAT
CHAR = {
    "gul": dict(outfit="bluetee", x=250, girl=False, pivot=(396, 526), voc="gul"),
    "misheal": dict(outfit="pink", x=830, girl=True, pivot=(388, 526), voc="mishu"),
}
G = {}


def init():
    meta = json.load(open(HERE / "notes.json"))
    G["events"], G["total"] = meta["events"], meta["total"] + 0.5
    G["layers"] = {}
    for n in CHAR:
        d = {}
        for p in (KIT / n).glob("*.png"):
            im = Image.open(p)
            d[p.stem] = im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS)
        G["layers"][n] = d
    bg = Image.open(ART / "bg_farm.png").convert("RGBA")
    k = H / bg.height
    bg = bg.resize((int(bg.width * k), H), Image.LANCZOS)
    x0 = (bg.width - W) // 2
    G["bg"] = bg.crop((x0, 0, x0 + W, H))
    G["art"] = {k: Image.open(ART / f"fruit_{k}.png").convert("RGBA") for k in ("elephant", "bunny", "monkey", "duckling")}
    G["env"] = {}
    for n, c in CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["fonts"], G["cache"], G["rays"] = {}, {}, {}
    rng = np.random.default_rng(4)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(260, 520), rng.uniform(0, 6.28),
                      RAINBOW[int(rng.integers(6))]) for _ in range(90)]


def font(size):
    if size not in G["fonts"]:
        G["fonts"][size] = ImageFont.truetype(FONT, size)
    return G["fonts"][size]


def ease_back(x):
    x = min(max(x, 0.0), 1.0)
    return 1 + 2.70158 * (x - 1) ** 3 + 1.70158 * (x - 1) ** 2


def rainbow_text(img, cx, cy, text, size, start=None, t=0.0, colour=None):
    d = ImageDraw.Draw(img)
    f = font(size)
    widths = [d.textlength(ch, font=f) for ch in text]
    x = cx - (sum(widths) + 6 * (len(text) - 1)) / 2
    for i, ch in enumerate(text):
        dy = 0
        if start is not None:
            k = t - (start + i * 0.06)
            if 0 <= k < 0.3:
                dy = -math.sin(k / 0.3 * math.pi) * size * 0.3
        col = colour or RAINBOW[i % len(RAINBOW)]
        y = cy - size * 0.62 + dy
        d.text((x, y), ch, font=f, fill=INK, stroke_width=int(size * 0.13), stroke_fill=INK)
        d.text((x, y), ch, font=f, fill=col, stroke_width=int(size * 0.07), stroke_fill=(255, 255, 255))
        x += widths[i] + 6


def beat_pos(t):
    return t / B


def compose_char(name, t):
    c, L = CHAR[name], G["layers"][name]
    o = c["outfit"]
    env = G["env"][name]
    v = env[min(int(t * FPS), len(env) - 1)]
    singing = v > 0.12
    mouth = "smile" if not singing else ("o" if v < 0.5 else "open")
    eyes = "closed" if (not singing and int(beat_pos(t)) % 8 == 7 and (beat_pos(t) % 1) < 0.5) else "open"
    key = (name, eyes, mouth)
    if key not in G["cache"]:
        over = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for n in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if c["girl"] else []):
            over.alpha_composite(L[n])
        G["cache"][key] = over
    if (name, "under") not in G["cache"]:
        u = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for n in (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}"]:
            u.alpha_composite(L[n])
        G["cache"][(name, "under")] = u
    im = G["cache"][(name, "under")].copy()
    if t > 0.5:                                    # dance: wave the arm on the beat
        a = L[f"arm_r_wave_{o}"]
        px, py = c["pivot"][0] * 2 * S, c["pivot"][1] * 2 * S
        sw = math.sin(beat_pos(t) * math.pi) * (16 if singing else 9)
        im.alpha_composite(a.rotate(sw, center=(px, py), resample=Image.BICUBIC))
    else:
        im.alpha_composite(L[f"arm_r_down_{o}"])
    im.alpha_composite(G["cache"][key])
    return im


def paste_center(frame, im, cx, cy, size, rot=0.0, sx=1.0, sy=1.0):
    w, h = max(1, int(size * sx)), max(1, int(size * sy))
    a = im.resize((w, h), Image.BICUBIC)
    if rot:
        a = a.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(a, (int(cx - a.width / 2), int(cy - a.height / 2)))


def animal(frame, key, act, t, b0):
    """Animal centre stage, acting out the verse on the beat."""
    lb = beat_pos(t) - b0                          # beats since verse start
    cx, cy, size = W / 2, 900, 660
    rot, sx, sy, dy = 0.0, 1.0, 1.0, 0.0
    side = -1 if (int(b0) // 8) % 2 == 0 else 1
    if lb < 0.9:                                   # fly in with a spin
        k = ease_back(lb / 0.9)
        cx += side * (1 - k) * 900
        rot += (1 - k) * 200 * side
    if lb > 7.5:                                   # whoosh out the other way
        k = (lb - 7.5) / 0.5
        cx -= side * k * k * 1100
        rot -= side * k * 90
    ph = lb % 1
    if lb < 4:                                     # dance during the name lines
        dy = -70 * abs(math.sin(lb * math.pi))
        rot += 12 * math.sin(lb * math.pi)
        sx = sy = 1 + 0.06 * math.cos(lb * 2 * math.pi)
    elif act == "stomp":
        if ph < 0.15:
            sy, sx, dy = 0.86, 1.1, 30
        else:
            dy = -60 * math.sin(min(1, (ph - 0.15) / 0.85) * math.pi)
    elif act == "jump":
        dy = -330 * math.sin(ph * math.pi)
        sy, sx = (0.9, 1.08) if ph > 0.9 or ph < 0.08 else (1.05, 0.96)
        if int(lb) == 6:                           # flip on the last jump
            rot += 360 * min(1, ph / 0.8)
    elif act == "swing":
        rot += 32 * math.sin(lb * math.pi)
        cx += 140 * math.sin(lb * math.pi)
        dy = -40 * abs(math.cos(lb * math.pi))
    elif act == "quack":
        rot += 16 * math.sin(lb * 2 * math.pi)
        cx += 120 * math.sin(lb * math.pi / 2)
        sx = sy = 1 + 0.08 * max(0, math.cos(ph * math.pi * 2))
    paste_center(frame, G["art"][key], cx, cy + dy, size, rot, sx, sy)


def shadow(frame, cx, cy, w):
    sh = Image.new("RGBA", (int(w), int(w * 0.18)), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((0, 0, sh.width - 1, sh.height - 1), fill=(40, 60, 20, 70))
    frame.alpha_composite(sh, (int(cx - w / 2), int(cy)))


RAY_COL = {"stomp": (120, 170, 255), "jump": (255, 150, 200), "swing": (130, 220, 120), "quack": (255, 215, 90)}


def rays(col):
    """Big soft sunburst behind the stage (rotated per frame)."""
    if col not in G["rays"]:
        R = 1500
        c = R / 2
        im = Image.new("RGBA", (R, R), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for k in range(16):
            a0, a1 = k * 2 * math.pi / 16, (k + 0.5) * 2 * math.pi / 16
            d.polygon([(c, c), (c + R * math.cos(a0), c + R * math.sin(a0)), (c + R * math.cos(a1), c + R * math.sin(a1))],
                      fill=col + (110,))
        yy, xx = np.mgrid[0:R, 0:R]
        fade = np.clip(1 - np.hypot(xx - c, yy - c) / c, 0, 1) ** 0.6
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * fade).astype(np.uint8)
        G["rays"][col] = Image.fromarray(a)
    return G["rays"][col]


def draw_rays(frame, col, t, cy, alpha=1.0):
    im = rays(col).rotate(t * 25 % 360, resample=Image.BILINEAR)
    if alpha < 1:
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * alpha).astype(np.uint8)
        im = Image.fromarray(a)
    frame.alpha_composite(im, (int(W / 2 - im.width / 2), int(cy - im.height / 2)))


def clouds(frame, t):
    d = ImageDraw.Draw(frame)
    for i, (y, sp, sc) in enumerate(((170, 38, 1.0), (330, 24, 0.7), (480, 55, 0.85))):
        x = (i * 420 + t * sp) % (W + 400) - 200
        for dx, dy, r in ((0, 0, 55), (55, -25, 65), (115, 0, 55), (55, 15, 50)):
            rr = r * sc
            d.ellipse((x + dx * sc - rr, y + dy * sc - rr, x + dx * sc + rr, y + dy * sc + rr), fill=(255, 255, 255, 235))


def burst(frame, cx, cy, k, seed):
    """Star burst; k runs 0..1 after the hit."""
    if not 0 <= k < 1:
        return
    d = ImageDraw.Draw(frame)
    for j in range(10):
        a = seed * 1.3 + j * 2 * math.pi / 10
        r = 120 + 380 * (1 - (1 - k) ** 2)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * 0.85
        sz = 34 * (1 - k) + 6
        pts = []
        for q in range(10):
            aa = q * math.pi / 5 - math.pi / 2 + k * 3
            rr = sz if q % 2 == 0 else sz * 0.45
            pts.append((x + rr * math.cos(aa), y + rr * math.sin(aa)))
        d.polygon(pts, fill=RAINBOW[(j + seed) % 6], outline=INK, width=3)


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 18 * abs(math.cos(t * 5 + ph)) + 3
            d.rectangle((x - w / 2, y - 9, x + w / 2, y + 9), fill=col)


def note_particles(frame, t):
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(7):
        p = (t * 0.25 + i / 7) % 1
        x = 90 + (i * 157) % 900 + 30 * math.sin(t * 2 + i)
        y = 1500 - p * 1300
        col = RAINBOW[i % 6] + (int(255 * math.sin(p * math.pi)),)
        r = 22
        d.ellipse((x - r, y - r * 0.75, x + r, y + r * 0.75), fill=col)
        d.line((x + r - 3, y, x + r - 3, y - 70), fill=col, width=7)
        d.line((x + r - 3, y - 70, x + r + 25, y - 50), fill=col, width=7)
    frame.alpha_composite(layer)


def current_word(t):
    best = None
    for e in G["events"]:
        if e["t"] - 0.05 <= t < e["t"] + max(e["dur"], B * 0.9):
            best = e
    return best


def render_frame(f):
    t = f / FPS
    frame = G["bg"].copy()
    clouds(frame, t)
    lb = beat_pos(t)
    spans = song.verse_spans()
    chorus0 = spans[-1][1]
    shake = (0, 0)
    # --- centre stage
    if lb < spans[0][0]:                           # intro: title on spinning rays
        draw_rays(frame, (255, 200, 80), t, 880, min(1, t / 0.8))
        note_particles(frame, t)
        k = t / 0.6
        pulse = 1 + 0.08 * max(0, math.cos((lb % 1) * math.pi)) if t > 1 else 1
        rainbow_text(frame, W / 2, 760, "ANIMAL", int(190 * pulse * ease_back(k)) or 1, start=math.floor(lb), t=t)
        rainbow_text(frame, W / 2, 980, "DANCE!", int(210 * pulse * ease_back(k - 0.4)) or 1, start=math.floor(lb), t=t)
    elif lb < chorus0:
        for b0, b1, who, key, act in spans:
            if b0 <= lb < b1:
                draw_rays(frame, RAY_COL[act], t, 900)
                note_particles(frame, t)
                if 1 < lb - b0 < 7.5:
                    shadow(frame, W / 2, 1200, 520)
                animal(frame, key, act, t, b0)
                for q in (4, 5, 6):                # star burst on each action word
                    burst(frame, W / 2, 880, (lb - b0 - q) / 0.8, q + int(b0))
                if act == "stomp" and 4 <= lb - b0 < 7 and (lb - b0) % 1 < 0.18:
                    a = 1 - ((lb - b0) % 1) / 0.18
                    shake = (int(18 * a * math.sin(t * 90)), int(14 * a))
    else:                                          # chorus: animals circle round, confetti
        lc = lb - chorus0
        draw_rays(frame, RAINBOW[int(lc) % 6], t, 900)
        note_particles(frame, t)
        for i, key in enumerate(("elephant", "bunny", "monkey", "duckling")):
            ang = lc * math.pi / 4 + i * math.pi / 2
            cx, cy = W / 2 + 290 * math.cos(ang), 900 + 230 * math.sin(ang)
            g = ease_back((lc - i * 0.25) / 1.0)
            dy = -60 * abs(math.sin((lc + i * 0.5) * math.pi))
            rot = 14 * math.sin((lc + i) * math.pi)
            if g > 0:
                paste_center(frame, G["art"][key], cx, cy + dy, 380 * g, rot)
        confetti(frame, t, chorus0 * B)
    # --- karaoke word, pulsing on the beat
    e = current_word(t)
    yay = song.notes()[1] - 1.6                    # kids cheer "Yay!" (added in music.py)
    if lb >= yay:
        rainbow_text(frame, W / 2, 330, "YAY!", int(190 * ease_back((lb - yay) * B / 0.3)) or 1, start=yay * B, t=t)
    elif e and lb >= song.INTRO_BARS * 4 - 0.1:
        word = e["word"].upper()
        size = 150 if len(word) <= 7 else 120
        pulse = 1 + 0.07 * max(0, math.cos((lb % 1) * math.pi))
        rainbow_text(frame, W / 2, 330, word, int(size * pulse * ease_back((t - e["t"]) / 0.25)) or 1, start=e["t"], t=t)
    # --- Gul & Mishu dancing at the bottom
    for n, c in CHAR.items():
        im = compose_char(n, t)
        off = 0.5 if n == "misheal" else 0
        ph = (lb + off) % 1
        hop = abs(math.sin((lb + off) * math.pi)) * 55 if t > 0.5 else 0
        sway = math.sin(lb * math.pi / 2 + off * 2) * 7 if t > 0.5 else 0
        if t > 0.5 and (ph < 0.08 or ph > 0.94):  # squash on landing
            im = im.resize((int(im.width * 1.05), int(im.height * 0.95)), Image.BICUBIC)
        im = im.rotate(sway, center=(im.width / 2, im.height), resample=Image.BICUBIC)
        frame.alpha_composite(im, (int(c["x"] - im.width / 2), int(1885 - im.height - hop)))
    # --- camera: small zoom pulse on every beat + stomp shake
    z = 1.02 + (0.025 * max(0, math.cos((lb % 1) * math.pi)) ** 4 if t > 0.5 else 0)
    big = frame.resize((int(W * z), int(H * z)), Image.BILINEAR)
    x0 = min(max(0, (big.width - W) // 2 + shake[0]), big.width - W)
    y0 = min(max(0, (big.height - H) // 2 + shake[1]), big.height - H)
    return big.crop((x0, y0, x0 + W, y0 + H)).convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(lo, hi):
        p.stdin.write(render_frame(f).tobytes())
    p.stdin.close()
    p.wait()
    return path


if __name__ == "__main__":
    init()
    if sys.argv[1] == "frames":
        for f in [int(x) for x in sys.argv[2].split(",")]:
            render_frame(f).save(HERE / f"_f{f:04d}.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = 8
    bnd = np.linspace(0, n, NW + 1).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k}.mp4")) for k in range(NW)]
    with Pool(NW, initializer=worker_init) as pool:
        parts = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Animal Dance - Short {os.environ.get('VER', 'v2')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
