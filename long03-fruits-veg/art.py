"""New art for Long video 3 (fruits & vegetables): fruits + cut-open halves, vegetables, props, backgrounds.

python art.py -> art/item_<key>.png (800x800) and art/bg_<name>.png (1920x1080), plus _sheet.png preview
Plain food drawings (no faces), same thick-outline style as Ep1 fruits.
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
LEAF = lambda x, y, rot, c="#5DBB46": f'<path d="M{x} {y} q30 -40 75 -20 q-30 40 -75 20 Z" fill="{c}" {SW} transform="rotate({rot} {x} {y})"/>'
STEM = lambda x, y: f'<path d="M{x} {y} q-4 -30 10 -50" stroke="#6B4423" stroke-width="12" fill="none" stroke-linecap="round"/>'

I = {}
# ------------------------------------------------------------------ new fruits
I["guava"] = f'''<circle cx="200" cy="215" r="135" fill="#9ACD32" {SW}/>{STEM(200, 85)}{LEAF(205, 75, -10)}
<circle cx="150" cy="250" r="9" fill="#7FB02A"/><circle cx="250" cy="200" r="7" fill="#7FB02A"/><circle cx="230" cy="290" r="8" fill="#7FB02A"/>
{SHINE(140, 160, 34, 18)}'''
I["guava_half"] = f'''<circle cx="200" cy="215" r="140" fill="#9ACD32" {SW}/><circle cx="200" cy="215" r="118" fill="#FF8FA3"/>
<circle cx="200" cy="215" r="62" fill="#FF6F8E"/>''' + "".join(
    f'<ellipse cx="{200 + 40 * __import__("math").cos(a / 8 * 6.283):.0f}" cy="{215 + 40 * __import__("math").sin(a / 8 * 6.283):.0f}" rx="7" ry="10" fill="#FFF3C4" {SW.replace("6", "3")}/>'
    for a in range(8))
I["pomegranate"] = f'''<circle cx="200" cy="225" r="135" fill="#D7263D" {SW}/>
<path d="M165 95 L172 60 L190 85 L200 52 L210 85 L228 60 L235 95 Z" fill="#B01E33" {SW}/>{SHINE(140, 170, 36, 18)}'''
I["pomegranate_half"] = f'''<circle cx="200" cy="225" r="140" fill="#D7263D" {SW}/><circle cx="200" cy="225" r="118" fill="#FFE6D5"/>''' + "".join(
    f'<ellipse cx="{x}" cy="{y}" rx="13" ry="16" fill="#E8354E" stroke="#8E1525" stroke-width="3"/>'
    for x in range(120, 290, 30) for y in range(150, 310, 32) if (x - 200) ** 2 + (y - 225) ** 2 < 100 ** 2)
I["papaya"] = f'''<ellipse cx="200" cy="215" rx="98" ry="165" fill="#FFC24A" {SW}/>
<path d="M200 50 Q120 60 108 200 Q140 120 200 95 Q260 120 292 200 Q280 60 200 50 Z" fill="#7CB342" opacity="0.85"/>
<path d="M150 110 Q130 220 160 360 M250 110 Q270 220 240 360" stroke="#E8A12E" stroke-width="6" fill="none"/>{STEM(200, 52)}{SHINE(160, 170, 18, 40)}'''
I["papaya_half"] = f'''<ellipse cx="200" cy="210" rx="115" ry="165" fill="#FFC24A" {SW} transform="rotate(-25 200 210)"/>
<ellipse cx="200" cy="210" rx="98" ry="148" fill="#FF8C42" transform="rotate(-25 200 210)"/>
<ellipse cx="200" cy="210" rx="40" ry="80" fill="#FFB067" transform="rotate(-25 200 210)"/>''' + "".join(
    f'<circle cx="{200 + dx}" cy="{210 + dy}" r="9" fill="#2B1B17"/>' for dx, dy in
    ((-10, -50), (8, -30), (-12, -10), (10, 10), (-8, 30), (12, 50), (-20, 20), (20, -20), (0, -70), (0, 70)))
I["peach"] = f'''<circle cx="200" cy="225" r="135" fill="#FFB38A" {SW}/><path d="M200 95 Q170 220 210 355" stroke="#F08A62" stroke-width="8" fill="none"/>
<circle cx="250" cy="200" r="70" fill="#FF8C7A" opacity="0.5"/>{STEM(200, 95)}{LEAF(208, 72, 0)}{SHINE(140, 170, 30, 16)}'''
I["peach_half"] = f'''<circle cx="200" cy="225" r="140" fill="#FFB38A" {SW}/><circle cx="200" cy="225" r="120" fill="#FFD27A"/>
<ellipse cx="200" cy="225" rx="48" ry="62" fill="#B5543A" {SW}/><path d="M185 190 Q200 225 185 260 M215 190 Q200 225 215 260" stroke="#8A3B28" stroke-width="5" fill="none"/>'''
I["coconut"] = f'''<circle cx="200" cy="215" r="140" fill="#8B5A2B" {SW}/>''' + "".join(
    f'<path d="M{x} {y} l18 10" stroke="#5E3A17" stroke-width="5" stroke-linecap="round"/>'
    for x, y in ((110, 160), (150, 120), (240, 130), (280, 190), (120, 260), (260, 280), (200, 320), (170, 200))) + \
    '<circle cx="175" cy="110" r="10" fill="#4A2C12"/><circle cx="205" cy="102" r="10" fill="#4A2C12"/><circle cx="192" cy="130" r="10" fill="#4A2C12"/>'
I["coconut_half"] = f'''<circle cx="200" cy="215" r="140" fill="#8B5A2B" {SW}/><circle cx="200" cy="215" r="110" fill="#FFFFFF" {SW}/>
<circle cx="200" cy="215" r="80" fill="#EAF6FF"/>'''
I["blueberries"] = "".join(
    f'<circle cx="{x}" cy="{y}" r="58" fill="#3F5BD9" {SW}/><path d="M{x - 14} {y - 30} l14 10 l14 -10" stroke="#2A3C99" stroke-width="7" fill="none"/>'
    f'{SHINE(x - 22, y - 10, 12, 6)}' for x, y in ((140, 270), (260, 270), (200, 175), (310, 175), (95, 170)))
I["plum"] = f'''<ellipse cx="200" cy="225" rx="128" ry="138" fill="#7B3F99" {SW}/><path d="M200 95 Q180 220 205 360" stroke="#5E2D78" stroke-width="7" fill="none"/>
{STEM(200, 92)}{LEAF(208, 72, -5)}{SHINE(140, 170, 30, 16)}'''
I["avocado"] = f'''<path d="M200 50 Q270 60 290 200 Q330 360 200 365 Q70 360 110 200 Q130 60 200 50 Z" fill="#3E7D2E" {SW}/>{SHINE(160, 150, 26, 14)}'''
I["avocado_half"] = f'''<path d="M200 50 Q270 60 290 200 Q330 360 200 365 Q70 360 110 200 Q130 60 200 50 Z" fill="#3E7D2E" {SW}/>
<path d="M200 70 Q258 80 274 200 Q306 345 200 348 Q94 345 126 200 Q142 80 200 70 Z" fill="#D8EB8C"/>
<circle cx="200" cy="250" r="58" fill="#8A5A34" {SW}/>{SHINE(185, 230, 14, 8)}'''

# ------------------------------------------------------------------ vegetables
I["carrot"] = f'''<path d="M160 120 L240 120 L205 370 Z" fill="#FF8C1A" {SW}/>
<path d="M175 170 l25 0 M182 230 l22 0 M190 290 l15 0" stroke="#D96A00" stroke-width="7" stroke-linecap="round"/>
<path d="M200 120 q-60 -60 -50 -95 q35 10 50 80 q10 -75 45 -85 q15 40 -45 100 Z" fill="#4CAF50" {SW}/>'''
I["potato"] = f'''<ellipse cx="200" cy="215" rx="155" ry="118" fill="#C9A06A" {SW} transform="rotate(-10 200 215)"/>''' + "".join(
    f'<ellipse cx="{x}" cy="{y}" rx="9" ry="6" fill="#9C7442"/>' for x, y in ((120, 190), (190, 150), (260, 200), (170, 270), (290, 260), (230, 300)))
I["onion"] = f'''<path d="M200 70 Q215 110 270 150 Q340 230 280 320 Q200 380 120 320 Q60 230 130 150 Q185 110 200 70 Z" fill="#B5527A" {SW}/>
<path d="M200 100 Q160 200 200 340 M200 100 Q240 200 200 340" stroke="#8E3A5C" stroke-width="6" fill="none"/>
<path d="M175 345 l-10 30 M200 350 l0 32 M225 345 l10 30" stroke="#C9B48A" stroke-width="6" stroke-linecap="round"/>{SHINE(150, 220, 22, 12)}'''
I["broccoli"] = f'''<path d="M175 230 L165 360 L235 360 L225 230 Z" fill="#9CCC65" {SW}/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2E8B3E" {SW}/>' for x, y, r in
    ((120, 190, 62), (280, 190, 62), (200, 140, 72), (160, 220, 55), (240, 220, 55), (200, 210, 50)))
I["corn"] = f'''<path d="M200 50 Q290 90 280 230 Q270 340 200 365 Q130 340 120 230 Q110 90 200 50 Z" fill="#FFD23F" {SW}/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="11" fill="#F5B700"/>' for x in range(150, 260, 26) for y in range(100, 340, 28)
    if abs(x - 200) < 70 - abs(y - 210) * 0.2) + f'''
<path d="M200 365 Q100 330 70 160 Q130 250 200 300 Z" fill="#7CC444" {SW}/><path d="M200 365 Q300 330 330 160 Q270 250 200 300 Z" fill="#6BB33A" {SW}/>'''
I["peas"] = f'''<path d="M60 250 Q200 120 350 200 Q330 260 200 290 Q100 310 60 250 Z" fill="#5DBB46" {SW}/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="27" fill="#8BD86A" {SW}/>' for x, y in ((115, 250), (170, 238), (225, 228), (280, 220))) + \
    '<path d="M350 200 q20 -30 0 -60" stroke="#4CAF50" stroke-width="8" fill="none" stroke-linecap="round"/>'
I["tomato"] = f'''<circle cx="200" cy="225" r="140" fill="#E8352E" {SW}/>
<path d="M200 95 L215 125 L250 110 L230 140 L265 155 L225 160 L200 185 L175 160 L135 155 L170 140 L150 110 L185 125 Z" fill="#4CAF50" {SW}/>{SHINE(135, 190, 34, 18)}'''
I["cucumber"] = f'''<rect x="60" y="150" width="290" height="110" rx="55" fill="#3E8E41" {SW} transform="rotate(-20 205 205)"/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="6" fill="#9CCC65"/>' for x, y in ((110, 250), (170, 220), (230, 195), (290, 170), (140, 210), (260, 220)))
I["eggplant"] = f'''<path d="M150 120 Q290 110 300 260 Q300 370 200 360 Q110 350 130 250 Q140 180 150 120 Z" fill="#6A2C91" {SW}/>
<path d="M120 120 Q160 80 230 105 L210 140 L170 130 L140 150 Z" fill="#4CAF50" {SW}/><path d="M175 95 q-5 -40 25 -55" stroke="#4CAF50" stroke-width="14" fill="none" stroke-linecap="round"/>
{SHINE(190, 190, 22, 40)}'''
I["cabbage"] = f'''<circle cx="200" cy="220" r="145" fill="#A5D66F" {SW}/><circle cx="200" cy="225" r="105" fill="#C5E59A" {SW}/>
<path d="M200 120 Q170 220 200 330 M140 150 Q120 230 160 310 M260 150 Q280 230 240 310" stroke="#86B85A" stroke-width="7" fill="none"/>'''
I["pumpkinveg"] = f'''<path d="M190 120 Q186 82 206 62 Q218 56 222 66 Q206 84 212 120 Z" fill="#6B8E23" {SW}/>
<ellipse cx="130" cy="235" rx="95" ry="120" fill="#FF9A2E" {SW}/><ellipse cx="270" cy="235" rx="95" ry="120" fill="#FF9A2E" {SW}/>
<ellipse cx="200" cy="235" rx="80" ry="128" fill="#FFA940" {SW}/>'''

# ------------------------------------------------------------------ props
I["basket"] = f'''<path d="M80 150 Q200 -10 320 150" stroke="#A0703C" stroke-width="18" fill="none"/>
<path d="M50 160 L350 160 L310 350 L90 350 Z" fill="#D9A55B" {SW}/>''' + "".join(
    f'<path d="M{70 + i * 4} {190 + i * 40} L{330 - i * 4} {190 + i * 40}" stroke="#B07D3A" stroke-width="6"/>' for i in range(4)) + "".join(
    f'<path d="M{x} 165 L{x + (200 - x) * 0.12:.0f} 345" stroke="#B07D3A" stroke-width="6"/>' for x in range(100, 320, 40))
I["bowl"] = f'''<path d="M40 170 L360 170 Q350 330 200 340 Q50 330 40 170 Z" fill="#4CC9F0" {SW}/><ellipse cx="200" cy="170" rx="160" ry="30" fill="#8FE0F8" {SW}/>
<path d="M90 230 Q200 260 310 230" stroke="#FFFFFF" stroke-width="10" fill="none" opacity="0.6"/>'''
I["pot"] = f'''<rect x="70" y="150" width="260" height="200" rx="30" fill="#FF6B6B" {SW}/><ellipse cx="200" cy="150" rx="140" ry="28" fill="#FFB0A0" {SW}/>
<rect x="30" y="185" width="45" height="26" rx="12" fill="#FF6B6B" {SW}/><rect x="325" y="185" width="45" height="26" rx="12" fill="#FF6B6B" {SW}/>
<path d="M150 120 q-15 -30 0 -60 M200 115 q-15 -30 0 -60 M250 120 q-15 -30 0 -60" stroke="#FFFFFF" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.8"/>'''
I["crate_fruit"] = f'''<rect x="40" y="150" width="320" height="200" rx="14" fill="#E6B26A" {SW}/>''' + "".join(
    f'<rect x="40" y="{y}" width="320" height="14" fill="#C98F45"/>' for y in (200, 250, 300)) + \
    f'<circle cx="130" cy="140" r="48" fill="#E8352E" {SW}/><circle cx="215" cy="130" r="48" fill="#FF9A2E" {SW}/><circle cx="295" cy="140" r="44" fill="#9ACD32" {SW}/>'
I["crate_veg"] = f'''<rect x="40" y="150" width="320" height="200" rx="14" fill="#E6B26A" {SW}/>''' + "".join(
    f'<rect x="40" y="{y}" width="320" height="14" fill="#C98F45"/>' for y in (200, 250, 300)) + \
    f'<path d="M100 150 L150 150 L125 70 Z" fill="#FF8C1A" {SW}/><circle cx="215" cy="125" r="45" fill="#2E8B3E" {SW}/><ellipse cx="300" cy="135" rx="50" ry="36" fill="#C9A06A" {SW}/>'

# ------------------------------------------------------------------ backgrounds (1920x1080)
SKY = A.sky_and_clouds(1920)
BGS = {
    "market": f'''{SKY}<rect y="720" width="1920" height="360" fill="#D9C2A0"/>
      <rect x="0" y="520" width="1920" height="230" fill="#C08A4D" {SW}/><rect x="0" y="520" width="1920" height="26" fill="#A06C35"/>
      {"".join(f'<path d="M{x} 200 L{x + 160} 200 L{x + 160} 300 Q{x + 120} 340 {x + 80} 300 Q{x + 40} 340 {x} 300 Z" fill="{c}" {SW}/>' for x, c in zip(range(0, 1920, 160), ["#FF6B8B", "#FFFFFF"] * 6))}
      <rect x="40" y="300" width="22" height="420" fill="#8A5A2B" {SW}/><rect x="1858" y="300" width="22" height="420" fill="#8A5A2B" {SW}/>
      {"".join(f'<rect x="{x}" y="560" width="200" height="150" rx="10" fill="#E6B26A" {SW}/>' for x in (120, 1600))}
      {"".join(f'<circle cx="{x}" cy="{y}" r="30" fill="{c}" {SW}/>' for x, y, c in ((170, 545, "#E8352E"), (230, 540, "#FF9A2E"), (290, 548, "#FFD23F"), (1650, 545, "#5DBB46"), (1710, 540, "#E8352E"), (1770, 548, "#FF8C1A")))}''',
    "patch": f'''{SKY}<rect y="560" width="1920" height="520" fill="#8DD16A"/>
      {"".join(f'<rect x="-20" y="{y}" width="1960" height="70" rx="35" fill="#8B5A2B" {SW}/>' for y in (640, 760, 880))}
      {"".join(f'<path d="M{x} {y} q-15 -40 0 -60 q15 20 0 60 M{x} {y} q20 -35 40 -40 q-5 25 -40 40" fill="#4CAF50" {SW}/>' for x in range(80, 1900, 210) for y in (650, 770) if x % 420 < 300)}
      <rect x="1720" y="420" width="18" height="160" fill="#8A5A2B"/><path d="M1650 430 L1810 430 L1790 470 L1670 470 Z" fill="#FFFFFF" {SW}/>''',
    "kitchen": f'''<rect width="1920" height="1080" fill="#FFF3D6"/>
      {"".join(f'<rect x="{x}" y="{y}" width="118" height="118" fill="{"#FFFFFF" if (x // 120 + y // 120) % 2 else "#D6F0FF"}"/>' for x in range(0, 1920, 120) for y in range(0, 600, 120))}
      <rect x="0" y="600" width="1920" height="60" fill="#C08A4D" {SW}/><rect x="0" y="660" width="1920" height="420" fill="#E6B26A"/>
      {"".join(f'<rect x="{x}" y="700" width="300" height="330" rx="16" fill="#F2C98A" {SW}/><circle cx="{x + 260}" cy="860" r="12" fill="#8A5A2B"/>' for x in range(30, 1920, 330))}
      <rect x="1500" y="120" width="300" height="240" rx="20" fill="#9ED8FF" {SW}/><path d="M1650 120 L1650 360 M1500 240 L1800 240" stroke="{INK}" stroke-width="10"/>''',
}


def render():
    names = list(I)
    for start in range(0, len(names), 12):
        chunk = names[start:start + 12]
        cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{I[n]}</svg></div>'
                        for i, n in enumerate(chunk))
        w = 400 * len(chunk)
        A.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>', str(OUT / "_items.png"), w, 400, scale=2)
        im = Image.open(OUT / "_items.png")
        for i, n in enumerate(chunk):
            im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_{n}.png")
        (OUT / "_items.png").unlink()
    for n, svg in BGS.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>',
               str(OUT / f"bg_{n}.png"), 1920, 1080)
    cols = 10
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 160, rows * 160 + 300), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((150, 150)), ((i % cols) * 160, (i // cols) * 160))
    for j, n in enumerate(BGS):
        sheet.alpha_composite(Image.open(OUT / f"bg_{n}.png").convert("RGBA").resize((520, 292)), (j * 530, rows * 160 + 4))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items +", len(BGS), "backgrounds")


if __name__ == "__main__":
    render()
