"""Simple long-video thumbnail (1280x720): plain colour background, Gul & Mishu, ONE big object, 2-3 words.

python tools/thumb_simple.py OUT.png ITEM_PNG "WORD ONE" "#RRGGBB" [gul_outfit] [mishu_outfit]
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
KIT = ROOT / "characters" / "layers"
FONT = "C:/Windows/Fonts/seguibl.ttf"
INK = (58, 36, 32)
W, H = 1280, 720


def outlined(im, width=10):
    m = im.getchannel("A").filter(ImageFilter.MaxFilter(width * 2 + 1))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), m)
    out.alpha_composite(im)
    return out


def character(name, outfit):
    girl = name == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    parts = (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}", f"arm_r_wave_{outfit}", "neck", "head",
                                               "eyes_open", "brows", "mouth_open", "hair_front"] + (["earrings"] if girl else [])
    for p in parts:
        im.alpha_composite(Image.open(KIT / name / f"{p}.png"))
    return im.crop(im.getbbox())


def main(out, item, words, colour, gul_outfit="tee", mishu_outfit="yellow"):
    bg = tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5))
    fr = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(fr)
    d.ellipse((330, 60, 950, 680), fill=tuple(min(255, c + 45) for c in bg))          # soft glow behind the object
    obj = Image.open(item).convert("RGBA")
    obj = obj.crop(obj.getbbox())
    k = 470 / max(obj.size)
    obj = outlined(obj.resize((int(obj.width * k), int(obj.height * k)), Image.LANCZOS), 12)
    fr.alpha_composite(obj, (W // 2 - obj.width // 2, 400 - obj.height // 2))
    for name, outfit, x in (("gul", gul_outfit, 165), ("misheal", mishu_outfit, 1115)):
        c = character(name, outfit)
        k = 600 / c.height
        c = outlined(c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS), 9)
        fr.alpha_composite(c, (x - c.width // 2, H - c.height + 40))
    size = 120
    f = ImageFont.truetype(FONT, size)
    while d.textlength(words, font=f) > 1180:
        size -= 6
        f = ImageFont.truetype(FONT, size)
    w = d.textlength(words, font=f)
    d.text((W / 2 - w / 2, 18), words, font=f, fill=(255, 255, 255), stroke_width=int(size * 0.12), stroke_fill=INK)
    fr.convert("RGB").save(out, quality=95)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:])
