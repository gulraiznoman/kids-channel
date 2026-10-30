"""Short S17: GARBAGE TRUCK CLEAN-UP. The truck's arm lifts bins and CRUNCHES the trash; grey / blue / yellow / green bins
(trash, paper, plastic, food), then it beeps away. Hook at 0:00: a bin is already flying up and flips at 0.5 s.
python tools/short_garbage.py art|frames|video
"""
import math, os, subprocess, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
_argv = sys.argv[1:]
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(ROOT / "tools"))
import rhyme_shorts as RS
import rhyme_v4 as RV
sys.path.insert(0, str(ROOT / "long01-animals-fun"))
import art as ART

A, M, LS, R, SR = RS.A, RS.M, RS.LS, RS.R, RS.SR
W, H, FPS = 1080, 1920, 30
SW, INK = ART.SW, ART.INK
TMP = ROOT / "tools" / "_garbage"
TMP.mkdir(exist_ok=True)

BINS = [  # bin colour, label, trash pieces, line said at the flip
    ("grey", "TRASH!", ["trashbag", "trashbag2", "can"], "Crunch, crunch, crunch!"),
    ("blue", "PAPER!", ["newspaper", "box", "paperball"], "Paper and boxes!"),
    ("yellow", "PLASTIC!", ["bottle", "cup", "bottle2"], "Plastic bottles!"),
    ("green", "FOOD!", ["bananapeel", "applecore", "eggshell"], "Yucky old food!"),
]
BIN_HEX = {"grey": "#8C93A3", "blue": "#2E8CFF", "yellow": "#FFC928", "green": "#3BB54A"}
BIN_RGB = {"grey": (140, 147, 163), "blue": (46, 140, 255), "yellow": (255, 201, 40), "green": (59, 181, 74)}
HOOK = 3.4           # first (grey) bin, already lifting at 0:00
SEG = 4.2            # each later bin
OUT_T = HOOK + SEG * 3
TOTAL = OUT_T + 4.0
ROAD = 1440          # wheel line
PIVOT = (800, 1010)  # top of the hopper where the arm turns
GROUND = (925, 1440)  # bin bottom-centre when it waits


# ------------------------------------------------------------------ art (SVG, rendered once)
def svg_items():
    I = {}
    I["truck"] = f'''<rect x="40" y="430" width="900" height="40" rx="12" fill="#4A4F5C" {SW}/>
<path d="M300 140 L860 140 Q900 140 905 180 L920 440 L300 440 Z" fill="#3BB54A" {SW}/>
<path d="M330 200 L880 200 M330 260 L885 260" stroke="#2E9440" stroke-width="12"/>
<rect x="430" y="300" width="300" height="90" rx="20" fill="#FFFFFF" {SW}/>
<path d="M470 345 l25 -30 l25 30 M555 345 l25 -30 l25 30 M640 345 l25 -30 l25 30" stroke="#3BB54A" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M820 140 L940 120 L960 200 L905 200 Z" fill="#2E9440" {SW}/>
<path d="M60 440 L60 230 Q60 190 100 185 L240 175 Q290 172 300 220 L300 440 Z" fill="#FFD23F" {SW}/>
<path d="M85 300 L85 235 Q87 210 110 208 L235 200 Q262 200 266 225 L270 300 Z" fill="#9ED8FF" {SW}/>
<circle cx="180" cy="250" r="14" fill="#FFFFFF" opacity="0.7"/>
<rect x="40" y="380" width="40" height="40" rx="8" fill="#FFF3B0" {SW}/><rect x="150" y="160" width="60" height="22" rx="8" fill="#FF6B6B" {SW}/>
<rect x="250" y="330" width="40" height="12" rx="6" fill="#4A4F5C"/>'''
    I["wheel"] = f'<circle cx="200" cy="200" r="150" fill="#2B2B33" {SW}/><circle cx="200" cy="200" r="70" fill="#C9CCD6" {SW}/><circle cx="200" cy="200" r="20" fill="#4A4F5C"/>' + \
        "".join(f'<rect x="192" y="135" width="16" height="30" rx="5" fill="#4A4F5C" transform="rotate({a} 200 200)"/>' for a in range(0, 360, 72))
    for c, hx in BIN_HEX.items():
        I[f"bin_{c}"] = f'''<path d="M90 110 L310 110 L290 380 L110 380 Z" fill="{hx}" {SW}/>
<rect x="70" y="80" width="260" height="42" rx="12" fill="{hx}" {SW}/><rect x="170" y="62" width="60" height="22" rx="8" fill="{hx}" {SW}/>
<path d="M140 160 L150 340 M200 160 L200 340 M260 160 L250 340" stroke="#000" stroke-opacity="0.15" stroke-width="12" stroke-linecap="round"/>
<circle cx="120" cy="385" r="22" fill="#2B2B33" {SW}/><circle cx="280" cy="385" r="22" fill="#2B2B33" {SW}/>'''
    I["trashbag"] = f'<path d="M200 70 Q170 110 120 140 Q60 220 90 310 Q120 370 200 370 Q280 370 310 310 Q340 220 280 140 Q230 110 200 70 Z" fill="#3A3A44" {SW}/><path d="M175 75 l25 -40 l25 40" stroke="{INK}" stroke-width="8" fill="#3A3A44"/><path d="M150 200 Q160 260 140 310" stroke="#55556A" stroke-width="10" fill="none" stroke-linecap="round"/>'
    I["trashbag2"] = I["trashbag"].replace("#3A3A44", "#5A6070")
    I["can"] = f'<rect x="130" y="90" width="140" height="240" rx="20" fill="#C9CCD6" {SW}/><rect x="130" y="150" width="140" height="110" fill="#FF6B6B" stroke="{INK}" stroke-width="5"/><ellipse cx="200" cy="92" rx="70" ry="16" fill="#E9EBF0" {SW}/>'
    I["newspaper"] = f'<path d="M70 110 L330 90 L340 300 L80 320 Z" fill="#FFFFFF" {SW}/>' + "".join(
        f'<path d="M{110} {150 + k * 34 - k * 1.5} L{300} {137 + k * 34 - k * 1.5}" stroke="#9AA0AE" stroke-width="10" stroke-linecap="round"/>' for k in range(5))
    I["box"] = f'<path d="M80 150 L320 150 L320 340 L80 340 Z" fill="#D9A066" {SW}/><path d="M80 150 L140 80 L380 80 L320 150 Z" fill="#E8B77E" {SW}/><path d="M320 150 L380 80 L380 270 L320 340 Z" fill="#B97E45" {SW}/><path d="M200 150 L200 210" stroke="{INK}" stroke-width="6"/>'
    I["paperball"] = f'<circle cx="200" cy="200" r="130" fill="#FFFFFF" {SW}/><path d="M110 170 L180 210 L150 280 M220 100 L230 190 L310 220 M200 300 L240 240" stroke="#B8BCC8" stroke-width="7" fill="none"/>'
    I["bottle"] = f'<rect x="165" y="40" width="70" height="50" rx="10" fill="#2E8CFF" {SW}/><path d="M160 90 L240 90 L270 150 L270 360 Q270 380 250 380 L150 380 Q130 380 130 360 L130 150 Z" fill="#BDE6FF" {SW}/><rect x="130" y="200" width="140" height="80" fill="#7ED957" stroke="{INK}" stroke-width="5"/>'
    I["bottle2"] = I["bottle"].replace("#7ED957", "#FF8FB1").replace("#2E8CFF", "#FF6B6B")
    I["cup"] = f'<path d="M110 110 L290 110 L265 360 L135 360 Z" fill="#FFFFFF" {SW}/><rect x="95" y="85" width="210" height="35" rx="10" fill="#FF8FB1" {SW}/><path d="M125 200 L275 200" stroke="#FF8FB1" stroke-width="18"/>'
    I["bananapeel"] = f'<path d="M200 120 Q150 220 70 300 Q120 320 190 230 Q200 330 160 380 Q230 360 220 240 Q280 330 340 320 Q260 240 220 120 Z" fill="#FFD23F" {SW}/><rect x="185" y="70" width="30" height="60" rx="8" fill="#8A5A2B" {SW}/><path d="M200 140 Q190 200 180 230" stroke="#E0A800" stroke-width="7" fill="none"/>'
    I["applecore"] = f'<path d="M130 70 Q200 40 270 70 Q240 120 230 200 Q240 280 270 330 Q200 360 130 330 Q160 280 170 200 Q160 120 130 70 Z" fill="#FFF3D6" {SW}/><path d="M130 70 Q200 40 270 70 L262 85 Q200 62 138 85 Z" fill="#E8352E" stroke="{INK}" stroke-width="5"/><path d="M138 318 Q200 340 262 318 L270 330 Q200 360 130 330 Z" fill="#E8352E" stroke="{INK}" stroke-width="5"/><path d="M200 50 L205 15" stroke="#8A5A2B" stroke-width="12" stroke-linecap="round"/><ellipse cx="190" cy="190" rx="10" ry="16" fill="#5A3A22"/><ellipse cx="215" cy="215" rx="10" ry="16" fill="#5A3A22"/>'
    I["eggshell"] = f'<path d="M90 220 Q90 360 200 360 Q310 360 310 220 L270 250 L240 200 L200 255 L160 195 L125 250 Z" fill="#FFF8EC" {SW}/><path d="M120 160 Q200 40 280 160 L250 140 L220 175 L190 130 L160 170 Z" fill="#FFF8EC" {SW} transform="rotate(-25 200 120) translate(-30 -40)"/>'
    return I


def bg_street():
    return f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FD3FF"/><stop offset="1" stop-color="#D6F1FF"/></linearGradient></defs>
      <rect width="1080" height="1920" fill="url(#sk)"/>
      <circle cx="900" cy="420" r="80" fill="#FFD23F" {SW}/>
      <g fill="#FFFFFF">{"".join(f'<ellipse cx="{x}" cy="{y}" rx="90" ry="38"/><ellipse cx="{x + 55}" cy="{y - 22}" rx="58" ry="38"/>' for x, y in ((160, 520), (620, 470)))}</g>
      <rect x="40" y="760" width="300" height="560" fill="#FFB3C7" {SW}/><path d="M20 770 L190 620 L360 770 Z" fill="#E8573C" {SW}/>
      <rect x="90" y="830" width="90" height="90" fill="#9ED8FF" {SW}/><rect x="200" y="830" width="90" height="90" fill="#9ED8FF" {SW}/>
      <rect x="390" y="700" width="330" height="620" fill="#B7E4A8" {SW}/><path d="M370 710 L555 560 L740 710 Z" fill="#4C79D8" {SW}/>
      <rect x="440" y="780" width="100" height="100" fill="#9ED8FF" {SW}/><rect x="580" y="780" width="100" height="100" fill="#9ED8FF" {SW}/>
      <rect x="770" y="820" width="280" height="500" fill="#FFE08A" {SW}/><path d="M750 830 L910 700 L1070 830 Z" fill="#9B5DE5" {SW}/>
      <rect x="0" y="1300" width="1080" height="40" fill="#BFC4CF" {SW}/>
      <rect x="0" y="1338" width="1080" height="210" fill="#5C6070"/>
      {"".join(f'<rect x="{x}" y="1438" width="80" height="14" rx="6" fill="#FFFFFF"/>' for x in range(30, 1080, 160))}
      <rect x="0" y="1548" width="1080" height="372" fill="#D9DCE4"/><rect x="0" y="1548" width="1080" height="18" fill="#BFC4CF"/>
      {"".join(f'<path d="M{x} 1566 L{x} 1920" stroke="#C9CCD6" stroke-width="6"/>' for x in range(0, 1080, 180))}'''


def make_art():
    I = svg_items()
    names = [n for n in I if n != "truck"]
    cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{I[n]}</svg></div>'
                    for i, n in enumerate(names))
    w = 400 * len(names)
    ART.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>', str(TMP / "_items.png"), w, 400, scale=2)
    im = Image.open(TMP / "_items.png")
    for i, n in enumerate(names):
        im.crop((i * 800, 0, i * 800 + 800, 800)).save(TMP / f"item_{n}.png")
    (TMP / "_items.png").unlink()
    ART.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500">{I["truck"]}</svg></body></html>',
             str(TMP / "item_truck.png"), 1000, 500, scale=2)
    ART.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">{bg_street()}</svg></body></html>',
             str(TMP / "bg.png"), 1080, 1920)
    print("art done", len(names))


# ------------------------------------------------------------------ timing
def segs():
    """(colour, t_start, lift0, lift1, flip, back0, back1, slide_out, seg_end)"""
    out = [("grey", 0.0, -0.3, 0.35, 0.5, 1.4, 2.1, 2.5, HOOK)]
    for k in range(1, 4):
        t0 = HOOK + (k - 1) * SEG
        out.append((BINS[k][0], t0, t0 + 0.9, t0 + 1.8, t0 + 2.2, t0 + 2.9, t0 + 3.5, t0 + 3.6, t0 + SEG))
    return out


def plan():
    L = [("mishu", "Garbage truck!", 0.05, 1.3), ("gul", "Crunch, crunch, crunch!", 1.4, 1.6)]
    for k in range(1, 4):
        t0 = HOOK + (k - 1) * SEG
        a, b = ("gul", "mishu") if k % 2 else ("mishu", "gul")
        L += [(a, BINS[k][0].capitalize() + " bin!", t0 + 0.1, 1.1), (b, BINS[k][3], t0 + 2.2, 1.5)]
    L += [("both", "Beep beep! Bye bye, trash!", OUT_T + 0.4, 2.0), ("mishu", "Keep it clean!", OUT_T + 2.6, 1.2)]
    return L


# ------------------------------------------------------------------ audio (all made in code)
rng = np.random.default_rng(17)


def noise(d, lp=1):
    x = rng.standard_normal(int(d * SR))
    return np.convolve(x, np.ones(lp) / lp, mode="same") if lp > 1 else x


def whirr(d):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 90 + 70 * t / d
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25 + noise(d, 30)[:n] * 0.8
    return np.convolve(x, np.ones(20) / 20, mode="same") * np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.1)


def crunch():
    d = 0.9
    n = int(d * SR)
    out = np.zeros(n)
    for k in range(9):
        a = int(rng.uniform(0, 0.6) * SR)
        m = int(0.07 * SR)
        out[a:a + m] += noise(0.07, 3)[:m] * np.exp(-np.arange(m) / SR / 0.02) * rng.uniform(0.5, 1.0)
    t = np.arange(n) / SR
    return out + np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.25) * 0.8


def beep():
    out = np.zeros(int(1.0 * SR))
    for k in range(2):
        m = int(0.22 * SR)
        t = np.arange(m) / SR
        out[int(k * 0.4 * SR):int(k * 0.4 * SR) + m] += np.sign(np.sin(2 * np.pi * 1040 * t)) * 0.3 * np.minimum(1, (0.22 - t) / 0.02)
    return out


def engine(d):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 38 + 25 * np.minimum(1, t / 1.5)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * 0.5 * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t)) * np.minimum(1, (d - t) / 0.4)


def audio(path):
    n = int(TOTAL * SR)
    v = np.zeros((n, 2))
    for who, text, t, slot in plan():
        for w, g, pan in ((("mishu", 0.95, 0.12), ("gul", 0.5, -0.12)) if who == "both" else ((who, 1.0, 0.0),)):
            A.add(v, RS.chant(w, text, slot), t, g, pan)
    RS.CHORD.setdefault("D", [62, 66, 69])
    beat = 0.45
    song = {"chords": ["G", "C", "D", "G"]}
    tune = [79, 83, 86, 83, 84, 81, 79, 0, 81, 83, 86, 88, 86, 83, 81, 0]
    toks = [dict(t=i * beat, dur=beat, notes=[tune[i % 16]]) for i in range(int(TOTAL / beat)) if tune[i % 16]]
    m = RV.exciting_music(song, toks, TOTAL, beat)
    fx = np.zeros_like(m)
    for c, t0, l0, l1, flip, b0, b1, so, end in segs():
        if c != "grey":
            A.add(fx, A.sfx_whoosh(), t0, 0.3)                       # bin rolls in
        A.add(fx, whirr(l1 - max(l0, 0)), max(l0, 0), 0.5)
        A.add(fx, crunch(), flip, 0.9)
        A.add(fx, LS.kick() * 1.1, flip, 0.6)
        A.add(fx, whirr(b1 - b0), b0, 0.35)
    A.add(fx, beep(), OUT_T + 0.3, 0.5)
    A.add(fx, engine(3.4), OUT_T + 0.2, 0.6)
    A.add(fx, A.sfx_sparkle(), OUT_T + 2.6, 0.4)
    v /= np.abs(v).max() / 0.9
    e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
    m = m / np.abs(m).max() * (1 - 0.35 * e)[:, None]
    LS.finish_audio(v + m * 0.55 + fx * 0.6, path)


# ------------------------------------------------------------------ frames
def bez(p0, p1, p2, k):
    return ((1 - k) ** 2 * p0[0] + 2 * (1 - k) * k * p1[0] + k * k * p2[0], (1 - k) ** 2 * p0[1] + 2 * (1 - k) * k * p1[1] + k * k * p2[1])


def bin_pose(k):
    """k=0 on the ground, k=1 tipped over the hopper. Returns centre and rotation."""
    g = (GROUND[0], GROUND[1] - 140)
    top = (PIVOT[0] + 40, PIVOT[1] - 150)
    c = bez(g, (GROUND[0] + 90, PIVOT[1] - 120), top, k)
    return c, 150 * k


def frame(G, t):
    fr = G["bg"].copy()
    d = ImageDraw.Draw(fr)
    # which bin is active
    cur = None
    for sg in segs():
        if sg[1] <= t < sg[8]:
            cur = sg
    shake = 0
    if cur and cur[4] <= t < cur[4] + 0.5:
        shake = 8 * math.sin(t * 70) * (1 - (t - cur[4]) / 0.5)
    drive = 0
    if t >= OUT_T + 0.6:
        q = t - OUT_T - 0.6
        drive = -min(1600, 260 * q * q + 80 * q)
    tx = 420 + drive + shake
    # bin + arm (drawn behind the truck body)
    if cur:
        c, t0, l0, l1, flip, b0, b1, so, end = cur
        if t < l0:
            k = 0
        elif t < l1:
            k = R.ease_io((t - l0) / (l1 - l0))
        elif t < b0:
            k = 1
        elif t < b1:
            k = 1 - R.ease_io((t - b0) / (b1 - b0))
        else:
            k = 0
        if c == "grey" and t < l1:
            k = 0.55 + 0.45 * R.ease_io(min(1, t / 0.35))
        (bx, by), rot = bin_pose(k)
        if c != "grey" and t < t0 + 0.6:
            bx += 400 * (1 - R.ease_back((t - t0) / 0.6))
        if t >= so:
            bx += 900 * ((t - so) / 0.6) ** 2
        px, py = PIVOT[0] + shake, PIVOT[1]
        d.line((px, py, bx, by), fill=(90, 95, 110), width=34)
        d.line((px, py, bx, by), fill=(150, 155, 170), width=20)
        d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=(90, 95, 110), outline=INK, width=5)
        LS.paste(fr, G["bin"][c], bx, by, rot=rot)
        # trash flies out of the bin into the hopper
        pieces = next(b[2] for b in BINS if b[0] == c)
        if t < flip - 0.2 and not (c == "grey" and t > l1):
            for j, p in enumerate(pieces):          # peeking out of the bin while it's full
                if k < 0.5:
                    a = math.radians(rot)
                    ox, oy = (j - 1) * 55, -120
                    LS.paste(fr, G["trash"][p], bx + ox * math.cos(a) + oy * math.sin(a), by - ox * math.sin(a) + oy * math.cos(a), scale=0.85, rot=rot + (j - 1) * 15)
        for j, p in enumerate(pieces):
            tj = flip - 0.35 + j * 0.12
            if tj <= t < tj + 0.7:
                u = (t - tj) / 0.7
                sx, sy = bin_pose(1)[0]
                ex, ey = PIVOT[0] - 140 + j * 50, PIVOT[1] + 40
                x = sx + (ex - sx) * u
                y = sy + (ey - sy) * u - 260 * math.sin(math.pi * u) - 60 * (j - 1)
                LS.paste(fr, G["trash"][p], x, y, scale=1.0 - 0.4 * u, rot=360 * u * (1 if j % 2 else -1))
    # truck
    LS.paste(fr, G["truck"], tx, ROAD - 230 - abs(shake) * 0.6)
    for wx in (tx - 340, tx + 110, tx + 300):
        spin = (drive / 1.0) % 360
        LS.paste(fr, G["wheel"], wx, ROAD - 10, rot=spin)
    if t >= OUT_T + 0.3:                                       # exhaust puffs while driving off
        dd = ImageDraw.Draw(fr, "RGBA")
        for j in range(5):
            p = ((t - OUT_T) * 1.5 + j / 5) % 1
            r = 24 + 50 * p
            x, y = tx + 470 + 120 * p, ROAD - 60 - 120 * p
            dd.ellipse((x - r, y - r, x + r, y + r), fill=(235, 235, 240, int(200 * (1 - p))))
    # words
    if cur:
        c = cur[0]
        lab = next(b[1] for b in BINS if b[0] == c)
        if t >= cur[4]:
            R.rainbow_text(fr, W / 2, 260, lab, int(200 * R.ease_back((t - cur[4]) / 0.25)), colour=BIN_RGB[c] if c != "grey" else None, maxw=1000)
            if t < cur[4] + 0.8:
                q = (t - cur[4]) / 0.8
                R.rainbow_text(fr, PIVOT[0] - 260, PIVOT[1] - 260 - 40 * q, "CRUNCH!", int(120 * R.ease_back(q / 0.3)), colour=(255, 255, 255), maxw=700)
        elif c != "grey":
            R.rainbow_text(fr, W / 2, 260, f"{c.upper()} BIN!", int(180 * R.ease_back((t - cur[1]) / 0.3)), colour=BIN_RGB[c], maxw=1000)
        else:
            R.rainbow_text(fr, W / 2, 260, "GARBAGE TRUCK!", int(150 * (1 + 0.08 * math.sin(t * 12))), maxw=1000)
    if t >= OUT_T:
        q = t - OUT_T
        R.rainbow_text(fr, W / 2, 260, "BEEP BEEP!", int(190 * R.ease_back(q / 0.3)), maxw=1000)
        if t >= OUT_T + 2.6:
            R.rainbow_text(fr, W / 2, 520, "KEEP IT CLEAN!", int(110 * R.ease_back((t - OUT_T - 2.6) / 0.3)), colour=(59, 181, 74), maxw=1000)
            d2 = ImageDraw.Draw(fr)
            for j in range(10):
                a = j / 10 * 2 * math.pi + t
                R.star(d2, 540 + 440 * math.cos(a), 520 + 130 * math.sin(a), 24, R.RAINBOW[j % 6], rot=t * 2)
    # kids on the pavement
    for name, outfit, x, off in (("gul", "polo", 200, 0.0), ("misheal", "kurta", 880, 0.5)):
        im = LS.character(name, outfit, mouth="open" if ((t * 2 + off) % 1) < 0.5 else "smile", wave=18 * math.sin(t * 6.28 + off * 3))
        LS.paste(fr, im, x, 1912 - 22 * abs(math.sin((t * 2 + off) * math.pi)), scale=0.27, bottom=True)
    return fr.convert("RGB")


def load_G():
    R.G["fonts"] = {}
    G = {"bg": Image.open(TMP / "bg.png").convert("RGBA"), "truck": LS.load(TMP / "item_truck.png", 960),
         "wheel": LS.load(TMP / "item_wheel.png", 150),
         "bin": {c: LS.load(TMP / f"item_bin_{c}.png", 310) for c in BIN_HEX},
         "trash": {p: LS.load(TMP / f"item_{p}.png", 150) for b in BINS for p in b[2]}}
    return G


def main():
    if _argv and _argv[0] == "art":
        make_art()
        return
    G = load_G()
    if _argv and _argv[0] == "frames":
        ts = [float(x) for x in _argv[1].split(",")] if len(_argv) > 1 else [0.0, 0.5, 0.9, 1.3, 4.0, 5.5, 6.0, 12.0, 16.5, 18.5]
        sheet = Image.new("RGB", (270 * 5, 480 * ((len(ts) + 4) // 5)))
        for i, t in enumerate(ts):
            sheet.paste(frame(G, t).resize((270, 480)), ((i % 5) * 270, (i // 5) * 480))
        sheet.save(TMP / "_sheet.png")
        print("sheet", TMP / "_sheet.png")
        return
    audio(TMP / "a.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(TMP / "v.mp4")],
                         stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)):
        p.stdin.write(frame(G, f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    out = ROOT / "VIDEOS" / "S17 Garbage Truck" / f"Garbage Truck - Short {os.environ.get('VER', 'v1')}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "v.mp4"), "-i", str(TMP / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
