#!/usr/bin/env python3
"""Monte Carlo estimation of pi - Douyin video, 20s, 1080x1920, 30fps.
Storyboard:
  0-4s   hook: square + inscribed circle, dots raining in from frame 0,
         "随机撒点，居然能算出 π"
  4-8s   live counters: dots inside circle vs total dots
  8-12s  formula "圆里点数 ÷ 总点数 × 4 ≈ π" + live estimate
  12-16s estimate converges: "点越多，越接近 3.14" + live estimate vs 3.1416
  16-20s closing freeze: "蒙特卡洛方法" + "随机，也能算出 π"
Numbers are REAL: one simulation, fixed seed 20261111, N=1600 dots,
first 60 dots present at t=0, the rest arrive uniformly over (0,16s].
Checkpoints (verified 2026-11-11):
  t=0:  60/53   est 3.5333 (noisy, not shown)
  t=4:  442/353 est 3.1946
  t=8:  840/659 est 3.1381
  t=12: 1233/979 est 3.1760
  t=16: 1600/1260 est 3.1500 (final, frozen for closing)
Opening push-in 1.0 -> 1.22 over the first 2.6s, centred on the square
(CY=820 so the zoomed square top clears the subtitle; spec says 1.9, but
1.9x would push the square off-frame and over the hook/counter text;
Koch precedent used 1.10 for the same reason). No follow CTA, no capsule
inside the video.
"""
import math, random, subprocess, sys, time
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 20.0
NFRAMES = int(DUR * FPS)
OUT = "/home/hatch/workspace/imagine_media/montecarlo-20s-1080x1920.mp4"

BG = (10, 10, 15)
BLUE = (88, 196, 221)
YELLOW = (255, 217, 61)
RED = (255, 107, 107)
GREEN = (131, 193, 103)
WHITE = (248, 250, 252)
GREY = (138, 148, 166)
CARD = (17, 20, 31)
CIRCLE_FILL = (14, 58, 88)

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
SEED = 20261111
N = 1600
CX, CY, HS = 540.0, 820.0, 320.0  # square centre + half side; circle r = HS

rng = random.Random(SEED)
DOTS = []  # (arrival_t, ux, uy, inside) with ux, uy in [-1, 1]
for i in range(N):
    ux = rng.uniform(-1, 1)
    uy = rng.uniform(-1, 1)
    inside = (ux * ux + uy * uy) <= 1.0
    arr = 0.0 if i < 60 else rng.uniform(0, 16)
    DOTS.append((arr, ux, uy, inside))
DOTS.sort(key=lambda p: p[0])
ARRIVALS = [d[0] for d in DOTS]
# cumulative inside counts, prefix sums for O(1) lookup per frame
INSIDE_PREFIX = []
c = 0
for _, _, _, ins in DOTS:
    c += 1 if ins else 0
    INSIDE_PREFIX.append(c)


def counts_at(t):
    """(total, inside) dots arrived by time t, via binary search."""
    import bisect
    n = bisect.bisect_right(ARRIVALS, t)
    ins = INSIDE_PREFIX[n - 1] if n else 0
    return n, ins


for t in (0, 4, 8, 12, 16, 20):
    tot, ins = counts_at(t)
    print(f"checkpoint t={t:2d}s total={tot:4d} inside={ins:4d} "
          f"est={4 * ins / tot if tot else 0:.4f}", flush=True)


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

    # opening push-in 1.00 -> 1.22 over first 2.6s, centred on the square
    zoom = 1.0 + 0.22 * ease_out(t / 2.6) if t < 2.6 else 1.22

    def zx(x):
        return CX + (x - CX) * zoom

    def zy(y):
        return CY + (y - CY) * zoom

    # square + inscribed circle (zoomed)
    x0, y0, x1, y1 = zx(CX - HS), zy(CY - HS), zx(CX + HS), zy(CY + HS)
    r = HS * zoom
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([x0, y0, x1, y1], fill=CARD + (255,))
    d.ellipse([CX - r, CY - r, CX + r, CY + r], fill=CIRCLE_FILL + (255,))

    # dots arrived by now
    tot, ins = counts_at(t)
    for k in range(tot):
        _, ux, uy, inside = DOTS[k]
        px = CX + ux * HS * zoom
        py = CY + uy * HS * zoom
        rad = max(3.5, 5.0 * zoom * 0.75)
        col = BLUE if inside else RED
        d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=col + (255,))
    d.rectangle([x0, y0, x1, y1], outline=BLUE + (255,), width=5)
    d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=YELLOW + (255,), width=5)
    img.alpha_composite(layer)

    d = ImageDraw.Draw(img)

    # hook, fades in within 0.33s (square + dots already visible at frame 0)
    p = ease_out(t / 0.33)
    if p > 0:
        draw_centered_text(d, 250, "随机撒点，居然能算出 π",
                           cjk(64), (255, 255, 255, int(255 * p)))
        draw_centered_text(d, 340, "不用量尺，也不用解方程",
                           cjk(32, bold=False), (138, 148, 166, int(255 * p)))

    est = 4 * ins / tot if tot else 0.0

    if 4 <= t < 8:
        draw_centered_text(d, 1300, f"圆里 {ins} 个", cjk(52), BLUE + (255,))
        draw_centered_text(d, 1400, f"总共 {tot} 个", cjk(52), WHITE + (255,))
    elif 8 <= t < 12:
        draw_centered_text(d, 1290, "圆里点数 ÷ 总点数 × 4 ≈ π",
                           cjk(48), YELLOW + (255,))
        draw_centered_text(d, 1400, f"≈ {est:.2f}", cjk(76), GREEN + (255,))
    elif 12 <= t < 16:
        draw_centered_text(d, 1280, "点越多，越接近 3.14",
                           cjk(52), WHITE + (255,))
        draw_centered_text(d, 1390, f"π ≈ {est:.3f}", cjk(76), GREEN + (255,))
        draw_centered_text(d, 1500, "真实值 π ≈ 3.1416",
                           cjk(30, bold=False), GREY + (255,))
    elif t >= 16:
        q = ease_out((t - 16) / 0.6)
        if q > 0:
            draw_centered_text(d, 1300, "蒙特卡洛方法",
                               cjk(64), (255, 255, 255, int(255 * q)))
            draw_centered_text(d, 1400, "随机，也能算出 π",
                               cjk(56), (255, 217, 61, int(255 * q)))
            draw_centered_text(d, 1500, "1600 个点 → π ≈ 3.15",
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
