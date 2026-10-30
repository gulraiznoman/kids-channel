import math, sys, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.argv = ["x"]
sys.path.insert(0, str(ROOT / "tools"))
import thumb_fun as TF
fr = TF.sunburst((80, 200, 110), (255, 210, 60))
TF.R.G["fonts"] = {}
lay = Image.new("RGBA", fr.size, (0, 0, 0, 0))
TF.R.rainbow_text(lay, 640, 400, "20", 280, colour=(255, 120, 40))
fr.alpha_composite(TF.outlined(lay, 8))
d = ImageDraw.Draw(fr)
cell = 40
for f in range(2):
    x0 = 640 - 5 * cell - 15 + f * (5 * cell + 30) - (5 * cell + 30) / 2 + 5 * cell / 2 + 7
    for k in range(10):
        x, y = x0 + (k % 5) * cell, 560 + (k // 5) * cell
        d.rectangle((x, y, x + cell, y + cell), fill=(255, 255, 255), outline=TF.INK, width=3)
        c = (255, 77, 109) if f == 0 else (46, 168, 255)
        d.ellipse((x + 6, y + 6, x + cell - 6, y + cell - 6), fill=c, outline=TF.INK, width=2)
gul = TF.character("gul", "tee", (ROOT / "ep01-fruits/art/fruit_apple.png", 220, 0, 0, -40))
mishu = TF.character("misheal", "kurta", (ROOT / "long01-animals-fun/art/fruit_star.png", 230, 0, 0, -40))
TF.place_kids(fr, gul, mishu)
TF.float_bubbles(fr)
TF.finish(fr, "COUNT TO 20!", ROOT / "VIDEOS" / "L14 Count to 20" / "THUMBNAIL v1.jpg", size=135)
