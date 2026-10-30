"""Body Parts v2 renderer (1920x1080): big opening, face/body with 30 parts + fact line + counter, x-ray INSIDE MY BODY,
left & right, zoom-in game, senses, games, songs. Reuses v1 helpers.

python render2.py frames 100,900,...  -> preview PNGs
python render2.py video               -> VIDEOS/L05 Body Parts/Body Parts for Kids v2.mp4
"""
import importlib.util, json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location("bp1", HERE / "render.py")
V1 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, ["x"]
spec.loader.exec_module(V1)
sys.argv = _argv
R = V1.R
W, H, FPS = R.W, R.H, R.FPS
G = R.G
INK, RAINBOW = R.INK, R.RAINBOW
OUT = V1.OUT
ease_back, ease_io, rt, paste = R.ease_back, R.ease_io, R.rainbow_text, R.paste


def _plain_text(img, cx, cy, text, size, fill=(255, 255, 255), stroke=None):
    d = ImageDraw.Draw(img)
    f = R.font(size)
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, cy - size * 0.62), text, font=f, fill=fill, stroke_width=max(1, int(size * 0.14)), stroke_fill=stroke or INK)


R.plain_text = _plain_text

FACE_PTS = {  # Mishu canvas
    "head": [(600, 330)], "hair": [(330, 520), (870, 520)], "forehead": [(600, 455)], "brows": [(480, 512), (720, 512)],
    "lashes": [(390, 590), (810, 590)], "eyes": [(480, 636), (720, 636)], "nose": [(600, 748)], "cheeks": [(430, 760), (770, 760)],
    "ears": [(240, 760), (960, 760)], "lips": [(600, 826)], "teeth": [(600, 820)], "tongue": [(600, 840)], "chin": [(600, 915)]}
BODY_PTS = {  # Gul canvas, arms down
    "neck": [(600, 985)], "shoulders": [(410, 1015), (790, 1015)], "chest": [(600, 1120)], "tummy": [(600, 1320)],
    "arms": [(390, 1090), (810, 1090)], "elbows": [(320, 1200), (880, 1200)], "wrists": [(345, 1335), (855, 1335)],
    "hands": [(370, 1390), (830, 1390)], "thumbs": [(410, 1370), (790, 1370)], "fingers": [(360, 1420), (840, 1420)],
    "hips": [(470, 1460), (730, 1460)], "legs": [(525, 1600), (675, 1600)], "knees": [(530, 1665), (670, 1665)],
    "ankles": [(530, 1790), (670, 1790)], "feet": [(525, 1830), (675, 1830)], "toes": [(515, 1845), (685, 1845)],
    "head": [(600, 400)], "eyes": [(480, 636), (720, 636)], "ears": [(205, 690), (995, 690)], "mouth": [(600, 826)], "nose": [(600, 748)],
    "hair": [(600, 250)]}
WINDOWS = {"head": (300, 260, 900, 930), "chest": (410, 990, 790, 1270), "tummy": (420, 1190, 780, 1470),
           "leg": (440, 1480, 760, 1850), "arm": (230, 990, 520, 1430)}
ORGAN_SPOT = {"brain": ("head", 600, 470, 380), "heart_organ": ("chest", 600, 1130, 230), "lungs": ("chest", 600, 1130, 300),
              "stomach": ("tummy", 600, 1330, 260), "bone": ("leg", 600, 1665, 300), "muscle": ("arm", 375, 1210, 260),
              "hand": ("arm", 375, 1210, 260), "mouth": ("head", 600, 760, 300)}


def init():
    V1.init()
    tl = json.load(open(HERE / "timeline2.json"))
    G.update(tl)
    G["env"] = {}
    for n, c in R.CHAR.items():
        x, sr = sf.read(HERE / f"vocal2_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["bg"]["stage"] = Image.open(HERE / "art" / "bg_stage.png").convert("RGBA")
    rng = np.random.default_rng(3)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]
    G["c2"] = {}


def compose(name, t, mouth_force=None, arms_down=True, missing=None, waving=False):
    """Full-res character with arms DOWN (so body-part rings stay on target) unless waving."""
    L = G["full"][name]
    o = V1.BIG_OUTFIT[name]
    env = G["env"][name]
    v = env[min(int(t * FPS), len(env) - 1)]
    talking = v > 0.12
    mouth = mouth_force or ("smile" if not talking else ("o" if v < 0.5 else "open"))
    eyes = "blink" if (t + 0.7) % 4.3 < 0.12 else "open"
    key = (name, mouth, eyes, missing, waving)
    if key in G["c2"]:
        return G["c2"][key]
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    girl = name == "misheal"
    for p in (["hair_back"] if girl else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_{'wave' if waving else 'down'}_{o}", "neck"]:
        im.alpha_composite(L[p])
    im.alpha_composite(L["head"])
    for p in [f"eyes_{eyes}", "brows", f"mouth_{mouth}"] + ([] if missing == "hair" else ["hair_front"]) + (["earrings"] if girl else []):
        im.alpha_composite(L[p])
    if missing == "nose":
        ImageDraw.Draw(im).ellipse((560, 715, 640, 780), fill=G["skin"])
    if len(G["c2"]) > 60:
        G["c2"].clear()
    G["c2"][key] = im
    return im


def face2(frame, name, t, mouth_force=None, missing=None):
    im = compose(name, t, mouth_force, missing=missing)
    s = 0.95
    crop = im.crop((150, 100, 1050, 1000)).resize((int(900 * s), int(900 * s)), Image.BICUBIC)
    bob = 6 * math.sin(t * 2)
    frame.alpha_composite(crop, (int(960 - 450 * s), int(560 - 450 * s + bob)))
    return lambda x, y: (960 + (x - 600) * s, 560 + (y - 550) * s + bob)


def body2(frame, name, t, hop=0.0, waving=False):
    im = compose(name, t, waving=waving)
    s = 0.48
    sm = im.resize((int(1200 * s), int(2000 * s)), Image.BICUBIC)
    top = 70 - hop
    frame.alpha_composite(sm, (int(960 - 600 * s), int(top)))
    return lambda x, y: (960 + (x - 600) * s, top + y * s)


def fact_line(frame, s, t):
    if s.get("fact") and t >= s["label_t"] + 0.2:
        R.plain_text(frame, 960, 178, s["fact"], 44, fill=(255, 255, 255))


def counter(frame, s):
    if "num" in s:
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((40, 40, 290, 140), radius=40, fill=(255, 255, 255), outline=INK, width=6)
        rt(frame, 165, 95, f"{s['num']}/30", 62, colour=(255, 107, 139))


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 20 * abs(math.cos(t * 5 + ph)) + 4
            d.rectangle((x - w / 2, y - 10, x + w / 2, y + 10), fill=col)


# ------------------------------------------------------------------ scenes
def scene_intro(frame, s, t):
    c, lg, ti = s["crash_t"], s["logo_t"], s["title_t"]
    if t < c:                                                         # drum roll: spotlight sweeps
        d = ImageDraw.Draw(frame)
        x = 960 + 700 * math.sin(t * 3)
        mask = Image.new("L", frame.size, 150)
        ImageDraw.Draw(mask).ellipse((x - 300, 300, x + 300, 900), fill=0)
        dark = Image.new("RGBA", frame.size, (10, 10, 40, 255))
        dark.putalpha(mask)
        frame.alpha_composite(dark)
        rt(frame, 960, 560, "?", int(200 + 30 * math.sin(t * 8)), colour=(255, 255, 255))
        return
    confetti(frame, t, c)
    if t >= lg:
        k = (t - lg) / 0.6
        size = int(140 * ease_back(k))
        lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        rt(lay, 960, 220, "GUL & MISHU", size)
        if k < 1:
            lay = lay.rotate((1 - k) * 360, center=(960, 220))
        frame.alpha_composite(lay)
        for n, x0, x1 in (("gul", -400, 520), ("misheal", 2300, 1400)):  # kids jump in
            q = min(1, (t - lg) / 0.7)
            im = compose(n, t, "open", waving=True)
            sm = im.resize((456, 760), Image.BICUBIC)
            x = x0 + (x1 - x0) * ease_io(q)
            y = 300 - 200 * math.sin(q * math.pi)
            frame.alpha_composite(sm, (int(x - 228), int(y)))
    if t >= ti:
        q = (t - ti) / 0.35
        rt(frame, 960, 470, "BODY PARTS!", int(220 * ease_back(q)))
        if q < 1:
            flash = Image.new("RGBA", frame.size, (255, 255, 255, int(200 * (1 - q))))
            frame.alpha_composite(flash)


def scene_hook(frame, s, t):
    missing = "nose" if t < s["found_t"] else None
    m = face2(frame, "gul", t, missing=missing)
    if t < s["found_t"]:
        rt(frame, 960, 90, "WHERE IS MY NOSE?!", int(110 * ease_back((t - s["t0"]) / 0.3)))
        q = s["found_t"] - t
        if q < 0.7:
            k = 1 - q / 0.7
            x, y = m(600, 748)
            paste(frame, "nose", 1700 + (x - 1700) * k, 300 + (y - 300) * k - 200 * math.sin(k * math.pi), 160 * (1.3 - 0.5 * k), k * 360)
    else:
        rt(frame, 960, 90, "BOOP! FOUND IT!", int(110 * ease_back((t - s["found_t"]) / 0.3)))
        V1.rings(frame, [m(600, 748)], t, s["found_t"], (59, 193, 74))


def scene_face(frame, s, t):
    force = "open" if s["part"] in ("teeth", "tongue") else None
    m = face2(frame, s["who"], t, force)
    V1.rings(frame, [m(*p) for p in FACE_PTS[s["part"]]], t, s["label_t"])
    rt(frame, 960, 90, s["label"], int((150 if s.get("quick") else 130) * ease_back((t - s["label_t"]) / 0.3)), start=s["label_t"], t=t)
    counter(frame, s)
    fact_line(frame, s, t)


def scene_body(frame, s, t):
    hop = 22 * abs(math.sin(t * 7)) if s["part"] in ("feet", "toes", "knees", "legs", "hips") and t > s["label_t"] + 1.0 else 0
    m = body2(frame, s["who"], t, hop)
    V1.rings(frame, [m(*p) for p in BODY_PTS[s["part"]]], t, s["label_t"])
    rt(frame, 960, 70, s["label"], int((140 if s.get("quick") else 120) * ease_back((t - s["label_t"]) / 0.3)), start=s["label_t"], t=t)
    counter(frame, s)
    fact_line(frame, s, t)


def scene_thirty(frame, s, t):
    confetti(frame, t, s["t0"])
    rt(frame, 960, 420, "30", int(330 * ease_back((t - s["t0"]) / 0.4)))
    rt(frame, 960, 680, "BODY PARTS!", int(150 * ease_back((t - s["t0"] - 0.3) / 0.4)))


def zoom_body(frame, name, t, focus_y, scale=0.8):
    """Bigger view of the character, centred on canvas row focus_y (for the x-ray)."""
    im = compose(name, t)
    sm = im.resize((int(1200 * scale), int(2000 * scale)), Image.BICUBIC)
    top = 570 - focus_y * scale
    frame.alpha_composite(sm, (int(960 - 600 * scale), int(top)))
    return lambda x, y: (960 + (x - 600) * scale, top + y * scale)


def scene_xray(frame, s, t):
    art, win, label = s["art"], s["win"], s["label"]
    x0, y0, x1, y1 = WINDOWS[ORGAN_SPOT[art][0]]
    m = zoom_body(frame, s["who"], t, (y0 + y1) / 2, 0.85 if ORGAN_SPOT[art][0] != "head" else 0.75)
    k = min(1, (t - s["t0"]) / 0.5)
    (ax, ay), (bx, by) = m(x0, y0), m(x1, y1)
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    hw, hh = (bx - ax) / 2 * k, (by - ay) / 2 * k
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((cx - hw, cy - hh, cx + hw, cy + hh), radius=30, fill=(25, 40, 90, 225), outline=(120, 220, 255, 255), width=8)
    for j in range(5):                                                  # scan lines
        yy = cy - hh + ((t * 140 + j * 50) % max(1, 2 * hh))
        d.line((cx - hw + 10, yy, cx + hw - 10, yy), fill=(120, 220, 255, 60), width=3)
    frame.alpha_composite(lay)
    if k >= 1:
        _, ox, oy, osz = ORGAN_SPOT[art]
        px, py = m(ox, oy)
        size = osz * 0.85 * 1.15
        if art == "heart_organ":
            size *= 1 + 0.12 * max(0, math.sin((t - s["label_t"]) * 2 * math.pi / 0.8)) ** 4
        elif art == "lungs":
            size *= 1 + 0.12 * math.sin((t - s["label_t"]) * math.pi / 2.0)
        elif art == "stomach":
            size *= 1 + 0.05 * math.sin(t * 12)
        paste(frame, art, px, py, size, 4 * math.sin(t * 3) if art == "brain" else 0)
        if art == "brain":
            dd = ImageDraw.Draw(frame)
            for j in range(5):
                ang = t * 2 + j * 1.256
                R.star(dd, px + 120 * math.cos(ang), py + 90 * math.sin(ang), 14, (255, 230, 80), rot=t * 3)
    rt(frame, 960, 70, label + "!", int(130 * ease_back((t - s["label_t"]) / 0.3)), start=s["label_t"], t=t)
    if art == "lungs" and "breath_t" in s and t >= s["breath_t"]:
        q = (t - s["breath_t"]) % 2.0
        R.plain_text(frame, 1500, 540, "BREATHE IN..." if q < 1.0 else "...BREATHE OUT", 60, fill=(255, 255, 255))


def scene_leftright(frame, s, t):
    m = body2(frame, s["who"], t, waving=False)
    pts = BODY_PTS[s["part"]]
    pt = pts[0] if s["side"] == 1 else pts[-1]
    V1.rings(frame, [m(*pt)], t, s["label_t"], (59, 193, 74) if s["side"] == 1 else (46, 168, 255))
    x, y = m(*pt)
    rt(frame, x + (-260 if s["side"] == 1 else 260), y, "RIGHT" if s["side"] == 1 else "LEFT", 80,
       colour=(59, 193, 74) if s["side"] == 1 else (46, 168, 255))
    rt(frame, 960, 70, s["label"], int(120 * ease_back((t - s["label_t"]) / 0.3)), start=s["label_t"], t=t)


ZOOM = {"ears": (60, 540, 360, 840), "eyes": (380, 520, 600, 740), "hands": (250, 1280, 490, 1520), "nose": (500, 660, 700, 860),
        "knees": (430, 1560, 630, 1760), "hair": (300, 120, 900, 520)}


def scene_zoom(frame, s, t):
    im = compose("gul", t)
    if t < s["reveal_t"]:
        x0, y0, x1, y1 = ZOOM[s["part"]]
        crop = im.crop((x0, y0, x1, y1)).resize((620, int(620 * (y1 - y0) / (x1 - x0))), Image.BICUBIC)
        lay = Image.new("RGBA", (680, crop.height + 60), (255, 255, 255, 255))
        ImageDraw.Draw(lay).rounded_rectangle((0, 0, lay.width - 1, lay.height - 1), radius=40, outline=INK, width=10)
        lay.alpha_composite(crop, (30, 30))
        mask = Image.new("L", lay.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, lay.width - 1, lay.height - 1), fill=255)
        circ = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        circ.paste(lay, (0, 0), mask)
        ImageDraw.Draw(circ).ellipse((4, 4, lay.width - 5, lay.height - 5), outline=INK, width=12)
        sc = ease_back((t - s["t0"]) / 0.4)
        circ = circ.resize((max(1, int(circ.width * sc * 0.9)), max(1, int(circ.height * sc * 0.9))), Image.BICUBIC)
        frame.alpha_composite(circ, (int(960 - circ.width / 2), int(560 - circ.height / 2)))
        rt(frame, 960, 90, "WHAT IS IT?", int(120 * ease_back((t - s["t0"]) / 0.3)))
    else:
        m = body2(frame, "gul", t)
        V1.rings(frame, [m(*p) for p in BODY_PTS[s["part"]]], t, s["reveal_t"], (59, 193, 74))
        rt(frame, 960, 70, s["part"].rstrip("s").upper().replace("KNEE", "KNEE").replace("HAI", "HAIR") + "!", int(130 * ease_back((t - s["reveal_t"]) / 0.3)))


def scene_listen(frame, s, t):
    V1.spotlight(frame, 960, 560, 260)
    paste(frame, "ear", 960, 560, 380 * ease_back((t - s["t0"]) / 0.4))
    if t >= s["sound_t"]:
        paste(frame, "bell", 1350 + 12 * math.sin(t * 10), 520, 260)
        rt(frame, 960, 150, "DING, DING!", int(130 * ease_back((t - s["sound_t"]) / 0.3)))
    else:
        rt(frame, 960, 150, "CLOSE YOUR EYES...", int(100 * ease_back((t - s["t0"]) / 0.4)))


def scene_outro(frame, s, t):
    confetti(frame, t, s["t0"])
    for i, k in enumerate(("brain", "heart_organ", "lungs", "stomach", "muscle")):
        paste(frame, k, 620 + i * 170, 600 - 25 * abs(math.sin(t * 3 + i)), 170 * ease_back((t - s["t0"] - i * 0.1) / 0.4))
    rt(frame, 960, 250, "BYE BYE!" if t >= s["bye_t"] else "AMAZING BODY!", int(160 * ease_back((t - s["t0"]) / 0.4)))


SC = dict(V1.SCENES)
SC.update({"intro": scene_intro, "hook": scene_hook, "face": scene_face, "body": scene_body, "thirty": scene_thirty, "xray": scene_xray,
           "leftright": scene_leftright, "zoom": scene_zoom, "listen": scene_listen, "outro": scene_outro})
BIG = {"intro", "hook", "face", "body", "xray", "leftright", "zoom", "song", "thirty"}


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SC[sc["kind"]](frame, sc, t)
    R.stars_burst(frame, t)
    if sc["kind"] not in BIG:
        R.draw_kids(frame, t)
    R.your_turn(frame, t)
    return frame.convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
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
            render_frame(f).save(HERE / f"_g{f:05d}.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "4"))
    parts = 24
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (HERE / "_chunks2").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks2" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks2" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Body Parts for Kids {os.environ.get('VER', 'v2')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks2" / "list.txt"),
                    "-i", str(HERE / "mix2.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
