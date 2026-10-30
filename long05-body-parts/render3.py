"""Body Parts v3 renderer: same timeline/audio as v2, but Gul uses the DETAILED barefoot body (real fingers, thumbs,
elbows, wrists, knees, ankles, toes) and hand/foot/arm/leg parts get a labelled close-up card next to him.

python render3.py frames 100,900,...  -> preview PNGs
python render3.py video               -> VIDEOS/L05 Body Parts/Body Parts for Kids v3.mp4
"""
import importlib.util, math, os, subprocess, sys, pathlib
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bp2", HERE / "render2.py")
V2 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, ["x"]
spec.loader.exec_module(V2)
sys.argv = _argv
sys.path.insert(0, str(HERE))
from art3 import CARD_SPOTS

R, G = V2.R, V2.G
W, H, FPS = R.W, R.H, R.FPS
rt, paste, ease_back = R.rainbow_text, R.paste, R.ease_back

V2.BODY_PTS.update({
    "neck": [(600, 985)], "shoulders": [(420, 1030), (780, 1030)], "chest": [(600, 1110)], "tummy": [(600, 1300)],
    "arms": [(370, 1130), (830, 1130)], "elbows": [(345, 1200), (855, 1200)], "wrists": [(335, 1372), (865, 1372)],
    "hands": [(333, 1440), (867, 1440)], "thumbs": [(385, 1410), (815, 1410)], "fingers": [(333, 1495), (867, 1495)],
    "hips": [(440, 1480), (760, 1480)], "legs": [(515, 1590), (685, 1590)], "knees": [(512, 1655), (688, 1655)],
    "ankles": [(510, 1792), (690, 1792)], "feet": [(480, 1840), (720, 1840)], "toes": [(480, 1878), (720, 1878)]})
V2.ZOOM.update({"hands": (230, 1330, 490, 1590), "knees": (430, 1560, 630, 1760)})
_orig_compose = V2.compose


def compose(name, t, mouth_force=None, arms_down=True, missing=None, waving=False):
    if name != "gul":
        return _orig_compose(name, t, mouth_force, arms_down, missing, waving)
    L = G["full"]["gul"]
    env = G["env"]["gul"]
    v = env[min(int(t * FPS), len(env) - 1)]
    talking = v > 0.12
    mouth = mouth_force or ("smile" if not talking else ("o" if v < 0.5 else "open"))
    eyes = "blink" if (t + 0.7) % 4.3 < 0.12 else "open"
    key = ("gul3", mouth, eyes, missing)
    if key in G["c2"]:
        return G["c2"][key]
    im = G["detail_body"].copy()
    for p in ["neck", "head", f"eyes_{eyes}", "brows", f"mouth_{mouth}"] + ([] if missing == "hair" else ["hair_front"]):
        im.alpha_composite(L[p])
    if missing == "nose":
        ImageDraw.Draw(im).ellipse((560, 715, 640, 780), fill=G["skin"])
    if len(G["c2"]) > 60:
        G["c2"].clear()
    G["c2"][key] = im
    return im


V2.compose = compose


def init():
    V2.init()
    G["detail_body"] = Image.open(HERE / "art" / "gul_body_detail.png").convert("RGBA")
    for n in ("hand", "foot", "arm", "leg"):
        G["art"][f"card_{n}"] = Image.open(HERE / "art" / f"item_card_{n}.png").convert("RGBA")


def body_at(frame, name, t, cx, hop=0.0):
    im = compose(name, t)
    s = 0.48
    sm = im.resize((int(1200 * s), int(2000 * s)), Image.BICUBIC)
    top = 70 - hop
    frame.alpha_composite(sm, (int(cx - 600 * s), int(top)))
    return lambda x, y: (cx + (x - 600) * s, top + y * s)


def card(frame, part, t, t0):
    which, sx, sy = CARD_SPOTS[part]
    k = ease_back((t - t0) / 0.45)
    size = 600 * k
    if size < 4:
        return
    cx, cy = 1390, 560
    paste(frame, f"card_{which}", cx, cy, size, 3 * math.sin(t * 1.5))
    if k >= 0.95:
        px, py = cx + (sx - 200) * 1.5, cy + (sy - 200) * 1.5
        V2.V1.rings(frame, [(px, py)], t, t0 + 0.4, (255, 77, 109))


def scene_body(frame, s, t):
    hop = 22 * abs(math.sin(t * 7)) if s["part"] in ("feet", "toes", "knees", "legs", "hips") and t > s["label_t"] + 1.0 else 0
    has_card = s["part"] in CARD_SPOTS and not s.get("quick")
    cx = 640 if has_card else 960
    m = body_at(frame, s["who"], t, cx, hop)
    V2.V1.rings(frame, [m(*p) for p in V2.BODY_PTS[s["part"]]], t, s["label_t"])
    if has_card:
        card(frame, s["part"], t, s["label_t"] + 0.3)
    rt(frame, 960, 70, s["label"], int((140 if s.get("quick") else 120) * ease_back((t - s["label_t"]) / 0.3)), start=s["label_t"], t=t)
    V2.counter(frame, s)
    V2.fact_line(frame, s, t)


def scene_leftright(frame, s, t):
    m = body_at(frame, s["who"], t, 960)
    pts = V2.BODY_PTS[s["part"]]
    pt = pts[0] if s["side"] == 1 else pts[-1]
    col = (59, 193, 74) if s["side"] == 1 else (46, 168, 255)
    V2.V1.rings(frame, [m(*pt)], t, s["label_t"], col)
    x, y = m(*pt)
    rt(frame, x + (-250 if s["side"] == 1 else 250), y, "RIGHT" if s["side"] == 1 else "LEFT", 80, colour=col)
    rt(frame, 960, 70, s["label"], int(120 * ease_back((t - s["label_t"]) / 0.3)), start=s["label_t"], t=t)


V2.SC["body"] = scene_body
V2.SC["leftright"] = scene_leftright


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(lo, hi):
        p.stdin.write(V2.render_frame(f).tobytes())
    p.stdin.close()
    p.wait()
    return path


if __name__ == "__main__":
    init()
    if sys.argv[1] == "frames":
        for f in [int(x) for x in sys.argv[2].split(",")]:
            V2.render_frame(f).save(HERE / f"_h{f:05d}.png")
        sys.exit()
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "4"))
    parts = 24
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (HERE / "_chunks3").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(HERE / "_chunks3" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(HERE / "_chunks3" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    dst = V2.OUT / f"Body Parts for Kids {os.environ.get('VER', 'v3')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(HERE / "_chunks3" / "list.txt"),
                    "-i", str(HERE / "mix2.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)
