"""Bright thumbnail (1080x1920): Halloween sunburst, items, Gul & Mishu in costume.  python thumb.py"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import render as R

VER = os.environ.get("VER", "v1")


def outlined(im, width=12):
    m = im.getchannel("A").filter(ImageFilter.MaxFilter(width * 2 + 1))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), m)
    out.alpha_composite(im)
    return out


def sunburst():
    W, H = R.W, R.H
    cols = [(255, 140, 30), (150, 90, 230), (255, 190, 60), (120, 70, 200)]
    im = Image.new("RGB", (W, H), cols[0])
    d = ImageDraw.Draw(im)
    cx, cy, rr = W / 2, 1000, 2600
    for k in range(24):
        a0, a1 = k * 2 * math.pi / 24, (k + 1) * 2 * math.pi / 24
        d.polygon([(cx, cy), (cx + rr * math.cos(a0), cy + rr * math.sin(a0)), (cx + rr * math.cos(a1), cy + rr * math.sin(a1))],
                  fill=cols[k % 4])
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.clip(1 - np.hypot(xx - cx, (yy - cy) * 0.9) / 650, 0, 1) ** 1.5
    return Image.composite(Image.new("RGB", (W, H), (255, 245, 210)), im, Image.fromarray((g * 255).astype(np.uint8))).convert("RGBA")


if __name__ == "__main__":
    R.init()
    W, H = R.W, R.H
    fr = sunburst()
    A = R.G["art"]
    for key, cx, cy, size, rot in (("bat", 250, 720, 380, -10), ("ghost", 840, 760, 380, 8),
                                   ("blackcat", 220, 1180, 400, 6), ("candy", 860, 1190, 400, -6),
                                   ("jackolantern", 540, 960, 520, 0)):
        a = outlined(A[key].resize((size, size), Image.LANCZOS)).rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(a, (int(cx - a.width / 2), int(cy - a.height / 2)))
    for n, cx, rot in (("gul", 320, 4), ("misheal", 770, -4)):
        L = R.G["layers"][n]
        o = R.CHAR[n]["outfit"]
        im = Image.new("RGBA", L["head"].size, (0, 0, 0, 0))
        parts = (["hair_back"] if n == "misheal" else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_wave_{o}", "neck", "head",
                 "eyes_open", "brows", "mouth_open", "hair_front"] + (["earrings"] if n == "misheal" else [])
        for p in parts:
            im.alpha_composite(L[p])
        im.alpha_composite(R.G["hat"][n])
        im = im.resize((int(im.width * 1.5), int(im.height * 1.5)), Image.LANCZOS)
        im = outlined(im, 14).rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(im, (int(cx - im.width / 2), H - im.height + 300))
    R.rainbow_text(fr, W / 2, 190, "HALLOWEEN", 200)
    R.rainbow_text(fr, W / 2, 410, "GET READY!", 190)
    out = ImageEnhance.Color(fr.convert("RGB")).enhance(1.1)
    dst = R.OUT / f"THUMBNAIL {VER}.png"
    R.OUT.mkdir(parents=True, exist_ok=True)
    out.save(dst)
    out.resize((405, 720)).save(R.HERE / "_t.png")
    print("wrote", dst)
