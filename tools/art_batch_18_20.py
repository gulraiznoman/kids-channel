"""Art for L18 Days of the Week, L19 Santa & Christmas Eve, L20 Cooking for Kids.
python tools/art_batch_18_20.py -> long18-days/art, long19-santa/art, long20-cooking/art (+ tools/_sheet_18_20.png)
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


SETS = {}
# ------------------------------------------------------------------ L18 days of the week
D = {}
D["calendar"] = f'''<rect x="50" y="70" width="300" height="290" rx="20" fill="#FFFFFF" {SW}/><rect x="50" y="70" width="300" height="80" rx="20" fill="#FF4D6D" {SW}/>
<rect x="110" y="40" width="22" height="60" rx="10" fill="#C9CCD6" {SW}/><rect x="268" y="40" width="22" height="60" rx="10" fill="#C9CCD6" {SW}/>
{"".join(f'<rect x="{75 + (i % 7) * 38}" y="{175 + (i // 7) * 42}" width="30" height="32" rx="6" fill="{"#FFD23F" if i == 9 else "#F2F4F8"}" stroke="{INK}" stroke-width="3"/>' for i in range(28))}'''
D["swimring"] = f'''<circle cx="200" cy="200" r="150" fill="#FF6B8B" {SW}/><circle cx="200" cy="200" r="70" fill="#9ED8FF" {SW}/>
{"".join(f'<path d="M{200 + 75 * __import__("math").cos(a)} {200 + 75 * __import__("math").sin(a)} L{200 + 145 * __import__("math").cos(a)} {200 + 145 * __import__("math").sin(a)}" stroke="#FFFFFF" stroke-width="34"/>' for a in (0.4, 2.0, 3.6, 5.2))}'''
D["house"] = f'''<rect x="80" y="180" width="240" height="190" fill="#FFB3C7" {SW}/><path d="M50 190 L200 60 L350 190 Z" fill="#E8573C" {SW}/>
<rect x="175" y="270" width="55" height="100" rx="8" fill="#8A5A2B" {SW}/><rect x="105" y="215" width="55" height="50" fill="#9ED8FF" {SW}/><rect x="245" y="215" width="55" height="50" fill="#9ED8FF" {SW}/>
<path d="M200 140 Q185 120 195 108 Q205 100 210 112 Q215 100 225 108 Q235 120 220 140 Q210 150 200 140 Z" fill="#FF4D6D"/>'''
D["paint"] = f'''<rect x="60" y="80" width="280" height="240" rx="12" fill="#FFFFFF" {SW}/><circle cx="150" cy="170" r="40" fill="#FFD23F"/>
<path d="M60 280 Q200 200 340 280 L340 320 L60 320 Z" fill="#7ED957"/><path d="M220 230 L250 150 L280 230 Z" fill="#FF6B6B"/>
<path d="M330 330 L380 380" stroke="#8A5A2B" stroke-width="14" stroke-linecap="round"/><path d="M312 312 L340 340" stroke="#4CC9F0" stroke-width="22" stroke-linecap="round"/>'''
SETS["long18-days"] = (D, {})

# ------------------------------------------------------------------ L19 santa
S = {}
S["santa"] = f'''<path d="M120 380 L130 300 L270 300 L280 380 Z" fill="#2B2B33" {SW}/>
<path d="M100 320 Q90 180 200 170 Q310 180 300 320 Z" fill="#E8352E" {SW}/><rect x="98" y="270" width="204" height="34" fill="#2B2B33" {SW}/>
<rect x="180" y="268" width="40" height="38" rx="6" fill="#FFD23F" {SW}/><path d="M200 175 L200 320" stroke="#FFFFFF" stroke-width="22"/>
<path d="M100 210 Q60 250 75 300" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M100 210 Q60 250 75 300" stroke="#E8352E" stroke-width="28" fill="none" stroke-linecap="round"/>
<path d="M300 210 Q350 170 345 120" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M300 210 Q350 170 345 120" stroke="#E8352E" stroke-width="28" fill="none" stroke-linecap="round"/>
<circle cx="345" cy="110" r="22" fill="#FFFFFF" {SW}/><circle cx="75" cy="305" r="22" fill="#FFFFFF" {SW}/>
<path d="M120 150 Q120 260 200 265 Q280 260 280 150 Z" fill="#FFFFFF" {SW}/><circle cx="200" cy="120" r="62" fill="#F2C29B" {SW}/>
<circle cx="160" cy="130" r="13" fill="#FF9FB0"/><circle cx="240" cy="130" r="13" fill="#FF9FB0"/>
<path d="M142 120 Q128 225 200 248 Q272 225 258 120 Q245 165 200 165 Q155 165 142 120 Z" fill="#FFFFFF" {SW}/>
<ellipse cx="200" cy="160" rx="13" ry="9" fill="#B03030" stroke="{INK}" stroke-width="4"/>
<ellipse cx="178" cy="145" rx="26" ry="13" fill="#FFFFFF" {SW}/><ellipse cx="222" cy="145" rx="26" ry="13" fill="#FFFFFF" {SW}/>
<circle cx="200" cy="130" r="13" fill="#FF8FA3" stroke="{INK}" stroke-width="4"/>{eyes(178, 222, 105, 9)}
<path d="M135 85 Q170 10 260 40 Q290 55 275 95 Z" fill="#E8352E" {SW}/><rect x="125" y="78" width="160" height="30" rx="14" fill="#FFFFFF" {SW}/><circle cx="285" cy="40" r="18" fill="#FFFFFF" {SW}/>'''
S["reindeer"] = f'''<rect x="140" y="250" width="24" height="120" rx="12" fill="#8A5A33" {SW}/><rect x="185" y="255" width="24" height="115" rx="12" fill="#8A5A33" {SW}/>
<rect x="260" y="250" width="24" height="120" rx="12" fill="#8A5A33" {SW}/><rect x="300" y="245" width="24" height="125" rx="12" fill="#8A5A33" {SW}/>
<ellipse cx="235" cy="240" rx="115" ry="55" fill="#A8743F" {SW}/><path d="M340 230 Q370 210 360 190" stroke="{INK}" stroke-width="16" fill="none"/>
<path d="M150 230 Q120 170 130 120" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M150 230 Q120 170 130 120" stroke="#A8743F" stroke-width="30" fill="none" stroke-linecap="round"/>
<ellipse cx="120" cy="105" rx="55" ry="42" fill="#A8743F" {SW}/><circle cx="72" cy="112" r="14" fill="#2B2B33"/>{eyes(110, 145, 92, 8)}
<path d="M110 70 L90 20 M100 45 L70 40 M140 68 L160 18 M150 45 L180 38" stroke="#8A5A33" stroke-width="10" stroke-linecap="round"/>
<path d="M170 215 Q200 250 230 215" stroke="#E8352E" stroke-width="12" fill="none"/><circle cx="200" cy="245" r="10" fill="#FFD23F" stroke="{INK}" stroke-width="3"/>'''
S["sleigh"] = f'''<path d="M60 320 Q40 320 50 345 L340 345 Q380 345 375 300" stroke="#C8A040" stroke-width="16" fill="none" stroke-linecap="round"/>
<path d="M70 300 L90 160 L170 160 L180 220 L330 220 L340 300 Z" fill="#E8352E" {SW}/><path d="M90 175 Q60 160 70 120 Q100 130 110 165" fill="#E8352E" {SW}/>
<path d="M100 300 L110 330 M300 300 L310 330" stroke="#C8A040" stroke-width="12"/><path d="M100 250 L320 250" stroke="#FFD23F" stroke-width="10"/>
<rect x="190" y="150" width="70" height="70" rx="8" fill="#4CC9F0" {SW}/><rect x="250" y="120" width="70" height="100" rx="8" fill="#7ED957" {SW}/>
<path d="M190 185 L260 185 M225 150 L225 220 M250 170 L320 170 M285 120 L285 220" stroke="#FFFFFF" stroke-width="8"/>'''
S["letter"] = f'''<rect x="60" y="110" width="280" height="190" rx="12" fill="#FFFFFF" {SW}/><path d="M60 110 L200 220 L340 110" fill="none" stroke="{INK}" stroke-width="6"/>
<path d="M200 230 Q185 210 195 198 Q205 190 210 202 Q215 190 225 198 Q235 210 220 230 Q210 240 200 230 Z" fill="#E8352E"/>
<rect x="270" y="130" width="50" height="60" fill="#7ED957" stroke="{INK}" stroke-width="4"/>'''
S["chimney"] = f'''<rect x="120" y="120" width="160" height="250" fill="#C9502E" {SW}/>{"".join(f'<path d="M120 {y} L280 {y}" stroke="#8A3F2B" stroke-width="5"/>' for y in range(170, 370, 50))}
{"".join(f'<path d="M{x} {y} L{x} {y + 50}" stroke="#8A3F2B" stroke-width="5"/>' for x, y in ((200, 120), (160, 170), (240, 170), (200, 220), (160, 270), (240, 270), (200, 320)))}
<rect x="100" y="90" width="200" height="40" fill="#C9502E" {SW}/><path d="M100 90 Q200 60 300 90" fill="#FFFFFF" {SW}/>'''
S["milk"] = f'''<path d="M130 100 L270 100 L255 350 L145 350 Z" fill="#FFFFFF" {SW}/><path d="M138 160 L262 160 L255 350 L145 350 Z" fill="#E9F2FF"/>
<ellipse cx="200" cy="100" rx="70" ry="14" fill="#FFFFFF" {SW}/>'''
S["toytrain"] = f'''<rect x="40" y="200" width="120" height="100" rx="12" fill="#4CC9F0" {SW}/><rect x="170" y="160" width="180" height="140" rx="14" fill="#FF6B6B" {SW}/>
<rect x="200" y="185" width="60" height="50" fill="#9ED8FF" {SW}/><rect x="300" y="110" width="30" height="55" fill="#2B2B33" {SW}/>
{"".join(f'<circle cx="{x}" cy="310" r="32" fill="#2B2B33" {SW}/>' for x in (80, 130, 220, 300))}'''
SETS["long19-santa"] = (S, {
    "northpole": f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9D8FF"/><stop offset="1" stop-color="#EAF6FF"/></linearGradient></defs>
  <rect width="1920" height="1080" fill="url(#sk)"/>
  <path d="M0 640 Q480 560 960 620 Q1440 680 1920 600 L1920 1080 L0 1080 Z" fill="#FFFFFF" {SW}/>
  <rect x="1180" y="300" width="560" height="380" fill="#C9502E" {SW}/><path d="M1140 310 L1460 120 L1780 310 Z" fill="#7A3E1E" {SW}/>
  <path d="M1140 310 Q1460 270 1780 310 L1780 340 Q1460 300 1140 340 Z" fill="#FFFFFF" {SW}/>
  <rect x="1410" y="490" width="110" height="190" rx="10" fill="#8A5A2B" {SW}/><rect x="1240" y="400" width="110" height="90" fill="#FFE27A" {SW}/><rect x="1580" y="400" width="110" height="90" fill="#FFE27A" {SW}/>
  <rect x="1300" y="210" width="320" height="60" rx="12" fill="#FFFFFF" {SW}/>
  <path d="M300 640 L300 380" stroke="#C9CCD6" stroke-width="22"/>{"".join(f'<path d="M300 {y} L300 {y + 30}" stroke="#E8352E" stroke-width="22"/>' for y in range(390, 640, 60))}
  <circle cx="300" cy="370" r="24" fill="#FFD23F" {SW}/>
  {"".join(f'<path d="M{x} 640 L{x - 60} 640 L{x} 470 L{x + 60} 640 Z" fill="#2E9E4A" {SW}/>' for x in (560, 700, 860))}''',
    "roof": f'''<rect width="1920" height="1080" fill="#1E2A5E"/>
  <circle cx="1650" cy="180" r="90" fill="#FFF3B0" {SW}/>
  {"".join(f'<circle cx="{(i * 271) % 1920}" cy="{(i * 113) % 560}" r="4" fill="#FFFFFF"/>' for i in range(70))}
  {"".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1080 - y}" fill="{c}" {SW}/><path d="M{x - 20} {y} L{x + w / 2} {y - 120} L{x + w + 20} {y} Z" fill="#7A3E1E" {SW}/><path d="M{x - 20} {y} Q{x + w / 2} {y - 30} {x + w + 20} {y}" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>' + "".join(f'<rect x="{x + 30 + j * 80}" y="{y + 60}" width="50" height="50" fill="#FFE27A" stroke="{INK}" stroke-width="4"/>' for j in range(int((w - 30) / 80))) for x, y, w, c in ((0, 760, 360, "#8C6A9E"), (420, 700, 420, "#4E7FB5"), (900, 780, 380, "#6E9E5A"), (1340, 720, 440, "#B5604E")))}'''})

# ------------------------------------------------------------------ L20 cooking
C = {}
C["chefhat"] = f'''<rect x="110" y="250" width="180" height="90" rx="10" fill="#FFFFFF" {SW}/>
<path d="M110 260 Q50 250 60 180 Q70 120 140 130 Q150 60 220 70 Q290 70 290 140 Q350 130 345 200 Q340 255 290 260 Z" fill="#FFFFFF" {SW}/>'''
C["apron"] = f'''<path d="M130 60 L270 60 L270 140 Q340 160 330 360 L70 360 Q60 160 130 140 Z" fill="#FF8FB1" {SW}/><path d="M130 60 Q200 20 270 60" stroke="{INK}" stroke-width="6" fill="none"/>
<rect x="140" y="220" width="120" height="80" rx="10" fill="#FFD23F" {SW}/>'''
C["rollingpin"] = f'''<rect x="90" y="160" width="220" height="80" rx="36" fill="#E8B77E" {SW}/><rect x="20" y="182" width="80" height="36" rx="18" fill="#C9954A" {SW}/><rect x="300" y="182" width="80" height="36" rx="18" fill="#C9954A" {SW}/>'''
C["whisk"] = f'''<path d="M200 380 L200 230" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M200 380 L200 230" stroke="#FF6B6B" stroke-width="18" stroke-linecap="round"/>
{"".join(f'<path d="M200 235 Q{200 + dx} 140 200 40 Q{200 - dx} 140 200 235" stroke="#9AA0AE" stroke-width="7" fill="none"/>' for dx in (30, 60, 90))}'''
C["mitt"] = f'''<path d="M120 380 L120 180 Q120 80 200 80 Q280 80 280 180 L280 260 Q340 230 340 290 Q330 330 280 340 L280 380 Z" fill="#4CC9F0" {SW}/>
<rect x="110" y="330" width="180" height="50" rx="12" fill="#FFFFFF" {SW}/>{"".join(f'<circle cx="{x}" cy="{y}" r="10" fill="#FFFFFF"/>' for x, y in ((170, 160), (230, 200), (180, 260)))}'''
C["flour"] = f'''<path d="M100 120 L300 120 L320 360 L80 360 Z" fill="#F2E6C9" {SW}/><path d="M100 120 Q200 70 300 120" fill="#F2E6C9" {SW}/>
<rect x="130" y="200" width="140" height="90" rx="10" fill="#FFFFFF" {SW}/><path d="M160 260 Q200 210 240 260" stroke="#E8B964" stroke-width="10" fill="none"/>'''
C["cheese"] = f'''<path d="M50 300 L350 300 L350 200 L120 130 Z" fill="#FFD23F" {SW}/><path d="M50 300 L120 130 L350 200" fill="none" stroke="{INK}" stroke-width="5"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E8B000"/>' for x, y, r in ((150, 250, 18), (240, 270, 14), (300, 235, 12), (190, 210, 10)))}'''
C["sauce"] = f'''<rect x="120" y="110" width="160" height="250" rx="30" fill="#E8352E" {SW}/><rect x="140" y="70" width="120" height="50" rx="10" fill="#7ED957" {SW}/>
<rect x="140" y="190" width="120" height="90" rx="10" fill="#FFFFFF" {SW}/><circle cx="200" cy="235" r="28" fill="#E8352E"/>'''
C["olive"] = f'''<ellipse cx="200" cy="200" rx="130" ry="100" fill="#3A3A44" {SW}/><ellipse cx="200" cy="200" rx="50" ry="38" fill="#C9CCD6" {SW}/>'''
C["pepper"] = f'''<path d="M200 90 Q320 80 320 220 Q320 350 200 350 Q80 350 80 220 Q80 80 200 90 Z" fill="#7ED957" {SW}/><path d="M200 90 L215 40" stroke="#4E9A35" stroke-width="16" stroke-linecap="round"/>'''
C["mushroom"] = f'''<path d="M60 220 Q60 90 200 80 Q340 90 340 220 Z" fill="#C8894E" {SW}/><rect x="160" y="210" width="80" height="130" rx="30" fill="#F2E6C9" {SW}/>
{"".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#F2E6C9"/>' for x, y in ((140, 150), (220, 130), (270, 180)))}'''
C["blender"] = f'''<path d="M120 60 L280 60 L260 260 L140 260 Z" fill="#E9F6FF" {SW}/><path d="M138 160 L262 160 L258 255 L142 255 Z" fill="#FF8FB1"/>
<rect x="110" y="40" width="180" height="30" rx="10" fill="#2B2B33" {SW}/><path d="M120 260 L280 260 L300 370 L100 370 Z" fill="#4CC9F0" {SW}/>
<circle cx="200" cy="320" r="22" fill="#FFFFFF" {SW}/>'''
C["smoothie"] = f'''<path d="M120 100 L280 100 L255 370 L145 370 Z" fill="#FF8FB1" {SW}/><ellipse cx="200" cy="100" rx="80" ry="16" fill="#FFB3C7" {SW}/>
<path d="M230 20 L210 230" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M230 20 L210 230" stroke="#4CC9F0" stroke-width="12" stroke-linecap="round"/>
<circle cx="275" cy="105" r="30" fill="#E8352E" {SW}/>'''
C["skewer"] = f'''<path d="M30 200 L370 200" stroke="#C9954A" stroke-width="10" stroke-linecap="round"/>
{"".join(f'<circle cx="{x}" cy="200" r="34" fill="{c}" {SW}/>' for x, c in ((80, "#E8352E"), (150, "#FF9F1C"), (220, "#FFD23F"), (290, "#7ED957"), (350, "#9B5DE5")))}'''
C["oven"] = f'''<rect x="50" y="60" width="300" height="310" rx="20" fill="#C9CCD6" {SW}/><rect x="80" y="150" width="240" height="190" rx="14" fill="#3A3D46" {SW}/>
<rect x="100" y="170" width="200" height="150" rx="10" fill="#FF9F1C" opacity="0.6"/>{"".join(f'<circle cx="{x}" cy="105" r="16" fill="#FFFFFF" {SW}/>' for x in (120, 180, 240, 290))}
<rect x="110" y="135" width="180" height="14" rx="7" fill="#9AA0AE"/>'''
C["knife"] = f'''<path d="M60 230 L250 170 Q330 160 350 200 L250 240 Z" fill="#DDE2EA" {SW}/><rect x="20" y="215" width="110" height="50" rx="20" fill="#2B2B33" {SW} transform="rotate(-17 75 240)"/>'''
C["fridge"] = f'''<rect x="90" y="20" width="220" height="370" rx="24" fill="#E9F6FF" {SW}/><path d="M90 150 L310 150" stroke="{INK}" stroke-width="6"/>
<rect x="270" y="60" width="14" height="60" rx="7" fill="#9AA0AE"/><rect x="270" y="190" width="14" height="80" rx="7" fill="#9AA0AE"/>
<circle cx="150" cy="210" r="16" fill="#FF6B6B"/><rect x="180" y="240" width="40" height="30" fill="#FFD23F" stroke="{INK}" stroke-width="3"/>'''
SETS["long20-cooking"] = (C, {})


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
    sheet.save(ROOT / "tools" / "_sheet_18_20.png")
    print("done")


if __name__ == "__main__":
    render()
