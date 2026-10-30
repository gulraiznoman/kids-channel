"""Grown-up wild animals (full body, cartoon) + habitat backgrounds for Long video 13 "Wild Animals Safari".
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


def eyes(x1, x2, y, r=12):
    return (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{x1 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/>')


def cheeks(x1, x2, y):
    return f'<ellipse cx="{x1}" cy="{y}" rx="14" ry="9" fill="#FF8FA3" opacity="0.7"/><ellipse cx="{x2}" cy="{y}" rx="14" ry="9" fill="#FF8FA3" opacity="0.7"/>'


def smile(cx, cy, w=18):
    return f'<path d="M{cx - w} {cy} Q{cx} {cy + w} {cx + w} {cy}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'


def legs4(xs, y0, y1, col, w=34):
    return "".join(f'<rect x="{x - w / 2}" y="{y0}" width="{w}" height="{y1 - y0}" rx="{w / 2}" fill="{col}" {SW}/>' for x in xs)


I = {}
I["lion"] = f'''{legs4((130, 175, 265, 305), 260, 365, "#E8A94E")}<path d="M290 200 Q370 180 365 120 Q385 160 350 220" stroke="#E8A94E" stroke-width="16" fill="none"/><circle cx="363" cy="118" r="14" fill="#A0582C"/>
<ellipse cx="225" cy="245" rx="120" ry="65" fill="#F2BE6A" {SW}/>
{"".join(f'<circle cx="{120 + 70 * __import__("math").cos(a / 10 * 6.283)}" cy="{170 + 70 * __import__("math").sin(a / 10 * 6.283)}" r="38" fill="#B5652E" {SW}/>' for a in range(10))}
<circle cx="120" cy="170" r="60" fill="#F2BE6A" {SW}/><circle cx="85" cy="120" r="16" fill="#F2BE6A" {SW}/><circle cx="155" cy="120" r="16" fill="#F2BE6A" {SW}/>
{eyes(100, 140, 160, 10)}<ellipse cx="120" cy="190" rx="16" ry="11" fill="#7A3E1E"/>{smile(120, 200, 14)}{cheeks(88, 152, 190)}'''
I["giraffe"] = f'''{legs4((150, 185, 255, 290), 250, 380, "#F2C14E", 26)}<ellipse cx="220" cy="240" rx="100" ry="50" fill="#F2C14E" {SW}/>
<path d="M150 230 L120 70" stroke="{INK}" stroke-width="58" stroke-linecap="round"/><path d="M150 230 L120 70" stroke="#F2C14E" stroke-width="44" stroke-linecap="round"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#B5743A"/>' for x, y, r in ((200, 230, 16), (245, 250, 13), (280, 225, 12), (180, 260, 10), (140, 180, 10), (132, 130, 9), (148, 210, 8)))}
<ellipse cx="115" cy="55" rx="48" ry="38" fill="#F2C14E" {SW}/><path d="M100 25 L95 0 M130 25 L135 0" stroke="{INK}" stroke-width="7"/><circle cx="95" cy="0" r="8" fill="#B5743A"/><circle cx="135" cy="0" r="8" fill="#B5743A"/>
{eyes(100, 130, 48, 8)}<ellipse cx="88" cy="72" rx="20" ry="12" fill="#E8B060"/>{cheeks(95, 145, 66)}'''
I["tiger"] = f'''{legs4((130, 175, 265, 305), 260, 365, "#FF9A2E")}<path d="M330 230 Q385 200 370 140" stroke="{INK}" stroke-width="22" fill="none"/><path d="M330 230 Q385 200 370 140" stroke="#FF9A2E" stroke-width="12" fill="none"/>
<ellipse cx="225" cy="245" rx="120" ry="62" fill="#FF9A2E" {SW}/>{"".join(f'<path d="M{x} 190 Q{x + 12} 240 {x} 290" stroke="{INK}" stroke-width="10" fill="none"/>' for x in (180, 220, 260, 300))}
<circle cx="120" cy="175" r="68" fill="#FF9A2E" {SW}/><circle cx="72" cy="118" r="20" fill="#FF9A2E" {SW}/><circle cx="168" cy="118" r="20" fill="#FF9A2E" {SW}/>
<path d="M95 115 l10 25 M120 108 l0 25 M145 115 l-10 25" stroke="{INK}" stroke-width="8"/><ellipse cx="120" cy="205" rx="38" ry="25" fill="#FFF3E0"/>
{eyes(98, 142, 165, 10)}<ellipse cx="120" cy="192" rx="13" ry="9" fill="#FF6B8B"/>{smile(120, 205, 12)}'''
I["hippo"] = f'''{legs4((120, 170, 260, 300), 270, 360, "#9C8FB8", 44)}<ellipse cx="220" cy="240" rx="150" ry="85" fill="#B3A6D4" {SW}/>
<ellipse cx="115" cy="210" rx="85" ry="70" fill="#B3A6D4" {SW}/><circle cx="85" cy="140" r="20" fill="#B3A6D4" {SW}/><circle cx="150" cy="140" r="20" fill="#B3A6D4" {SW}/>
{eyes(95, 140, 168, 10)}<ellipse cx="100" cy="230" rx="70" ry="40" fill="#C9BEE4" {SW}/><circle cx="80" cy="220" r="7" fill="{INK}"/><circle cx="120" cy="220" r="7" fill="{INK}"/>{smile(100, 245, 22)}'''
I["rhino"] = f'''{legs4((130, 175, 265, 305), 260, 360, "#8E97A8", 40)}<ellipse cx="225" cy="235" rx="140" ry="75" fill="#A7B0C0" {SW}/>
<ellipse cx="105" cy="215" rx="75" ry="58" fill="#A7B0C0" {SW}/><path d="M45 205 L20 130 L70 185 Z" fill="#F2E6D6" {SW}/><path d="M80 175 L72 140 L95 170 Z" fill="#F2E6D6" {SW}/>
<circle cx="140" cy="150" r="16" fill="#A7B0C0" {SW}/>{eyes(110, 135, 195, 8)}{smile(75, 240, 14)}'''
I["gorilla"] = f'''<ellipse cx="200" cy="250" rx="115" ry="105" fill="#4A4A55" {SW}/><ellipse cx="200" cy="270" rx="70" ry="70" fill="#7A7A88"/>
<path d="M95 220 Q40 290 70 360 L110 360 Q100 300 130 260" fill="#4A4A55" {SW}/><path d="M305 220 Q360 290 330 360 L290 360 Q300 300 270 260" fill="#4A4A55" {SW}/>
<circle cx="200" cy="120" r="70" fill="#4A4A55" {SW}/><ellipse cx="200" cy="138" rx="50" ry="42" fill="#9A9AA8"/>{eyes(180, 220, 118, 10)}
<circle cx="190" cy="148" r="5" fill="{INK}"/><circle cx="210" cy="148" r="5" fill="{INK}"/>{smile(200, 160, 14)}'''
I["kangaroo"] = f'''<path d="M260 330 Q360 340 380 260" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M260 330 Q360 340 380 260" stroke="#D99A5A" stroke-width="28" fill="none" stroke-linecap="round"/>
<ellipse cx="220" cy="250" rx="70" ry="100" fill="#D99A5A" {SW}/><ellipse cx="205" cy="270" rx="40" ry="55" fill="#F2C08A"/>
<ellipse cx="200" cy="360" rx="75" ry="22" fill="#D99A5A" {SW}/><path d="M160 210 L130 260 M175 215 L150 270" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>
<ellipse cx="190" cy="120" rx="48" ry="40" fill="#D99A5A" {SW}/><path d="M170 85 L160 30 L190 75 M205 85 L215 30 L220 80" fill="#D99A5A" stroke="{INK}" stroke-width="6"/>
{eyes(178, 205, 112, 8)}<ellipse cx="160" cy="135" rx="8" ry="6" fill="{INK}"/>{cheeks(170, 215, 135)}'''
I["panda"] = f'''<ellipse cx="200" cy="260" rx="110" ry="100" fill="#FFFFFF" {SW}/><ellipse cx="200" cy="245" rx="112" ry="40" fill="#2B2B33"/>
<ellipse cx="135" cy="340" rx="40" ry="30" fill="#2B2B33" {SW}/><ellipse cx="265" cy="340" rx="40" ry="30" fill="#2B2B33" {SW}/>
<circle cx="200" cy="130" r="75" fill="#FFFFFF" {SW}/><circle cx="140" cy="70" r="25" fill="#2B2B33" {SW}/><circle cx="260" cy="70" r="25" fill="#2B2B33" {SW}/>
<ellipse cx="172" cy="128" rx="22" ry="28" fill="#2B2B33" transform="rotate(-20 172 128)"/><ellipse cx="228" cy="128" rx="22" ry="28" fill="#2B2B33" transform="rotate(20 228 128)"/>
{eyes(175, 225, 125, 7)}<ellipse cx="200" cy="155" rx="12" ry="8" fill="#2B2B33"/>{smile(200, 165, 12)}{cheeks(160, 240, 160)}
<path d="M300 200 L330 160 M305 205 L345 190" stroke="#5DBB46" stroke-width="12" stroke-linecap="round"/>'''
I["bear"] = f'''{legs4((140, 185, 265, 305), 270, 365, "#8A5A33", 44)}<ellipse cx="225" cy="245" rx="130" ry="80" fill="#A0703F" {SW}/>
<circle cx="115" cy="190" r="65" fill="#A0703F" {SW}/><circle cx="72" cy="135" r="20" fill="#A0703F" {SW}/><circle cx="158" cy="135" r="20" fill="#A0703F" {SW}/>
<ellipse cx="105" cy="210" rx="34" ry="24" fill="#D9A066"/>{eyes(98, 135, 180, 9)}<ellipse cx="100" cy="200" rx="11" ry="8" fill="{INK}"/>{smile(104, 214, 10)}'''
I["parrot"] = f'''<path d="M200 260 L230 390 L260 380 Z M210 270 L200 390 L235 385 Z" fill="#4C79D8" {SW}/>
<ellipse cx="200" cy="200" rx="75" ry="100" fill="#E8352E" {SW}/><path d="M150 180 Q110 260 160 300 Q190 240 175 190 Z" fill="#FFD23F" {SW}/><path d="M160 260 Q150 300 185 300" fill="#4C79D8" stroke="{INK}" stroke-width="5"/>
<circle cx="200" cy="105" r="58" fill="#E8352E" {SW}/><ellipse cx="220" cy="100" rx="28" ry="22" fill="#FFFFFF"/>{eyes(225, 225, 100, 9)}
<path d="M250 110 Q300 115 285 160 Q270 140 245 140 Z" fill="#3A3A44" {SW}/><path d="M185 300 L175 330 M215 300 L225 330" stroke="#888" stroke-width="10" stroke-linecap="round"/>'''
I["flamingo"] = f'''<path d="M200 260 L200 380 M200 300 L240 280" stroke="#FF8FB1" stroke-width="10" stroke-linecap="round"/>
<ellipse cx="220" cy="220" rx="90" ry="55" fill="#FF8FB1" {SW}/><path d="M250 210 Q330 200 300 250" fill="#FF6B9A" {SW}/>
<path d="M150 210 Q110 140 160 90 Q200 60 175 40" stroke="{INK}" stroke-width="36" fill="none" stroke-linecap="round"/><path d="M150 210 Q110 140 160 90 Q200 60 175 40" stroke="#FF8FB1" stroke-width="24" fill="none" stroke-linecap="round"/>
<circle cx="165" cy="40" r="30" fill="#FF8FB1" {SW}/><path d="M140 45 Q110 60 125 85 Q135 70 150 62 Z" fill="#3A3A44" {SW}/>{eyes(172, 172, 34, 7)}'''
I["cheetah"] = f'''{legs4((125, 165, 275, 310), 255, 370, "#F2C14E", 24)}<path d="M320 230 Q385 230 380 170" stroke="{INK}" stroke-width="20" fill="none"/><path d="M320 230 Q385 230 380 170" stroke="#F2C14E" stroke-width="10" fill="none"/>
<ellipse cx="220" cy="235" rx="120" ry="45" fill="#F2C14E" {SW}/>{"".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{INK}"/>' for x, y in ((170, 220), (200, 245), (235, 215), (265, 245), (295, 225), (185, 260), (250, 260)))}
<circle cx="115" cy="190" r="52" fill="#F2C14E" {SW}/><circle cx="80" cy="148" r="14" fill="#F2C14E" {SW}/><circle cx="150" cy="148" r="14" fill="#F2C14E" {SW}/>
{eyes(98, 132, 182, 9)}<path d="M98 192 L92 225 M132 192 L138 225" stroke="{INK}" stroke-width="5"/><ellipse cx="115" cy="210" rx="10" ry="7" fill="{INK}"/>{smile(115, 222, 10)}'''
I["camel"] = f'''{legs4((140, 175, 260, 295), 260, 380, "#D9A066", 24)}<ellipse cx="220" cy="245" rx="110" ry="45" fill="#D9A066" {SW}/>
<path d="M150 230 Q180 130 220 225 Q260 130 290 230" fill="#D9A066" {SW}/>
<path d="M120 240 Q90 170 110 120" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M120 240 Q90 170 110 120" stroke="#D9A066" stroke-width="30" fill="none" stroke-linecap="round"/>
<ellipse cx="90" cy="110" rx="48" ry="30" fill="#D9A066" {SW}/>{eyes(98, 98, 98, 8)}<ellipse cx="55" cy="115" rx="6" ry="4" fill="{INK}"/>{smile(70, 125, 10)}'''
I["koala"] = f'''<path d="M60 380 L340 380" stroke="#8A5A2B" stroke-width="30" stroke-linecap="round"/>
<ellipse cx="200" cy="270" rx="95" ry="95" fill="#A7B0C0" {SW}/><ellipse cx="200" cy="290" rx="55" ry="60" fill="#E4E8EF"/>
<circle cx="200" cy="140" r="75" fill="#A7B0C0" {SW}/><circle cx="125" cy="105" r="42" fill="#A7B0C0" {SW}/><circle cx="275" cy="105" r="42" fill="#A7B0C0" {SW}/>
<circle cx="125" cy="105" r="24" fill="#FFFFFF"/><circle cx="275" cy="105" r="24" fill="#FFFFFF"/>{eyes(175, 225, 130, 9)}
<ellipse cx="200" cy="160" rx="22" ry="28" fill="#3A3A44"/>{cheeks(160, 240, 165)}'''
I["wolf"] = f'''{legs4((140, 175, 265, 300), 260, 365, "#8E97A8", 26)}<path d="M320 230 Q385 230 370 160" stroke="{INK}" stroke-width="34" fill="none"/><path d="M320 230 Q385 230 370 160" stroke="#A7B0C0" stroke-width="22" fill="none"/>
<ellipse cx="225" cy="240" rx="110" ry="55" fill="#A7B0C0" {SW}/>
<path d="M60 170 L120 110 L140 60 L160 115 L190 120 L210 70 L215 130 L200 220 Q120 240 60 170 Z" fill="#A7B0C0" {SW}/>
<path d="M60 170 Q90 200 130 195 Q110 175 120 160 Z" fill="#E4E8EF"/>{eyes(130, 175, 150, 8)}<circle cx="62" cy="170" r="9" fill="{INK}"/>'''

BG = {}
BG["desert"] = f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD58F"/><stop offset="1" stop-color="#FFF1D6"/></linearGradient></defs>
  <rect width="1920" height="1080" fill="url(#sk)"/><circle cx="1600" cy="220" r="120" fill="#FFB347" {SW}/>
  <path d="M0 640 Q300 520 620 620 Q900 520 1260 620 Q1600 540 1920 620 L1920 1080 L0 1080 Z" fill="#F2C97A" {SW}/>
  <path d="M0 780 Q500 700 1000 780 Q1500 850 1920 760 L1920 1080 L0 1080 Z" fill="#E8B964"/>
  <path d="M300 640 L300 470 Q300 440 325 440 Q350 440 350 470 L350 640 M300 540 L260 540 L260 500 M350 520 L390 520 L390 480" stroke="#5DBB46" stroke-width="30" fill="none" stroke-linecap="round"/>'''
BG["forest"] = f'''<rect width="1920" height="1080" fill="#CFEFD0"/>
  {"".join(f'<path d="M{x} 760 L{x - 140} 760 L{x} 260 L{x + 140} 760 Z" fill="{c}" {SW}/><rect x="{x - 20}" y="760" width="40" height="70" fill="#8A5A2B"/>' for x, c in ((180, "#3E9B4B"), (520, "#4CAF50"), (1420, "#3E9B4B"), (1760, "#4CAF50")))}
  <rect x="0" y="800" width="1920" height="280" fill="#7ED957"/><path d="M0 800 L1920 800" stroke="{INK}" stroke-width="5"/>
  {"".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/>' for x, y, c in ((300, 900, "#FF6B8B"), (900, 980, "#FFD23F"), (1300, 920, "#FFFFFF"), (1650, 1000, "#B79BEA")))}'''
BG["outback"] = f'''<rect width="1920" height="1080" fill="#FFD9A0"/><circle cx="300" cy="220" r="110" fill="#FF9F1C" {SW}/>
  <path d="M0 660 Q500 600 1000 660 Q1500 720 1920 640 L1920 1080 L0 1080 Z" fill="#E8935A" {SW}/>
  <path d="M1350 640 Q1300 450 1380 300 M1380 300 Q1250 250 1200 300 M1380 300 Q1480 230 1560 300" stroke="#8A5A2B" stroke-width="28" fill="none" stroke-linecap="round"/>
  {"".join(f'<ellipse cx="{x}" cy="{y}" rx="90" ry="50" fill="#7BAE3F" {SW}/>' for x, y in ((1200, 290), (1380, 250), (1560, 290)))}'''


def render():
    names = list(I)
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 -20 400 420">{I[n]}</svg></div>'
                    for i, n in enumerate(names))
    w = 400 * len(names)
    A.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>', str(OUT / "_items.png"), w, 400, scale=2)
    im = Image.open(OUT / "_items.png")
    for i, n in enumerate(names):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_{n}.png")
    (OUT / "_items.png").unlink()
    for k, svg in BG.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>', str(OUT / f"bg_{k}.png"), 1920, 1080)
    sheet = Image.new("RGBA", (180 * 8, 180 * 2 + 220), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((170, 170)), ((i % 8) * 180, (i // 8) * 180))
    for j, k in enumerate(BG):
        sheet.alpha_composite(Image.open(OUT / f"bg_{k}.png").convert("RGBA").resize((360, 200)), (j * 380, 370))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "animals +", len(BG), "bgs")


if __name__ == "__main__":
    render()
