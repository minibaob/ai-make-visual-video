#!/usr/bin/env python3
"""Sierpinski triangle covers, same library spec as the Liu Hui covers:
vertical 1080x1920, horizontal 1440x1080, palette BG #0A0A0F / blue #58C4DD /
yellow #FFD93D / green #83C167. Capsule '每天一个可视化概念' on covers only,
never in the video itself. Numbers EXACT: remaining area (3/4)^n:
iter 1 -> 75.0%, iter 5 -> 23.7% (56.25 -> 56.3% half-up). Collection
episode 12 (assuming Sierpinski publishes before the Earth-belt video)."""
import math
from PIL import Image, ImageDraw, ImageFont

BG = (10, 10, 15); BLUE = (88, 196, 221); YELLOW = (255, 217, 61)
GREEN = (131, 193, 103); WHITE = (248, 250, 252); GREY = (138, 148, 166)
CARD = (17, 20, 31); BORDER = (35, 43, 61)

CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CJK_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def cjk(sz, bold=True):
    return ImageFont.truetype(CJK if bold else CJK_R, sz, index=0)


def mono(sz):
    return ImageFont.truetype(MONO, sz)


def cw(d, s, font, cx, y, fill):
    w = d.textlength(s, font=font)
    d.text((cx - w / 2, y), s, font=font, fill=fill)


def pill(d, cx, y, s, font, outline, fill, pad_x=28, h=72):
    w = d.textlength(s, font=font) + pad_x * 2
    x0 = cx - w / 2
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=h // 2, outline=outline, width=3)
    d.text((cx - d.textlength(s, font=font) / 2, y + (h - font.size) // 2 - 4), s, font=font, fill=fill)


def capsule(d, cx, y, s, font, outline, fill, pad_x=44, h=88):
    w = d.textlength(s, font=font) + pad_x * 2
    x0 = cx - w / 2
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=h // 2, outline=outline, width=4)
    d.text((cx - d.textlength(s, font=font) / 2, y + (h - font.size) // 2 - 4), s, font=font, fill=fill)


def dots_bg(d, W, H):
    for gx in range(60, W, 120):
        for gy in range(60, H, 120):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(22, 24, 36))


def subdivide(tri, n):
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


def draw_fractal(d, cx, cy, r, n=5):
    """Sierpinski triangle, apex top, same geometry as the video."""
    h = r * math.sqrt(3) / 2
    apex = (cx, cy - h)
    bl = (cx - r, cy + h)
    br = (cx + r, cy + h)
    for tri in subdivide((apex, bl, br), n):
        d.polygon(tri, fill=BLUE)


# ---------- vertical 1080x1920 ----------
W, H = 1080, 1920
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 110, "数学可视化 · 分形", cjk(36), BLUE, BLUE)
cw(d, "一个三角形", cjk(72), W // 2, 250, WHITE)
cw(d, "无限挖下去", cjk(72), W // 2, 350, YELLOW)
draw_fractal(d, W // 2, 900, 330)
d.rounded_rectangle([70, 1330, 1010, 1620], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((110, 1355), "第 1 次 → 剩下 75.0%", font=cjk(40), fill=WHITE)
d.text((110, 1430), "第 5 次 → 剩下 23.7%", font=cjk(40), fill=BLUE)
d.text((110, 1505), "剩下 (3/4)^n", font=cjk(40), fill=GREEN)
d.text((110, 1560), "谢尔宾斯基三角形", font=cjk(30, bold=False), fill=GREY)
capsule(d, W // 2, 1700, "每天一个可视化概念", cjk(44), YELLOW, YELLOW)
im.save("/home/hatch/workspace/imagine_media/cover_sierpinski_vertical_9x16.png")
print("vertical", im.size)

# ---------- horizontal 1440x1080 ----------
W, H = 1440, 1080
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 64, "数学可视化 · 分形", cjk(34), BLUE, BLUE)
d.text((90, 200), "一个三角形", font=cjk(64), fill=WHITE)
d.text((90, 290), "无限挖下去", font=cjk(64), fill=YELLOW)
d.rounded_rectangle([90, 420, 700, 780], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((120, 445), "第 1 次 → 剩下 75.0%", font=cjk(38), fill=WHITE)
d.text((120, 515), "第 5 次 → 剩下 23.7%", font=cjk(38), fill=BLUE)
d.text((120, 585), "剩下 (3/4)^n", font=cjk(38), fill=GREEN)
d.text((120, 650), "谢尔宾斯基三角形", font=cjk(30, bold=False), fill=GREY)
draw_fractal(d, 1080, 560, 300)
capsule(d, W // 2, 920, "每天一个可视化概念", cjk(42), YELLOW, YELLOW, h=84)
im.save("/home/hatch/workspace/imagine_media/cover_sierpinski_horizontal_4x3.png")
print("horizontal", im.size)
