"""Truck bodies + props + backgrounds for Long video 12 "Excavator & Construction Trucks".
Truck bodies are drawn WITHOUT wheels / moving parts (render.py animates those). All trucks face LEFT.
viewBox for trucks is 800x400 with the ground at y=380.
python art.py -> art/truck_<key>.png (1600x800), art/item_<key>.png (800x800), art/bg_<name>.png, _sheet.png
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
Y, YD = "#FFC21A", "#E0A000"


def window(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#9ED8FF" {SW}/><path d="M{x + 14} {y + h - 16} L{x + w * 0.45} {y + 14}" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.8"/>'


def tracks(x0, x1, y0=300):
    rollers = "".join(f'<circle cx="{x}" cy="{y0 + 40}" r="22" fill="#6E7280" stroke="{INK}" stroke-width="5"/>' for x in range(x0 + 45, x1 - 20, 70))
    return f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="80" rx="40" fill="#3A3D46" {SW}/>{rollers}'


T = {}
T["excavator"] = f'''{tracks(150, 590)}<rect x="200" y="270" width="340" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M220 270 L220 170 Q220 140 250 140 L360 140 L360 270 Z" fill="{Y}" {SW}/>{window(240, 160, 100, 80)}
<rect x="360" y="180" width="200" height="90" rx="16" fill="{Y}" {SW}/><rect x="540" y="150" width="20" height="60" fill="#4A4F5C" {SW}/>
<path d="M375 215 L545 215" stroke="{YD}" stroke-width="10"/>'''
T["dumptruck"] = f'''<rect x="60" y="290" width="680" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M60 300 L60 180 Q60 140 100 130 L230 120 L250 300 Z" fill="{Y}" {SW}/>{window(85, 145, 120, 80)}
<rect x="40" y="250" width="40" height="30" rx="8" fill="#FFF3B0" {SW}/><rect x="250" y="160" width="30" height="140" fill="#4A4F5C" {SW}/>'''
T["bulldozer"] = f'''{tracks(220, 680)}<path d="M260 300 L260 170 L460 170 L460 120 L600 120 L640 300 Z" fill="{Y}" {SW}/>{window(480, 140, 100, 90)}
<path d="M270 210 L450 210" stroke="{YD}" stroke-width="10"/><rect x="380" y="90" width="18" height="80" fill="#4A4F5C" {SW}/>
<path d="M220 300 L120 260 L130 230 L230 260" stroke="#4A4F5C" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M60 160 Q110 230 70 380 L140 380 Q170 260 130 160 Z" fill="{YD}" {SW}/>'''
T["mixer"] = f'''<rect x="60" y="290" width="680" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M60 300 L60 180 Q60 140 100 130 L230 120 L250 300 Z" fill="#FF6B6B" {SW}/>{window(85, 145, 120, 80)}
<rect x="40" y="250" width="40" height="30" rx="8" fill="#FFF3B0" {SW}/><path d="M700 290 L740 170 L720 160 L670 290" fill="#4A4F5C" {SW}/>'''
T["crane"] = f'''<rect x="60" y="290" width="680" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M60 300 L60 180 Q60 140 100 130 L230 120 L250 300 Z" fill="#FF9F1C" {SW}/>{window(85, 145, 120, 80)}
<rect x="300" y="220" width="420" height="80" rx="12" fill="#FF9F1C" {SW}/><rect x="560" y="170" width="120" height="60" rx="10" fill="#E8851A" {SW}/>
<rect x="40" y="250" width="40" height="30" rx="8" fill="#FFF3B0" {SW}/>'''
T["roller"] = f'''<path d="M300 300 L300 160 L560 160 L560 120 L660 120 L700 300 Z" fill="#7ED957" {SW}/>{window(570, 140, 80, 90)}
<rect x="300" y="290" width="400" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M300 220 L170 220" stroke="#4A4F5C" stroke-width="30" stroke-linecap="round"/><rect x="90" y="150" width="160" height="40" rx="10" fill="#5CC060" {SW}/>'''
T["towtruck"] = f'''<rect x="60" y="290" width="680" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M60 300 L60 180 Q60 140 100 130 L230 120 L250 300 Z" fill="#4CC9F0" {SW}/>{window(85, 145, 120, 80)}
<rect x="250" y="230" width="380" height="70" rx="10" fill="#3BA8D0" {SW}/><path d="M560 230 L700 110 L740 130" stroke="#4A4F5C" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M740 130 L740 220 Q740 250 715 245" stroke="{INK}" stroke-width="10" fill="none"/><rect x="40" y="250" width="40" height="30" rx="8" fill="#FFF3B0" {SW}/>
<rect x="140" y="105" width="60" height="22" rx="8" fill="#FF9F1C" {SW}/>'''
T["monster"] = f'''<path d="M120 200 L160 120 Q170 100 200 100 L420 100 Q450 100 470 130 L560 180 L680 190 Q710 195 710 230 L710 260 L110 260 Q90 260 95 235 Z" fill="#9B5DE5" {SW}/>
{window(200, 120, 110, 70)}{window(330, 120, 110, 70)}<path d="M130 230 L700 230" stroke="#7B3FC8" stroke-width="10"/>
<path d="M480 150 L660 150" stroke="#FFD23F" stroke-width="16" stroke-linecap="round"/><rect x="200" y="255" width="420" height="30" rx="10" fill="#4A4F5C" {SW}/>'''
T["garbage"] = f'''<rect x="60" y="290" width="680" height="40" rx="10" fill="#4A4F5C" {SW}/>
<path d="M60 300 L60 180 Q60 140 100 130 L230 120 L250 300 Z" fill="#3BB54A" {SW}/>{window(85, 145, 120, 80)}
<path d="M250 300 L250 110 Q250 90 270 90 L690 90 Q730 90 735 130 L745 300 Z" fill="#2E9440" {SW}/>
<rect x="320" y="150" width="300" height="80" rx="18" fill="#FFFFFF" {SW}/><path d="M360 200 l25 -30 l25 30 M430 200 l25 -30 l25 30 M500 200 l25 -30 l25 30" stroke="#3BB54A" stroke-width="10" fill="none" stroke-linecap="round"/>
<rect x="40" y="250" width="40" height="30" rx="8" fill="#FFF3B0" {SW}/>'''

I = {}
I["dirt"] = f'''<path d="M20 360 Q60 200 160 170 Q220 110 280 170 Q370 200 380 360 Z" fill="#A0703F" {SW}/>
{"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#7A522C"/>' for x, y, r in ((120, 280, 14), (200, 230, 10), (280, 300, 16), (170, 330, 9), (310, 250, 8)))}'''
I["slide"] = f'''<path d="M280 380 L280 90 M340 380 L340 90" stroke="#4CC9F0" stroke-width="18"/>{"".join(f'<path d="M280 {y} L340 {y}" stroke="#4CC9F0" stroke-width="12"/>' for y in (140, 200, 260, 320))}
<rect x="250" y="70" width="120" height="30" rx="10" fill="#FF6B6B" {SW}/><path d="M260 100 Q160 120 120 260 Q90 360 30 370 L60 390 Q130 380 165 280 Q200 160 280 130 Z" fill="#FFD23F" {SW}/>'''
I["swing"] = f'''<path d="M60 380 L120 60 L180 380 M220 380 L280 60 L340 380" stroke="#FF6B6B" stroke-width="16" fill="none" stroke-linejoin="round"/>
<rect x="100" y="45" width="200" height="30" rx="10" fill="#FF6B6B" {SW}/><path d="M170 75 L170 270 M230 75 L230 270" stroke="{INK}" stroke-width="5"/>
<rect x="150" y="265" width="100" height="22" rx="8" fill="#7ED957" {SW}/>'''
I["cone"] = f'''<rect x="80" y="330" width="240" height="40" rx="10" fill="#FF7A1A" {SW}/><path d="M175 50 L225 50 L290 335 L110 335 Z" fill="#FF7A1A" {SW}/>
<path d="M155 130 L245 130 L258 185 L142 185 Z M132 230 L268 230 L280 285 L120 285 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'''
I["hardhat"] = f'''<path d="M60 260 Q60 110 200 100 Q340 110 340 260 Z" fill="{Y}" {SW}/><rect x="30" y="250" width="340" height="40" rx="18" fill="{Y}" {SW}/>
<path d="M200 105 L200 255" stroke="{YD}" stroke-width="22"/>'''
I["toytruck"] = f'''<rect x="80" y="230" width="250" height="60" rx="12" fill="#FF6B6B" {SW}/><path d="M80 240 L80 170 L170 170 L190 240 Z" fill="#FF6B6B" {SW}/>{window(95, 182, 70, 45)}
<circle cx="130" cy="300" r="30" fill="#3A3D46" {SW}/><circle cx="280" cy="300" r="30" fill="#3A3D46" {SW}/>'''

BG = {}
BG["site"] = f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ED3FF"/><stop offset="1" stop-color="#E4F6FF"/></linearGradient></defs>
  <rect width="1920" height="1080" fill="url(#sk)"/><circle cx="1700" cy="160" r="80" fill="#FFD23F" {SW}/>
  <g fill="#FFFFFF">{"".join(f'<ellipse cx="{x}" cy="{y}" rx="100" ry="40"/><ellipse cx="{x + 60}" cy="{y - 22}" rx="62" ry="38"/>' for x, y in ((260, 150), (900, 110)))}</g>
  <path d="M1350 640 L1350 200 L1370 200 L1370 640 M1350 220 L1680 220 M1360 210 L1300 230" stroke="#B5BAC6" stroke-width="16" fill="none"/>
  <path d="M1350 260 L1680 230" stroke="#B5BAC6" stroke-width="6"/><path d="M1600 220 L1600 330" stroke="{INK}" stroke-width="4"/>
  {"".join(f'<rect x="{x}" y="520" width="18" height="130" fill="#D9A066"/>' for x in range(30, 1920, 160))}
  <rect x="0" y="540" width="1920" height="18" fill="#FF9F1C"/><rect x="0" y="590" width="1920" height="18" fill="#FF9F1C"/>
  <rect x="0" y="640" width="1920" height="440" fill="#C9935F"/><path d="M0 640 L1920 640" stroke="{INK}" stroke-width="6"/>
  {"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#A0703F"/>' for x, y, r in [((i * 233) % 1920, 700 + (i * 97) % 360, 6 + i % 8) for i in range(40)])}'''
BG["city"] = f'''<rect width="1920" height="1080" fill="#A8E2FF"/>
  {"".join(f'<rect x="{x}" y="{y}" width="{w}" height="{700 - y}" fill="{c}" {SW}/>' + "".join(f'<rect x="{x + 25 + i * 60}" y="{yy}" width="35" height="40" fill="#FFF3B0" stroke="{INK}" stroke-width="3"/>' for i in range(int((w - 40) / 60)) for yy in range(y + 30, 640, 80)) for x, y, w, c in ((0, 300, 260, "#FF8FA3"), (290, 200, 300, "#B79BEA"), (620, 340, 260, "#7ED957"), (1040, 240, 280, "#4CC9F0"), (1350, 330, 250, "#FFD23F"), (1640, 220, 280, "#FF9F80")))}
  <rect x="0" y="700" width="1920" height="60" fill="#BFC4CF" {SW}/><rect x="0" y="760" width="1920" height="320" fill="#5C6070"/>
  {"".join(f'<rect x="{x}" y="900" width="100" height="16" rx="6" fill="#FFFFFF"/>' for x in range(40, 1920, 200))}'''
BG["park"] = f'''<rect width="1920" height="1080" fill="#A8E2FF"/><circle cx="1700" cy="160" r="80" fill="#FFD23F" {SW}/>
  <path d="M0 640 Q480 590 960 630 Q1440 670 1920 610 L1920 1080 L0 1080 Z" fill="#7ED957" {SW}/>
  <rect x="0" y="880" width="1920" height="200" fill="#9AA0AE"/><path d="M0 880 L1920 880" stroke="{INK}" stroke-width="6"/>
  {"".join(f'<rect x="{x}" y="970" width="110" height="16" rx="6" fill="#FFFFFF"/>' for x in range(40, 1920, 220))}'''


def render():
    names = list(T)
    cells = "".join(f'<div style="position:absolute;left:{i * 800}px;top:0;width:800px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">{T[n]}</svg></div>' for i, n in enumerate(names))
    A.shot(f'<html><body style="margin:0;position:relative;width:{800 * len(names)}px;height:400px">{cells}</body></html>', str(OUT / "_t.png"), 800 * len(names), 400, scale=2)
    im = Image.open(OUT / "_t.png")
    for i, n in enumerate(names):
        im.crop((i * 1600, 0, i * 1600 + 1600, 800)).save(OUT / f"truck_{n}.png")
    (OUT / "_t.png").unlink()
    names2 = list(I)
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{I[n]}</svg></div>' for i, n in enumerate(names2))
    A.shot(f'<html><body style="margin:0;position:relative;width:{400 * len(names2)}px;height:400px">{cells}</body></html>', str(OUT / "_i.png"), 400 * len(names2), 400, scale=2)
    im = Image.open(OUT / "_i.png")
    for i, n in enumerate(names2):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_{n}.png")
    (OUT / "_i.png").unlink()
    for k, svg in BG.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>', str(OUT / f"bg_{k}.png"), 1920, 1080)
    sheet = Image.new("RGBA", (4 * 340, 3 * 180 + 220), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"truck_{n}.png").resize((320, 160)), ((i % 4) * 340, (i // 4) * 180))
    for i, n in enumerate(names2):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((150, 150)), (i * 160, 2 * 180 + 10))
    for j, k in enumerate(BG):
        sheet.alpha_composite(Image.open(OUT / f"bg_{k}.png").convert("RGBA").resize((360, 200)), (j * 380, 3 * 180 + 10))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "trucks,", len(names2), "items,", len(BG), "bgs")


if __name__ == "__main__":
    render()
