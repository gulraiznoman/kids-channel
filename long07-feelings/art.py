"""Props + backgrounds for Long video 7 "Feelings & Emotions".
python art.py -> art/item_<key>.png (800x800), art/bg_<name>.png (1920x1080), _sheet.png
"""
import math, pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)

I = {}
I["gift"] = f'''<rect x="70" y="170" width="260" height="190" rx="14" fill="#FF6B8B" {SW}/><rect x="50" y="130" width="300" height="60" rx="12" fill="#FF8FA3" {SW}/>
<rect x="180" y="130" width="40" height="230" fill="#FFD23F" {SW}/>
<path d="M200 130 Q130 50 110 100 Q100 140 200 130 Q270 140 290 100 Q270 50 200 130 Z" fill="#FFD23F" {SW}/>'''
I["balloons"] = "".join(f'<path d="M{x} {y + 85} Q{x + 10} {y + 170} 200 370" stroke="{INK}" stroke-width="4" fill="none"/>'
                        f'<ellipse cx="{x}" cy="{y}" rx="62" ry="78" fill="{c}" {SW}/><ellipse cx="{x - 20}" cy="{y - 30}" rx="12" ry="20" fill="#FFFFFF" opacity="0.6"/>'
                        for x, y, c in ((120, 140, "#FF6B6B"), (200, 100, "#4CC9F0"), (285, 150, "#FFD23F")))
I["drawing"] = f'''<rect x="40" y="50" width="320" height="300" rx="10" fill="#FFFFFF" {SW}/>
<rect x="110" y="190" width="160" height="120" fill="#FF8FA3" stroke="{INK}" stroke-width="5"/><path d="M95 195 L190 120 L285 195 Z" fill="#E8352E" stroke="{INK}" stroke-width="5"/>
<rect x="170" y="240" width="40" height="70" fill="#8A5A2B"/><circle cx="310" cy="100" r="28" fill="#FFD23F"/>
<path d="M40 330 L360 330" stroke="#5DBB46" stroke-width="20"/>'''
I["candle"] = f'''<rect x="160" y="180" width="80" height="180" rx="10" fill="#FFB3C7" {SW}/>
<path d="M200 180 L200 150" stroke="{INK}" stroke-width="6"/>
<path d="M200 70 Q235 110 220 140 Q200 160 180 140 Q165 110 200 70 Z" fill="#FFB020" {SW}/><path d="M200 100 Q215 120 205 138 Q195 145 190 135 Q188 120 200 100 Z" fill="#FFE27A"/>'''
I["ballbroken"] = f'''<path d="M60 250 Q60 140 170 120 L190 250 Z" fill="#2EA8FF" {SW} transform="rotate(-12 150 200)"/>
<path d="M210 120 Q330 130 340 250 L230 250 Z" fill="#FFD23F" {SW} transform="rotate(14 270 200)"/>
<path d="M120 300 l20 -30 l20 30 M250 300 l20 -30 l20 30" stroke="{INK}" stroke-width="6" fill="none"/>'''
I["icecream_drop"] = f'''<ellipse cx="200" cy="330" rx="140" ry="36" fill="#FF9EB5" {SW}/><circle cx="200" cy="300" r="70" fill="#FF9EB5" {SW}/>
<path d="M260 190 L330 120 L380 220 Z" fill="#E6B26A" {SW}/>'''
I["thunder"] = f'''<g fill="#9AA5B8" {SW}><ellipse cx="200" cy="140" rx="150" ry="75"/><ellipse cx="120" cy="170" rx="85" ry="60"/><ellipse cx="290" cy="170" rx="90" ry="60"/></g>
<rect x="60" y="150" width="280" height="60" fill="#9AA5B8"/>
<path d="M210 200 L160 290 L205 290 L170 380 L270 260 L220 260 L250 200 Z" fill="#FFD23F" {SW}/>'''
I["puzzle"] = f'''<path d="M60 120 L170 120 Q170 80 200 80 Q230 80 230 120 L340 120 L340 230 Q380 230 380 260 Q380 290 340 290 L340 360 L60 360 Z" fill="#7ED957" {SW}/>
<path d="M200 120 L200 360 M60 240 L340 240" stroke="{INK}" stroke-width="6"/>'''
I["pillow"] = f'''<rect x="40" y="150" width="320" height="190" rx="70" fill="#B79BEA" {SW}/>
<path d="M90 245 Q200 220 310 245" stroke="#9B7BD6" stroke-width="10" fill="none"/>'''
I["speech"] = f'''<path d="M60 90 Q60 50 100 50 L300 50 Q340 50 340 90 L340 230 Q340 270 300 270 L170 270 L110 340 L120 270 L100 270 Q60 270 60 230 Z" fill="#FFFFFF" {SW}/>
<path d="M150 170 l50 40 l70 -80" stroke="#FF6B8B" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''
I["hearthug"] = f'''<path d="M200 350 L70 220 Q20 160 70 100 Q130 50 200 120 Q270 50 330 100 Q380 160 330 220 Z" fill="#FF4D6D" {SW}/>
<ellipse cx="140" cy="150" rx="26" ry="14" fill="#FFFFFF" opacity="0.5" transform="rotate(-30 140 150)"/>'''


def bg_room():
    return f'''<rect width="1920" height="1080" fill="#FFE9D6"/>
      {"".join(f'<rect x="{x}" y="0" width="60" height="760" fill="#FFDCC2"/>' for x in range(0, 1920, 120))}
      <rect x="0" y="760" width="1920" height="320" fill="#C9935F"/><rect x="0" y="750" width="1920" height="20" fill="#FFFFFF" {SW}/>
      <rect x="1440" y="130" width="340" height="300" rx="20" fill="#9ED8FF" {SW}/><path d="M1610 130 L1610 430 M1440 280 L1780 280" stroke="{INK}" stroke-width="10"/>
      <path d="M1420 120 Q1500 260 1440 440 L1400 440 Z M1800 120 Q1720 260 1780 440 L1820 440 Z" fill="#FF8FA3" {SW}/>
      <rect x="140" y="170" width="260" height="190" rx="12" fill="#FFFFFF" {SW}/>
      {"".join(f'<circle cx="{200 + i * 70}" cy="265" r="26" fill="{c}" {SW.replace("6", "4")}/>' for i, c in enumerate(("#FFD23F", "#4CC9F0", "#FF6B6B")))}
      <path d="M600 760 L600 560 Q600 520 640 520 L1280 520 Q1320 520 1320 560 L1320 760 Z" fill="#4CC9F0" {SW}/>
      <rect x="560" y="600" width="800" height="170" rx="40" fill="#5DD3F5" {SW}/>
      <rect x="660" y="560" width="180" height="80" rx="30" fill="#FFD23F" {SW}/><rect x="1080" y="560" width="180" height="80" rx="30" fill="#FF8FA3" {SW}/>
      <ellipse cx="960" cy="960" rx="600" ry="90" fill="#FFB38A" opacity="0.8"/>
      <rect x="1600" y="560" width="30" height="200" fill="#8A5A2B"/><path d="M1540 560 L1690 560 L1650 460 L1580 460 Z" fill="#FFE27A" {SW}/>'''


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
    A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{bg_room()}</svg></body></html>',
           str(OUT / "bg_room.png"), 1920, 1080)
    sheet = Image.new("RGBA", (180 * len(names), 180 + 300), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((170, 170)), (i * 180, 0))
    sheet.alpha_composite(Image.open(OUT / "bg_room.png").convert("RGBA").resize((520, 292)), (0, 184))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items + room bg")


if __name__ == "__main__":
    render()
