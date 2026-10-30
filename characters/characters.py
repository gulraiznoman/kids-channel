"""Character kit for the kids channel: Gul (Gulraiz as a kid) and Misheal (as a kid).

Every character is drawn on the same 600x1000 canvas (feet at y~930, centre x=300),
split into named layers so videos can animate blinks, talking, waving and sunglasses.

python characters.py            -> renders previews + PNG layers into this folder
"""
import os, subprocess, sys, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 600, 1000

OUTLINE = "#3A2420"
SW = 'stroke="#3A2420" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'

CHARS = {
    "gul": dict(
        skin="#DCA27A", skin_dk="#C0865E", hair="#1F1A1C", hair_hi="#4A4146",
        iris="#4A2C1A", cheek="#E7826F",
    ),
    "misheal": dict(
        skin="#EDC2A0", skin_dk="#D7A381", hair="#6B3826", hair_hi="#9A5634",
        iris="#5A3420", cheek="#F2877F",
    ),
}


# ----------------------------------------------------------------- shared face parts
def ears(c):
    return f'''
    <circle cx="132" cy="335" r="34" fill="{c['skin']}" {SW}/>
    <circle cx="468" cy="335" r="34" fill="{c['skin']}" {SW}/>
    <path d="M128 322 q14 12 0 28" fill="none" stroke="{c['skin_dk']}" stroke-width="6" stroke-linecap="round"/>
    <path d="M472 322 q-14 12 0 28" fill="none" stroke="{c['skin_dk']}" stroke-width="6" stroke-linecap="round"/>'''


def face(c):
    return f'<ellipse cx="300" cy="320" rx="172" ry="165" fill="{c["skin"]}" {SW}/>'


def neck(c):
    return f'<path d="M268 462 L268 505 Q300 520 332 505 L332 462 Z" fill="{c["skin_dk"]}"/>'


def cheeks(c):
    return f'''
    <ellipse cx="200" cy="392" rx="30" ry="18" fill="{c['cheek']}" opacity="0.45"/>
    <ellipse cx="400" cy="392" rx="30" ry="18" fill="{c['cheek']}" opacity="0.45"/>'''


def nose(c):
    return f'<path d="M292 362 Q300 374 308 362" fill="none" stroke="{c["skin_dk"]}" stroke-width="6" stroke-linecap="round"/>'


def eye(x, y, c, lashes=False, side=1):
    s = f'''
    <ellipse cx="{x}" cy="{y}" rx="36" ry="42" fill="#FFFFFF" {SW}/>
    <circle cx="{x + 3}" cy="{y + 7}" r="27" fill="{c['iris']}"/>
    <circle cx="{x + 3}" cy="{y + 9}" r="15" fill="#140B07"/>
    <circle cx="{x - 7}" cy="{y - 4}" r="10" fill="#FFFFFF"/>
    <circle cx="{x + 14}" cy="{y + 18}" r="4.5" fill="#FFFFFF"/>'''
    if lashes:
        ox = x + side * 30
        s += f'''
    <path d="M{ox} {y - 30} l{side * 16} -12 M{ox + side * 6} {y - 18} l{side * 18} -6" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'''
    return s


def eyes_open(c, lashes=False):
    return eye(232, 318, c, lashes, -1) + eye(368, 318, c, lashes, 1)


def eyes_closed(c, lashes=False):
    # happy closed eyes (upside-down U)
    s = f'''
    <path d="M200 326 Q232 290 264 326" fill="none" stroke="{OUTLINE}" stroke-width="7" stroke-linecap="round"/>
    <path d="M336 326 Q368 290 400 326" fill="none" stroke="{OUTLINE}" stroke-width="7" stroke-linecap="round"/>'''
    if lashes:
        s += f'''<path d="M202 318 l-14 -8 M398 318 l14 -8" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'''
    return s


def eyes_blink(c, lashes=False):
    s = f'''
    <path d="M198 322 Q232 340 266 322" fill="none" stroke="{OUTLINE}" stroke-width="7" stroke-linecap="round"/>
    <path d="M334 322 Q368 340 402 322" fill="none" stroke="{OUTLINE}" stroke-width="7" stroke-linecap="round"/>'''
    if lashes:
        s += f'''<path d="M200 324 l-14 6 M400 324 l14 6" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'''
    return s


def brows(c, kind="gul"):
    col = c["hair"]
    w = 11 if kind == "gul" else 8
    return f'''
    <path d="M196 262 Q228 244 262 256" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>
    <path d="M338 256 Q372 244 404 262" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'''


MOUTHS = {
    "smile": '''
    <path d="M258 398 Q300 446 342 398 Q300 418 258 398 Z" fill="#7C2B2E" stroke="#3A2420" stroke-width="5" stroke-linejoin="round"/>
    <path d="M280 422 Q300 436 320 422 Q300 414 280 422 Z" fill="#F07C86"/>''',
    "open": '''
    <path d="M268 396 Q300 392 332 396 Q336 448 300 452 Q264 448 268 396 Z" fill="#7C2B2E" stroke="#3A2420" stroke-width="5" stroke-linejoin="round"/>
    <path d="M280 438 Q300 426 320 438 Q300 452 280 438 Z" fill="#F07C86"/>
    <path d="M276 398 L324 398 L320 408 L280 408 Z" fill="#FFFFFF"/>''',
    "o": '''
    <ellipse cx="300" cy="414" rx="17" ry="21" fill="#7C2B2E" stroke="#3A2420" stroke-width="5"/>
    <ellipse cx="300" cy="424" rx="9" ry="7" fill="#F07C86"/>''',
    "closed": '''
    <path d="M272 408 Q300 426 328 408" fill="none" stroke="#3A2420" stroke-width="6" stroke-linecap="round"/>''',
}


# ----------------------------------------------------------------- Gil
def gul_hair_front(c):
    return f'''
    <path d="M134 312 C124 236 150 178 196 150 C214 104 270 72 330 70 C392 68 438 92 452 132
             C474 170 478 240 466 312 C456 272 440 244 418 226 C372 212 326 208 290 210
             C248 212 212 216 182 230 C160 250 144 280 134 312 Z" fill="{c['hair']}" {SW}/>
    <path d="M222 150 C262 102 330 88 400 104" fill="none" stroke="{c['hair_hi']}" stroke-width="9" stroke-linecap="round"/>
    <path d="M250 190 C300 160 362 156 424 176" fill="none" stroke="{c['hair_hi']}" stroke-width="7" stroke-linecap="round"/>
    <path d="M196 150 C214 168 230 190 236 214" fill="none" stroke="{c['hair_hi']}" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'''


def gul_body(c, outfit="polo"):
    cream, taupe, brown = "#F3EADB", "#B9A58F", "#5B3B2F"
    TEE = {"tee": ("#E84A3C", "#FFD23F", "#3A6FD8"), "bluetee": ("#3D8BFD", "#FFD23F", "#FFB627")}
    tee, star, shorts = TEE.get(outfit, (None, None, "#4A3328"))
    if outfit == "polo":
        shirt = f'''
    <clipPath id="gulshirt"><path d="M196 500 Q300 476 404 500 L422 712 Q300 728 178 712 Z"/></clipPath>
    <g clip-path="url(#gulshirt)">
      <rect x="150" y="470" width="300" height="270" fill="{cream}"/>
      <rect x="150" y="470" width="62" height="270" fill="{taupe}"/>
      <rect x="338" y="470" width="44" height="270" fill="{taupe}"/>
      <rect x="382" y="470" width="80" height="270" fill="{brown}"/>
    </g>
    <path d="M196 500 Q300 476 404 500 L422 712 Q300 728 178 712 Z" fill="none" {SW}/>
    <path d="M300 506 L250 490 L262 540 Z" fill="{cream}" {SW}/>
    <path d="M300 506 L350 490 L338 540 Z" fill="{cream}" {SW}/>
    <path d="M300 506 L300 590" stroke="#8F8F8F" stroke-width="5"/>
    <rect x="293" y="582" width="14" height="22" rx="4" fill="#B5B5B5" stroke="#6E6E6E" stroke-width="3"/>'''
    else:   # bright tee with a star
        shirt = f'''
    <path d="M196 500 Q300 476 404 500 L422 712 Q300 728 178 712 Z" fill="{tee}" {SW}/>
    <path d="M262 492 Q300 520 338 492" fill="none" {SW}/>
    <path d="M300 566 L313 594 L343 597 L320 617 L327 647 L300 631 L273 647 L280 617 L257 597 L287 594 Z" fill="{star}" {SW}/>'''
    return f'''
    <!-- legs -->
    <rect x="222" y="760" width="50" height="130" rx="20" fill="{c['skin']}" {SW}/>
    <rect x="328" y="760" width="50" height="130" rx="20" fill="{c['skin']}" {SW}/>
    <!-- sneakers -->
    <path d="M196 900 Q196 872 240 872 Q284 872 286 900 Q286 922 240 924 L206 924 Q194 922 196 900 Z" fill="#FFFFFF" {SW}/>
    <path d="M196 912 L286 912" stroke="#C9CED6" stroke-width="10"/>
    <path d="M404 900 Q404 872 360 872 Q316 872 314 900 Q314 922 360 924 L394 924 Q406 922 404 900 Z" fill="#FFFFFF" {SW}/>
    <path d="M314 912 L404 912" stroke="#C9CED6" stroke-width="10"/>
    <!-- shorts -->
    <path d="M190 690 L410 690 L418 790 L312 792 L300 745 L288 792 L182 790 Z" fill="{shorts}" {SW}/>
    {shirt}'''


def gul_arm_l(c, sleeve="#B9A58F"):        # viewer's left, hanging down
    return f'''
    <path d="M206 520 Q168 590 168 662" fill="none" stroke="{OUTLINE}" stroke-width="56" stroke-linecap="round"/>
    <path d="M206 520 Q168 590 168 662" fill="none" stroke="{c['skin']}" stroke-width="46" stroke-linecap="round"/>
    <path d="M200 502 Q160 520 156 588 L214 600 Q222 548 214 504 Z" fill="{sleeve}" {SW}/>'''


def gul_arm_r(c, pose="down", sleeve="#5B3B2F"):
    if pose == "wave":
        return f'''
    <path d="M396 526 Q492 520 516 410" fill="none" stroke="{OUTLINE}" stroke-width="56" stroke-linecap="round"/>
    <path d="M396 526 Q492 520 516 410" fill="none" stroke="{c['skin']}" stroke-width="46" stroke-linecap="round"/>
    <circle cx="518" cy="396" r="30" fill="{c['skin']}" {SW}/>
    <path d="M388 504 Q440 486 458 540 L410 572 Q400 540 386 528 Z" fill="{sleeve}" {SW}/>'''
    return f'''
    <path d="M394 520 Q432 590 432 662" fill="none" stroke="{OUTLINE}" stroke-width="56" stroke-linecap="round"/>
    <path d="M394 520 Q432 590 432 662" fill="none" stroke="{c['skin']}" stroke-width="46" stroke-linecap="round"/>
    <path d="M400 502 Q440 520 444 588 L386 600 Q378 548 386 504 Z" fill="{sleeve}" {SW}/>'''


def gul_glasses(c):
    return f'''
    <path d="M150 300 L190 296 M410 296 L450 300" stroke="#C0C4CA" stroke-width="6" stroke-linecap="round"/>
    <rect x="182" y="284" width="100" height="74" rx="14" fill="#2C3140" opacity="0.94" stroke="#C0C4CA" stroke-width="6"/>
    <rect x="318" y="284" width="100" height="74" rx="14" fill="#2C3140" opacity="0.94" stroke="#C0C4CA" stroke-width="6"/>
    <path d="M282 300 Q300 290 318 300" fill="none" stroke="#C0C4CA" stroke-width="6"/>
    <path d="M196 298 L230 298" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.55"/>
    <path d="M332 298 L366 298" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.55"/>'''


# ----------------------------------------------------------------- Mishu
def misheal_hair_back(c):
    return f'''
    <path d="M122 330 C100 170 196 96 300 96 C408 96 504 170 478 330
             C482 410 496 468 522 506 C476 522 438 500 428 478 L172 478
             C162 500 124 522 78 506 C104 468 118 410 122 330 Z" fill="{c['hair']}" {SW}/>'''


def misheal_hair_front(c):
    return f'''
    <path d="M346 112 C266 112 168 168 146 312 C176 238 236 204 302 200 C336 190 352 150 346 112 Z" fill="{c['hair']}" {SW}/>
    <path d="M346 112 C420 120 470 186 468 312 C446 248 404 214 362 204 C368 170 362 136 346 112 Z" fill="{c['hair']}" {SW}/>
    <path d="M318 132 C252 146 196 196 178 262" fill="none" stroke="{c['hair_hi']}" stroke-width="9" stroke-linecap="round"/>
    <path d="M372 136 C420 160 446 210 452 262" fill="none" stroke="{c['hair_hi']}" stroke-width="8" stroke-linecap="round"/>
    <path d="M110 420 C112 452 104 476 92 494" fill="none" stroke="{c['hair_hi']}" stroke-width="8" stroke-linecap="round"/>
    <path d="M490 420 C488 452 496 476 508 494" fill="none" stroke="{c['hair_hi']}" stroke-width="8" stroke-linecap="round"/>'''


def misheal_earrings(c):
    return '''
    <circle cx="136" cy="388" r="15" fill="none" stroke="#E2B23C" stroke-width="7"/>
    <circle cx="464" cy="388" r="15" fill="none" stroke="#E2B23C" stroke-width="7"/>'''


def misheal_body(c, outfit="kurta"):
    PAL = {"kurta": ("#74302B", "#5A2421", "#E2B23C", "#74302B"), "yellow": ("#FFC93C", "#E0A21E", "#FFFFFF", "#F06A9A"),
           "pink": ("#FF7EB6", "#E8559A", "#FFFFFF", "#8A5CF6")}
    dress, dress_dk, gold, shoes = PAL[outfit]
    dots = []
    # gold embroidery dots along the V-neck and the hem
    for i, (x, y) in enumerate([(276, 516), (270, 536), (266, 556), (324, 516), (330, 536), (334, 556),
                                (300, 578)]):
        dots.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{gold}"/>')
    for x in range(186, 420, 26):
        dots.append(f'<circle cx="{x}" cy="{786 + (6 if (x // 26) % 2 else 0)}" r="5.5" fill="{gold}"/>')
    return f'''
    <!-- legs (tights) + shoes -->
    <rect x="232" y="790" width="46" height="100" rx="18" fill="#F0E2CF" {SW}/>
    <rect x="322" y="790" width="46" height="100" rx="18" fill="#F0E2CF" {SW}/>
    <path d="M208 902 Q208 876 250 876 Q288 876 288 902 Q288 920 250 922 L218 922 Q206 920 208 902 Z" fill="{shoes}" {SW}/>
    <path d="M392 902 Q392 876 350 876 Q312 876 312 902 Q312 920 350 922 L382 922 Q394 920 392 902 Z" fill="{shoes}" {SW}/>
    <!-- dress (maroon tunic with gold dots, like the real outfit) -->
    <path d="M206 500 Q300 480 394 500 L444 806 Q300 828 156 806 Z" fill="{dress}" {SW}/>
    <path d="M206 500 Q300 480 394 500 L398 530 Q300 512 202 530 Z" fill="{dress_dk}" opacity="0.35"/>
    <path d="M270 498 L300 566 L330 498 Z" fill="{c['skin_dk']}" {SW}/>
    {''.join(dots)}'''


def misheal_arm_l(c, sleeve="#74302B"):
    return f'''
    <path d="M214 520 Q176 590 176 662" fill="none" stroke="{OUTLINE}" stroke-width="52" stroke-linecap="round"/>
    <path d="M214 520 Q176 590 176 662" fill="none" stroke="{c['skin']}" stroke-width="42" stroke-linecap="round"/>
    <path d="M208 502 Q164 524 160 618 L214 626 Q224 560 218 504 Z" fill="{sleeve}" {SW}/>
    <circle cx="186" cy="604" r="4.5" fill="#E2B23C"/>'''


def misheal_arm_r(c, pose="down", sleeve="#74302B"):
    if pose == "wave":
        return f'''
    <path d="M388 526 Q484 520 508 410" fill="none" stroke="{OUTLINE}" stroke-width="52" stroke-linecap="round"/>
    <path d="M388 526 Q484 520 508 410" fill="none" stroke="{c['skin']}" stroke-width="42" stroke-linecap="round"/>
    <circle cx="510" cy="398" r="28" fill="{c['skin']}" {SW}/>
    <path d="M382 504 Q444 482 466 560 L414 580 Q402 540 380 530 Z" fill="{sleeve}" {SW}/>'''
    return f'''
    <path d="M386 520 Q424 590 424 662" fill="none" stroke="{OUTLINE}" stroke-width="52" stroke-linecap="round"/>
    <path d="M386 520 Q424 590 424 662" fill="none" stroke="{c['skin']}" stroke-width="42" stroke-linecap="round"/>
    <path d="M392 502 Q436 524 440 618 L386 626 Q376 560 382 504 Z" fill="{sleeve}" {SW}/>
    <circle cx="414" cy="604" r="4.5" fill="#E2B23C"/>'''


def misheal_glasses(c):
    return '''
    <path d="M150 304 L194 300 M406 300 L450 304" stroke="#C9A75A" stroke-width="5" stroke-linecap="round"/>
    <circle cx="232" cy="318" r="48" fill="#3A2E33" opacity="0.93" stroke="#C9A75A" stroke-width="5"/>
    <circle cx="368" cy="318" r="48" fill="#3A2E33" opacity="0.93" stroke="#C9A75A" stroke-width="5"/>
    <path d="M280 312 Q300 300 320 312" fill="none" stroke="#C9A75A" stroke-width="5"/>
    <path d="M206 300 Q218 288 236 286" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.5"/>
    <path d="M342 300 Q354 288 372 286" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.5"/>'''


def hands_down(c, r=28):
    return f'''
    <circle cx="168" cy="672" r="{r}" fill="{c['skin']}" {SW}/>
    <circle cx="432" cy="672" r="{r}" fill="{c['skin']}" {SW}/>'''


# ----------------------------------------------------------------- assembly
OUTFITS = {
    # name: (sleeve_left, sleeve_right)
    "gul": {"polo": ("#B9A58F", "#5B3B2F"), "tee": ("#E84A3C", "#E84A3C"), "bluetee": ("#3D8BFD", "#3D8BFD")},
    "misheal": {"kurta": ("#74302B", "#74302B"), "yellow": ("#FFC93C", "#FFC93C"), "pink": ("#FF7EB6", "#FF7EB6")},
}
DEFAULT_OUTFIT = {"gul": "tee", "misheal": "yellow"}


def layers(name, eyes="open", mouth="smile", arm="down", glasses=False, outfit=None):
    """Ordered (layer_name, svg) list, back to front. The face/hair layers never change;
    the outfit (body + sleeves) is swappable per video."""
    c = CHARS[name]
    girl = name == "misheal"
    outfit = outfit or DEFAULT_OUTFIT[name]
    sl, sr = OUTFITS[name][outfit]
    L = []
    if girl:
        L.append(("hair_back", misheal_hair_back(c)))
    L.append((f"body_{outfit}", misheal_body(c, outfit) if girl else gul_body(c, outfit)))
    hx_l, hx_r, hr = (176, 424, 26) if girl else (168, 432, 28)
    L.append((f"arm_l_{outfit}", (misheal_arm_l(c, sl) if girl else gul_arm_l(c, sl))
              + f'<circle cx="{hx_l}" cy="672" r="{hr}" fill="{c["skin"]}" {SW}/>'))
    if arm == "wave":
        L.append((f"arm_r_wave_{outfit}", misheal_arm_r(c, "wave", sr) if girl else gul_arm_r(c, "wave", sr)))
    else:
        L.append((f"arm_r_down_{outfit}", (misheal_arm_r(c, "down", sr) if girl else gul_arm_r(c, "down", sr))
                  + f'<circle cx="{hx_r}" cy="672" r="{hr}" fill="{c["skin"]}" {SW}/>'))
    L.append(("neck", neck(c)))
    L.append(("head", ears(c) + face(c) + cheeks(c) + nose(c)))
    eye_fn = {"open": eyes_open, "closed": eyes_closed, "blink": eyes_blink}[eyes]
    L.append((f"eyes_{eyes}", eye_fn(c, lashes=girl)))
    L.append(("brows", brows(c, name)))
    L.append((f"mouth_{mouth}", MOUTHS[mouth]))
    L.append(("hair_front", misheal_hair_front(c) if girl else gul_hair_front(c)))
    if girl:
        L.append(("earrings", misheal_earrings(c)))
    if glasses:
        L.append(("glasses", misheal_glasses(c) if girl else gul_glasses(c)))
    return L


def svg(parts, w=W, h=H, scale=1.0):
    body = "".join(s for _, s in parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * scale:.0f}" height="{h * scale:.0f}" '
            f'viewBox="0 0 {w} {h}">{body}</svg>')


def chrome_shot(html, out_png, w, h, scale=2):
    tmp = HERE / "_render.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={out_png}", tmp.as_uri()],
                   check=True, capture_output=True)
    tmp.unlink()


def grid_html(cells, cw, ch, cols, bg="transparent"):
    rows = (len(cells) + cols - 1) // cols
    divs = "".join(f'<div style="position:absolute;left:{(i % cols) * cw}px;top:{(i // cols) * ch}px;'
                   f'width:{cw}px;height:{ch}px">{c}</div>' for i, c in enumerate(cells))
    return (f'<html><body style="margin:0;background:{bg};width:{cols * cw}px;height:{rows * ch}px;'
            f'position:relative;overflow:hidden">{divs}</body></html>'), cols * cw, rows * ch


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if which == "preview":
        cells = [svg(layers("gul", outfit="polo")), svg(layers("misheal", outfit="kurta")),
                 svg(layers("gul", arm="wave", mouth="open")), svg(layers("misheal", arm="wave", mouth="open", eyes="closed")),
                 svg(layers("gul", glasses=True, outfit="polo")), svg(layers("misheal", glasses=True, outfit="kurta"))]
        html, w, h = grid_html(cells, W, H, 6, bg="#FFF6E5")
        chrome_shot(html, str(HERE / "preview.png"), w, h, scale=1)
        print("wrote preview.png")


def export_layers():
    """Render every layer of both characters (all outfits / eyes / mouths / arms) as
    transparent 1200x2000 PNGs on the shared canvas, so videos can stack them."""
    for name in CHARS:
        seen = {}
        for outfit in OUTFITS[name]:
            for arm in ("down", "wave"):
                for eyes in ("open", "closed", "blink"):
                    for mouth in MOUTHS:
                        for lname, s in layers(name, eyes, mouth, arm, True, outfit):
                            seen.setdefault(lname, s)
        names = sorted(seen)
        cells = [svg([(n, seen[n])]) for n in names]
        html, w, h = grid_html(cells, W, H, 6)
        sheet = HERE / f"_{name}_layers.png"
        chrome_shot(html, str(sheet), w, h, scale=2)
        im = Image.open(sheet)
        out = HERE / "layers" / name
        out.mkdir(parents=True, exist_ok=True)
        for i, n in enumerate(names):
            x, y = (i % 6) * W * 2, (i // 6) * H * 2
            im.crop((x, y, x + W * 2, y + H * 2)).save(out / f"{n}.png")
        sheet.unlink()
        print(name, len(names), "layers:", ", ".join(names))


def character_sheet(path):
    cells = []
    for name, o1, o2 in (("gul", "polo", "tee"), ("misheal", "kurta", "yellow")):
        cells += [svg(layers(name, outfit=o1)), svg(layers(name, outfit=o2)),
                  svg(layers(name, arm="wave", mouth="open", outfit=o2)),
                  svg(layers(name, eyes="closed", mouth="smile", outfit=o2)),
                  svg(layers(name, mouth="o", outfit=o2)),
                  svg(layers(name, glasses=True, outfit=o1))]
    html, w, h = grid_html(cells, W, H, 6, bg="#FFF6E5")
    chrome_shot(html, str(path), w, h, scale=1)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "export":
    export_layers()
    character_sheet(HERE / "Character Sheet v3.png")
    print("wrote Character Sheet v3.png")
