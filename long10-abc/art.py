"""New props + backgrounds for Long video 10 "ABC Phonics" (everything else reuses earlier art).
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


def eyes(x1, x2, y, r=14):
    return (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{x1 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/><circle cx="{x2 + r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.35}" fill="#FFF"/>')


I = {}
I["queen"] = f'''<path d="M110 380 Q120 250 200 240 Q280 250 290 380 Z" fill="#B79BEA" {SW}/>
<path d="M150 380 L170 300 L200 330 L230 300 L250 380" fill="#FFD23F" stroke="{INK}" stroke-width="5"/>
<circle cx="200" cy="170" r="72" fill="#F2C29B" {SW}/>
<path d="M128 175 Q120 95 200 92 Q280 95 272 175 Q262 130 200 128 Q138 130 128 175 Z" fill="#6A3523" {SW}/>
<path d="M140 100 L150 40 L180 80 L200 30 L220 80 L250 40 L260 100 Z" fill="#FFD23F" {SW}/>
<circle cx="200" cy="55" r="9" fill="#FF4D6D"/><circle cx="160" cy="70" r="7" fill="#4CC9F0"/><circle cx="240" cy="70" r="7" fill="#4CC9F0"/>
{eyes(178, 222, 168, 11)}<ellipse cx="160" cy="195" rx="14" ry="9" fill="#FF8FA3" opacity="0.7"/><ellipse cx="240" cy="195" rx="14" ry="9" fill="#FF8FA3" opacity="0.7"/>
<path d="M182 200 Q200 216 218 200" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'''
I["violin"] = f'''<path d="M200 20 L200 120" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M200 20 L200 120" stroke="#5A3A22" stroke-width="12" stroke-linecap="round"/>
<path d="M200 110 Q130 110 135 175 Q140 205 165 215 Q130 230 128 290 Q130 370 200 375 Q270 370 272 290 Q270 230 235 215 Q260 205 265 175 Q270 110 200 110 Z" fill="#C9752E" {SW}/>
<path d="M175 240 q-10 20 0 40 M225 240 q10 20 0 40" stroke="{INK}" stroke-width="5" fill="none"/>
<path d="M190 120 L190 340 M210 120 L210 340" stroke="#F2E6C9" stroke-width="3"/><rect x="175" y="330" width="50" height="16" rx="6" fill="#3A2420"/>
<path d="M330 60 L90 330" stroke="#8A5A2B" stroke-width="10" stroke-linecap="round"/><path d="M325 70 L95 330" stroke="#F2E6C9" stroke-width="3"/>'''
I["xylophone"] = f'''<path d="M60 330 L340 300 M60 130 L340 160" stroke="#8A5A2B" stroke-width="16" stroke-linecap="round"/>''' + \
    "".join(f'<rect x="{70 + i * 38}" y="{130 + i * 4}" width="30" height="{200 - i * 12}" rx="8" fill="{c}" {SW}/>'
            for i, c in enumerate(("#FF4D6D", "#FF9F1C", "#FFD23F", "#7ED957", "#4CC9F0", "#4C79D8", "#9B5DE5"))) + \
    f'''<path d="M300 40 L250 150" stroke="#8A5A2B" stroke-width="9" stroke-linecap="round"/><circle cx="250" cy="155" r="20" fill="#FF8FB1" {SW}/>'''
I["yoyo"] = f'''<path d="M200 30 Q240 60 220 120" stroke="{INK}" stroke-width="5" fill="none"/><circle cx="200" cy="25" r="14" fill="none" stroke="{INK}" stroke-width="5"/>
<circle cx="220" cy="230" r="130" fill="#FF4D6D" {SW}/><circle cx="220" cy="230" r="80" fill="#FF8FA3" {SW}/><circle cx="220" cy="230" r="22" fill="#FFD23F" {SW}/>
<path d="M220 120 L220 208" stroke="{INK}" stroke-width="5"/><ellipse cx="170" cy="170" rx="30" ry="16" fill="#FFF" opacity="0.5" transform="rotate(-40 170 170)"/>'''
I["zebra"] = f'''<path d="M120 300 L115 375 M170 305 L170 378 M250 305 L250 378 M300 300 L305 375" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>
<path d="M120 300 L115 375 M170 305 L170 378 M250 305 L250 378 M300 300 L305 375" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
<ellipse cx="210" cy="250" rx="130" ry="75" fill="#FFFFFF" {SW}/>
{"".join(f'<path d="M{x} 182 Q{x + 15} 250 {x} 318" stroke="{INK}" stroke-width="14" fill="none"/>' for x in (130, 175, 220, 265))}
<path d="M80 230 Q50 260 60 300" stroke="{INK}" stroke-width="8" fill="none"/>
<path d="M300 210 Q320 120 330 100" stroke="{INK}" stroke-width="56" fill="none" stroke-linecap="round"/><path d="M300 210 Q320 120 330 100" stroke="#FFFFFF" stroke-width="42" fill="none" stroke-linecap="round"/>
<path d="M295 170 l30 -6 M305 140 l28 -4" stroke="{INK}" stroke-width="10"/>
<ellipse cx="340" cy="95" rx="48" ry="58" fill="#FFFFFF" {SW}/><ellipse cx="350" cy="140" rx="34" ry="22" fill="#B0B0BC" {SW}/>
<path d="M300 60 Q320 20 345 45 Q350 20 370 45" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/>
{eyes(328, 362, 88, 10)}<path d="M320 70 l-14 -26 l20 10 Z M372 70 l12 -26 l-20 10 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'''

BG = {}
BG["abcpark"] = f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#86D6FF"/><stop offset="1" stop-color="#E2F6FF"/></linearGradient></defs>
  <rect width="1920" height="1080" fill="url(#sk)"/>
  <g fill="#FFFFFF" opacity="0.95">{"".join(f'<ellipse cx="{x}" cy="{y}" rx="100" ry="40"/><ellipse cx="{x + 60}" cy="{y - 24}" rx="62" ry="40"/>' for x, y in ((240, 150), (1650, 130)))}</g>
  <path d="M0 160 Q480 260 960 200 Q1440 140 1920 240" stroke="{INK}" stroke-width="5" fill="none"/>
  {"".join(f'<path d="M{80 + i * 120} {190 + (i * 7) % 40} l50 0 l-25 60 Z" fill="{c}" stroke="{INK}" stroke-width="4"/>' for i, c in enumerate((["#FF4D6D", "#FF9F1C", "#FFD23F", "#7ED957", "#4CC9F0", "#9B5DE5"] * 3)[:15]))}
  <path d="M0 640 Q480 560 960 620 Q1440 680 1920 600 L1920 1080 L0 1080 Z" fill="#8BDB6A" {SW}/>
  <path d="M0 760 Q600 720 1100 780 Q1500 830 1920 770 L1920 1080 L0 1080 Z" fill="#6CC24A"/>
  {"".join(f'<circle cx="{x}" cy="{y}" r="14" fill="{c}"/><circle cx="{x}" cy="{y}" r="6" fill="#FFD23F"/>' for x, y, c in ((160, 900, "#FF6B8B"), (420, 1000, "#FFFFFF"), (1500, 950, "#B79BEA"), (1780, 880, "#FF6B8B"), (900, 1030, "#FFFFFF"), (1250, 1000, "#FF9F1C")))}
  <rect x="1650" y="430" width="40" height="230" fill="#8A5A2B" {SW}/><circle cx="1670" cy="390" r="120" fill="#5DBB46" {SW}/>
  <rect x="200" y="460" width="34" height="200" fill="#8A5A2B" {SW}/><circle cx="217" cy="420" r="100" fill="#5DBB46" {SW}/>'''


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
    for k, svg in BG.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>',
               str(OUT / f"bg_{k}.png"), 1920, 1080)
    sheet = Image.new("RGBA", (180 * len(names) + 400, 230), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((170, 170)), (i * 180, 0))
    sheet.alpha_composite(Image.open(OUT / "bg_abcpark.png").convert("RGBA").resize((390, 220)), (180 * len(names) + 5, 0))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items + bg")


if __name__ == "__main__":
    render()
