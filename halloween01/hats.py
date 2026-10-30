"""Halloween costume hats on the 1200x2000 character canvas. python hats.py -> art/hat_gul.png, art/hat_misheal.png"""
import pathlib, sys
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A
SW = A.SW.replace('stroke-width="6"', 'stroke-width="14"')

STAR = lambda x, y, r, c: (f'<path d="M{x} {y - r} L{x + r * .3} {y - r * .3} L{x + r} {y} L{x + r * .3} {y + r * .3} L{x} {y + r} '
                           f'L{x - r * .3} {y + r * .3} L{x - r} {y} L{x - r * .3} {y - r * .3} Z" fill="{c}"/>')
HATS = {
    # Mishu: purple witch hat with a bent tip, orange band and gold stars
    "misheal": f'''<path d="M380 330 Q520 260 560 120 Q600 10 760 30 Q660 70 690 200 Q720 290 830 330 Z" fill="#7B4FC9" {SW}/>
      <path d="M420 300 Q600 340 800 300 L812 336 Q600 380 410 336 Z" fill="#FF9A2E" {SW}/>
      <ellipse cx="600" cy="352" rx="420" ry="62" fill="#6A3FB8" {SW}/>
      {STAR(560, 210, 34, "#FFD23F")}{STAR(650, 120, 24, "#FFD23F")}{STAR(700, 250, 20, "#FFE98A")}''',
    # Gul: pumpkin hat with a green stem and leaf
    "gul": f'''<path d="M300 330 Q300 130 600 110 Q900 130 900 330 Q600 380 300 330 Z" fill="#FF9A2E" {SW}/>
      <path d="M450 130 Q430 230 445 345 M750 130 Q770 230 755 345" stroke="#E07A12" stroke-width="14" fill="none"/>
      <path d="M575 120 Q565 50 600 20 Q630 12 638 34 Q610 60 625 118 Z" fill="#6B8E23" {SW}/>
      <path d="M630 50 Q720 0 770 50 Q720 80 640 70 Z" fill="#7CC444" {SW}/>''',
}

if __name__ == "__main__":
    for n, svg in HATS.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1200" height="2000">{svg}</svg></body></html>',
               str(HERE / "art" / f"hat_{n}.png"), 1200, 2000)
    # preview on the heads
    L = HERE.parent / "characters" / "layers"
    prev = Image.new("RGBA", (1200, 1100), (230, 220, 245, 255))
    for i, (n, o) in enumerate((("gul", "bluetee"), ("misheal", "pink"))):
        im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
        parts = (["hair_back"] if n == "misheal" else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_down_{o}", "neck", "head",
                 "eyes_open", "brows", "mouth_smile", "hair_front"] + (["earrings"] if n == "misheal" else [])
        for p in parts:
            im.alpha_composite(Image.open(L / n / f"{p}.png"))
        im.alpha_composite(Image.open(HERE / "art" / f"hat_{n}.png"))
        prev.alpha_composite(im.resize((600, 1000)), (i * 600, 50))
    prev.save(HERE / "_hats.png")
    print("hats ok")
