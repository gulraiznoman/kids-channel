"""Three DIFFERENT thumbnail layouts for L18 Days, L19 Santa, L20 Cooking.  python tools/thumbs_18_20.py
Days: 7 rainbow day-stripes, title box on top.  Santa: giant Santa hero + red diagonal ribbon, bright snow day.
Cooking: top-down giant pizza on checked tablecloth, chef kids on the right, chalkboard title."""
import math, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

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


def kid(fr, name, emo, outfit, x, h, flip=False, bottom=H + 40, wave=True):
    c = face_char(name, emo, outfit, wave)
    k = h / c.height
    c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    if flip:
        c = c.transpose(Image.FLIP_LEFT_RIGHT)
    c = TF.outlined(c, 8)
    fr.alpha_composite(c, (int(x - c.width / 2), int(bottom - c.height)))
    return c


def text_outline(fr, cx, cy, s, size, colour=None, maxw=1200):
    R.G["fonts"] = {}
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0))
    R.rainbow_text(lay, cx, cy, s, size, colour=colour, maxw=maxw)
    fr.alpha_composite(TF.outlined(lay, 8))


def paste(fr, p, size, x, y, rot=0, ol=7, flip=False):
    im = TF.load(p, size)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = TF.outlined(im, ol)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))


def save(fr, out):
    o = ImageEnhance.Color(fr.convert("RGB")).enhance(1.15)
    o = ImageEnhance.Contrast(o).enhance(1.06)
    out.parent.mkdir(parents=True, exist_ok=True)
    o.save(out, quality=95)
    print("wrote", out)


# ---------------------------------------------------------------- L18 DAYS: seven rainbow stripes
def days():
    cols = [(232, 53, 46), (255, 140, 26), (245, 196, 30), (59, 170, 74), (46, 120, 230), (140, 80, 210), (240, 90, 160)]
    fr = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(fr)
    sw = W / 7
    for i, c in enumerate(cols):
        d.rectangle((i * sw, 0, (i + 1) * sw, H), fill=c)
        d.rectangle((i * sw, 0, i * sw + 6, H), fill=(255, 255, 255))
    for i, lab in enumerate(("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")):
        R.G["fonts"] = {}
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        R.rainbow_text(lay, i * sw + sw / 2, 255, lab, 62, colour=(255, 255, 255), maxw=sw - 14)
        fr.alpha_composite(TF.outlined(lay, 6))
    paste(fr, ROOT / "long18-days/art/item_calendar.png", 300, 640, 470, rot=-6, ol=9)
    kid(fr, "gul", "excited", "bluetee", 230, 470)
    kid(fr, "misheal", "excited", "pink", 1050, 470, flip=True)
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((90, 22, W - 90, 190), radius=40, fill=(255, 255, 255), outline=INK, width=10)
    text_outline(fr, 640, 106, "DAYS OF THE WEEK", 104, maxw=1060)
    save(fr, ROOT / "VIDEOS/L18 Days of the Week/THUMBNAIL v1.jpg")


# ---------------------------------------------------------------- L19 SANTA: giant santa, red ribbon, bright snow
def santa():
    A = ROOT / "long19-santa/art"
    yy = np.linspace(0, 1, H)[:, None, None]
    bg = (np.array([110, 190, 255]) * (1 - yy) + np.array([215, 238, 255]) * yy)
    fr = Image.fromarray(np.repeat(bg.astype(np.uint8), W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(fr)
    for i in range(16):
        a = i / 16 * 2 * math.pi
        d.polygon([(760, 420), (760 + 1100 * math.cos(a), 420 + 1100 * math.sin(a)), (760 + 1100 * math.cos(a + 0.17), 420 + 1100 * math.sin(a + 0.17))],
                  fill=(150, 210, 255))
    rng = np.random.default_rng(9)
    for _ in range(60):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(4, 10)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))
    d.ellipse((-300, 580, W + 300, 1000), fill=(255, 255, 255), outline=INK, width=8)
    paste(fr, A / "item_santa.png", 640, 800, 400, ol=10)
    paste(fr, A / "item_reindeer.png", 300, 1140, 560, ol=8, flip=True)
    paste(fr, ROOT / "long17-xmastree/art/item_present1.png", 150, 470, 640, rot=-8, ol=6)
    paste(fr, ROOT / "long17-xmastree/art/item_present2.png", 130, 1110, 330, rot=10, ol=6)
    kid(fr, "misheal", "excited", "pink", 230, 520)
    rib = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rib)
    rd.polygon([(-40, 30), (760, 30), (720, 200), (-40, 200)], fill=(220, 30, 40), outline=(255, 255, 255))
    rd.line((-40, 40, 757, 40), fill=(255, 255, 255), width=8)
    rd.line((-40, 190, 723, 190), fill=(255, 255, 255), width=8)
    fr.alpha_composite(rib)
    text_outline(fr, 360, 115, "SANTA CLAUS!", 110, colour=(255, 230, 60), maxw=680)
    save(fr, ROOT / "VIDEOS/L19 Santa Christmas Eve/THUMBNAIL v1.jpg")


# ---------------------------------------------------------------- L20 COOKING: top-down pizza on check cloth
def cooking():
    spec = __import__("importlib.util").util.spec_from_file_location("l20r", ROOT / "long20-cooking" / "render.py")
    R20 = __import__("importlib.util").util.module_from_spec(spec)
    spec.loader.exec_module(R20)
    K = R20.K
    K.G["item"] = {k: Image.open(p).convert("RGBA") for k, p in R20.ART.items()}
    K.G["sized"] = {}
    fr = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(fr)
    s = 80
    for y in range(0, H, s):
        for x in range(0, W, s):
            if (x // s + y // s) % 2 == 0:
                d.rectangle((x, y, x + s, y + s), fill=(235, 70, 70))
            elif (x // s) % 2 == 0 or (y // s) % 2 == 0:
                d.rectangle((x, y, x + s, y + s), fill=(255, 190, 190))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    R20.pizza(lay, 440, 430, 330, tops=(5, 4, 3), slices=8)
    fr.alpha_composite(TF.outlined(lay, 9))
    paste(fr, ROOT / "long20-cooking/art/item_rollingpin.png", 300, 170, 640, rot=25, ol=7)
    paste(fr, ROOT / "long20-cooking/art/item_smoothie.png", 200, 830, 590, rot=-8, ol=7)
    c = face_char("gul", "excited", "bluetee")
    k = 430 / c.height
    c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    hat = TF.load(ROOT / "long20-cooking/art/item_chefhat.png", int(c.width * 0.85))
    c2 = Image.new("RGBA", (c.width, c.height + int(hat.height * 0.6)), (0, 0, 0, 0))
    c2.alpha_composite(c, (0, int(hat.height * 0.6)))
    c2.alpha_composite(hat, ((c.width - hat.width) // 2 - 15, 0))
    c2 = TF.outlined(c2, 8)
    fr.alpha_composite(c2, (1060 - c2.width // 2, H + 40 - c2.height))
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((760, 14, 1260, 190), radius=30, fill=(40, 60, 50), outline=(160, 110, 60), width=14)
    text_outline(fr, 1010, 102, "LET'S COOK!", 100, colour=(255, 220, 60), maxw=460)
    save(fr, ROOT / "VIDEOS/L20 Cooking for Kids/THUMBNAIL v1.jpg")


if __name__ == "__main__":
    days(); santa(); cooking()
    ims = [Image.open(ROOT / f"VIDEOS/{d}/THUMBNAIL v1.jpg").resize((640, 360)) for d in ("L18 Days of the Week", "L19 Santa Christmas Eve", "L20 Cooking for Kids")]
    sh = Image.new("RGB", (1920, 360))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 640, 0))
    sh.save(ROOT / "tools/_thumbs_18_20.png")
