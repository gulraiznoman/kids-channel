"""Props + backgrounds for Long video 8 "Colors & Shapes".
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
EYES = lambda x1, x2, y, r=16: (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
                                f'<circle cx="{x1 + 5}" cy="{y - 6}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + 5}" cy="{y - 6}" r="{r * 0.35}" fill="#FFF"/>')
SMILE = lambda cx, cy, w=34: f'<path d="M{cx - w} {cy} Q{cx} {cy + w * 0.9} {cx + w} {cy}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'

I = {}
# ---- colour objects (all new compared with Ep2's balloons)
I["frog"] = f'''<ellipse cx="200" cy="270" rx="150" ry="100" fill="#4CC34A" {SW}/>
<circle cx="135" cy="150" r="52" fill="#4CC34A" {SW}/><circle cx="265" cy="150" r="52" fill="#4CC34A" {SW}/>
<circle cx="135" cy="148" r="30" fill="#FFF"/><circle cx="265" cy="148" r="30" fill="#FFF"/>{EYES(140, 270, 150, 15)}
<path d="M110 260 Q200 330 290 260" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>
<ellipse cx="120" cy="235" rx="18" ry="11" fill="#FF8FA3" opacity="0.7"/><ellipse cx="280" cy="235" rx="18" ry="11" fill="#FF8FA3" opacity="0.7"/>
<path d="M70 340 Q40 370 90 372 L140 360 Z M330 340 Q360 370 310 372 L260 360 Z" fill="#3AA83A" {SW}/>'''
I["cupcake"] = f'''<path d="M100 230 L300 230 L270 370 L130 370 Z" fill="#B07A4E" {SW}/>
<path d="M150 235 L160 368 M200 235 L200 368 M250 235 L240 368" stroke="#8A5A33" stroke-width="6"/>
<path d="M85 235 Q80 170 140 165 Q140 100 200 95 Q260 100 260 165 Q320 170 315 235 Z" fill="#6B3E22" {SW}/>
<path d="M120 200 Q200 225 280 200" stroke="#8A5534" stroke-width="10" fill="none"/>
<circle cx="200" cy="80" r="26" fill="#E8352E" {SW}/><path d="M200 55 Q210 30 230 25" stroke="{INK}" stroke-width="5" fill="none"/>'''
I["tophat"] = f'''<ellipse cx="200" cy="320" rx="175" ry="45" fill="#1E1E24" {SW}/>
<path d="M110 315 L120 90 Q200 70 280 90 L290 315 Z" fill="#26262E" {SW}/>
<ellipse cx="200" cy="92" rx="80" ry="20" fill="#3A3A46" {SW}/>
<path d="M115 255 L285 255 L287 300 L113 300 Z" fill="#111116" stroke="{INK}" stroke-width="5"/>
<path d="M150 110 L145 240" stroke="#55556A" stroke-width="12" stroke-linecap="round" opacity="0.8"/>'''
I["snowman"] = f'''<circle cx="200" cy="290" r="95" fill="#FFFFFF" {SW}/><circle cx="200" cy="140" r="70" fill="#FFFFFF" {SW}/>
<path d="M115 250 L40 190 M285 250 L360 190 M55 202 L40 170 M345 202 L360 170" stroke="#8A5A2B" stroke-width="9" stroke-linecap="round"/>
{EYES(175, 225, 125, 10)}<path d="M200 145 L255 158 L200 165 Z" fill="#FF8A1F" stroke="{INK}" stroke-width="4"/>
<path d="M172 178 Q200 192 228 178" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>
<circle cx="200" cy="255" r="10" fill="{INK}"/><circle cx="200" cy="295" r="10" fill="{INK}"/><circle cx="200" cy="335" r="10" fill="{INK}"/>'''
# ---- shape examples
I["window"] = f'''<rect x="60" y="60" width="280" height="280" rx="8" fill="#FFFFFF" {SW}/>
<rect x="85" y="85" width="105" height="105" fill="#9ED8FF" stroke="{INK}" stroke-width="5"/><rect x="210" y="85" width="105" height="105" fill="#9ED8FF" stroke="{INK}" stroke-width="5"/>
<rect x="85" y="210" width="105" height="105" fill="#9ED8FF" stroke="{INK}" stroke-width="5"/><rect x="210" y="210" width="105" height="105" fill="#9ED8FF" stroke="{INK}" stroke-width="5"/>
<path d="M100 170 L150 100 M225 170 L275 100" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.8"/>'''
I["pizza"] = f'''<path d="M200 370 L50 70 Q200 20 350 70 Z" fill="#FFD966" {SW}/>
<path d="M50 70 Q200 20 350 70 L338 100 Q200 55 62 100 Z" fill="#D9963F" {SW}/>
<circle cx="200" cy="150" r="30" fill="#D9412E" {SW}/><circle cx="150" cy="210" r="24" fill="#D9412E" {SW}/>
<circle cx="245" cy="230" r="22" fill="#D9412E" {SW}/><circle cx="200" cy="300" r="16" fill="#D9412E" {SW}/>'''
I["kite"] = f'''<path d="M200 30 L330 180 L200 330 L70 180 Z" fill="#FF6B8B" {SW}/>
<path d="M200 30 L200 330 M70 180 L330 180" stroke="{INK}" stroke-width="5"/><path d="M200 30 L330 180 L200 180 Z" fill="#FFD23F" stroke="{INK}" stroke-width="5"/>
<path d="M200 180 L70 180 L200 330 Z" fill="#4CC9F0" stroke="{INK}" stroke-width="5"/>
<path d="M200 330 Q240 350 200 370 Q160 385 200 398" stroke="{INK}" stroke-width="5" fill="none"/>
<path d="M200 352 l-22 -12 l0 24 Z M200 352 l22 -12 l0 24 Z" fill="#7ED957" stroke="{INK}" stroke-width="4"/>'''
I["heartcookie"] = f'''<path d="M200 360 L60 215 Q15 150 65 95 Q130 45 200 120 Q270 45 335 95 Q385 150 340 215 Z" fill="#D9963F" {SW}/>
<path d="M200 325 L85 205 Q55 160 90 120 Q140 85 200 150 Q260 85 310 120 Q345 160 315 205 Z" fill="#FF8FB1" stroke="{INK}" stroke-width="4"/>
{"".join(f'<rect x="{x}" y="{y}" width="14" height="6" rx="3" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, c, r in ((150, 160, "#FFF", 30), (250, 170, "#FFD23F", -20), (200, 230, "#4CC9F0", 60), (140, 210, "#7ED957", -40), (255, 225, "#FFF", 10)))}'''
I["birdhouse"] = f'''<path d="M200 50 L340 160 L340 350 L60 350 L60 160 Z" fill="#FFB547" {SW}/>
<path d="M200 50 L340 160 L60 160 Z" fill="#E8573C" {SW}/>
<circle cx="200" cy="245" r="48" fill="{INK}"/><rect x="185" y="310" width="30" height="12" rx="4" fill="#8A5A2B"/>
<path d="M200 316 L200 375" stroke="#8A5A2B" stroke-width="10" stroke-linecap="round"/>'''
HEX = lambda cx, cy, r: " ".join(f"{cx + r * __import__('math').cos(a * 3.14159 / 3):.1f},{cy + r * __import__('math').sin(a * 3.14159 / 3):.1f}" for a in range(6))
I["honeycomb"] = "".join(f'<polygon points="{HEX(x, y, 62)}" fill="{c}" {SW}/>' for x, y, c in (
    (200, 200, "#FFC233"), (107, 146, "#FFB000"), (293, 146, "#FFB000"), (107, 254, "#FFB000"), (293, 254, "#FFB000"), (200, 92, "#FFD45C"), (200, 308, "#FFD45C"))) + \
    '<ellipse cx="185" cy="185" rx="18" ry="10" fill="#FFF3B0" opacity="0.8"/>'
I["dice"] = f'''<path d="M200 60 L340 130 L200 200 L60 130 Z" fill="#FFFFFF" {SW}/><path d="M60 130 L200 200 L200 360 L60 290 Z" fill="#E9E9F2" {SW}/>
<path d="M340 130 L200 200 L200 360 L340 290 Z" fill="#D4D4E2" {SW}/>
<ellipse cx="200" cy="130" rx="20" ry="11" fill="#E8352E"/>
<circle cx="100" cy="190" r="13" fill="{INK}"/><circle cx="160" cy="300" r="13" fill="{INK}"/><circle cx="130" cy="245" r="13" fill="{INK}"/>
<circle cx="240" cy="230" r="13" fill="{INK}"/><circle cx="300" cy="200" r="13" fill="{INK}"/><circle cx="240" cy="320" r="13" fill="{INK}"/><circle cx="300" cy="290" r="13" fill="{INK}"/>'''
I["trafficcone"] = f'''<rect x="60" y="330" width="280" height="40" rx="10" fill="#FF7A1A" {SW}/>
<path d="M170 40 L230 40 L300 335 L100 335 Z" fill="#FF7A1A" {SW}/>
<path d="M152 120 L248 120 L262 180 L138 180 Z M128 225 L272 225 L286 285 L114 285 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'''
I["pyramidegypt"] = f'''<rect x="0" y="300" width="400" height="80" fill="#F2D18B"/>
<path d="M200 60 L360 320 L40 320 Z" fill="#E8B964" {SW}/><path d="M200 60 L360 320 L230 320 Z" fill="#C9954A" {SW}/>
<path d="M120 190 L280 190 M85 255 L315 255" stroke="#B5843F" stroke-width="5"/><circle cx="340" cy="70" r="38" fill="#FFD23F" {SW}/>'''
# ---- 3D shapes (shaded)
DEFS = '''<defs><radialGradient id="sph" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#BDE6FF"/><stop offset="0.5" stop-color="#2EA8FF"/><stop offset="1" stop-color="#1360B8"/></radialGradient>
<linearGradient id="con" x1="0" x2="1"><stop offset="0" stop-color="#FFE47A"/><stop offset="0.6" stop-color="#FFC21A"/><stop offset="1" stop-color="#D99A00"/></linearGradient>
<linearGradient id="cyl" x1="0" x2="1"><stop offset="0" stop-color="#9BEA8C"/><stop offset="0.55" stop-color="#3BC14A"/><stop offset="1" stop-color="#23862E"/></linearGradient></defs>'''
I["sphere"] = DEFS + f'<circle cx="200" cy="200" r="160" fill="url(#sph)" {SW}/><ellipse cx="140" cy="130" rx="40" ry="25" fill="#FFF" opacity="0.6" transform="rotate(-30 140 130)"/>'
I["cube"] = f'''<path d="M200 50 L345 120 L200 190 L55 120 Z" fill="#FF8A8A" {SW}/><path d="M55 120 L200 190 L200 360 L55 290 Z" fill="#F0454B" {SW}/>
<path d="M345 120 L200 190 L200 360 L345 290 Z" fill="#C42B33" {SW}/>'''
I["cone"] = DEFS + f'<path d="M200 40 L345 320 Q200 380 55 320 Z" fill="url(#con)" {SW}/><path d="M55 320 Q200 270 345 320" stroke="{INK}" stroke-width="4" fill="none" stroke-dasharray="12 10"/>'
I["cylinder"] = DEFS + f'''<path d="M70 90 L70 310 Q200 370 330 310 L330 90 Z" fill="url(#cyl)" {SW}/>
<ellipse cx="200" cy="90" rx="130" ry="40" fill="#B7F2AA" {SW}/>'''
I["pyramid3d"] = f'''<path d="M200 40 L360 300 L210 360 Z" fill="#7B4FCF" {SW}/><path d="M200 40 L210 360 L40 300 Z" fill="#A77BEB" {SW}/>'''


def bg_studio():
    splats = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.55"/><circle cx="{x + r * 0.9}" cy="{y + r * 0.6}" r="{r * 0.3}" fill="{c}" opacity="0.55"/>'
                     for x, y, r, c in ((180, 120, 60, "#FF6B6B"), (520, 90, 45, "#FFD23F"), (1380, 110, 55, "#4CC9F0"), (1780, 90, 50, "#7ED957"),
                                        (930, 70, 35, "#B79BEA"), (1650, 330, 40, "#FF9F1C"), (80, 420, 38, "#FF8FB1")))
    return f'''<rect width="1920" height="1080" fill="#FFF6E6"/>{splats}
      <rect x="0" y="790" width="1920" height="290" fill="#E9C79A"/><rect x="0" y="780" width="1920" height="18" fill="#FFFFFF" {SW}/>
      {"".join(f'<rect x="{x}" y="790" width="6" height="290" fill="#D7B282"/>' for x in range(0, 1920, 160))}
      <path d="M150 790 L250 380 L350 790 M250 380 L250 790" stroke="#8A5A2B" stroke-width="16" stroke-linecap="round"/>
      <rect x="120" y="300" width="260" height="330" rx="8" fill="#FFFFFF" {SW}/>
      <circle cx="210" cy="420" r="45" fill="#FF6B6B"/><rect x="250" y="440" width="90" height="90" fill="#4CC9F0"/><path d="M160 590 L220 490 L280 590 Z" fill="#FFD23F"/>
      <rect x="1560" y="250" width="300" height="20" fill="#C08A55" {SW}/><rect x="1560" y="440" width="300" height="20" fill="#C08A55" {SW}/>
      {"".join(f'<rect x="{1580 + i * 45}" y="{170 + (i % 2) * 10}" width="36" height="{80 - (i % 2) * 10}" rx="6" fill="{c}" {SW}/>' for i, c in enumerate(("#FF6B6B", "#FF9F1C", "#FFD23F", "#7ED957", "#4CC9F0", "#B79BEA")))}
      <circle cx="1620" cy="400" r="38" fill="#FF8FB1" {SW}/><rect x="1680" y="365" width="72" height="72" fill="#7ED957" {SW}/><path d="M1770 437 L1810 362 L1850 437 Z" fill="#FFD23F" {SW}/>
      <ellipse cx="960" cy="960" rx="620" ry="80" fill="#FFFFFF" opacity="0.45"/>'''


def bg_sky():
    return f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FD3FF"/><stop offset="1" stop-color="#D9F3FF"/></linearGradient></defs>
      <rect width="1920" height="1080" fill="url(#sk)"/>
      <g fill="#FFFFFF" opacity="0.95">{"".join(f'<ellipse cx="{x}" cy="{y}" rx="110" ry="45"/><ellipse cx="{x + 70}" cy="{y - 25}" rx="70" ry="45"/><ellipse cx="{x - 60}" cy="{y - 15}" rx="55" ry="35"/>' for x, y in ((260, 160), (1640, 140), (980, 90)))}</g>
      <path d="M0 820 Q480 700 960 800 Q1440 900 1920 780 L1920 1080 L0 1080 Z" fill="#7ED957" {SW}/>
      <path d="M0 920 Q600 850 1100 930 Q1500 990 1920 900 L1920 1080 L0 1080 Z" fill="#5DBB46"/>
      {"".join(f'<circle cx="{x}" cy="{y}" r="14" fill="{c}"/><circle cx="{x}" cy="{y}" r="6" fill="#FFD23F"/>' for x, y, c in ((140, 980, "#FF6B8B"), (420, 1020, "#FFFFFF"), (1500, 1000, "#B79BEA"), (1780, 960, "#FF6B8B"), (900, 1040, "#FFFFFF")))}'''


def bg_track():
    return f'''<rect width="1920" height="1080" fill="#BDE8FF"/>
      <circle cx="1720" cy="150" r="80" fill="#FFD23F" {SW}/>
      <path d="M0 640 Q300 420 640 600 Q960 400 1300 590 Q1620 430 1920 600 L1920 1080 L0 1080 Z" fill="#9BDB6A" {SW}/>
      <rect x="0" y="760" width="1920" height="320" fill="#7CC94E"/>
      <rect x="0" y="905" width="1920" height="40" fill="#A0703F"/>
      {"".join(f'<rect x="{x}" y="895" width="26" height="60" fill="#7A4E26"/>' for x in range(10, 1920, 70))}
      <rect x="0" y="900" width="1920" height="10" fill="#8C8C9A"/><rect x="0" y="940" width="1920" height="10" fill="#8C8C9A"/>
      {"".join(f'<path d="M{x} 760 l18 -40 l18 40 Z" fill="#4E9A35"/>' for x in range(60, 1920, 260))}'''


def bg_board():
    return f'''<rect width="1920" height="1080" fill="#FFE7B8"/>
      {"".join(f'<rect x="0" y="{y}" width="1920" height="30" fill="#FFDFA6"/>' for y in range(0, 800, 60))}
      <rect x="0" y="800" width="1920" height="280" fill="#B5835A"/><rect x="0" y="790" width="1920" height="16" fill="#FFFFFF" {SW}/>
      <rect x="300" y="90" width="1320" height="660" rx="20" fill="#A0703F" {SW}/>
      <rect x="330" y="120" width="1260" height="600" rx="10" fill="#2F6B4F" stroke="{INK}" stroke-width="5"/>
      <path d="M380 690 Q520 670 640 695" stroke="#FFFFFF" stroke-width="4" opacity="0.25" fill="none"/>
      <rect x="320" y="735" width="1280" height="26" rx="8" fill="#8A5A2B" {SW}/>
      <rect x="1350" y="728" width="60" height="14" rx="4" fill="#FFFFFF"/><rect x="1430" y="728" width="60" height="14" rx="4" fill="#FFD23F"/>'''


# shape-hunt targets (pixel coords on the street background)
HUNT = {"triangle": ("poly", [(560, 470), (860, 230), (1160, 470)]),
        "square": ("rect", (640, 540, 790, 690)),
        "rectangle": ("rect", (920, 600, 1060, 880)),
        "circle": ("circle", (1660, 170, 95)),
        "diamond": ("poly", [(330, 150), (420, 260), (330, 370), (240, 260)]),
        "oval": ("ellipse", (1380, 920, 1700, 1010))}


def bg_street():
    tri = " ".join(f"{x},{y}" for x, y in HUNT["triangle"][1])
    dia = " ".join(f"{x},{y}" for x, y in HUNT["diamond"][1])
    return f'''<rect width="1920" height="1080" fill="#A8E2FF"/>
      <circle cx="1660" cy="170" r="95" fill="#FFD23F" {SW}/>
      <polygon points="{dia}" fill="#FF6B8B" {SW}/><path d="M330 370 Q360 420 320 460 Q290 500 330 540" stroke="{INK}" stroke-width="5" fill="none"/>
      <rect x="0" y="880" width="1920" height="200" fill="#7ED957"/><rect x="0" y="872" width="1920" height="14" fill="#5DBB46"/>
      <rect x="590" y="470" width="540" height="410" fill="#FFF0C9" {SW}/>
      <polygon points="{tri}" fill="#E8573C" {SW}/>
      <rect x="640" y="540" width="150" height="150" fill="#9ED8FF" {SW}/><path d="M715 540 L715 690 M640 615 L790 615" stroke="{INK}" stroke-width="6"/>
      <rect x="920" y="600" width="140" height="280" rx="6" fill="#4CC9F0" {SW}/><circle cx="1035" cy="745" r="10" fill="#FFD23F" stroke="{INK}" stroke-width="4"/>
      <ellipse cx="1540" cy="965" rx="160" ry="45" fill="#6EC6FF" {SW}/>
      <rect x="140" y="640" width="40" height="240" fill="#8A5A2B" {SW}/><circle cx="160" cy="590" r="110" fill="#5DBB46" {SW}/>
      {"".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/>' for x, y, c in ((400, 960, "#FF6B8B"), (470, 1000, "#FFD23F"), (1260, 990, "#B79BEA")))}'''


BGS = {"studio": bg_studio, "sky": bg_sky, "track": bg_track, "board": bg_board, "street": bg_street}


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
    for k, fn in BGS.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{fn()}</svg></body></html>',
               str(OUT / f"bg_{k}.png"), 1920, 1080)
    sheet = Image.new("RGBA", (180 * 11, 180 * 2 + 300), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((170, 170)), ((i % 11) * 180, (i // 11) * 180))
    for j, k in enumerate(BGS):
        sheet.alpha_composite(Image.open(OUT / f"bg_{k}.png").convert("RGBA").resize((390, 219)), (j * 396, 370))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items +", len(BGS), "bgs")


if __name__ == "__main__":
    render()
