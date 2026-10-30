"""Thumbnail v2 for Good Habits (1280x720): Gul brushing with foam, Mishu washing hands with bubbles,
a big sparkly smiling tooth, bubbles and stars, rainbow title.  python thumb2.py
"""
import importlib.util, math, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location("gh_render", HERE / "render.py")
GH = importlib.util.module_from_spec(spec)
sys.argv = ["x"]
spec.loader.exec_module(GH)
R = GH.R
KIT = ROOT / "characters" / "layers"
W, H = 1280, 720
INK = R.INK
OUT = ROOT / "VIDEOS" / "L04 Good Habits" / "THUMBNAIL v2.jpg"


def outlined(im, width=10):
    m = im.getchannel("A").filter(ImageFilter.MaxFilter(width * 2 + 1))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), m)
    out.alpha_composite(im)
    return out


def character(name, outfit, wave=True):
    girl = name == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    parts = (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}", f"arm_r_{'wave' if wave else 'down'}_{outfit}",
                                               "neck", "head", "eyes_open", "brows", "mouth_open", "hair_front"] + (["earrings"] if girl else [])
    for p in parts:
        im.alpha_composite(Image.open(KIT / name / f"{p}.png"))
    mb = Image.open(KIT / name / "mouth_open.png").getbbox()
    return im, ((mb[0] + mb[2]) / 2, (mb[1] + mb[3]) / 2)


def art(path, size, rot=0):
    im = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    im = outlined(im, 8)
    return im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im


def bubble(d, x, y, r):
    d.ellipse((x - r, y - r, x + r, y + r), fill=(240, 250, 255), outline=(120, 190, 230), width=max(2, int(r / 8)))
    d.ellipse((x - r * 0.55, y - r * 0.6, x - r * 0.15, y - r * 0.25), fill=(255, 255, 255))


def big_tooth(frame, cx, cy, u):
    """Cute sparkly tooth: thick outline, rosy cheeks, big open smile, on a sunny glow."""
    d = ImageDraw.Draw(frame)
    d.ellipse((cx - 250 * u, cy - 230 * u, cx + 250 * u, cy + 230 * u), fill=(255, 236, 140))
    pts = [(cx - 130 * u, cy - 110 * u), (cx - 60 * u, cy - 150 * u), (cx, cy - 120 * u), (cx + 60 * u, cy - 150 * u),
           (cx + 130 * u, cy - 110 * u), (cx + 140 * u, cy), (cx + 100 * u, cy + 150 * u), (cx + 50 * u, cy + 160 * u),
           (cx + 20 * u, cy + 60 * u), (cx - 20 * u, cy + 60 * u), (cx - 50 * u, cy + 160 * u), (cx - 100 * u, cy + 150 * u), (cx - 140 * u, cy)]
    d.polygon(pts, fill=INK)
    inner = [(cx + (x - cx) * 0.93, cy + (y - cy) * 0.93) for x, y in pts]
    d.polygon(inner, fill=(255, 255, 255))
    d.ellipse((cx - 95 * u, cy - 95 * u, cx - 55 * u, cy - 70 * u), fill=(230, 245, 255))
    for ex in (-48, 48):
        d.ellipse((cx + ex * u - 20 * u, cy - 62 * u - 26 * u, cx + ex * u + 20 * u, cy - 62 * u + 26 * u), fill=INK)
        d.ellipse((cx + ex * u - 11 * u, cy - 76 * u, cx + ex * u - 1 * u, cy - 64 * u), fill=(255, 255, 255))
    for ex in (-88, 88):
        d.ellipse((cx + ex * u - 22 * u, cy - 22 * u, cx + ex * u + 22 * u, cy - 4 * u), fill=(255, 150, 170))
    d.chord((cx - 48 * u, cy - 40 * u, cx + 48 * u, cy + 38 * u), 0, 180, fill=(150, 40, 60), outline=INK, width=6)
    d.chord((cx - 26 * u, cy + 4 * u, cx + 26 * u, cy + 34 * u), 0, 180, fill=(255, 120, 140))


def main():
    R.G["fonts"] = {}
    # bright sunburst background: turquoise + yellow rays, white glow centre
    bg = Image.new("RGB", (W, H), (60, 200, 230))
    d = ImageDraw.Draw(bg)
    cx, cy = W / 2, 430
    for k in range(20):
        a0, a1 = k * 2 * math.pi / 20, (k + 1) * 2 * math.pi / 20
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a0), cy + 1600 * math.sin(a0)), (cx + 1600 * math.cos(a1), cy + 1600 * math.sin(a1))],
                  fill=(255, 214, 70) if k % 2 else (70, 205, 235))
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.clip(1 - np.hypot(xx - cx, (yy - cy) * 1.1) / 420, 0, 1) ** 1.4
    fr = Image.composite(Image.new("RGB", (W, H), (255, 252, 235)), bg, Image.fromarray((g * 255).astype(np.uint8))).convert("RGBA")
    d = ImageDraw.Draw(fr)
    # the big smiling sparkly tooth in the middle
    big_tooth(fr, 640, 450, 1.25)
    for j in range(10):
        ang = j / 10 * 2 * math.pi + 0.3
        R.star(d, 640 + 230 * math.cos(ang), 445 + 205 * math.sin(ang), 20 if j % 2 else 30, (255, 230, 60))
    # little routine icons on the tooth's sides
    for name, x, y, s, rot in (("clock", 470, 610, 120, -12), ("soap", 815, 615, 120, 10)):
        ic = art(HERE / "art" / f"item_{name}.png", s, rot)
        fr.alpha_composite(ic, (int(x - ic.width / 2), int(y - ic.height / 2)))
    # Gul brushing his teeth (left), Mishu washing hands (right)
    for name, outfit, x, rot in (("gul", "bluetee", 205, 4), ("misheal", "pink", 1080, -4)):
        im, (mx, my) = character(name, outfit)
        k = 0.47
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        mx, my = mx * k, my * k
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        if name == "gul":
            tb = Image.open(HERE / "art" / "item_toothbrush.png").convert("RGBA").resize((210, 210), Image.LANCZOS).rotate(-15, expand=True)
            lay.alpha_composite(tb, (int(mx - 20), int(my - tb.height / 2 + 10)))
            for bx, by, r in ((mx - 30, my + 15, 16), (mx + 5, my + 30, 12), (mx - 55, my - 5, 11), (mx + 25, my - 10, 9)):
                bubble(ld, bx, by, r)
        else:
            hd = Image.open(HERE / "art" / "item_hands.png").convert("RGBA").resize((150, 150), Image.LANCZOS)
            lay.alpha_composite(hd, (int(im.width / 2 - 120), int(im.height * 0.55)))
            lay.alpha_composite(hd.transpose(Image.FLIP_LEFT_RIGHT), (int(im.width / 2 - 30), int(im.height * 0.55)))
            for bx, by, r in ((im.width / 2 - 50, im.height * 0.57, 26), (im.width / 2 + 55, im.height * 0.56, 20),
                              (im.width / 2 - 115, im.height * 0.62, 18), (im.width / 2 + 5, im.height * 0.53, 14)):
                bubble(ld, bx, by, r)
        im.alpha_composite(lay)
        im = im.crop(im.getbbox())
        im = outlined(im, 10).rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(im, (int(x - im.width / 2), H - im.height + 175))
    # floating soap bubbles everywhere
    rng = np.random.default_rng(5)
    for _ in range(22):
        x, y, r = rng.uniform(30, W - 30), rng.uniform(150, 690), rng.uniform(10, 26)
        if abs(x - 640) < 300 and y > 200:              # keep clear of the tooth
            continue
        if (x < 420 or x > 860) and 150 < y < 470:      # keep clear of Gul's and Mishu's faces
            continue
        bubble(d, x, y, r)
    # title: big rainbow letters
    R.rainbow_text(fr, 640, 98, "GOOD HABITS!", 128, maxw=1220)
    out = ImageEnhance.Color(fr.convert("RGB")).enhance(1.15)
    out = ImageEnhance.Contrast(out).enhance(1.05)
    out.save(OUT, quality=95)
    out.resize((640, 360)).save(HERE / "_t2.png")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
