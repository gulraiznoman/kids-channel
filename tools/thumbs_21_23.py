"""Three DIFFERENT thumbnail layouts for L21 Presents, L22 Write ABC, L23 Bugs.  python tools/thumbs_21_23.py
Presents: toys exploding out of an open box on a purple burst.  Writing: full notebook page, giant pencil mid-letter.
Bugs: giant magnifying glass over the garden, a huge ladybug inside the lens."""
import math, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "long22-writing"))
import thumbs_18_20 as T
from strokes import UP, partial
TF, R, INK, W, H = T.TF, T.R, T.INK, T.W, T.H
paste, kid, text_outline, save = T.paste, T.kid, T.text_outline, T.save


# ---------------------------------------------------------------- L21 PRESENTS: toys explode from a box
def presents():
    A, L1, A17 = ROOT / "long21-presents/art", ROOT / "long01-animals-fun/art", ROOT / "long17-xmastree/art"
    fr = Image.new("RGBA", (W, H), (120, 60, 200, 255))
    d = ImageDraw.Draw(fr)
    for i in range(18):
        a = i / 18 * 2 * math.pi
        d.polygon([(640, 560), (640 + 1200 * math.cos(a), 560 + 1200 * math.sin(a)), (640 + 1200 * math.cos(a + 0.175), 560 + 1200 * math.sin(a + 0.175))], fill=(160, 95, 235))
    xx, yy = np.meshgrid(np.arange(W), np.arange(H))
    g = np.clip(1 - np.hypot(xx - 640, (yy - 500) * 1.1) / 420, 0, 1) ** 1.5
    glow = Image.new("RGBA", (W, H), (255, 240, 150, 0))
    glow.putalpha(Image.fromarray((g * 235).astype(np.uint8)))
    fr.alpha_composite(glow)
    for key, p, s, x, y, r in (("firetruck", L1 / "fruit_firetruck.png", 230, 250, 300, 12), ("rocket", A / "item_rocket.png", 240, 630, 250, -6),
                               ("teddy", ROOT / "long04-good-habits/art/item_teddy.png", 220, 1010, 300, -10), ("frog", ROOT / "long08-colors-shapes/art/item_frog.png", 170, 160, 520, 10),
                               ("robot", A / "item_robot.png", 210, 1130, 520, -8), ("duck", ROOT / "long11-bath/art/item_duck.png", 140, 420, 420, 15), ("basketball", A / "item_basketball.png", 130, 860, 410, 0)):
        paste(fr, p, s, x, y, rot=r, ol=7)
    d = ImageDraw.Draw(fr)
    # open box in front, lid knocked off
    d.polygon([(400, 480), (880, 480), (940, 760), (340, 760)], fill=(232, 53, 46), outline=INK)
    d.polygon([(400, 480), (880, 480), (840, 540), (440, 540)], fill=(150, 25, 25), outline=INK)
    d.polygon([(600, 540), (680, 540), (695, 760), (585, 760)], fill=(255, 215, 60), outline=INK)
    text_outline(fr, 640, 80, "SURPRISE TOYS!", 120, colour=(255, 230, 60), maxw=1180)
    save(fr, ROOT / "VIDEOS/L21 Christmas Presents/THUMBNAIL v1.jpg")


# ---------------------------------------------------------------- L22 WRITING: full notebook page, giant pencil
def writing():
    fr = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(fr)
    for y in range(90, H, 90):
        d.line((0, y, W, y), fill=(150, 210, 255), width=5)
    d.line((110, 0, 110, H), fill=(255, 120, 140), width=6)
    for y in (70, 360, 650):
        d.ellipse((30, y - 26, 82, y + 26), fill=(225, 230, 240), outline=INK, width=4)

    def letter(L, cx, cy, h, col, f=1.0):
        w = h * 0.82
        x0, y0 = cx - w / 2, cy - h / 2
        dd = ImageDraw.Draw(fr)
        for poly in UP[L]:
            pts = [(x0 + p[0] * w, y0 + p[1] * h) for p in poly]
            prev = None
            run, dist = 0, 0
            for a, b in zip(pts, pts[1:]):
                L2 = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
                while run <= L2:
                    px, py = a[0] + (b[0] - a[0]) * run / L2, a[1] + (b[1] - a[1]) * run / L2
                    dd.ellipse((px - 7, py - 7, px + 7, py + 7), fill=(195, 200, 212))
                    run += 26
                run -= L2
        part, tip = partial(UP[L], f)
        for poly in part:
            pts = [(x0 + p[0] * w, y0 + p[1] * h) for p in poly]
            if len(pts) > 1:
                dd.line(pts, fill=INK, width=44, joint="curve")
                dd.line(pts, fill=col, width=32, joint="curve")
            for x, y in (pts[0], pts[-1]):
                dd.ellipse((x - 16, y - 16, x + 16, y + 16), fill=col)
        return x0 + tip[0] * w, y0 + tip[1] * h

    letter("A", 300, 340, 360, (255, 77, 109))
    letter("B", 640, 340, 360, (46, 130, 235))
    tip = letter("C", 960, 340, 360, (59, 170, 74), f=0.72)
    paste(fr, ROOT / "long22-writing/art/item_pencil.png", 460, tip[0] + 140, tip[1] - 150, ol=9)
    kid(fr, "misheal", "excited", "pink", 170, 330, bottom=H + 30, wave=True)
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((340, 560, 1250, 705), radius=36, fill=(255, 210, 40), outline=INK, width=8)
    text_outline(fr, 795, 632, "LEARN TO WRITE!", 92, colour=(255, 77, 109), maxw=860)
    save(fr, ROOT / "VIDEOS/L22 Learn to Write ABC/THUMBNAIL v1.jpg")


# ---------------------------------------------------------------- L23 BUGS: giant magnifying glass
def bugs():
    A = ROOT / "long23-bugs/art"
    yy = np.linspace(0, 1, H)[:, None, None]
    bg = (np.array([150, 225, 120]) * (1 - yy) + np.array([60, 160, 70]) * yy)
    fr = Image.fromarray(np.repeat(bg.astype(np.uint8), W, axis=1)).convert("RGBA")
    d = ImageDraw.Draw(fr)
    rng = np.random.default_rng(23)
    for _ in range(200):
        x, y, h = rng.uniform(0, W), rng.uniform(120, H + 40), rng.uniform(30, 70)
        d.polygon([(x - 9, y), (x + 9, y), (x + rng.uniform(-14, 14), y - h)], fill=(50, 140, 60))
    paste(fr, A / "item_bee.png", 200, 170, 230, rot=6, ol=7)
    paste(fr, ROOT / "long09-eggs/art/item_butterfly.png", 200, 1150, 200, rot=-8, ol=7)
    paste(fr, A / "item_ant.png", 180, 1120, 620, ol=6)
    paste(fr, A / "item_grasshopper.png", 210, 150, 610, ol=6)
    cx, cy, r = 640, 370, 300
    lens = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lens)
    ld.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(235, 250, 255, 255))
    fr.alpha_composite(lens)
    bug = TF.load(A / "item_ladybug.png", 500)
    fr.alpha_composite(bug, (cx - bug.width // 2, cy - bug.height // 2))
    d = ImageDraw.Draw(fr)
    d.line((cx + 205, cy + 225, cx + 365, cy + 400), fill=INK, width=74)
    d.line((cx + 205, cy + 225, cx + 365, cy + 400), fill=(200, 150, 74), width=54)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=44)
    d.ellipse((cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), outline=(255, 215, 60), width=26)
    text_outline(fr, 640, 640, "BUG HUNT!", 130, colour=(255, 235, 60), maxw=720)
    save(fr, ROOT / "VIDEOS/L23 Bugs and Insects/THUMBNAIL v1.jpg")


if __name__ == "__main__":
    presents(); writing(); bugs()
    ims = [Image.open(ROOT / f"VIDEOS/{d}/THUMBNAIL v1.jpg").resize((640, 360)) for d in ("L21 Christmas Presents", "L22 Learn to Write ABC", "L23 Bugs and Insects")]
    sh = Image.new("RGB", (1920, 360))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 640, 0))
    sh.save(ROOT / "tools/_thumbs_21_23.png")
