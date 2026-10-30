"""Cute (never scary) cartoon dinosaurs + dino props + prehistoric backgrounds + explorer hats.
All full-body, side view facing RIGHT, big friendly eyes, rosy cheeks, smiles.

python art.py -> art/dino_<key>.png, art/item_<key>.png (800x800), art/bg_<name>.png (1920x1080), art/hat_<gul|misheal>.png, _sheet.png
"""
import math, pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as A
import animals_v2 as AV

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
eye, cheek = AV.eye, AV.cheek


def smile(x, y, w=16):
    return f'<path d="M{x - w} {y} Q{x} {y + w} {x + w} {y}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'


def leg(x, y, w, h, col):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w / 2.2:.0f}" fill="{col}" {SW}/>'
            f'<path d="M{x + 6} {y + h - 4} l0 -10 M{x + w / 2:.0f} {y + h - 4} l0 -10 M{x + w - 6} {y + h - 4} l0 -10" stroke="{INK}" stroke-width="4"/>')


def spots(pts, col):
    return "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.75:.0f}" fill="{col}" opacity="0.55"/>' for x, y, r in pts)


D = {}
# ---------------- T-Rex (green), big head, tiny arms
G1, G2, G3 = "#6CC24A", "#D8F0A0", "#4E9A36"
D["trex"] = f'''
<path d="M120 230 Q60 250 10 300 Q70 285 130 275 Z" fill="{G1}" {SW}/>
{leg(130, 280, 46, 90, G3)}
<ellipse cx="175" cy="235" rx="90" ry="72" fill="{G1}" {SW}/>
<ellipse cx="190" cy="260" rx="55" ry="40" fill="{G2}"/>
{leg(185, 285, 48, 90, G1)}
<path d="M240 250 q30 0 32 20 q-10 6 -18 -6" fill="{G1}" {SW}/>
<path d="M210 170 Q230 70 310 70 Q385 75 385 145 Q385 195 330 200 L240 205 Z" fill="{G1}" {SW}/>
<path d="M300 172 Q345 190 380 160" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M318 178 l6 12 l6 -10 M338 178 l6 12 l6 -10" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>
{eye(300, 118, 20)}{cheek(345, 150, 14)}
{spots([(150, 210, 14), (120, 250, 10), (270, 100, 10)], G3)}
<path d="M240 70 l14 -18 l10 18 l14 -20 l10 20" fill="{G3}" {SW}/>'''
# ---------------- Triceratops (blue), orange frill, 3 horns
B1, B2 = "#4FA3E0", "#BFE3FF"
D["triceratops"] = f'''
<path d="M90 250 Q40 260 10 300 Q60 290 100 285 Z" fill="{B1}" {SW}/>
{leg(105, 285, 44, 75, B1)}{leg(215, 285, 44, 75, B1)}
<ellipse cx="180" cy="245" rx="110" ry="70" fill="{B1}" {SW}/>
<ellipse cx="190" cy="275" rx="70" ry="30" fill="{B2}"/>
{leg(140, 290, 44, 75, B1)}{leg(250, 290, 44, 75, B1)}
<circle cx="285" cy="175" r="78" fill="#FF9A2E" {SW}/>
{"".join(f'<circle cx="{285 + 70 * math.cos(a):.0f}" cy="{175 + 70 * math.sin(a):.0f}" r="9" fill="#FFD23F"/>' for a in [i * 0.6 - 2.6 for i in range(8)])}
<ellipse cx="310" cy="225" rx="68" ry="55" fill="{B1}" {SW}/>
<path d="M292 175 L330 92 L314 182 Z M332 182 L380 112 L348 192 Z" fill="#FFF6E0" {SW}/>
<path d="M366 228 L398 214 L370 244 Z" fill="#FFF6E0" {SW}/>
{eye(318, 212, 17)}{cheek(350, 245, 12)}{smile(340, 255, 12)}'''
# ---------------- Stegosaurus (orange body, purple plates)
O1, O2, P1 = "#F2A65A", "#FFE0B8", "#9B5DE5"
plates = "".join(f'<path d="M{x - 26} {y + 16} L{x} {y - 34} L{x + 26} {y + 16} Z" fill="{P1}" {SW}/>' for x, y in
                 ((110, 205), (150, 180), (192, 172), (234, 180), (272, 200)))
D["stegosaurus"] = f'''
{plates}
<path d="M85 245 Q40 230 10 200 Q30 260 90 275 Z" fill="{O1}" {SW}/>
<path d="M20 205 l-14 -24 M30 212 l-8 -28 M14 222 l-22 -10 M22 230 l-20 2" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
{leg(105, 280, 44, 80, O1)}{leg(235, 280, 44, 80, O1)}
<ellipse cx="190" cy="245" rx="115" ry="65" fill="{O1}" {SW}/>
<ellipse cx="195" cy="275" rx="70" ry="25" fill="{O2}"/>
{leg(140, 285, 44, 80, O1)}{leg(270, 285, 44, 80, O1)}
<ellipse cx="330" cy="268" rx="52" ry="34" fill="{O1}" {SW}/>
{eye(338, 258, 14)}{cheek(360, 282, 10)}{smile(355, 290, 10)}'''
# ---------------- Brachiosaurus (purple), long neck up
V1, V2 = "#B57BFF", "#E6D4FF"
D["brachiosaurus"] = f'''
<path d="M90 300 Q40 300 10 340 Q60 335 100 325 Z" fill="{V1}" {SW}/>
{leg(105, 300, 40, 75, V1)}{leg(200, 290, 42, 85, V1)}
<ellipse cx="160" cy="290" rx="95" ry="58" fill="{V1}" {SW}/>
<path d="M200 270 Q250 200 270 90 L315 90 Q300 210 245 300 Z" fill="{V1}" {SW}/>
<path d="M232 270 Q268 200 282 110" stroke="{V2}" stroke-width="16" fill="none" stroke-linecap="round"/>
{leg(135, 305, 40, 75, V1)}{leg(230, 300, 42, 80, V1)}
<ellipse cx="315" cy="70" rx="58" ry="38" fill="{V1}" {SW}/>
{eye(320, 58, 13)}{cheek(345, 80, 9)}{smile(345, 88, 9)}
{spots([(130, 270, 12), (180, 300, 9), (285, 150, 8)], "#8E55E0")}'''
# ---------------- Pteranodon (pink), wings spread (a flying reptile)
K1, K2 = "#FF8FA3", "#FFD3DC"
D["pteranodon"] = f'''
<path d="M200 200 L20 120 Q40 210 120 240 Z" fill="{K1}" {SW}/>
<path d="M200 200 L380 120 Q360 210 280 240 Z" fill="{K1}" {SW}/>
<path d="M40 140 L130 225 M360 140 L270 225" stroke="#E86A84" stroke-width="5"/>
<ellipse cx="200" cy="230" rx="55" ry="45" fill="{K1}" {SW}/>
<ellipse cx="200" cy="245" rx="32" ry="22" fill="{K2}"/>
<path d="M200 190 Q230 130 270 145 L330 160 L262 175 Q240 195 210 200 Z" fill="{K1}" {SW}/>
<path d="M205 160 L150 120 L210 175 Z" fill="#E86A84" {SW}/>
{eye(232, 160, 12)}{cheek(250, 180, 8)}
<path d="M180 272 l-6 22 M220 272 l6 22" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'''
# ---------------- Velociraptor (yellow), slim with feathers
Y1, Y2 = "#F2C14E", "#FFF0BF"
D["velociraptor"] = f'''
<path d="M150 230 Q70 230 10 200 Q60 250 150 260 Z" fill="{Y1}" {SW}/>
<path d="M20 205 l-12 -16 M34 210 l-8 -18 M48 214 l-4 -18" stroke="#E07A12" stroke-width="6" stroke-linecap="round"/>
<path d="M165 260 L150 340 L180 345 M210 260 L215 340 L245 345" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M165 260 L150 340 L180 345 M210 260 L215 340 L245 345" stroke="{Y1}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<ellipse cx="190" cy="235" rx="62" ry="45" fill="{Y1}" {SW}/>
<ellipse cx="200" cy="250" rx="35" ry="20" fill="{Y2}"/>
<path d="M230 215 Q250 150 300 140 Q360 135 365 170 Q362 200 310 200 L250 215 Z" fill="{Y1}" {SW}/>
<path d="M235 240 q25 10 30 30 M245 230 q30 0 40 18" stroke="#E07A12" stroke-width="7" fill="none" stroke-linecap="round"/>
{eye(305, 160, 15)}{cheek(340, 185, 10)}{smile(335, 190, 10)}
<path d="M250 140 l-8 -26 l18 16 l2 -28 l14 28" fill="#E07A12" {SW}/>'''
# ---------------- Ankylosaurus (brown), armour + club tail
N1, N2 = "#B07D4F", "#E8C9A0"
D["ankylosaurus"] = f'''
<path d="M90 260 Q50 255 30 240" stroke="{INK}" stroke-width="30" fill="none" stroke-linecap="round"/>
<path d="M90 260 Q50 255 30 240" stroke="{N1}" stroke-width="18" fill="none" stroke-linecap="round"/>
<circle cx="25" cy="236" r="28" fill="#8A5A34" {SW}/>
{leg(105, 285, 46, 65, N1)}{leg(235, 285, 46, 65, N1)}
<path d="M80 280 Q90 175 200 170 Q310 175 320 280 Z" fill="{N1}" {SW}/>
{"".join(f'<circle cx="{x}" cy="{y}" r="12" fill="#8A5A34" {SW.replace("6", "4")}/>' for x, y in ((120, 230), (160, 205), (200, 198), (240, 205), (280, 230), (140, 260), (200, 240), (260, 260)))}
{leg(140, 290, 46, 65, N1)}{leg(270, 290, 46, 65, N1)}
<ellipse cx="335" cy="262" rx="50" ry="36" fill="{N1}" {SW}/>
{eye(343, 250, 13)}{cheek(365, 275, 9)}{smile(360, 282, 9)}'''
# ---------------- Spinosaurus (teal), big red sail, long snout
T1, T2 = "#3FB8AF", "#C8F0EC"
D["spinosaurus"] = f'''
<path d="M100 220 Q190 40 280 220 Z" fill="#FF6B6B" {SW}/>
{"".join(f'<path d="M{x} 220 L{x + (190 - x) * 0.15:.0f} {220 - 150 * math.sin(math.pi * (x - 100) / 180):.0f}" stroke="#D94545" stroke-width="5"/>' for x in range(125, 275, 25))}
<path d="M110 240 Q50 260 10 310 Q70 295 120 285 Z" fill="{T1}" {SW}/>
{leg(130, 285, 44, 80, "#2E9A92")}
<ellipse cx="185" cy="245" rx="95" ry="62" fill="{T1}" {SW}/>
<ellipse cx="195" cy="268" rx="55" ry="30" fill="{T2}"/>
{leg(185, 290, 46, 80, T1)}
<path d="M250 210 Q280 160 320 165 L390 180 Q395 200 360 205 L270 230 Z" fill="{T1}" {SW}/>
{eye(305, 178, 15)}{cheek(330, 205, 10)}{smile(345, 205, 9)}'''
# ---------------- Parasaurolophus (orange-yellow), tube crest
Q1, Q2 = "#FFB347", "#FFE6C2"
D["parasaurolophus"] = f'''
<path d="M120 240 Q60 260 10 300 Q70 290 130 280 Z" fill="{Q1}" {SW}/>
{leg(130, 285, 44, 80, "#E89A2E")}
<ellipse cx="180" cy="245" rx="85" ry="65" fill="{Q1}" {SW}/>
<ellipse cx="190" cy="270" rx="50" ry="30" fill="{Q2}"/>
{leg(185, 290, 46, 80, Q1)}
<path d="M230 200 Q240 120 290 110 Q340 110 345 150 Q350 180 320 190 L250 210 Z" fill="{Q1}" {SW}/>
<path d="M290 115 Q230 60 160 70" stroke="{INK}" stroke-width="34" fill="none" stroke-linecap="round"/>
<path d="M290 115 Q230 60 160 70" stroke="#FF6B6B" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M330 165 Q360 168 372 180 Q355 192 330 185 Z" fill="{Q2}" {SW}/>
{eye(298, 140, 15)}{cheek(320, 168, 10)}'''
# ---------------- Diplodocus (lime), long neck forward + long tail
L1, L2 = "#8BC34A", "#DDF2B8"
D["diplodocus"] = f'''
<path d="M120 250 Q60 240 5 200 Q50 260 120 275 Z" fill="{L1}" {SW}/>
{leg(125, 270, 40, 85, "#6FA336")}{leg(225, 270, 40, 85, "#6FA336")}
<ellipse cx="190" cy="250" rx="95" ry="55" fill="{L1}" {SW}/>
<ellipse cx="195" cy="272" rx="55" ry="22" fill="{L2}"/>
<path d="M260 230 Q320 170 340 110 L375 120 Q355 200 280 265 Z" fill="{L1}" {SW}/>
{leg(155, 275, 40, 85, L1)}{leg(255, 275, 40, 85, L1)}
<ellipse cx="365" cy="105" rx="34" ry="24" fill="{L1}" {SW}/>
{eye(365, 96, 10)}{cheek(382, 112, 7)}'''
# ---------------- Pachycephalosaurus (red-pink), dome head
R1, R2 = "#E57373", "#FFD0D0"
D["pachycephalosaurus"] = f'''
<path d="M120 240 Q60 260 10 300 Q70 290 130 280 Z" fill="{R1}" {SW}/>
{leg(130, 285, 44, 80, "#C95A5A")}
<ellipse cx="180" cy="245" rx="85" ry="65" fill="{R1}" {SW}/>
<ellipse cx="190" cy="270" rx="50" ry="30" fill="{R2}"/>
{leg(185, 290, 46, 80, R1)}
<path d="M230 205 Q235 160 260 150 L340 150 Q370 170 365 200 Q350 225 300 222 Z" fill="{R1}" {SW}/>
<path d="M245 165 Q250 70 310 70 Q365 75 355 165 Z" fill="#C24A4A" {SW}/>
{"".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#FFF6E0" {SW.replace("6", "3")}/>' for x, y in ((250, 172), (268, 160), (350, 172)))}
{eye(318, 182, 14)}{cheek(345, 205, 9)}{smile(335, 210, 9)}'''
# ---------------- Compsognathus (light green), a tiny dinosaur
C1 = "#9BE07A"
D["compsognathus"] = f'''
<path d="M160 250 Q90 250 30 230 Q80 270 160 275 Z" fill="{C1}" {SW}/>
<path d="M190 270 L180 340 L205 345 M220 270 L230 340 L255 345" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M190 270 L180 340 L205 345 M220 270 L230 340 L255 345" stroke="{C1}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<ellipse cx="205" cy="250" rx="55" ry="38" fill="{C1}" {SW}/>
<path d="M240 230 Q255 175 295 172 Q340 172 342 200 Q340 222 300 222 L255 232 Z" fill="{C1}" {SW}/>
{eye(298, 192, 14)}{cheek(322, 212, 9)}{smile(318, 214, 8)}'''

I = {}
I["egg"] = f'''<ellipse cx="200" cy="215" rx="120" ry="160" fill="#FFF6E0" {SW}/>
{spots([(150, 150, 22), (240, 120, 16), (250, 260, 26), (160, 290, 18), (200, 210, 14)], "#7ED957")}'''
I["egg_bottom"] = f'''<path d="M80 230 L110 205 L140 235 L170 200 L200 238 L230 202 L260 236 L290 206 L320 232 Q330 375 200 375 Q70 375 80 230 Z" fill="#FFF6E0" {SW}/>
{spots([(250, 300, 26), (160, 320, 18)], "#7ED957")}'''
I["egg_top"] = f'''<path d="M80 230 L110 205 L140 235 L170 200 L200 238 L230 202 L260 236 L290 206 L320 232 Q330 55 200 55 Q70 55 80 230 Z" fill="#FFF6E0" {SW}/>
{spots([(150, 150, 22), (240, 120, 16)], "#7ED957")}'''
I["footprint"] = f'''<ellipse cx="200" cy="270" rx="85" ry="95" fill="#8A5A34" {SW}/>
<ellipse cx="110" cy="120" rx="36" ry="62" fill="#8A5A34" {SW} transform="rotate(-25 110 120)"/>
<ellipse cx="200" cy="90" rx="36" ry="68" fill="#8A5A34" {SW}/>
<ellipse cx="290" cy="120" rx="36" ry="62" fill="#8A5A34" {SW} transform="rotate(25 290 120)"/>'''
I["fossil"] = f'''<rect x="20" y="60" width="360" height="290" rx="40" fill="#D9C2A0" {SW}/>
<path d="M90 260 Q200 200 330 210" stroke="#FFF8E7" stroke-width="16" fill="none" stroke-linecap="round"/>
{"".join(f'<path d="M{x} 225 l-8 50 M{x} 225 l8 -40" stroke="#FFF8E7" stroke-width="10" stroke-linecap="round"/>' for x in range(130, 300, 34))}
<path d="M300 205 Q330 140 360 160 Q372 190 345 205 Z" fill="#FFF8E7" {SW.replace("6", "4")}/><circle cx="342" cy="172" r="7" fill="#8A6A4A"/>
<path d="M90 260 Q60 280 40 300" stroke="#FFF8E7" stroke-width="12" fill="none" stroke-linecap="round"/>'''
I["brush"] = f'''<rect x="170" y="40" width="50" height="210" rx="20" fill="#C08A4D" {SW} transform="rotate(25 195 145)"/>
<path d="M120 250 L230 290 L210 370 L90 330 Z" fill="#FFD23F" {SW}/>
<path d="M110 300 L215 335" stroke="#E8A12E" stroke-width="6"/>'''
I["leaves"] = "".join(f'<path d="M200 330 Q{200 + 140 * math.cos(a):.0f} {330 + 140 * math.sin(a) - 120:.0f} {200 + 230 * math.cos(a):.0f} {330 + 230 * math.sin(a):.0f}" '
                      f'stroke="#3E9C2E" stroke-width="40" fill="none" stroke-linecap="round"/>' for a in (-2.6, -2.1, -1.57, -1.05, -0.55)) + \
    f'<rect x="185" y="300" width="30" height="80" fill="#8A5A2B" {SW}/>'
I["meat"] = f'''<path d="M120 300 L80 340 Q55 345 60 320 Q40 300 65 285 L105 250 Z" fill="#FFF8E7" {SW}/>
<ellipse cx="215" cy="190" rx="135" ry="110" fill="#C0503A" {SW} transform="rotate(-30 215 190)"/>
<ellipse cx="225" cy="180" rx="85" ry="62" fill="#E07A5F" transform="rotate(-30 225 180)"/>'''
I["volcano"] = f'''<path d="M20 370 L150 120 L250 120 L380 370 Z" fill="#8A5A34" {SW}/>
<path d="M150 120 Q200 160 250 120 L240 150 Q200 175 160 150 Z" fill="#FF6B3D"/>
<path d="M170 125 Q180 200 160 260 M230 125 Q220 190 245 250" stroke="#FF6B3D" stroke-width="16" stroke-linecap="round" fill="none"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E0E0E8" {SW.replace("6", "4")}/>' for x, y, r in ((200, 90, 34), (240, 55, 30), (175, 40, 26)))}'''
I["building"] = f'''<rect x="120" y="40" width="160" height="340" fill="#7EC8FF" {SW}/>''' + "".join(
    f'<rect x="{x}" y="{y}" width="40" height="44" fill="#FFFFFF" {SW.replace("6", "4")}/>' for x in (145, 215) for y in (70, 150, 230, 310))

HATS = {
    "gul": '''<path d="M300 330 Q300 150 600 140 Q900 150 900 330 Z" fill="#E8D2A0" stroke="#3A2420" stroke-width="14"/>
      <ellipse cx="600" cy="335" rx="420" ry="70" fill="#D9BE84" stroke="#3A2420" stroke-width="14"/>
      <path d="M305 300 Q600 345 895 300 L898 330 Q600 375 302 330 Z" fill="#6CC24A"/>''',
    "misheal": '''<path d="M300 400 Q300 220 600 210 Q900 220 900 400 Z" fill="#E8D2A0" stroke="#3A2420" stroke-width="14"/>
      <ellipse cx="600" cy="405" rx="430" ry="72" fill="#D9BE84" stroke="#3A2420" stroke-width="14"/>
      <path d="M305 370 Q600 415 895 370 L898 400 Q600 445 302 400 Z" fill="#FF8FA3"/>''',
}


def bg_valley():
    rnd = __import__("random").Random(4)
    ferns = "".join(
        f'<g transform="translate({x} {y}) scale({s})">' + "".join(
            f'<path d="M0 0 Q{70 * math.cos(a):.0f} {70 * math.sin(a) - 50:.0f} {120 * math.cos(a):.0f} {120 * math.sin(a):.0f}" stroke="#3E9C2E" stroke-width="18" fill="none" stroke-linecap="round"/>'
            for a in (-2.7, -2.2, -1.57, -0.95, -0.45)) + '</g>' for x, y, s in ((90, 900, 1.2), (360, 960, 0.9), (1580, 930, 1.1), (1820, 900, 1.3), (1100, 980, 0.8)))
    palms = "".join(
        f'<rect x="{x - 14}" y="{y}" width="28" height="{h}" fill="#8A5A2B" stroke="{INK}" stroke-width="6"/>' + "".join(
            f'<path d="M{x} {y} Q{x + 90 * math.cos(a):.0f} {y + 90 * math.sin(a) - 40:.0f} {x + 160 * math.cos(a):.0f} {y + 160 * math.sin(a):.0f}" stroke="#4CAF50" stroke-width="26" fill="none" stroke-linecap="round"/>'
            for a in (-2.9, -2.3, -1.6, -0.9, -0.3)) for x, y, h in ((260, 480, 380), (1680, 450, 420)))
    return f'''<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7EC8FF"/><stop offset="1" stop-color="#FFE3B0"/></linearGradient></defs>
      <rect width="1920" height="1080" fill="url(#s)"/>
      <circle cx="1650" cy="160" r="85" fill="#FFE066"/>
      <path d="M820 640 L960 330 L1080 330 L1240 640 Z" fill="#9C6B45" {SW}/>
      <path d="M960 330 Q1020 370 1080 330 L1070 360 Q1020 385 970 360 Z" fill="#FF6B3D"/>
      {"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F0F0F6"/>' for x, y, r in ((1020, 290, 40), (1060, 245, 34), (1000, 230, 28), (1040, 195, 24)))}
      <path d="M0 620 Q300 540 640 600 Q980 660 1300 580 Q1620 520 1920 600 L1920 1080 L0 1080 Z" fill="#8DD16A"/>
      <path d="M0 760 Q480 700 960 750 Q1440 800 1920 740 L1920 1080 L0 1080 Z" fill="#7CC456"/>
      {palms}{ferns}
      <ellipse cx="1300" cy="1000" rx="160" ry="34" fill="#6BB34A"/>'''


def bg_dig():
    return f'''<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#FFEBC2"/></linearGradient></defs>
      <rect width="1920" height="1080" fill="url(#s)"/>
      <path d="M0 560 Q500 500 960 540 Q1400 580 1920 520 L1920 1080 L0 1080 Z" fill="#E8C98A"/>
      <path d="M0 700 Q960 650 1920 700 L1920 1080 L0 1080 Z" fill="#DDB872"/>
      {"".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.6:.0f}" fill="#B8955A" {SW}/>' for x, y, r in ((200, 640, 50), (1700, 620, 60), (1500, 960, 40), (380, 980, 36)))}
      {"".join(f'<rect x="{x}" y="560" width="16" height="140" fill="#8A5A2B" {SW.replace("6", "4")}/>' for x in (80, 1820))}
      <path d="M88 580 Q960 640 1828 580" stroke="#C0392B" stroke-width="8" fill="none"/>
      <rect x="1500" y="420" width="260" height="170" rx="12" fill="#FFFFFF" {SW}/><text x="1530" y="520" font-size="60" font-family="Arial Black" fill="#8A5A34">DIG!</text>
      <rect x="1615" y="590" width="20" height="110" fill="#8A5A2B"/>'''


def shot_items(items, prefix):
    names = list(items)
    for start in range(0, len(names), 12):
        chunk = names[start:start + 12]
        cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{items[n]}</svg></div>'
                        for i, n in enumerate(chunk))
        w = 400 * len(chunk)
        A.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>', str(OUT / "_items.png"), w, 400, scale=2)
        im = Image.open(OUT / "_items.png")
        for i, n in enumerate(chunk):
            im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"{prefix}{n}.png")
        (OUT / "_items.png").unlink()


def render():
    shot_items(D, "dino_")
    shot_items(I, "item_")
    for n, svg in HATS.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1200" height="2000">{svg}</svg></body></html>',
               str(OUT / f"hat_{n}.png"), 1200, 2000)
    for n, fn in (("valley", bg_valley), ("dig", bg_dig)):
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{fn()}</svg></body></html>',
               str(OUT / f"bg_{n}.png"), 1920, 1080)
    names = [f"dino_{n}" for n in D] + [f"item_{n}" for n in I]
    cols = 8
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 200, rows * 200 + 300), (225, 230, 240, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"{n}.png").resize((190, 190)), ((i % cols) * 200, (i // cols) * 200))
    for j, n in enumerate(("valley", "dig")):
        sheet.alpha_composite(Image.open(OUT / f"bg_{n}.png").convert("RGBA").resize((520, 292)), (j * 530, rows * 200 + 4))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(D), "dinos +", len(I), "items + 2 bgs + hats")


if __name__ == "__main__":
    render()
