"""v3 art: a DETAILED barefoot body for Gul (5-finger hands, thumbs, elbows, wrists, knees, ankles, toes) on the
1200x2000 character canvas, plus labelled close-up cards (hand, foot, arm, leg).

python art3.py -> art/gul_body_detail.png, art/item_card_<hand|foot|arm|leg>.png, _sheet3.png
"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as A

INK = A.INK
SKIN, SKIN_D = "#DCA27A", "#B9774D"
OUT = HERE / "art"


def limb(d, w):
    """Thick outlined limb: ink stroke then skin stroke along the same path."""
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{w + 14}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{SKIN}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def hand(cx, cy, mirror=1):
    """Front view hand hanging down: palm + 4 fingers pointing down + thumb pointing toward the body."""
    s = mirror
    fingers = "".join(
        f'<rect x="{cx + dx * s - 16}" y="{cy + 20}" width="32" height="{ln}" rx="16" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>'
        f'<ellipse cx="{cx + dx * s}" cy="{cy + 20 + ln - 14}" rx="10" ry="8" fill="#F2C9A8"/>'
        for dx, ln in ((-42, 88), (-14, 104), (14, 102), (42, 84)))
    thumb = (f'<rect x="{cx + 52 * s - 16}" y="{cy - 28}" width="32" height="78" rx="16" fill="{SKIN}" stroke="{INK}" stroke-width="7" '
             f'transform="rotate({-38 * s} {cx + 52 * s} {cy - 28})"/>')
    palm = f'<rect x="{cx - 62}" y="{cy - 55}" width="124" height="100" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>'
    cover = f'<rect x="{cx - 54}" y="{cy + 8}" width="108" height="30" fill="{SKIN}"/>'
    return fingers + thumb + palm + cover


def foot(cx, cy, mirror=1):
    s = mirror
    toes = "".join(f'<circle cx="{cx + dx * s}" cy="{cy + 34 - abs(dx) * 0.12}" r="{r}" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'
                   for dx, r in ((-58, 21), (-29, 19), (0, 18), (27, 16), (51, 15)))
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="98" ry="52" fill="{SKIN}" stroke="{INK}" stroke-width="8"/>{toes}'
            f'<ellipse cx="{cx}" cy="{cy + 6}" rx="80" ry="24" fill="{SKIN}"/>')


BODY = f'''
{limb("M415 1030 Q365 1150 345 1200 Q330 1290 335 1370", 92)}
{limb("M785 1030 Q835 1150 855 1200 Q870 1290 865 1370", 92)}
<path d="M318 1200 q27 -14 54 0 M828 1200 q27 -14 54 0" stroke="{SKIN_D}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M298 1372 l74 0 M828 1372 l74 0" stroke="{SKIN_D}" stroke-width="7" stroke-linecap="round"/>
{hand(333, 1430, 1)}{hand(867, 1430, -1)}
{limb("M520 1500 L512 1660 L510 1790", 104)}
{limb("M680 1500 L688 1660 L690 1790", 104)}
<path d="M478 1650 q34 22 68 0 M654 1650 q34 22 68 0" stroke="{SKIN_D}" stroke-width="8" fill="none" stroke-linecap="round"/>
<circle cx="466" cy="1792" r="9" fill="{SKIN_D}"/><circle cx="734" cy="1792" r="9" fill="{SKIN_D}"/>
{foot(480, 1840, 1)}{foot(720, 1840, -1)}
<path d="M392 1395 L405 1520 Q600 1545 795 1520 L808 1395 Z" fill="#3B6FD9" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>
<path d="M600 1430 L600 1528" stroke="{INK}" stroke-width="9"/>
<path d="M430 1000 Q600 960 770 1000 L870 1140 L800 1180 L800 1410 L400 1410 L400 1180 L330 1140 Z" fill="#E84C3D" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>
<path d="M600 1150 l26 52 l57 8 l-41 40 l10 57 l-52 -27 l-52 27 l10 -57 l-41 -40 l57 -8 Z" fill="#FFD23F" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
<path d="M540 985 Q600 1020 660 985" stroke="{INK}" stroke-width="9" fill="none"/>'''


def label(x, y, tx, ty, text, anchor="start"):
    return (f'<path d="M{x} {y} L{tx} {ty}" stroke="{INK}" stroke-width="4"/><circle cx="{x}" cy="{y}" r="7" fill="#FF4D6D" stroke="#FFFFFF" stroke-width="3"/>'
            f'<text x="{tx + (8 if anchor == "start" else -8)}" y="{ty + 10}" font-size="27" font-family="Arial Black" fill="#2E2A3A" '
            f'text-anchor="{anchor}" stroke="#FFFFFF" stroke-width="6" paint-order="stroke">{text}</text>')


CARD_BG = '<rect x="6" y="6" width="388" height="388" rx="40" fill="#FFFFFF" stroke="#3A2420" stroke-width="10"/>'
CARDS = {
    # big open hand, fingers up
    "hand": CARD_BG + f'''
      <rect x="150" y="290" width="100" height="90" rx="20" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>
      <path d="M150 300 L250 300" stroke="{SKIN_D}" stroke-width="6"/>
      {"".join(f'<rect x="{x}" y="{y}" width="40" height="{h}" rx="20" fill="{SKIN}" stroke="{INK}" stroke-width="7"/><ellipse cx="{x + 20}" cy="{y + 18}" rx="13" ry="11" fill="#F7D9C2" stroke="{SKIN_D}" stroke-width="3"/>'
                for x, y, h in ((118, 95, 150), (165, 70, 170), (212, 78, 162), (259, 105, 140)))}
      <rect x="290" y="175" width="40" height="110" rx="20" fill="{SKIN}" stroke="{INK}" stroke-width="7" transform="rotate(38 300 270)"/>
      <rect x="112" y="180" width="190" height="130" rx="50" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>
      <rect x="120" y="175" width="175" height="40" fill="{SKIN}"/>
      {label(205, 250, 15, 345, "PALM")}{label(140, 110, 15, 40, "FINGERS")}{label(325, 230, 390, 70, "THUMB", "end")}
      {label(232, 96, 390, 140, "NAILS", "end")}{label(200, 335, 390, 385, "WRIST", "end")}''',
    # side view foot
    "foot": CARD_BG + f'''
      {limb("M150 40 L150 240", 90)}
      <path d="M105 230 Q100 300 140 320 L300 330 Q345 330 345 300 Q345 270 300 262 L200 250 Q195 225 195 200 L105 200 Z" fill="{SKIN}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      {"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>' for x, y, r in ((338, 300, 17), (318, 312, 14), (300, 319, 12)))}
      <circle cx="170" cy="232" r="11" fill="{SKIN_D}"/>
      {label(330, 300, 390, 245, "TOES", "end")}{label(110, 290, 15, 370, "HEEL")}{label(172, 232, 390, 150, "ANKLE", "end")}{label(230, 325, 390, 385, "SOLE", "end")}''',
    # bent arm
    "arm": CARD_BG + f'''
      <path d="M60 80 Q100 60 140 85 L150 150 L80 150 Z" fill="#E84C3D" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      {limb("M110 150 L130 270 L290 230", 70)}
      {"".join(f'<rect x="300" y="{y}" width="70" height="20" rx="10" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>' for y in (190, 210, 230, 250))}
      <rect x="290" y="168" width="20" height="50" rx="10" fill="{SKIN}" stroke="{INK}" stroke-width="5" transform="rotate(-30 300 190)"/>
      <rect x="270" y="190" width="55" height="80" rx="22" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>
      <path d="M118 270 q14 18 28 4" stroke="{SKIN_D}" stroke-width="6" fill="none"/><path d="M270 214 l8 32" stroke="{SKIN_D}" stroke-width="6"/>
      {label(105, 95, 390, 60, "SHOULDER", "end")}{label(130, 275, 15, 370, "ELBOW")}{label(262, 240, 390, 330, "WRIST", "end")}{label(330, 220, 390, 140, "HAND", "end")}''',
    # leg side view
    "leg": CARD_BG + f'''
      <path d="M120 40 L280 40 L285 130 L115 130 Z" fill="#3B6FD9" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      {limb("M200 130 L200 300", 88)}
      <path d="M160 300 Q160 350 200 352 L320 356 Q350 356 350 335 Q350 315 320 312 L245 300 Z" fill="{SKIN}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M175 210 q25 14 50 0" stroke="{SKIN_D}" stroke-width="7" fill="none"/><circle cx="222" cy="300" r="9" fill="{SKIN_D}"/>
      {label(120, 95, 15, 170, "HIP")}{label(200, 213, 390, 170, "KNEE", "end")}{label(222, 300, 390, 262, "ANKLE", "end")}{label(300, 340, 390, 385, "FOOT", "end")}''',
}
# where each label sits on the card (0..400 space) so the renderer can ring it
CARD_SPOTS = {"palm": ("hand", 205, 260), "fingers": ("hand", 185, 120), "thumbs": ("hand", 325, 230), "wrists": ("hand", 200, 335),
              "hands": ("hand", 205, 230), "feet": ("foot", 230, 300), "toes": ("foot", 320, 305), "ankles": ("foot", 172, 232),
              "arms": ("arm", 200, 250), "elbows": ("arm", 130, 275), "shoulders": ("arm", 105, 100), "legs": ("leg", 200, 220),
              "knees": ("leg", 200, 213), "hips": ("leg", 120, 95)}


def render():
    A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1200" height="2000">{BODY}</svg></body></html>',
           str(OUT / "gul_body_detail.png"), 1200, 2000)
    names = list(CARDS)
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{CARDS[n]}</svg></div>'
                    for i, n in enumerate(names))
    A.shot(f'<html><body style="margin:0;position:relative;width:{400 * len(names)}px;height:400px">{cells}</body></html>',
           str(OUT / "_cards.png"), 400 * len(names), 400, scale=2)
    im = Image.open(OUT / "_cards.png")
    for i, n in enumerate(names):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_card_{n}.png")
    (OUT / "_cards.png").unlink()
    # preview: full detailed Gul + cards
    K = ROOT / "characters" / "layers" / "gul"
    g = Image.open(OUT / "gul_body_detail.png").convert("RGBA")
    for p in ("neck", "head", "eyes_open", "brows", "mouth_smile", "hair_front"):
        g.alpha_composite(Image.open(K / f"{p}.png"))
    sheet = Image.new("RGBA", (360 + 4 * 300, 600), (225, 230, 240, 255))
    sheet.alpha_composite(g.resize((360, 600)), (0, 0))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_card_{n}.png").resize((290, 290)), (370 + i * 300, 150))
    sheet.save(HERE / "_sheet3.png")
    print("rendered detailed body + cards")


if __name__ == "__main__":
    render()
