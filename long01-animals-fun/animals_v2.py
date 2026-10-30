"""Full-body cartoon baby animals (v2), replacing the head-only 'avatar' style.

python animals_v2.py -> art/fruit_<animal>.png (old head-only versions kept in art/old_heads/)
"""
import pathlib, shutil
from PIL import Image
import art as A

HERE = pathlib.Path(__file__).resolve().parent
SW, INK = A.SW, A.INK


def eye(cx, cy, r, iris="#4A2C1A"):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 1.15:.0f}" fill="#FFFFFF" {SW}/>'
            f'<circle cx="{cx + r * 0.08:.0f}" cy="{cy + r * 0.2:.0f}" r="{r * 0.72:.0f}" fill="{iris}"/>'
            f'<circle cx="{cx + r * 0.08:.0f}" cy="{cy + r * 0.25:.0f}" r="{r * 0.42:.0f}" fill="#140B07"/>'
            f'<circle cx="{cx - r * 0.25:.0f}" cy="{cy - r * 0.15:.0f}" r="{r * 0.3:.0f}" fill="#FFFFFF"/>'
            f'<circle cx="{cx + r * 0.35:.0f}" cy="{cy + r * 0.5:.0f}" r="{r * 0.14:.0f}" fill="#FFFFFF"/>')


def cheek(x, y, r=16):
    return f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.6:.0f}" fill="#FF8FA3" opacity="0.6"/>'


def leg(x, y, w, h, col, hoof=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w / 2:.0f}" fill="{col}" {SW}/>'
    if hoof:
        s += f'<rect x="{x}" y="{y + h - 18}" width="{w}" height="18" rx="8" fill="{hoof}" {SW}/>'
    return s


ANIMALS = {}

# --- puppy: sitting, front view, red collar ------------------------------------------------
B, L, D = "#E8B878", "#F8E3BF", "#B8823F"
ANIMALS["puppy"] = f'''
<path d="M285 335 Q365 310 350 240 Q340 222 326 238 Q338 292 280 305 Z" fill="{B}" {SW}/>
<path d="M128 365 Q112 262 200 238 Q288 262 272 365 Z" fill="{B}" {SW}/>
<ellipse cx="200" cy="312" rx="44" ry="50" fill="{L}"/>
<ellipse cx="128" cy="350" rx="48" ry="28" fill="{B}" {SW}/><ellipse cx="272" cy="350" rx="48" ry="28" fill="{B}" {SW}/>
{leg(160, 282, 36, 86, B)}{leg(204, 282, 36, 86, B)}
<ellipse cx="178" cy="368" rx="24" ry="13" fill="{L}" {SW}/><ellipse cx="222" cy="368" rx="24" ry="13" fill="{L}" {SW}/>
<path d="M140 244 Q200 274 260 244 L262 262 Q200 294 138 262 Z" fill="#E8352E" {SW}/>
<circle cx="200" cy="284" r="12" fill="#FFD23F" {SW}/>
<ellipse cx="200" cy="150" rx="94" ry="86" fill="{B}" {SW}/>
<ellipse cx="112" cy="158" rx="33" ry="66" fill="{D}" {SW} transform="rotate(16 112 158)"/>
<ellipse cx="288" cy="158" rx="33" ry="66" fill="{D}" {SW} transform="rotate(-16 288 158)"/>
<ellipse cx="200" cy="192" rx="50" ry="37" fill="{L}" {SW}/>
<ellipse cx="200" cy="173" rx="18" ry="12" fill="#2B1B17"/><ellipse cx="195" cy="169" rx="6" ry="3" fill="#FFFFFF"/>
<path d="M190 207 Q200 236 210 207 Z" fill="#FF7A90" {SW}/>
<path d="M200 185 L200 198 M200 198 Q186 211 174 201 M200 198 Q214 211 226 201" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
{eye(162, 138, 17)}{eye(238, 138, 17)}{cheek(140, 185)}{cheek(260, 185)}'''

# --- kitten: sitting, orange tabby ---------------------------------------------------------
B, L, D = "#F2A65A", "#FFE2C2", "#D9802E"
ANIMALS["kitten"] = f'''
<path d="M262 345 Q352 340 342 258 Q336 238 321 254 Q332 312 258 322 Z" fill="{B}" {SW}/>
<path d="M140 368 Q124 258 200 242 Q276 258 260 368 Z" fill="{B}" {SW}/>
<ellipse cx="200" cy="318" rx="38" ry="46" fill="{L}"/>
<path d="M150 280 Q165 285 168 300 M250 280 Q235 285 232 300" stroke="{D}" stroke-width="8" fill="none" stroke-linecap="round"/>
<ellipse cx="140" cy="352" rx="40" ry="24" fill="{B}" {SW}/><ellipse cx="260" cy="352" rx="40" ry="24" fill="{B}" {SW}/>
{leg(168, 286, 30, 82, B)}{leg(202, 286, 30, 82, B)}
<ellipse cx="183" cy="368" rx="20" ry="11" fill="#FFFFFF" {SW}/><ellipse cx="217" cy="368" rx="20" ry="11" fill="#FFFFFF" {SW}/>
<path d="M118 135 L122 52 L184 100 Z" fill="{B}" {SW}/><path d="M282 135 L278 52 L216 100 Z" fill="{B}" {SW}/>
<path d="M132 118 L134 75 L168 102 Z" fill="#FFB3C7"/><path d="M268 118 L266 75 L232 102 Z" fill="#FFB3C7"/>
<ellipse cx="200" cy="165" rx="90" ry="80" fill="{B}" {SW}/>
<path d="M182 92 L186 125 M200 88 L200 125 M218 92 L214 125" stroke="{D}" stroke-width="9" stroke-linecap="round"/>
<ellipse cx="200" cy="205" rx="40" ry="26" fill="{L}"/>
{eye(162, 165, 18, "#5FA845")}{eye(238, 165, 18, "#5FA845")}
<path d="M189 196 L211 196 L200 208 Z" fill="#FF7A90"/>
<path d="M200 208 Q190 224 178 216 M200 208 Q210 224 222 216" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
<path d="M88 195 L150 202 M88 220 L150 212 M312 195 L250 202 M312 220 L250 212" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
{cheek(140, 200)}{cheek(260, 200)}'''

# --- duckling: side view, waddling ---------------------------------------------------------
B, D = "#FFD93B", "#F2BE12"
ANIMALS["duckling"] = f'''
<path d="M190 330 L185 368 M240 330 L245 368" stroke="#FF9420" stroke-width="12" stroke-linecap="round"/>
<path d="M160 368 L210 368 L188 352 Z M222 368 L272 368 L250 352 Z" fill="#FF9420" {SW}/>
<path d="M330 250 Q370 225 360 270 Q345 285 320 280 Z" fill="{B}" {SW}/>
<ellipse cx="225" cy="275" rx="118" ry="76" fill="{B}" {SW}/>
<ellipse cx="238" cy="268" rx="62" ry="38" fill="{D}" {SW} transform="rotate(-12 238 268)"/>
<circle cx="145" cy="172" r="68" fill="{B}" {SW}/>
<path d="M135 106 Q140 72 158 102 Q170 78 172 108" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<path d="M80 178 Q40 182 42 198 Q48 214 84 206 Z" fill="#FF9420" {SW}/>
{eye(140, 160, 15)}{cheek(165, 200)}'''

# --- chick: standing --------------------------------------------------------------------------
B, D = "#FFE45C", "#F5C918"
ANIMALS["chick"] = f'''
<path d="M175 320 L170 365 M225 320 L230 365" stroke="#FF9420" stroke-width="11" stroke-linecap="round"/>
<path d="M145 368 L195 368 L172 352 Z M208 368 L258 368 L234 352 Z" fill="#FF9420" {SW}/>
<ellipse cx="85" cy="230" rx="38" ry="22" fill="{D}" {SW} transform="rotate(-25 85 230)"/>
<ellipse cx="315" cy="230" rx="38" ry="22" fill="{D}" {SW} transform="rotate(25 315 230)"/>
<ellipse cx="200" cy="215" rx="118" ry="122" fill="{B}" {SW}/>
<path d="M185 96 Q190 62 205 92 Q218 66 220 98" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
{eye(158, 180, 17)}{eye(242, 180, 17)}
<path d="M180 215 L220 215 L200 245 Z" fill="#FF9420" {SW}/>{cheek(130, 225)}{cheek(270, 225)}'''

# --- lamb: standing, fluffy ----------------------------------------------------------------
W = "#FFFFFF"
fluff = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{W}" {SW}/>' for x, y, r in
                ((150, 210, 52), (210, 195, 55), (270, 210, 52), (300, 255, 48), (255, 290, 50), (190, 292, 50), (140, 265, 48)))
fluff_in = "".join(f'<circle cx="{x}" cy="{y}" r="{r - 4}" fill="{W}"/>' for x, y, r in
                   ((150, 210, 52), (210, 195, 55), (270, 210, 52), (300, 255, 48), (255, 290, 50), (190, 292, 50), (140, 265, 48))) + \
    f'<ellipse cx="220" cy="250" rx="90" ry="55" fill="{W}"/>'
ANIMALS["lamb"] = f'''
{leg(150, 285, 26, 85, "#5B5B66", "#2B2B33")}{leg(185, 295, 26, 75, "#5B5B66", "#2B2B33")}
{leg(245, 295, 26, 75, "#5B5B66", "#2B2B33")}{leg(280, 285, 26, 85, "#5B5B66", "#2B2B33")}
{fluff}{fluff_in}
<ellipse cx="65" cy="175" rx="38" ry="17" fill="#8A8A96" {SW} transform="rotate(-20 65 175)"/>
<ellipse cx="185" cy="175" rx="38" ry="17" fill="#8A8A96" {SW} transform="rotate(20 185 175)"/>
<ellipse cx="125" cy="190" rx="56" ry="64" fill="#FBE3D0" {SW}/>
<circle cx="105" cy="128" r="22" fill="{W}" {SW}/><circle cx="130" cy="120" r="24" fill="{W}" {SW}/><circle cx="153" cy="130" r="21" fill="{W}" {SW}/>
{eye(105, 185, 13)}{eye(148, 185, 13)}
<ellipse cx="126" cy="222" rx="12" ry="8" fill="#FF8FA3"/>
<path d="M114 234 Q126 246 138 234" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>{cheek(95, 215, 12)}{cheek(158, 215, 12)}'''

# --- piglet: standing side ----------------------------------------------------------------
B, D = "#FFB3C7", "#FF8FA8"
ANIMALS["piglet"] = f'''
{leg(140, 290, 30, 75, B, "#B5446A")}{leg(180, 300, 30, 65, B, "#B5446A")}{leg(250, 300, 30, 65, B, "#B5446A")}{leg(290, 290, 30, 75, B, "#B5446A")}
<path d="M325 245 Q360 230 352 210 Q340 198 335 215 Q345 225 330 232" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>
<path d="M325 245 Q360 230 352 210 Q340 198 335 215 Q345 225 330 232" fill="none" stroke="{B}" stroke-width="6" stroke-linecap="round"/>
<ellipse cx="225" cy="255" rx="118" ry="78" fill="{B}" {SW}/>
<path d="M95 150 L92 95 L140 125 Z M160 135 L180 85 L195 135 Z" fill="{D}" {SW}/>
<circle cx="130" cy="205" r="72" fill="{B}" {SW}/>
<ellipse cx="72" cy="225" rx="30" ry="25" fill="{D}" {SW}/>
<ellipse cx="62" cy="225" rx="6" ry="9" fill="#B5446A"/><ellipse cx="82" cy="225" rx="6" ry="9" fill="#B5446A"/>
{eye(115, 185, 14)}{eye(160, 185, 14)}
<path d="M110 250 Q125 262 140 250" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>{cheek(165, 228)}'''

# --- calf: standing side, black & white -----------------------------------------------------
ANIMALS["calf"] = f'''
{leg(140, 275, 30, 95, "#FFFFFF", "#3A3A44")}{leg(180, 285, 30, 85, "#FFFFFF", "#3A3A44")}
{leg(260, 285, 30, 85, "#FFFFFF", "#3A3A44")}{leg(300, 275, 30, 95, "#FFFFFF", "#3A3A44")}
<path d="M340 215 Q372 260 360 300" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
<ellipse cx="360" cy="305" rx="11" ry="16" fill="#3A3A44"/>
<clipPath id="cowb"><rect x="110" y="170" width="240" height="135" rx="60"/></clipPath>
<rect x="110" y="170" width="240" height="135" rx="60" fill="#FFFFFF"/>
<g clip-path="url(#cowb)"><path d="M200 165 Q250 170 240 220 Q205 240 185 205 Z M290 230 Q340 225 345 270 Q310 300 285 270 Z" fill="#2B2B33"/></g>
<rect x="110" y="170" width="240" height="135" rx="60" fill="none" {SW}/>
<path d="M75 105 Q65 80 82 75 L92 108 Z M150 105 Q160 80 143 75 L133 108 Z" fill="#F2D06B" {SW}/>
<ellipse cx="45" cy="135" rx="35" ry="16" fill="#FFFFFF" {SW} transform="rotate(-15 45 135)"/>
<ellipse cx="180" cy="135" rx="35" ry="16" fill="#FFFFFF" {SW} transform="rotate(15 180 135)"/>
<ellipse cx="112" cy="165" rx="60" ry="68" fill="#FFFFFF" {SW}/>
<path d="M75 120 Q95 105 110 130 Q95 150 75 140 Z" fill="#2B2B33"/>
<ellipse cx="112" cy="210" rx="52" ry="32" fill="#FFB3C7" {SW}/>
<ellipse cx="96" cy="210" rx="8" ry="11" fill="#B5446A"/><ellipse cx="128" cy="210" rx="8" ry="11" fill="#B5446A"/>
{eye(90, 158, 14)}{eye(136, 158, 14)}'''

# --- bunny: sitting side --------------------------------------------------------------------
B, L = "#E9E2EF", "#FFFFFF"
ANIMALS["bunny"] = f'''
<ellipse cx="135" cy="95" rx="24" ry="78" fill="{B}" {SW} transform="rotate(-12 135 95)"/>
<ellipse cx="185" cy="90" rx="24" ry="78" fill="{B}" {SW} transform="rotate(10 185 90)"/>
<ellipse cx="135" cy="98" rx="11" ry="56" fill="#FFB3C7" transform="rotate(-12 135 98)"/>
<ellipse cx="185" cy="93" rx="11" ry="56" fill="#FFB3C7" transform="rotate(10 185 93)"/>
<circle cx="318" cy="300" r="28" fill="{L}" {SW}/>
<ellipse cx="225" cy="290" rx="100" ry="78" fill="{B}" {SW}/>
<ellipse cx="255" cy="360" rx="62" ry="18" fill="{B}" {SW}/>
<ellipse cx="150" cy="350" rx="24" ry="14" fill="{L}" {SW}/>
<ellipse cx="200" cy="300" rx="40" ry="45" fill="{L}"/>
<circle cx="160" cy="200" r="70" fill="{B}" {SW}/>
{eye(132, 192, 15)}{eye(182, 192, 15)}
<ellipse cx="157" cy="226" rx="10" ry="7" fill="#FF7A90"/>
<path d="M145 240 Q157 250 169 240" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
<path d="M95 222 L135 228 M95 240 L135 234 M220 222 L180 228 M220 240 L180 234" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>
{cheek(120, 228, 12)}{cheek(195, 228, 12)}'''

# --- foal: standing side -------------------------------------------------------------------
B, L, M = "#C68A52", "#E9C9A2", "#5A3A22"
import math as _m
_mane = "".join(f'<circle cx="{198 + (232 - 198) * k / 6 + 6:.0f}" cy="{100 + (200 - 100) * k / 6:.0f}" r="15" fill="{M}" {SW}/>' for k in range(7))
ANIMALS["foal"] = f'''
{leg(165, 250, 24, 120, B, M)}{leg(195, 258, 24, 112, B, M)}{leg(275, 258, 24, 112, B, M)}{leg(305, 250, 24, 120, B, M)}
<path d="M335 215 Q380 240 370 310 Q352 300 345 255 Z" fill="{M}" {SW}/>
{_mane}
<path d="M178 225 Q150 175 145 115 Q170 92 198 102 Q205 165 240 205 Z" fill="{B}" {SW}/>
<ellipse cx="245" cy="232" rx="100" ry="55" fill="{B}" {SW}/>
<path d="M180 222 Q165 200 160 170" fill="none" stroke="{B}" stroke-width="30"/>
<ellipse cx="128" cy="118" rx="44" ry="58" fill="{B}" {SW} transform="rotate(-35 128 118)"/>
<path d="M148 72 L150 34 L172 66 Z" fill="{B}" {SW}/>
<ellipse cx="96" cy="150" rx="31" ry="26" fill="{L}" {SW} transform="rotate(-35 96 150)"/>
<ellipse cx="86" cy="153" rx="5" ry="7" fill="{M}"/>
<path d="M150 72 Q170 60 190 80" fill="none" stroke="{M}" stroke-width="14" stroke-linecap="round"/>
{eye(135, 108, 13)}{cheek(118, 140, 11)}'''

# --- lion cub: sitting front ----------------------------------------------------------------
B, L, MN = "#F2B54E", "#FCE3B0", "#E07B24"
mane = "".join(f'<circle cx="{200 + 92 * __import__("math").cos(k * 0.5236):.0f}" cy="{150 + 86 * __import__("math").sin(k * 0.5236):.0f}" r="34" fill="{MN}" {SW}/>' for k in range(12))
ANIMALS["cub"] = f'''
<path d="M282 340 Q350 330 345 270" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
<path d="M282 340 Q350 330 345 270" fill="none" stroke="{B}" stroke-width="9" stroke-linecap="round"/>
<ellipse cx="345" cy="262" rx="16" ry="20" fill="{MN}" {SW}/>
<path d="M135 368 Q120 262 200 240 Q280 262 265 368 Z" fill="{B}" {SW}/>
<ellipse cx="200" cy="315" rx="40" ry="48" fill="{L}"/>
<ellipse cx="135" cy="352" rx="44" ry="26" fill="{B}" {SW}/><ellipse cx="265" cy="352" rx="44" ry="26" fill="{B}" {SW}/>
{leg(163, 285, 34, 83, B)}{leg(203, 285, 34, 83, B)}
<ellipse cx="180" cy="369" rx="22" ry="12" fill="{L}" {SW}/><ellipse cx="220" cy="369" rx="22" ry="12" fill="{L}" {SW}/>
{mane}<ellipse cx="200" cy="150" rx="92" ry="86" fill="{MN}"/>
<circle cx="130" cy="88" r="24" fill="{B}" {SW}/><circle cx="270" cy="88" r="24" fill="{B}" {SW}/>
<ellipse cx="200" cy="155" rx="78" ry="74" fill="{B}" {SW}/>
<ellipse cx="200" cy="192" rx="44" ry="32" fill="{L}" {SW}/>
<path d="M186 176 L214 176 L200 192 Z" fill="#5A3A22"/>
<path d="M200 192 Q188 206 178 198 M200 192 Q212 206 222 198" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
{eye(168, 145, 15)}{eye(232, 145, 15)}{cheek(150, 185)}{cheek(250, 185)}'''

# --- baby elephant: standing side ----------------------------------------------------------
B, D = "#A3A3AF", "#8E8E9C"
ANIMALS["elephant"] = f'''
{leg(165, 260, 42, 110, B)}{leg(210, 270, 42, 100, B)}{leg(275, 270, 42, 100, B)}{leg(318, 260, 42, 110, B)}
<path d="M355 220 Q378 250 370 285" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
<ellipse cx="255" cy="225" rx="115" ry="82" fill="{B}" {SW}/>
<path d="M70 200 Q40 260 55 315 Q65 340 85 330 Q72 300 90 255 Z" fill="{B}" {SW}/>
<circle cx="120" cy="175" r="72" fill="{B}" {SW}/>
<ellipse cx="185" cy="182" rx="46" ry="62" fill="{D}" {SW}/>
<ellipse cx="185" cy="182" rx="28" ry="42" fill="#E9B8C4"/>
{eye(98, 160, 14)}{cheek(95, 200, 13)}'''

# --- monkey: sitting, holding a banana -------------------------------------------------------
B, L = "#8B5A2B", "#E9C29A"
ANIMALS["monkey"] = f'''
<path d="M270 345 Q360 350 355 270 Q350 225 315 240 Q300 255 320 262 Q335 262 332 280 Q330 320 265 320" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>
<path d="M270 345 Q360 350 355 270 Q350 225 315 240 Q300 255 320 262 Q335 262 332 280 Q330 320 265 320" fill="none" stroke="{B}" stroke-width="10" stroke-linecap="round"/>
<path d="M135 368 Q120 262 200 240 Q280 262 265 368 Z" fill="{B}" {SW}/>
<ellipse cx="200" cy="318" rx="44" ry="48" fill="{L}"/>
<ellipse cx="140" cy="355" rx="40" ry="22" fill="{B}" {SW}/><ellipse cx="260" cy="355" rx="40" ry="22" fill="{B}" {SW}/>
<path d="M175 300 Q200 255 245 285 Q235 310 205 315 Z" fill="#FFD93B" {SW}/>
<path d="M150 280 Q165 315 190 305" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>
<path d="M150 280 Q165 315 190 305" fill="none" stroke="{B}" stroke-width="14" stroke-linecap="round"/>
<circle cx="110" cy="150" r="34" fill="{B}" {SW}/><circle cx="290" cy="150" r="34" fill="{B}" {SW}/>
<circle cx="110" cy="150" r="19" fill="{L}"/><circle cx="290" cy="150" r="19" fill="{L}"/>
<circle cx="200" cy="150" r="90" fill="{B}" {SW}/>
<path d="M200 105 Q155 70 128 125 Q112 195 200 235 Q288 195 272 125 Q245 70 200 105 Z" fill="{L}" {SW}/>
{eye(172, 140, 15)}{eye(228, 140, 15)}
<ellipse cx="190" cy="185" rx="4" ry="6" fill="#5A3A22"/><ellipse cx="210" cy="185" rx="4" ry="6" fill="#5A3A22"/>
<path d="M178 205 Q200 222 222 205" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>{cheek(150, 190, 13)}{cheek(250, 190, 13)}'''


if __name__ == "__main__":
    old = HERE / "art" / "old_heads"
    old.mkdir(exist_ok=True)
    for k in ANIMALS:
        p = HERE / "art" / f"fruit_{k}.png"
        if p.exists() and not (old / p.name).exists():
            shutil.copy2(p, old / p.name)
    A.ITEMS.clear()
    A.ITEMS.update(ANIMALS)
    A.render_items()
    keys = list(ANIMALS)
    s = Image.new("RGB", (6 * 260, 2 * 260), (126, 200, 255))
    for i, k in enumerate(keys):
        t = Image.open(HERE / "art" / f"fruit_{k}.png").resize((250, 250))
        s.paste(t, ((i % 6) * 260 + 5, (i // 6) * 260 + 5), t)
    s.save(HERE / "_animals.png")
    print("ok", len(keys))
