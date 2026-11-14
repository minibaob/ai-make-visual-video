#!/usr/bin/env python3
"""Liu Hui 割圆术 covers, same library spec as the Buffon covers:
vertical 1080x1920, horizontal 1440x1080, palette BG #0A0A0F / blue #58C4DD /
yellow #FFD93D / green #83C167. Capsule '每天一个可视化概念' on covers only,
never in the video itself. Numbers EXACT: inscribed n-gon pi ~ n*sin(pi/n):
6 -> 3.0000, 12 -> 3.1058, 24 -> 3.1326, 48 -> 3.1394, 96 -> 3.1410."""
import math
from PIL import Image, ImageDraw, ImageFont

BG = (10, 10, 15); BLUE = (88, 196, 221); YELLOW = (255, 217, 61)
GREEN = (131, 193, 103); WHITE = (248, 250, 252); GREY = (138, 148, 166)
CARD = (17, 20, 31); BORDER = (35, 43, 61)
CIRCLE_COL = (96, 118, 150)

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


def draw_polys(d, cx, cy, r):
    """Faint circle + hexagon + 96-gon, same geometry as the video."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CIRCLE_COL, width=3)
    for n, col, wd in ((6, BLUE, 4), (96, GREEN, 3)):
        pts = [(cx + r * math.cos(2 * math.pi * k / n - math.pi / 2),
                cy + r * math.sin(2 * math.pi * k / n - math.pi / 2))
               for k in range(n + 1)]
        d.line(pts, fill=col, width=wd, joint="curve")
    for k in range(6):
        px = cx + r * math.cos(2 * math.pi * k / 6 - math.pi / 2)
        py = cy + r * math.sin(2 * math.pi * k / 6 - math.pi / 2)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=YELLOW)


# ---------- vertical 1080x1920 ----------
W, H = 1080, 1920
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 110, "数学可视化 · 反常识", cjk(36), BLUE, BLUE)
cw(d, "把圆切成多边形", cjk(72), W // 2, 250, WHITE)
cw(d, "π 就出来了", cjk(72), W // 2, 350, YELLOW)
draw_polys(d, W // 2, 900, 330)
d.rounded_rectangle([70, 1330, 1010, 1620], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((110, 1355), "6 边形 → π ≈ 3.0000", font=cjk(40), fill=WHITE)
d.text((110, 1430), "96 边形 → π ≈ 3.1410", font=cjk(40), fill=BLUE)
d.text((110, 1505), "边越多，越接近圆", font=cjk(40), fill=GREEN)
d.text((110, 1560), "这就是刘徽割圆术", font=cjk(30, bold=False), fill=GREY)
capsule(d, W // 2, 1700, "每天一个可视化概念", cjk(44), YELLOW, YELLOW)
im.save("/home/hatch/workspace/imagine_media/cover_liuhui_vertical_9x16.png")
print("vertical", im.size)

# ---------- horizontal 1440x1080 ----------
W, H = 1440, 1080
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 64, "数学可视化 · 反常识", cjk(34), BLUE, BLUE)
d.text((90, 200), "把圆切成多边形", font=cjk(64), fill=WHITE)
d.text((90, 290), "π 就出来了", font=cjk(64), fill=YELLOW)
d.rounded_rectangle([90, 420, 700, 780], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((120, 445), "6 边形 → π ≈ 3.0000", font=cjk(38), fill=WHITE)
d.text((120, 515), "96 边形 → π ≈ 3.1410", font=cjk(38), fill=BLUE)
d.text((120, 585), "边越多，越接近圆", font=cjk(38), fill=GREEN)
d.text((120, 650), "这就是刘徽割圆术", font=cjk(30, bold=False), fill=GREY)
draw_polys(d, 1080, 560, 300)
capsule(d, W // 2, 920, "每天一个可视化概念", cjk(42), YELLOW, YELLOW, h=84)
im.save("/home/hatch/workspace/imagine_media/cover_liuhui_horizontal_4x3.png")
print("horizontal", im.size)
