"""Art for long video 1: farm + road backgrounds, baby animals, shapes, vehicles, counting, weather."""
import math, pathlib, random, subprocess
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
FRUIT_ART = HERE.parent / "ep01-fruits" / "art"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SW = 'stroke="#3A2420" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
INK = "#3A2420"


def shot(html, out, w, h, scale=1):
    tmp = HERE / "_r.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={out}", tmp.as_uri()], check=True, capture_output=True)
    tmp.unlink()


# ------------------------------------------------------------------ backgrounds
def sky_and_clouds(w):
    clouds = "".join(f'<g transform="translate({cx} {cy}) scale({s})" fill="#FFFFFF"><ellipse cx="0" cy="0" rx="110" ry="55"/>'
                     f'<ellipse cx="-80" cy="20" rx="70" ry="45"/><ellipse cx="85" cy="18" rx="80" ry="48"/><ellipse cx="10" cy="-35" rx="70" ry="50"/></g>'
                     for cx, cy, s in ((300, 170, 1.0), (1000, 110, 0.8), (1600, 200, 1.1)))
    return f'''<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7EC8FF"/><stop offset="1" stop-color="#D8F1FF"/></linearGradient></defs>
    <rect width="{w}" height="1080" fill="url(#sky)"/>
    <circle cx="1720" cy="150" r="90" fill="#FFE066"/><circle cx="1720" cy="150" r="120" fill="#FFE066" opacity="0.3"/>{clouds}'''


def bg_farm():
    rnd = random.Random(3)
    fence = "".join(f'<rect x="{x}" y="760" width="22" height="120" rx="6" fill="#FFFFFF" {SW}/>' for x in range(20, 1920, 110))
    flowers = "".join(f'<circle cx="{rnd.uniform(20, 1900):.0f}" cy="{rnd.uniform(960, 1060):.0f}" r="{rnd.uniform(8, 12):.0f}" '
                      f'fill="{rnd.choice(["#FF6B8B", "#FFD23F", "#FFFFFF", "#B57BFF"])}"/>' for _ in range(40))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{sky_and_clouds(1920)}
    <path d="M0 690 Q300 580 640 650 Q980 720 1300 630 Q1620 540 1920 650 L1920 1080 L0 1080 Z" fill="#9BDB6B"/>
    <!-- barn (behind the middle) -->
    <path d="M700 520 L960 360 L1220 520 Z" fill="#B23A2E" {SW}/>
    <rect x="720" y="520" width="480" height="300" fill="#D9473A" {SW}/>
    <rect x="880" y="640" width="160" height="180" fill="#FFFFFF" {SW}/>
    <path d="M880 640 L1040 820 M1040 640 L880 820" stroke="#D9473A" stroke-width="12"/>
    <rect x="910" y="440" width="100" height="70" fill="#FFFFFF" {SW}/>
    <!-- haystack + tree -->
    <ellipse cx="1420" cy="760" rx="120" ry="90" fill="#F2C14E" {SW}/>
    <path d="M1330 740 Q1420 700 1510 740 M1340 780 Q1420 750 1500 780" stroke="#D9A23A" stroke-width="6" fill="none"/>
    <path d="M0 780 Q420 720 900 770 Q1400 820 1920 750 L1920 1080 L0 1080 Z" fill="#7CCB4F"/>
    <rect x="0" y="790" width="1920" height="22" fill="#FFFFFF" {SW}/><rect x="0" y="840" width="1920" height="22" fill="#FFFFFF" {SW}/>
    {fence}
    <rect x="0" y="960" width="1920" height="120" fill="#6CBF45"/>{flowers}</svg>'''
    shot(f'<html><body style="margin:0">{svg}</body></html>', str(OUT / "bg_farm.png"), 1920, 1080)


def bg_road():
    rnd = random.Random(5)
    cols = ["#FF8FA3", "#FFD166", "#8ECAE6", "#B8E986", "#C3A6FF", "#FFB4A2"]
    blds = ""
    x = 0
    while x < 1920:
        w, h = rnd.randint(110, 190), rnd.randint(200, 380)
        c = rnd.choice(cols)
        blds += f'<rect x="{x}" y="{700 - h}" width="{w}" height="{h}" fill="{c}" {SW}/>'
        for wy in range(700 - h + 30, 680, 60):
            for wx in range(x + 22, x + w - 30, 45):
                blds += f'<rect x="{wx}" y="{wy}" width="24" height="30" rx="4" fill="#FFFFFF" opacity="0.85"/>'
        x += w + rnd.randint(6, 30)
    dashes = "".join(f'<rect x="{x}" y="806" width="90" height="16" rx="8" fill="#FFFFFF"/>' for x in range(30, 1920, 170))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{sky_and_clouds(1920)}
    {blds}
    <rect x="0" y="700" width="1920" height="40" fill="#BFC6CE" {SW}/>
    <rect x="0" y="740" width="1920" height="150" fill="#5B6370"/>
    {dashes}
    <rect x="0" y="890" width="1920" height="40" fill="#BFC6CE" {SW}/>
    <rect x="0" y="930" width="1920" height="150" fill="#7CCB4F"/></svg>'''
    shot(f'<html><body style="margin:0">{svg}</body></html>', str(OUT / "bg_road.png"), 1920, 1080)


# ------------------------------------------------------------------ helpers for cute faces
def eyes(x1, x2, y, r=15):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2B1B17"/><circle cx="{x - r * 0.35:.0f}" cy="{y - r * 0.35:.0f}" r="{r * 0.38:.0f}" fill="#FFFFFF"/>' for x in (x1, x2))


def smile(cx, cy, w=30):
    return f'<path d="M{cx - w} {cy} Q{cx} {cy + w * 0.9} {cx + w} {cy}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'


def cheeks(x1, x2, y):
    return f'<ellipse cx="{x1}" cy="{y}" rx="20" ry="12" fill="#FF8FA3" opacity="0.6"/><ellipse cx="{x2}" cy="{y}" rx="20" ry="12" fill="#FF8FA3" opacity="0.6"/>'


A = {}
A["puppy"] = f'''<ellipse cx="95" cy="200" rx="50" ry="95" fill="#A0703C" {SW} transform="rotate(18 95 200)"/>
<ellipse cx="305" cy="200" rx="50" ry="95" fill="#A0703C" {SW} transform="rotate(-18 305 200)"/>
<circle cx="200" cy="205" r="125" fill="#E3B47A" {SW}/>
<ellipse cx="200" cy="265" rx="70" ry="52" fill="#FFF1DC" {SW}/>
<ellipse cx="200" cy="240" rx="24" ry="17" fill="#2B1B17"/>
<path d="M188 290 Q200 330 214 290 Z" fill="#FF7A90" {SW}/>{eyes(150, 250, 185)}'''
A["kitten"] = f'''<path d="M90 160 L95 40 L185 110 Z" fill="#F2A65A" {SW}/><path d="M310 160 L305 40 L215 110 Z" fill="#F2A65A" {SW}/>
<path d="M105 130 L108 75 L155 112 Z" fill="#FFB3C7"/><path d="M295 130 L292 75 L245 112 Z" fill="#FFB3C7"/>
<circle cx="200" cy="215" r="130" fill="#F2A65A" {SW}/>
<path d="M180 100 L185 140 M200 95 L200 140 M220 100 L215 140" stroke="#D9802E" stroke-width="10" stroke-linecap="round"/>
{eyes(150, 250, 205, 17)}<path d="M188 245 L212 245 L200 258 Z" fill="#FF7A90"/>
<path d="M200 258 Q185 280 170 270 M200 258 Q215 280 230 270" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<path d="M70 245 L140 252 M70 275 L140 266 M330 245 L260 252 M330 275 L260 266" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'''
A["duckling"] = f'''<ellipse cx="215" cy="290" rx="130" ry="85" fill="#FFD93B" {SW}/>
<path d="M300 260 Q350 230 345 280 Q330 300 300 295 Z" fill="#FFD93B" {SW}/>
<circle cx="165" cy="165" r="95" fill="#FFD93B" {SW}/>
<path d="M150 72 Q160 40 175 70 Q185 45 190 75" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<ellipse cx="85" cy="185" rx="50" ry="22" fill="#FF9420" {SW}/>{eyes(140, 205, 150, 13)}{cheeks(130, 215, 190)}'''
A["chick"] = f'''<circle cx="200" cy="180" r="115" fill="#FFE45C" {SW}/>
<path d="M185 70 Q195 35 210 68" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
{eyes(160, 240, 160, 14)}<path d="M180 195 L220 195 L200 225 Z" fill="#FF9420" {SW}/>{cheeks(140, 260, 200)}
<path d="M70 250 L100 220 L130 255 L165 222 L200 258 L235 222 L270 255 L300 220 L330 250 L330 330 Q200 390 70 330 Z" fill="#FFFFFF" {SW}/>'''
A["lamb"] = "".join(f'<circle cx="{200 + 115 * math.cos(k * math.pi / 5):.0f}" cy="{200 + 110 * math.sin(k * math.pi / 5):.0f}" r="55" fill="#FFFFFF" {SW}/>' for k in range(10)) + \
    f'''<circle cx="200" cy="200" r="120" fill="#FFFFFF"/>
<ellipse cx="85" cy="210" rx="45" ry="20" fill="#6E6E78" {SW}/><ellipse cx="315" cy="210" rx="45" ry="20" fill="#6E6E78" {SW}/>
<ellipse cx="200" cy="225" rx="85" ry="100" fill="#FBE3D0" {SW}/>{eyes(165, 235, 205, 14)}
<ellipse cx="200" cy="262" rx="14" ry="9" fill="#FF8FA3"/>{smile(200, 280, 18)}{cheeks(150, 250, 250)}'''
A["piglet"] = f'''<path d="M95 130 L90 50 L170 100 Z" fill="#FF9EB5" {SW}/><path d="M305 130 L310 50 L230 100 Z" fill="#FF9EB5" {SW}/>
<circle cx="200" cy="210" r="130" fill="#FFB3C7" {SW}/>
<ellipse cx="200" cy="250" rx="55" ry="40" fill="#FF8FA8" {SW}/>
<ellipse cx="183" cy="250" rx="9" ry="14" fill="#B5446A"/><ellipse cx="217" cy="250" rx="9" ry="14" fill="#B5446A"/>
{eyes(150, 250, 180, 14)}{smile(200, 305, 22)}'''
A["calf"] = f'''<ellipse cx="80" cy="150" rx="55" ry="25" fill="#FFFFFF" {SW} transform="rotate(-20 80 150)"/>
<ellipse cx="320" cy="150" rx="55" ry="25" fill="#FFFFFF" {SW} transform="rotate(20 320 150)"/>
<path d="M140 80 Q130 50 150 45 L160 85 Z M260 80 Q270 50 250 45 L240 85 Z" fill="#F2D06B" {SW}/>
<ellipse cx="200" cy="200" rx="125" ry="135" fill="#FFFFFF" {SW}/>
<path d="M110 120 Q150 100 160 150 Q130 175 105 160 Z" fill="#2B2B33"/><path d="M265 210 Q300 190 315 230 Q290 255 265 240 Z" fill="#2B2B33"/>
<ellipse cx="200" cy="275" rx="85" ry="55" fill="#FFB3C7" {SW}/>
<ellipse cx="175" cy="275" rx="10" ry="14" fill="#B5446A"/><ellipse cx="225" cy="275" rx="10" ry="14" fill="#B5446A"/>{eyes(155, 245, 185, 15)}'''
A["bunny"] = f'''<ellipse cx="150" cy="95" rx="38" ry="95" fill="#F4F1F6" {SW}/><ellipse cx="250" cy="95" rx="38" ry="95" fill="#F4F1F6" {SW}/>
<ellipse cx="150" cy="100" rx="18" ry="65" fill="#FFB3C7"/><ellipse cx="250" cy="100" rx="18" ry="65" fill="#FFB3C7"/>
<circle cx="200" cy="250" r="120" fill="#F4F1F6" {SW}/>{eyes(160, 240, 235, 15)}
<ellipse cx="200" cy="272" rx="13" ry="9" fill="#FF7A90"/>
<rect x="188" y="285" width="24" height="26" rx="5" fill="#FFFFFF" {SW}/>{cheeks(140, 260, 280)}'''
A["foal"] = f'''<path d="M130 110 L120 40 L175 85 Z M270 110 L280 40 L225 85 Z" fill="#B07A45" {SW}/>
<path d="M165 65 Q200 30 235 65 Q220 100 200 95 Q180 100 165 65 Z" fill="#5A3A22" {SW}/>
<ellipse cx="200" cy="215" rx="105" ry="145" fill="#C68A52" {SW}/>
<ellipse cx="200" cy="305" rx="78" ry="55" fill="#E9C9A2" {SW}/>
<ellipse cx="175" cy="305" rx="9" ry="13" fill="#5A3A22"/><ellipse cx="225" cy="305" rx="9" ry="13" fill="#5A3A22"/>{eyes(160, 240, 185, 15)}'''
A["cub"] = "".join(f'<circle cx="{200 + 128 * math.cos(k * math.pi / 7):.0f}" cy="{210 + 128 * math.sin(k * math.pi / 7):.0f}" r="48" fill="#E07B24" {SW}/>' for k in range(14)) + \
    f'''<circle cx="200" cy="210" r="135" fill="#E07B24"/>
<circle cx="115" cy="120" r="32" fill="#F2B54E" {SW}/><circle cx="285" cy="120" r="32" fill="#F2B54E" {SW}/>
<circle cx="200" cy="215" r="105" fill="#F2B54E" {SW}/>
<ellipse cx="200" cy="262" rx="50" ry="36" fill="#FCE3B0" {SW}/>
<path d="M186 245 L214 245 L200 260 Z" fill="#5A3A22"/>{eyes(160, 240, 195, 14)}{smile(200, 272, 16)}'''
A["elephant"] = f'''<ellipse cx="95" cy="190" rx="80" ry="105" fill="#9A9AA6" {SW}/><ellipse cx="305" cy="190" rx="80" ry="105" fill="#9A9AA6" {SW}/>
<ellipse cx="95" cy="190" rx="50" ry="70" fill="#C9A2AE"/><ellipse cx="305" cy="190" rx="50" ry="70" fill="#C9A2AE"/>
<circle cx="200" cy="180" r="110" fill="#A3A3AF" {SW}/>
<path d="M175 240 Q160 330 200 370 Q235 390 245 360 Q215 350 222 300 Q228 260 225 240 Z" fill="#A3A3AF" {SW}/>
{eyes(160, 240, 165, 13)}{cheeks(140, 260, 205)}'''
A["monkey"] = f'''<circle cx="80" cy="200" r="50" fill="#8B5A2B" {SW}/><circle cx="320" cy="200" r="50" fill="#8B5A2B" {SW}/>
<circle cx="80" cy="200" r="28" fill="#E9C29A"/><circle cx="320" cy="200" r="28" fill="#E9C29A"/>
<circle cx="200" cy="200" r="130" fill="#8B5A2B" {SW}/>
<path d="M200 130 Q150 90 120 150 Q100 230 200 320 Q300 230 280 150 Q250 90 200 130 Z" fill="#E9C29A" {SW}/>
{eyes(165, 235, 185, 14)}<ellipse cx="185" cy="235" rx="5" ry="7" fill="#5A3A22"/><ellipse cx="215" cy="235" rx="5" ry="7" fill="#5A3A22"/>{smile(200, 262, 28)}'''

SH = {}
face = lambda cx, cy: eyes(cx - 35, cx + 35, cy, 13) + smile(cx, cy + 35, 22) + cheeks(cx - 60, cx + 60, cy + 30)
SH["circle"] = f'<circle cx="200" cy="200" r="150" fill="#FF4D6D" {SW}/>' + face(200, 190)
SH["square"] = f'<rect x="60" y="60" width="280" height="280" rx="14" fill="#2E8CFF" {SW}/>' + face(200, 190)
SH["triangle"] = f'<path d="M200 40 L360 340 L40 340 Z" fill="#3BC14A" {SW}/>' + face(200, 240)
SH["star"] = '<path d="' + " ".join(("M" if k == 0 else "L") + f"{200 + (165 if k % 2 == 0 else 72) * math.cos(-math.pi / 2 + k * math.pi / 5):.0f} {210 + (165 if k % 2 == 0 else 72) * math.sin(-math.pi / 2 + k * math.pi / 5):.0f}" for k in range(10)) + f' Z" fill="#FFD23F" {SW}/>' + face(200, 205)
SH["heart"] = f'<path d="M200 350 C40 250 40 110 120 80 C165 64 195 95 200 120 C205 95 235 64 280 80 C360 110 360 250 200 350 Z" fill="#FF6EAA" {SW}/>' + face(200, 175)
SH["rectangle"] = f'<rect x="105" y="30" width="190" height="340" rx="14" fill="#FF9F1C" {SW}/><circle cx="265" cy="210" r="10" fill="{INK}"/>' + face(200, 150)
SH["oval"] = f'<ellipse cx="200" cy="200" rx="120" ry="165" fill="#9B5DE5" {SW}/>' + face(200, 185)
SH["diamond"] = f'<path d="M200 25 L345 200 L200 375 L55 200 Z" fill="#20C9B5" {SW}/>' + face(200, 185)

V = {}
wheel = lambda x, y, r=38: f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2B2B33" {SW}/><circle cx="{x}" cy="{y}" r="{r * 0.42:.0f}" fill="#C9CED6"/>'
V["car"] = f'''<path d="M40 280 L40 220 Q45 195 80 190 L120 185 L160 125 Q170 112 190 112 L270 112 Q290 112 302 128 L340 185 Q370 190 370 215 L370 280 Z" fill="#E8352E" {SW}/>
<path d="M175 130 L250 130 L250 180 L140 180 Z" fill="#BDE6FF" {SW}/><path d="M265 130 L290 130 L325 180 L265 180 Z" fill="#BDE6FF" {SW}/>
<rect x="340" y="205" width="22" height="16" rx="5" fill="#FFE066"/>{wheel(115, 285)}{wheel(295, 285)}'''
V["bus"] = f'''<rect x="25" y="90" width="355" height="200" rx="26" fill="#FFC21A" {SW}/>
{"".join(f'<rect x="{x}" y="120" width="56" height="60" rx="8" fill="#BDE6FF" {SW}/>' for x in (50, 120, 190, 260))}
<rect x="320" y="120" width="44" height="120" rx="8" fill="#BDE6FF" {SW}/>
<rect x="25" y="205" width="355" height="18" fill="#2B2B33"/>{wheel(100, 290)}{wheel(300, 290)}'''
V["firetruck"] = f'''<rect x="20" y="140" width="250" height="140" rx="12" fill="#E8352E" {SW}/>
<path d="M270 140 L330 140 L375 200 L375 280 L270 280 Z" fill="#E8352E" {SW}/>
<path d="M285 155 L325 155 L355 200 L285 200 Z" fill="#BDE6FF" {SW}/>
<rect x="30" y="95" width="230" height="22" rx="6" fill="#C9CED6" {SW}/>
{"".join(f'<path d="M{x} 95 L{x} 117" stroke="{INK}" stroke-width="5"/>' for x in range(55, 260, 30))}
<rect x="300" y="115" width="34" height="22" rx="6" fill="#4DA3FF" {SW}/>
<rect x="20" y="215" width="250" height="14" fill="#FFFFFF"/>{wheel(85, 285)}{wheel(230, 285)}{wheel(330, 285)}'''
V["police"] = f'''<path d="M40 280 L40 220 Q45 195 80 190 L120 185 L160 125 Q170 112 190 112 L270 112 Q290 112 302 128 L340 185 Q370 190 370 215 L370 280 Z" fill="#FFFFFF" {SW}/>
<path d="M40 225 L370 225 L370 262 L40 262 Z" fill="#2E5AAC"/>
<path d="M175 130 L250 130 L250 180 L140 180 Z" fill="#BDE6FF" {SW}/><path d="M265 130 L290 130 L325 180 L265 180 Z" fill="#BDE6FF" {SW}/>
<rect x="185" y="88" width="34" height="24" rx="6" fill="#FF3B3B" {SW}/><rect x="219" y="88" width="34" height="24" rx="6" fill="#2E8CFF" {SW}/>
{wheel(115, 285)}{wheel(295, 285)}'''
V["ambulance"] = f'''<rect x="20" y="110" width="270" height="170" rx="14" fill="#FFFFFF" {SW}/>
<path d="M290 150 L335 150 L375 205 L375 280 L290 280 Z" fill="#FFFFFF" {SW}/><path d="M300 165 L330 165 L358 205 L300 205 Z" fill="#BDE6FF" {SW}/>
<path d="M125 150 L165 150 L165 180 L195 180 L195 220 L165 220 L165 250 L125 250 L125 220 L95 220 L95 180 L125 180 Z" fill="#E8352E"/>
<rect x="20" y="255" width="355" height="12" fill="#E8352E"/><rect x="140" y="88" width="40" height="22" rx="6" fill="#FF3B3B" {SW}/>
{wheel(90, 285)}{wheel(300, 285)}'''
V["train"] = f'''<circle cx="110" cy="70" r="26" fill="#E6E9EE"/><circle cx="85" cy="45" r="20" fill="#E6E9EE"/><circle cx="60" cy="25" r="15" fill="#E6E9EE"/>
<rect x="95" y="95" width="40" height="70" rx="6" fill="#2B2B33" {SW}/>
<rect x="40" y="160" width="230" height="110" rx="14" fill="#3BC14A" {SW}/>
<rect x="240" y="100" width="130" height="170" rx="14" fill="#2E8CFF" {SW}/><rect x="265" y="125" width="80" height="60" rx="8" fill="#BDE6FF" {SW}/>
<path d="M40 270 L20 300 L60 300 Z" fill="#E8352E" {SW}/>{wheel(95, 295, 34)}{wheel(185, 295, 34)}{wheel(305, 295, 34)}'''
V["airplane"] = f'''<path d="M40 210 Q40 170 90 165 L310 160 Q370 165 380 200 Q370 240 310 240 L90 240 Q40 240 40 210 Z" fill="#FFFFFF" {SW}/>
<path d="M60 170 L30 80 L90 80 L130 165 Z" fill="#2E8CFF" {SW}/>
<path d="M170 235 L120 330 L190 330 L250 235 Z" fill="#2E8CFF" {SW}/><path d="M180 165 L140 100 L195 100 L240 165 Z" fill="#2E8CFF" {SW}/>
{"".join(f'<circle cx="{x}" cy="200" r="11" fill="#BDE6FF" {SW}/>' for x in (150, 190, 230, 270))}
<path d="M330 180 Q360 185 365 205 L330 205 Z" fill="#BDE6FF" {SW}/>'''
V["boat"] = f'''<path d="M195 60 L195 250" stroke="{INK}" stroke-width="8"/>
<path d="M200 70 L320 230 L200 230 Z" fill="#FFFFFF" {SW}/><path d="M190 100 L100 230 L190 230 Z" fill="#FFD23F" {SW}/>
<path d="M40 250 L360 250 L320 320 L80 320 Z" fill="#E8352E" {SW}/>
<path d="M20 340 Q70 315 120 340 Q170 365 220 340 Q270 315 320 340 Q360 360 390 340" fill="none" stroke="#2E8CFF" stroke-width="10" stroke-linecap="round"/>'''
V["tractor"] = f'''<rect x="60" y="170" width="190" height="90" rx="12" fill="#3BC14A" {SW}/>
<path d="M170 90 L260 90 L260 210 L170 210 Z" fill="#3BC14A" {SW}/><rect x="185" y="105" width="60" height="55" rx="6" fill="#BDE6FF" {SW}/>
<rect x="90" y="110" width="20" height="60" fill="#2B2B33" {SW}/>
<circle cx="280" cy="265" r="75" fill="#2B2B33" {SW}/><circle cx="280" cy="265" r="35" fill="#FFD23F" {SW}/>{wheel(105, 290, 42)}'''
V["helicopter"] = f'''<path d="M60 70 L340 70" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><rect x="190" y="70" width="20" height="45" fill="#2B2B33"/>
<path d="M70 200 Q70 120 170 115 L250 115 Q320 120 320 200 Q320 270 230 270 L160 270 Q70 270 70 200 Z" fill="#FF9F1C" {SW}/>
<path d="M300 190 L385 175 L385 215 L300 215 Z" fill="#FF9F1C" {SW}/><path d="M370 150 L370 240" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
<path d="M95 190 Q100 140 160 140 L160 210 L95 210 Z" fill="#BDE6FF" {SW}/>
<path d="M110 300 L300 300 M150 270 L140 300 M260 270 L270 300" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'''

WX = {}
sunface = eyes(170, 230, 190, 11) + smile(200, 225, 20)
WX["sunny"] = "".join(f'<path d="M{200 + 110 * math.cos(k * math.pi / 6):.0f} {200 + 110 * math.sin(k * math.pi / 6):.0f} L{200 + 175 * math.cos(k * math.pi / 6):.0f} {200 + 175 * math.sin(k * math.pi / 6):.0f}" stroke="#FFB800" stroke-width="18" stroke-linecap="round"/>' for k in range(12)) + \
    f'<circle cx="200" cy="200" r="95" fill="#FFD23F" {SW}/>' + sunface + cheeks(150, 250, 222)
cloud = lambda dx, dy, col, s=1.0: f'<g transform="translate({dx} {dy}) scale({s})"><path d="M90 250 Q35 250 40 200 Q46 152 100 156 Q104 92 168 94 Q200 40 258 72 Q318 54 328 124 Q372 134 366 192 Q362 250 310 250 Z" fill="{col}" {SW}/></g>'
WX["rainy"] = cloud(0, -20, "#B8C2CE") + "".join(f'<path d="M{x} {y} Q{x - 12} {y + 30} {x} {y + 40} Q{x + 12} {y + 30} {x} {y} Z" fill="#2E8CFF" {SW}/>' for x, y in ((110, 270), (180, 300), (250, 270), (320, 300), (145, 340), (285, 340)))
WX["cloudy"] = cloud(-30, 10, "#D7DEE7", 0.8) + cloud(90, 60, "#B8C2CE", 0.8) + eyes(250, 300, 220, 10) + smile(275, 245, 16)
WX["windy"] = "".join(f'<path d="M30 {y} Q200 {y - 40} 260 {y} Q330 {y + 40} 340 {y - 20} Q345 {y - 60} 300 {y - 55}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>' for y in (130, 220, 310) for c, w in (("#2B4E8C", 24), ("#FFFFFF", 12))) + \
    f'<path d="M300 90 Q330 60 360 95 Q330 120 300 90 Z" fill="#4CAF3E" {SW}/><path d="M80 330 Q110 300 140 335 Q110 360 80 330 Z" fill="#FF9F1C" {SW}/>'
flake = lambda x, y, r=24: "".join(f'<path d="M{x - r * math.cos(k * math.pi / 3):.0f} {y - r * math.sin(k * math.pi / 3):.0f} L{x + r * math.cos(k * math.pi / 3):.0f} {y + r * math.sin(k * math.pi / 3):.0f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>' for c, w in (("#2B4E8C", 13), ("#FFFFFF", 6)) for k in range(3))
WX["snowy"] = cloud(0, -20, "#E6EEF7") + "".join(flake(x, y) for x, y in ((110, 290), (200, 320), (290, 290), (155, 360), (250, 360)))
WX["rainbow"] = "".join(f'<path d="M{40 + k * 22} 300 A{160 - k * 22} {160 - k * 22} 0 0 1 {360 - k * 22} 300" fill="none" stroke="{c}" stroke-width="22"/>' for k, c in enumerate(["#FF4D6D", "#FF9F1C", "#FFD23F", "#3BC14A", "#2E8CFF", "#9B5DE5"])) + \
    cloud(-20, 140, "#FFFFFF", 0.42) + cloud(250, 140, "#FFFFFF", 0.42)

OC = {}
OC["fish"] = f'''<path d="M290 200 L380 130 L370 200 L380 270 Z" fill="#FF8A1F" {SW}/>
<ellipse cx="180" cy="200" rx="140" ry="95" fill="#FF8A1F" {SW}/>
<path d="M150 108 Q165 200 150 292" fill="none" stroke="#FFFFFF" stroke-width="22"/><path d="M230 112 Q245 200 230 288" fill="none" stroke="#FFFFFF" stroke-width="22"/>
{eyes(95, 95, 180, 16)}{smile(95, 225, 14)}'''
OC["octopus"] = "".join(f'<path d="M{110 + k * 26} 250 Q{95 + k * 26 + (20 if k % 2 else -20)} 320 {115 + k * 26} 370" fill="none" stroke="#3A2420" stroke-width="30" stroke-linecap="round"/><path d="M{110 + k * 26} 250 Q{95 + k * 26 + (20 if k % 2 else -20)} 320 {115 + k * 26} 370" fill="none" stroke="#B57BFF" stroke-width="20" stroke-linecap="round"/>' for k in range(8)) + \
    f'<ellipse cx="200" cy="180" rx="130" ry="120" fill="#B57BFF" {SW}/>' + eyes(160, 240, 175, 16) + smile(200, 220, 22) + cheeks(130, 270, 210)
OC["whale"] = f'''<path d="M300 170 Q330 90 390 80 Q370 140 330 180 Z" fill="#4D8FE0" {SW}/>
<path d="M30 220 Q30 110 170 105 Q300 100 330 190 Q340 290 190 300 Q30 305 30 220 Z" fill="#4D8FE0" {SW}/>
<path d="M50 240 Q190 290 320 230 Q300 290 190 298 Q70 300 50 240 Z" fill="#CFE3FA"/>
<path d="M150 100 Q140 60 120 50 M150 100 Q160 55 185 45 M150 100 Q150 55 150 35" fill="none" stroke="#7FC4FF" stroke-width="10" stroke-linecap="round"/>
{eyes(110, 110, 190, 15)}{smile(120, 230, 18)}'''
OC["crab"] = f'''<path d="M70 230 Q20 160 70 110 Q100 140 90 170 Q120 150 110 120" fill="#F2472C" {SW}/>
<path d="M330 230 Q380 160 330 110 Q300 140 310 170 Q280 150 290 120" fill="#F2472C" {SW}/>
{"".join(f'<path d="M{x} 270 L{x + d} 330" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M{x} 270 L{x + d} 330" stroke="#F2472C" stroke-width="8" stroke-linecap="round"/>' for x, d in ((120, -30), (150, -20), (250, 20), (280, 30)))}
<ellipse cx="200" cy="240" rx="125" ry="75" fill="#F2472C" {SW}/>
<path d="M165 175 L160 120 M235 175 L240 120" stroke="{INK}" stroke-width="7"/>
<circle cx="160" cy="115" r="20" fill="#FFFFFF" {SW}/><circle cx="240" cy="115" r="20" fill="#FFFFFF" {SW}/>
<circle cx="160" cy="118" r="9" fill="#2B1B17"/><circle cx="240" cy="118" r="9" fill="#2B1B17"/>{smile(200, 245, 28)}'''
OC["turtle"] = f'''<circle cx="335" cy="215" r="48" fill="#8BD07A" {SW}/>
<ellipse cx="110" cy="300" rx="30" ry="22" fill="#8BD07A" {SW}/><ellipse cx="270" cy="300" rx="30" ry="22" fill="#8BD07A" {SW}/>
<path d="M40 280 Q40 120 190 120 Q320 120 320 280 Z" fill="#3E9E35" {SW}/>
<path d="M130 160 L180 140 L230 160 L235 210 L180 235 L125 210 Z M80 260 L125 210 M180 235 L180 280 M235 210 L290 260" fill="#6CC05B" stroke="#2E7D32" stroke-width="7"/>
<rect x="35" y="270" width="290" height="22" rx="10" fill="#C9E7A6" {SW}/>{eyes(345, 345, 205, 11)}{smile(345, 235, 12)}'''
OC["starfish"] = '<path d="' + " ".join(("M" if k == 0 else "L") + f"{200 + (170 if k % 2 == 0 else 80) * math.cos(-math.pi / 2 + k * math.pi / 5):.0f} {210 + (170 if k % 2 == 0 else 80) * math.sin(-math.pi / 2 + k * math.pi / 5):.0f}" for k in range(10)) + f' Z" fill="#FF8A5B" {SW}/>' + \
    "".join(f'<circle cx="{200 + 110 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5):.0f}" cy="{210 + 110 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5):.0f}" r="9" fill="#FFD2B8"/>' for k in range(5)) + face(200, 200)
OC["dolphin"] = f'''<path d="M70 240 L15 190 L30 248 L15 305 Z" fill="#5FA3E8" {SW}/>
<path d="M190 140 Q205 70 255 60 Q245 110 250 142 Z" fill="#5FA3E8" {SW}/>
<path d="M55 245 Q110 130 250 135 Q330 138 355 180 Q385 190 385 205 Q385 215 350 212 L320 212 Q300 280 200 285 Q100 290 55 245 Z" fill="#5FA3E8" {SW}/>
<path d="M95 255 Q200 300 320 215 Q300 270 205 280 Q130 285 95 255 Z" fill="#DCEBFA"/>
<circle cx="300" cy="175" r="13" fill="#2B1B17"/><circle cx="296" cy="170" r="5" fill="#FFFFFF"/>
<path d="M330 205 Q350 215 370 208" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>{cheeks(270, 270, 205)}'''
OC["jellyfish"] = "".join(f'<path d="M{110 + k * 36} 220 Q{95 + k * 36} 280 {115 + k * 36} 330 Q{130 + k * 36} 360 {110 + k * 36} 385" fill="none" stroke="#FF6EAA" stroke-width="10" stroke-linecap="round"/>' for k in range(6)) + \
    f'<path d="M60 230 Q60 70 200 70 Q340 70 340 230 Q300 250 270 230 Q235 255 200 230 Q165 255 130 230 Q95 255 60 230 Z" fill="#FFB3D9" {SW}/>' + face(200, 160)
OC["fish"] = OC["fish"].replace(eyes(95, 95, 180, 16), f'<circle cx="95" cy="180" r="16" fill="#2B1B17"/><circle cx="90" cy="174" r="6" fill="#FFFFFF"/>')


def bg_beach():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{sky_and_clouds(1920)}
    <rect x="0" y="560" width="1920" height="260" fill="#2E9BE6"/>
    {"".join(f'<path d="M{x} {y} q40 -20 80 0" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.8"/>' for x, y in ((120, 620), (520, 680), (900, 610), (1300, 700), (1650, 640), (300, 760), (1100, 760)))}
    <path d="M0 800 Q480 760 960 790 Q1440 820 1920 780 L1920 1080 L0 1080 Z" fill="#F7DC9C"/>
    <path d="M0 800 Q480 760 960 790 Q1440 820 1920 780" fill="none" stroke="#FFFFFF" stroke-width="16"/>
    <g transform="translate(1500 900)"><path d="M0 0 L40 -70 L80 0 Z" fill="#FF6E6E" {SW}/><rect x="-20" y="0" width="120" height="20" rx="8" fill="#FFD23F" {SW}/></g>
    <circle cx="420" cy="960" r="26" fill="#FF8A5B" {SW}/></svg>'''
    shot(f'<html><body style="margin:0">{svg}</body></html>', str(OUT / "bg_beach.png"), 1920, 1080)


ITEMS = {**A, **SH, **V, **WX, **OC}


def render_items():
    names = list(ITEMS)
    for start in range(0, len(names), 12):
        chunk = names[start:start + 12]
        cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{ITEMS[n]}</svg></div>'
                        for i, n in enumerate(chunk))
        w = 400 * len(chunk)
        shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>',
             str(OUT / "_items.png"), w, 400, scale=2)
        im = Image.open(OUT / "_items.png")
        for i, n in enumerate(chunk):
            im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"fruit_{n}.png")
        (OUT / "_items.png").unlink()


def render_counting():
    """n1..n10: a big number plus that many fruits."""
    fruit = ["apple", "banana", "orange", "strawberry", "lemon", "cherry", "pear", "kiwi", "pineapple", "mango"]
    from PIL import ImageFont
    f = ImageFont.truetype("C:/Windows/Fonts/seguibl.ttf", 230)
    rb = [(255, 77, 109), (255, 159, 28), (255, 200, 40), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
    for n in range(1, 11):
        im = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        txt = str(n)
        w = d.textlength(txt, font=f)
        d.text((400 - w / 2, 20), txt, font=f, fill=rb[(n - 1) % 6], stroke_width=16, stroke_fill=(58, 36, 32))
        src = Image.open(FRUIT_ART / f"fruit_{fruit[n - 1]}.png")
        per_row = 1 if n == 1 else (n if n <= 3 else (min(5, (n + 1) // 2)))
        rows = (n + per_row - 1) // per_row
        size = int(min(320, 760 / per_row, 470 / rows))
        top = 300 + (470 - rows * size) // 2
        k = 0
        for r in range(rows):
            cnt = min(per_row, n - k)
            left = 400 - cnt * size // 2
            for c in range(cnt):
                im.alpha_composite(src.resize((size, size), Image.LANCZOS), (left + c * size, top + r * size))
                k += 1
        im.save(OUT / f"fruit_n{n}.png")


if __name__ == "__main__":
    bg_farm()
    bg_road()
    bg_beach()
    render_items()
    render_counting()
    keys = list(ITEMS) + [f"n{n}" for n in range(1, 11)]
    cols = 10
    sheet = Image.new("RGB", (cols * 160, ((len(keys) + cols - 1) // cols) * 160 + 280), (126, 200, 255))
    for i, k in enumerate(keys):
        t = Image.open(OUT / f"fruit_{k}.png").resize((150, 150))
        sheet.paste(t, ((i % cols) * 160 + 5, (i // cols) * 160 + 5), t)
    y = ((len(keys) + cols - 1) // cols) * 160
    sheet.paste(Image.open(OUT / "bg_farm.png").resize((480, 270)), (0, y + 5))
    sheet.paste(Image.open(OUT / "bg_road.png").resize((480, 270)), (500, y + 5))
    sheet.save(HERE / "_art_check.png")
    print("ok", len(keys))
