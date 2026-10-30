"""v2 renderer: calm, clear, one vehicle at a time (name, what it does, its sound).

python render_edu.py frames 60,200,...   -> preview PNGs
python render_edu.py video               -> VIDEOS/S02 Vehicle Sounds/Vehicles for Kids - Short vN.mp4
"""
import json, math, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw
import render as R

W, H, FPS = R.W, R.H, R.FPS
INK = R.INK
SOUND_TEXT = {"firetruck": "WEE-OO!", "police": "WEE-OO!", "ambulance": "WEE-OO!", "bus": "BEEP BEEP!", "train": "CHOO-CHOO!"}
LIGHTS = {"firetruck": (0.33, -0.22), "police": (0.0, -0.36), "ambulance": (0.0, -0.42)}
STAGE_Y, SIZE = 1060, 640
G = R.G


def plain_text(img, cx, cy, text, size, fill=(255, 255, 255), stroke=INK):
    d = ImageDraw.Draw(img)
    f = R.font(size)
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, cy - size * 0.62), text, font=f, fill=fill, stroke_width=max(1, int(size * 0.12)), stroke_fill=stroke)


def star(d, cx, cy, r, col, rot=0.0):
    pts = []
    for k in range(10):
        a = rot + k * math.pi / 5 - math.pi / 2
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=INK, width=4)


R.plain_text, R.star = plain_text, star


def init():
    R.init()
    D = json.load(open(R.HERE / "edu.json"))
    G.update(D)
    G["edu_total"] = D["total"]
    for s in D["segs"]:
        G["art"].setdefault(s["key"], Image.open(R.ART / f"fruit_{s['key']}.png").convert("RGBA"))
    G["bgs"] = {}


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def background(col):
    """Soft sky in the vehicle's colour, white glow, simple road."""
    if col not in G["bgs"]:
        top = np.array(col, float)
        bot = np.array((255, 255, 255), float)
        y = np.linspace(0, 1, H)[:, None, None]
        img = (top * (1 - y * 0.75) + bot * y * 0.75).astype(np.uint8)
        im = Image.fromarray(np.repeat(img, W, axis=1)).convert("RGBA")
        d = ImageDraw.Draw(im)
        d.rectangle((0, 1250, W, 1420), fill=(96, 104, 120))
        d.rectangle((0, 1240, W, 1252), fill=(200, 205, 215))
        d.rectangle((0, 1420, W, 1440), fill=(200, 205, 215))
        for x in range(-40, W, 160):
            d.rounded_rectangle((x, 1328, x + 90, 1342), radius=6, fill=(255, 255, 255))
        d.rectangle((0, 1440, W, H), fill=(140, 214, 110))
        G["bgs"][col] = im
    return G["bgs"][col].copy()


def bubble(frame, cx, cy, r, k):
    s = r * R.ease_back(k)
    if s < 2:
        return 0
    d = ImageDraw.Draw(frame)
    d.ellipse((cx - s - 8, cy - s - 8, cx + s + 8, cy + s + 8), fill=INK)
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=(255, 255, 255))
    return s


def icon(frame, kind, cx, cy, s, t):
    """Simple picture of what the vehicle does, drawn inside the bubble (s = bubble radius)."""
    d = ImageDraw.Draw(frame)
    u = s / 100
    if kind == "fire":                               # flame being put out by falling water drops
        fl = 1 - min(1, max(0, (t - G["_t_job"] - 0.6) / 1.2)) * 0.6
        fw, fh = 46 * u * fl, 70 * u * fl
        d.polygon([(cx, cy + 50 * u - fh * 2), (cx + fw, cy + 50 * u - fh * 0.6), (cx + fw * 0.7, cy + 50 * u),
                   (cx - fw * 0.7, cy + 50 * u), (cx - fw, cy + 50 * u - fh * 0.6)], fill=(255, 120, 30), outline=INK)
        d.polygon([(cx, cy + 50 * u - fh * 1.2), (cx + fw * 0.5, cy + 50 * u - fh * 0.3), (cx, cy + 50 * u),
                   (cx - fw * 0.5, cy + 50 * u - fh * 0.3)], fill=(255, 210, 60))
        for j in range(5):
            p = ((t * 1.6) + j / 5) % 1
            x = cx - 50 * u + j * 25 * u
            y = cy - 75 * u + p * 90 * u
            d.ellipse((x - 9 * u, y - 12 * u, x + 9 * u, y + 12 * u), fill=(60, 150, 255), outline=INK)
    elif kind == "badge":                            # gold star badge
        R.star(d, cx, cy, 70 * u, (255, 200, 40), rot=0.15 * math.sin(t * 3))
        d.ellipse((cx - 20 * u, cy - 20 * u, cx + 20 * u, cy + 20 * u), fill=(255, 235, 140), outline=INK, width=3)
    elif kind == "heart":                            # beating heart with a white cross
        p = 1 + 0.1 * max(0, math.sin(t * 7))
        r = 34 * u * p
        d.ellipse((cx - 2 * r, cy - 1.6 * r, cx, cy + 0.2 * r), fill=(240, 60, 80), outline=INK, width=4)
        d.ellipse((cx, cy - 1.6 * r, cx + 2 * r, cy + 0.2 * r), fill=(240, 60, 80), outline=INK, width=4)
        d.polygon([(cx - 1.95 * r, cy - 0.4 * r), (cx + 1.95 * r, cy - 0.4 * r), (cx, cy + 1.9 * r)], fill=(240, 60, 80))
        d.rectangle((cx - 1.95 * r + 3, cy - 0.85 * r, cx + 1.95 * r - 3, cy - 0.4 * r), fill=(240, 60, 80))
        d.rectangle((cx - 9 * u, cy - 40 * u, cx + 9 * u, cy + 10 * u), fill=(255, 255, 255))
        d.rectangle((cx - 25 * u, cy - 24 * u, cx + 25 * u, cy - 6 * u), fill=(255, 255, 255))
    elif kind == "abc":                              # letter blocks for school
        for j, (ch, col) in enumerate((("A", (255, 90, 110)), ("B", (60, 170, 255)), ("C", (80, 200, 100)))):
            x = cx - 62 * u + j * 62 * u
            y = cy + 8 * u - 10 * u * abs(math.sin(t * 4 + j))
            d.rounded_rectangle((x - 28 * u, y - 28 * u, x + 28 * u, y + 28 * u), radius=int(8 * u), fill=col, outline=INK, width=3)
            f = R.font(max(8, int(40 * u)))
            w = d.textlength(ch, font=f)
            d.text((x - w / 2, y - 26 * u), ch, font=f, fill=(255, 255, 255))
    elif kind == "tracks":                           # railway track
        for j in range(5):
            y = cy - 60 * u + j * 30 * u
            d.rounded_rectangle((cx - 60 * u, y - 7 * u, cx + 60 * u, y + 7 * u), radius=4, fill=(150, 100, 60), outline=INK)
        for x in (cx - 32 * u, cx + 32 * u):
            d.rectangle((x - 6 * u, cy - 80 * u, x + 6 * u, cy + 80 * u), fill=(140, 150, 165), outline=INK)


def sound_burst(frame, cx, cy, text, k):
    """Comic 'sound' burst while the real sound plays."""
    if not 0 <= k <= 1.2:
        return
    s = R.ease_back(min(1, k / 0.25))
    d = ImageDraw.Draw(frame)
    r = 175 * s
    pts = []
    for q in range(24):
        a = q * math.pi / 12
        rr = r if q % 2 == 0 else r * 0.78
        pts.append((cx + rr * 1.35 * math.cos(a), cy + rr * 0.8 * math.sin(a)))
    if r > 5:
        d.polygon(pts, fill=(255, 235, 80), outline=INK, width=6)
        R.rainbow_text(frame, cx, cy + 10, text, int(80 * s) or 1, colour=(255, 80, 60))


def lights(frame, key, cx, cy, t, flip):
    if key not in LIGHTS:
        return
    lx, ly = LIGHTS[key]
    lx = -lx if flip else lx
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    on = int(t * 6) % 2
    for j, col in enumerate(((255, 40, 40), (40, 110, 255))):
        x, y = cx + lx * SIZE + (-40 if j == 0 else 40), cy + ly * SIZE
        r = 60 if j == on else 26
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (140 if j == on else 80,))
        if j == on:
            d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(255, 255, 255, 230))
    frame.alpha_composite(layer)


def steam(frame, cx, cy, t, t0):
    d = ImageDraw.Draw(frame)
    for j in range(5):
        p = ((t - t0) * 0.9 + j / 5) % 1
        x = cx + SIZE * 0.25 - p * 120
        y = cy - SIZE * 0.42 - p * 300
        r = 26 + 50 * p
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(220 * (1 - p))))


def vehicle(frame, s, t):
    key = s["key"]
    a = G["art"][key]
    flip = not R.song.FACES_RIGHT.get(key, True) if hasattr(R.song, "FACES_RIGHT") else False
    if key == "train":
        flip = True
    if flip:
        a = a.transpose(Image.FLIP_LEFT_RIGHT)
    cx, cy = W / 2, STAGE_Y
    if t < s["t_name"]:                              # drive in from the left and stop
        cx = -SIZE / 2 + (W / 2 + SIZE / 2) * ease_out((t - s["t0"]) / 0.9)
    elif t > s["t_out"]:                             # drive away to the right
        k = (t - s["t_out"]) / 0.55
        cx = W / 2 + k * k * (W / 2 + SIZE)
    bounce = 6 * abs(math.sin(t * 9)) if (t < s["t_name"] or t > s["t_out"]) else 3 * abs(math.sin(t * 3))
    sx = sy = 1.0
    if s["t_sound"] <= t < s["t_out"]:
        k = t - s["t_sound"]
        if key == "bus":                            # honk squash on each beep
            if (k < 0.15) or (0.3 <= k < 0.45):
                sx, sy = 1.06, 0.94
        else:
            bounce += 4 * abs(math.sin(t * 14))
    if key == "train" and t >= s["t0"]:
        steam(frame, cx, cy, t, s["t0"])
    R.shadow(frame, cx, cy + SIZE * 0.25, SIZE * 0.8)
    R.paste_center(frame, a, cx, cy - bounce, SIZE, 0, sx, sy)
    if s["t_sound"] <= t < s["t_out"] or (key in LIGHTS and t >= s["t_job"]):
        lights(frame, key, cx, cy - bounce, t, flip)


def kids(frame, t, talking_bob=True):
    for n, c in R.CHAR.items():
        im = R.compose_char(n, t)
        env = G["env"][n]
        v = env[min(int(t * FPS), len(env) - 1)]
        hop = 10 * abs(math.sin(t * 4)) if v > 0.15 else 3 * abs(math.sin(t * 1.5 + (1 if n == "gul" else 0)))
        frame.alpha_composite(im, (int(c["x"] - im.width / 2), int(1885 - im.height - hop)))


def render_frame(f):
    t = f / FPS
    segs = G["segs"]
    cur = next((s for s in segs if s["t0"] <= t < s["t1"]), None)
    if t < G["intro_end"] or cur is None and t < segs[0]["t0"]:
        frame = background((255, 236, 200))
        k = t / 0.5
        R.rainbow_text(frame, W / 2, 420, "VEHICLES", int(190 * R.ease_back(k)) or 1, start=0.2, t=t)
        R.plain_text(frame, W / 2, 610, "for kids", int(90 * R.ease_back(k - 0.6)) or 1, fill=(255, 255, 255))
        for i, s in enumerate(segs):                 # parade of all five
            x = ((t * 260 + i * 260) % (W + 400)) - 200
            R.paste_center(frame, G["art"][s["key"]].transpose(Image.FLIP_LEFT_RIGHT) if s["key"] == "train" else G["art"][s["key"]],
                           x, 1180 - 6 * abs(math.sin(t * 8 + i)), 250)
    elif cur is not None:
        frame = background(tuple(cur["col"]))
        G["_t_job"] = cur["t_job"]
        vehicle(frame, cur, t)
        if t >= cur["t_name"]:                       # name stays up once said
            R.rainbow_text(frame, W / 2, 300, cur["name"], int(150 * R.ease_back((t - cur["t_name"]) / 0.35)) or 1,
                           start=cur["t_name"], t=t)
        if t >= cur["t_job"] and t < cur["t_out"] + 0.3:
            k = (t - cur["t_job"]) / 0.35 if t < cur["t_out"] else 1 - (t - cur["t_out"]) / 0.3
            r = bubble(frame, W / 2, 600, 170, k)
            if r > 20:
                icon(frame, cur["icon"], W / 2, 600, r, t)
        if cur["t_sound"] <= t < cur["t_out"]:
            sound_burst(frame, W / 2 + 230, 820, SOUND_TEXT[cur["key"]], t - cur["t_sound"])
    else:                                            # outro: line-up with names
        frame = background((230, 225, 255))
        k = t - G["outro"]
        pos = [(270, 600), (810, 600), (270, 920), (810, 920), (540, 1210)]
        for i, (s, (x, y)) in enumerate(zip(segs, pos)):
            g = R.ease_back((k - i * 0.15) / 0.4)
            if g > 0:
                art = G["art"][s["key"]].transpose(Image.FLIP_LEFT_RIGHT) if s["key"] == "train" else G["art"][s["key"]]
                R.paste_center(frame, art, x, y - 8 * abs(math.sin(t * 3 + i)), 330 * g)
                R.plain_text(frame, x, y + 140, s["name"].replace("BIG ", "").title(), int(50 * g) or 1, fill=(255, 255, 255))
        bye = next(e for e in G["events"] if e["text"] == "Bye bye!")["t"]
        R.rainbow_text(frame, W / 2, 330, "BYE BYE!" if t >= bye else "WHICH ONE?",
                       int(140 * R.ease_back((t - (bye if t >= bye else G["outro"] + 0.6)) / 0.35)) or 1)
    kids(frame, t)
    return frame.convert("RGB")


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
            render_frame(f).save(R.HERE / f"_e{f:04d}.png")
        sys.exit()
    n = int(G["edu_total"] * FPS)
    NW = int(os.environ.get("NW", "4"))
    bnd = np.linspace(0, n, NW + 1).astype(int)
    (R.HERE / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(R.HERE / "_chunks" / f"e{k}.mp4")) for k in range(NW)]
    with Pool(NW, initializer=worker_init) as pool:
        parts = pool.map(render_chunk, jobs)
    with open(R.HERE / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    R.OUT.mkdir(parents=True, exist_ok=True)
    dst = R.OUT / f"Vehicles for Kids - Short {os.environ.get('VER', 'v2')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(R.HERE / "_chunks" / "list.txt"),
                    "-i", str(R.HERE / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
