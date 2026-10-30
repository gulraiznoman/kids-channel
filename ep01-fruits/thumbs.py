"""Three thumbnail options (1280x720) for episode 1."""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFilter
import render as R

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "VIDEOS" / "01 Learn Fruits"


def char(name, eyes="open", mouth="open", arm="wave", scale=1.0, glasses=False, wave_amt=0.4):
    im = R.compose_char(name, eyes, mouth, arm, wave_amt)
    if glasses:
        g = R.G["layers"][name]["glasses"]
        im.alpha_composite(g)
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    return im


def fruit(key, size, rot=0):
    f = R.G["fruit"][key].resize((size, size), Image.LANCZOS)
    return f.rotate(rot, resample=Image.BICUBIC, expand=False)


def glow_paste(base, im, xy, glow=(255, 255, 255), rad=10):
    a = im.split()[3].filter(ImageFilter.MaxFilter(rad * 2 + 1)).filter(ImageFilter.GaussianBlur(rad / 2))
    g = Image.new("RGBA", im.size, glow + (0,))
    g.putalpha(a)
    base.alpha_composite(g, xy)
    base.alpha_composite(im, xy)


def sunburst(w, h, c1, c2, cx, cy, n=18):
    im = Image.new("RGBA", (w, h), c1)
    d = ImageDraw.Draw(im)
    import math
    for k in range(n):
        a0, a1 = k * 2 * math.pi / n, (k + 0.5) * 2 * math.pi / n
        d.polygon([(cx, cy), (cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0)),
                   (cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))], fill=c2)
    return im


def option_a():
    """Both kids waving in the garden, fruits all around, big title."""
    bg = R.G["bg"].resize((1280, 720), Image.LANCZOS)
    im = bg.copy()
    for key, x, y, s, r in (("apple", 470, 300, 190, -10), ("banana", 640, 330, 190, 15), ("grapes", 560, 470, 180, 0),
                            ("strawberry", 720, 470, 160, 10), ("mango", 400, 470, 170, -15), ("watermelon", 560, 230, 200, 0)):
        glow_paste(im, fruit(key, s, r), (x - s // 2 + 80, y - s // 2 + 60), rad=6)
    g = char("gul", "open", "open", "wave", 0.95)
    m = char("misheal", "closed", "open", "wave", 0.95)
    glow_paste(im, g, (-60, 120))
    glow_paste(im, m, (1280 - m.width + 70, 120))
    R.rainbow_text(im, 640, 120, "LEARN FRUITS!", 118)
    return im


def option_b():
    """Sunburst, one giant mango + apple, kids peeking from the sides."""
    im = sunburst(1280, 720, (255, 214, 64, 255), (255, 190, 30, 255), 640, 380)
    glow_paste(im, fruit("watermelon", 330, -8), (470, 200), rad=8)
    glow_paste(im, fruit("apple", 250, -12), (360, 360), rad=8)
    glow_paste(im, fruit("banana", 250, 20), (680, 360), rad=8)
    g = char("gul", "open", "open", "down", 1.05)
    m = char("misheal", "open", "open", "down", 1.05)
    glow_paste(im, g, (-150, 120), rad=8)
    glow_paste(im, m, (1280 - m.width + 150, 120), rad=8)
    R.rainbow_text(im, 640, 110, "YUMMY FRUITS!", 120)
    return im


def option_c():
    """Cool Gul in sunglasses + Mishu, rainbow of fruits in a row, sky-blue background."""
    im = Image.new("RGBA", (1280, 720), (126, 200, 255, 255))
    d = ImageDraw.Draw(im)
    for k, col in enumerate([(255, 77, 109), (255, 159, 28), (255, 210, 63), (59, 193, 74), (46, 168, 255), (155, 93, 229)]):
        d.ellipse((640 - 900 + k * 40, 560 - 520 + k * 40, 640 + 900 - k * 40, 560 + 520 - k * 40), outline=col, width=40)
    d.rectangle((0, 600, 1280, 720), fill=(124, 203, 79))
    keys = ["apple", "orange", "banana", "pear", "grapes", "strawberry"]
    for i, key in enumerate(keys):
        glow_paste(im, fruit(key, 150), (330 + i * 105 - 75 + (40 if i % 2 else 0) * 0, 430 - (30 if i % 2 else 0)), rad=5)
    g = char("gul", "open", "smile", "wave", 0.95, glasses=True)
    m = char("misheal", "closed", "open", "down", 0.95)
    glow_paste(im, g, (-40, 160))
    glow_paste(im, m, (1280 - m.width + 40, 160))
    R.rainbow_text(im, 640, 140, "FRUITS", 150)
    R.plain_text(im, 640, 278, "with Gul & Mishu", 54, fill=(255, 255, 255))
    return im


if __name__ == "__main__":
    R.init()
    OUT.mkdir(parents=True, exist_ok=True)
    for tag, fn in (("A", option_a), ("B", option_b), ("C", option_c)):
        fn().convert("RGB").save(OUT / f"THUMBNAIL option {tag}.jpg", quality=92)
    sheet = Image.new("RGB", (1280 * 3 + 40, 720), "white")
    for i, tag in enumerate("ABC"):
        sheet.paste(Image.open(OUT / f"THUMBNAIL option {tag}.jpg"), (i * 1300, 0))
    sheet.resize((sheet.width // 2, 360)).save(HERE / "_thumbs.png")
    # feed-size check
    small = Image.new("RGB", (3 * 330, 186), "white")
    for i, tag in enumerate("ABC"):
        small.paste(Image.open(OUT / f"THUMBNAIL option {tag}.jpg").resize((320, 180)), (i * 330, 3))
    small.save(HERE / "_thumbs_small.png")
    print("ok")
