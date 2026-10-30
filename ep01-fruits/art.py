"""Static art for episode 1: garden background + 10 fruits (SVG -> PNG via headless Chrome)."""
import pathlib, subprocess, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SW = 'stroke="#3A2420" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'


def shot(html, out, w, h, scale=1):
    tmp = HERE / "_r.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={out}", tmp.as_uri()], check=True, capture_output=True)
    tmp.unlink()


def background():
    flowers = []
    import random
    rnd = random.Random(4)
    for _ in range(26):
        x, y = rnd.uniform(40, 1880), rnd.uniform(880, 1060)
        col = rnd.choice(["#FF6B8B", "#FFD23F", "#FFFFFF", "#B57BFF", "#FF9F43"])
        r = rnd.uniform(9, 14)
        petals = "".join(f'<circle cx="{x + r * 1.1 * c}" cy="{y + r * 1.1 * s}" r="{r}" fill="{col}"/>'
                         for c, s in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        flowers.append(petals + f'<circle cx="{x}" cy="{y}" r="{r * 0.8}" fill="#FFB800"/>')
    clouds = []
    for cx, cy, s in ((300, 170, 1.0), (1000, 110, 0.8), (1600, 200, 1.1)):
        clouds.append(f'<g transform="translate({cx} {cy}) scale({s})" fill="#FFFFFF">'
                      '<ellipse cx="0" cy="0" rx="110" ry="55"/><ellipse cx="-80" cy="20" rx="70" ry="45"/>'
                      '<ellipse cx="85" cy="18" rx="80" ry="48"/><ellipse cx="10" cy="-35" rx="70" ry="50"/></g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
    <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7EC8FF"/><stop offset="1" stop-color="#D8F1FF"/></linearGradient></defs>
    <rect width="1920" height="1080" fill="url(#sky)"/>
    <circle cx="1720" cy="150" r="90" fill="#FFE066"/><circle cx="1720" cy="150" r="120" fill="#FFE066" opacity="0.3"/>
    {''.join(clouds)}
    <path d="M0 690 Q300 560 640 650 Q980 740 1300 620 Q1620 520 1920 640 L1920 1080 L0 1080 Z" fill="#9BDB6B"/>
    <path d="M0 780 Q420 700 900 770 Q1400 840 1920 740 L1920 1080 L0 1080 Z" fill="#7CCB4F"/>
    <!-- tree left -->
    <rect x="120" y="440" width="60" height="330" rx="20" fill="#9A6A43" {SW}/>
    <circle cx="150" cy="400" r="150" fill="#5DBB46" {SW}/>
    <circle cx="80" cy="440" r="90" fill="#5DBB46"/><circle cx="230" cy="430" r="95" fill="#5DBB46"/>
    <circle cx="110" cy="380" r="16" fill="#E8483B"/><circle cx="200" cy="450" r="16" fill="#E8483B"/><circle cx="160" cy="330" r="16" fill="#E8483B"/>
    <!-- bush right -->
    <ellipse cx="1800" cy="820" rx="170" ry="100" fill="#5DBB46" {SW}/>
    <rect x="0" y="960" width="1920" height="120" fill="#6CBF45"/>
    {''.join(flowers)}
    </svg>'''
    shot(f'<html><body style="margin:0">{svg}</body></html>', str(OUT / "bg.png"), 1920, 1080)


# 400x400 fruit drawings, centred
FRUIT_SVG = {
    "apple": f'''<path d="M200 110 C140 70 60 100 60 200 C60 300 130 360 200 340 C270 360 340 300 340 200 C340 100 260 70 200 110 Z" fill="#E8352E" {SW}/>
      <path d="M200 112 Q205 70 222 50" fill="none" stroke="#6B4226" stroke-width="12" stroke-linecap="round"/>
      <path d="M215 80 Q270 40 300 75 Q255 105 215 80 Z" fill="#5DBB46" {SW}/>
      <ellipse cx="130" cy="170" rx="22" ry="42" fill="#FFFFFF" opacity="0.45" transform="rotate(20 130 170)"/>''',
    "banana": f'''<path d="M90 120 Q60 300 230 340 Q330 360 350 300 Q260 320 200 280 Q120 220 130 110 Z" fill="#FFD93B" {SW}/>
      <path d="M130 110 L120 75 L95 80 L90 120 Z" fill="#7A5A2E" {SW}/>
      <path d="M150 170 Q170 260 260 300" fill="none" stroke="#E5B820" stroke-width="8" stroke-linecap="round"/>''',
    "orange": f'''<circle cx="200" cy="210" r="140" fill="#FF9420" {SW}/>
      <path d="M200 72 Q210 55 225 50" fill="none" stroke="#6B4226" stroke-width="10" stroke-linecap="round"/>
      <path d="M210 70 Q260 40 290 70 Q250 95 210 70 Z" fill="#5DBB46" {SW}/>
      <g fill="#E07A0E">{''.join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x, y in ((150, 180), (250, 160), (220, 260), (160, 280), (280, 230), (190, 210)))}</g>
      <ellipse cx="140" cy="150" rx="25" ry="40" fill="#FFFFFF" opacity="0.4" transform="rotate(30 140 150)"/>''',
    "grapes": f'''<path d="M200 70 Q205 45 225 35" fill="none" stroke="#6B4226" stroke-width="10" stroke-linecap="round"/>
      <path d="M215 60 Q265 30 295 65 Q255 90 215 60 Z" fill="#5DBB46" {SW}/>
      {''.join(f'<circle cx="{x}" cy="{y}" r="42" fill="#8E44C9" {SW}/><circle cx="{x - 12}" cy="{y - 12}" r="9" fill="#FFFFFF" opacity="0.5"/>'
               for x, y in ((140, 120), (220, 115), (290, 125), (175, 190), (255, 190), (140, 255), (215, 260), (280, 250), (180, 325), (245, 320)))}''',
    "strawberry": f'''<path d="M200 350 C110 300 60 200 90 140 C120 95 280 95 310 140 C340 200 290 300 200 350 Z" fill="#F0313A" {SW}/>
      <path d="M200 110 L150 80 L170 120 L120 115 L165 140 L200 125 L235 140 L280 115 L230 120 L250 80 Z" fill="#4CAF3E" {SW}/>
      <g fill="#FFE27A">{''.join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="8"/>' for x, y in ((150, 180), (200, 170), (250, 180), (130, 230), (180, 230), (230, 230), (270, 225), (160, 280), (210, 285), (245, 275), (195, 325)))}</g>''',
    "watermelon": f'''<path d="M40 150 L360 150 A160 160 0 0 1 40 150 Z" fill="#4CAF3E" {SW}/>
      <path d="M62 150 L338 150 A138 138 0 0 1 62 150 Z" fill="#F7F3D5"/>
      <path d="M76 150 L324 150 A124 124 0 0 1 76 150 Z" fill="#F44957"/>
      <g fill="#2B1B17">{''.join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="11"/>' for x, y in ((140, 190), (200, 205), (260, 190), (170, 240), (230, 240), (200, 175)))}</g>''',
    "mango": f'''<ellipse cx="200" cy="220" rx="160" ry="112" fill="#FFB627" transform="rotate(-35 200 220)" {SW}/>
      <clipPath id="mclip"><ellipse cx="200" cy="220" rx="156" ry="108" transform="rotate(-35 200 220)"/></clipPath>
      <g clip-path="url(#mclip)">
      <ellipse cx="140" cy="160" rx="100" ry="70" fill="#9BCB3C" opacity="0.55" transform="rotate(-35 140 160)"/>
      <ellipse cx="265" cy="285" rx="90" ry="55" fill="#FF6A2B" opacity="0.45" transform="rotate(-35 265 285)"/></g>
      <ellipse cx="200" cy="220" rx="160" ry="112" fill="none" transform="rotate(-35 200 220)" {SW}/>
      <path d="M295 105 Q305 75 325 62" fill="none" stroke="#6B4226" stroke-width="10" stroke-linecap="round"/>
      <path d="M310 80 Q360 40 392 80 Q350 108 310 80 Z" fill="#5DBB46" {SW}/>
      <ellipse cx="140" cy="230" rx="18" ry="40" fill="#FFFFFF" opacity="0.4" transform="rotate(-35 140 230)"/>''',
    "pineapple": f'''
      <path d="M200 150 Q140 125 112 70 Q170 90 206 132 Z" fill="#3E9E35" {SW}/>
      <path d="M200 150 Q260 125 288 70 Q230 90 194 132 Z" fill="#3E9E35" {SW}/>
      <path d="M200 145 Q160 90 168 28 Q205 80 210 140 Z" fill="#4CAF3E" {SW}/>
      <path d="M200 145 Q240 90 232 28 Q195 80 190 140 Z" fill="#4CAF3E" {SW}/>
      <path d="M200 140 Q185 70 200 8 Q215 70 200 140 Z" fill="#5DBB46" {SW}/>
      <ellipse cx="200" cy="255" rx="115" ry="135" fill="#F7B731" {SW}/>
      <g stroke="#C98A12" stroke-width="6" fill="none">
        <path d="M110 190 L260 370 M130 150 L300 340 M170 125 L310 280 M90 250 L200 385"/>
        <path d="M290 190 L140 370 M270 150 L100 340 M230 125 L90 280 M310 250 L200 385"/></g>''',
    "cherry": f'''<path d="M200 60 Q160 140 130 250" fill="none" stroke="#5B8C2A" stroke-width="10" stroke-linecap="round"/>
      <path d="M200 60 Q240 150 270 240" fill="none" stroke="#5B8C2A" stroke-width="10" stroke-linecap="round"/>
      <path d="M200 60 Q260 30 300 70 Q250 95 200 60 Z" fill="#5DBB46" {SW}/>
      <circle cx="130" cy="290" r="70" fill="#C8102E" {SW}/><circle cx="270" cy="280" r="70" fill="#C8102E" {SW}/>
      <circle cx="105" cy="265" r="15" fill="#FFFFFF" opacity="0.5"/><circle cx="245" cy="255" r="15" fill="#FFFFFF" opacity="0.5"/>''',
    "lemon": f'''<path d="M30 210 Q70 190 90 150 Q140 105 200 105 Q260 105 310 150 Q330 190 370 210 Q330 230 310 270 Q260 315 200 315 Q140 315 90 270 Q70 230 30 210 Z" fill="#FFE135" {SW}/>
      <path d="M200 106 Q210 80 228 70" fill="none" stroke="#6B4226" stroke-width="10" stroke-linecap="round"/>
      <path d="M215 85 Q265 50 300 82 Q255 110 215 85 Z" fill="#5DBB46" {SW}/>
      <ellipse cx="140" cy="170" rx="40" ry="16" fill="#FFFFFF" opacity="0.45" transform="rotate(-15 140 170)"/>''',
    "kiwi": f'''<circle cx="150" cy="215" r="125" fill="#8B5A2B" {SW}/>
      <g fill="#6E4520">{''.join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x, y in ((90, 170), (120, 280), (200, 150), (80, 240), (170, 300), (210, 230)))}</g>
      <circle cx="255" cy="215" r="120" fill="#7A4E26" {SW}/>
      <circle cx="255" cy="215" r="104" fill="#8BC53F"/>
      <circle cx="255" cy="215" r="44" fill="#F4F1C9"/>
      <g fill="#2B1B17">{''.join(f'<ellipse cx="{255 + 62 * __import__("math").cos(k * 0.5236):.1f}" cy="{215 + 62 * __import__("math").sin(k * 0.5236):.1f}" rx="5" ry="9" transform="rotate({k * 30 + 90} {255 + 62 * __import__("math").cos(k * 0.5236):.1f} {215 + 62 * __import__("math").sin(k * 0.5236):.1f})"/>' for k in range(12))}</g>''',
    "pear": f'''<path d="M200 80 C160 80 150 140 140 180 C90 220 80 340 200 350 C320 340 310 220 260 180 C250 140 240 80 200 80 Z" fill="#A6D44A" {SW}/>
      <path d="M200 82 Q205 55 220 45" fill="none" stroke="#6B4226" stroke-width="10" stroke-linecap="round"/>
      <path d="M212 62 Q262 30 292 66 Q250 90 212 62 Z" fill="#4CAF3E" {SW}/>
      <ellipse cx="160" cy="250" rx="20" ry="40" fill="#FFFFFF" opacity="0.4" transform="rotate(20 160 250)"/>''',
}


def fruits():
    names = list(FRUIT_SVG)
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{FRUIT_SVG[n]}</svg></div>'
                    for i, n in enumerate(names))
    w = 400 * len(names)
    shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>',
         str(OUT / "_fruits.png"), w, 400, scale=2)
    im = Image.open(OUT / "_fruits.png")
    for i, n in enumerate(names):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"fruit_{n}.png")
    (OUT / "_fruits.png").unlink()


def background_vertical():
    import random
    rnd = random.Random(5)
    flowers = []
    for _ in range(30):
        x, y = rnd.uniform(30, 1050), rnd.uniform(1640, 1900)
        col = rnd.choice(["#FF6B8B", "#FFD23F", "#FFFFFF", "#B57BFF", "#FF9F43"])
        r = rnd.uniform(9, 14)
        flowers.append("".join(f'<circle cx="{x + r * 1.1 * c}" cy="{y + r * 1.1 * s}" r="{r}" fill="{col}"/>'
                               for c, s in ((1, 0), (-1, 0), (0, 1), (0, -1))) + f'<circle cx="{x}" cy="{y}" r="{r * 0.8}" fill="#FFB800"/>')
    clouds = "".join(f'<g transform="translate({cx} {cy}) scale({sc})" fill="#FFFFFF"><ellipse cx="0" cy="0" rx="110" ry="55"/>'
                     f'<ellipse cx="-80" cy="20" rx="70" ry="45"/><ellipse cx="85" cy="18" rx="80" ry="48"/><ellipse cx="10" cy="-35" rx="70" ry="50"/></g>'
                     for cx, cy, sc in ((180, 330, 0.9), (860, 260, 0.8), (620, 520, 0.6)))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
    <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7EC8FF"/><stop offset="1" stop-color="#D8F1FF"/></linearGradient></defs>
    <rect width="1080" height="1920" fill="url(#sky)"/>
    <circle cx="930" cy="150" r="85" fill="#FFE066"/><circle cx="930" cy="150" r="115" fill="#FFE066" opacity="0.3"/>
    {clouds}
    <path d="M0 1240 Q270 1140 560 1220 Q840 1300 1080 1200 L1080 1920 L0 1920 Z" fill="#9BDB6B"/>
    <path d="M0 1380 Q300 1320 600 1370 Q860 1420 1080 1350 L1080 1920 L0 1920 Z" fill="#7CCB4F"/>
    <rect x="0" y="1780" width="1080" height="140" fill="#6CBF45"/>
    {''.join(flowers)}
    </svg>'''
    shot(f'<html><body style="margin:0">{svg}</body></html>', str(OUT / "bg_vertical.png"), 1080, 1920)


if __name__ == "__main__":
    background()
    background_vertical()
    fruits()
    sheet = Image.new("RGB", (2000, 400 + 1080 // 2), "#FFFFFF")
    sheet.paste(Image.open(OUT / "bg.png").resize((960, 540)), (0, 400))
    for i, n in enumerate(FRUIT_SVG):
        f = Image.open(OUT / f"fruit_{n}.png").resize((200, 200))
        sheet.paste(f, (i * 200, 0), f)
    sheet.save(HERE / "_art_check.png")
    print("ok")
