"""Three DIFFERENT thumbnail layouts for L24 Space, L25 First Words, L26 Months.  python tools/thumbs_24_26.py
Space: rocket on a diagonal trail through planets.  Words: picture-tile wall with a speech bubble.  Months: 12-slice colour wheel."""
import math, sys, pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import thumbs_18_20 as T
TF, R, INK, W, H = T.TF, T.R, T.INK, T.W, T.H
paste, kid, text_outline, save = T.paste, T.kid, T.text_outline, T.save


def space():
    A = ROOT / "long24-space/art"
    fr = Image.open(A / "bg_space.png").convert("RGBA").resize((W, H))
    d = ImageDraw.Draw(fr)
    for j in range(9):
        k = j / 8
        x, y, r = 120 + 500 * k, 660 - 400 * k, 34 + 60 * (1 - k)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 150 + j * 11, 40 + j * 10))
    paste(fr, A / "item_saturn.png", 480, 1000, 200, ol=9)
    paste(fr, A / "item_jupiter.png", 300, 1100, 540, ol=8)
    paste(fr, A / "item_earth.png", 190, 170, 170, ol=7)
    paste(fr, A / "item_mars.png", 130, 800, 620, ol=6)
    paste(fr, ROOT / "long21-presents/art/item_rocket.png", 430, 640, 310, rot=-48, ol=9)
    paste(fr, A / "item_astronaut.png", 240, 150, 560, rot=8, ol=7)
    text_outline(fr, 470, 75, "8 PLANETS!", 118, colour=(255, 230, 60), maxw=640)
    save(fr, ROOT / "VIDEOS/L24 Space and Planets/THUMBNAIL v1.jpg")


def words():
    L1, L4 = ROOT / "long01-animals-fun/art", ROOT / "long04-good-habits/art"
    fr = Image.new("RGBA", (W, H), (255, 245, 200, 255))
    d = ImageDraw.Draw(fr)
    tiles = [("dog", L1 / "fruit_puppy.png", (255, 200, 120)), ("ball", L4 / "item_ball.png", (255, 170, 190)), ("apple", ROOT / "ep01-fruits/art/fruit_apple.png", (170, 230, 170)),
             ("milk", ROOT / "long25-words/art/item_bottle.png", (170, 215, 255)), ("car", ROOT / "long16-sharing/art/item_car.png", (255, 225, 120)), ("duck", ROOT / "long11-bath/art/item_duck.png", (200, 180, 245))]
    for i, (n, p, c) in enumerate(tiles):
        x, y = 24 + (i % 3) * 262, 150 + (i // 3) * 278
        d.rounded_rectangle((x, y, x + 246, y + 258), radius=30, fill=c, outline=INK, width=7)
        paste(fr, p, 180, x + 123, y + 105, ol=5)
        d = ImageDraw.Draw(fr)
        text_outline(fr, x + 123, y + 222, n.upper(), 44, colour=(255, 255, 255), maxw=225)
        d = ImageDraw.Draw(fr)
    kid(fr, "misheal", "excited", "pink", 1040, 590, bottom=H + 60)
    d = ImageDraw.Draw(fr)
    text_outline(fr, 460, 74, "FIRST WORDS!", 108, colour=(255, 77, 109), maxw=860)
    save(fr, ROOT / "VIDEOS/L25 First Words/THUMBNAIL v1.jpg")


def months():
    MCOL = [(46, 120, 230), (240, 90, 160), (59, 170, 74), (0, 170, 190), (140, 190, 40), (245, 170, 20), (255, 120, 30), (232, 53, 46), (140, 80, 210), (205, 95, 30), (120, 90, 60), (30, 130, 90)]
    fr = Image.new("RGBA", (W, H), (20, 26, 82, 255))
    d = ImageDraw.Draw(fr)
    cx, cy, r = 640, 330, 285
    for i in range(12):
        d.pieslice((cx - r, cy - r, cx + r, cy + r), i * 30 - 90, (i + 1) * 30 - 90, fill=MCOL[i], outline=(255, 255, 255), width=6)
    for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()):
        a = math.radians(i * 30 - 75)
        text_outline(fr, cx + 215 * math.cos(a), cy + 215 * math.sin(a), m, 44, colour=(255, 255, 255), maxw=110)
    d = ImageDraw.Draw(fr)
    d.ellipse((cx - 118, cy - 118, cx + 118, cy + 118), fill=(255, 255, 255), outline=INK, width=8)
    text_outline(fr, cx, cy, "12", 130, colour=(255, 77, 109), maxw=200)
    for x, y, s, n in ((160, 150, 280, 0), (1120, 170, 300, 1), (1160, 520, 210, 2)):
        paste(fr, ROOT / "long26-months/art/item_firework.png", s, x, y, rot=n * 20, ol=0 + 1)
    kid(fr, "gul", "excited", "bluetee", 150, 400, bottom=H + 30)
    text_outline(fr, 640, 655, "MONTHS OF THE YEAR", 80, colour=(255, 230, 60), maxw=860)
    save(fr, ROOT / "VIDEOS/L26 Months and New Year/THUMBNAIL v1.jpg")


if __name__ == "__main__":
    space(); words(); months()
    ims = [Image.open(ROOT / f"VIDEOS/{d}/THUMBNAIL v1.jpg").resize((640, 360)) for d in ("L24 Space and Planets", "L25 First Words", "L26 Months and New Year")]
    sh = Image.new("RGB", (1920, 360))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 640, 0))
    sh.save(ROOT / "tools/_thumbs_24_26.png")
