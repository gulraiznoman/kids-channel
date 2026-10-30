"""Facebook Week 1 pack for Gul & Mishu: images + captions (posts.md) in kids-channel/FACEBOOK/Week 1/."""
import pathlib, re, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "FACEBOOK" / "Week 1"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "branding"))
sys.path.insert(0, str(ROOT / "characters"))
import banner as BN                 # kid(), glow(), and render text helpers (R)
import characters as CH
R = BN.R
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
INK = (58, 36, 32)


def sky(w, h):
    im = Image.new("RGBA", (w, h))
    px = im.load()
    for y in range(h):
        k = y / h
        c = (int(126 + (216 - 126) * k), int(200 + (241 - 200) * k), 255, 255)
        for x in range(w):
            px[x, y] = c
    return im


def rainbow_bg(w, h):
    im = sky(w, h)
    d = ImageDraw.Draw(im)
    cols = [(255, 77, 109), (255, 159, 28), (255, 210, 63), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
    for k, col in enumerate(cols):
        r = w * 0.62 - k * 34
        d.ellipse((w / 2 - r, h * 0.92 - r, w / 2 + r, h * 0.92 + r), outline=col, width=34)
    d.rectangle((0, int(h * 0.86), w, h), fill=(124, 203, 79))
    return im


def item(path, size):
    return Image.open(path).resize((size, size), Image.LANCZOS)


def card(text_lines, w, y0, size=46):
    """White rounded card with dark text lines."""
    lay = Image.new("RGBA", (w, 80 + len(text_lines) * int(size * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((0, 0, lay.width - 1, lay.height - 1), radius=40, fill=(255, 255, 255, 240), outline=INK, width=6)
    f = R.font(size)
    for i, t in enumerate(text_lines):
        d.text((40, 40 + i * int(size * 1.6)), t, font=f, fill=INK)
    return lay


# ---------------------------------------------------------------- 1. intro
def intro():
    im = rainbow_bg(1080, 1080)
    g = BN.glow(BN.kid("gul", "open", "open", "wave", 620)).transpose(Image.FLIP_LEFT_RIGHT)
    m = BN.glow(BN.kid("misheal", "closed", "open", "wave", 620))
    im.alpha_composite(g, (70, 1080 - g.height - 30))
    im.alpha_composite(m, (1080 - m.width - 70, 1080 - m.height - 30))
    R.rainbow_text(im, 540, 120, "MEET GUL & MISHU!", 80)
    R.plain_text(im, 540, 245, "New learning videos for toddlers", 50)
    im.convert("RGB").save(OUT / "Day 1 - Meet Gul and Mishu.jpg", quality=92)


# ---------------------------------------------------------------- 2/7. tip cards
def tip(name, title, lines, pics):
    im = sky(1080, 1080)
    t1, t2 = title
    R.rainbow_text(im, 540, 95, t1, 78)
    R.rainbow_text(im, 540, 190, t2, 78)
    c = card(lines, 960, 0, 40)
    im.alpha_composite(c, (60, 270))
    y = 270 + c.height + 20
    n = len(pics)
    sz = min(260, int(960 / n))
    for i, p in enumerate(pics):
        it = BN.glow(item(p, sz), 6)
        im.alpha_composite(it, (int(540 - n * sz / 2 + i * sz), min(y, 1080 - sz - 70)))
    R.plain_text(im, 540, 1035, "Watch Gul & Mishu on YouTube!", 40)
    im.convert("RGB").save(OUT / name, quality=92)


# ---------------------------------------------------------------- 4. poll
def poll():
    im = sky(1080, 1080)
    d = ImageDraw.Draw(im)
    R.rainbow_text(im, 540, 110, "WHAT SHOULD WE", 80)
    R.rainbow_text(im, 540, 210, "LEARN NEXT?", 96)
    for i, (p, label, emo) in enumerate(((ROOT / "long01-animals-fun/art/fruit_n3.png", "NUMBERS", "👍"),
                                          (ROOT / "long01-animals-fun/art/fruit_circle.png", "SHAPES", "❤️"))):
        x0 = 60 + i * 500
        d.rounded_rectangle((x0, 320, x0 + 460, 900), radius=50, fill=(255, 255, 255), outline=INK, width=8)
        im.alpha_composite(item(p, 360), (x0 + 50, 360))
        R.rainbow_text(im, x0 + 230, 790, label, 70)
    R.plain_text(im, 540, 975, "Comment 1 for Numbers or 2 for Shapes!", 42)
    im.convert("RGB").save(OUT / "Day 4 - Poll.jpg", quality=92)


# ---------------------------------------------------------------- 5. colouring page (line art)
KEEP_DARK = ("#140B07", "#2B1B17", "#3A2420")


def line_art(svg):
    def f(m):
        col = m.group(1).upper()
        return m.group(0) if col in KEEP_DARK else 'fill="#FFFFFF"'
    svg = re.sub(r'fill="(#[0-9A-Fa-f]{6})"', f, svg)
    def st(m):
        # thick coloured strokes are filled shapes (arms, stems drawn wide): make them white;
        # thin coloured strokes are lines: make them dark
        return f'stroke="#FFFFFF" stroke-width="{m.group(2)}"' if float(m.group(2)) >= 20 else f'stroke="#3A2420" stroke-width="{m.group(2)}"'
    svg = re.sub(r'stroke="#(?!3A2420)([0-9A-Fa-f]{6})" stroke-width="([0-9.]+)"', st, svg)
    return svg.replace('opacity="0.45"', 'opacity="0"').replace('opacity="0.5"', 'opacity="0"')


def colouring():
    sys.path.insert(0, str(ROOT / "ep01-fruits"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("fruitart", ROOT / "ep01-fruits" / "art.py")
    FA = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(FA)
    gul = CH.svg(CH.layers("gul", eyes="open", mouth="smile", arm="wave"))
    mishu = CH.svg(CH.layers("misheal", eyes="open", mouth="smile"))
    fruits = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:330px;height:330px">'
                     f'<svg xmlns="http://www.w3.org/2000/svg" width="330" height="330" viewBox="0 0 400 400">{line_art(FA.FRUIT_SVG[k])}</svg></div>'
                     for k, x, y in (("apple", 120, 1330), ("banana", 455, 1360), ("strawberry", 790, 1330)))
    html = (f'<html><body style="margin:0;background:#FFFFFF;position:relative;width:1240px;height:1754px">'
            f'<div style="position:absolute;left:80px;top:250px;width:540px;height:900px">{line_art(gul).replace("<svg ", "<svg style=\'width:540px;height:900px\' ")}</div>'
            f'<div style="position:absolute;left:620px;top:250px;width:540px;height:900px">{line_art(mishu).replace("<svg ", "<svg style=\'width:540px;height:900px\' ")}</div>'
            f'{fruits}</body></html>')
    tmp = OUT / "_c.html"
    tmp.write_text(html, encoding="utf-8")
    png = OUT / "_c.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=FFFFFFFF",
                    "--window-size=1240,1754", f"--screenshot={png}", tmp.as_uri()], check=True, capture_output=True)
    tmp.unlink()
    im = Image.open(png).convert("RGBA")
    png.unlink()
    d = ImageDraw.Draw(im)
    f = R.font(86)
    t = "Colour Gul & Mishu!"
    w = d.textlength(t, font=f)
    d.text((620 - w / 2, 70), t, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=INK)
    f2 = R.font(34)
    t2 = "Free colouring page · youtube.com/@GulAndMishu"
    w2 = d.textlength(t2, font=f2)
    d.text((620 - w2 / 2, 1690), t2, font=f2, fill=INK)
    im.convert("RGB").save(OUT / "Day 5 - Colouring Page (print A4).jpg", quality=95)


if __name__ == "__main__":
    F = ROOT / "ep01-fruits" / "art"
    C = ROOT / "ep02-colours" / "art"
    intro()
    tip("Day 2 - Tip Teach Colours.jpg", ("TEACH COLOURS", "AT HOME!"),
        ["1. Name colours at snack time:", "    \"A red apple! A yellow banana!\"",
         "2. Play \"find something blue!\" at home.", "3. Sort toys into colour piles together.",
         "4. Watch Learn Colours with Gul & Mishu!"],
        [C / "fruit_red.png", C / "fruit_yellow.png", C / "fruit_blue.png", C / "fruit_green.png"])
    poll()
    colouring()
    tip("Day 7 - Tip Snack Time Words.jpg", ("SNACK TIME", "= WORD TIME!"),
        ["1. Say each fruit's name as you cut it.", "2. Ask \"What colour is it?\"",
         "3. Count the pieces together: 1, 2, 3!", "4. Let your toddler say it back. Clap!"],
        [F / "fruit_apple.png", F / "fruit_banana.png", F / "fruit_orange.png", F / "fruit_grapes.png"])
    print("ok")
