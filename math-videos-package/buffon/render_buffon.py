#!/usr/bin/env python3
"""Buffon's needle estimation of pi - Douyin video, 20s, 1080x1920, 30fps.
Storyboard:
  0-4s   hook: parallel lines + needles raining in from frame 0,
         "往地上扔针，居然能算出 π"
  4-8s   live counters: needles crossing a line vs total needles
  8-12s  formula "2 × 总针数 ÷ 压线针数 ≈ π" + live estimate
  12-16s estimate converges: "针越多，越接近 3.14" + live estimate vs 3.1416
  16-20s closing freeze: "布丰投针" + "随机，也能算出 π"
Numbers are REAL: one simulation, fixed seed 20261112, N=1500 needles,
needle length l = line spacing d = 120 px, so P(cross) = 2l/(pi*d) = 2/pi
and pi = 2N/C. First 60 needles present at t=0, the rest arrive uniformly
over (0,16s]. Needle centres uniform over exactly 5 line periods
(y 560..1160) so the residue mod d is uniform.
Checkpoints (verified 2026-11-12):
  t=0:  60/36   est 3.3333 (noisy, not shown)
  t=4:  440/285 est 3.0877
  t=8:  789/508 est 3.1063
  t=12: 1155/728 est 3.1731
  t=16: 1500/946 est 3.1712 (final, frozen for closing)
Opening push-in 1.0 -> 1.12 over the first 2.6s, centred on the field
(CY=860); spec says 1.9, but 1.9x would push the field off-frame and over
the hook/counter text (Koch used 1.10, Monte Carlo 1.22, same reason).
No follow CTA, no capsule inside the video.
"""
import bisect
import math
import random
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 20.0
NFRAMES = int(DUR * FPS)
OUT = "/home/hatch/workspace/imagine_media/buffon-20s-1080x1920.mp4"

BG = (10, 10, 15)
BLUE = (88, 196, 221)
YELLOW = (255, 217, 61)
RED = (255, 107, 107)
GREEN = (131, 193, 103)
WHITE = (248, 250, 252)
GREY = (138, 148, 166)
CARD = (17, 20, 31)
LINE_COL = (96, 118, 150)

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


# ---------- simulation (real numbers, fixed seed) ----------
SEED = 20261112
N = 1500
D = 120.0   # line spacing; needle length l = D
L = 120.0
Y0, Y1 = 560.0, 1160.0
CX, CY = 540.0, 860.0  # field centre (zoom centre)

rng = random.Random(SEED)
NEEDLES = []  # (arrival_t, cx, cy, theta, crosses)
for i in range(N):
    cx = rng.uniform(40, 1040)
    cy = rng.uniform(Y0, Y1)
    th = rng.uniform(0, math.pi)
    r = (cy - 560.0) % D
    dist = min(r, D - r)
    crosses = dist < (L / 2.0) * abs(math.sin(th))
    arr = 0.0 if i < 60 else rng.uniform(0, 16)
    NEEDLES.append((arr, cx, cy, th, crosses))
NEEDLES.sort(key=lambda p: p[0])
ARRIVALS = [n[0] for n in NEEDLES]
CROSS_PREFIX = []
c = 0
for _, _, _, _, cr in NEEDLES:
    c += 1 if cr else 0
    CROSS_PREFIX.append(c)


def counts_at(t):
    """(total, crossing) needles arrived by time t, via binary search."""
    k = bisect.bisect_right(ARRIVALS, t)
    cr = CROSS_PREFIX[k - 1] if k else 0
    return k, cr


for t in (0, 4, 8, 12, 16, 20):
    tot, cr = counts_at(t)
    print(f"checkpoint t={t:2d}s total={tot:4d} cross={cr:4d} "
          f"est={2 * tot / cr if cr else 0:.4f}", flush=True)


# ---------- background ----------
def make_bg():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for gx in range(40, W, 90):
        for gy in range(40, H, 90):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(24, 27, 40))
    return img


BGIMG = make_bg()
LINES_Y = [560 + 120 * k for k in range(6)]  # 560..1160


def draw_centered_text(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def render_frame(i):
    t = i / FPS
    img = BGIMG.copy().convert("RGBA")

    # opening push-in 1.00 -> 1.12 over first 2.6s, centred on the field
    zoom = 1.0 + 0.12 * ease_out(t / 2.6) if t < 2.6 else 1.12

    def zx(x):
        return CX + (x - CX) * zoom

    def zy(y):
        return CY + (y - CY) * zoom

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # field card behind the lines
    d.rectangle([zx(30), zy(520), zx(1050), zy(1200)], fill=CARD + (255,))

    # parallel lines
    for ly in LINES_Y:
        d.line([zx(30), zy(ly), zx(1050), zy(ly)], fill=LINE_COL + (255,), width=4)

    # needles arrived by now
    tot, cr = counts_at(t)
    half = (L / 2.0) * zoom
    for k in range(tot):
        _, nx, ny, th, crosses = NEEDLES[k]
        px, py = zx(nx), zy(ny)
        dx = half * math.cos(th)
        dy = half * math.sin(th)
        col = YELLOW if crosses else BLUE
        d.line([px - dx, py - dy, px + dx, py + dy], fill=col + (255,), width=5)

    # field border
    d.rectangle([zx(30), zy(520), zx(1050), zy(1200)], outline=BLUE + (255,), width=4)
    img.alpha_composite(layer)

    d = ImageDraw.Draw(img)

    # hook, fades in within 0.33s (lines + needles already visible at frame 0)
    p = ease_out(t / 0.33)
    if p > 0:
        draw_centered_text(d, 250, "往地上扔针，居然能算出 π",
                           cjk(64), (255, 255, 255, int(255 * p)))
        draw_centered_text(d, 340, "针的长度，正好等于线与线的距离",
                           cjk(32, bold=False), (138, 148, 166, int(255 * p)))

    est = 2 * tot / cr if cr else 0.0

    if 4 <= t < 8:
        draw_centered_text(d, 1300, f"压到线 {cr} 根", cjk(52), YELLOW + (255,))
        draw_centered_text(d, 1400, f"总共扔了 {tot} 根", cjk(52), WHITE + (255,))
    elif 8 <= t < 12:
        draw_centered_text(d, 1290, "2 × 总针数 ÷ 压线针数 ≈ π",
                           cjk(48), YELLOW + (255,))
        draw_centered_text(d, 1400, f"≈ {est:.2f}", cjk(76), GREEN + (255,))
    elif 12 <= t < 16:
        draw_centered_text(d, 1280, "针越多，越接近 3.14",
                           cjk(52), WHITE + (255,))
        draw_centered_text(d, 1390, f"π ≈ {est:.3f}", cjk(76), GREEN + (255,))
        draw_centered_text(d, 1500, "真实值 π ≈ 3.1416",
                           cjk(30, bold=False), GREY + (255,))
    elif t >= 16:
        q = ease_out((t - 16) / 0.6)
        if q > 0:
            draw_centered_text(d, 1300, "布丰投针",
                               cjk(64), (255, 255, 255, int(255 * q)))
            draw_centered_text(d, 1400, "随机，也能算出 π",
                               cjk(56), (255, 217, 61, int(255 * q)))
            draw_centered_text(d, 1500, "1500 根针 → π ≈ 3.17",
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
