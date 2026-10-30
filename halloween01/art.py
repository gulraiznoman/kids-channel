"""Cute, not-scary Halloween items (same SVG style as long01 animals). python art.py -> art/item_<key>.png (800x800)"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A
import animals_v2 as AV

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
eye, cheek = AV.eye, AV.cheek

PUMPKIN_BODY = f'''
<path d="M190 120 Q186 82 206 62 Q218 56 222 66 Q206 84 212 120 Z" fill="#6B8E23" {SW}/>
<path d="M214 78 Q262 46 290 78 Q258 96 222 88 Z" fill="#7CC444" {SW}/>
<ellipse cx="130" cy="235" rx="95" ry="120" fill="#FF9A2E" {SW}/>
<ellipse cx="270" cy="235" rx="95" ry="120" fill="#FF9A2E" {SW}/>
<ellipse cx="200" cy="235" rx="80" ry="128" fill="#FFA940" {SW}/>
<path d="M118 140 Q100 235 118 330 M282 140 Q300 235 282 330" stroke="#E07A12" stroke-width="7" fill="none" stroke-linecap="round"/>'''

ITEMS = {}
ITEMS["pumpkin"] = PUMPKIN_BODY + f'''{eye(160, 225, 20)}{eye(240, 225, 20)}{cheek(135, 265)}{cheek(265, 265)}
{A.smile(200, 270, 32)}'''

ITEMS["jackolantern"] = f'''<circle cx="200" cy="235" r="175" fill="#FFE27A" opacity="0.35"/>''' + PUMPKIN_BODY + f'''
<path d="M135 220 L165 170 L195 220 Z" fill="#FFD23F" {SW}/><path d="M205 220 L235 170 L265 220 Z" fill="#FFD23F" {SW}/>
<path d="M188 238 L200 258 L212 238 Z" fill="#FFD23F" {SW}/>
<path d="M120 270 Q200 350 280 270 L260 280 L245 268 L228 292 L210 274 L190 292 L172 268 L155 280 Z" fill="#FFD23F" {SW}/>'''

K = "#2E2A3A"
ITEMS["blackcat"] = f'''
<path d="M290 340 Q370 330 360 250 Q352 215 330 225 Q345 290 285 305 Z" fill="{K}" {SW}/>
<path d="M135 365 Q120 270 200 250 Q280 270 265 365 Z" fill="{K}" {SW}/>
<ellipse cx="150" cy="358" rx="38" ry="22" fill="{K}" {SW}/><ellipse cx="250" cy="358" rx="38" ry="22" fill="{K}" {SW}/>
<path d="M105 150 L112 55 L175 110 Z" fill="{K}" {SW}/><path d="M295 150 L288 55 L225 110 Z" fill="{K}" {SW}/>
<path d="M122 125 L125 85 L155 110 Z" fill="#FF9EB5"/><path d="M278 125 L275 85 L245 110 Z" fill="#FF9EB5"/>
<circle cx="200" cy="175" r="105" fill="{K}" {SW}/>
{eye(160, 165, 26, "#7ED957")}{eye(240, 165, 26, "#7ED957")}
<path d="M190 205 L210 205 L200 216 Z" fill="#FF8FA3"/>
<path d="M200 216 Q188 236 175 228 M200 216 Q212 236 225 228" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
<path d="M95 200 L150 206 M95 225 L150 218 M305 200 L250 206 M305 225 L250 218" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
{cheek(140, 215, 14)}{cheek(260, 215, 14)}
<path d="M160 262 Q200 285 240 262" stroke="#FF8A3D" stroke-width="14" fill="none" stroke-linecap="round"/>
<circle cx="200" cy="282" r="12" fill="#FFD23F" {SW}/>'''

P = "#6C4BA6"
ITEMS["bat"] = f'''
<path d="M150 205 Q95 120 20 150 Q55 175 45 215 Q80 200 95 235 Q115 205 150 230 Z" fill="{P}" {SW}/>
<path d="M250 205 Q305 120 380 150 Q345 175 355 215 Q320 200 305 235 Q285 205 250 230 Z" fill="{P}" {SW}/>
<path d="M150 135 L140 80 L182 118 Z" fill="{P}" {SW}/><path d="M250 135 L260 80 L218 118 Z" fill="{P}" {SW}/>
<circle cx="200" cy="205" r="72" fill="#7D5BBE" {SW}/>
<ellipse cx="200" cy="232" rx="40" ry="28" fill="#B79BEA"/>
{eye(175, 195, 18)}{eye(225, 195, 18)}{cheek(160, 230, 11)}{cheek(240, 230, 11)}
<path d="M182 236 Q200 254 218 236" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<path d="M190 243 L194 252 L198 243 Z M202 243 L206 252 L210 243 Z" fill="#FFFFFF"/>'''

ITEMS["ghost"] = f'''
<path d="M95 330 Q95 90 200 85 Q305 90 305 330 Q285 360 262 330 Q240 362 220 330 Q200 362 180 330 Q160 362 138 330 Q117 360 95 330 Z" fill="#FFFFFF" {SW}/>
<path d="M98 220 Q50 200 55 160 Q85 175 104 190 Z" fill="#FFFFFF" {SW}/>
<path d="M302 220 Q350 200 345 160 Q315 175 296 190 Z" fill="#FFFFFF" {SW}/>
{eye(165, 190, 22)}{eye(235, 190, 22)}{cheek(145, 232, 16)}{cheek(255, 232, 16)}
<path d="M168 236 Q200 280 232 236 Z" fill="#7A2E3A" {SW}/><path d="M184 252 Q200 268 216 252 Q200 246 184 252 Z" fill="#FF7A90"/>'''

ITEMS["candy"] = f'''
<path d="M95 150 Q200 20 305 150" stroke="{INK}" stroke-width="10" fill="none"/>
<ellipse cx="200" cy="160" rx="135" ry="34" fill="#7A3E0C" {SW}/>
<rect x="246" y="40" width="12" height="110" rx="6" fill="#FFFFFF" {SW}/>
<circle cx="252" cy="44" r="38" fill="#4CC9F0" {SW}/>
<path d="M252 44 m-24 0 a24 24 0 1 0 48 0 a17 17 0 1 0 -34 0 a10 10 0 1 0 20 0" stroke="#FFFFFF" stroke-width="5" fill="none"/>
<path d="M115 128 L132 112 L160 112 L177 128 L160 144 L132 144 Z" fill="#FF6B8B" {SW}/>
<path d="M98 128 L115 118 L115 138 Z M194 128 L177 118 L177 138 Z" fill="#FF6B8B" {SW}/>
<rect x="175" y="96" width="44" height="58" rx="8" fill="#B57BFF" {SW} transform="rotate(-12 197 125)"/>
<circle cx="300" cy="138" r="20" fill="#FFD23F" {SW}/><circle cx="292" cy="132" r="6" fill="#FFFFFF"/>
<path d="M65 160 Q70 350 200 352 Q330 350 335 160 Q270 195 200 195 Q130 195 65 160 Z" fill="#FF9A2E" {SW}/>
<path d="M140 240 L165 210 L185 240 Z M215 240 L240 210 L260 240 Z" fill="#3A2420"/>
<path d="M140 275 Q200 325 260 275 Q230 290 200 290 Q170 290 140 275 Z" fill="#3A2420"/>'''


def render():
    names = list(ITEMS)
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{ITEMS[n]}</svg></div>'
                    for i, n in enumerate(names))
    w = 400 * len(names)
    A.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>',
           str(OUT / "_items.png"), w, 400, scale=2)
    im = Image.open(OUT / "_items.png")
    for i, n in enumerate(names):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_{n}.png")
    (OUT / "_items.png").unlink()
    sheet = Image.new("RGBA", (300 * len(names), 300), (210, 200, 235, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((300, 300)), (i * 300, 0))
    sheet.save(HERE / "_sheet.png")
    print("rendered", names)


if __name__ == "__main__":
    render()
