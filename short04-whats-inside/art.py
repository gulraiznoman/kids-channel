"""Art for Short "What's Inside?": whole fruits + their insides (not used in any other video).
python art.py -> art/item_<key>.png (800x800) + _sheet.png
"""
import math, pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
SHINE = lambda x, y, rx, ry: f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#FFFFFF" opacity="0.45" transform="rotate(-30 {x} {y})"/>'

I = {}
# apple cut across: pale flesh with a 5-point seed star in the middle
star = " ".join(f"{200 + 85 * math.cos(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45):.0f},"
                f"{215 + 85 * math.sin(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45):.0f}" for k in range(10))
seeds = "".join(f'<ellipse cx="{200 + 50 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5):.0f}" cy="{215 + 50 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5):.0f}" '
                f'rx="9" ry="14" fill="#4A2C12" transform="rotate({k * 72} {200 + 50 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5):.0f} '
                f'{215 + 50 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5):.0f})"/>' for k in range(5))
I["apple_half"] = f'''<circle cx="200" cy="215" r="150" fill="#E8352E" {SW}/><circle cx="200" cy="215" r="132" fill="#FFF6D8"/>
<polygon points="{star}" fill="#F2E3A6" stroke="#C9B26A" stroke-width="5"/>{seeds}'''
# orange cut across: segments
segs = "".join(f'<path d="M200 215 L{200 + 112 * math.cos(a):.0f} {215 + 112 * math.sin(a):.0f} A112 112 0 0 1 {200 + 112 * math.cos(a + 0.628):.0f} '
               f'{215 + 112 * math.sin(a + 0.628):.0f} Z" fill="#FFA62B" stroke="#FFF3D6" stroke-width="7"/>'
               for a in [k * 0.628 for k in range(10)])
I["orange_half"] = f'''<circle cx="200" cy="215" r="150" fill="#FF9420" {SW}/><circle cx="200" cy="215" r="128" fill="#FFF3D6"/>{segs}
<circle cx="200" cy="215" r="14" fill="#FFF3D6"/>'''
# watermelon: whole (striped) and half
stripes = "".join(f'<path d="M{x} 95 Q{x + (200 - x) * 0.35:.0f} 215 {x} 335" stroke="#2E7D32" stroke-width="16" fill="none"/>' for x in (120, 165, 200, 235, 280))
I["watermelon_whole"] = f'''<defs><clipPath id="wm"><ellipse cx="200" cy="215" rx="167" ry="127"/></clipPath></defs>
<ellipse cx="200" cy="215" rx="170" ry="130" fill="#66BB6A" {SW}/><g clip-path="url(#wm)">{stripes}</g>
<ellipse cx="200" cy="215" rx="170" ry="130" fill="none" {SW}/>{SHINE(130, 150, 40, 18)}'''
wseeds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="12" fill="#2B1B17"/>' for x, y in
                 ((130, 180), (170, 230), (210, 170), (250, 225), (290, 185), (150, 270), (230, 280), (200, 220), (270, 265), (110, 235)))
I["watermelon_half"] = f'''<ellipse cx="200" cy="215" rx="175" ry="135" fill="#2E7D32" {SW}/><ellipse cx="200" cy="215" rx="160" ry="120" fill="#C8F0A0"/>
<ellipse cx="200" cy="215" rx="148" ry="108" fill="#FF4D5E"/>{wseeds}'''
# tomato cut across: red with four seed rooms
rooms = "".join(f'<ellipse cx="{200 + 58 * math.cos(a):.0f}" cy="{215 + 58 * math.sin(a):.0f}" rx="36" ry="28" fill="#FF9A8A" '
                f'transform="rotate({math.degrees(a):.0f} {200 + 58 * math.cos(a):.0f} {215 + 58 * math.sin(a):.0f})"/>' +
                "".join(f'<circle cx="{200 + (52 + d) * math.cos(a + e):.0f}" cy="{215 + (52 + d) * math.sin(a + e):.0f}" r="5" fill="#FFF3C4"/>'
                        for d, e in ((-10, -0.2), (8, 0.15), (16, -0.1), (0, 0.3)))
                for a in (math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4))
I["tomato_half"] = f'''<circle cx="200" cy="215" r="150" fill="#E8352E" {SW}/><circle cx="200" cy="215" r="134" fill="#F2483F"/>{rooms}
<circle cx="200" cy="215" r="22" fill="#F78A7C"/>'''


def render():
    names = list(I)
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{I[n]}</svg></div>'
                    for i, n in enumerate(names))
    w = 400 * len(names)
    A.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>', str(OUT / "_items.png"), w, 400, scale=2)
    im = Image.open(OUT / "_items.png")
    for i, n in enumerate(names):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_{n}.png")
    (OUT / "_items.png").unlink()
    sheet = Image.new("RGBA", (220 * len(names), 220), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((210, 210)), (i * 220, 5))
    sheet.save(HERE / "_sheet.png")
    print("rendered", names)


if __name__ == "__main__":
    render()
