"""Cut a vertical Short (1080x1920) from a long video's renderer, with a 1-2 second hook:
frame 1 = the most exciting moment (teaser), a punchy sound at 0:00, a white flash, then the full moment.
Top band = big hook title, bottom band = live captions of what Gul & Mishu say, blurred video behind both.

python tools/make_short.py <key>        e.g. nose, xray, brush, rocket, says, pull, junk
"""
import importlib.util, json, math, os, subprocess, sys, pathlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
FPS, W, H = 30, 1080, 1920
SR = 48000

CONFIGS = {
    "nose": dict(proj="long05-body-parts", mod="render3.py", mix="mix2.wav", tl="timeline2.json", frame="V2.render_frame",
                 teaser=(5.35, 6.9), segs=[(5.28, 22.0)], cx=960, zoom=1.3,
                 title="WHERE'S MY NOSE?!", out="S05 Wheres My Nose", name="Where's My Nose - Short"),
    "xray": dict(proj="long05-body-parts", mod="render3.py", mix="mix2.wav", tl="timeline2.json", frame="V2.render_frame",
                 teaser=(290.9, 292.4), segs=[(285.06, 306.64)], cx=960, zoom=1.45,
                 title="WHAT'S INSIDE YOU?", out="S06 Whats Inside Your Body", name="Inside Your Body - Short"),
    "brush": dict(proj="long04-good-habits", mod="render.py", mix="mix.wav", tl="timeline.json", frame="render_frame",
                  teaser=(89.7, 91.2), segs=[(62.9, 95.16)], cx=960, zoom=1.4,
                  title="BRUSH WITH US!", out="S07 Brush Your Teeth Song", name="Brush Your Teeth Song - Short"),
    "rocket": dict(proj="long02-counting", mod="render.py", mix="mix.wav", tl="timeline.json", frame="render_frame",
                   teaser=(655.3, 656.9), segs=[(646.5, 660.5)], cx=960, zoom=1.45,
                   title="BLAST OFF!", out="S08 Rocket Countdown", name="Rocket Countdown - Short"),
    "says": dict(proj="long05-body-parts", mod="render3.py", mix="mix2.wav", tl="timeline2.json", frame="V2.render_frame",
                 teaser=(380.5, 382.0), segs=[(368.68, 395.33)], cx=960, zoom=0.95,
                 title="MISHU SAYS!", out="S09 Mishu Says", name="Mishu Says - Short"),
    "pull": dict(proj="long03-fruits-veg", mod="render.py", mix="mix.wav", tl="timeline.json", frame="render_frame",
                 teaser=(143.1, 144.7), segs=[(137.48, 151.86), (166.6, 181.9)], cx=960, zoom=1.35,
                 title="PULL IT OUT!", out="S10 Pull It Out Vegetables", name="Pull It Out - Short"),
    "junk": dict(proj="long04-good-habits", mod="render.py", mix="mix.wav", tl="timeline.json", frame="render_frame",
                 teaser=(231.0, 232.5), segs=[(217.95, 250.7)], cx=1040, zoom=1.3,
                 title="HEALTHY OR JUNK?", out="S11 Healthy or Junk Food", name="Healthy or Junk Food - Short"),
}
FLASH = 0.18


def load_renderer(cfg):
    d = ROOT / cfg["proj"]
    sys.path.insert(0, str(ROOT / "long02-counting"))
    sys.path.insert(1, str(d))
    spec = importlib.util.spec_from_file_location("srcrender", d / cfg["mod"])
    mod = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, ["x"]
    old = os.getcwd()
    os.chdir(d)
    spec.loader.exec_module(mod)
    mod.init()
    os.chdir(old)
    sys.argv = argv
    fn = mod
    for part in cfg["frame"].split("."):
        fn = getattr(fn, part)
    return mod, fn


def plan(cfg):
    """List of (out_time, src_time) and the cut points (for the flash)."""
    pieces = [cfg["teaser"]] + list(cfg["segs"])
    m, cuts, t = [], [], 0.0
    for a, b in pieces:
        n = int(round((b - a) * FPS))
        for i in range(n):
            m.append(a + i / FPS)
        t += n / FPS
        cuts.append(t)
    return m, cuts[:-1], pieces


def font_text(R, img, cx, cy, text, size, maxw=1000, colour=None):
    R.rainbow_text(img, cx, cy, text, size, maxw=maxw, colour=colour)


def caption(R, img, text, y):
    d = ImageDraw.Draw(img)
    size = 50
    f = R.font(size)
    words, lines, cur = text.split(), [], ""
    for w in words:
        if d.textlength((cur + " " + w).strip(), font=f) > 960:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    for i, ln in enumerate(lines[:2]):
        w = d.textlength(ln, font=f)
        d.text((W / 2 - w / 2, y + i * 70), ln, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(58, 36, 32))


def compose(R, land, t_out, total, cfg, cuts, line):
    z = cfg["zoom"]
    big = land.resize((int(1920 * z), int(1080 * z)), Image.BICUBIC)
    cw = W
    x0 = int(cfg["cx"] * z - cw / 2)
    x0 = max(0, min(big.width - cw, x0))
    mid = big.crop((x0, 0, x0 + cw, big.height))
    bg = land.resize((96, 54)).filter(ImageFilter.GaussianBlur(2)).resize((W * 2, H), Image.BICUBIC).crop((W // 2, 0, W // 2 + W, H))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (30, 20, 60)), 0.35).convert("RGBA")
    y0 = (H - mid.height) // 2
    bg.paste(mid, (0, y0))
    d = ImageDraw.Draw(bg)
    d.rectangle((0, y0 - 6, W, y0), fill=(255, 255, 255))
    d.rectangle((0, y0 + mid.height, W, y0 + mid.height + 6), fill=(255, 255, 255))
    end = t_out > total - 2.2
    title = "WATCH THE FULL VIDEO!" if end else cfg["title"]
    pulse = 1 + 0.06 * math.sin(t_out * 6)
    k = min(1.0, t_out / 0.25)
    font_text(R, bg, W / 2, y0 / 2 + 12, title, int(min(118, y0 * 0.6) * pulse * (0.6 + 0.4 * k)), maxw=1020)
    if line:
        caption(R, bg, line, y0 + mid.height + max(20, (y0 - 70) / 2))
    for c in cuts:                                                   # white flash at the cut after the teaser
        if 0 <= t_out - c < FLASH:
            a = int(255 * (1 - (t_out - c) / FLASH))
            bg.alpha_composite(Image.new("RGBA", bg.size, (255, 255, 255, a)))
    return bg.convert("RGB")


def build_audio(cfg, pieces, cuts, out_wav):
    sys.path.insert(0, str(ROOT / "ep02-colours"))
    import audio_mix as A
    x, sr = sf.read(ROOT / cfg["proj"] / cfg["mix"])
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    parts = []
    for a, b in pieces:
        seg = x[int(a * sr): int(a * sr) + int(round((b - a) * FPS)) * sr // FPS].copy()
        f = min(len(seg) // 4, int(0.02 * sr))
        seg[:f] *= np.linspace(0, 1, f)[:, None]
        seg[-f:] *= np.linspace(1, 0, f)[:, None]
        parts.append(seg)
    y = np.concatenate(parts)
    hit = np.zeros_like(y)                                           # punchy sound at 0:00 + whoosh at each cut
    A.add(hit, A.sfx_sparkle(), 0.0, 0.5)
    A.add(hit, A.sfx_pop(), 0.0, 0.6)
    for c in cuts:
        A.add(hit, A.sfx_whoosh(), max(0, c - 0.15), 0.5)
    y = y + hit
    y /= np.abs(y).max() / 0.9
    sf.write(out_wav, y.astype(np.float32), sr, subtype="PCM_16")


def main(key):
    cfg = CONFIGS[key]
    mod, frame_fn = load_renderer(cfg)
    R = sys.modules.get("render") or mod
    tl = json.load(open(ROOT / cfg["proj"] / cfg["tl"]))
    lines = tl["lines"]
    times, cuts, pieces = plan(cfg)
    total = len(times) / FPS
    out_dir = ROOT / "VIDEOS" / cfg["out"]
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "tools" / f"_short_{key}"
    tmp.mkdir(exist_ok=True)
    build_audio(cfg, pieces, cuts, tmp / "a.wav")
    vid = tmp / "v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(vid)], stdin=subprocess.PIPE)
    for i, ts in enumerate(times):
        land = frame_fn(int(round(ts * FPS)))
        cur = next((e["text"] for e in reversed(lines) if e["t"] - 0.05 <= ts < e["t"] + e["dur"] + 0.35), None)
        p.stdin.write(compose(R, land, i / FPS, total, cfg, cuts, cur).tobytes())
        if i == 0:
            land.save(tmp / "_first_land.png")
    p.stdin.close()
    p.wait()
    dst = out_dir / f"{cfg['name']} {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(tmp / "a.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst, f"{total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
