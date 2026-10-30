"""Three DIFFERENT thumbnail layouts for L15 Potty, L16 Sharing, L17 Christmas Tree.  python tools/thumbs_15_17.py"""
import math, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.argv = ["x"]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "characters"))
import thumb_fun as TF
import expressions as EX
R, INK = TF.R, TF.INK
W, H = 1280, 720
KIT = ROOT / "characters" / "layers"


def face_char(name, emo, outfit, wave=True):
    im = EX.face(name, emo, outfit)
    if wave:
        im.alpha_composite(Image.open(KIT / name / f"arm_r_wave_{outfit}.png"))
    return im.crop(im.getbbox())


def text_outline(fr, cx, cy, s, size, colour=None, maxw=1200):
    R.G["fonts"] = {}
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0))
    R.rainbow_text(lay, cx, cy, s, size, colour=colour, maxw=maxw)
    fr.alpha_composite(TF.outlined(lay, 8))


def save(fr, out):
    o = ImageEnhance.Color(fr.convert("RGB")).enhance(1.15)
    o = ImageEnhance.Contrast(o).enhance(1.06)
    out.parent.mkdir(parents=True, exist_ok=True)
    o.save(out, quality=95)
    print("wrote", out)


# ---------------------------------------------------------------- L15 POTTY: big close-up + bottom banner
def potty():
    A = ROOT / "long15-potty/art"
    yy = np.linspace(0, 1, H)[:, None, None]
    bg = (np.array([200, 240, 225]) * (1 - yy) + np.array([150, 220, 200]) * yy)
    fr = Image.fromarray(np.repeat(bg.astype(np.uint8), W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(fr)
    for x in range(0, W, 80):
        d.rectangle((x, 0, x + 40, 560), fill=(185, 232, 214))
    gul = face_char("gul", "proud", "tee")
    k = 700 / gul.height
    gul = TF.outlined(gul.resize((int(gul.width * k), int(gul.height * k)), Image.LANCZOS), 10)
    fr.alpha_composite(gul, (480 - gul.width // 2, 0))
    potty = TF.outlined(TF.load(A / "item_potty.png", 460), 9)
    fr.alpha_composite(potty, (460 - potty.width // 2, 560 - potty.height + 10))
    star = TF.outlined(TF.load(A / "item_star.png", 300), 9).rotate(-12, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(star, (870, -10))
    chart = TF.outlined(TF.load(A / "item_chart.png", 280), 7).rotate(8, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(chart, (930, 250))
    paper = TF.outlined(TF.load(A / "item_paper.png", 170), 6).rotate(-10, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(paper, (60, 330))
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((-20, 560, W + 20, H + 20), radius=0, fill=(255, 77, 109))
    d.rectangle((-20, 560, W + 20, 572), fill=(255, 255, 255))
    text_outline(fr, 640, 640, "POTTY TIME!", 120, colour=(255, 230, 60))
    save(fr, ROOT / "VIDEOS/L15 Potty Training/THUMBNAIL v1.jpg")


# ---------------------------------------------------------------- L16 SHARING: before / after split
def sharing():
    A = ROOT / "long16-sharing/art"
    fr = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(fr)
    d.polygon([(0, 0), (690, 0), (590, H), (0, H)], fill=(255, 110, 110))
    d.polygon([(690, 0), (W, 0), (W, H), (590, H)], fill=(120, 215, 120))
    for i in range(12):
        a = i / 12 * 2 * math.pi
        d.polygon([(960, 400), (960 + 900 * math.cos(a), 400 + 900 * math.sin(a)), (960 + 900 * math.cos(a + 0.2), 400 + 900 * math.sin(a + 0.2))],
                  fill=(140, 225, 140))
    d.polygon([(690, 0), (W, 0), (W, H), (590, H)], outline=None)
    d.polygon([(0, 0), (690, 0), (590, H), (0, H)], fill=(255, 110, 110))
    d.line((690, 0, 590, H), fill=(255, 255, 255), width=18)
    # left: angry tug
    for name, x, flip in (("gul", 130, False), ("misheal", 470, True)):
        c = face_char(name, "angry", "polo" if name == "gul" else "yellow", wave=False)
        k = 520 / c.height
        c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
        if flip:
            c = c.transpose(Image.FLIP_LEFT_RIGHT)
        c = TF.outlined(c, 8)
        fr.alpha_composite(c, (x - c.width // 2, H - c.height + 60))
    ted = TF.outlined(TF.load(ROOT / "long15-potty/art/item_teddy.png", 200), 7).rotate(15, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(ted, (300 - ted.width // 2, 300))
    text_outline(fr, 300, 110, "MINE!", 130, colour=(255, 255, 255), maxw=520)
    # right: happy sharing
    for name, x in (("gul", 830), ("misheal", 1150)):
        c = face_char(name, "excited" if name == "gul" else "happy", "polo" if name == "gul" else "yellow")
        k = 520 / c.height
        c = TF.outlined(c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS), 8)
        fr.alpha_composite(c, (x - c.width // 2, H - c.height + 60))
    heart = TF.outlined(TF.load(A / "item_heart.png", 240), 8)
    fr.alpha_composite(heart, (990 - heart.width // 2, 200))
    cookie = TF.outlined(TF.load(A / "item_cookie.png", 120), 6)
    fr.alpha_composite(cookie, (990 - cookie.width // 2, 430))
    text_outline(fr, 990, 100, "SHARE!", 130, maxw=520)
    d = ImageDraw.Draw(fr)
    d.polygon([(600, 330), (690, 330), (690, 290), (770, 370), (690, 450), (690, 410), (600, 410)], fill=(255, 210, 40), outline=INK, width=6)
    save(fr, ROOT / "VIDEOS/L16 Sharing is Caring/THUMBNAIL v1.jpg")


# ---------------------------------------------------------------- L17 CHRISTMAS: glowing tree at night
def xmas():
    spec = __import__("importlib.util").util.spec_from_file_location("l17r", ROOT / "long17-xmastree" / "render.py")
    R17 = __import__("importlib.util").util.module_from_spec(spec)
    spec.loader.exec_module(R17)
    K = R17.K
    K.G["item"] = {k: Image.open(p).convert("RGBA") for k, p in R17.ART.items()}
    K.G["sized"] = {}
    yy = np.linspace(0, 1, H)[:, None, None]
    bg = (np.array([20, 30, 90]) * (1 - yy) + np.array([60, 40, 120]) * yy)
    fr = Image.fromarray(np.repeat(bg.astype(np.uint8), W, axis=1)).convert("RGBA")
    xx, yv = np.meshgrid(np.arange(W), np.arange(H))
    g = np.clip(1 - np.hypot(xx - 640, (yv - 420) * 1.2) / 430, 0, 1) ** 1.6
    glow = Image.new("RGBA", (W, H), (255, 200, 90, 0))
    glow.putalpha(Image.fromarray((g * 220).astype(np.uint8)))
    fr.alpha_composite(glow)
    d = ImageDraw.Draw(fr)
    rng = np.random.default_rng(5)
    for _ in range(90):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 6)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))
    d.ellipse((-200, 640, W + 200, 900), fill=(240, 246, 255))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    R17.tree(lay, 640, 700, 560, 0.4)
    fr.alpha_composite(TF.outlined(lay, 7))
    for i, p in enumerate(("present1", "present2", "present3")):
        im = TF.outlined(TF.load(R17.ART[p], 120), 5)
        fr.alpha_composite(im, (500 + i * 120, 620))
    for name, x, outfit in (("gul", 150, "bluetee"), ("misheal", 1130, "pink")):
        c = face_char(name, "excited", outfit)
        k = 430 / c.height
        c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
        if name == "misheal":
            c = c.transpose(Image.FLIP_LEFT_RIGHT)
        c = TF.outlined(c, 8)
        fr.alpha_composite(c, (x - c.width // 2, H - c.height + 40))
    hat = TF.outlined(TF.load(R17.ART["santahat"], 160), 5).rotate(15, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(hat, (62, 212))
    text_outline(fr, 640, 80, "CHRISTMAS TREE!", 110, colour=(255, 215, 70))
    save(fr, ROOT / "VIDEOS/L17 Christmas Tree/THUMBNAIL v1.jpg")


if __name__ == "__main__":
    potty(); sharing(); xmas()
    ims = [Image.open(ROOT / f"VIDEOS/{d}/THUMBNAIL v1.jpg").resize((640, 360)) for d in ("L15 Potty Training", "L16 Sharing is Caring", "L17 Christmas Tree")]
    sh = Image.new("RGB", (1920, 360))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 640, 0))
    sh.save(ROOT / "tools/_thumbs_15_17.png")
