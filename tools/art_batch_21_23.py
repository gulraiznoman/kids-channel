"""Art for L21 Christmas Presents, L22 Write Letters, L23 Bugs & Insects.
python tools/art_batch_21_23.py -> long21-presents/art, long22-writing/art, long23-bugs/art (+ tools/_sheet_21_23.png)
"""
import math, pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK


def eyes(x1, x2, y, r=11):
    return (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{x1 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/>')


def smile(cx, cy, w=16):
    return f'<path d="M{cx - w} {cy} Q{cx} {cy + w} {cx + w} {cy}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'


def legs(pts):
    return "".join(f'<path d="{p}" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for p in pts)


SETS = {}
# ------------------------------------------------------------------ L21 presents
P = {}
P["basketball"] = f'''<circle cx="200" cy="200" r="150" fill="#FF8C1A" {SW}/><path d="M50 200 H350 M200 50 V350" stroke="{INK}" stroke-width="7" fill="none"/>
<path d="M95 95 Q170 200 95 305 M305 95 Q230 200 305 305" stroke="{INK}" stroke-width="7" fill="none"/>'''
P["rocket"] = f'''<path d="M200 30 Q290 120 280 270 L120 270 Q110 120 200 30 Z" fill="#9B5DE5" {SW}/><circle cx="200" cy="160" r="46" fill="#9ED8FF" {SW}/>
<path d="M120 200 L60 310 L125 270 Z M280 200 L340 310 L275 270 Z" fill="#FFD23F" {SW}/><path d="M150 270 L200 370 L250 270 Z" fill="#FF8C1A" {SW}/>'''
P["robot"] = f'''<rect x="120" y="170" width="160" height="150" rx="20" fill="#B8BFCC" {SW}/><rect x="130" y="60" width="140" height="100" rx="20" fill="#CBD2DE" {SW}/>
<path d="M200 60 V25" stroke="{INK}" stroke-width="8"/><circle cx="200" cy="22" r="13" fill="#FF4D6D" {SW}/>{eyes(170, 230, 105, 12)}{smile(200, 128, 18)}
<rect x="165" y="205" width="70" height="50" rx="8" fill="#4CC9F0" {SW}/><rect x="72" y="185" width="42" height="100" rx="18" fill="#B8BFCC" {SW}/><rect x="286" y="185" width="42" height="100" rx="18" fill="#B8BFCC" {SW}/>
<rect x="140" y="320" width="48" height="55" rx="10" fill="#8C94A6" {SW}/><rect x="212" y="320" width="48" height="55" rx="10" fill="#8C94A6" {SW}/>'''
P["jackbox"] = f'''<path d="M200 230 Q140 205 200 180 Q260 155 200 130" stroke="{INK}" stroke-width="16" fill="none"/><path d="M200 230 Q140 205 200 180 Q260 155 200 130" stroke="#7ED957" stroke-width="8" fill="none"/>
<circle cx="200" cy="90" r="58" fill="#F2C29B" {SW}/>{eyes(178, 222, 80, 9)}{smile(200, 105, 18)}<path d="M145 65 L125 15 L180 42 L205 5 L225 42 L280 18 L255 65 Z" fill="#FF4D6D" {SW}/>
<rect x="85" y="225" width="230" height="150" rx="10" fill="#4CC9F0" {SW}/><path d="M85 225 L60 175 L110 170 L140 225 Z" fill="#FFD23F" {SW}/><circle cx="200" cy="300" r="26" fill="#FF8C1A" {SW}/>'''
P["card"] = f'''<rect x="70" y="70" width="260" height="270" rx="14" fill="#FFF3C4" {SW}/><path d="M200 255 C110 195 130 125 180 135 Q198 140 200 165 Q202 140 220 135 C270 125 290 195 200 255 Z" fill="#FF4D6D" {SW}/>
<path d="M95 100 H150" stroke="#9B5DE5" stroke-width="9" stroke-linecap="round"/><path d="M250 305 H305" stroke="#4CC9F0" stroke-width="9" stroke-linecap="round"/>'''
P["paperchain"] = "".join(f'<ellipse cx="{70 + i * 52}" cy="{200 + (i % 2) * 8}" rx="38" ry="52" fill="none" stroke="{INK}" stroke-width="28"/><ellipse cx="{70 + i * 52}" cy="{200 + (i % 2) * 8}" rx="38" ry="52" fill="none" stroke="{c}" stroke-width="17"/>'
                       for i, c in enumerate(("#FF4D6D", "#FFD23F", "#7ED957", "#4CC9F0", "#9B5DE5", "#FF8C1A")))
P["bone"] = f'''<path d="M110 165 A42 42 0 1 1 165 110 L235 180 A42 42 0 1 1 290 235 A42 42 0 1 1 235 290 A42 42 0 1 1 180 235 L110 165 Z" fill="#FFF8E7" {SW}/>'''
SETS["long21-presents"] = (P, {})

# ------------------------------------------------------------------ L22 writing
W = {}
W["pencil"] = f'''<g transform="rotate(35 200 200)"><rect x="160" y="60" width="80" height="230" fill="#FFD23F" {SW}/><path d="M160 290 L200 365 L240 290 Z" fill="#F2C29B" {SW}/><path d="M188 342 L200 365 L212 342 Z" fill="#3A3A44"/>
<rect x="160" y="30" width="80" height="34" fill="#C9CCD6" {SW}/><path d="M160 30 Q160 0 200 0 Q240 0 240 30 Z" fill="#FF8FA3" {SW}/><path d="M187 64 V290 M213 64 V290" stroke="#E8B000" stroke-width="6"/></g>'''
W["crayon"] = f'''<g transform="rotate(35 200 200)"><rect x="160" y="90" width="80" height="220" rx="6" fill="#FF4D6D" {SW}/><path d="M165 90 L200 25 L235 90 Z" fill="#FF4D6D" {SW}/>
<rect x="160" y="150" width="80" height="100" fill="#FFFFFF" {SW}/></g>'''
W["eraser"] = f'''<rect x="70" y="130" width="260" height="140" rx="26" fill="#FF8FA3" {SW}/><rect x="70" y="130" width="130" height="140" rx="26" fill="#4CC9F0" {SW}/>'''
W["paper"] = f'''<rect x="80" y="30" width="240" height="340" rx="8" fill="#FFFFFF" {SW}/>{"".join(f'<path d="M100 {y} H300" stroke="#9ED8FF" stroke-width="5"/>' for y in range(90, 350, 50))}<path d="M125 30 V370" stroke="#FF8FA3" stroke-width="4"/>'''
SETS["long22-writing"] = (W, {})

# ------------------------------------------------------------------ L23 bugs
B = {}
B["bee"] = f'''<ellipse cx="120" cy="130" rx="62" ry="86" fill="#D9F1FF" {SW} transform="rotate(-25 120 130)"/><ellipse cx="225" cy="115" rx="62" ry="86" fill="#D9F1FF" {SW} transform="rotate(20 225 115)"/>
<path d="M45 225 L10 245 L45 268 Z" fill="#3A3A44" {SW}/><ellipse cx="190" cy="245" rx="150" ry="95" fill="#FFD23F" {SW}/><path d="M110 165 Q90 245 110 325 L155 335 Q135 245 155 155 Z M205 150 Q225 245 205 340 L250 335 Q270 245 250 155 Z" fill="#3A3A44"/>
<circle cx="305" cy="235" r="62" fill="#FFD23F" {SW}/>{eyes(290, 335, 222, 10)}{smile(315, 255, 16)}<path d="M290 175 Q280 130 250 120 M325 175 Q335 130 365 125" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'''
B["ladybug"] = legs(["M105 150 L55 115", "M85 215 L30 215", "M105 285 L55 320", "M295 150 L345 115", "M315 215 L370 215", "M295 285 L345 320"]) + f'''<circle cx="200" cy="220" r="145" fill="#E8352E" {SW}/>
<path d="M90 130 Q200 60 310 130 Q200 195 90 130 Z" fill="#3A3A44" {SW}/>{eyes(165, 235, 115, 13)}{smile(200, 148, 22).replace(INK, "#FFF")}<path d="M200 170 V365" stroke="{INK}" stroke-width="9"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="24" fill="#3A3A44"/>' for x, y in ((130, 210), (270, 210), (110, 280), (290, 280), (155, 320), (245, 320)))}
<path d="M170 80 Q150 40 120 35 M230 80 Q250 40 280 35" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'''
B["ant"] = legs(["M170 235 L120 330 L90 350", "M200 235 L200 340 L175 365", "M230 235 L285 330 L315 350", "M170 225 L115 170 L85 170", "M200 200 L205 145 L180 120", "M230 225 L290 175 L320 170"]) + f'''<ellipse cx="85" cy="235" rx="72" ry="58" fill="#7A3E1E" {SW}/><ellipse cx="195" cy="230" rx="52" ry="42" fill="#7A3E1E" {SW}/>
<circle cx="295" cy="205" r="62" fill="#7A3E1E" {SW}/>{eyes(280, 325, 195, 10)}{smile(305, 225, 14)}<path d="M285 148 Q265 95 225 90 M320 148 Q345 95 380 95" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'''
B["spider"] = legs(["M150 215 Q90 130 25 150", "M150 240 Q80 215 15 255", "M155 265 Q90 305 35 350", "M170 280 Q130 345 95 385", "M250 215 Q310 130 375 150", "M250 240 Q320 215 385 255", "M245 265 Q310 305 365 350", "M230 280 Q270 345 305 385"]) + f'''<circle cx="200" cy="245" r="92" fill="#6A4BB5" {SW}/>{eyes(168, 232, 228, 18)}{smile(200, 275, 26)}<path d="M200 153 V20" stroke="{INK}" stroke-width="6"/>'''
B["grasshopper"] = f'''<path d="M95 225 L40 120 L30 330" stroke="{INK}" stroke-width="28" fill="none" stroke-linejoin="round"/><path d="M95 225 L40 120 L30 330" stroke="#5FBF3A" stroke-width="15" fill="none" stroke-linejoin="round"/>
<path d="M210 260 L220 345 M260 255 L285 345" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><ellipse cx="185" cy="205" rx="150" ry="65" fill="#7ED957" {SW}/><path d="M60 180 Q170 110 280 170 Q190 195 60 180 Z" fill="#4E9A35" {SW}/>
<circle cx="315" cy="185" r="54" fill="#7ED957" {SW}/>{eyes(305, 345, 170, 10)}{smile(330, 205, 13)}<path d="M305 135 Q280 60 215 50 M335 135 Q345 70 300 30" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'''
B["dragonfly"] = f'''<ellipse cx="105" cy="130" rx="95" ry="35" fill="#BDEBFF" {SW} transform="rotate(25 105 130)"/><ellipse cx="295" cy="130" rx="95" ry="35" fill="#BDEBFF" {SW} transform="rotate(-25 295 130)"/>
<ellipse cx="105" cy="205" rx="95" ry="32" fill="#D9F1FF" {SW} transform="rotate(-12 105 205)"/><ellipse cx="295" cy="205" rx="95" ry="32" fill="#D9F1FF" {SW} transform="rotate(12 295 205)"/>
<path d="M200 200 L200 380" stroke="{INK}" stroke-width="34" stroke-linecap="round"/><path d="M200 200 L200 380" stroke="#0FA3B1" stroke-width="20" stroke-linecap="round"/><ellipse cx="200" cy="165" rx="38" ry="58" fill="#0FA3B1" {SW}/><circle cx="200" cy="85" r="46" fill="#0FA3B1" {SW}/>{eyes(180, 220, 78, 14)}{smile(200, 105, 12)}'''
B["firefly"] = f'''<circle cx="200" cy="280" r="95" fill="#FFF3A0" opacity="0.8"/><ellipse cx="130" cy="140" rx="60" ry="30" fill="#D9F1FF" {SW} transform="rotate(40 130 140)"/><ellipse cx="270" cy="140" rx="60" ry="30" fill="#D9F1FF" {SW} transform="rotate(-40 270 140)"/>
<ellipse cx="200" cy="205" rx="66" ry="110" fill="#3A3A44" {SW}/><path d="M138 245 Q200 280 262 245 Q255 315 200 318 Q145 315 138 245 Z" fill="#FFE34D" {SW}/><circle cx="200" cy="95" r="52" fill="#E8573C" {SW}/>{eyes(180, 220, 88, 10)}{smile(200, 112, 13)}
<path d="M180 45 Q165 15 135 15 M220 45 Q235 15 265 15" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'''
B["beetle"] = legs(["M105 170 L50 135", "M95 230 L35 230", "M110 295 L55 335", "M295 170 L350 135", "M305 230 L365 230", "M290 295 L345 335"]) + f'''<ellipse cx="200" cy="235" rx="118" ry="140" fill="#1F9E7A" {SW}/><path d="M200 105 V375" stroke="{INK}" stroke-width="8"/>
<ellipse cx="150" cy="215" rx="26" ry="70" fill="#5FD9B5" opacity="0.8"/><circle cx="200" cy="105" r="66" fill="#176B57" {SW}/>{eyes(175, 225, 95, 11)}{smile(200, 122, 15)}<path d="M175 45 Q160 15 130 15 M225 45 Q240 15 270 15" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'''
B["worm"] = f'''<path d="M45 300 Q110 180 170 290 T290 280" stroke="{INK}" stroke-width="72" fill="none" stroke-linecap="round"/><path d="M45 300 Q110 180 170 290 T290 280" stroke="#FF9FB0" stroke-width="58" fill="none" stroke-linecap="round"/>
<circle cx="310" cy="235" r="56" fill="#FF9FB0" {SW}/>{eyes(295, 335, 222, 10)}{smile(315, 250, 14)}'''
B["snail"] = f'''<path d="M40 325 Q200 345 345 325 Q370 310 345 280 Q335 255 330 205" stroke="{INK}" stroke-width="56" fill="none" stroke-linecap="round"/><path d="M40 325 Q200 345 345 325 Q370 310 345 280 Q335 255 330 205" stroke="#F2C97B" stroke-width="42" fill="none" stroke-linecap="round"/>
<circle cx="185" cy="205" r="115" fill="#C8894E" {SW}/><path d="M185 205 m-85 0 a85 85 0 1 1 85 85 a60 60 0 1 1 -60 -60 a36 36 0 1 1 35 35" stroke="{INK}" stroke-width="9" fill="none"/>
<path d="M320 180 V115 M355 190 L375 125" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><circle cx="320" cy="108" r="13" fill="{INK}"/><circle cx="377" cy="118" r="13" fill="{INK}"/>{smile(340, 228, 13)}'''
B["magnifier"] = f'''<path d="M250 250 L350 350" stroke="{INK}" stroke-width="46" stroke-linecap="round"/><path d="M250 250 L350 350" stroke="#C9954A" stroke-width="30" stroke-linecap="round"/><circle cx="165" cy="165" r="120" fill="#D9F1FF" opacity="0.8"/>
<circle cx="165" cy="165" r="120" fill="none" stroke="{INK}" stroke-width="34"/><circle cx="165" cy="165" r="120" fill="none" stroke="#FFD23F" stroke-width="20"/><path d="M95 130 Q115 90 155 80" stroke="#FFFFFF" stroke-width="14" fill="none" stroke-linecap="round"/>'''
B["hive"] = f'''<path d="M200 20 V60" stroke="#7A3E1E" stroke-width="20"/>{"".join(f'<ellipse cx="200" cy="{95 + i * 60}" rx="{v}" ry="38" fill="#FFC93C" {SW}/>' for i, v in enumerate((85, 130, 150, 130, 90)))}<circle cx="200" cy="245" r="26" fill="#3A3A44" {SW}/>'''
B["honey"] = f'''<path d="M100 130 Q70 160 80 290 Q90 355 200 355 Q310 355 320 290 Q330 160 300 130 Z" fill="#FFB300" {SW}/><rect x="100" y="80" width="200" height="55" rx="10" fill="#E9F6FF" {SW}/>
<rect x="125" y="185" width="150" height="100" rx="12" fill="#FFF8E7" {SW}/><circle cx="200" cy="235" r="26" fill="#FFD23F" {SW}/>'''
B["web"] = f'''{"".join(f'<path d="M200 200 L{200 + 190 * math.cos(i / 8 * 6.283):.0f} {200 + 190 * math.sin(i / 8 * 6.283):.0f}" stroke="#E9EEF7" stroke-width="7"/>' for i in range(8))}
{"".join('<polygon points="' + " ".join(f"{200 + r * math.cos(i / 8 * 6.283):.0f},{200 + r * math.sin(i / 8 * 6.283):.0f}" for i in range(8)) + '" fill="none" stroke="#E9EEF7" stroke-width="6"/>' for r in (55, 100, 145, 190))}'''
B["soil"] = f'''<ellipse cx="200" cy="300" rx="185" ry="80" fill="#7A4E2B" {SW}/><path d="M120 240 Q200 150 280 240 Q200 262 120 240 Z" fill="#5A3A20" {SW}/>'''
SETS["long23-bugs"] = (B, {
    "underground": f'''<rect width="1920" height="1080" fill="#7A4E2B"/><rect width="1920" height="220" fill="#A9E1FF"/><path d="M0 190 Q480 150 960 190 T1920 190 L1920 240 L0 240 Z" fill="#6BC24A" {SW}/>
  {"".join(f'<circle cx="{(i * 283) % 1920}" cy="{270 + (i * 157) % 780}" r="{6 + i % 3 * 4}" fill="#62401F"/>' for i in range(90))}
  <path d="M960 240 V440 Q960 500 800 500 H420 M960 440 Q980 520 1180 520 H1560 M800 500 Q760 650 560 690 M1180 520 Q1230 700 1420 760 M960 460 V840" stroke="#3E2A17" stroke-width="86" fill="none" stroke-linecap="round"/>
  <path d="M960 240 V440 Q960 500 800 500 H420 M960 440 Q980 520 1180 520 H1560 M800 500 Q760 650 560 690 M1180 520 Q1230 700 1420 760 M960 460 V840" stroke="#B5844E" stroke-width="64" fill="none" stroke-linecap="round"/>
  {"".join(f'<ellipse cx="{x}" cy="{y}" rx="130" ry="74" fill="#B5844E" stroke="#3E2A17" stroke-width="12"/>' for x, y in ((360, 500), (500, 700), (1620, 520), (1480, 770), (960, 860)))}'''})


def render():
    sheet = Image.new("RGBA", (180 * 16, 180 * 3 + 220), (230, 230, 230, 255))
    for row, (folder, (items, bgs)) in enumerate(SETS.items()):
        out = ROOT / folder / "art"
        out.mkdir(parents=True, exist_ok=True)
        names = list(items)
        cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{items[n]}</svg></div>' for i, n in enumerate(names))
        A.shot(f'<html><body style="margin:0;position:relative;width:{400 * len(names)}px;height:400px">{cells}</body></html>', str(out / "_i.png"), 400 * len(names), 400, scale=2)
        im = Image.open(out / "_i.png")
        for i, n in enumerate(names):
            c = im.crop((i * 800, 0, i * 800 + 800, 800))
            c.save(out / f"item_{n}.png")
            sheet.alpha_composite(c.convert("RGBA").resize((170, 170)), (i * 180, row * 180))
        (out / "_i.png").unlink()
        for j, (k, svg) in enumerate(bgs.items()):
            A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>', str(out / f"bg_{k}.png"), 1920, 1080)
            sheet.alpha_composite(Image.open(out / f"bg_{k}.png").convert("RGBA").resize((360, 200)), (j * 380, 3 * 180 + 10))
    sheet.save(ROOT / "tools" / "_sheet_21_23.png")
    print("done")


if __name__ == "__main__":
    render()
