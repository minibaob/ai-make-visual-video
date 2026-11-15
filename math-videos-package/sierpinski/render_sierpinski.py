#!/usr/bin/env python3
"""Sierpinski triangle - Douyin video, 20s, 1080x1920, 30fps.
Collection episode 12 (fractal line, after Koch).

KEY LESSON from Liu Hui (weakest ever: 579 plays, 13.5% completion):
the payoff came too late. So the finished fractal is ALREADY on screen
at frame 0 (iteration 5, zooming in), and only then do we rebuild it.

Storyboard:
  0-4s   hook: finished Sierpinski (iter 5) fully visible at frame 0,
         zooming in; "一个三角形，挖掉中间" / "挖 5 次，只剩 23.7%"
  4-6s   reset (0.3s crossfade) to solid triangle, iter 0, 100%
  6-8s   iter 1: 3 triangles, 75.0%
  8-10s  iter 2: 9 triangles, 56.3%
  10-12s iter 3: 27 triangles, 42.2%
  12-14s iter 4: 81 triangles, 31.6%
  14-16s iter 5: 243 triangles, 23.7%
  16-20s closing freeze: "谢尔宾斯基三角形" + "面积 -> 0，图形还在"

Math (verified 2026-11-15): each iteration removes the central inverted
triangle of every filled triangle, leaving 3 copies at half scale;
remaining area after n iterations = (3/4)^n of the original:
  n=0 -> 100.0%, n=1 -> 75.0%, n=2 -> 56.3% (56.25, half-up),
  n=3 -> 42.2%, n=4 -> 31.6%, n=5 -> 23.7%.
As n -> infinity, (3/4)^n -> 0, yet the fractal set never disappears.

Opening push-in 1.0 -> 1.12 over first 2.6s, centred on the triangle
(CX=540, CY=850), same as Liu Hui/Buffon. No follow CTA, no capsule
inside. New triangles pop in (scale 0.7 -> 1.0 over 0.8s) each stage.
"""
import math
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 20.0
NFRAMES = int(DUR * FPS)
OUT = "/home/hatch/workspace/imagine_media/sierpinski-20s-1080x1920.mp4"

BG = (10, 10, 15)
BLUE = (88, 196, 221)
YELLOW = (255, 217, 61)
GREEN = (131, 193, 103)
RED = (255, 107, 107)
WHITE = (248, 250, 252)
GREY = (138, 148, 166)
CARD = (17, 20, 31)

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


def pct_half_up(n):
    """Remaining area percent after n iterations, 1 decimal, half-up."""
    p = (3 / 4) ** n * 100
    return math.floor(p * 10 + 0.5) / 10


# ---------- exact numbers (verified) ----------
for n in range(6):
    print(f"iter {n}: triangles={3 ** n:3d}  remaining={(3/4)**n:.6f} -> {pct_half_up(n):.1f}%", flush=True)


# ---------- triangle geometry ----------
# Big triangle: apex top, base bottom. Side 620, height 620*sqrt(3)/2 ~ 537.
APEX = (540.0, 580.0)
BL = (230.0, 1117.0)
BR = (850.0, 1117.0)
CX, CY = 540.0, 850.0


def subdivide(tri, n):
    """All filled triangles at iteration n (3^n of them)."""
    if n == 0:
        return [tri]
    (ax, ay), (bx, by), (cx, cy) = tri
    ab = ((ax + bx) / 2, (ay + by) / 2)
    bc = ((bx + cx) / 2, (by + cy) / 2)
    ca = ((cx + ax) / 2, (cy + ay) / 2)
    out = []
    for t in (((ax, ay), ab, ca), (ab, (bx, by), bc), (ca, bc, (cx, cy))):
        out += subdivide(t, n - 1)
    return out


ITERS = [subdivide((APEX, BL, BR), n) for n in range(6)]


def scaled_tri(tri, s):
    """Scale triangle about its centroid by s."""
    cx = sum(p[0] for p in tri) / 3
    cy = sum(p[1] for p in tri) / 3
    return [(cx + (x - cx) * s, cy + (y - cy) * s) for (x, y) in tri]


# ---------- stages ----------
# (t_start, iteration) for the build; hook (0-4s) shows iter 5.
BUILD = [
    (4.0, 0),
    (6.0, 1),
    (8.0, 2),
    (10.0, 3),
    (12.0, 4),
    (14.0, 5),
]


def iteration_at(t):
    """(iteration, local_t, pop_scale) for time t."""
    if t < 4.0:
        return 5, t, 1.0  # hook: finished fractal, no pop-in
    cur_n, cur_start = 0, 4.0
    for start, n in BUILD:
        if t >= start:
            cur_n, cur_start = n, start
    local = t - cur_start
    pop = 0.7 + 0.3 * ease_out(local / 0.8) if local < 0.8 else 1.0
    return cur_n, local, pop


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


def draw_triangles(d, tris, zx, zy, alpha, scale=1.0):
    for tri in tris:
        if scale != 1.0:
            tri = scaled_tri(tri, scale)
        pts = [(zx(x), zy(y)) for (x, y) in tri]
        d.polygon(pts, fill=BLUE + (alpha,))


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

    n, local, pop = iteration_at(t)
    if 4.0 <= t < 4.3:
        # reset crossfade: iter 5 fades out, iter 0 fades in
        p = (t - 4.0) / 0.3
        draw_triangles(d, ITERS[5], zx, zy, int(255 * (1 - p)), scale=1.0)
        draw_triangles(d, ITERS[0], zx, zy, int(255 * p), scale=1.0)
        n = 0
    else:
        draw_triangles(d, ITERS[n], zx, zy, 255, scale=pop)

    d.rectangle([zx(30), zy(520), zx(1050), zy(1200)],
                outline=BLUE + (255,), width=4)
    img.alpha_composite(layer)

    d = ImageDraw.Draw(img)

    # hook, fades in within 0.33s
    p = ease_out(t / 0.33)
    if p > 0 and t < 4.0:
        draw_centered_text(d, 250, "一个三角形，挖掉中间",
                           cjk(60), (255, 255, 255, int(255 * p)))
        draw_centered_text(d, 340, "挖 5 次，只剩 23.7%",
                           cjk(32, bold=False), (255, 217, 61, int(255 * p)))

    if t < 16:
        # counter: iteration + remaining area + shrinking bar
        draw_centered_text(d, 1300, f"第 {n} 次",
                           cjk(56), WHITE + (255,))
        draw_centered_text(d, 1400, f"剩下 {pct_half_up(n):.1f}%",
                           cjk(52), GREEN + (255,))
        frac = (3 / 4) ** n
        bx0, bx1, by = 240, 840, 1480
        d.rectangle([bx0, by, bx1, by + 28], outline=GREY + (255,), width=2)
        if frac > 0:
            d.rectangle([bx0, by, bx0 + (bx1 - bx0) * frac, by + 28],
                        fill=YELLOW + (255,))
        draw_centered_text(d, 1530, "面积 = (3/4)^n",
                           cjk(30, bold=False), GREY + (255,))
    else:
        q = ease_out((t - 16) / 0.6)
        if q > 0:
            draw_centered_text(d, 1300, "谢尔宾斯基三角形",
                               cjk(60), (255, 255, 255, int(255 * q)))
            draw_centered_text(d, 1400, "面积 → 0，图形还在",
                               cjk(52), (255, 217, 61, int(255 * q)))
            draw_centered_text(d, 1500, "每挖一次，面积只剩 3/4",
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
