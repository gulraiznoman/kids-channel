"""Animate episode 1 from timeline.json + character layers + art.

python render.py frames N1,N2,...   -> preview PNGs
python render.py video OUT.mp4      -> silent 1920x1080 30fps video (parallel)
"""
import json, math, os, subprocess, sys, wave, pathlib, random
from multiprocessing import Pool
import numpy as np
import script as EP
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent / "characters" / "layers"
FPS = 30
VERTICAL = os.environ.get("LAYOUT") == "vertical"          # Shorts: 1080x1920
LAYOUTS = {
    False: dict(W=1920, H=1080, cx=960, fruit_y=400, fruit=430, label_y=800, label_w=760, label_max=150,
                prompt_y=60, feet=1050, gul_x=340, mishu_x=1580, bg="bg.png"),
    True: dict(W=1080, H=1920, cx=540, fruit_y=720, fruit=500, label_y=1075, label_w=720, label_max=160,
               prompt_y=360, feet=1880, gul_x=300, mishu_x=780, bg="bg_vertical.png", S=0.40),
}
L = LAYOUTS[VERTICAL]
W, H = L["W"], L["H"]
S = L.get("S", 0.46)                       # layer scale: 1200x2000 -> 552x920 (landscape)
FONT = "C:/Windows/Fonts/seguibl.ttf"
INK = (58, 36, 32)
RAINBOW = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]

CHAR = {
    "gul": dict(outfit=EP.OUTFITS["gul"], x=L["gul_x"], pivot=(396, 526), girl=False, phase=0.0),
    "misheal": dict(outfit=EP.OUTFITS["misheal"], x=L["mishu_x"], pivot=(388, 526), girl=True, phase=1.7),
}
SPEAKER_ID = {"gul": "gul", "mishu": "misheal"}
G = {}


# ----------------------------------------------------------------- loading
def load_layers(name):
    d = {}
    for p in (KIT / name).glob("*.png"):
        im = Image.open(p)
        d[p.stem] = im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS)
    return d


def envelope(wav_path):
    with wave.open(str(wav_path)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop = sr // FPS
    n = len(x) // hop + 1
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    ref = np.percentile(rms, 90) + 1e-6
    return np.clip(rms / ref, 0, 1.5)


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G["beats"], G["total"] = tl["beats"], tl["total"]
    G["layers"] = {n: load_layers(n) for n in CHAR}
    G["bg"] = Image.open(HERE / "art" / L["bg"]).convert("RGBA")
    G["fruit"] = {p.stem[6:]: Image.open(p) for p in (HERE / "art").glob("fruit_*.png")}
    G["env"] = {b["wav"]: envelope(HERE / "audio" / b["wav"]) for b in G["beats"] if "wav" in b}
    G["fonts"] = {}
    G["cache"] = {}
    # blink schedule per character
    rnd = random.Random(7)
    G["blinks"] = {}
    for n in CHAR:
        t, bl = 1.0, []
        while t < G["total"] + 5:
            bl.append(t)
            t += rnd.uniform(2.8, 5.0)
        G["blinks"][n] = bl
    # derived spans
    B = G["beats"]
    spans = dict(fruit=[], label=[], spell=[], prompt=[], stars=[], wave=[], happy=[], speak=[])
    cur = None
    for i, b in enumerate(B):
        t0, t1 = b["t"], b["t"] + b["dur"]
        if "fruit_in" in b:
            cur = dict(key=b["fruit_in"], tin=t0, tout=None, label=None, name=None, spell=None)
            spans["fruit"].append(cur)
        if "label" in b and cur:
            cur["label"], cur["name"] = t0, b["label"]
        if "spell" in b and cur:
            cur["spell"] = t0
        if "fruit_out" in b and cur:
            cur["tout"] = t0
        if b.get("prompt"):
            spans["prompt"].append((t0, t1))
        if b.get("stars"):
            spans["stars"].append(t0)
        if "wave" in b:
            spans["wave"].append((SPEAKER_ID[b["wave"]], t0 - 0.2, t1 + 0.6))
        if "eyes_closed" in b:
            spans["happy"].append((SPEAKER_ID[b["eyes_closed"]], t0, t1))
        if "wav" in b:
            spans["speak"].append((SPEAKER_ID[b["who"]], t0, t1, b["wav"]))
        if b.get("recap"):
            G["recap_t"] = t0
        if b.get("recap_walk"):
            G["recap_walk"] = (t0, t1)
        if b.get("scene") == "outro":
            G["outro_t"] = t0
    G["spans"] = spans
    G["intro_end"] = B[3]["t"]


def font(size):
    if size not in G["fonts"]:
        G["fonts"][size] = ImageFont.truetype(FONT, size)
    return G["fonts"][size]


# ----------------------------------------------------------------- helpers
def ease_back(x):
    x = min(max(x, 0.0), 1.0)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def rainbow_text(img, cx, cy, text, size, bounce=None, t=0.0, colour=None):
    """Big colourful letters with white + dark outline. bounce=(start_time) makes letters hop in turn."""
    d = ImageDraw.Draw(img)
    f = font(size)
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + 6 * (len(text) - 1)
    x = cx - total / 2
    for i, ch in enumerate(text):
        dy = 0
        if bounce is not None:
            k = t - (bounce + i * 0.11)
            if 0 <= k < 0.35:
                dy = -math.sin(k / 0.35 * math.pi) * size * 0.35
        col = colour or RAINBOW[i % len(RAINBOW)]
        y = cy - size * 0.62 + dy
        d.text((x, y), ch, font=f, fill=INK, stroke_width=int(size * 0.13), stroke_fill=INK)
        d.text((x, y), ch, font=f, fill=col, stroke_width=int(size * 0.07), stroke_fill=(255, 255, 255))
        x += widths[i] + 6


def plain_text(img, cx, cy, text, size, fill=(255, 255, 255), stroke=INK):
    d = ImageDraw.Draw(img)
    f = font(size)
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, cy - size * 0.62), text, font=f, fill=fill, stroke_width=int(size * 0.12), stroke_fill=stroke)


def star(d, cx, cy, r, col, rot=0.0):
    pts = []
    for k in range(10):
        a = rot + k * math.pi / 5 - math.pi / 2
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=INK, width=4)


# ----------------------------------------------------------------- characters
def char_state(name, t):
    eyes, mouth, arm, wave_amt, speaking = "open", "smile", "down", 0.0, False
    for (n, t0, t1, wav) in G["spans"]["speak"]:
        if n == name and t0 <= t < t1:
            env = G["env"][wav]
            k = int((t - t0) * FPS)
            v = env[min(k, len(env) - 1)]
            mouth = "closed" if v < 0.15 else ("o" if v < 0.55 else "open")
            speaking = True
            break
    for (n, t0, t1) in G["spans"]["wave"]:
        if n == name and t0 <= t < t1:
            arm = "wave"
            wave_amt = math.sin((t - t0) * 2 * math.pi * 1.6)
    for (n, t0, t1) in G["spans"]["happy"]:
        if n == name and t0 <= t < t1:
            eyes = "closed"
    if eyes == "open":
        for bt in G["blinks"][name]:
            if bt <= t < bt + 0.12:
                eyes = "blink"
                break
            if bt > t:
                break
    return eyes, mouth, arm, wave_amt, speaking


def compose_char(name, eyes, mouth, arm, wave_amt):
    c = CHAR[name]
    L = G["layers"][name]
    o = c["outfit"]
    key = (name, eyes, mouth)
    if key not in G["cache"]:
        over = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for n in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if c["girl"] else []):
            over.alpha_composite(L[n])
        G["cache"][key] = over
    ukey = (name, "under")
    if ukey not in G["cache"]:
        under = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        for n in (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}"]:
            under.alpha_composite(L[n])
        G["cache"][ukey] = under
    im = G["cache"][ukey].copy()
    if arm == "wave":
        a = L[f"arm_r_wave_{o}"]
        px, py = c["pivot"][0] * 2 * S, c["pivot"][1] * 2 * S
        a = a.rotate(-12 * wave_amt, center=(px, py), resample=Image.BICUBIC)
        im.alpha_composite(a)
    else:
        im.alpha_composite(L[f"arm_r_down_{o}"])
    im.alpha_composite(G["cache"][key])
    return im


# ----------------------------------------------------------------- frame
def render_frame(f):
    t = f / FPS
    frame = G["bg"].copy()
    d = ImageDraw.Draw(frame)

    # characters
    for name, c in CHAR.items():
        eyes, mouth, arm, wave_amt, speaking = char_state(name, t)
        im = compose_char(name, eyes, mouth, arm, wave_amt)
        bob = math.sin(2 * math.pi * 0.7 * t + c["phase"]) * 6
        if speaking:
            bob -= abs(math.sin(2 * math.pi * 2.0 * t)) * 9
        x = c["x"] - im.width // 2
        y = int(L["feet"] - 0.93 * im.height + bob)
        frame.alpha_composite(im, (x, y))

    # fruit of the moment
    for fr in G["spans"]["fruit"]:
        tin, tout = fr["tin"], fr["tout"] or 1e9
        if tin <= t < tout + 0.4:
            img = G["fruit"][fr["key"]]
            if t < tout:
                sc = ease_back((t - tin) / 0.45)
            else:
                sc = max(0.0, 1 - (t - tout) / 0.4)
            float_y = math.sin(t * 2.2) * 10
            size = int(L["fruit"] * sc)
            if size > 4:
                fi = img.resize((size, size), Image.LANCZOS)
                if t >= tout:
                    fi = fi.rotate((t - tout) * 400, resample=Image.BICUBIC)
                frame.alpha_composite(fi, (L["cx"] - size // 2, int(L["fruit_y"] - size // 2 + float_y)))
            # stars burst
            for st in G["spans"]["stars"]:
                k = t - st
                if tin <= st < tout and 0 <= k < 1.3:
                    for j in range(9):
                        a = j / 9 * 2 * math.pi + 0.3
                        r = 120 + 260 * min(1, k / 0.6)
                        alpha_scale = 1 - max(0, (k - 0.8) / 0.5)
                        rr = int(34 * alpha_scale) + 1
                        star(d, L["cx"] + r * math.cos(a), L["fruit_y"] + r * math.sin(a) * 0.8, rr,
                             RAINBOW[j % len(RAINBOW)], rot=k * 3)
            # label
            if fr["label"] is not None and fr["label"] <= t < tout:
                k = t - fr["label"]
                s2 = ease_back(k / 0.35)
                size = int(min(L["label_max"], L["label_w"] / max(4, len(fr["name"])) * 1.55) * max(0.05, s2))
                if size > 6:
                    rainbow_text(frame, L["cx"], L["label_y"], fr["name"].upper(), size,
                                 colour=getattr(EP, "LABEL_COLOURS", {}).get(fr["name"]),
                                 bounce=fr["spell"], t=t)

    # Shorts hook banner
    if VERTICAL:
        for fr in G["spans"]["fruit"]:
            if fr["tin"] - 0.2 <= t < (fr["label"] or 1e9):
                k = t - fr["tin"] + 0.2
                rainbow_text(frame, L["cx"], 170, "GUESS THE", int(110 * ease_back(k / 0.4)) or 1)
                rainbow_text(frame, L["cx"], 300, EP.NOUN + "!", int(130 * ease_back((k - 0.15) / 0.4)) or 1)

    # "your turn" prompt
    for (t0, t1) in G["spans"]["prompt"]:
        if t0 <= t < t1:
            k = t - t0
            sc = ease_back(k / 0.3) * (1 + 0.05 * math.sin(k * 10))
            w, h = int(520 * sc), int(120 * sc)
            if w > 10:
                d.rounded_rectangle((L["cx"] - w // 2, L["prompt_y"], L["cx"] + w // 2, L["prompt_y"] + h), radius=h // 2,
                                    fill=(255, 255, 255), outline=INK, width=6)
                plain_text(frame, L["cx"], L["prompt_y"] + h * 0.55, "YOUR TURN!", int(64 * sc), fill=(255, 77, 109), stroke=(255, 255, 255))

    # intro banner
    if not VERTICAL and t < G["intro_end"] + 0.5:
        k = t
        a = 1 if t < G["intro_end"] else max(0, 1 - (t - G["intro_end"]) / 0.5)
        if a > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            rainbow_text(lay, 960, 190, "GUL & MISHU", int(140 * ease_back(k / 0.6)) or 1)
            if t > 0.6:
                plain_text(lay, 960, 360, EP.TOPIC, int(90 * ease_back((t - 0.6) / 0.5)) or 1,
                           fill=(255, 210, 63))
            if a < 1:
                lay.putalpha(Image.fromarray((np.array(lay.split()[3]) * a).astype(np.uint8)))
            frame.alpha_composite(lay)

    # recap grid
    if not VERTICAL and "recap_t" in G and G["recap_t"] <= t < G.get("outro_t", 1e9):
        keys = [fr["key"] for fr in G["spans"]["fruit"]]
        w0, w1 = G["recap_walk"]
        hi = int((t - w0) / (w1 - w0) * len(keys)) if w0 <= t < w1 else -1
        for i, key in enumerate(keys):
            k = t - G["recap_t"] - i * 0.08
            sc = ease_back(k / 0.4)
            base = 175 * (1.28 if i == hi else 1.0) * sc
            size = int(base)
            if size > 4:
                cols = 4
                cx = int(960 + (i % cols - (cols - 1) / 2) * 200)
                cy = 190 + (i // cols) * 200
                if i == hi:
                    d.ellipse((cx - 120, cy - 120, cx + 120, cy + 120), fill=(255, 240, 150))
                frame.alpha_composite(G["fruit"][key].resize((size, size), Image.LANCZOS),
                                      (cx - size // 2, cy - size // 2))

    # outro banner
    if not VERTICAL and "outro_t" in G and t >= G["outro_t"]:
        k = t - G["outro_t"]
        rainbow_text(frame, 960, 300, "BYE BYE!", int(160 * ease_back(k / 0.5)) or 1)
        if k > 1.2:
            plain_text(frame, 960, 480, "See you next time!", int(70 * ease_back((k - 1.2) / 0.4)) or 1,
                       fill=(255, 210, 63))

    return frame.convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                          "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(lo, hi):
        p.stdin.write(render_frame(f).tobytes())
    p.stdin.close()
    p.wait()
    return path


if __name__ == "__main__":
    if sys.argv[1] == "frames":
        init()
        for f in [int(x) for x in sys.argv[2].split(",")]:
            render_frame(f).save(HERE / f"_f{f:05d}.png")
        print("total", G["total"])
    else:
        init()
        n = int(G["total"] * FPS)
        NW = int(os.environ.get("NW", "8"))
        b = np.linspace(0, n, NW + 1).astype(int)
        os.makedirs(HERE / "_chunks", exist_ok=True)
        jobs = [(b[k], b[k + 1], str(HERE / "_chunks" / f"c{k:02d}.mp4")) for k in range(NW)]
        with Pool(NW, initializer=worker_init) as pool:
            parts = pool.map(render_chunk, jobs)
        with open(HERE / "_chunks" / "list.txt", "w") as fh:
            for p in parts:
                fh.write(f"file '{os.path.basename(p)}'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", str(HERE / "_chunks" / "list.txt"), "-c", "copy", sys.argv[2]], check=True)
        print("wrote", sys.argv[2])
