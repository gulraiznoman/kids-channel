"""YouTube profile picture options (800x800, shown as a circle)."""
import math, pathlib
from PIL import Image, ImageDraw, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent / "characters" / "layers"
INK = (58, 36, 32)


def head(name, eyes="open", mouth="smile"):
    """Head + shoulders from the full-resolution layers, cropped tight."""
    girl = name == "misheal"
    order = (["hair_back"] if girl else []) + [f"body_{'yellow' if girl else 'tee'}", "neck", "head",
                                                f"eyes_{eyes}", "brows", f"mouth_{mouth}", "hair_front"] + (["earrings"] if girl else [])
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    for n in order:
        im.alpha_composite(Image.open(KIT / name / f"{n}.png"))
    return im.crop((120, 120, 1080, 1180))          # 960 x 1060


def outline_glow(im, rad=14, col=(255, 255, 255)):
    a = im.split()[3].filter(ImageFilter.MaxFilter(rad * 2 + 1))
    g = Image.new("RGBA", im.size, col + (0,))
    g.putalpha(a)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(im)
    return out


def sunburst(size, c1, c2, n=16):
    im = Image.new("RGBA", (size, size), c1)
    d = ImageDraw.Draw(im)
    c = size / 2
    for k in range(n):
        a0, a1 = k * 2 * math.pi / n, (k + 0.5) * 2 * math.pi / n
        d.polygon([(c, c), (c + size * math.cos(a0), c + size * math.sin(a0)),
                   (c + size * math.cos(a1), c + size * math.sin(a1))], fill=c2)
    return im


def rainbow_rings(size):
    im = Image.new("RGBA", (size, size), (126, 200, 255, 255))
    d = ImageDraw.Draw(im)
    cols = [(255, 77, 109), (255, 159, 28), (255, 210, 63), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
    for k, col in enumerate(cols):
        r = size * 0.98 - k * 38
        d.ellipse((size / 2 - r, size * 0.95 - r, size / 2 + r, size * 0.95 + r), outline=col, width=38)
    return im


def compose(bg, g_eyes="open", m_eyes="open", g_mouth="smile", m_mouth="smile", tilt=7, scale=0.53):
    S = 1600                                  # work at 2x, downsample to 800
    im = bg.resize((S, S), Image.LANCZOS)
    g = outline_glow(head("gul", g_eyes, g_mouth))
    m = outline_glow(head("misheal", m_eyes, m_mouth))
    g = g.resize((int(g.width * scale * 1.67), int(g.height * scale * 1.67)), Image.LANCZOS).rotate(-tilt, resample=Image.BICUBIC, expand=True)
    m = m.resize((int(m.width * scale * 1.67), int(m.height * scale * 1.67)), Image.LANCZOS).rotate(tilt, resample=Image.BICUBIC, expand=True)
    y = int(S * 0.27)
    im.alpha_composite(m, (int(S * 0.5 - m.width * 0.10), y + 30))
    im.alpha_composite(g, (int(S * 0.5 - g.width * 0.90), y))
    return im.resize((800, 800), Image.LANCZOS)


def circle_preview(im, d=160):
    sm = im.resize((d, d), Image.LANCZOS)
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d - 1, d - 1), fill=255)
    out = Image.new("RGBA", (d, d), (255, 255, 255, 255))
    out.paste(sm, (0, 0), mask)
    return out


if __name__ == "__main__":
    opts = {
        "A": compose(sunburst(800, (255, 214, 64, 255), (255, 190, 30, 255)), "open", "closed", "open", "open"),
        "B": compose(rainbow_rings(800), "open", "open", "smile", "smile"),
        "C": compose(sunburst(800, (126, 200, 255, 255), (100, 182, 250, 255)), "closed", "open", "open", "smile"),
    }
    for k, im in opts.items():
        im.convert("RGB").save(HERE / f"PROFILE PICTURE option {k}.png")
    # preview: full size + how it looks as a small circle on YouTube
    sheet = Image.new("RGB", (3 * 420, 600), "white")
    for i, (k, im) in enumerate(opts.items()):
        sheet.paste(im.resize((400, 400)).convert("RGB"), (i * 420, 0))
        c = circle_preview(im, 160)
        sheet.paste(c.convert("RGB"), (i * 420 + 120, 420))
        s48 = circle_preview(im, 48)
        sheet.paste(s48.convert("RGB"), (i * 420 + 300, 500))
    sheet.save(HERE / "_profile_check.png")
    print("ok")
