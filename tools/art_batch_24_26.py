"""Art for L24 Space, L25 First Words, L26 Months & New Year.
python tools/art_batch_24_26.py -> long24-space/art, long25-words/art, long26-months/art (+ tools/_sheet_24_26.png)
"""
import pathlib, sys
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


def planet(col, extra="", r=150, face=True):
    return (f'<defs><clipPath id="c"><circle cx="200" cy="200" r="{r}"/></clipPath></defs><circle cx="200" cy="200" r="{r}" fill="{col}" {SW}/>'
            f'<g clip-path="url(#c)">{extra}</g><circle cx="200" cy="200" r="{r}" fill="none" stroke="{INK}" stroke-width="7"/>'
            + (eyes(165, 235, 190, 13) + smile(200, 225, 24) if face else ""))


SETS = {}
# ------------------------------------------------------------------ L24 space
S = {}
S["sun"] = "".join(f'<path d="M200 200 L{200 + 60 * __import__("math").cos(i * .524 - .2):.0f} {200 + 60 * __import__("math").sin(i * .524 - .2):.0f} L{200 + 195 * __import__("math").cos(i * .524):.0f} {200 + 195 * __import__("math").sin(i * .524):.0f} L{200 + 60 * __import__("math").cos(i * .524 + .2):.0f} {200 + 60 * __import__("math").sin(i * .524 + .2):.0f} Z" fill="#FF9F1C" {SW}/>' for i in range(12)) + f'<circle cx="200" cy="200" r="130" fill="#FFD23F" {SW}/>{eyes(165, 235, 185, 13)}{smile(200, 225, 26)}'
S["mercury"] = planet("#A9A39B", '<circle cx="120" cy="130" r="26" fill="#8C867E"/><circle cx="280" cy="280" r="34" fill="#8C867E"/><circle cx="270" cy="110" r="16" fill="#8C867E"/>', 100)
S["venus"] = planet("#F2C14E", '<path d="M40 150 Q200 110 360 160 M40 260 Q200 300 360 240" stroke="#E0A030" stroke-width="26" fill="none"/>', 125)
S["earth"] = planet("#3FA7F5", '<path d="M70 120 Q140 70 190 120 Q210 170 150 190 Q90 220 70 170 Z M230 230 Q300 200 340 250 Q330 320 270 330 Q220 300 230 230 Z M240 80 Q280 70 300 110 Q270 130 240 110 Z" fill="#5FC85A"/>', 130)
S["mars"] = planet("#D9572B", '<circle cx="130" cy="140" r="28" fill="#B8441F"/><circle cx="270" cy="270" r="36" fill="#B8441F"/><path d="M120 62 Q200 40 280 62 L270 90 Q200 76 130 90 Z" fill="#FFF"/>', 115)
S["jupiter"] = planet("#E8B98A", '<path d="M0 95 H400 M0 150 H400 M0 255 H400 M0 310 H400" stroke="#C4824C" stroke-width="28"/><ellipse cx="280" cy="280" rx="48" ry="30" fill="#D9572B" stroke="#7A3E1E" stroke-width="5"/>', 180)
S["saturn"] = f'<ellipse cx="200" cy="200" rx="195" ry="62" fill="none" stroke="{INK}" stroke-width="40" transform="rotate(-15 200 200)"/><ellipse cx="200" cy="200" rx="195" ry="62" fill="none" stroke="#E8CB8A" stroke-width="28" transform="rotate(-15 200 200)"/>' + planet("#F0D58C", '<path d="M0 150 H400 M0 250 H400" stroke="#D9B765" stroke-width="22"/>', 120) + f'<path d="M15 248 Q200 305 385 150" fill="none" stroke="{INK}" stroke-width="40"/><path d="M15 248 Q200 305 385 150" fill="none" stroke="#E8CB8A" stroke-width="28"/>'
S["uranus"] = planet("#8FE3E6", '<path d="M0 130 H400 M0 270 H400" stroke="#6CCFD3" stroke-width="20"/>', 135)
S["neptune"] = planet("#3B5BDB", '<path d="M40 120 Q200 90 360 130 M40 280 Q200 310 360 270" stroke="#5C7CFA" stroke-width="24" fill="none"/><ellipse cx="270" cy="150" rx="36" ry="20" fill="#1E3A9E"/>', 135)
S["moon2"] = planet("#D7DAE2", '<circle cx="120" cy="130" r="30" fill="#B6BAC6"/><circle cx="285" cy="130" r="22" fill="#B6BAC6"/><circle cx="130" cy="285" r="24" fill="#B6BAC6"/><circle cx="275" cy="285" r="36" fill="#B6BAC6"/>', 150)
S["astronaut"] = f'''<rect x="70" y="170" width="44" height="130" rx="20" fill="#C9CCD6" {SW}/><rect x="286" y="170" width="44" height="130" rx="20" fill="#C9CCD6" {SW}/>
<rect x="130" y="290" width="58" height="95" rx="16" fill="#F2F4F8" {SW}/><rect x="212" y="290" width="58" height="95" rx="16" fill="#F2F4F8" {SW}/><rect x="110" y="165" width="180" height="150" rx="30" fill="#F2F4F8" {SW}/>
<rect x="150" y="205" width="100" height="60" rx="10" fill="#FF6B6B" {SW}/><circle cx="175" cy="235" r="11" fill="#FFD23F"/><circle cx="225" cy="235" r="11" fill="#4CC9F0"/>
<circle cx="200" cy="95" r="92" fill="#F2F4F8" {SW}/><circle cx="200" cy="95" r="66" fill="#F2C29B" {SW}/>{eyes(175, 225, 85, 10)}{smile(200, 115, 18)}<path d="M150 55 Q200 20 250 55 L250 70 Q200 45 150 70 Z" fill="#3A3A44"/>'''
S["comet"] = f'''<path d="M260 150 L30 60 L180 190 L20 200 L190 250 L60 340 L260 250 Z" fill="#9ED8FF" {SW}/><circle cx="280" cy="195" r="78" fill="#FFD23F" {SW}/>'''
S["telescope"] = f'''<path d="M200 230 L120 380 M200 230 L200 380 M200 230 L280 380" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><g transform="rotate(-28 200 170)"><rect x="60" y="130" width="280" height="80" rx="12" fill="#4CC9F0" {SW}/><rect x="320" y="115" width="46" height="110" rx="10" fill="#FFD23F" {SW}/><rect x="30" y="145" width="40" height="50" rx="8" fill="#3A3A44" {SW}/></g>'''
S["alien"] = f'''<path d="M150 90 Q130 40 100 35 M250 90 Q270 40 300 35" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="98" cy="32" r="16" fill="#FFD23F" {SW}/><circle cx="302" cy="32" r="16" fill="#FFD23F" {SW}/>
<ellipse cx="200" cy="180" rx="115" ry="105" fill="#7ED957" {SW}/>{eyes(160, 240, 165, 26)}{smile(200, 225, 30)}<path d="M125 270 Q200 400 275 270 Z" fill="#5FBF3A" {SW}/>'''
S["footprint"] = f'''<path d="M145 345 Q90 200 150 105 Q205 45 250 110 Q295 190 250 345 Q200 385 145 345 Z" fill="#8C94A6" {SW}/>{"".join(f'<path d="M145 {y} H255" stroke="#6C7486" stroke-width="12"/>' for y in (150, 200, 250, 300))}'''
SETS["long24-space"] = (S, {
    "space": f'''<rect width="1920" height="1080" fill="#0E1140"/>
  {"".join(f'<circle cx="{(i * 271) % 1920}" cy="{(i * 433) % 1080}" r="{2 + i % 3}" fill="#FFFFFF"/>' for i in range(220))}
  {"".join(f'<path d="M{(i * 487) % 1920} {(i * 311) % 1080} l9 20 20 9 -20 9 -9 20 -9 -20 -20 -9 20 -9 Z" fill="#FFE27A"/>' for i in range(22))}
  <ellipse cx="400" cy="260" rx="430" ry="150" fill="#3B2C8C" opacity="0.5"/><ellipse cx="1500" cy="820" rx="480" ry="170" fill="#7A2C8C" opacity="0.4"/>''',
    "moonland": f'''<rect width="1920" height="1080" fill="#0E1140"/>
  {"".join(f'<circle cx="{(i * 271) % 1920}" cy="{(i * 137) % 620}" r="{2 + i % 3}" fill="#FFFFFF"/>' for i in range(110))}
  <circle cx="1560" cy="220" r="120" fill="#3FA7F5" {SW}/><path d="M1490 170 Q1540 130 1590 170 Q1600 220 1540 240 Q1480 240 1490 170 Z" fill="#5FC85A"/>
  <path d="M0 720 Q480 640 960 700 Q1440 760 1920 680 L1920 1080 L0 1080 Z" fill="#C9CCD6" {SW}/>
  {"".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.34}" fill="#A5A9B6" stroke="#7E8290" stroke-width="5"/>' for x, y, r in ((300, 830, 110), (820, 930, 150), (1420, 840, 90), (1700, 980, 120), (120, 1000, 70)))}''',
    "launch": f'''<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6EC6FF"/><stop offset="1" stop-color="#D9F1FF"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#s)"/>
  <path d="M0 860 Q960 800 1920 860 L1920 1080 L0 1080 Z" fill="#7ED957" {SW}/><rect x="760" y="830" width="400" height="60" fill="#8C94A6" {SW}/>
  <path d="M1230 860 V240 M1330 860 V240 M1230 340 L1330 440 M1330 340 L1230 440 M1230 540 L1330 640 M1330 540 L1230 640" stroke="#E8573C" stroke-width="20" fill="none"/>'''})

# ------------------------------------------------------------------ L25 words
W = {}
W["cupkid"] = f'''<path d="M95 110 H265 L245 345 Q180 370 115 345 Z" fill="#4CC9F0" {SW}/><path d="M262 160 Q335 160 330 225 Q325 290 250 285" fill="none" stroke="{INK}" stroke-width="28"/><path d="M262 160 Q335 160 330 225 Q325 290 250 285" fill="none" stroke="#4CC9F0" stroke-width="15"/>'''
W["baby"] = f'''<ellipse cx="200" cy="295" rx="118" ry="88" fill="#FFD6E5" {SW}/><circle cx="200" cy="145" r="112" fill="#F2C29B" {SW}/>{eyes(160, 240, 140, 15)}{smile(200, 185, 26)}<circle cx="120" cy="175" r="18" fill="#FF9FB0"/><circle cx="280" cy="175" r="18" fill="#FF9FB0"/><path d="M200 34 Q180 10 205 5 Q230 8 215 28" fill="none" stroke="#3A3A44" stroke-width="9" stroke-linecap="round"/>'''
W["mama"] = f'''<path d="M85 395 Q95 220 200 215 Q305 220 315 395 Z" fill="#FF8FB1" {SW}/><path d="M92 185 Q70 40 200 28 Q330 40 308 185 Q300 270 270 230 L130 230 Q100 270 92 185 Z" fill="#5A3420" {SW}/><circle cx="200" cy="140" r="88" fill="#E8B48A" {SW}/><path d="M112 125 Q150 45 200 60 Q250 45 288 125 Q240 90 200 95 Q160 90 112 125 Z" fill="#5A3420"/>{eyes(168, 232, 140, 11)}{smile(200, 178, 22)}'''
W["papa"] = f'''<path d="M75 395 Q85 230 200 225 Q315 230 325 395 Z" fill="#3B7DDD" {SW}/><path d="M160 228 L200 280 L240 228 Z" fill="#FFF" {SW}/><circle cx="200" cy="140" r="90" fill="#D9A070" {SW}/><path d="M108 125 Q115 40 200 38 Q285 40 292 125 Q250 85 200 92 Q150 85 108 125 Z" fill="#2B2B33" {SW}/>{eyes(168, 232, 140, 11)}<path d="M160 168 Q200 150 240 168 Q200 190 160 168 Z" fill="#2B2B33"/>{smile(200, 188, 16)}'''
W["bottle"] = f'''<rect x="130" y="130" width="140" height="240" rx="30" fill="#E9F6FF" {SW}/><rect x="130" y="215" width="140" height="155" rx="26" fill="#FFF8E7"/><rect x="130" y="130" width="140" height="240" rx="30" fill="none" stroke="{INK}" stroke-width="7"/><rect x="118" y="95" width="164" height="42" rx="14" fill="#FF8FB1" {SW}/><path d="M170 95 Q172 35 200 28 Q228 35 230 95 Z" fill="#FFD6A0" {SW}/>'''
W["spoonfood"] = f'''<ellipse cx="200" cy="255" rx="165" ry="70" fill="#FFFFFF" {SW}/><path d="M50 250 Q200 400 350 250 Z" fill="#FFB3C7" {SW}/><path d="M70 235 Q200 150 330 235 Q200 275 70 235 Z" fill="#FFD23F" {SW}/>'''
SETS["long25-words"] = (W, {})

# ------------------------------------------------------------------ L26 months
M = {}
M["firework"] = "".join(f'<path d="M200 200 L{200 + 180 * __import__("math").cos(i * .524):.0f} {200 + 180 * __import__("math").sin(i * .524):.0f}" stroke="{c}" stroke-width="16" stroke-linecap="round"/><circle cx="{200 + 190 * __import__("math").cos(i * .524):.0f}" cy="{200 + 190 * __import__("math").sin(i * .524):.0f}" r="10" fill="{c}"/>' for i, c in zip(range(12), ["#FF4D6D", "#FFD23F", "#4CC9F0", "#7ED957", "#9B5DE5", "#FF8C1A"] * 2))
M["party"] = f'''<path d="M200 40 L320 350 Q200 395 80 350 Z" fill="#9B5DE5" {SW}/><path d="M140 195 L260 195 M105 280 L295 280" stroke="#FFD23F" stroke-width="20"/><circle cx="200" cy="38" r="26" fill="#FF4D6D" {SW}/>'''
M["clock12"] = f'''<circle cx="200" cy="200" r="165" fill="#FFFFFF" {SW}/><path d="M200 200 V70 M200 200 V90" stroke="{INK}" stroke-width="13" stroke-linecap="round"/><circle cx="200" cy="200" r="13" fill="{INK}"/>
{"".join(f'<circle cx="{200 + 138 * __import__("math").cos(i * .5236):.0f}" cy="{200 + 138 * __import__("math").sin(i * .5236):.0f}" r="8" fill="#FF4D6D"/>' for i in range(12))}'''
M["schoolbag"] = f'''<path d="M150 90 Q150 40 200 40 Q250 40 250 90" fill="none" stroke="{INK}" stroke-width="18"/><rect x="85" y="85" width="230" height="285" rx="46" fill="#4CC9F0" {SW}/><rect x="125" y="225" width="150" height="110" rx="18" fill="#FFD23F" {SW}/><path d="M85 165 H315" stroke="{INK}" stroke-width="7"/>'''
M["autumnleaf"] = f'''<path d="M200 25 L240 115 L325 80 L295 170 L375 210 L285 245 L300 335 L215 295 L200 380 L185 295 L100 335 L115 245 L25 210 L105 170 L75 80 L160 115 Z" fill="#E8742B" {SW}/><path d="M200 120 V380" stroke="#7A3E1E" stroke-width="10"/>'''
M["icecream2"] = f'''<path d="M125 190 L200 380 L275 190 Z" fill="#E8B964" {SW}/><circle cx="200" cy="130" r="92" fill="#FF9FB0" {SW}/><path d="M125 190 Q200 240 275 190" fill="#FF9FB0" {SW}/>'''
M["blossom"] = "".join(f'<ellipse cx="200" cy="105" rx="62" ry="86" fill="#FFB3C7" {SW} transform="rotate({a} 200 200)"/>' for a in (0, 72, 144, 216, 288)) + f'<circle cx="200" cy="200" r="46" fill="#FFD23F" {SW}/>'
SETS["long26-months"] = (M, {
    "city": f'''<rect width="1920" height="1080" fill="#141A52"/>
  {"".join(f'<circle cx="{(i * 271) % 1920}" cy="{(i * 113) % 620}" r="{2 + i % 3}" fill="#FFFFFF"/>' for i in range(90))}
  {"".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1080 - y}" fill="{c}" {SW}/>' + "".join(f'<rect x="{x + 24 + j * 60}" y="{y + 30 + k * 76}" width="36" height="46" fill="#FFE27A"/>' for j in range(int((w - 30) / 60)) for k in range(int((1040 - y) / 76))) for x, y, w, c in ((0, 700, 300, "#3B3F88"), (310, 590, 240, "#4F3B88"), (560, 760, 330, "#2F5D88"), (900, 620, 280, "#5C3B88"), (1190, 720, 300, "#3B3F88"), (1500, 560, 420, "#2F5D88")))}'''})


def render():
    sheet = Image.new("RGBA", (180 * 19, 180 * 3 + 220), (230, 230, 230, 255))
    for row, (folder, (items, bgs)) in enumerate(SETS.items()):
        out = ROOT / folder / "art"
        out.mkdir(parents=True, exist_ok=True)
        names = list(items)
        for i, n in enumerate(names):
            A.shot(f'<html><body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{items[n]}</svg></body></html>', str(out / f"item_{n}.png"), 400, 400, scale=2)
            sheet.alpha_composite(Image.open(out / f"item_{n}.png").convert("RGBA").resize((170, 170)), (i * 180, row * 180))
        for j, (k, svg) in enumerate(bgs.items()):
            A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>', str(out / f"bg_{k}.png"), 1920, 1080)
            sheet.alpha_composite(Image.open(out / f"bg_{k}.png").convert("RGBA").resize((360, 200)), ((row * 3 + j) * 380 % 1520, 3 * 180 + 10))
    sheet.save(ROOT / "tools" / "_sheet_24_26.png")
    print("done")


if __name__ == "__main__":
    render()
