"""Animate Long video 3 "Fruits and Vegetables" (1920x1080) from timeline.json.
Reuses drawing helpers from long02-counting/render.py (text, items, badges, kids).

python render.py frames 100,900,...  -> preview PNGs
python render.py video               -> VIDEOS/L03 Fruits and Vegetables/Fruits and Vegetables for Kids vN.mp4
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
OUT = ROOT / "VIDEOS" / "L03 Fruits and Vegetables"
R.CHAR["gul"]["outfit"] = "bluetee"                  # new outfit pairing, different look from L01/L02
R.CHAR["misheal"]["outfit"] = "yellow"
ART_DIRS = [(HERE / "art", "item_"), (ROOT / "ep01-fruits" / "art", "fruit_"), (ROOT / "long01-animals-fun" / "art", "fruit_")]
CENTER = (960, 470)


def init():
    tl = json.load(open(HERE / "timeline.json"))
    G.update(tl)
    G["fonts"], G["cache"], G["sized"] = {}, {}, {}
    G["art"] = {}
    for d, pre in ART_DIRS:
        for p in d.glob(f"{pre}*.png"):
            k = p.stem[len(pre):]
            G["art"].setdefault(k, Image.open(p).convert("RGBA"))
    G["layers"] = {}
    for n in R.CHAR:
        G["layers"][n] = {p.stem: (lambda im: im.resize((int(im.width * R.S), int(im.height * R.S)), Image.LANCZOS))(Image.open(p))
                          for p in (R.KIT / n).glob("*.png")}
    G["env"] = {}
    for n, c in R.CHAR.items():
        x, sr = sf.read(HERE / f"vocal_{c['voc']}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["bg"] = {n: Image.open(HERE / "art" / f"bg_{n}.png").convert("RGBA") for n in ("market", "patch", "kitchen")}


ease_back, ease_io, rt, paste = R.ease_back, R.ease_io, R.rainbow_text, R.paste


def spotlight(frame, cx, cy, r):
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 190), outline=(255, 214, 102, 255), width=8)
    frame.alpha_composite(lay)


def basket(frame, items, cx=960, cy=905, size=300):
    """Basket with the fruits collected so far peeking out of the top."""
    for i, k in enumerate(items[-6:]):
        x = cx - 105 + (i % 3) * 105
        y = cy - size * 0.18 - (i // 3) * 40
        paste(frame, k, x, y, 120)
    paste(frame, "basket", cx, cy, size)


def label(frame, s, t):
    if "label_t" in s and t >= s["label_t"]:
        rt(frame, 960, 175, s["name"], int(150 * ease_back((t - s["label_t"]) / 0.35)), start=s["label_t"], t=t)


def into_basket(t, s, cx, cy, size, tx=960, ty=880):
    if "drop_t" in s and t >= s["drop_t"]:
        k = ease_io((t - s["drop_t"]) / 0.8)
        return cx + (tx - cx) * k, cy + (ty - cy) * k - 160 * math.sin(k * math.pi), size * (1 - 0.7 * k)
    return cx, cy, size


# ------------------------------------------------------------------ scenes
def scene_fruit(frame, s, t):
    basket(frame, s["basket"])
    cx, cy = CENTER
    a = t - s["t0"]
    size = 440 * ease_back(a / 0.45)
    key = s["key"]
    if "cut_t" in s and t >= s["cut_t"] + 0.25:
        key = s["key"] + "_half"
    x, y, sz = into_basket(t, s, cx, cy + 8 * math.sin(t * 2.2), size)
    if "drop_t" not in s or t < s["drop_t"]:
        spotlight(frame, cx, cy, 260)
    if "cut_t" in s and s["cut_t"] <= t < s["cut_t"] + 0.25:      # knife flash across the fruit
        paste(frame, s["key"], x, y, sz)
        d = ImageDraw.Draw(frame)
        k = (t - s["cut_t"]) / 0.25
        d.line((x - 260 + 520 * k - 60, y - 230, x - 260 + 520 * k + 60, y + 230), fill=(255, 255, 255), width=18)
    else:
        sc = 1.0
        if "cut_t" in s and s["cut_t"] + 0.25 <= t < s["cut_t"] + 0.6:
            sc = ease_back((t - s["cut_t"] - 0.25) / 0.35)
        paste(frame, key, x, y, sz * sc)
    label(frame, s, t)


def scene_veg(frame, s, t):
    cx, cy = CENTER
    pulled = t >= s["pull_t"]
    d = ImageDraw.Draw(frame)
    if not pulled or t < s["pull_t"] + 0.5:
        if s["grows"] == "under":                                     # leafy tuft poking out of the soil
            wob = 6 * math.sin(t * 4)
            for j, ang in enumerate((-30, -10, 10, 30)):
                bx, by = 960, 705
                tx, ty = bx + 120 * math.sin(math.radians(ang)) + wob, by - 170 + abs(ang) * 1.5
                d.polygon([(bx - 14, by), (tx - 22, ty + 20), (tx, ty), (tx + 22, ty + 20), (bx + 14, by)], fill=(76, 175, 80), outline=INK)
        else:                                                         # a leafy plant
            for j, (dx, dy, r) in enumerate(((-110, -60, 90), (110, -60, 90), (0, -150, 110), (-60, 30, 80), (60, 30, 80), (0, -40, 100))):
                rr = r + 4 * math.sin(t * 3 + j)
                d.ellipse((960 + dx - rr, 560 + dy - rr, 960 + dx + rr, 560 + dy + rr), fill=(86, 170, 70), outline=INK, width=5)
            d.rectangle((945, 620, 975, 720), fill=(110, 140, 60), outline=INK, width=4)
    if pulled:
        k = (t - s["pull_t"]) / 0.6
        y0 = 720 if s["grows"] == "under" else 560
        y = y0 + (cy - y0) * ease_back(k)
        size = 160 + 260 * min(1, k)
        if s["grows"] == "under" and k < 1.2:                          # dirt bits flying
            for j in range(10):
                q = min(1.2, k)
                ang = math.pi + j / 9 * math.pi
                d.ellipse((960 + math.cos(ang) * 260 * q - 12, 720 + math.sin(ang) * 220 * q + 300 * q * q - 12,
                           960 + math.cos(ang) * 260 * q + 12, 720 + math.sin(ang) * 220 * q + 300 * q * q + 12), fill=(139, 90, 43))
        x, y, size = into_basket(t, s, cx, y + (8 * math.sin(t * 2.2) if k > 1 else 0), size, 960, 1150)
        if k > 0.6 and ("drop_t" not in s or t < s["drop_t"]):
            spotlight(frame, cx, cy, 240)
        paste(frame, s["key"], x, y, size)
    label(frame, s, t)


def crate(frame, cx, cy, which, items):
    paste(frame, "crate_fruit" if which == "fruit" else "crate_veg", cx, cy, 400)
    for i, k in enumerate(items):
        paste(frame, k, cx - 110 + (i % 3) * 110, cy - 150 - (i // 3) * 70, 120)
    rt(frame, cx, cy + 60, "FRUIT" if which == "fruit" else "VEGETABLE", 56, colour=(255, 255, 255), maxw=330)


def scene_shadow(frame, s, t):
    a = t - s["t0"]
    size = 460 * ease_back(a / 0.45)
    y = 500 + 8 * math.sin(t * 2.2)
    spotlight(frame, 960, 500, 270)
    im = R.item(s["key"], size)
    if t < s["reveal_t"]:
        arr = np.array(im)
        arr[:, :, :3] = (40, 36, 60)
        im = Image.fromarray(arr)
        rt(frame, 960, 150, "WHO AM I?", int(130 * ease_back(a / 0.4)))
    else:
        k = (t - s["reveal_t"]) / 0.4
        if k < 1:
            arr = np.array(im).astype(float)
            arr[:, :, :3] = arr[:, :, :3] * k + np.array((40, 36, 60)) * (1 - k)
            im = Image.fromarray(arr.astype(np.uint8))
        rt(frame, 960, 150, s["key"].replace("veg", "").upper(), int(140 * ease_back(k)), start=s["reveal_t"], t=t)
    rot = 360 * ease_io((t - s["reveal_t"]) / 0.6) if s["reveal_t"] <= t < s["reveal_t"] + 0.6 else 0
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.alpha_composite(im, (int(960 - im.width / 2), int(y - im.height / 2)))


def scene_size(frame, s, t):
    a = t - s["t0"]
    xb, xs = (1260, 660) if s["flip"] else (660, 1260)
    for key, x, base, is_big in ((s["big"], xb, 440, True), (s["small"], xs, 170, False)):
        size = base * ease_back(a / 0.45)
        y = 500 + 8 * math.sin(t * 2.2 + x)
        if is_big and t >= s["answer_t"]:
            q = t - s["answer_t"]
            size *= 1 + 0.12 * abs(math.sin(q * 5)) * max(0, 1 - q / 1.5)
            rt(frame, x, 830, "BIG!", int(110 * ease_back(q / 0.3)))
        if not is_big and t >= s["small_t"]:
            rt(frame, x, 830, "small", int(70 * ease_back((t - s["small_t"]) / 0.3)), colour=(255, 255, 255))
        paste(frame, key, x, y, size)
    rt(frame, 960, 150, "WHICH IS BIGGER?", int(110 * ease_back(a / 0.4)))


def scene_sort(frame, s, t):
    done_f = [k for k, f in s["done"] if f]
    done_v = [k for k, f in s["done"] if not f]
    crate(frame, 600, 760, "fruit", done_f)
    crate(frame, 1320, 760, "veg", done_v)
    a = t - s["t0"]
    x, y, size = 960, 360 + 8 * math.sin(t * 2.2), 330 * ease_back(a / 0.45)
    if t >= s["fly_t"]:
        k = ease_io((t - s["fly_t"]) / 0.8)
        tx = 600 if s["fruit"] else 1320
        x, y, size = 960 + (tx - 960) * k, 360 + (610 - 360) * k - 200 * math.sin(k * math.pi), 330 - 210 * k
    else:
        spotlight(frame, 960, 360, 210)
    paste(frame, s["key"], x, y, size)
    if t >= s["answer_t"]:
        rt(frame, 960, 120, "FRUIT!" if s["fruit"] else "VEGETABLE!", int(120 * ease_back((t - s["answer_t"]) / 0.3)))
    else:
        rt(frame, 960, 120, "FRUIT OR VEGETABLE?", int(100 * ease_back(a / 0.4)))


def plate(frame, items, cx=960, cy=870, big=False):
    d = ImageDraw.Draw(frame)
    w, h = (820, 250) if big else (760, 220)
    d.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(255, 255, 255), outline=INK, width=6)
    d.ellipse((cx - w / 2 + 40, cy - h / 2 + 22, cx + w / 2 - 40, cy + h / 2 - 22), outline=(220, 225, 235), width=6)
    n = len(items)
    for i, (k, _) in enumerate(items):
        ang = math.pi + (i + 0.5) / max(1, n) * math.pi
        x = cx + math.cos(ang) * (w / 2 - 110) * 0.95
        y = cy + 15 + math.sin(ang) * (h / 2 - 20) * 0.9 + (0 if i % 2 else 30)
        paste(frame, k, x, y, 150 if big else 120)


def scene_plate(frame, s, t):
    plate(frame, s["plate"])
    col = tuple(s["rgb"])
    rt(frame, 960, 120, f"FIND {s['colour'].upper()}!", int(120 * ease_back((t - s["t0"]) / 0.4)), colour=col)
    xs = [570, 830, 1090, 1350]
    for i, k in enumerate(s["items"]):
        x, y, size = xs[i], 430 + 8 * math.sin(t * 2.4 + i), 250 * ease_back((t - s["t0"] - i * 0.1) / 0.4)
        target = k != s["other"]
        if t >= s["show_t"] and target:
            q = (t - s["show_t"]) % 0.9
            y -= 30 * abs(math.sin(q / 0.9 * math.pi)) if t < s["move_t"] else 0
            if t < s["move_t"] + 0.2:
                d = ImageDraw.Draw(frame)
                d.ellipse((x - 150, y - 150, x + 150, y + 150), outline=col, width=14)
        if t >= s["move_t"]:
            k2 = ease_io((t - s["move_t"]) / 0.8)
            if target:
                x, y, size = x + (960 - x) * k2 * 0.6, y + (860 - y) * k2, size * (1 - 0.5 * k2)
            else:
                size *= max(0, 1 - k2 * 1.5)
        if size > 3:
            paste(frame, k, x, y, size)


def scene_plate_done(frame, s, t):
    plate(frame, s["plate"], 960, 620, big=True)
    rt(frame, 960, 150, "EAT THE RAINBOW!", int(130 * ease_back((t - s["t0"]) / 0.4)))
    d = ImageDraw.Draw(frame)
    for j in range(12):
        a = j / 12 * 2 * math.pi + t
        R.star(d, 960 + 520 * math.cos(a), 620 + 260 * math.sin(a), 22, RAINBOW[j % 6], rot=t * 2)


def scene_rhyme(frame, s, t):
    cur = None
    for i, (t0, key, text) in enumerate(s["lines"]):
        if t >= t0:
            cur = (i, t0, key, text)
    if cur is None:
        return
    i, t0, key, text = cur
    clap = abs(math.sin((t - t0) * math.pi / 0.3)) if t - t0 < 0.6 else 0
    if key:
        spotlight(frame, 960, 520, 250)
        paste(frame, key, 960, 520 - 20 * clap, 420 * ease_back((t - t0) / 0.35))
    else:
        for j, k in enumerate(("apple", "banana", "grapes", "orange", "carrot", "broccoli")):
            paste(frame, k, 560 + j * 160, 520 - 40 * abs(math.sin(t * 5 + j)), 200)
    rt(frame, 960, 150, text.upper().rstrip("!"), int(100 * ease_back((t - t0) / 0.3)), maxw=1300)


def scene_cook(frame, s, t):
    dish = s["dish"]
    cx, cy = 960, 760
    wob = 6 * math.sin(t * 14) if s.get("stir_t") and s["stir_t"] <= t < s["stir_t"] + 1.6 else 0
    inside = [k for k, dt in zip(s["items"], s["drops"]) if t >= dt + 0.5]
    for i, k in enumerate(inside):                                     # food peeking out of the dish
        paste(frame, k, cx - 160 + i * 80, cy - 140 + (i % 2) * 20, 150, 10 * math.sin(t * 3 + i))
    paste(frame, dish, cx + wob, cy, 520)
    for k, dt in zip(s["items"], s["drops"]):                          # falling in
        q = t - dt
        if 0 <= q < 0.5:
            paste(frame, k, cx, -120 + (cy - 160 + 120) * ease_io(q / 0.5), 240, q * 300)
    if dish == "pot":
        d = ImageDraw.Draw(frame)
        for j in range(4):
            p = (t * 0.5 + j / 4) % 1
            x = cx - 120 + j * 80 + 20 * math.sin(t * 2 + j)
            y = cy - 280 - p * 260
            r = 30 + 40 * p
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(200 * (1 - p))))
    rt(frame, 960, 150, "FRUIT SALAD!" if dish == "bowl" else "VEGETABLE SOUP!", int(120 * ease_back((t - s["t0"]) / 0.4)))
    if s.get("stir_t") and t >= s["stir_t"]:
        d = ImageDraw.Draw(frame)
        ang = (t - s["stir_t"]) * 6
        sx, sy = cx + 90 * math.cos(ang), cy - 170 + 25 * math.sin(ang)
        d.line((sx, sy, sx + 60, sy - 260), fill=(150, 100, 60), width=22)
        d.ellipse((sx - 30, sy - 22, sx + 30, sy + 22), fill=(150, 100, 60), outline=INK, width=4)


def scene_intro(frame, s, t):
    rt(frame, 960, 150, "GUL & MISHU", int(140 * ease_back(t / 0.6)))
    if t > 0.6:
        rt(frame, 960, 300, "FRUITS & VEGETABLES!", int(95 * ease_back((t - 0.6) / 0.5)), colour=(255, 255, 255))
    for i, k in enumerate(("apple", "carrot", "banana", "broccoli", "grapes", "corn", "guava", "tomato")):
        x = ((t * 180 + i * 240) % 2200) - 140
        paste(frame, k, x, 560 - 30 * abs(math.sin(t * 4 + i)), 190)
    basket(frame, [], 960, 905)


def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    rt(frame, 960, 380, s["title"], int(150 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1300)


def scene_outro(frame, s, t):
    basket(frame, s["basket"], 960, 640, 520)
    if t >= s["bye_t"]:
        rt(frame, 960, 180, "BYE BYE!", int(170 * ease_back((t - s["bye_t"]) / 0.4)))
    else:
        rt(frame, 960, 180, "YUMMY & HEALTHY!", int(120 * ease_back((t - s["t0"]) / 0.4)))


SCENES = {"size": scene_size, "shadow": scene_shadow, "fruit": scene_fruit, "veg": scene_veg, "sort": scene_sort, "plate": scene_plate, "plate_done": scene_plate_done,
          "rhyme": scene_rhyme, "cook": scene_cook, "intro": scene_intro, "title": scene_title, "outro": scene_outro}


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    SCENES[sc["kind"]](frame, sc, t)
    R.stars_burst(frame, t)
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
    dst = OUT / f"Fruits and Vegetables for Kids {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks" / "list.txt"),
                    "-i", str(HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
