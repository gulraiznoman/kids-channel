"""Props + backgrounds for Long video 9 "Who's in the Egg?".
python art.py -> art/item_<key>.png (800x800), art/bg_<name>.png (1920x1080), _sheet.png
Eggs themselves are drawn in render.py (so they can crack).
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


def eyes(x1, x2, y, r=15):
    return (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{x1 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/>')


def cheeks(x1, x2, y, c="#FF8FA3"):
    return f'<ellipse cx="{x1}" cy="{y}" rx="16" ry="10" fill="{c}" opacity="0.7"/><ellipse cx="{x2}" cy="{y}" rx="16" ry="10" fill="{c}" opacity="0.7"/>'


def smile(cx, cy, w=22):
    return f'<path d="M{cx - w} {cy} Q{cx} {cy + w} {cx + w} {cy}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'


I = {}
I["turtle"] = f'''<ellipse cx="90" cy="300" rx="34" ry="18" fill="#7ED957" {SW} transform="rotate(-25 90 300)"/><ellipse cx="300" cy="305" rx="34" ry="18" fill="#7ED957" {SW} transform="rotate(25 300 305)"/>
<ellipse cx="120" cy="250" rx="40" ry="20" fill="#7ED957" {SW} transform="rotate(-40 120 250)"/><ellipse cx="275" cy="250" rx="40" ry="20" fill="#7ED957" {SW} transform="rotate(40 275 250)"/>
<path d="M95 280 Q100 150 200 145 Q300 150 305 280 Z" fill="#3E9B5B" {SW}/>
<path d="M150 190 L200 165 L250 190 L240 250 L160 250 Z M120 260 L160 250 M280 260 L240 250 M200 165 L200 150" stroke="#2C7A44" stroke-width="7" fill="#57B86F"/>
<rect x="95" y="270" width="210" height="25" rx="12" fill="#C9E7A8" {SW}/>
<circle cx="200" cy="105" r="62" fill="#7ED957" {SW}/>{eyes(178, 222, 98, 13)}{cheeks(160, 240, 120)}{smile(200, 125, 16)}'''
I["crocodile"] = f'''<path d="M60 260 Q30 250 25 225 Q60 230 90 235" fill="#4CAF50" {SW}/>
<ellipse cx="170" cy="260" rx="110" ry="55" fill="#4CAF50" {SW}/>
{"".join(f'<path d="M{x} 210 l12 -20 l12 20" fill="#3B8F3F" stroke="{INK}" stroke-width="5"/>' for x in (110, 145, 180, 215))}
<ellipse cx="110" cy="310" rx="22" ry="16" fill="#4CAF50" {SW}/><ellipse cx="220" cy="312" rx="22" ry="16" fill="#4CAF50" {SW}/>
<path d="M250 200 Q300 170 370 205 Q385 225 360 240 L260 255 Z" fill="#5CC060" {SW}/>
<path d="M265 240 Q320 262 365 238" stroke="{INK}" stroke-width="6" fill="none"/><path d="M285 245 l6 10 l6 -9 M310 249 l6 10 l6 -9 M335 247 l6 10 l6 -9" stroke="{INK}" stroke-width="3" fill="#FFF"/>
<circle cx="275" cy="180" r="30" fill="#5CC060" {SW}/><circle cx="318" cy="178" r="28" fill="#5CC060" {SW}/>
<circle cx="276" cy="178" r="17" fill="#FFF"/><circle cx="318" cy="176" r="16" fill="#FFF"/>{eyes(279, 321, 180, 9)}
<ellipse cx="355" cy="212" rx="5" ry="3" fill="{INK}"/>{cheeks(300, 300, 228)}'''
I["penguin"] = f'''<ellipse cx="200" cy="245" rx="105" ry="125" fill="#8E9AAF" {SW}/>
<ellipse cx="200" cy="270" rx="70" ry="95" fill="#F2F4F8" {SW}/>
<circle cx="200" cy="140" r="78" fill="#4A5160" {SW}/><path d="M145 150 Q200 100 255 150 Q255 200 200 205 Q145 200 145 150 Z" fill="#FFFFFF"/>
{eyes(178, 222, 150, 13)}<path d="M188 172 L212 172 L200 188 Z" fill="#FFB020" stroke="{INK}" stroke-width="4"/>{cheeks(160, 240, 175)}
<path d="M98 220 Q60 270 85 310 Q110 280 112 240 Z M302 220 Q340 270 315 310 Q290 280 288 240 Z" fill="#6F7B90" {SW}/>
<ellipse cx="165" cy="370" rx="32" ry="14" fill="#FFB020" {SW}/><ellipse cx="235" cy="370" rx="32" ry="14" fill="#FFB020" {SW}/>
<path d="M150 70 Q160 50 175 68 Q185 45 200 66" stroke="#4A5160" stroke-width="10" fill="none" stroke-linecap="round"/>'''
I["snake"] = f'''<path d="M70 330 Q60 270 130 270 Q210 270 210 320 Q210 370 280 365 Q340 360 330 300" stroke="{INK}" stroke-width="64" fill="none" stroke-linecap="round"/>
<path d="M70 330 Q60 270 130 270 Q210 270 210 320 Q210 370 280 365 Q340 360 330 300" stroke="#9BD45A" stroke-width="50" fill="none" stroke-linecap="round"/>
<path d="M95 290 l20 10 M150 272 l10 20 M200 300 l-20 8 M220 350 l18 -10 M280 352 l-4 -18" stroke="#FFD23F" stroke-width="12" stroke-linecap="round"/>
<path d="M330 300 Q330 200 260 170" stroke="{INK}" stroke-width="60" fill="none" stroke-linecap="round"/><path d="M330 300 Q330 200 260 170" stroke="#9BD45A" stroke-width="46" fill="none" stroke-linecap="round"/>
<ellipse cx="240" cy="150" rx="78" ry="62" fill="#9BD45A" {SW}/>{eyes(220, 265, 135, 13)}{cheeks(205, 285, 165)}
<path d="M218 172 Q240 186 262 172" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M240 186 L240 210 M240 210 l-10 12 M240 210 l10 12" stroke="#FF4D6D" stroke-width="5" stroke-linecap="round" fill="none"/>'''
I["ostrich"] = f'''<path d="M170 300 L160 375 M230 300 L240 375" stroke="#E8A86A" stroke-width="16" stroke-linecap="round"/>
<path d="M140 380 l20 -6 l20 6 M220 380 l20 -6 l20 6" stroke="#E8A86A" stroke-width="10" stroke-linecap="round" fill="none"/>
<ellipse cx="200" cy="260" rx="100" ry="70" fill="#C9A47A" {SW}/>
{"".join(f'<path d="M{x} {y} q12 -14 24 0" stroke="#A9825A" stroke-width="7" fill="none"/>' for x, y in ((140, 250), (180, 230), (220, 250), (160, 285), (210, 290)))}
<path d="M215 205 Q200 150 225 110" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M215 205 Q200 150 225 110" stroke="#E8C9A0" stroke-width="28" fill="none" stroke-linecap="round"/>
<circle cx="235" cy="90" r="52" fill="#E8C9A0" {SW}/>{eyes(222, 258, 82, 12)}
<path d="M262 100 Q300 102 300 112 Q290 122 258 116 Z" fill="#F2A65A" stroke="{INK}" stroke-width="5"/>
<path d="M200 45 l8 -22 l10 20 l10 -22 l6 26" stroke="#A9825A" stroke-width="8" fill="none" stroke-linecap="round"/>{cheeks(225, 225, 112)}'''
I["owl"] = f'''<ellipse cx="200" cy="230" rx="120" ry="135" fill="#B79BEA" {SW}/>
<ellipse cx="200" cy="270" rx="75" ry="85" fill="#E9DDFB" {SW}/>
{"".join(f'<path d="M{x} {y} q12 12 24 0" stroke="#B79BEA" stroke-width="6" fill="none"/>' for x, y in ((165, 240), (200, 240), (182, 275), (165, 310), (200, 310)))}
<path d="M95 115 L120 160 L145 130 Z M305 115 L280 160 L255 130 Z" fill="#9B7BD6" {SW}/>
<circle cx="155" cy="175" r="48" fill="#FFFFFF" {SW}/><circle cx="245" cy="175" r="48" fill="#FFFFFF" {SW}/>{eyes(155, 245, 178, 22)}
<path d="M188 200 L212 200 L200 225 Z" fill="#FFB020" stroke="{INK}" stroke-width="5"/>
<path d="M85 220 Q60 290 105 330 Q120 270 110 225 Z M315 220 Q340 290 295 330 Q280 270 290 225 Z" fill="#9B7BD6" {SW}/>
<path d="M165 362 l-10 18 M180 362 l0 20 M220 362 l0 20 M235 362 l10 18" stroke="#FFB020" stroke-width="9" stroke-linecap="round"/>'''
I["robin"] = f'''<path d="M60 320 Q200 410 340 320 Q330 280 200 275 Q70 280 60 320 Z" fill="#B07A4E" {SW}/>
{"".join(f'<path d="M{x} {y} q30 -14 60 4" stroke="#8A5A33" stroke-width="6" fill="none"/>' for x, y in ((80, 315), (150, 335), (220, 335), (280, 318)))}
<ellipse cx="200" cy="240" rx="95" ry="75" fill="#8C6A52" {SW}/><ellipse cx="200" cy="262" rx="62" ry="50" fill="#FF8A3D" {SW}/>
<circle cx="200" cy="160" r="66" fill="#8C6A52" {SW}/>{eyes(178, 222, 152, 13)}{cheeks(158, 242, 178)}
<path d="M170 185 L230 185 L200 238 Z" fill="#FFD23F" stroke="{INK}" stroke-width="5"/><path d="M174 190 L226 190" stroke="#FF8A3D" stroke-width="8"/>
<path d="M175 98 l10 -24 l12 22 l10 -22 l6 24" stroke="#8C6A52" stroke-width="9" fill="none" stroke-linecap="round"/>
<path d="M108 230 Q80 250 95 280 Q120 265 120 240 Z M292 230 Q320 250 305 280 Q280 265 280 240 Z" fill="#6F5240" {SW}/>'''
I["hen"] = f'''<path d="M300 170 Q370 130 360 230 Q340 200 310 215 Z" fill="#E8573C" {SW}/>
<ellipse cx="210" cy="250" rx="130" ry="100" fill="#FFFFFF" {SW}/>
<path d="M150 240 Q200 290 260 245" stroke="#E2E2EA" stroke-width="12" fill="none"/>
<path d="M175 340 L165 380 M235 340 L245 380 M150 384 l15 -6 l15 6 M230 384 l15 -6 l15 6" stroke="#FFB020" stroke-width="10" stroke-linecap="round" fill="none"/>
<circle cx="120" cy="150" r="62" fill="#FFFFFF" {SW}/>
<path d="M85 95 Q90 60 110 85 Q120 55 135 85 Q150 60 152 98 Z" fill="#E8352E" {SW}/>
{eyes(105, 140, 145, 11)}<path d="M60 150 L90 140 L90 165 Z" fill="#FFB020" stroke="{INK}" stroke-width="5"/>
<path d="M85 170 Q75 200 92 205 Q100 190 98 172 Z" fill="#E8352E" stroke="{INK}" stroke-width="4"/>{cheeks(150, 150, 170)}'''
I["caterpillar"] = "".join(f'<circle cx="{70 + i * 55}" cy="{250 + 15 * (i % 2)}" r="42" fill="{c}" {SW}/>' for i, c in enumerate(("#7ED957", "#5CC060", "#7ED957", "#5CC060", "#7ED957"))) + \
    f'''<circle cx="330" cy="200" r="58" fill="#9BE36B" {SW}/>{eyes(312, 350, 192, 11)}{cheeks(300, 362, 215)}{smile(331, 215, 14)}
<path d="M310 145 Q300 110 285 105 M350 145 Q360 110 375 105" stroke="{INK}" stroke-width="6" fill="none"/><circle cx="285" cy="105" r="9" fill="#FF6B8B"/><circle cx="375" cy="105" r="9" fill="#FF6B8B"/>
{"".join(f'<path d="M{70 + i * 55} {290 + 15 * (i % 2)} l-4 22 M{80 + i * 55} {290 + 15 * (i % 2)} l4 22" stroke="{INK}" stroke-width="5"/>' for i in range(5))}'''
I["cocoon"] = f'''<path d="M200 40 L200 85" stroke="#6B4A2A" stroke-width="10"/><rect x="40" y="25" width="320" height="30" rx="15" fill="#8A5A2B" {SW}/>
<path d="M200 80 Q290 120 280 230 Q270 340 200 370 Q130 340 120 230 Q110 120 200 80 Z" fill="#C9B26A" {SW}/>
<path d="M140 150 Q200 170 262 150 M128 210 Q200 235 272 210 M130 270 Q200 295 268 270 M150 325 Q200 345 250 325" stroke="#A8924D" stroke-width="7" fill="none"/>'''
I["butterfly"] = f'''<path d="M200 200 Q120 40 50 110 Q20 190 195 215 Z" fill="#FF8FB1" {SW}/><path d="M200 200 Q280 40 350 110 Q380 190 205 215 Z" fill="#FF8FB1" {SW}/>
<path d="M195 215 Q60 230 80 320 Q140 350 198 235 Z" fill="#B79BEA" {SW}/><path d="M205 215 Q340 230 320 320 Q260 350 202 235 Z" fill="#B79BEA" {SW}/>
<circle cx="110" cy="130" r="22" fill="#FFD23F"/><circle cx="290" cy="130" r="22" fill="#FFD23F"/><circle cx="125" cy="280" r="16" fill="#FFFFFF"/><circle cx="275" cy="280" r="16" fill="#FFFFFF"/>
<ellipse cx="200" cy="225" rx="22" ry="80" fill="#5A3A6E" {SW}/><circle cx="200" cy="140" r="30" fill="#5A3A6E" {SW}/>
{eyes(190, 212, 138, 7)}<path d="M190 112 Q175 75 160 70 M210 112 Q225 75 240 70" stroke="{INK}" stroke-width="5" fill="none"/>'''
I["leafeggs"] = f'''<path d="M40 300 Q120 80 360 90 Q340 300 40 300 Z" fill="#5DBB46" {SW}/><path d="M60 290 Q200 190 340 100" stroke="#3E8E2E" stroke-width="7" fill="none"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#FFF6C9" stroke="{INK}" stroke-width="4"/>' for x, y in ((170, 200), (205, 185), (190, 225), (225, 215), (240, 175)))}'''
I["nest"] = f'''<path d="M30 230 Q200 400 370 230 Q350 190 200 185 Q50 190 30 230 Z" fill="#B07A4E" {SW}/>
{"".join(f'<path d="M{x} {y} q40 -18 80 4" stroke="#8A5A33" stroke-width="7" fill="none"/>' for x, y in ((50, 240), (130, 270), (210, 272), (280, 245), (90, 300), (200, 310)))}
<path d="M40 225 Q200 270 360 225" stroke="{INK}" stroke-width="6" fill="none"/>'''
I["hay"] = f'''<path d="M10 260 Q200 380 390 260 Q370 190 200 190 Q30 190 10 260 Z" fill="#F2C94C" {SW}/>
{"".join(f'<path d="M{x} {y} l{dx} -26" stroke="#D9A82E" stroke-width="7" stroke-linecap="round"/>' for x, y, dx in ((40, 250, 20), (90, 230, -15), (150, 220, 18), (220, 222, -20), (290, 230, 16), (350, 248, -18), (120, 290, 10), (260, 295, -12)))}
<path d="M30 252 Q200 300 370 252" stroke="{INK}" stroke-width="6" fill="none"/>'''


I["tadpole"] = f'''<path d="M230 200 Q320 150 370 220 Q320 210 300 250 Q330 280 380 270 Q320 320 230 230 Z" fill="#6B8F4E" {SW}/>
<ellipse cx="170" cy="215" rx="95" ry="80" fill="#7FA35E" {SW}/>{eyes(150, 195, 195, 12)}{cheeks(130, 210, 235)}{smile(172, 240, 16)}'''
I["frogspawn"] = "".join(f'<circle cx="{x}" cy="{y}" r="44" fill="#D9F2FF" fill-opacity="0.85" stroke="#7FB8D9" stroke-width="5"/><circle cx="{x}" cy="{y}" r="13" fill="#2B2B33"/>'
                         for x, y in ((140, 160), (220, 150), (300, 175), (110, 240), (190, 235), (270, 250), (340, 255), (160, 315), (240, 320), (310, 330)))
I["platypus"] = f'''<path d="M70 250 Q40 220 60 190 Q90 200 110 225 Z" fill="#8A5A33" {SW}/>
<ellipse cx="200" cy="245" rx="120" ry="70" fill="#A0703F" {SW}/>
<ellipse cx="140" cy="305" rx="30" ry="14" fill="#8A5A33" {SW}/><ellipse cx="250" cy="308" rx="30" ry="14" fill="#8A5A33" {SW}/>
<circle cx="290" cy="200" r="58" fill="#A0703F" {SW}/>{eyes(278, 312, 185, 10)}
<path d="M320 205 Q400 190 395 230 Q385 255 320 240 Z" fill="#3A3A44" {SW}/>{cheeks(285, 285, 225)}'''
I["kiwi"] = f'''<path d="M170 300 L160 370 M230 300 L240 370 M140 374 l20 -6 l20 6 M220 374 l20 -6 l20 6" stroke="#E8A86A" stroke-width="10" stroke-linecap="round" fill="none"/>
<ellipse cx="200" cy="230" rx="130" ry="100" fill="#8C6A52" {SW}/>
{"".join(f'<path d="M{x} {y} q10 12 20 0" stroke="#6F5240" stroke-width="6" fill="none"/>' for x, y in ((130, 220), (170, 200), (210, 230), (150, 260), (200, 270), (240, 205)))}
<circle cx="300" cy="170" r="52" fill="#8C6A52" {SW}/>{eyes(290, 320, 160, 10)}
<path d="M335 180 Q400 230 395 280" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M335 180 Q400 230 395 280" stroke="#F2D18B" stroke-width="9" fill="none" stroke-linecap="round"/>'''


def sky(c1="#8FD8FF", c2="#E2F6FF"):
    return (f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<rect width="1920" height="1080" fill="url(#sk)"/>')


def clouds(pts):
    return '<g fill="#FFFFFF" opacity="0.95">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="100" ry="42"/><ellipse cx="{x + 60}" cy="{y - 24}" rx="62" ry="40"/>' for x, y in pts) + '</g>'


BG = {}
BG["barn"] = f'''<rect width="1920" height="1080" fill="#F7D9A8"/>
  {"".join(f'<rect x="{x}" y="0" width="150" height="800" fill="{c}" stroke="#B5674A" stroke-width="6"/>' for x, c in zip(range(0, 1920, 160), ["#D9714F", "#CF6847"] * 7))}
  <path d="M760 120 L960 30 L1160 120 L1160 520 L760 520 Z" fill="#8A3F2B" {SW}/><path d="M760 120 L1160 520 M1160 120 L760 520" stroke="#F7D9A8" stroke-width="18"/>
  <rect x="760" y="120" width="400" height="400" fill="none" stroke="#F7D9A8" stroke-width="18"/>
  <rect x="0" y="790" width="1920" height="290" fill="#E8B964"/>
  {"".join(f'<path d="M{x} {y} l{d} -30" stroke="#C9953F" stroke-width="7" stroke-linecap="round"/>' for x, y, d in [(i * 97 % 1920, 830 + (i * 53) % 220, (-1) ** i * 18) for i in range(60)])}
  <rect x="0" y="780" width="1920" height="16" fill="#A86A3A"/>
  <rect x="80" y="560" width="300" height="230" rx="16" fill="#F2C94C" {SW}/><rect x="1560" y="580" width="280" height="210" rx="16" fill="#F2C94C" {SW}/>
  {"".join(f'<path d="M{x} {y} l12 -22" stroke="#D9A82E" stroke-width="6"/>' for x, y in ((120, 600), (200, 640), (300, 610), (1600, 620), (1700, 660), (1780, 615)))}'''
BG["pond"] = sky() + clouds(((300, 160), (1500, 130))) + f'''
  <path d="M0 620 Q480 560 960 600 Q1440 640 1920 580 L1920 1080 L0 1080 Z" fill="#7ED957" {SW}/>
  <ellipse cx="960" cy="900" rx="820" ry="150" fill="#5EC8F2" {SW}/><ellipse cx="760" cy="880" rx="300" ry="40" fill="#A7E4FA" opacity="0.6"/>
  {"".join(f'<ellipse cx="{x}" cy="{y}" rx="70" ry="24" fill="#4CAF50" {SW}/>' for x, y in ((420, 920), (1480, 880), (1150, 980)))}
  {"".join(f'<path d="M{x} 760 Q{x + 8} 620 {x - 6} 540" stroke="#3E8E2E" stroke-width="12" fill="none"/><ellipse cx="{x - 6}" cy="560" rx="14" ry="40" fill="#8A5A2B" {SW}/>' for x in (180, 240, 1700, 1760, 1820))}'''
BG["beach"] = sky("#7FD3FF", "#D6F1FF") + clouds(((400, 150), (1450, 120))) + f'''
  <circle cx="1650" cy="200" r="85" fill="#FFD23F" {SW}/>
  <path d="M0 520 L1920 520 L1920 700 L0 700 Z" fill="#3FA9E8"/><path d="M0 560 Q240 540 480 560 T960 560 T1440 560 T1920 560" stroke="#A7E4FA" stroke-width="10" fill="none"/>
  <path d="M0 680 Q480 640 960 680 Q1440 720 1920 670 L1920 1080 L0 1080 Z" fill="#F7DFA0" {SW}/>
  {"".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#E2C47E"/>' for x, y in [((i * 211) % 1920, 760 + (i * 89) % 300) for i in range(40)])}
  <path d="M250 900 l18 -30 l18 30 Z" fill="#FF9F80" stroke="{INK}" stroke-width="4"/><path d="M1600 950 q20 -30 40 0 q-20 15 -40 0 Z" fill="#FFB3C7" stroke="{INK}" stroke-width="4"/>'''
BG["river"] = sky() + clouds(((260, 140), (1300, 110))) + f'''
  <path d="M0 560 Q500 480 1000 560 Q1500 640 1920 540 L1920 1080 L0 1080 Z" fill="#8BC86A" {SW}/>
  <path d="M0 640 Q600 600 1100 680 Q1500 740 1920 660 L1920 820 Q1400 880 900 800 Q400 740 0 790 Z" fill="#4CA3D9" {SW}/>
  <path d="M200 700 q60 -12 120 0 M900 730 q60 -12 120 0 M1500 750 q60 -12 120 0" stroke="#A7E4FA" stroke-width="8" fill="none"/>
  <path d="M0 800 Q500 760 960 830 Q1400 900 1920 820 L1920 1080 L0 1080 Z" fill="#C9A26A" {SW}/>
  {"".join(f'<path d="M{x} 560 Q{x + 30} 420 {x + 80} 380 M{x + 10} 560 Q{x - 40} 430 {x - 90} 400" stroke="#3E8E2E" stroke-width="14" fill="none"/>' for x in (180, 1720))}'''
BG["ice"] = sky("#BFE6FF", "#F2FBFF") + f'''
  <path d="M0 520 L300 300 L520 520 Z M380 520 L700 240 L1000 520 Z M1300 520 L1600 280 L1920 520 Z" fill="#E8F6FF" {SW}/>
  <path d="M300 300 L360 360 L330 380 L270 340 Z M700 240 L770 310 L730 330 L660 300 Z M1600 280 L1660 340 L1620 360 L1560 330 Z" fill="#FFFFFF"/>
  <rect x="0" y="520" width="1920" height="560" fill="#F4FBFF"/><path d="M0 520 L1920 520" stroke="{INK}" stroke-width="6"/>
  {"".join(f'<path d="M{x} {y} l60 10" stroke="#C9E6F7" stroke-width="6" stroke-linecap="round"/>' for x, y in [((i * 263) % 1900, 600 + (i * 71) % 400) for i in range(22)])}
  {"".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#FFFFFF" stroke="#C9E6F7" stroke-width="2"/>' for x, y in [((i * 331) % 1920, (i * 97) % 480) for i in range(30)])}'''
BG["jungle"] = f'''<rect width="1920" height="1080" fill="#BDE8B0"/>
  {"".join(f'<rect x="{x}" y="0" width="70" height="800" fill="#8A5A2B" {SW}/>' for x in (120, 520, 1350, 1760))}
  {"".join(f'<ellipse cx="{x}" cy="{y}" rx="190" ry="110" fill="{c}" {SW}/>' for x, y, c in ((150, 80, "#3E9B4B"), (520, 40, "#4CAF50"), (900, 90, "#3E9B4B"), (1350, 40, "#4CAF50"), (1760, 90, "#3E9B4B")))}
  {"".join(f'<path d="M{x} 0 Q{x + 30} 200 {x} 380" stroke="#3E8E2E" stroke-width="10" fill="none"/><ellipse cx="{x + 14}" cy="{200}" rx="22" ry="12" fill="#5DBB46"/>' for x in (330, 760, 1120, 1580))}
  <rect x="0" y="780" width="1920" height="300" fill="#7A5A3A"/>
  {"".join(f'<path d="M{x} 800 Q{x - 80} 700 {x - 160} 720 Q{x - 80} 760 {x} 800 Q{x + 80} 700 {x + 160} 720 Q{x + 80} 760 {x} 800 Z" fill="#5DBB46" {SW}/>' for x in (160, 600, 1300, 1760))}'''
BG["savanna"] = sky("#FFD58F", "#FFF1D6") + f'''
  <circle cx="1500" cy="300" r="120" fill="#FFB347" opacity="0.9"/>
  <path d="M0 640 Q500 590 1000 640 Q1500 690 1920 620 L1920 1080 L0 1080 Z" fill="#E8C66A" {SW}/>
  <rect x="300" y="420" width="34" height="230" fill="#8A5A2B" {SW}/><ellipse cx="317" cy="410" rx="230" ry="55" fill="#7BAE3F" {SW}/>
  <rect x="1560" y="460" width="26" height="190" fill="#8A5A2B" {SW}/><ellipse cx="1573" cy="452" rx="170" ry="40" fill="#7BAE3F" {SW}/>
  {"".join(f'<path d="M{x} {y} l-8 -34 M{x} {y} l0 -40 M{x} {y} l8 -34" stroke="#C9A24A" stroke-width="6" stroke-linecap="round"/>' for x, y in [((i * 157) % 1920, 720 + (i * 61) % 330) for i in range(36)])}'''
BG["tree"] = sky() + clouds(((1500, 140),)) + f'''
  <path d="M0 860 L1920 860 L1920 1080 L0 1080 Z" fill="#7ED957"/>
  <path d="M120 1080 L200 0 L720 0 L800 1080 Z" fill="#9A6A3F" {SW}/>
  {"".join(f'<path d="M{260 + k * 60} {80 + k * 140} q60 30 120 0" stroke="#7A5230" stroke-width="10" fill="none"/>' for k in range(6))}
  <ellipse cx="460" cy="470" rx="150" ry="190" fill="#5A3A22" {SW}/><ellipse cx="460" cy="600" rx="130" ry="40" fill="#7A5230"/>
  {"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" {SW}/>' for x, y, r, c in ((1100, 120, 180, "#4CAF50"), (1400, 60, 160, "#5DBB46"), (1750, 160, 200, "#4CAF50"), (900, 0, 160, "#5DBB46")))}'''


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
    sheet = Image.new("RGBA", (180 * 8, 180 * 2 + 230 * 2), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((170, 170)), ((i % 8) * 180, (i // 8) * 180))
    for j, k in enumerate(BG):
        sheet.alpha_composite(Image.open(OUT / f"bg_{k}.png").convert("RGBA").resize((356, 200)), ((j % 4) * 360, 370 + (j // 4) * 210))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items +", len(BG), "bgs")


if __name__ == "__main__":
    render()
