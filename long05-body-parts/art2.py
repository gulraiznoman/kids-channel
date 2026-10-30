"""v2 art for Body Parts: cute organs (brain, heart, lungs, stomach, bone, skull, muscle) + 'stage' background.
python art2.py -> art/item_<key>.png, art/bg_stage.png, _sheet2.png
"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A
import animals_v2 as AV

SW, INK = A.SW, A.INK
OUT = HERE / "art"
eye, cheek = AV.eye, AV.cheek
FACE = lambda x, y, s=1.0: (f'{eye(x - 30 * s, y, 15 * s)}{eye(x + 30 * s, y, 15 * s)}{cheek(x - 55 * s, y + 30 * s, 12 * s)}{cheek(x + 55 * s, y + 30 * s, 12 * s)}'
                            f'<path d="M{x - 18 * s} {y + 30 * s} Q{x} {y + 50 * s} {x + 18 * s} {y + 30 * s}" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>')

I = {}
I["brain"] = f'''<path d="M200 70 Q290 50 330 120 Q380 160 350 230 Q360 300 290 320 Q240 350 200 320 Q160 350 110 320 Q40 300 50 230 Q20 160 70 120 Q110 50 200 70 Z" fill="#FFA3C4" {SW}/>
<path d="M200 80 L200 315 M110 130 Q150 160 120 200 Q100 230 140 260 M290 130 Q250 160 280 200 Q300 230 260 260 M80 200 Q100 210 90 240 M320 200 Q300 210 310 240"
 stroke="#E06A96" stroke-width="8" fill="none" stroke-linecap="round"/>{FACE(200, 200, 0.9)}'''
I["heart_organ"] = f'''<path d="M200 350 L70 220 Q20 160 70 100 Q130 50 200 120 Q270 50 330 100 Q380 160 330 220 Z" fill="#FF4D6D" {SW}/>
<path d="M160 70 L160 30 M200 110 L200 40 M240 70 L240 30" stroke="#7EC8FF" stroke-width="22" stroke-linecap="round"/>{FACE(200, 190)}'''
I["lungs"] = f'''<path d="M200 40 L200 150 M200 150 Q160 160 150 190 M200 150 Q240 160 250 190" stroke="#B0B8C8" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M150 150 Q60 140 50 260 Q40 350 120 350 Q170 350 175 300 L175 190 Q170 150 150 150 Z" fill="#FF9EB5" {SW}/>
<path d="M250 150 Q340 140 350 260 Q360 350 280 350 Q230 350 225 300 L225 190 Q230 150 250 150 Z" fill="#FF9EB5" {SW}/>
{eye(100, 240, 13)}{eye(140, 240, 13)}{eye(260, 240, 13)}{eye(300, 240, 13)}
<path d="M105 280 Q120 295 135 280 M265 280 Q280 295 295 280" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'''
I["stomach"] = f'''<path d="M150 50 L150 130 Q90 150 80 230 Q75 330 190 340 Q300 345 330 270 Q345 220 300 210 Q260 205 250 250 Q240 290 200 280 Q170 270 185 180 L210 130 L210 50 Z" fill="#FFB38A" {SW}/>
{FACE(170, 230, 0.8)}'''
I["bone"] = f'''<path d="M110 120 Q60 80 90 50 Q120 30 140 70 L260 190 Q300 170 330 190 Q360 220 320 250 Q350 290 310 310 Q280 330 260 280 L140 160 Q100 180 70 160 Q40 130 80 110 Z" fill="#FFF8E7" {SW}/>'''
I["skull"] = f'''<path d="M200 50 Q330 50 330 180 Q330 240 290 260 L290 320 L110 320 L110 260 Q70 240 70 180 Q70 50 200 50 Z" fill="#FFF8E7" {SW}/>
<ellipse cx="150" cy="180" rx="38" ry="44" fill="{INK}"/><ellipse cx="250" cy="180" rx="38" ry="44" fill="{INK}"/>
<path d="M190 230 L200 255 L210 230 Z" fill="{INK}"/><path d="M140 290 L140 320 M180 290 L180 320 M220 290 L220 320 M260 290 L260 320" stroke="{INK}" stroke-width="6"/>
<path d="M120 280 Q200 300 280 280" stroke="{INK}" stroke-width="6" fill="none"/>'''
I["muscle"] = f'''<path d="M60 330 L60 230 Q60 170 120 170 L170 170 Q170 90 230 70 Q290 55 320 110 Q340 150 300 190 Q340 230 320 280 Q300 330 230 330 Z" fill="#DCA27A" {SW}/>
<path d="M200 140 Q250 110 290 150" stroke="#B9774D" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M330 60 l20 -20 M345 95 l28 -5 M300 40 l5 -28" stroke="#FFD23F" stroke-width="10" stroke-linecap="round"/>'''
I["poster"] = f'''<rect x="40" y="20" width="320" height="360" rx="14" fill="#FFFFFF" {SW}/>
<circle cx="200" cy="90" r="40" fill="#FFD9B8" {SW}/><path d="M200 130 L200 250 M200 160 L140 210 M200 160 L260 210 M200 250 L160 340 M200 250 L240 340" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#FF6B8B"/><path d="M{x} {y} L{x + d} {y}" stroke="#2EA8FF" stroke-width="4"/>' for x, y, d in ((200, 90, 110), (140, 210, -70), (260, 210, 70), (200, 250, 110)))}'''

STAGE = f'''<defs><radialGradient id="g" cx="0.5" cy="0.35" r="0.8"><stop offset="0" stop-color="#FFF3B0"/><stop offset="0.55" stop-color="#7FD8FF"/><stop offset="1" stop-color="#6A7DFF"/></radialGradient></defs>
<rect width="1920" height="1080" fill="url(#g)"/>
{"".join(f'<path d="M960 -50 L{x - 90} 820 L{x + 90} 820 Z" fill="#FFFFFF" opacity="0.13"/>' for x in (300, 960, 1620))}
<rect x="0" y="800" width="1920" height="280" fill="#FF8FB1"/><rect x="0" y="800" width="1920" height="26" fill="#FFFFFF" {SW}/>
<ellipse cx="960" cy="935" rx="700" ry="90" fill="#FFB3C7"/>
<g transform="translate(70 230) scale(0.9)">{I["poster"]}</g><g transform="translate(1520 230) scale(0.9)">
<rect x="40" y="20" width="320" height="360" rx="14" fill="#FFFFFF" {SW}/>
{FACE(200, 150, 1.6)}<text x="95" y="330" font-size="70" font-family="Arial Black" fill="#FF6B8B">ME!</text></g>
{"".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#FFFFFF"/>' for x, y in ((520, 120), (760, 80), (1180, 100), (1400, 150), (640, 200), (1290, 230)))}'''


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
    A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{STAGE}</svg></body></html>',
           str(OUT / "bg_stage.png"), 1920, 1080)
    sheet = Image.new("RGBA", (160 * len(names), 160 + 300), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((150, 150)), (i * 160, 0))
    sheet.alpha_composite(Image.open(OUT / "bg_stage.png").convert("RGBA").resize((520, 292)), (0, 164))
    sheet.save(HERE / "_sheet2.png")
    print("rendered", names)


if __name__ == "__main__":
    render()
