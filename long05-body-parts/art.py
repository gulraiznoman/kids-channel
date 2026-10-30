"""Art for Long video 5 "Body Parts": sense icons + sense objects + playroom/park backgrounds.
python art.py -> art/item_<key>.png (800x800), art/bg_<name>.png (1920x1080), _sheet.png
"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
SHINE = lambda x, y, rx, ry: f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#FFFFFF" opacity="0.45" transform="rotate(-30 {x} {y})"/>'
SKIN = "#DCA27A"

I = {}
# ------------------------------------------------------------------ sense icons
I["eye"] = f'''<path d="M30 200 Q200 40 370 200 Q200 360 30 200 Z" fill="#FFFFFF" {SW}/><circle cx="200" cy="200" r="85" fill="#6B4423" {SW}/>
<circle cx="200" cy="200" r="42" fill="#1B120E"/><circle cx="175" cy="175" r="18" fill="#FFFFFF"/>
<path d="M60 150 L35 110 M110 105 L95 60 M170 85 L165 40 M230 85 L235 40 M290 105 L305 60 M340 150 L365 110" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'''
I["ear"] = f'''<path d="M150 60 Q300 40 310 190 Q315 270 250 300 Q215 315 215 350 Q210 385 160 375 Q110 365 120 300 Q125 250 110 200 Q90 80 150 60 Z" fill="{SKIN}" {SW}/>
<path d="M170 110 Q260 100 260 190 Q258 240 215 255" stroke="#B9774D" stroke-width="14" fill="none" stroke-linecap="round"/>
<path d="M330 150 q30 50 0 100 M360 120 q45 80 0 160" stroke="#2EA8FF" stroke-width="10" fill="none" stroke-linecap="round"/>'''
I["nose"] = f'''<path d="M190 60 Q215 60 225 120 L270 270 Q285 320 240 330 Q220 335 200 320 Q180 335 160 330 Q115 320 130 270 L175 120 Q180 60 190 60 Z" fill="{SKIN}" {SW}/>
<ellipse cx="170" cy="300" rx="18" ry="11" fill="#8A4F2F"/><ellipse cx="230" cy="300" rx="18" ry="11" fill="#8A4F2F"/>
<path d="M60 180 q-25 -30 0 -60 M90 200 q-30 -45 0 -90" stroke="#7ED957" stroke-width="9" fill="none" stroke-linecap="round"/>'''
I["mouth"] = f'''<path d="M50 170 Q200 130 350 170 Q330 340 200 345 Q70 340 50 170 Z" fill="#B23A4A" {SW}/>
<path d="M75 175 Q200 150 325 175 L320 205 Q200 185 80 205 Z" fill="#FFFFFF"/><ellipse cx="200" cy="290" rx="80" ry="38" fill="#FF7A90"/>'''
I["hand"] = f'''<path d="M100 360 L100 210 Q100 180 125 180 Q150 180 150 210 L150 110 Q150 82 175 82 Q200 82 200 110 L200 95 Q200 67 225 67 Q250 67 250 95 L250 120 Q250 93 275 93 Q300 93 300 120 L300 245 Q320 200 345 205 Q370 213 355 250 L310 360 Z" fill="{SKIN}" {SW}/>'''
# ------------------------------------------------------------------ sense objects
I["bell"] = f'''<path d="M200 50 Q290 60 300 170 L320 280 L80 280 L100 170 Q110 60 200 50 Z" fill="#FFD23F" {SW}/><rect x="60" y="275" width="280" height="35" rx="16" fill="#F2B705" {SW}/>
<circle cx="200" cy="335" r="28" fill="#F2B705" {SW}/><rect x="185" y="25" width="30" height="35" rx="10" fill="#F2B705" {SW}/>{SHINE(150, 150, 22, 50)}'''
I["icecream"] = f'''<path d="M120 200 L280 200 L200 380 Z" fill="#E6B26A" {SW}/><path d="M140 240 L260 240 M160 285 L240 285 M175 330 L225 330" stroke="#C98F45" stroke-width="7"/>
<circle cx="200" cy="150" r="85" fill="#FF9EB5" {SW}/><circle cx="140" cy="200" r="45" fill="#FF9EB5" {SW}/><circle cx="260" cy="200" r="45" fill="#FF9EB5" {SW}/>
<path d="M200 65 Q190 40 210 25" stroke="#E8352E" stroke-width="10" fill="none"/><circle cx="212" cy="30" r="22" fill="#E8352E" {SW}/>'''
I["cactus"] = f'''<path d="M150 360 L250 360 L240 300 L160 300 Z" fill="#E07A5F" {SW}/><rect x="160" y="80" width="80" height="225" rx="40" fill="#4CAF50" {SW}/>
<path d="M160 200 L110 200 Q90 200 90 180 L90 130 Q90 110 110 115 Q120 118 120 135 L120 170 L160 170" fill="#4CAF50" {SW}/>
<path d="M240 160 L290 160 Q310 160 310 140 L310 110 Q310 90 290 95 Q280 98 280 115 L280 130 L240 130" fill="#4CAF50" {SW}/>''' + "".join(
    f'<path d="M{x} {y} l12 -8 M{x} {y} l12 8" stroke="{INK}" stroke-width="4"/>' for x, y in ((240, 110), (240, 190), (240, 260), (148, 140), (148, 230), (300, 120), (100, 150)))
I["flower"] = f'''<path d="M200 380 L200 220" stroke="#3E9C2E" stroke-width="16"/><path d="M200 300 Q140 280 120 230 Q180 235 200 300 Z" fill="#5DBB46" {SW}/>''' + "".join(
    f'<circle cx="{200 + 62 * __import__("math").cos(k * 1.2566):.0f}" cy="{160 + 62 * __import__("math").sin(k * 1.2566):.0f}" r="48" fill="#FF6B8B" {SW}/>' for k in range(5)) + \
    f'<circle cx="200" cy="160" r="42" fill="#FFD23F" {SW}/>'
I["drum"] = f'''<ellipse cx="200" cy="140" rx="150" ry="45" fill="#FFF3D6" {SW}/><path d="M50 140 L50 300 Q200 370 350 300 L350 140 Q200 210 50 140 Z" fill="#E8352E" {SW}/>
<path d="M50 160 L120 300 L200 175 L280 300 L350 160" stroke="#FFD23F" stroke-width="10" fill="none"/>
<path d="M120 40 L190 130 M290 40 L220 130" stroke="#C08A4D" stroke-width="16" stroke-linecap="round"/>'''


def room(wall, floor, extra=""):
    return f'''<rect width="1920" height="1080" fill="{wall}"/><rect y="770" width="1920" height="310" fill="{floor}"/>
      <rect y="760" width="1920" height="20" fill="#FFFFFF" {SW}/>{extra}'''


ABC = "".join(f'<rect x="{30 + i * 72}" y="30" width="62" height="62" rx="10" fill="{c}" {SW}/>'
              f'<text x="{46 + i * 72}" y="78" font-size="44" font-family="Arial Black" fill="#FFFFFF">{ch}</text>'
              for i, (ch, c) in enumerate(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", ["#FF6B6B", "#FFB020", "#7ED957", "#2EA8FF", "#B57BFF"] * 6)))
BGS = {
    "playroom": room("#E3F4FF", "#F2C98A", f'''{ABC}
      <rect x="120" y="300" width="300" height="220" rx="14" fill="#FFFFFF" {SW}/><circle cx="270" cy="380" r="55" fill="#FFD23F"/>
      <path d="M150 500 Q270 420 390 500 Z" fill="#7ED957"/>
      <rect x="1520" y="260" width="300" height="420" rx="20" fill="#C08A4D" {SW}/>
      {"".join(f'<rect x="1540" y="{y}" width="260" height="14" fill="#A06C35"/>' for y in (380, 520))}
      {"".join(f'<rect x="{x}" y="{y}" width="40" height="80" rx="6" fill="{c}" {SW}/>' for x, y, c in ((1560, 295, "#FF6B6B"), (1610, 295, "#2EA8FF"), (1660, 295, "#FFD23F"), (1570, 435, "#7ED957"), (1640, 435, "#B57BFF")))}
      <ellipse cx="960" cy="930" rx="560" ry="100" fill="#FFB3C7" opacity="0.7"/>'''),
    "park": f'''{A.sky_and_clouds(1920)}<path d="M0 640 Q480 560 960 620 Q1440 680 1920 600 L1920 1080 L0 1080 Z" fill="#8DD16A"/>
      <rect x="0" y="860" width="1920" height="220" fill="#7CC456"/>
      <rect x="160" y="420" width="40" height="260" fill="#8A5A2B" {SW}/><circle cx="180" cy="390" r="120" fill="#4CAF50" {SW}/><circle cx="110" cy="440" r="80" fill="#5DBB46" {SW}/>
      <path d="M1500 700 L1560 420 L1620 700 M1530 560 L1590 560" stroke="#FF6B6B" stroke-width="18" fill="none"/>
      <path d="M1600 440 Q1760 500 1800 700" stroke="#2EA8FF" stroke-width="26" fill="none" stroke-linecap="round"/>
      {"".join(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}"/>' for x, y, c in ((400, 900, "#FFD23F"), (700, 960, "#FF6B8B"), (1100, 920, "#FFFFFF"), (1350, 980, "#B57BFF")))}''',
}


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
    for n, svg in BGS.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>',
               str(OUT / f"bg_{n}.png"), 1920, 1080)
    sheet = Image.new("RGBA", (160 * len(names), 160 + 300), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((150, 150)), (i * 160, 0))
    for j, n in enumerate(BGS):
        sheet.alpha_composite(Image.open(OUT / f"bg_{n}.png").convert("RGBA").resize((520, 292)), (j * 530, 164))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items +", len(BGS), "backgrounds")


if __name__ == "__main__":
    render()
