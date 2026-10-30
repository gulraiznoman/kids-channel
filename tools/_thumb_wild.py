import sys, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.argv = ["x"]
sys.path.insert(0, str(ROOT / "tools"))
import thumb_fun as TF
A13 = ROOT / "long13-wild/art"
fr = TF.sunburst((255, 170, 50), (120, 200, 90))
TF.stars_ring(fr, 640, 430, 330, 240)
for p, size, x, y in ((A13 / "item_giraffe.png", 330, 760, 300), (ROOT / "long01-animals-fun/art/fruit_elephant.png", 270, 470, 470), (A13 / "item_lion.png", 330, 690, 520)):
    im = TF.outlined(TF.load(p, size), 7)
    fr.alpha_composite(im, (x - im.width // 2, y - im.height // 2))
gul = TF.character("gul", "bluetee", (A13 / "item_tiger.png", 260, 0, 0, -50))
mishu = TF.character("misheal", "yellow", (A13 / "item_panda.png", 250, 0, 0, -50))
TF.place_kids(fr, gul, mishu)
TF.finish(fr, "WILD ANIMALS!", ROOT / "VIDEOS" / "L13 Wild Animals" / "THUMBNAIL v1.jpg", size=130)
