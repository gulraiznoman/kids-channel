"""v2 frame drawing (patched into make_v2.Scene): peekaboo eyes, spin-out, happy dance, hearts, backflip, dive."""
import math
from PIL import Image, ImageDraw
import make_v2 as M


def puppy_pose(self, t):
    """(cx, top_y, angle, sx, sy, clip) or None; clip hides the part below the box rim."""
    land_top = M.BOX_TOP + 25 - M.PUP_SIZE * 0.92
    inside_top = M.BOX_TOP + 120
    cx = M.BOX_CX
    if t < M.T_OUT or t >= M.T_DIVE + 0.6:
        return None
    if t < M.T_LAND:                                     # spin out in an arc
        k = (t - M.T_OUT) / (M.T_LAND - M.T_OUT)
        y = inside_top + (land_top - inside_top) * k - 330 * math.sin(k * math.pi)
        return cx, y, -360 * M.ease_in_out(k), 1, 1, k < 0.35
    if t < M.T_LAND + 0.25:                              # squash on landing
        sq = math.sin((t - M.T_LAND) / 0.25 * math.pi) * 0.16
        return cx, land_top, 0, 1 + sq, 1 - sq, False
    if t < M.T_FLIP0:                                    # happy dance
        u = t - M.T_LAND - 0.25
        hop = abs(math.sin(u * 2 * math.pi * 1.25)) * 38
        return cx + math.sin(u * 2 * math.pi * 0.62) * 34, land_top - hop, math.sin(u * 2 * math.pi * 1.25) * 9, 1, 1, False
    if t < M.T_FLIP1:                                    # backflip
        k = (t - M.T_FLIP0) / (M.T_FLIP1 - M.T_FLIP0)
        return cx, land_top - 230 * math.sin(k * math.pi), 360 * M.ease_in_out(k), 1, 1, False
    if t < M.T_FLIP1 + 0.25:
        sq = math.sin((t - M.T_FLIP1) / 0.25 * math.pi) * 0.16
        return cx, land_top, 0, 1 + sq, 1 - sq, False
    if t < M.T_DIVE:                                     # wag
        return cx, land_top, math.sin(t * 2 * math.pi * 2.2) * 5, 1, 1, False
    k = (t - M.T_DIVE) / 0.6                             # dive: small jump, flip head-down, drop in
    y = land_top - 180 * math.sin(min(1, k * 1.6) * math.pi / 2) + 760 * max(0, k - 0.45) ** 1.5
    return cx, y, 180 * M.ease_in_out(min(1, k * 1.4)), 1, 1, k > 0.45


def heart(d, hx, hy, r, col):
    d.ellipse((hx - r, hy - r, hx, hy), fill=col)
    d.ellipse((hx, hy - r, hx + r, hy), fill=col)
    d.polygon([(hx - r, hy - r * 0.45), (hx + r, hy - r * 0.45), (hx, hy + r * 0.95)], fill=col)


def frame(self, f):
    t = f / M.FPS
    W, H, INK = M.W, M.H, M.INK
    BX, BT = M.BOX_CX, M.BOX_TOP
    im = self.bg.copy()
    d = ImageDraw.Draw(im)
    ramp = min(1.0, t / 0.3)
    # ---- box motion
    bx_dx = bx_dy = bx_ang = 0.0
    if t < M.T_PEEK0:                                    # hops like it's alive
        ph = (t * 2.0) % 1.0
        bx_dy = -math.sin(ph * math.pi) * 28 * ramp
        bx_ang = math.sin(t * 2 * math.pi) * 4 * ramp
    elif M.T_PEEK1 <= t < M.T_POP:                       # hard shake
        bx_dx = math.sin(t * 2 * math.pi * 13) * 14
        bx_ang = math.sin(t * 2 * math.pi * 13 + 1) * 3
    elif M.T_DIVE + 0.6 <= t < M.T_CLOSE:                # wobble after the dive
        bx_ang = math.sin((t - M.T_DIVE) * 2 * math.pi * 3) * 3 * (1 - (t - M.T_DIVE - 0.6) / (M.T_CLOSE - M.T_DIVE - 0.6))
    # ---- puppy (drawn before the box so the box front hides it)
    pose = puppy_pose(self, t)
    if pose:
        cx, top, ang, sx, sy, clip = pose
        p = self.pup
        if sx != 1 or sy != 1:
            p = p.resize((int(M.PUP_SIZE * sx), int(M.PUP_SIZE * sy)), Image.LANCZOS)
        p = p.rotate(ang, resample=Image.BICUBIC, expand=True)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(p, (int(cx - p.width / 2), int(top + M.PUP_SIZE * (1 - sy) + M.PUP_SIZE * sy / 2 - p.height / 2)))
        if clip:
            ImageDraw.Draw(layer).rectangle((0, BT + 30, W, H), fill=(0, 0, 0, 0))
        im.alpha_composite(layer)
    # ---- peekaboo eyes under the lifted lid
    lift = 0.0
    if M.T_PEEK0 <= t < M.T_PEEK1:
        k = (t - M.T_PEEK0) / (M.T_PEEK1 - M.T_PEEK0)
        lift = 150 * (M.ease_in_out(min(1, k / 0.25)) if k < 0.8 else max(0, 1 - (k - 0.8) / 0.08))
        if lift > 110:
            look = math.sin((t - M.T_PEEK0) * 2 * math.pi * 1.3) * 9
            blink = abs(t - (M.T_PEEK0 + 0.38)) < 0.06
            for ex in (BX - 62, BX + 62):
                ey = BT - 34
                d.ellipse((ex - 40, ey - 28, ex + 40, ey + 28), fill=(40, 30, 30))
                if blink:
                    d.line((ex - 28, ey, ex + 28, ey), fill=(255, 255, 255), width=7)
                else:
                    d.ellipse((ex - 32, ey - 22, ex + 32, ey + 22), fill=(255, 255, 255))
                    d.ellipse((ex - 14 + look, ey - 14, ex + 14 + look, ey + 14), fill=(30, 20, 15))
                    d.ellipse((ex - 8 + look, ey - 11, ex + 1 + look, ey - 2), fill=(255, 255, 255))
    # ---- box body
    body = self.body.rotate(bx_ang, resample=Image.BICUBIC)
    im.alpha_composite(body, (int(BX - body.width / 2 + bx_dx), int(BT - 10 + bx_dy)))
    # ---- lid
    lx, ly, lrot, show = BX + bx_dx, BT - 130 + bx_dy - lift, bx_ang - (8 if lift > 1 else 0), True
    if M.T_POP <= t < M.T_DIVE + 0.45:                   # flies away off the top-right
        k = (t - M.T_POP) / 0.7
        if k < 1:
            lx = BX + 650 * M.ease_in_out(k)
            ly = BT - 130 - 900 * math.sin(k * math.pi / 2)
            lrot = -260 * k
        else:
            show = False
    elif M.T_DIVE + 0.45 <= t < M.T_CLOSE:               # falls back from the top
        k = M.ease_in_out((t - M.T_DIVE - 0.45) / (M.T_CLOSE - M.T_DIVE - 0.45))
        lx, ly, lrot = BX, BT - 130 - 1000 * (1 - k), 20 * (1 - k)
    elif M.T_CLOSE <= t < M.T_CLOSE + 0.25:
        ly -= math.sin((t - M.T_CLOSE) / 0.25 * math.pi) * 16
    if show:
        lr = self.lid.rotate(lrot, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(lr, (int(lx - lr.width / 2), int(ly + self.lid.height / 2 - lr.height / 2)))
    # ---- "?" bubble while the box hops
    if 0.25 <= t < M.T_PEEK0:
        sc = M.ease_back((t - 0.25) / 0.35) * (1 + 0.08 * math.sin(t * 2 * math.pi * 2))
        r = max(1, int(70 * sc))
        qx, qy = BX + 270, BT - 190 + bx_dy * 0.5
        d.ellipse((qx - r, qy - r, qx + r, qy + r), fill=(255, 255, 255), outline=INK, width=6)
        f_ = M.font(max(8, int(100 * sc)))
        tw = d.textlength("?", font=f_)
        d.text((qx - tw / 2, qy - 66 * sc), "?", font=f_, fill=(255, 77, 109), stroke_width=4, stroke_fill=INK)
    # ---- pop burst
    k = t - M.T_POP
    if 0 <= k < 1.0:
        cols = [(255, 77, 109), (255, 159, 28), (255, 210, 63), (59, 193, 74), (46, 168, 255), (155, 93, 229)]
        for j in range(14):
            a_ = j / 14 * 2 * math.pi
            rr = 80 + 460 * M.ease_in_out(k / 0.8)
            sz = int(32 * (1 - max(0, k - 0.6) / 0.4)) + 1
            M.star(d, BX + rr * math.cos(a_), BT - 80 + rr * math.sin(a_) * 0.7, sz, cols[j % 6], k * 4)
    # ---- hearts floating up during the dance
    for j in range(6):
        k = t - (M.T_LAND + 0.2 + j * 0.35)
        if 0 <= k < 1.6:
            hx = BX + (-1) ** j * (190 + 30 * j) + math.sin(k * 5 + j) * 20
            hy = BT - 280 - k * 260
            r = 28 * min(1, k / 0.2) * (1 - max(0, k - 1.2) / 0.4)
            if r > 2:
                heart(d, hx, hy, r, [(255, 90, 130), (255, 130, 170)][j % 2])
    # ---- word label
    flip_hide = M.T_FLIP0 - 0.15 <= t < M.T_FLIP1 + 0.2
    if M.T_BARK - 0.1 <= t < M.T_DIVE and not flip_hide:
        t_in = M.T_BARK - 0.1 if t < M.T_FLIP0 else M.T_FLIP1 + 0.2
        sc = M.ease_back((t - t_in) / 0.4) * (1 + 0.04 * math.sin(t * 2 * math.pi * 2))
        if t > M.T_DIVE - 0.3:
            sc *= max(0, (M.T_DIVE - t) / 0.3)
        if sc > 0.05:
            M.rainbow_word(im, BX, 150, M.LABEL, int(165 * sc))
    # ---- kids
    for name, L, girl, outfit, x in (("gul", self.g, False, "tee", 250), ("mishu", self.m, True, "yellow", 830)):
        mouth, speaking = self.mouth(name, t)
        if mouth is None:
            surprised = (M.T_PEEK0 + 0.2 <= t < M.T_PEEK1 + 0.2) or (M.T_POP <= t < M.T_LAND + 0.1) or (M.T_FLIP0 <= t < M.T_FLIP0 + 0.4)
            mouth = "o" if surprised else "smile"
        cheer = (3.45 <= t < 4.35) or (M.T_FLIP1 - 0.1 <= t < M.T_FLIP1 + 0.6)
        eyes = "closed" if cheer else "open"
        fi = int(t * M.FPS)
        if eyes == "open" and ((name == "gul" and fi % 130 in (40, 41, 42)) or (name == "mishu" and fi % 150 in (95, 96, 97))):
            eyes = "blink"
        wave_ang = None
        if name == "mishu" and 5.65 <= t < 7.0:
            wave_ang = -12 * math.sin((t - 5.65) * 2 * math.pi * 1.6)
        if name == "gul" and 3.45 <= t < 4.35:
            wave_ang = -14 * math.sin((t - 3.45) * 2 * math.pi * 2)
        c = M.compose_char(L, girl, outfit, eyes, mouth, wave_ang)
        hop = 0.0
        if speaking:
            hop -= abs(math.sin(t * 2 * math.pi * 1.8)) * 12
        if cheer:
            hop -= abs(math.sin(t * 2 * math.pi * 2.2)) * 55
        if M.T_OUT <= t < M.T_OUT + 0.5:
            hop -= math.sin((t - M.T_OUT) / 0.5 * math.pi) * 40
        im.alpha_composite(c, (int(x - c.width / 2), int(H - 0.93 * c.height - 10 + hop)))
    return im.convert("RGB")


M.Scene.frame = frame
