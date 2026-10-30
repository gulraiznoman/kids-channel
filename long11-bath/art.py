"""Props + backgrounds for Long video 11 "Bath Time & Sink or Float".
python art.py -> art/item_<key>.png (800x800), art/bg_<name>.png (1920x1080), _sheet.png
"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)


def eyes(x1, x2, y, r=13):
    return (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{x1 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/>')


I = {}
I["duck"] = f'''<path d="M60 250 Q60 350 200 350 Q330 350 340 260 Q350 200 290 200 L230 200 Q250 170 245 140 Q235 70 165 72 Q100 78 100 145 Q102 185 130 205 Q60 210 60 250 Z" fill="#FFD23F" {SW}/>
<path d="M95 150 Q40 150 35 170 Q45 190 100 178 Z" fill="#FF8A1F" {SW}/>{eyes(150, 195, 125, 12)}
<ellipse cx="135" cy="160" rx="16" ry="9" fill="#FF8FA3" opacity="0.7"/><path d="M200 270 Q250 240 300 265" stroke="#E0A800" stroke-width="10" fill="none"/>'''
I["sponge"] = f'''<rect x="70" y="120" width="260" height="170" rx="40" fill="#FFE27A" {SW}/>
{"".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.7}" fill="#E8C13A"/>' for x, y, r in ((120, 170, 14), (200, 160, 10), (270, 190, 16), (150, 240, 12), (240, 245, 10), (300, 250, 8)))}
<rect x="70" y="250" width="260" height="40" rx="18" fill="#7ED957" stroke="{INK}" stroke-width="5"/>'''
I["shampoo"] = f'''<rect x="170" y="40" width="60" height="50" rx="10" fill="#FF6B8B" {SW}/><rect x="150" y="85" width="100" height="30" rx="8" fill="#FF6B8B" {SW}/>
<path d="M120 120 Q120 105 140 105 L260 105 Q280 105 280 120 L285 360 Q285 380 265 380 L135 380 Q115 380 115 360 Z" fill="#9BD7FF" {SW}/>
<rect x="135" y="190" width="130" height="110" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9BD7FF" stroke="{INK}" stroke-width="3"/>' for x, y, r in ((175, 230, 16), (215, 250, 12), (235, 220, 9)))}'''
I["rock"] = f'''<path d="M70 300 Q50 230 110 190 Q150 130 230 150 Q320 160 340 240 Q350 310 270 330 Q160 345 70 300 Z" fill="#9AA0AE" {SW}/>
<path d="M140 220 Q170 205 200 215 M240 260 Q270 250 290 265" stroke="#7C8190" stroke-width="8" fill="none" stroke-linecap="round"/>'''
I["key"] = f'''<circle cx="110" cy="200" r="70" fill="#FFC928" {SW}/><circle cx="110" cy="200" r="28" fill="#E9F6FF" {SW}/>
<rect x="170" y="180" width="200" height="40" rx="10" fill="#FFC928" {SW}/>
<path d="M290 220 L290 270 L320 270 L320 220 M340 220 L340 255 L365 255 L365 220" fill="#FFC928" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'''
I["coin"] = f'''<circle cx="200" cy="200" r="140" fill="#FFC928" {SW}/><circle cx="200" cy="200" r="105" fill="none" stroke="#E0A800" stroke-width="10"/>
<path d="M200 130 L200 270 M165 160 Q200 130 235 160 Q240 195 200 200 Q160 205 165 240 Q200 270 240 240" stroke="#B88400" stroke-width="14" fill="none" stroke-linecap="round"/>'''
I["spoon"] = f'''<ellipse cx="200" cy="110" rx="70" ry="90" fill="#D4D8E2" {SW}/><ellipse cx="185" cy="95" rx="22" ry="40" fill="#FFFFFF" opacity="0.7"/>
<path d="M200 200 L200 380" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M200 200 L200 380" stroke="#D4D8E2" stroke-width="28" stroke-linecap="round"/>'''
I["leaf"] = f'''<path d="M60 330 Q60 110 340 60 Q330 330 60 330 Z" fill="#7ED957" {SW}/><path d="M70 320 Q200 200 330 75" stroke="#4E9A35" stroke-width="8" fill="none"/>'''
I["toothbrush_cup"] = f'''<path d="M110 180 L290 180 L270 370 L130 370 Z" fill="#4CC9F0" {SW}/>
<path d="M160 180 L130 40 M240 180 L270 50" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M160 180 L130 40" stroke="#FF6B8B" stroke-width="12" stroke-linecap="round"/>
<path d="M240 180 L270 50" stroke="#7ED957" stroke-width="12" stroke-linecap="round"/>'''


BG = {}
BG["bath"] = f'''<rect width="1920" height="1080" fill="#CDEBFF"/>
  {"".join(f'<rect x="{x}" y="{y}" width="118" height="118" rx="8" fill="{"#BFE4FF" if (x // 120 + y // 120) % 2 else "#D9F0FF"}"/>' for x in range(0, 1920, 120) for y in range(0, 720, 120))}
  <rect x="1500" y="140" width="300" height="240" rx="24" fill="#FFFFFF" {SW}/><rect x="1530" y="170" width="240" height="180" rx="16" fill="#9ED8FF"/>
  <path d="M1580 330 Q1600 260 1650 300 Q1700 240 1740 320" stroke="#FFFFFF" stroke-width="10" fill="none"/>
  <rect x="140" y="250" width="220" height="24" rx="10" fill="#FFFFFF" {SW}/>
  <circle cx="190" cy="215" r="34" fill="#FF8FB1" {SW}/><rect x="245" y="170" width="44" height="80" rx="12" fill="#7ED957" {SW}/><rect x="300" y="185" width="40" height="66" rx="12" fill="#FFD23F" {SW}/>
  <rect x="0" y="720" width="1920" height="360" fill="#F2E6D6"/>
  {"".join(f'<rect x="{x}" y="720" width="4" height="360" fill="#E2D2BE"/>' for x in range(0, 1920, 160))}
  <rect x="0" y="712" width="1920" height="16" fill="#FFFFFF" {SW}/>
  <ellipse cx="960" cy="1010" rx="560" ry="60" fill="#8FD4F7" opacity="0.6"/>'''


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
    for k, svg in BG.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>',
               str(OUT / f"bg_{k}.png"), 1920, 1080)
    sheet = Image.new("RGBA", (180 * len(names) + 400, 230), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((170, 170)), (i * 180, 0))
    sheet.alpha_composite(Image.open(OUT / "bg_bath.png").convert("RGBA").resize((390, 220)), (180 * len(names) + 5, 0))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items + bg")


if __name__ == "__main__":
    render()
