"""Animate Long video 5 "Body Parts for Kids" (1920x1080) from timeline.json.
Big face close-ups and a big full-body presenter with pulsing rings on body parts; side kids for games.

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L05 Body Parts/Body Parts for Kids vN.mp4
"""
import json, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "long02-counting"))
import render as R

W, H, FPS = R.W, R.H, R.FPS
G = R.G
INK, RAINBOW = R.INK, R.RAINBOW
OUT = ROOT / "VIDEOS" / "L05 Body Parts"
ART_DIRS = [(HERE / "art", "item_"), (ROOT / "ep01-fruits" / "art", "fruit_"), (ROOT / "long01-animals-fun" / "art", "fruit_"),
            (ROOT / "long04-good-habits" / "art", "item_")]
R.CHAR["gul"]["outfit"] = "tee"
R.CHAR["misheal"]["outfit"] = "yellow"
BIG_OUTFIT = {"gul": "tee", "misheal": "yellow"}
# body-part points on the 1200x2000 character canvas
PTS = {
    "eyes": [(480, 636), (720, 636)], "nose": [(600, 748)], "mouth": [(600, 826)], "ears": [(205, 690), (995, 690)],
    "hair": [(600, 240)], "brows": [(480, 512), (720, 512)], "head": [(600, 400)],
    "shoulders": [(410, 1015), (790, 1015)], "arms": [(355, 1190), (845, 1190)], "hands": [(370, 1395), (830, 1395)],
    "tummy": [(600, 1320)], "knees": [(530, 1690), (670, 1690)], "feet": [(530, 1830), (670, 1830)], "toes": [(530, 1840), (670, 1840)],
    "neck": [(600, 985)], "elbows": [(330, 1160), (870, 1160)], "legs": [(530, 1620), (670, 1620)], "fingers": [(360, 1420), (840, 1420)],
}
WORD_PART = {"head": "head", "shoulders": "shoulders", "knees": "knees", "toes": "toes", "eyes": "eyes", "ears": "ears", "mouth": "mouth", "nose": "nose"}
ease_back, ease_io, rt, paste = R.ease_back, R.ease_io, R.rainbow_text, R.paste


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["fonts"], G["cache"], G["sized"] = {}, {}, {}
    G["art"] = {}
    for d, pre in ART_DIRS:
        for p in d.glob(f"{pre}*.png"):
            G["art"].setdefault(p.stem[len(pre):], Image.open(p).convert("RGBA"))
    G["layers"] = {}
    for n in R.CHAR:
        G["layers"][n] = {p.stem: (lambda im: im.resize((int(im.width * R.S), int(im.height * R.S)), Image.LANCZOS))(Image.open(p))
                          for p in (R.KIT / n).glob("*.png")}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (R.KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    head = G["full"]["gul"]["head"]
    G["skin"] = head.getpixel((600, 700))
    noear = np.array(head)                                            # head without ears (for "what's missing?")
    noear[560:820, :268, 3] = 0
    noear[560:820, 932:, 3] = 0
    G["head_noears"] = Image.fromarray(noear)
    G["env"] = {}
    for n, c in R.CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["bg"] = {n: Image.open(HERE / "art" / f"bg_{n}.png").convert("RGBA") for n in ("playroom", "park")}
    G["bigcache"] = {}


# ------------------------------------------------------------------ big presenter
def big_char(name, t, missing=None, waving=False, arms=True):
    L = G["full"][name]
    o = BIG_OUTFIT[name]
    env = G["env"][name]
    v = env[min(int(t * FPS), len(env) - 1)]
    talking = v > 0.12
    mouth = "smile" if not talking else ("o" if v < 0.5 else "open")
    eyes = "blink" if (t + 0.7) % 4.3 < 0.12 else "open"
    key = (name, mouth, eyes, missing, waving or talking, arms)
    if key in G["bigcache"]:
        return G["bigcache"][key]
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    girl = name == "misheal"
    arm_parts = [f"arm_l_{o}", f"arm_r_{'wave' if (waving or talking) else 'down'}_{o}"] if arms else []
    for p in (["hair_back"] if girl else []) + [f"body_{o}"] + arm_parts + ["neck"]:
        im.alpha_composite(L[p])
    im.alpha_composite(G["head_noears"] if (missing == "ears" and name == "gul") else L["head"])
    for p in [f"eyes_{eyes}"] + ([] if missing == "brows" else ["brows"]) + ([] if missing == "mouth" else [f"mouth_{mouth}"]) + ([] if missing == "hair" else ["hair_front"]) + (["earrings"] if girl else []):
        im.alpha_composite(L[p])
    if missing == "nose":
        d = ImageDraw.Draw(im)
        d.ellipse((560, 715, 640, 780), fill=G["skin"])
    if len(G["bigcache"]) > 60:
        G["bigcache"].clear()
    G["bigcache"][key] = im
    return im


def face_view(frame, name, t, missing=None, scale=0.95):
    """Close-up of the head: canvas box (150,100)-(1050,1000) shown at 900*scale px, centred at (960, 570)."""
    im = big_char(name, t, missing, arms=False)
    crop = im.crop((150, 100, 1050, 1000))
    s = scale
    crop = crop.resize((int(900 * s), int(900 * s)), Image.BICUBIC)
    bob = 6 * math.sin(t * 2)
    frame.alpha_composite(crop, (int(960 - 450 * s), int(570 - 450 * s + bob)))
    return lambda x, y: (960 + (x - 600) * s, 570 + (y - 550) * s + bob)


def body_view(frame, name, t, hop=0.0):
    im = big_char(name, t, waving=True)
    s = 0.5
    sm = im.resize((600, 1000), Image.BICUBIC)
    top = 60 - hop
    frame.alpha_composite(sm, (660, int(top)))
    return lambda x, y: (960 + (x - 600) * s, top + y * s)


def rings(frame, pts, t, t0, col=(255, 77, 109)):
    if t < t0:
        return
    d = ImageDraw.Draw(frame)
    q = t - t0
    for (x, y) in pts:
        r = 55 + 10 * math.sin(q * 6)
        d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=10)
        d.ellipse((x - r - 8, y - r - 8, x + r + 8, y + r + 8), outline=(255, 255, 255), width=4)


def spotlight(frame, cx, cy, r):
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 190), outline=(255, 214, 102, 255), width=8)
    frame.alpha_composite(lay)


# ------------------------------------------------------------------ scenes
def scene_hook(frame, s, t):
    missing = "nose" if t < s["found_t"] else None
    m = face_view(frame, "gul", t, missing)
    if t < s["found_t"]:
        rt(frame, 960, 90, "WHERE IS MY NOSE?!", int(110 * ease_back((t - s["t0"]) / 0.3)))
        if t >= s["search_t"]:
            for j in range(3):
                rt(frame, 300 + j * 660, 400 + 40 * math.sin(t * 4 + j), "?", 150, colour=RAINBOW[j])
        q = s["found_t"] - t
        if q < 0.7:                                                    # the nose flies back in
            k = 1 - q / 0.7
            x, y = m(600, 748)
            paste(frame, "nose", 1700 + (x - 1700) * k, 300 + (y - 300) * k - 200 * math.sin(k * math.pi), 160 * (1.3 - 0.5 * k), k * 360)
    else:
        q = t - s["found_t"]
        rt(frame, 960, 90, "BOOP! FOUND IT!", int(110 * ease_back(q / 0.3)))
        rings(frame, [m(600, 748)], t, s["found_t"], (59, 193, 74))


def scene_face(frame, s, t):
    m = face_view(frame, s["who"], t)
    rings(frame, [m(*p) for p in PTS[s["part"]]], t, s["label_t"])
    if t >= s["label_t"]:
        rt(frame, 960, 90, s["label"], int(130 * ease_back((t - s["label_t"]) / 0.35)), start=s["label_t"], t=t)


def scene_body(frame, s, t):
    acting = s["act_t"] <= t < s["t1"]
    hop = 30 * abs(math.sin(t * 7)) if acting and s["part"] in ("feet", "knees", "arms", "hands") else 0
    m = body_view(frame, s["who"], t, hop)
    rings(frame, [m(*p) for p in PTS[s["part"]]], t, s["label_t"])
    if t >= s["label_t"]:
        rt(frame, 960, 70, s["label"], int(110 * ease_back((t - s["label_t"]) / 0.35)), start=s["label_t"], t=t)


def scene_sense(frame, s, t):
    a = t - s["t0"]
    spotlight(frame, 640, 540, 210)
    paste(frame, s["icon"], 640, 540 + 8 * math.sin(t * 2), 340 * ease_back(a / 0.4))
    if t >= s["label_t"]:
        rt(frame, 960, 150, s["label"] + "!", int(150 * ease_back((t - s["label_t"]) / 0.35)), start=s["label_t"], t=t)
    if t >= s["objs_t"]:
        n = len(s["objs"])
        for i, k in enumerate(s["objs"]):
            g = ease_back((t - s["objs_t"] - i * 0.8) / 0.4)
            if g > 0:
                y = 520 + (i - (n - 1) / 2) * 280
                wob = 12 * math.sin(t * 9) if s["label"] == "HEAR" else 0
                paste(frame, k, 1280 + wob, y, (360 if n == 1 else 250) * g)


def scene_quiz(frame, s, t):
    rt(frame, 960, 160, s["q"], int(100 * ease_back((t - s["t0"]) / 0.4)), maxw=1300)
    if t >= s["answer_t"]:
        q = t - s["answer_t"]
        spotlight(frame, 960, 560, 230)
        paste(frame, s["icon"], 960, 560, 380 * ease_back(q / 0.4))
    else:
        rt(frame, 960, 560, "?", int(260 + 20 * math.sin(t * 6)), colour=(255, 255, 255))


def scene_says(frame, s, t):
    top = ("MISHU SAYS: " if s["said"] else "") + s["action"]
    rt(frame, 960, 160, top, int(95 * ease_back((t - s["say_t"]) / 0.35)), maxw=1400)
    if s["icon"]:
        paste(frame, s["icon"], 960, 520, 300 * ease_back((t - s["say_t"]) / 0.4))
    if t >= s["result_t"]:
        q = t - s["result_t"]
        if s["said"]:
            rt(frame, 960, 800, "YES!", int(150 * ease_back(q / 0.3)), colour=(59, 193, 74))
        else:
            rt(frame, 960, 800, "DON'T MOVE!", int(130 * ease_back(q / 0.3)), colour=(255, 77, 77))


def scene_missing(frame, s, t):
    missing = s["part"] if t < s["back_t"] else None
    m = face_view(frame, "gul", t, missing)
    if t < s["back_t"]:
        rt(frame, 960, 90, "WHAT'S MISSING?", int(110 * ease_back((t - s["t0"]) / 0.35)))
    else:
        rings(frame, [m(*p) for p in PTS[s["part"]]], t, s["back_t"], (59, 193, 74))
        rt(frame, 960, 90, s["part"].upper() + "!", int(130 * ease_back((t - s["back_t"]) / 0.35)))


def scene_animal(frame, s, t):
    rt(frame, 960, 160, s["q"], int(90 * ease_back((t - s["t0"]) / 0.4)), maxw=1300)
    if t >= s["reveal_t"]:
        q = t - s["reveal_t"]
        spotlight(frame, 960, 580, 260)
        paste(frame, s["key"], 960, 580 + 8 * math.sin(t * 2.2), 440 * ease_back(q / 0.45))
    else:
        rt(frame, 960, 580, "?", int(260 + 20 * math.sin(t * 6)), colour=(255, 255, 255))


def scene_song(frame, s, t):
    cur = None
    for t0, w in s["words"]:
        if t >= t0:
            cur = (t0, w)
    hop = 20 * abs(math.sin(t * (12 if s["fast"] else 7)))
    m = body_view(frame, s["who"], t, hop)
    if cur:
        t0, w = cur
        word = w.replace("and ", "").replace("And ", "").strip("!").lower()
        part = WORD_PART.get(word)
        if part and t - t0 < (0.6 if s["fast"] else 1.0):
            rings(frame, [m(*p) for p in PTS[part]], t, t0, RAINBOW[hash(word) % 6])
        rt(frame, 960, 70, w.upper().rstrip("!") + "!", int(120 * ease_back((t - t0) / 0.2)))
    if s["fast"]:
        rt(frame, 1650, 160, "FAST!", 90, colour=(255, 77, 77))


def scene_outro(frame, s, t):
    for i, k in enumerate(("eye", "ear", "nose", "mouth", "hand")):
        paste(frame, k, 620 + i * 170, 560 - 25 * abs(math.sin(t * 3 + i)), 170 * ease_back((t - s["t0"] - i * 0.1) / 0.4))
    if t >= s["bye_t"]:
        rt(frame, 960, 230, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.4)))
    else:
        rt(frame, 960, 230, "MY AMAZING BODY!", int(120 * ease_back((t - s["t0"]) / 0.4)))


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rt(frame, 960, 380, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1400)


def scene_count(frame, s, t):
    m = body_view(frame, s["who"], t)
    rt(frame, 960, 70, s["q"], int(80 * ease_back((t - s["t0"]) / 0.35)), maxw=1300)
    if t >= s["answer_t"]:
        pts = [m(*p) for p in PTS[s["part"]]]
        rings(frame, pts, t, s["answer_t"], (59, 193, 74))
        rt(frame, 1500, 520, str(s["num"]), int(260 * ease_back((t - s["answer_t"]) / 0.35)), colour=RAINBOW[s["num"] % 6])


def scene_use(frame, s, t):
    rt(frame, 960, 160, s["q"], int(80 * ease_back((t - s["t0"]) / 0.4)), maxw=1350)
    spotlight(frame, 760, 560, 210)
    paste(frame, s["obj"], 760, 560 + 8 * math.sin(t * 2), 330 * ease_back((t - s["t0"]) / 0.4))
    rt(frame, 1000, 560, "+", 140, colour=(255, 255, 255))
    if t >= s["answer_t"]:
        q = t - s["answer_t"]
        if s["icon"]:
            paste(frame, s["icon"], 1220, 560, 300 * ease_back(q / 0.4))
        else:
            paste(frame, "feet_icon" if "feet_icon" in G["art"] else "shoes", 1220, 560, 300 * ease_back(q / 0.4))
    else:
        rt(frame, 1220, 560, "?", int(240 + 20 * math.sin(t * 6)), colour=(255, 255, 255))


def scene_peek(frame, s, t):
    """A wooden window with a small round hole showing one body part; it opens at the reveal."""
    art = G["art"][s["key"]]
    size = 900
    im = art.resize((size, size), Image.BICUBIC)
    fx, fy = s["focus"]
    cx, cy = 960, 560
    if t < s["reveal_t"]:
        r = 150
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).ellipse((fx * size - r, fy * size - r, fx * size + r, fy * size + r), fill=255)
        win = Image.new("RGBA", (520, 520), (150, 100, 60, 255))
        d = ImageDraw.Draw(win)
        d.rectangle((0, 0, 519, 519), outline=INK, width=12)
        hole = Image.new("RGBA", (2 * r, 2 * r), (255, 255, 255, 255))
        piece = im.crop((int(fx * size - r), int(fy * size - r), int(fx * size + r), int(fy * size + r)))
        hole.alpha_composite(piece)
        hm = Image.new("L", hole.size, 0)
        ImageDraw.Draw(hm).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
        win.paste(hole, (260 - r, 260 - r), hm)
        d.ellipse((260 - r, 260 - r, 260 + r, 260 + r), outline=INK, width=10)
        frame.alpha_composite(win, (cx - 260, cy - 260))
        rt(frame, 960, 150, "WHO'S PEEKING?", int(110 * ease_back((t - s["t0"]) / 0.35)))
    else:
        q = (t - s["reveal_t"]) / 0.5
        spotlight(frame, cx, cy, 270)
        paste(frame, s["key"], cx, cy, 480 * ease_back(q))
        rt(frame, 960, 150, s["key"].replace("foal", "horse").upper() + "!", int(140 * ease_back(q)))


def scene_happy(frame, s, t):
    cur = None
    for t0, act, icon, verse in s["acts"]:
        if t >= t0:
            cur = (t0, act, icon, verse)
    if cur:
        t0, act, icon, verse = cur
        rt(frame, 960, 150, "IF YOU'RE HAPPY AND YOU KNOW IT...", 70, maxw=1400)
        q = (t - t0) % 3.3
        rt(frame, 960, 480, act, int(200 * (1 + 0.08 * math.sin(t * 10))))
        d = ImageDraw.Draw(frame)
        for j in range(10):
            ang = j / 10 * 2 * math.pi + t
            R.star(d, 960 + 450 * math.cos(ang), 500 + 220 * math.sin(ang), 22, RAINBOW[j % 6], rot=t * 3)


SCENES = {"count": scene_count, "use": scene_use, "peek": scene_peek, "happy": scene_happy, "hook": scene_hook, "face": scene_face, "body": scene_body, "sense": scene_sense, "quiz": scene_quiz, "says": scene_says,
          "missing": scene_missing, "animal": scene_animal, "song": scene_song, "outro": scene_outro, "title": scene_title}
BIG = {"hook", "face", "body", "missing", "song", "count"}                    # scenes with a big presenter (no side kids)


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SCENES[sc["kind"]](frame, sc, t)
    R.stars_burst(frame, t)
    if sc["kind"] not in BIG:
        hopping = sc["kind"] == "says" and t >= sc.get("say_t", 1e9) + 0.6 and sc["said"]
        if hopping:
            for n, c in R.CHAR.items():
                pass
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
            render_frame(f).save(HERE / f"_f{f:05d}.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "4"))
    parts = 24
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"Body Parts for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
