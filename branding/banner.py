"""YouTube channel banner 2560x1440. Safe area (all devices): centre 1546x423 -> x 507-2053, y 508-931."""
import math, pathlib, random, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "ep01-fruits"))
import render as R                                   # reuse text helpers
R.G["fonts"] = {}

W, H = 2560, 1440
SAFE = (507, 508, 2053, 931)
KIT = ROOT / "characters" / "layers"
FRUIT = ROOT / "ep01-fruits" / "art"


def kid(name, eyes, mouth, arm, height):
    girl = name == "misheal"
    o = "yellow" if girl else "tee"
    order = (["hair_back"] if girl else []) + [f"body_{o}", f"arm_l_{o}",
             f"arm_r_{'wave' if arm == 'wave' else 'down'}_{o}", "neck", "head", f"eyes_{eyes}", "brows",
             f"mouth_{mouth}", "hair_front"] + (["earrings"] if girl else [])
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    for n in order:
        im.alpha_composite(Image.open(KIT / name / f"{n}.png"))
    im = im.crop(im.getbbox())
    s = height / im.height
    return im.resize((int(im.width * s), height), Image.LANCZOS)


def glow(im, rad=10):
    a = im.split()[3].filter(ImageFilter.MaxFilter(rad * 2 + 1))
    g = Image.new("RGBA", im.size, (255, 255, 255, 0))
    g.putalpha(a)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(im)
    return out


def background():
    sky = Image.new("RGBA", (W, H))
    top, bot = (110, 190, 255), (205, 238, 255)
    px = sky.load()
    for y in range(H):
        k = y / H
        c = tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)) + (255,)
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(sky)
    # big rainbow behind the title
    cols = [(255, 77, 109), (255, 159, 28), (255, 210, 63), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
    for k, col in enumerate(cols):
        r = 980 - k * 46
        d.ellipse((W / 2 - r, 1180 - r, W / 2 + r, 1180 + r), outline=col, width=46)
    # sun + clouds
    d.ellipse((2250, 90, 2450, 290), fill=(255, 224, 102))
    rnd = random.Random(2)
    for cx, cy, s in ((260, 260, 1.3), (900, 170, 1.0), (1700, 230, 1.1), (2350, 520, 0.9), (180, 620, 0.8)):
        for dx, dy, rx, ry in ((0, 0, 120, 60), (-90, 22, 80, 50), (95, 20, 90, 54), (12, -40, 80, 56)):
            d.ellipse((cx + (dx - rx) * s, cy + (dy - ry) * s, cx + (dx + rx) * s, cy + (dy + ry) * s), fill=(255, 255, 255))
    # hills + grass
    d.ellipse((-400, 900, 1500, 1700), fill=(155, 219, 107))
    d.ellipse((1100, 880, 3000, 1700), fill=(155, 219, 107))
    d.rectangle((0, 1000, W, H), fill=(124, 203, 79))
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(1010, 1420)
        col = rnd.choice([(255, 107, 139), (255, 210, 63), (255, 255, 255), (181, 123, 255), (255, 159, 67)])
        r = rnd.uniform(10, 16)
        for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            d.ellipse((x + ox * r - r, y + oy * r - r, x + ox * r + r, y + oy * r + r), fill=col)
        d.ellipse((x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8), fill=(255, 184, 0))
    return sky


def build(path, guides=False):
    im = background()
    # fruits in the desktop-visible band, outside the phone safe area
    for key, x, y, s, r in (("apple", 250, 640, 190, -12), ("banana", 380, 820, 180, 18), ("grapes", 120, 840, 170, 0),
                            ("strawberry", 2320, 640, 170, 10), ("watermelon", 2200, 830, 200, -6), ("mango", 2450, 840, 170, 20)):
        f = Image.open(FRUIT / f"fruit_{key}.png").resize((s, s), Image.LANCZOS).rotate(r, resample=Image.BICUBIC)
        im.alpha_composite(glow(f, 6), (x - s // 2, y - s // 2))
    # kids inside the safe area
    g = glow(kid("gul", "open", "open", "wave", 400)).transpose(Image.FLIP_LEFT_RIGHT)   # wave outward on the left
    m = glow(kid("misheal", "closed", "open", "wave", 400))
    im.alpha_composite(g, (SAFE[0] + 10, SAFE[3] - g.height + 4))
    im.alpha_composite(m, (SAFE[2] - m.width - 10, SAFE[3] - m.height + 4))
    # title + tagline
    R.rainbow_text(im, W / 2, 645, "GUL & MISHU", 138)
    R.plain_text(im, W / 2, 810, "Learn, Sing & Play!", 72, fill=(255, 255, 255))
    if guides:
        d = ImageDraw.Draw(im)
        d.rectangle(SAFE, outline=(255, 0, 0), width=6)
        d.rectangle((0, 508, W, 931), outline=(0, 0, 255), width=4)
    im.convert("RGB").save(path, quality=92)


if __name__ == "__main__":
    build(HERE / "CHANNEL BANNER.jpg")
    build(HERE / "_banner_guides.jpg", guides=True)
    # how it looks on each device
    full = Image.open(HERE / "CHANNEL BANNER.jpg")
    phone = full.crop(SAFE).resize((773, 211))
    desk = full.crop((0, 508, W, 931)).resize((1280, 211))
    sheet = Image.new("RGB", (1280, 640 + 211 * 2 + 40), "white")
    sheet.paste(Image.open(HERE / "_banner_guides.jpg").resize((1280, 720)).crop((0, 40, 1280, 680)), (0, 0))
    sheet.paste(desk, (0, 650))
    sheet.paste(phone, (253, 650 + 211 + 20))
    sheet.save(HERE / "_banner_check.png")
    print("ok")
