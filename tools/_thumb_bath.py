import importlib.util, math, sys, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.argv = ["x"]
sys.path.insert(0, str(ROOT / "tools"))
import thumb_fun as TF
spec = importlib.util.spec_from_file_location("l11r", ROOT / "long11-bath" / "render.py")
R11 = importlib.util.module_from_spec(spec); spec.loader.exec_module(R11)
fr = TF.sunburst((70, 190, 255), (150, 225, 255))
d = ImageDraw.Draw(fr, "RGBA")
# bubbles everywhere
import numpy as np
rng = np.random.default_rng(3)
for _ in range(26):
    x, y, r = rng.uniform(60, 1220), rng.uniform(150, 520), rng.uniform(18, 50)
    R11.bubble(d, x, y, r)
# bathtub with foam
d.rounded_rectangle((330, 470, 950, 700), radius=50, fill=(255, 255, 255), outline=TF.INK, width=8)
for i in range(22):
    x = 350 + i * 28
    r = 34 + 10 * math.sin(i * 1.7)
    d.ellipse((x - r, 470 - r * 0.8, x + r, 470 + r * 0.8), fill=(255, 255, 255), outline=(200, 225, 240), width=3)
for fx in (400, 880):
    d.ellipse((fx - 30, 680, fx + 30, 730), fill=(255, 200, 40), outline=TF.INK, width=6)
duck = TF.outlined(TF.load(R11.ART["duck"], 230), 7)
fr.alpha_composite(duck, (530, 300))
apple = TF.outlined(TF.load(ROOT / "ep01-fruits/art/fruit_apple.png", 120), 6)
fr.alpha_composite(apple, (790, 390))
gul = TF.character("gul", "tee", (R11.ART["sponge"], 240, -20, 0, -40), bubbles=True)
mishu = TF.character("misheal", "yellow", (R11.ART["duck"], 230, 0, 0, -50), bubbles=True)
TF.place_kids(fr, gul, mishu)
TF.R.G["fonts"] = {}
TF.R.rainbow_text(fr, 640, 600, "SINK OR FLOAT?", 78, maxw=560)
TF.finish(fr, "BATH TIME!", ROOT / "VIDEOS" / "L11 Bath Time" / "THUMBNAIL v1.jpg", size=150)
