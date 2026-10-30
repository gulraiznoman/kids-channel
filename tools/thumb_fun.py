"""Exciting long-video thumbnails (1280x720), the style he approved on 2026-10-20:
two-colour sunburst + warm glow, Gul & Mishu big with happy open mouths HOLDING props in their raised hands,
a mascot/centre piece, stars and bubbles, big rainbow title.

python tools/thumb_fun.py habits|counting|fruits
"""
import importlib.util, math, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "long02-counting"))
import render as R

KIT = ROOT / "characters" / "layers"
W, H = 1280, 720
INK = R.INK
HAND = {"gul": (1034, 786), "misheal": (1018, 793)}              # raised hand on the 1200x2000 character canvas


def outlined(im, width=10):
    m = im.getchannel("A").filter(ImageFilter.MaxFilter(width * 2 + 1))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), m)
    out.alpha_composite(im)
    return out


def load(p, size, rot=0, flip=False):
    im = Image.open(p).convert("RGBA").resize((size, size), Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im


def bubble(d, x, y, r):
    d.ellipse((x - r, y - r, x + r, y + r), fill=(240, 250, 255), outline=(120, 190, 230), width=max(2, int(r / 8)))
    d.ellipse((x - r * 0.55, y - r * 0.6, x - r * 0.15, y - r * 0.25), fill=(255, 255, 255))


def character(name, outfit, prop=None, bubbles=False):
    """Character on its 1200x2000 canvas with `prop` = (png, size, rot, dx, dy) held in the raised hand."""
    girl = name == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    for p in (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}"]:
        im.alpha_composite(Image.open(KIT / name / f"{p}.png"))
    for p in ["neck", "head", "eyes_open", "brows", "mouth_open", "hair_front"] + (["earrings"] if girl else []):
        im.alpha_composite(Image.open(KIT / name / f"{p}.png"))
    im.alpha_composite(Image.open(KIT / name / f"arm_r_wave_{outfit}.png"))   # arm in front so the hand holds the prop
    hx, hy = HAND[name]
    if prop:
        png, size, rot, dx, dy = prop
        pr = outlined(load(png, size, rot), 6)
        im.alpha_composite(pr, (int(hx + dx - pr.width / 2), int(hy + dy - pr.height / 2)))
    if bubbles:
        d = ImageDraw.Draw(im)
        for bx, by, r in ((hx - 60, hy - 120, 45), (hx + 70, hy - 160, 34), (hx + 120, hy - 40, 28), (hx - 120, hy - 30, 26)):
            bubble(d, bx, by, r)
    return im.crop(im.getbbox())


def sunburst(c1, c2, glow=(255, 252, 235), cy=430):
    bg = Image.new("RGB", (W, H), c1)
    d = ImageDraw.Draw(bg)
    cx = W / 2
    for k in range(20):
        a0, a1 = k * 2 * math.pi / 20, (k + 1) * 2 * math.pi / 20
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a0), cy + 1600 * math.sin(a0)), (cx + 1600 * math.cos(a1), cy + 1600 * math.sin(a1))],
                  fill=c2 if k % 2 else c1)
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.clip(1 - np.hypot(xx - cx, (yy - cy) * 1.1) / 420, 0, 1) ** 1.4
    return Image.composite(Image.new("RGB", (W, H), glow), bg, Image.fromarray((g * 255).astype(np.uint8))).convert("RGBA")


def stars_ring(fr, cx, cy, rx, ry, n=10):
    d = ImageDraw.Draw(fr)
    for j in range(n):
        ang = j / n * 2 * math.pi + 0.3
        R.star(d, cx + rx * math.cos(ang), cy + ry * math.sin(ang), 20 if j % 2 else 30, (255, 230, 60))


def place_kids(fr, gul, mishu, scale=0.47):
    mishu = mishu.transpose(Image.FLIP_LEFT_RIGHT)                       # mirror Mishu so her prop hand faces the middle
    for im, x, rot in ((gul, 205, 4), (mishu, 1075, -4)):
        k = scale * 1.0
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        im = outlined(im, 10).rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(im, (int(x - im.width / 2), H - im.height + 175))


def float_bubbles(fr, seed=5, n=20):
    d = ImageDraw.Draw(fr)
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x, y, r = rng.uniform(30, W - 30), rng.uniform(150, 690), rng.uniform(10, 24)
        if abs(x - 640) < 300 and y > 200:
            continue
        if (x < 420 or x > 860) and 120 < y < 520:
            continue
        bubble(d, x, y, r)


def finish(fr, title, out, size=128):
    R.G["fonts"] = {}
    R.rainbow_text(fr, 640, 98, title, size, maxw=1220)
    o = ImageEnhance.Color(fr.convert("RGB")).enhance(1.15)
    o = ImageEnhance.Contrast(o).enhance(1.05)
    o.save(out, quality=95)
    o.resize((640, 360)).save(ROOT / "_t.png")
    print("wrote", out)


# ------------------------------------------------------------------ the three videos
def habits():
    spec = importlib.util.spec_from_file_location("th2", ROOT / "long04-good-habits" / "thumb2.py")
    th2 = importlib.util.module_from_spec(spec)
    sys_argv, sys.argv = sys.argv, ["x"]
    spec.loader.exec_module(th2)
    sys.argv = sys_argv
    A = ROOT / "long04-good-habits" / "art"
    fr = sunburst((60, 200, 230), (255, 214, 70))
    th2.big_tooth(fr, 640, 450, 1.25)
    stars_ring(fr, 640, 450, 280, 230)
    gul = character("gul", "bluetee", (A / "item_toothbrush.png", 430, 150, -215, 30))
    d = ImageDraw.Draw(gul)
    mishu = character("misheal", "pink", (A / "item_soap.png", 230, -10, 0, -40), bubbles=True)
    place_kids(fr, gul, mishu)
    float_bubbles(fr)
    finish(fr, "GOOD HABITS!", ROOT / "VIDEOS" / "L04 Good Habits" / "THUMBNAIL v3.jpg")


def counting():
    fr = sunburst((80, 200, 110), (255, 200, 60))
    d = ImageDraw.Draw(fr)
    R.G["fonts"] = {}
    R.rainbow_text(fr, 640, 420, "123", 300, maxw=900)
    apple = ROOT / "ep01-fruits" / "art" / "fruit_apple.png"
    for i in range(5):                                                   # five apples with number badges
        im = outlined(load(apple, 110), 5)
        x = 640 + (i - 2) * 115
        fr.alpha_composite(im, (int(x - im.width / 2), 575))
        R.badge(fr, x + 38, 590, i + 1, 1.0)
    stars_ring(fr, 640, 450, 300, 220)
    gul = character("gul", "tee", (ROOT / "ep01-fruits" / "art" / "fruit_banana.png", 260, 20, 10, -60))
    mishu = character("misheal", "yellow", (ROOT / "long01-animals-fun" / "art" / "fruit_star.png", 250, 0, 0, -60))
    place_kids(fr, gul, mishu)
    finish(fr, "COUNT TO 10!", ROOT / "VIDEOS" / "L02 Count 1 to 10" / "THUMBNAIL v2.jpg")


def fruits():
    A3 = ROOT / "long03-fruits-veg" / "art"
    fr = sunburst((255, 140, 60), (120, 210, 90))
    basket = Image.new("RGBA", (900, 900), (0, 0, 0, 0))
    for k, x, y, s, rot in (("carrot", 580, 400, 320, 20), ("broccoli", 290, 450, 270, -12), ("pomegranate", 660, 500, 230, 0),
                            ("guava_half", 440, 440, 260, 0), ("corn", 500, 500, 240, 15)):
        im = load(A3 / f"item_{k}.png", s, rot)
        basket.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
    bk = load(A3 / "item_basket.png", 640)
    basket.alpha_composite(bk, (450 - 320, 640 - 320))
    basket = outlined(basket.crop(basket.getbbox()), 8)
    k = 470 / basket.height
    basket = basket.resize((int(basket.width * k), 470), Image.LANCZOS)
    fr.alpha_composite(basket, (640 - basket.width // 2, 205))
    stars_ring(fr, 640, 450, 300, 230)
    gul = character("gul", "bluetee", (A3 / "item_carrot.png", 280, -30, 0, -80))
    mishu = character("misheal", "yellow", (A3 / "item_guava_half.png", 250, 0, 0, -60))
    place_kids(fr, gul, mishu)
    finish(fr, "FRUITS & VEGGIES!", ROOT / "VIDEOS" / "L03 Fruits and Vegetables" / "THUMBNAIL v2.jpg", 118)


def body():
    A5 = ROOT / "long05-body-parts" / "art"
    fr = sunburst((255, 120, 150), (255, 210, 70))
    for k, (name, ang) in enumerate((("eye", -90), ("ear", -18), ("hand", 54), ("mouth", 126), ("nose", 198))):
        a = math.radians(ang)
        x, y = 640 + 200 * math.cos(a), 450 + 165 * math.sin(a)
        im = outlined(load(A5 / f"item_{name}.png", 215), 8)
        fr.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
    stars_ring(fr, 640, 440, 300, 230)
    gul = character("gul", "tee")
    mishu = character("misheal", "yellow")
    place_kids(fr, gul, mishu)
    finish(fr, "BODY PARTS!", ROOT / "VIDEOS" / "L05 Body Parts" / "THUMBNAIL v1.jpg")


def body2():
    A5 = ROOT / "long05-body-parts" / "art"
    fr = sunburst((90, 120, 255), (255, 210, 70))
    for name, x, y, sz, rot in (("brain", 520, 330, 230, -10), ("lungs", 770, 330, 230, 10), ("heart_organ", 640, 520, 300, 0)):
        im = outlined(load(A5 / f"item_{name}.png", sz, rot), 9)
        fr.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
    stars_ring(fr, 640, 450, 310, 240)
    gul = character("gul", "tee", (A5 / "item_muscle.png", 230, 0, 0, -60))
    mishu = character("misheal", "yellow", (A5 / "item_eye.png", 220, 0, 0, -50))
    place_kids(fr, gul, mishu)
    finish(fr, "BODY PARTS!", ROOT / "VIDEOS" / "L05 Body Parts" / "THUMBNAIL v2.jpg")


def dinos():
    A6 = ROOT / "long06-dinosaurs" / "art"
    fr = sunburst((120, 200, 80), (255, 200, 60))
    for name, x, y, sz, rot, fl in (("brachiosaurus", 470, 330, 280, 0, True), ("pteranodon", 820, 250, 230, 8, False),
                                    ("triceratops", 820, 520, 250, 0, False)):
        im = outlined(load(A6 / f"dino_{name}.png", sz, rot, flip=fl), 8)
        fr.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
    eggb = outlined(load(A6 / "item_egg_bottom.png", 300), 8)
    trex = outlined(load(A6 / "dino_trex.png", 330), 9)
    fr.alpha_composite(trex, (640 - trex.width // 2, 330))
    fr.alpha_composite(eggb, (640 - eggb.width // 2, 470))
    stars_ring(fr, 640, 470, 330, 240)
    hat = lambda n: Image.open(A6 / f"hat_{n}.png").convert("RGBA")
    gul = character("gul", "tee")
    mishu = character("misheal", "yellow")
    for im, n in ((gul, "gul"), (mishu, "misheal")):
        pass
    gul_full = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    place_kids_hat(fr, "gul", "tee", "misheal", "yellow", A6)
    finish(fr, "DINOSAURS!", ROOT / "VIDEOS" / "L06 Dinosaurs" / "THUMBNAIL v1.jpg")


def place_kids_hat(fr, g, go, m, mo, A6):
    out = []
    for name, outfit in ((g, go), (m, mo)):
        girl = name == "misheal"
        im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
        for p in (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}", "neck", "head", "eyes_open", "brows", "mouth_open", "hair_front"] + (["earrings"] if girl else []):
            im.alpha_composite(Image.open(KIT / name / f"{p}.png"))
        im.alpha_composite(Image.open(KIT / name / f"arm_r_wave_{outfit}.png"))
        im.alpha_composite(Image.open(A6 / f"hat_{name}.png"))
        out.append(im.crop(im.getbbox()))
    place_kids(fr, out[0], out[1])


def feelings():
    sys.path.insert(0, str(ROOT / "characters"))
    import expressions as EX
    fr = sunburst((255, 120, 170), (255, 205, 60))
    for (n, e, o), (x, y) in zip((("gul", "happy", "bluetee"), ("misheal", "sad", "pink"), ("gul", "angry", "bluetee"), ("misheal", "surprised", "pink")),
                                 ((540, 330), (740, 330), (540, 545), (740, 545))):
        f = EX.face(n, e, o).crop((150, 150, 1050, 1050)).resize((220, 220), Image.LANCZOS)
        f = outlined(f, 7)
        fr.alpha_composite(f, (x - f.width // 2, y - f.height // 2))
    stars_ring(fr, 640, 440, 320, 240)
    out = []
    for n, e, o in (("gul", "excited", "bluetee"), ("misheal", "happy", "pink")):
        im = EX.face(n, e, o)
        im.alpha_composite(Image.open(KIT / n / f"arm_r_wave_{o}.png"))
        out.append(im.crop(im.getbbox()))
    place_kids(fr, out[0], out[1])
    finish(fr, "FEELINGS!", ROOT / "VIDEOS" / "L07 Feelings" / "THUMBNAIL v1.jpg")


def colorshapes():
    spec = importlib.util.spec_from_file_location("l08render", ROOT / "long08-colors-shapes" / "render.py")
    R8 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R8)
    R8.G["shp"] = {}
    A8 = ROOT / "long08-colors-shapes" / "art"
    cr = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cr)
    red, dark = (232, 53, 46), (180, 30, 30)
    dc.polygon([(315, 150), (485, 150), (485, 30), (315, 30)], fill=red, outline=INK, width=8)
    dc.polygon([(315, 150), (485, 150), (485, 620), (315, 620)], fill=red, outline=INK, width=8)
    dc.polygon([(315, 330), (485, 330), (485, 470), (315, 470)], fill=(255, 255, 255), outline=INK, width=6)
    for y in (360, 440):
        dc.line((315, y, 485, y), fill=red, width=12)
    dc.polygon([(315, 620), (485, 620), (400, 775)], fill=red, outline=INK, width=8)
    dc.polygon([(372, 724), (428, 724), (400, 775)], fill=dark)
    cr = cr.crop(cr.getbbox())
    sq = Image.new("RGBA", (cr.height, cr.height), (0, 0, 0, 0))
    sq.alpha_composite(cr, ((cr.height - cr.width) // 2, 0))
    sq.save(A8 / "_crayon_red.png")
    R8.shape_img("star", 400, R8.cv("orange"), True).save(A8 / "_star_face.png")
    fr = sunburst((70, 190, 255), (255, 210, 60))
    R8.rainbow_arcs(fr, 640, 640, 330, 34)
    for c, x, y, r in (("pink", 455, 300, 52), ("green", 840, 290, 46), ("purple", 640, 210, 40)):
        R8.blob(fr, x, y, r, c, seed=int(x))
    for shp, x, y, sz, rot in (("circle", 520, 440, 190, -8), ("square", 760, 440, 190, 8), ("triangle", 640, 560, 200, 0), ("heart", 640, 345, 150, 0)):
        im = outlined(R8.shape_img(shp, sz, R8.cv(R8.SHAPE_COL[shp]), True), 6).rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(im, (x - im.width // 2, y - im.height // 2))
    stars_ring(fr, 640, 440, 330, 250)
    gul = character("gul", "polo", (A8 / "_crayon_red.png", 470, 35, -30, 10))
    mishu = character("misheal", "yellow", (A8 / "_star_face.png", 330, -12, 0, -60))
    place_kids(fr, gul, mishu)
    float_bubbles(fr)
    (ROOT / "VIDEOS" / "L08 Colors and Shapes").mkdir(parents=True, exist_ok=True)
    finish(fr, "COLORS & SHAPES!", ROOT / "VIDEOS" / "L08 Colors and Shapes" / "THUMBNAIL v1.jpg", size=118)


def eggs():
    spec = importlib.util.spec_from_file_location("l09render", ROOT / "long09-eggs" / "render.py")
    R9 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R9)
    R9.G["eggs"] = {}
    A9 = ROOT / "long09-eggs" / "art"
    fr = sunburst((255, 150, 60), (255, 220, 80))
    stars_ring(fr, 640, 430, 330, 250)
    for kind, x, y, sc, rot in (("robin", 430, 690, 0.8, -12), ("dino", 860, 700, 0.5, 10)):
        w2, _, _ = R9.egg_parts(kind, sc)
        w2 = outlined(w2, 6).rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(w2, (x - w2.width // 2, y - w2.height))
    whole, top, bot = R9.egg_parts("plain", 1.15)
    chick = outlined(load(R9.ART["chick"], 340), 8)
    fr.alpha_composite(chick, (640 - chick.width // 2, 470 - chick.height // 2 - 40))
    b = outlined(bot, 7)
    fr.alpha_composite(b, (640 - b.width // 2, 715 - b.height))
    tp = outlined(top, 7).resize((int(top.width * 0.75), int(top.height * 0.75))).rotate(-35, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(tp, (790, 165))
    gul = character("gul", "tee", (A9 / "item_penguin.png", 400, 0, 0, -60))
    mishu = character("misheal", "pink", (A9 / "item_turtle.png", 380, 0, 0, -60))
    place_kids(fr, gul, mishu)
    float_bubbles(fr)
    finish(fr, "WHO'S IN THE EGG?", ROOT / "VIDEOS" / "L09 Whos in the Egg" / "THUMBNAIL v1.jpg", size=120)

def abc():
    spec = importlib.util.spec_from_file_location("l10render", ROOT / "long10-abc" / "render.py")
    R10 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R10)
    R10.R.G["fonts"] = {}
    fr = sunburst((90, 200, 255), (255, 215, 70))
    stars_ring(fr, 640, 440, 340, 250)
    for i, (L, pic) in enumerate((("A", "apple"), ("B", "ball"), ("C", "cat"))):
        x = 500 + i * 140
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        R.G["fonts"] = {}
        R.rainbow_text(lay, x, 360 - (25 if i == 1 else 0), L, 230, colour=R10.lcol(L))
        fr.alpha_composite(outlined(lay, 7))
        pim = outlined(load(R10.ART[pic], 120), 6)
        fr.alpha_composite(pim, (x - 60, 520 - (25 if i == 1 else 0)))
    gul = character("gul", "bluetee", (R10.ART["apple"], 260, 0, 0, -50))
    mishu = character("misheal", "kurta", (R10.ART["ball"], 250, 0, 0, -50))
    place_kids(fr, gul, mishu)
    float_bubbles(fr)
    finish(fr, "ABC PHONICS!", ROOT / "VIDEOS" / "L10 ABC Phonics" / "THUMBNAIL v1.jpg", size=130)


if __name__ == "__main__":
    {"abc": abc, "eggs": eggs, "colorshapes": colorshapes, "feelings": feelings, "dinos": dinos, "habits": habits, "counting": counting, "fruits": fruits, "body": body, "body2": body2}[sys.argv[1]]()
