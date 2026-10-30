"""Extra face-expression layers for Gul & Mishu (1200x2000 canvas, same alignment as the kit).
Adds: brows_sad / brows_angry / brows_up, mouth_frown / mouth_angry / mouth_wavy / mouth_bigo / mouth_bigsmile /
mouth_yawn / mouth_small, and overlays tears / angry / sweat / blush / lids / sparkle.  Existing layers are untouched.

python expressions.py  -> layers/<name>/x_*.png  +  _expressions.png preview
EMOTIONS below says which layers make each feeling.
"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A

INK = "#3A2420"
CH = {"gul": dict(brow="#1C151C", skin="#DCA27A"), "misheal": dict(brow="#6A3523", skin="#EDC2A0")}
EL, ER, EY, ERX, ERY = 464, 736, 636, 77, 89          # eye centres / radii


def brows(kind, col):
    paths = {"sad": ("M385 518 Q458 508 532 478", "M815 518 Q742 508 668 478"),
             "angry": ("M385 486 Q460 494 534 532", "M815 486 Q740 494 666 532"),
             "up": ("M385 478 Q458 430 532 466", "M815 478 Q742 430 668 466")}[kind]
    return "".join(f'<path d="{p}" stroke="{col}" stroke-width="24" fill="none" stroke-linecap="round"/>' for p in paths)


MOUTH = {
    "frown": f'<path d="M532 856 Q600 792 668 856" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/>',
    "angry": f'<rect x="538" y="806" width="124" height="46" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M540 829 L660 829 M570 808 L570 850 M600 808 L600 850 M630 808 L630 850" stroke="{INK}" stroke-width="5"/>',
    "wavy": f'<path d="M526 832 q18 -20 37 0 t37 0 t37 0 t37 0" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>',
    "bigo": f'<ellipse cx="600" cy="840" rx="40" ry="52" fill="#7A2E3A" stroke="{INK}" stroke-width="10"/>'
            f'<ellipse cx="600" cy="866" rx="22" ry="12" fill="#FF8FA3"/>',
    "bigsmile": f'<path d="M515 798 Q600 912 685 798 Z" fill="#7A2E3A" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
                f'<path d="M530 802 L670 802 L662 818 L538 818 Z" fill="#FFFFFF"/><ellipse cx="600" cy="866" rx="40" ry="18" fill="#FF8FA3"/>',
    "yawn": f'<ellipse cx="600" cy="852" rx="46" ry="66" fill="#7A2E3A" stroke="{INK}" stroke-width="10"/>'
            f'<ellipse cx="600" cy="895" rx="26" ry="14" fill="#FF8FA3"/>',
    "small": f'<path d="M566 832 Q600 852 634 832" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>',
}


def overlays(skin):
    drop = lambda x, y, s=1.0: (f'<path d="M{x} {y - 34 * s} Q{x + 26 * s} {y} {x} {y + 22 * s} Q{x - 26 * s} {y} {x} {y - 34 * s} Z" '
                                f'fill="#6EC6FF" stroke="{INK}" stroke-width="5"/><ellipse cx="{x - 7 * s}" cy="{y}" rx="{5 * s}" ry="{8 * s}" fill="#FFFFFF"/>')
    lid = lambda cx: (f'<path d="M{cx - ERX - 4} {EY + 6} A{ERX + 4} {ERY + 4} 0 0 1 {cx + ERX + 4} {EY + 6} Z" fill="{skin}"/>'
                      f'<path d="M{cx - ERX} {EY + 6} L{cx + ERX} {EY + 6}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    spark = lambda cx: (f'<path d="M{cx} {EY - 52} L{cx + 10} {EY - 24} L{cx + 38} {EY - 14} L{cx + 10} {EY - 4} L{cx} {EY + 24} '
                        f'L{cx - 10} {EY - 4} L{cx - 38} {EY - 14} L{cx - 10} {EY - 24} Z" fill="#FFF6A0" stroke="{INK}" stroke-width="3"/>')
    return {
        "tears": f'<path d="M430 725 Q422 800 430 880 M770 725 Q778 800 770 880" stroke="#6EC6FF" stroke-width="18" fill="none" stroke-linecap="round" opacity="0.85"/>'
                 + drop(430, 900) + drop(770, 900),
        "angry": '<ellipse cx="385" cy="770" rx="62" ry="36" fill="#FF4040" opacity="0.45"/><ellipse cx="815" cy="770" rx="62" ry="36" fill="#FF4040" opacity="0.45"/>',
        "sweat": drop(850, 520, 1.4) + drop(880, 600, 0.9),
        "blush": '<ellipse cx="390" cy="768" rx="70" ry="40" fill="#FF6F91" opacity="0.6"/><ellipse cx="810" cy="768" rx="70" ry="40" fill="#FF6F91" opacity="0.6"/>'
                 + "".join(f'<path d="M{x} 752 l-16 30" stroke="#E0466E" stroke-width="7" stroke-linecap="round"/>' for x in (372, 396, 420, 792, 816, 840)),
        "lids": lid(EL) + lid(ER),
        "sparkle": spark(EL - 18) + spark(ER - 18),
    }


# feeling -> (eyes layer, brows, mouth, overlays)
EMOTIONS = {
    "happy": ("eyes_closed", None, "bigsmile", []),
    "sad": ("eyes_open", "sad", "frown", ["tears"]),
    "angry": ("eyes_open", "angry", "angry", ["angry"]),
    "scared": ("eyes_open", "up", "wavy", ["sweat"]),
    "surprised": ("eyes_open", "up", "bigo", []),
    "excited": ("eyes_open", "up", "bigsmile", ["sparkle"]),
    "tired": ("eyes_open", "sad", "yawn", ["lids"]),
    "shy": ("eyes_open", "sad", "small", ["blush", "lids"]),
    "proud": ("eyes_closed", "up", "bigsmile", ["blush"]),
    "calm": ("eyes_closed", None, "small", []),
}


def svg_layer(name, svg):
    out = HERE / "layers" / name
    A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1200" height="2000">{svg}</svg></body></html>',
           str(out / "_tmp.png"), 1200, 2000)
    return out / "_tmp.png"


def build():
    for name, c in CH.items():
        L = HERE / "layers" / name
        for k in ("sad", "angry", "up"):
            svg_layer(name, brows(k, c["brow"])).replace(L / f"x_brows_{k}.png")
        for k, svg in MOUTH.items():
            svg_layer(name, svg).replace(L / f"x_mouth_{k}.png")
        for k, svg in overlays(c["skin"]).items():
            svg_layer(name, svg).replace(L / f"x_over_{k}.png")
    preview()


def face(name, emo, outfit):
    L = HERE / "layers" / name
    eyes, brw, mouth, ovs = EMOTIONS[emo]
    girl = name == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    parts = (["hair_back"] if girl else []) + [f"body_{outfit}", f"arm_l_{outfit}", f"arm_r_down_{outfit}", "neck", "head", eyes]
    for p in parts:
        im.alpha_composite(Image.open(L / f"{p}.png"))
    for ov in ovs:
        if ov == "lids":
            im.alpha_composite(Image.open(L / f"x_over_{ov}.png"))
    im.alpha_composite(Image.open(L / (f"x_brows_{brw}.png" if brw else "brows.png")))
    im.alpha_composite(Image.open(L / f"x_mouth_{mouth}.png"))
    im.alpha_composite(Image.open(L / "hair_front.png"))
    if girl:
        im.alpha_composite(Image.open(L / "earrings.png"))
    for ov in ovs:                                   # tears, sweat, blush... go on top of the hair
        if ov != "lids":
            im.alpha_composite(Image.open(L / f"x_over_{ov}.png"))
    return im


def preview():
    emos = list(EMOTIONS)
    sheet = Image.new("RGBA", (len(emos) * 220, 470), (235, 235, 240, 255))
    for i, e in enumerate(emos):
        for j, (n, o) in enumerate((("gul", "tee"), ("misheal", "yellow"))):
            f = face(n, e, o).crop((150, 150, 1050, 1050)).resize((210, 210))
            sheet.alpha_composite(f, (i * 220 + 5, 20 + j * 225))
    sheet.save(HERE / "_expressions.png")
    print("expressions:", emos)


if __name__ == "__main__":
    build()
