#!/usr/bin/env python3
"""Earth belt problem (give Earth a belt) - Douyin video, 20s, 1080x1920, 30fps.
Problem: a rope fits snugly around Earth's equator. Lift it so it sits 1m
above the ground all the way around. How much longer must the rope be?
Answer: 2*pi ~ 6.28 m, INDEPENDENT of Earth's size.
Math (exact, verified 2026-11-15):
  C  = 2*pi*r           (r = 6371 km)
  C' = 2*pi*(r+1)
  C' - C = 2*pi*(r+1) - 2*pi*r = 2*pi = 6.283185... m -> 6.28 m
  The radius cancels. Earth's circumference 2*pi*6371 ~ 40030 km.
Storyboard (lesson from Liu Hui, weakest ever: payoff came too late,
so the answer lands in the first seconds):
  0-2.5s  hook: Earth + rope already drawn at frame 0, rope lifts off the
          surface to a visible 1m gap (schematic, gap exaggerated),
          "给地球系根腰带 / 离地1米，绳子要加长多少？"
  2.5-8s  ANSWER big on screen: "6.28米" + "2pi ~ 6.28 米"
  8-12s   why: formula "2pi(r+1) - 2pi*r = 2pi", radius lines r / r+1,
          "r 抵消了，跟地球多大没关系"
  12-16s  scale check: a basketball with its own rope ring,
          "换成篮球，也一样 / 还是 6.28 米"
  16-20s  closing freeze: "6.28米" + "周长差就是 2pi" + formula
Opening push-in 1.0 -> 1.12 over first 2.6s, centred on Earth (540, 860),
same as Liu Hui / Buffon. No follow CTA, no capsule inside.
"""
import math
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 20.0
NFRAMES = int(DUR * FPS)
OUT = "/home/hatch/workspace/imagine_media/earthbelt-20s-1080x1920.mp4"

BG = (10, 10, 15)
BLUE = (88, 196, 221)
YELLOW = (255, 217, 61)
RED = (255, 107, 107)
GREEN = (131, 193, 103)
WHITE = (248, 250, 252)
GREY = (138, 148, 166)
CARD = (17, 20, 31)
OCEAN = (36, 116, 190)
LAND = (131, 193, 103)
BALL = (214, 122, 62)

CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CJK_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def cjk(sz, bold=True):
    return ImageFont.truetype(CJK if bold else CJK_R, sz, index=0)


def mono(sz):
    return ImageFont.truetype(MONO, sz)


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


print("2*pi =", 2 * math.pi, "-> 6.28 m", flush=True)
print("Earth C = 2*pi*6371 km =", 2 * math.pi * 6371, "km", flush=True)

CX, CY, R = 540.0, 860.0, 300.0


def rope_radius(t):
    """Snug (R+4) at t=0, lifts to R+55 by t=2.0, gentle pulse after."""
    if t < 2.0:
        return R + 4 + 51 * ease_out(t / 2.0)
    if t < 16.0:
        return R + 55 + 3 * math.sin(2 * math.pi * (t - 2.0) / 2.0)
    return R + 55


# ---------- background ----------
def make_bg():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for gx in range(40, W, 90):
        for gy in range(40, H, 90):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(24, 27, 40))
    return img


BGIMG = make_bg()


def draw_centered_text(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def draw_earth(zx, zy):
    """Earth disc with abstract continents + cloud arcs, centred (CX, CY).
    Returns an RGBA layer clipped to the disc."""
    earth = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    de = ImageDraw.Draw(earth)
    de.ellipse([zx(CX - R), zy(CY - R), zx(CX + R), zy(CY + R)], fill=OCEAN + (255,))
    blobs = [
        (430, 700, 120, 70), (600, 780, 150, 80), (470, 950, 130, 60),
        (650, 1000, 90, 50), (560, 680, 70, 40), (380, 860, 80, 55),
    ]
    for bx, by, bw, bh in blobs:
        de.ellipse([zx(bx - bw / 2), zy(by - bh / 2), zx(bx + bw / 2), zy(by + bh / 2)],
                   fill=LAND + (255,))
    for (ax, ay, aw, ah, a0, a1) in [
        (470, 760, 260, 90, 200, 330), (600, 980, 240, 80, 20, 150),
        (540, 700, 200, 70, 300, 60),
    ]:
        de.arc([zx(ax - aw / 2), zy(ay - ah / 2), zx(ax + aw / 2), zy(ay + ah / 2)],
               a0, a1, fill=(255, 255, 255, 110), width=6)
    de.ellipse([zx(CX - R), zy(CY - R), zx(CX + R), zy(CY + R)],
               outline=(120, 170, 220, 255), width=3)
    mask = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(mask)
    dm.ellipse([zx(CX - R), zy(CY - R), zx(CX + R), zy(CY + R)], fill=255)
    return Image.composite(earth, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask)


def render_frame(i):
    t = i / FPS
    img = BGIMG.copy().convert("RGBA")

    zoom = 1.0 + 0.12 * ease_out(t / 2.6) if t < 2.6 else 1.12

    def zx(x):
        return CX + (x - CX) * zoom

    def zy(y):
        return CY + (y - CY) * zoom

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # field card
    d.rectangle([zx(30), zy(520), zx(1050), zy(1200)], fill=CARD + (255,))

    layer.alpha_composite(draw_earth(zx, zy))

    # rope ring
    rr = rope_radius(t)
    d.ellipse([zx(CX - rr), zy(CY - rr), zx(CX + rr), zy(CY + rr)],
              outline=YELLOW + (255,), width=7)

    # 1m gap indicator (upper right, -30 deg), fades in from t=1.2
    q = ease_out((t - 1.2) / 0.6)
    if q > 0:
        a = math.radians(-30)
        ex = CX + R * math.cos(a)
        ey = CY + R * math.sin(a)
        rx = CX + rr * math.cos(a)
        ry = CY + rr * math.sin(a)
        col = YELLOW + (int(255 * q),)
        d.line([zx(ex), zy(ey), zx(rx), zy(ry)], fill=col, width=4)
        # label placed clearly OUTSIDE the rope ring so the "1" can't
        # be covered by the ring line
        la = math.radians(-30)
        lx = CX + (rr + 48) * math.cos(la)
        ly = CY + (rr + 48) * math.sin(la)
        fnt = cjk(32)
        lw = d.textlength("1米", font=fnt)
        d.text((zx(lx) - lw / 2, zy(ly) - 16), "1米", font=fnt,
               fill=(255, 217, 61, int(255 * q)))
        d.text((zx(1050) - 320, zy(1150)), "示意图 · 间隙已放大",
               font=cjk(24, bold=False), fill=(138, 148, 166, int(255 * q)))

    # radius lines r / r+1 (upper left, 135 deg) during the formula phase
    if 8.0 <= t < 12.0:
        q2 = ease_out((t - 8.0) / 0.5)
        a = math.radians(135)
        ex = CX + R * math.cos(a)
        ey = CY + R * math.sin(a)
        rx = CX + rr * math.cos(a)
        ry = CY + rr * math.sin(a)
        d.line([zx(CX), zy(CY), zx(ex), zy(ey)],
               fill=(255, 255, 255, int(255 * q2)), width=4)
        d.line([zx(ex), zy(ey), zx(rx), zy(ry)],
               fill=(255, 217, 61, int(255 * q2)), width=4)
        d.text((zx(375), zy(700)), "r",
               font=cjk(36), fill=(255, 255, 255, int(255 * q2)))
        d.text((zx(255), zy(585)), "r+1",
               font=cjk(36), fill=(255, 217, 61, int(255 * q2)))

    # basketball mini-diagram (bottom right of the card) 12-16s
    if t >= 12.0:
        q3 = ease_out((t - 12.0) / 0.6)
        bx, by, br = 880.0, 1060.0, 48.0
        d.ellipse([zx(bx - br), zy(by - br), zx(bx + br), zy(by + br)],
                  fill=(BALL[0], BALL[1], BALL[2], int(255 * q3)))
        d.arc([zx(bx - br), zy(by - br), zx(bx + br), zy(by + br)],
              300, 60, fill=(120, 60, 20, int(255 * q3)), width=4)
        d.arc([zx(bx - br), zy(by - br), zx(bx + br), zy(by + br)],
              120, 240, fill=(120, 60, 20, int(255 * q3)), width=4)
        d.ellipse([zx(bx - br - 14), zy(by - br - 14), zx(bx + br + 14), zy(by + br + 14)],
                  outline=YELLOW + (int(255 * q3),), width=5)
        d.text((zx(bx) - 30, zy(by + br + 16)), "篮球",
               font=cjk(28, bold=False), fill=(138, 148, 166, int(255 * q3)))

    d.rectangle([zx(30), zy(520), zx(1050), zy(1200)],
                outline=BLUE + (255,), width=4)
    img.alpha_composite(layer)

    d = ImageDraw.Draw(img)

    # hook, fades in within 0.33s
    p = ease_out(t / 0.33)
    if p > 0:
        draw_centered_text(d, 250, "给地球系根腰带",
                           cjk(60), (255, 255, 255, int(255 * p)))
        draw_centered_text(d, 340, "离地1米，绳子要加长多少？",
                           cjk(34, bold=False), (138, 148, 166, int(255 * p)))

    if t < 2.5:
        draw_centered_text(d, 1300, "地球半径 6371km",
                           cjk(44), WHITE + (255,))
        draw_centered_text(d, 1400, "绳子正好贴着地面",
                           cjk(32, bold=False), GREY + (255,))
    elif t < 8.0:
        q = ease_out((t - 2.5) / 0.5)
        if q > 0:
            draw_centered_text(d, 1280, "6.28米",
                               cjk(110), (255, 217, 61, int(255 * q)))
            draw_centered_text(d, 1430, "2π ≈ 6.28 米",
                               cjk(46), (131, 193, 103, int(255 * q)))
    elif t < 12.0:
        q = ease_out((t - 8.0) / 0.5)
        if q > 0:
            draw_centered_text(d, 1300, "2π(r+1) − 2πr = 2π",
                               cjk(48), (255, 255, 255, int(255 * q)))
            draw_centered_text(d, 1400, "r 抵消了，跟地球多大没关系",
                               cjk(34, bold=False), (138, 148, 166, int(255 * q)))
    elif t < 16.0:
        q = ease_out((t - 12.0) / 0.5)
        if q > 0:
            draw_centered_text(d, 1300, "换成篮球，也一样",
                               cjk(52), (255, 255, 255, int(255 * q)))
            draw_centered_text(d, 1400, "还是 6.28 米",
                               cjk(52), (255, 217, 61, int(255 * q)))
    else:
        draw_centered_text(d, 1280, "6.28米",
                           cjk(100), YELLOW + (255,))
        draw_centered_text(d, 1410, "周长差就是 2π",
                           cjk(48), WHITE + (255,))
        draw_centered_text(d, 1490, "2π(r+1) − 2πr = 2π",
                           cjk(34), GREEN + (255,))

    return img.convert("RGB")


def main():
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-movflags", "+faststart", OUT,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0 = time.time()
    try:
        for i in range(NFRAMES):
            frame = render_frame(i)
            proc.stdin.write(frame.tobytes())
            if i % 60 == 0:
                print(i, "frames, %.1fs elapsed" % (time.time() - t0), flush=True)
    finally:
        proc.stdin.close()
        proc.wait()
    print("done", NFRAMES, "frames in %.1fs" % (time.time() - t0))
    print("saved:", OUT)


if __name__ == "__main__":
    main()
