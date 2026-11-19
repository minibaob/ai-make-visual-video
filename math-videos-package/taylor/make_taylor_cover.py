#!/usr/bin/env python3
"""Taylor (sin x) cover, 1080x1920, same library spec as the earthbelt covers:
palette BG #0A0A0F / blue #58C4DD / yellow #FFD93D / green #83C167.
Capsule '每天一个可视化概念' on the cover only, never in the video.
Math EXACT: sin x = x - x^3/6 + x^5/120 - x^7/5040.
Mini plot: sin curve (blue) with P7 (white) hugging it and P1 (yellow)
diverging, same geometry as the video's axes."""
import math
from PIL import Image, ImageDraw, ImageFont

BG = (10, 10, 15); BLUE = (88, 196, 221); YELLOW = (255, 217, 61)
GREEN = (131, 193, 103); WHITE = (248, 250, 252); GREY = (138, 148, 166)
CARD = (17, 20, 31); BORDER = (35, 43, 61)

CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CJK_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def cjk(sz, bold=True):
    return ImageFont.truetype(CJK if bold else CJK_R, sz, index=0)


def sans(sz):
    return ImageFont.truetype(SANS_B, sz)


def cw(d, s, font, cx, y, fill):
    w = d.textlength(s, font=font)
    d.text((cx - w / 2, y), s, font=font, fill=fill)


def pill(d, cx, y, s, font, outline, fill, pad_x=28, h=72):
    w = d.textlength(s, font=font) + pad_x * 2
    x0 = cx - w / 2
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=h // 2, outline=outline, width=3)
    d.text((cx - d.textlength(s, font=font) / 2, y + (h - font.size) // 2 - 4),
           s, font=font, fill=fill)


def capsule(d, cx, y, s, font, outline, fill, pad_x=44, h=88):
    w = d.textlength(s, font=font) + pad_x * 2
    x0 = cx - w / 2
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=h // 2, outline=outline, width=4)
    d.text((cx - d.textlength(s, font=font) / 2, y + (h - font.size) // 2 - 4),
           s, font=font, fill=fill)


W, H = 1080, 1920
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im, "RGBA")
for gx in range(60, W, 120):
    for gy in range(60, H, 120):
        d.ellipse([gx, gy, gx + 3, gy + 3], fill=(22, 24, 36))

pill(d, W // 2, 110, "数学可视化 · 泰勒公式", cjk(36), BLUE, BLUE)
cw(d, "sin x 拆开", cjk(76), W // 2, 250, WHITE)
cw(d, "就是多项式", cjk(76), W // 2, 350, YELLOW)

# ---- mini plot: sin (blue) + P7 (white) + P1 (yellow) ----
CX, CY = 540, 900
SX, SY = 122, 170  # px per math unit


def px(x):
    return CX + x * SX


def py(y):
    return CY - y * SY


def p7(x):
    return x - x ** 3 / 6 + x ** 5 / 120 - x ** 7 / 5040


# axes
d.line([px(-3.6), CY, px(3.6), CY], fill=GREY, width=3)
d.line([CX, py(1.6), CX, py(-1.6)], fill=GREY, width=3)
d.text((px(3.6) + 8, CY - 14), "x", font=sans(28), fill=GREY)
d.text((CX + 10, py(1.6) - 34), "y", font=sans(28), fill=GREY)


def curve(fn, x0, x1, color, width):
    pts = []
    x = x0
    while x <= x1:
        y = fn(x)
        if -1.6 <= y <= 1.6:
            pts.append((px(x), py(y)))
        x += 0.05
    d.line(pts, fill=color, width=width, joint="curve")


curve(lambda x: x, -1.6, 1.6, YELLOW, 5)
curve(lambda x: math.sin(x), -3.6, 3.6, BLUE, 7)
curve(p7, -3.6, 3.6, WHITE, 5)

# legend
d.line([150, 1240, 210, 1240], fill=BLUE, width=6)
d.text((225, 1222), "sin x", font=sans(30), fill=WHITE)
d.line([470, 1240, 530, 1240], fill=WHITE, width=6)
d.text((545, 1222), "七次多项式", font=cjk(30), fill=WHITE)
d.line([820, 1240, 880, 1240], fill=YELLOW, width=6)
d.text((895, 1222), "x", font=sans(30), fill=WHITE)

# ---- formula card ----
d.rounded_rectangle([70, 1330, 1010, 1620], radius=28, fill=CARD, outline=BORDER, width=2)
f = "sin x ≈ x − x³/6 + x⁵/120 − x⁷/5040"
fw = d.textlength(f, font=sans(38))
d.text(((W - fw) / 2, 1370), f, font=sans(38), fill=YELLOW)
cw(d, "多项式一项一项加，越贴越远", cjk(32, bold=False), W // 2, 1470, GREY)
cw(d, "sin x = x − x³/3! + x⁵/5! − x⁷/7!", sans(30), W // 2, 1530, GREEN)

capsule(d, W // 2, 1700, "每天一个可视化概念", cjk(44), YELLOW, YELLOW)
im.save("/home/hatch/workspace/imagine_media/taylor-cover-1080x1920.png")
print("cover saved:", im.size)
