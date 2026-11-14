#!/usr/bin/env python3
"""Liu Hui's割圆术 (method of exhaustion) - Douyin video, 20s, 1080x1920, 30fps.
Storyboard:
  0-4s   hook: unit circle + inscribed hexagon already drawn at frame 0,
         "拿多边形，也能逼近圆周率", counter "6 边形 -> pi ~ 3.0000"
  4-8s   12-gon draws in, "12 边形 -> pi ~ 3.1058"
  8-12s  24-gon, "24 边形 -> pi ~ 3.1326"
  12-16s 48-gon then 96-gon, "96 边形 -> pi ~ 3.1410"
  16-20s closing freeze: "割圆术" + "割之弥细，所失弥少"
Numbers are EXACT: inscribed regular n-gon, pi ~ n*sin(pi/n)
(perimeter / diameter, diameter = 2R). Verified 2026-11-13:
  n=6 -> 3.0000, n=12 -> 3.1058, n=24 -> 3.1326, n=48 -> 3.1394,
  n=96 -> 3.1410. (Liu Hui historically cut to 3072 sides -> 3.1416;
  the video stops at 96 sides / 3.1410 and does not claim otherwise.)
Opening push-in 1.0 -> 1.12 over first 2.6s, centred on the circle
(CX=540, CY=860), same as Buffon. No follow CTA, no capsule inside.
"""
import math
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 20.0
NFRAMES = int(DUR * FPS)
OUT = "/home/hatch/workspace/imagine_media/liuhui-20s-1080x1920.mp4"

BG = (10, 10, 15)
BLUE = (88, 196, 221)
YELLOW = (255, 217, 61)
GREEN = (131, 193, 103)
WHITE = (248, 250, 252)
GREY = (138, 148, 166)
CARD = (17, 20, 31)
CIRCLE_COL = (96, 118, 150)

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


# ---------- exact numbers (verified) ----------
STAGES = [
    # (t_start, n_sides)
    (0.0, 6),
    (4.0, 12),
    (8.0, 24),
    (12.0, 48),
    (14.0, 96),
]
for _, n in STAGES:
    print(f"n={n:3d}  pi~{n * math.sin(math.pi / n):.4f}", flush=True)


def stage_at(t):
    """(n_sides, seg_local_t) for time t; seg_local resets each stage."""
    cur_n, cur_start = STAGES[0][1], STAGES[0][0]
    for start, n in STAGES:
        if t >= start:
            cur_n, cur_start = n, start
    return cur_n, t - cur_start


CX, CY, R = 540.0, 860.0, 300.0


def polygon_points(n):
    return [
        (CX + R * math.cos(2 * math.pi * k / n - math.pi / 2),
         CY + R * math.sin(2 * math.pi * k / n - math.pi / 2))
        for k in range(n)
    ]


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

    # faint circle the polygon is approximating
    d.ellipse([zx(CX - R), zy(CY - R), zx(CX + R), zy(CY + R)],
              outline=CIRCLE_COL + (255,), width=3)

    # polygon: edges draw in over the first 1.0s of each stage
    n, local = stage_at(t)
    pts = polygon_points(n)
    if local < 0.05:
        frac = 1.0  # frame 0: hexagon fully visible (motion at open)
    else:
        frac = min(1.0, local / 1.0)
    drawn = frac * n
    full = int(drawn)
    for k in range(min(full, n)):
        a, b = pts[k], pts[(k + 1) % n]
        d.line([zx(a[0]), zy(a[1]), zx(b[0]), zy(b[1])],
               fill=BLUE + (255,), width=5)
    if full < n and frac > 0:
        a = pts[full]
        b = pts[(full + 1) % n]
        p = drawn - full
        mx = a[0] + (b[0] - a[0]) * p
        my = a[1] + (b[1] - a[1]) * p
        d.line([zx(a[0]), zy(a[1]), zx(mx), zy(my)],
               fill=BLUE + (255,), width=5)
    # vertices
    for k in range(min(full + 1, n)):
        px, py = pts[k]
        d.ellipse([zx(px - 6), zy(py - 6), zx(px + 6), zy(py + 6)],
                  fill=YELLOW + (255,))

    d.rectangle([zx(30), zy(520), zx(1050), zy(1200)],
                outline=BLUE + (255,), width=4)
    img.alpha_composite(layer)

    d = ImageDraw.Draw(img)

    # hook, fades in within 0.33s
    p = ease_out(t / 0.33)
    if p > 0:
        draw_centered_text(d, 250, "拿多边形，也能逼近圆周率",
                           cjk(60), (255, 255, 255, int(255 * p)))
        draw_centered_text(d, 340, "割圆术 · 刘徽",
                           cjk(32, bold=False), (138, 148, 166, int(255 * p)))

    est = n * math.sin(math.pi / n)

    if t < 16:
        draw_centered_text(d, 1300, f"{n} 边形",
                           cjk(56), WHITE + (255,))
        draw_centered_text(d, 1400, f"周长 ÷ 直径 ≈ {est:.4f}",
                           cjk(52), GREEN + (255,))
        draw_centered_text(d, 1500, "边越多，越接近圆",
                           cjk(30, bold=False), GREY + (255,))
    else:
        q = ease_out((t - 16) / 0.6)
        if q > 0:
            draw_centered_text(d, 1300, "割圆术",
                               cjk(64), (255, 255, 255, int(255 * q)))
            draw_centered_text(d, 1400, "割之弥细，所失弥少",
                               cjk(52), (255, 217, 61, int(255 * q)))
            draw_centered_text(d, 1500, "96 边形 → π ≈ 3.1410",
                               cjk(30, bold=False), (138, 148, 166, int(255 * q)))

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
