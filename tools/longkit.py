"""Shared toolkit for Gul & Mishu long videos (L15 onwards).

A video folder needs:
  make.py   -> from longkit import Maker;  M = Maker(__file__);  T = M.TL();  ... ;  M.finish(T, music=dict(...), sfx=fn)
  render.py -> import longkit as K;  K.configure(__file__, outfit, art, bgs, scenes, out_dir, out_name);  if __name__ == "__main__": K.main()
Scene functions get (frame, s, t) and can use K.body / K.item / K.word / ... helpers.
"""
import hashlib, importlib.util, json, math, os, subprocess, sys, pathlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "voices"))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "characters"))

W, H, FPS = 1920, 1080, 30
PRAISE = ["Great job!", "Yes! You got it!", "Awesome!", "Well done!", "Super!", "You're so smart!"]


# =====================================================================================================  MAKE side
class Maker:
    def __init__(self, file):
        _argv = sys.argv
        import kidvoice
        import loop_shorts as LS
        import rhyme_v4 as RV
        sys.argv = _argv
        self.kv, self.LS, self.RV = kidvoice, LS, RV
        self.A, self.M = LS.A, LS.M
        self.SR = self.A.SR
        self.here = pathlib.Path(file).resolve().parent
        self.cache = self.here / "words"
        self.cache.mkdir(exist_ok=True)

    def line(self, who, text):
        c = self.kv.CHARACTERS[who]
        p = self.cache / f"{who}_{hashlib.md5((who + text + str(c)).encode()).hexdigest()[:10]}.wav"
        if not p.exists():
            self.kv.say_as(who, text, p)
        x, sr = sf.read(p)
        idx = np.where(np.abs(x) > 0.03 * np.abs(x).max())[0]
        return x[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.05 * sr)]

    def TL(self):
        return TL(self)

    # -------------------------------------------------------------------------------------------- audio
    def tt(self, d):
        return np.arange(int(d * self.SR)) / self.SR

    def music(self, total, bpm=118, prog=None, hook=None, start=2.5, tick=None):
        A, M, LS, RV, SR = self.A, self.M, self.LS, self.RV, self.SR
        n = int(total * SR)
        mus = np.zeros((n, 2))
        B = 60 / bpm
        prog = prog or [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
        hook = hook or [72, 76, 79, 76, 77, 74, 72, 0, 74, 77, 79, 81, 79, 76, 74, 0]
        bar, t0 = 0, start
        while t0 < total - 1.5:
            ch = prog[bar % 4]
            for q in range(4):
                b0 = t0 + q * B
                A.add(mus, LS.kick(), b0, 0.48)
                if q in (1, 3):
                    A.add(mus, M.clap(), b0, 0.28, 0.05)
                    A.add(mus, RV.snare(), b0, 0.13)
                A.add(mus, LS.hat(), b0 + B / 2, 0.42, -0.3)
                if tick is not None:
                    A.add(mus, tick, b0 + B * 0.75, 0.1, 0.35)
                for e, mm in ((0, ch[0] - 12), (0.5, ch[0]), (0.75, ch[0] - 12)):
                    A.add(mus, RV.bass(mm - 12, B * 0.4), b0 + e * B, 0.28)
                for j, nt in enumerate(ch):
                    A.add(mus, A.tone(A.mtof(nt + 12), 0.3, ((1, 1), (3, 0.3), (5, 0.1)), 0.003, 0.1), b0 + B / 2, 0.045, -0.25 + 0.25 * j)
            if bar % 8 >= 4:
                for i, mm in enumerate(hook[(bar % 2) * 8:(bar % 2) * 8 + 8]):
                    if mm:
                        A.add(mus, M.toy_piano(mm, 0.4), t0 + i * B / 2, 0.06, 0.2)
            t0 += 4 * B
            bar += 1
        ts = np.arange(n) / SR
        mus *= np.clip((total - ts) / 1.5, 0, 1)[:, None]
        return mus

    def std_sfx(self, kind):
        """common sound marks; returns list of (array, offset, gain) or None"""
        A, M, LS = self.A, self.M, self.LS
        if kind == "pop":
            return [(A.sfx_pop(), 0, 0.35)]
        if kind == "slam":
            return [(LS.kick() * 1.3, 0, 0.9), (A.sfx_sparkle(), 0, 0.4)]
        if kind == "riser":
            return [(A.sfx_whoosh(), -0.1, 0.35), (M.clap(), 0.45, 0.35)]
        if kind == "ding":
            return [(A.sfx_ding(84), 0, 0.15)]
        if kind == "yes":
            return [(A.sfx_ding(79), 0, 0.2), (A.sfx_ding(84), 0.12, 0.2)]
        if kind == "stomp2":
            return [(M.stomp(), 0.2 + k * 0.35, 0.4) for k in range(3)]
        if kind == "clap":
            return [(M.clap(), 0.05, 0.4)]
        if kind == "sparkle":
            return [(A.sfx_sparkle(), 0.1, 0.4)]
        if kind == "boing":
            return [(M.boing(), 0, 0.35)]
        if kind == "whoosh":
            return [(A.sfx_whoosh(), 0, 0.35)]
        if kind == "tada":
            return [(A.sfx_sparkle(), 0, 0.6)] + [(M.clap(), 0.2 + k * 0.25, 0.4) for k in range(4)]
        return None

    def finish(self, T, music=None, sfx=None, duck=None):
        """write vocals, timeline.json and mix.wav.  sfx(kind) -> list of (array, offset, gain) for custom marks.
        duck: list of (t0, t1, gain) windows where music drops."""
        A, SR = self.A, self.SR
        total = round(T.t, 2)
        n = int(total * SR)
        tracks = {}
        for s, items in T.voc.items():
            y = np.zeros(n)
            for at, x in items:
                i = int(at * SR)
                y[i:i + len(x)] += x[: n - i]
            tracks[s] = y
            sf.write(self.here / f"vocal_{s}.wav", (y / max(1e-9, np.abs(y).max()) * 0.9).astype(np.float32), SR, subtype="PCM_16")
        json.dump(dict(lines=T.lines, scenes=T.scenes, prompts=T.prompts, stars=T.stars, total=total), open(self.here / "timeline.json", "w"), indent=1)
        mus = self.music(total, **(music or {}))
        if duck:
            g = np.ones(n)
            for a, b, gain in duck:
                g[int(a * SR):int(b * SR)] = np.minimum(g[int(a * SR):int(b * SR)], gain)
            g = np.convolve(g, np.ones(SR // 3) / (SR // 3), mode="same")
            mus *= g[:, None]
        v = np.zeros((n, 2))
        A.add(v, tracks["gul"], 0, 1.0, -0.12)
        A.add(v, tracks["mishu"], 0, 1.0, 0.12)
        v /= np.abs(v).max() / 0.9
        e = np.convolve(np.abs(v).mean(axis=1), np.ones(4800) / 4800, mode="same")
        e = np.clip(e / (np.percentile(e[e > 1e-3], 80) + 1e-9), 0, 1)
        mus = mus / max(1e-9, np.abs(mus).max()) * (1 - 0.5 * e)[:, None]
        f = np.zeros((n, 2))
        for kind, at in T.fx:
            parts = (sfx(kind) if sfx else None) or self.std_sfx(kind) or []
            for x, off, gain in parts:
                A.add(f, x, at + off, gain)
        for st in T.stars:
            A.add(f, A.sfx_sparkle(), st, 0.15)
        for p0, p1 in T.prompts:
            A.add(f, A.sfx_ding(86), p0, 0.1)
        mix = v + mus * 0.33 + f * 0.6
        mix /= np.abs(mix).max() / 0.9
        sf.write(self.here / "mix.wav", mix.astype(np.float32), SR, subtype="PCM_16")
        print(f"total {total}s ({total / 60:.1f} min), {len(T.lines)} lines, {len(T.scenes)} scenes")


class TL:
    def __init__(self, mk):
        self.mk = mk
        self.t, self.lines, self.scenes, self.voc, self.prompts, self.stars, self.fx = 0.0, [], [], {"gul": [], "mishu": []}, [], [], []

    def say(self, who, text, gap=0.3):
        singers = ["gul", "mishu"] if who == "both" else [who]
        d = 0
        for s in singers:
            x = self.mk.line(s, text)
            self.voc[s].append((self.t, x * ((0.9 if s == "mishu" else 0.45) if who == "both" else 1.0)))
            d = max(d, len(x) / self.mk.SR)
        start = round(self.t, 3)
        self.lines.append(dict(who=who, text=text, t=start, dur=round(d, 3)))
        self.t += d + gap + 0.15
        return start

    def pause(self, s):
        self.t += s

    def scene(self, kind, bg, **data):
        sc = dict(kind=kind, bg=bg, t0=round(self.t, 3), **data)
        self.scenes.append(sc)
        return sc

    def end(self, sc):
        sc["t1"] = round(self.t, 3)

    def prompt(self, who, text, wait=2.3):
        self.say(who, text, gap=0.1)
        self.prompts.append((round(self.t, 3), round(self.t + wait, 3)))
        self.pause(wait)

    def mark(self, kind):
        self.fx.append((kind, round(self.t, 3)))
        return round(self.t, 3)

    def title(self, bg, title, who, text):
        sc = self.scene("title", bg, title=title)
        self.mark("riser")
        self.pause(0.5)
        self.say(who, text, gap=0.3)
        self.end(sc)

    def quiz(self, bg, items, kind="quiz"):
        """items: (question, answer, visual)"""
        for k, (q, ans, vis) in enumerate(items):
            a = "gul" if k % 2 == 0 else "mishu"
            sc = self.scene(kind, bg, q=q.upper(), vis=vis)
            self.mark("ding")
            self.prompt(a, q, wait=2.4)
            sc["answer_t"] = self.mark("yes")
            self.say(other(a), ans, gap=0.5)
            self.stars.append(round(self.t, 3))
            self.end(sc)

    def dance(self, bg, moves, who_faster="mishu"):
        """moves: (text, move). two rounds, second faster"""
        for rnd in range(2):
            if rnd == 1:
                sc = self.scene("title", bg, title="FASTER!")
                self.mark("riser")
                self.say(who_faster, "Again, faster!", gap=0.2)
                self.end(sc)
            for text, move in moves:
                sc = self.scene("dance", bg, move=move, fast=rnd == 1, word=text.split("!")[0].upper() + "!")
                self.mark("stomp2" if move in ("stomp", "jump") else "pop")
                sc["say_t"] = self.say("both", text, gap=0.0)
                self.prompts.append((round(self.t, 3), round(self.t + (1.6 if rnd == 0 else 0.9), 3)))
                self.pause(1.6 if rnd == 0 else 0.9)
                self.end(sc)


def other(w):
    return "mishu" if w == "gul" else "gul"


# =====================================================================================================  RENDER side
_spec = importlib.util.spec_from_file_location("l02render", ROOT / "long02-counting" / "render.py")
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
INK, RAINBOW = R.INK, R.RAINBOW
ease_back, ease_io, rt = R.ease_back, R.ease_io, R.rainbow_text
KIT = ROOT / "characters" / "layers"
VOC = {"gul": "gul", "misheal": "mishu"}
G = {}
CFG = {}


def configure(file, outfit, art, bgs, scenes, out_dir, out_name):
    CFG.update(here=pathlib.Path(file).resolve().parent, outfit=outfit, art=art, bgs=bgs, scenes=scenes, out_dir=out_dir, out_name=out_name)


def init():
    from expressions import EMOTIONS
    here = CFG["here"]
    tl = json.load(open(here / "timeline.json"))
    G.update(tl)
    G["EMO"] = EMOTIONS
    G["dur"] = {round(l["t"], 3): l["dur"] for l in tl["lines"]}
    R.G["fonts"] = {}
    G["full"] = {n: {p.stem: Image.open(p).convert("RGBA") for p in (KIT / n).glob("*.png")} for n in ("gul", "misheal")}
    G["item"] = {k: Image.open(p).convert("RGBA") for k, p in CFG["art"].items()}
    G["bg"] = {}
    for k, p in CFG["bgs"].items():
        G["bg"][k] = (p() if callable(p) else Image.open(p)).convert("RGBA").resize((W, H))
    G["env"] = {}
    for n in ("gul", "misheal"):
        x, sr = sf.read(here / f"vocal_{VOC[n]}.wav")
        hop = sr // FPS
        rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(len(x) // hop + 1)])
        G["env"][n] = np.clip(rms / (np.percentile(rms[rms > 0.01], 90) + 1e-6), 0, 1.5)
    G["cache"], G["sized"] = {}, {}
    rng = np.random.default_rng(7)
    G["confetti"] = [(rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(300, 600), rng.uniform(0, 6.28), RAINBOW[int(rng.integers(6))]) for _ in range(120)]


def dur(t0):
    return G["dur"].get(round(t0, 3), 1.5)


def line_text(t0):
    return next((l["text"] for l in G["lines"] if abs(l["t"] - t0) < 0.01), "")


def talking(n, t):
    env = G["env"][n]
    return env[min(int(t * FPS), len(env) - 1)]


def compose(n, t, emo=None, wave=False, outfit=None):
    L = G["full"][n]
    o = outfit or CFG["outfit"][n]
    v = talking(n, t)
    if emo:
        eyes, brw, mouth, ovs = G["EMO"][emo]
        mouth_l = f"x_mouth_{mouth}"
    else:
        eyes, brw, ovs = ("blink" if (t + (1.3 if n == "gul" else 0)) % 4.1 < 0.12 else "open"), None, []
        eyes = f"eyes_{eyes}"
        mouth_l = "mouth_smile" if v < 0.12 else ("mouth_o" if v < 0.5 else "mouth_open")
    key = (n, o, eyes, brw, mouth_l, tuple(ovs), wave or v > 0.12)
    if key in G["cache"]:
        return G["cache"][key]
    girl = n == "misheal"
    im = Image.new("RGBA", (1200, 2000), (0, 0, 0, 0))
    for p in (["hair_back"] if girl else []) + [f"body_{o}", f"arm_l_{o}", f"arm_r_{'wave' if (wave or v > 0.12) else 'down'}_{o}", "neck", "head", eyes]:
        im.alpha_composite(L[p])
    if "lids" in ovs:
        im.alpha_composite(L["x_over_lids"])
    im.alpha_composite(L[f"x_brows_{brw}"] if brw else L["brows"])
    im.alpha_composite(L[mouth_l])
    im.alpha_composite(L["hair_front"])
    if girl:
        im.alpha_composite(L["earrings"])
    for ov in ovs:
        if ov != "lids":
            im.alpha_composite(L[f"x_over_{ov}"])
    if len(G["cache"]) > 80:
        G["cache"].clear()
    G["cache"][key] = im
    return im


def body(frame, n, t, emo, cx, feet=1075, scale=0.5, hop=0.0, rot=0.0, wave=False, outfit=None):
    im = compose(n, t, emo, wave=wave, outfit=outfit)
    sm = im.resize((int(1200 * scale), int(2000 * scale)), Image.BICUBIC)
    if rot:
        sm = sm.rotate(rot, center=(sm.width / 2, sm.height), resample=Image.BICUBIC)
    frame.alpha_composite(sm, (int(cx - sm.width / 2), int(feet - sm.height * 0.93 - hop)))


def head(frame, n, t, emo, cx, cy, scale=0.42):
    im = compose(n, t, emo)
    crop = im.crop((150, 60, 1050, 1000)).resize((int(900 * scale), int(940 * scale)), Image.BICUBIC)
    frame.alpha_composite(crop, (int(cx - crop.width / 2), int(cy - crop.height / 2)))


def side_kids(frame, t, emo=None, xs=(160, 1760), scale=0.3, feet=1075):
    for n, x in zip(("gul", "misheal"), xs):
        body(frame, n, t, emo, x, feet=feet, scale=scale, hop=4 * abs(math.sin(t * 1.4 + (1 if n == "gul" else 0))))


def item(frame, key, cx, cy, size, rot=0.0, alpha=1.0, flip=False):
    if size < 3:
        return
    k = (key, int(size), flip)
    if k not in G["sized"]:
        if len(G["sized"]) > 250:
            G["sized"].clear()
        im = G["item"][key]
        im = im.crop(im.getbbox())
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        f = size / max(im.size)
        G["sized"][k] = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
    im = G["sized"][k]
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * max(0, alpha))))
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def confetti(frame, t, t0):
    d = ImageDraw.Draw(frame)
    for x0, y0, sp, ph, col in G["confetti"]:
        y = y0 + (t - t0) * sp
        if -30 < y < H:
            x = x0 + 40 * math.sin(t * 2 + ph)
            w = 20 * abs(math.cos(t * 5 + ph)) + 4
            d.rectangle((x - w / 2, y - 10, x + w / 2, y + 10), fill=col)


def stars_ring(frame, cx, cy, rx, ry, t, n=8, r=22):
    d = ImageDraw.Draw(frame)
    for j in range(n):
        a = j / n * 2 * math.pi + t
        R.star(d, cx + rx * math.cos(a), cy + ry * math.sin(a), r, RAINBOW[j % 6], rot=t * 2)


def badge(frame, x, y, text, col=(255, 107, 139)):
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((x - 105, y - 45, x + 105, y + 45), radius=40, fill=(255, 255, 255), outline=INK, width=6)
    rt(frame, x, y, text, 56, colour=col)


def word(frame, text, t, t0, y=120, size=130, col=None, maxw=1500, x=960):
    rt(frame, x, y, text, int(size * ease_back((t - t0) / 0.3)), colour=col, maxw=maxw)


def card(frame, x, y, w, h, good=False, dim=False, fill=(255, 255, 255)):
    d = ImageDraw.Draw(frame, "RGBA")
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=30, fill=fill + (110 if dim else 215,),
                        outline=(59, 193, 74) if good else INK, width=14 if good else 6)


def choice_row(frame, t, keys, good, t_ans, y=560, size=300, draw=None):
    """three picture cards; the right one turns green and bounces after t_ans"""
    n = len(keys)
    for i, key in enumerate(keys):
        x = 960 + (i - (n - 1) / 2) * 520
        ok = t >= t_ans and key == good
        dim = t >= t_ans and key != good
        card(frame, x, y, 430, 430, ok, dim)
        bob = 25 * abs(math.sin((t - t_ans) * 6)) if ok else 0
        (draw or item)(frame, key, x, y - bob, size)
        if ok:
            stars_ring(frame, x, y, 250, 250, t, n=8, r=18)


# ---------------------------------------------------------------------------------------------- standard scenes
def scene_title(frame, s, t):
    k = t - s["t0"]
    a = min(1, (s["t1"] - t) / 0.3)
    keys = CFG.get("title_items") or list(G["item"])[:5]
    for j, key in enumerate(keys[:5]):
        ang = j / 5 * 2 * math.pi + t * 0.5
        item(frame, key, 960 + 600 * math.cos(ang), 480 + 230 * math.sin(ang), 170 * ease_back((k - j * 0.06) / 0.4))
    rt(frame, 960, 420, s["title"], int(140 * ease_back(k / 0.5) * max(0.3, a)), start=s["t0"], t=t, maxw=1500)
    side_kids(frame, t, "happy", xs=(190, 1730), scale=0.32)


def scene_dance(frame, s, t, pics=None):
    q = (t - s["t0"]) * (1.7 if s.get("fast") else 1.0)
    mv = s["move"]
    for i, (n, x) in enumerate((("gul", 700), ("misheal", 1220))):
        hop, rot, dx = 0, 0, 0
        if mv in ("jump", "hop"):
            hop = 95 * abs(math.sin(q * 5 + i))
        elif mv in ("stomp", "march"):
            hop = 30 * abs(math.sin(q * 6 + i))
        elif mv in ("sway", "swing", "wiggle"):
            rot = 10 * math.sin(q * 5 + i)
        elif mv in ("shake", "jiggle"):
            dx = 14 * math.sin(q * 40)
        elif mv in ("spin", "twirl"):
            rot = 12 * math.sin(q * 9 + i)
        elif mv in ("stretch", "reach"):
            hop = 40 + 20 * math.sin(q * 3)
        else:
            hop = 40 * abs(math.sin(q * 6 + i))
        body(frame, n, t, "excited" if mv in ("jump", "hop") else "happy", x + dx, scale=0.55, hop=hop, rot=rot, wave=True)
    if pics and mv in pics:
        item(frame, pics[mv], 960, 470, 240)
    word(frame, s["word"], t, s["t0"], size=110)


def scene_quiz(frame, s, t, draw=None):
    q = t - s["t0"]
    rt(frame, 960, 120, s["q"], int(80 * ease_back(q / 0.35)), maxw=1600)
    if t >= s["answer_t"]:
        k = ease_back((t - s["answer_t"]) / 0.4)
        if draw:
            draw(frame, s["vis"], t, k)
        elif s["vis"] in G["item"]:
            item(frame, s["vis"], 960, 580, 420 * k)
        else:
            rt(frame, 960, 580, str(s["vis"]), int(200 * k), colour=RAINBOW[2], maxw=1400)
        stars_ring(frame, 960, 580, 360, 260, t, n=8, r=20)
        side_kids(frame, t, "happy")
    else:
        rt(frame, 960, 580, "?", int(280 + 20 * math.sin(t * 6)), colour=(255, 255, 255))
        side_kids(frame, t)


def render_frame(f):
    t = f / FPS
    sc = next((s for s in G["scenes"] if s["t0"] <= t < s.get("t1", 1e9)), G["scenes"][-1])
    frame = G["bg"][sc["bg"]].copy()
    fn = CFG["scenes"].get(sc["kind"]) or {"title": scene_title, "dance": scene_dance, "quiz": scene_quiz}[sc["kind"]]
    fn(frame, sc, t)
    for p0, p1 in G["prompts"]:
        if p0 <= t < p1:
            k = t - p0
            sc2 = ease_back(k / 0.3) * (1 + 0.04 * math.sin(k * 9))
            w, h = int(520 * sc2), int(110 * sc2)
            if w > 10:
                d = ImageDraw.Draw(frame)
                d.rounded_rectangle((960 - w // 2, 955, 960 + w // 2, 955 + h), radius=h // 2, fill=(255, 255, 255), outline=INK, width=6)
                f2 = R.font(max(8, int(62 * sc2)))
                tw = d.textlength("YOUR TURN!", font=f2)
                d.text((960 - tw / 2, 955 + h * 0.5 - 62 * sc2 * 0.62), "YOUR TURN!", font=f2, fill=(255, 77, 109), stroke_width=4, stroke_fill=(255, 255, 255))
    for st in G["stars"]:
        k = t - st
        if 0 <= k < 1.2:
            d = ImageDraw.Draw(frame)
            for j in range(10):
                a = j / 10 * 2 * math.pi + 0.3
                r = 160 + 380 * min(1, k / 0.6)
                R.star(d, 960 + r * math.cos(a), 600 + r * math.sin(a) * 0.7, int(36 * (1 - max(0, (k - 0.7) / 0.5))) + 1, RAINBOW[j % 6], rot=k * 3)
    return frame.convert("RGB")


def worker_init():
    init()


def render_chunk(args):
    lo, hi, path = args
    if os.path.exists(path):
        n = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                            "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
        if n.isdigit() and int(n) == hi - lo:
            return path
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(lo, hi):
        p.stdin.write(render_frame(f).tobytes())
    p.stdin.close()
    p.wait()
    return path


def main():
    from multiprocessing import Pool
    here = CFG["here"]
    init()
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        if sys.argv[2] == "auto":                       # one frame at 80% of every distinct scene kind (+ every 6th scene)
            seen, fs = set(), []
            for i, s in enumerate(G["scenes"]):
                if s["kind"] not in seen or i % 6 == 0:
                    seen.add(s["kind"])
                    fs.append(int((s["t0"] + (s.get("t1", s["t0"] + 2) - s["t0"]) * 0.8) * FPS))
            fs = fs[:24]
        else:
            fs = [int(x) for x in sys.argv[2].split(",")]
        cols = 4
        sheet = Image.new("RGB", (480 * cols, 270 * ((len(fs) + cols - 1) // cols)))
        for i, f in enumerate(fs):
            sheet.paste(render_frame(f).resize((480, 270)), ((i % cols) * 480, (i // cols) * 270))
        sheet.save(here / "_sheet.png")
        return
    n = int(G["total"] * FPS)
    NW = int(os.environ.get("NW", "3"))
    parts = 24
    bnd = np.linspace(0, n, parts + 1).astype(int)
    (here / "_chunks").mkdir(exist_ok=True)
    jobs = [(bnd[k], bnd[k + 1], str(here / "_chunks" / f"c{k:02d}.mp4")) for k in range(parts)]
    with Pool(NW, initializer=worker_init) as pool:
        done = pool.map(render_chunk, jobs)
    with open(here / "_chunks" / "list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in done)
    out = ROOT / "VIDEOS" / CFG["out_dir"]
    out.mkdir(parents=True, exist_ok=True)
    dst = out / f"{CFG['out_name']} {os.environ.get('VER', 'v1')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(here / "_chunks" / "list.txt"),
                    "-i", str(here / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85:level=0", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    print("wrote", dst)


def srt_and_chapters(here, out_dir):
    """writes VIDEOS/<out_dir>/SUBTITLES - English.srt and returns chapter list from title scenes"""
    here = pathlib.Path(here)
    tl = json.load(open(here / "timeline.json"))
    NM = {"gul": "Gul", "mishu": "Mishu", "both": "Gul & Mishu"}

    def ts(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    L = tl["lines"]
    out = []
    for i, l in enumerate(L):
        end = l["t"] + l["dur"] + 0.2
        if i + 1 < len(L):
            end = min(end, L[i + 1]["t"] - 0.05)
        out.append(f"{i + 1}\n{ts(l['t'])} --> {ts(end)}\n{NM[l['who']]}: {l['text']}\n")
    d = ROOT / "VIDEOS" / out_dir
    d.mkdir(parents=True, exist_ok=True)
    (d / "SUBTITLES - English.srt").write_text("\n".join(out), encoding="utf-8")
    chapters = []
    for s in tl["scenes"]:
        if s["kind"] == "title" and s["title"] != "FASTER!" or s.get("chapter"):
            t = int(s["t0"])
            chapters.append((f"{t // 60}:{t % 60:02d}", s.get("chapter") or s["title"]))
    return chapters
