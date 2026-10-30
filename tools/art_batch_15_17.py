"""Art for L15 Potty Training, L16 Sharing & Kindness, L17 Christmas Tree.
python tools/art_batch_15_17.py -> long15-potty/art, long16-sharing/art, long17-xmastree/art (+ _sheet.png in tools/)
"""
import math, pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK


def eyes(x1, x2, y, r=12):
    return (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{x1 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/>')


def smile(cx, cy, w=18):
    return f'<path d="M{cx - w} {cy} Q{cx} {cy + w} {cx + w} {cy}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'


SETS = {}
# ------------------------------------------------------------------ L15 potty
P = {}
P["potty"] = f'''<ellipse cx="200" cy="330" rx="150" ry="40" fill="#4CC9F0" {SW}/><path d="M70 200 L90 330 L310 330 L330 200 Z" fill="#4CC9F0" {SW}/>
<ellipse cx="200" cy="200" rx="135" ry="45" fill="#9BE3F7" {SW}/><ellipse cx="200" cy="200" rx="90" ry="26" fill="#3A9BC0"/>
<path d="M300 170 Q350 120 330 90 L300 110 Q310 140 285 175" fill="#4CC9F0" {SW}/>{eyes(170, 230, 260, 9)}{smile(200, 280, 14)}'''
P["toilet"] = f'''<rect x="230" y="40" width="130" height="170" rx="16" fill="#FFFFFF" {SW}/><rect x="250" y="60" width="40" height="14" rx="6" fill="#C9CCD6"/>
<path d="M60 200 Q60 320 160 330 L180 380 L280 380 L290 330 Q340 300 340 210 Z" fill="#FFFFFF" {SW}/>
<ellipse cx="200" cy="205" rx="140" ry="38" fill="#E9EEF5" {SW}/><ellipse cx="195" cy="208" rx="95" ry="22" fill="#9ED8FF"/>'''
P["paper"] = f'''<rect x="90" y="120" width="220" height="200" rx="20" fill="#FFFFFF" {SW}/><ellipse cx="200" cy="120" rx="110" ry="30" fill="#F2F4F8" {SW}/>
<ellipse cx="200" cy="120" rx="35" ry="11" fill="#C9CCD6" {SW}/><path d="M310 170 L360 170 L360 330 L320 310" fill="#FFFFFF" {SW}/>
{"".join(f'<circle cx="340" cy="{y}" r="4" fill="#C9CCD6"/>' for y in (200, 240, 280))}'''
P["stool"] = f'''<path d="M60 200 L340 200 L320 360 L280 360 L270 280 L130 280 L120 360 L80 360 Z" fill="#7ED957" {SW}/>
<rect x="50" y="170" width="300" height="40" rx="14" fill="#9BE36B" {SW}/>'''
P["undies"] = f'''<path d="M60 120 L340 120 L320 210 Q260 230 230 320 L170 320 Q140 230 80 210 Z" fill="#FFD23F" {SW}/>
<rect x="60" y="100" width="280" height="40" rx="12" fill="#FF8FB1" {SW}/>
{"".join(f'<path d="M{x} {y} l8 16 l18 2 l-13 12 l4 18 l-17 -9 l-17 9 l4 -18 l-13 -12 l18 -2 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>' for x, y in ((140, 160), (240, 170), (195, 230)))}'''
P["chart"] = f'''<rect x="50" y="50" width="300" height="300" rx="20" fill="#FFFFFF" {SW}/>
<rect x="50" y="50" width="300" height="60" rx="20" fill="#FF8FB1" {SW}/>
{"".join(f'<rect x="{70 + (i % 4) * 70}" y="{130 + (i // 4) * 70}" width="55" height="55" rx="10" fill="#F2F4F8" stroke="{INK}" stroke-width="4"/>' for i in range(12))}
{"".join(f'<path d="M{97 + (i % 4) * 70} {140 + (i // 4) * 70} l7 14 l16 2 l-12 11 l3 16 l-14 -8 l-14 8 l3 -16 l-12 -11 l16 -2 Z" fill="#FFD23F" stroke="{INK}" stroke-width="3"/>' for i in range(7))}'''
P["star"] = f'''<path d="M200 40 L245 145 L360 155 L272 230 L300 345 L200 285 L100 345 L128 230 L40 155 L155 145 Z" fill="#FFD23F" {SW}/>{eyes(175, 225, 190, 11)}{smile(200, 215, 16)}'''
P["teddy"] = f'''<circle cx="120" cy="90" r="40" fill="#C8894E" {SW}/><circle cx="280" cy="90" r="40" fill="#C8894E" {SW}/>
<ellipse cx="200" cy="290" rx="110" ry="90" fill="#C8894E" {SW}/><circle cx="200" cy="150" r="95" fill="#C8894E" {SW}/>
<ellipse cx="200" cy="185" rx="45" ry="32" fill="#F2C99A"/>{eyes(170, 230, 140, 10)}<ellipse cx="200" cy="172" rx="13" ry="9" fill="{INK}"/>'''
SETS["long15-potty"] = (P, {"bathroom2": f'''<rect width="1920" height="1080" fill="#D9F0E6"/>
  {"".join(f'<rect x="{x}" y="0" width="118" height="720" fill="{"#C6E8D8" if (x // 120) % 2 else "#D9F0E6"}"/>' for x in range(0, 1920, 120))}
  <rect x="0" y="720" width="1920" height="360" fill="#E8D9C4"/>{"".join(f'<rect x="{x}" y="720" width="4" height="360" fill="#D6C4AA"/>' for x in range(0, 1920, 180))}
  <rect x="0" y="712" width="1920" height="16" fill="#FFFFFF" {SW}/>
  <rect x="1460" y="120" width="320" height="250" rx="24" fill="#9ED8FF" {SW}/><path d="M1620 120 L1620 370 M1460 245 L1780 245" stroke="{INK}" stroke-width="10"/>
  <rect x="140" y="230" width="230" height="24" rx="10" fill="#FFFFFF" {SW}/><circle cx="190" cy="200" r="30" fill="#FF8FB1" {SW}/><rect x="235" y="160" width="40" height="72" rx="12" fill="#7ED957" {SW}/>
  <rect x="300" y="175" width="40" height="58" rx="12" fill="#FFD23F" {SW}/>'''})

# ------------------------------------------------------------------ L16 sharing
S = {}
S["cookie"] = f'''<circle cx="200" cy="200" r="150" fill="#D9A066" {SW}/>{"".join(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="14" fill="#6B3E22"/>' for x, y in ((140, 140), (240, 130), (190, 210), (270, 240), (130, 260), (210, 290)))}'''
S["bucket"] = f'''<path d="M100 130 L300 130 L270 350 L130 350 Z" fill="#FF6B6B" {SW}/><ellipse cx="200" cy="130" rx="100" ry="25" fill="#FF8A8A" {SW}/>
<path d="M100 130 Q200 20 300 130" stroke="{INK}" stroke-width="10" fill="none"/>'''
S["spade"] = f'''<path d="M200 40 L200 260" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M200 40 L200 260" stroke="#FFD23F" stroke-width="18" stroke-linecap="round"/>
<path d="M120 250 L280 250 L260 340 Q200 380 140 340 Z" fill="#4CC9F0" {SW}/><rect x="160" y="25" width="80" height="30" rx="12" fill="#FFD23F" {SW}/>'''
S["sandcastle"] = f'''<rect x="60" y="230" width="280" height="120" fill="#F2D18B" {SW}/><rect x="110" y="140" width="180" height="100" fill="#F2D18B" {SW}/>
{"".join(f'<rect x="{x}" y="{y}" width="30" height="30" fill="#F2D18B" {SW}/>' for x, y in ((60, 205), (130, 205), (240, 205), (310, 205), (110, 115), (180, 115), (260, 115)))}
<rect x="180" y="290" width="40" height="60" rx="20" fill="#C9954A" {SW}/><path d="M200 140 L200 60 L250 80 L200 100" fill="#FF6B6B" stroke="{INK}" stroke-width="5"/>'''
S["crayons"] = "".join(f'<g transform="rotate({-20 + i * 10} 200 300)"><rect x="{120 + i * 40}" y="110" width="34" height="200" rx="6" fill="{c}" {SW}/><path d="M{120 + i * 40} 110 L{137 + i * 40} 60 L{154 + i * 40} 110 Z" fill="{c}" {SW}/></g>'
                        for i, c in enumerate(("#FF4D6D", "#FF9F1C", "#FFD23F", "#7ED957", "#4CC9F0")))
S["plate"] = f'''<ellipse cx="200" cy="220" rx="170" ry="80" fill="#FFFFFF" {SW}/><ellipse cx="200" cy="215" rx="120" ry="52" fill="#F2F4F8"/>'''
S["swing"] = open(ROOT / "long12-trucks" / "art.py", encoding="utf-8").read().split('I["swing"] = f\'\'\'')[1].split("'''")[0]
S["car"] = f'''<rect x="60" y="200" width="290" height="90" rx="30" fill="#4CC9F0" {SW}/><path d="M110 200 L150 130 L280 130 L310 200 Z" fill="#4CC9F0" {SW}/>
<path d="M160 145 L200 145 L200 195 L130 195 Z M215 145 L270 145 L295 195 L215 195 Z" fill="#9ED8FF" stroke="{INK}" stroke-width="5"/>
<circle cx="120" cy="295" r="40" fill="#3A3D46" {SW}/><circle cx="290" cy="295" r="40" fill="#3A3D46" {SW}/>'''
S["umbrella"] = f'''<path d="M30 200 Q200 20 370 200 Q330 175 285 200 Q245 175 200 200 Q155 175 115 200 Q70 175 30 200 Z" fill="#FF6B8B" {SW}/>
<path d="M200 200 L200 340 Q200 375 170 370" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>'''
S["heart"] = f'''<path d="M200 350 L70 220 Q20 160 70 100 Q130 50 200 120 Q270 50 330 100 Q380 160 330 220 Z" fill="#FF4D6D" {SW}/>{eyes(165, 235, 180, 11)}{smile(200, 210, 18)}'''
SETS["long16-sharing"] = (S, {})

# ------------------------------------------------------------------ L17 christmas tree
X = {}
X["tree"] = f'''<rect x="175" y="330" width="50" height="50" fill="#8A5A2B" {SW}/>
<path d="M200 30 L300 140 L260 140 L340 240 L290 240 L370 340 L30 340 L110 240 L60 240 L140 140 L100 140 Z" fill="#2E9E4A" {SW}/>
<path d="M140 140 L260 140 M110 240 L290 240" stroke="#25803C" stroke-width="8"/>'''
X["topstar"] = P["star"]
X["present1"] = f'''<rect x="70" y="160" width="260" height="190" rx="12" fill="#FF6B8B" {SW}/><rect x="55" y="125" width="290" height="50" rx="12" fill="#FF8FA3" {SW}/>
<rect x="180" y="125" width="40" height="225" fill="#FFD23F" {SW}/><path d="M200 125 Q130 55 110 100 Q100 135 200 125 Q270 135 290 100 Q270 55 200 125 Z" fill="#FFD23F" {SW}/>'''
X["present2"] = X["present1"].replace("#FF6B8B", "#4CC9F0").replace("#FF8FA3", "#7FD9F5").replace("#FFD23F", "#FFFFFF")
X["present3"] = X["present1"].replace("#FF6B8B", "#7ED957").replace("#FF8FA3", "#A6E87F").replace("#FFD23F", "#FF4D6D")
X["candycane"] = f'''<path d="M220 370 L220 130 Q220 60 160 60 Q100 60 100 120" stroke="{INK}" stroke-width="58" fill="none" stroke-linecap="round"/>
<path d="M220 370 L220 130 Q220 60 160 60 Q100 60 100 120" stroke="#FFFFFF" stroke-width="44" fill="none" stroke-linecap="round"/>
{"".join(f'<path d="M198 {y} L242 {y - 26}" stroke="#E8352E" stroke-width="12"/>' for y in range(150, 370, 40))}<path d="M120 70 L150 100 M175 58 L185 98" stroke="#E8352E" stroke-width="12"/>'''
X["stocking"] = f'''<path d="M120 60 L260 60 L260 250 Q260 280 290 290 Q350 310 330 355 Q300 390 220 360 L150 330 Q120 315 120 280 Z" fill="#E8352E" {SW}/>
<rect x="105" y="40" width="170" height="60" rx="18" fill="#FFFFFF" {SW}/>'''
X["gingerbread"] = f'''<circle cx="200" cy="100" r="62" fill="#C8894E" {SW}/>
<path d="M150 160 L100 190 Q70 210 90 240 Q110 255 140 230 L150 225 L135 330 Q130 370 165 370 Q190 370 195 335 L200 300 L205 335 Q210 370 235 370 Q270 370 265 330 L250 225 L260 230 Q290 255 310 240 Q330 210 300 190 L250 160 Z" fill="#C8894E" {SW}/>
{eyes(180, 220, 92, 9)}{smile(200, 115, 16)}<circle cx="200" cy="200" r="9" fill="#FF4D6D"/><circle cx="200" cy="240" r="9" fill="#7ED957"/>
<path d="M105 200 q10 -8 20 0 M275 200 q10 -8 20 0" stroke="#FFFFFF" stroke-width="6" fill="none"/>'''
X["santahat"] = f'''<path d="M60 300 Q120 80 280 60 Q340 60 330 130 L310 300 Z" fill="#E8352E" {SW}/><rect x="40" y="280" width="320" height="70" rx="30" fill="#FFFFFF" {SW}/>
<circle cx="325" cy="140" r="38" fill="#FFFFFF" {SW}/>'''
X["bell"] = open(ROOT / "long05-body-parts" / "art.py", encoding="utf-8").read().split('I["bell"] = f\'\'\'')[1].split("'''")[0] if 'I["bell"]' in open(ROOT / "long05-body-parts" / "art.py", encoding="utf-8").read() else \
    f'<path d="M120 300 Q120 120 200 100 Q280 120 280 300 Z" fill="#FFD23F" {SW}/><rect x="100" y="290" width="200" height="30" rx="12" fill="#FFD23F" {SW}/><circle cx="200" cy="335" r="22" fill="#E0A000" {SW}/>'
X["snowflake"] = "".join(f'<g transform="rotate({a} 200 200)"><path d="M200 200 L200 50 M200 100 L170 70 M200 100 L230 70 M200 150 L175 125 M200 150 L225 125" stroke="#9ED8FF" stroke-width="16" stroke-linecap="round"/></g>' for a in range(0, 360, 60))
SETS["long17-xmastree"] = (X, {"xmasroom": f'''<rect width="1920" height="1080" fill="#FFE7D1"/>
  {"".join(f'<rect x="{x}" y="0" width="60" height="760" fill="#FFDCC0"/>' for x in range(0, 1920, 120))}
  <rect x="0" y="760" width="1920" height="320" fill="#B5835A"/><rect x="0" y="750" width="1920" height="20" fill="#FFFFFF" {SW}/>
  <rect x="1450" y="120" width="360" height="320" rx="20" fill="#3A4E8C" {SW}/><path d="M1630 120 L1630 440 M1450 280 L1810 280" stroke="{INK}" stroke-width="10"/>
  {"".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#FFFFFF"/>' for x, y in ((1490, 170), (1560, 230), (1700, 160), (1770, 240), (1520, 330), (1660, 380), (1760, 350), (1590, 410)))}
  <path d="M1450 420 Q1630 380 1810 420 L1810 440 L1450 440 Z" fill="#FFFFFF"/>
  <rect x="80" y="420" width="420" height="340" fill="#C9502E" {SW}/><rect x="60" y="400" width="460" height="40" rx="10" fill="#8A3F2B" {SW}/>
  <rect x="160" y="520" width="260" height="240" rx="20" fill="#3A2420" {SW}/>
  <path d="M220 760 Q240 640 290 700 Q310 600 340 690 Q370 640 370 760 Z" fill="#FF9F1C"/><path d="M260 760 Q280 690 300 720 Q320 680 330 760 Z" fill="#FFD23F"/>
  {"".join(f'<path d="M{x} 760 L{x} 700" stroke="#FFFFFF" stroke-width="0"/>' for x in range(0, 1, 1))}
  <path d="M0 40 Q480 120 960 40 Q1440 120 1920 40" stroke="#2E9E4A" stroke-width="18" fill="none"/>
  {"".join(f'<circle cx="{x}" cy="{40 + 80 * (1 - abs(((x % 960) - 480) / 480)) ** 0.8 * 0.5}" r="14" fill="{c}" {SW}/>' for x, c in zip(range(80, 1920, 160), ["#FF4D6D", "#FFD23F", "#4CC9F0", "#7ED957"] * 4))}'''})


def render():
    sheet = Image.new("RGBA", (180 * 14, 180 * 3 + 220), (230, 230, 230, 255))
    for row, (folder, (items, bgs)) in enumerate(SETS.items()):
        out = ROOT / folder / "art"
        out.mkdir(parents=True, exist_ok=True)
        names = list(items)
        cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{items[n]}</svg></div>' for i, n in enumerate(names))
        A.shot(f'<html><body style="margin:0;position:relative;width:{400 * len(names)}px;height:400px">{cells}</body></html>', str(out / "_i.png"), 400 * len(names), 400, scale=2)
        im = Image.open(out / "_i.png")
        for i, n in enumerate(names):
            im.crop((i * 800, 0, i * 800 + 800, 800)).save(out / f"item_{n}.png")
            sheet.alpha_composite(im.crop((i * 800, 0, i * 800 + 800, 800)).convert("RGBA").resize((170, 170)), (i * 180, row * 180))
        (out / "_i.png").unlink()
        for j, (k, svg) in enumerate(bgs.items()):
            A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>', str(out / f"bg_{k}.png"), 1920, 1080)
            sheet.alpha_composite(Image.open(out / f"bg_{k}.png").convert("RGBA").resize((360, 200)), (row * 380, 3 * 180 + 10))
    sheet.save(ROOT / "tools" / "_sheet_15_17.png")
    print("done")


if __name__ == "__main__":
    render()
