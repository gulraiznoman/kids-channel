"""Bright vertical thumbnail for the Short (1080x1920).  python thumb.py -> VIDEOS/S01 Animal Dance/THUMBNAIL vN.png"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import render as R

VER = os.environ.get("VER", "v1")


def sunburst(cols, n=24):
    W, H = R.W, R.H
    im = Image.new("RGB", (W, H), cols[0])
    d = ImageDraw.Draw(im)
    cx, cy, rr = W / 2, 1000, 2600
    for k in range(n):
        a0, a1 = k * 2 * math.pi / n, (k + 1) * 2 * math.pi / n
        d.polygon([(cx, cy), (cx + rr * math.cos(a0), cy + rr * math.sin(a0)), (cx + rr * math.cos(a1), cy + rr * math.sin(a1))],
                  fill=cols[k % len(cols)])
    glow = Image.new("L", (W, H), 0)
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.clip(1 - np.hypot(xx - cx, (yy - cy) * 0.9) / 700, 0, 1) ** 1.5
    white = Image.new("RGB", (W, H), (255, 250, 220))
    return Image.composite(white, im, Image.fromarray((g * 255).astype(np.uint8))).convert("RGBA")


def char(name, mouth="open", eyes="open"):
    c, L = R.CHAR[name], R.G["layers"][name]
    o = c["outfit"]
    im = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
    parts = (["hair_back"] if c["girl"] else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_wave_{o}", "neck", "head",
                                                     f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"]
    for p in parts + (["earrings"] if c["girl"] else []):
        im.alpha_composite(L[p])
    return im


def outlined(im, width=14, col=(255, 255, 255, 255)):
    """White sticker outline around a cut-out, so it pops off the busy background."""
    a = np.array(im.getchannel("A"))
    from PIL import ImageFilter
    m = Image.fromarray(a).filter(ImageFilter.MaxFilter(width * 2 + 1))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, col), (0, 0), m)
    out.alpha_composite(im)
    return out


if __name__ == "__main__":
    R.init()
    W, H = R.W, R.H
    frame = sunburst([(255, 204, 0), (255, 140, 40), (255, 90, 120), (170, 90, 230), (40, 170, 255), (60, 200, 90)])
    d = ImageDraw.Draw(frame)
    # confetti stars
    rng = np.random.default_rng(11)
    for _ in range(26):
        x, y = rng.uniform(40, W - 40), rng.uniform(420, 1500)
        if abs(x - W / 2) < 260 and 800 < y < 1200:
            continue
        R.burst  # keep import used
        r = rng.uniform(14, 30)
        pts = [(x + (r if q % 2 == 0 else r * 0.45) * math.cos(q * math.pi / 5 - math.pi / 2),
                y + (r if q % 2 == 0 else r * 0.45) * math.sin(q * math.pi / 5 - math.pi / 2)) for q in range(10)]
        d.polygon(pts, fill=(255, 255, 255), outline=R.INK, width=3)
    # four animals mid-move, each with a white sticker outline
    art = R.G["art"]
    for key, cx, cy, size, rot in (("monkey", 250, 820, 470, 14), ("duckling", 830, 800, 430, -12),
                                   ("bunny", 830, 1260, 440, 10), ("elephant", 260, 1270, 500, -8)):
        a = art[key].resize((size, size), Image.LANCZOS)
        a = outlined(a, 12).rotate(rot, resample=Image.BICUBIC, expand=True)
        frame.alpha_composite(a, (int(cx - a.width / 2), int(cy - a.height / 2)))
    # Gul & Mishu, big and excited, in front
    for name, cx, rot in (("gul", 330, 4), ("misheal", 760, -4)):
        im = char(name, "open")
        im = im.resize((int(im.width * 1.55), int(im.height * 1.55)), Image.LANCZOS)
        im = outlined(im, 14).rotate(rot, resample=Image.BICUBIC, expand=True)
        frame.alpha_composite(im, (int(cx - im.width / 2), H - im.height + 330))
    # title
    R.G["fonts"] = {}
    R.rainbow_text(frame, W / 2, 190, "ANIMAL", 215)
    R.rainbow_text(frame, W / 2, 420, "DANCE!", 245)
    out = ImageEnhance.Color(frame.convert("RGB")).enhance(1.12)
    dst = R.OUT / f"THUMBNAIL {VER}.png"
    out.save(dst)
    out.resize((270, 480)).save(R.HERE / "_thumb_small.png")
    print("wrote", dst)
