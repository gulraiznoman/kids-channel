import importlib.util, math, sys, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.argv = ["x"]
sys.path.insert(0, str(ROOT / "tools"))
import thumb_fun as TF
spec = importlib.util.spec_from_file_location("l12r", ROOT / "long12-trucks" / "render.py")
R12 = importlib.util.module_from_spec(spec); spec.loader.exec_module(R12)
R12.G["item"] = {p.stem[5:]: Image.open(p).convert("RGBA") for p in (ROOT / "long12-trucks/art").glob("item_*.png")}
R12.G["truck"] = {p.stem[6:]: Image.open(p).convert("RGBA") for p in (ROOT / "long12-trucks/art").glob("truck_*.png")}
R12.G["tsz"], R12.G["sized"] = {}, {}
fr = TF.sunburst((255, 170, 40), (255, 220, 90))
lay = Image.new("RGBA", fr.size, (0, 0, 0, 0))
R12.truck(lay, "excavator", 720, 600, 0.62, 0, p=0.85)
R12.truck(lay, "dumptruck", 600, 700, 0.38, 0, p=0.0)
fr.alpha_composite(TF.outlined(lay, 7))
d = ImageDraw.Draw(fr)
for dx, dy, r in ((-60, -30, 14), (-20, -60, 10), (30, -40, 12), (-90, 10, 9), (60, -10, 8)):
    d.ellipse((470 + dx - r, 560 + dy - r, 470 + dx + r, 560 + dy + r), fill=(160, 112, 63), outline=TF.INK, width=3)
TF.stars_ring(fr, 640, 440, 330, 230)
cone = ROOT / "long12-trucks/art/item_cone.png"
gul = TF.character("gul", "polo", (ROOT / "long12-trucks/art/item_hardhat.png", 240, 0, 0, -60))
mishu = TF.character("misheal", "pink", (cone, 220, 0, 0, -50))
TF.place_kids(fr, gul, mishu)
TF.finish(fr, "BIG TRUCKS!", ROOT / "VIDEOS" / "L12 Trucks" / "THUMBNAIL v1.jpg", size=150)
