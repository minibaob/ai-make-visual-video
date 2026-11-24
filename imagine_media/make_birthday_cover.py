#!/usr/bin/env python3
"""Birthday paradox cover, 1080x1920, same library spec as the taylor cover:
palette BG #0A0A0F / blue #58C4DD / yellow #FFD93D / green #83C167.
Capsule '每天一个可视化概念' on the cover only, never in the video.
Math EXACT (verified 2026-11-23): 23人 -> 50.7%, 40人 -> 89%, 70人 -> 99.9%;
23 people make C(23,2) = 253 pairs.
Mini plot: probability curve P(n) with markers, same geometry as the video."""
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

pill(d, W // 2, 110, "数学可视化 · 生日悖论", cjk(36), BLUE, BLUE)
cw(d, "23 个人", cjk(76), W // 2, 250, WHITE)
cw(d, "居然同一天生日", cjk(76), W // 2, 350, YELLOW)

# ---- mini plot: P(n) curve, 0..70 people, 0..100% ----
CX, CY = 540, 900
SX, SY = 11, 4.6  # px per person / per percent


def px(n):
    return 110 + n * SX


def py(p):
    return 1240 - p * SY


# axes
d.line([110, 1240, 900, 1240], fill=GREY, width=3)
d.line([110, 1240, 110, 760], fill=GREY, width=3)
d.text((905, 1226), "人数", font=cjk(28), fill=GREY)
d.text((72, 730), "%", font=sans(28), fill=GREY)
# 50% dashed line
for x0 in range(110, 890, 24):
    d.line([x0, 1010, x0 + 13, 1010], fill=GREY, width=3)
d.text((118, 1022), "50%", font=sans(26), fill=GREY)


def prob(n):
    return 100 * (1 - math.prod((365 - i) / 365 for i in range(n)))


pts = [(px(n), py(prob(n))) for n in range(0, 71)]
d.line(pts, fill=GREEN, width=7, joint="curve")

# markers: 23人 50.7% / 40人 89% / 70人 99.9%
for n, label, color in [(23, "23人 50.7%", YELLOW),
                        (40, "40人 89%", GREEN),
                        (70, "70人 99.9%", GREEN)]:
    x, y = px(n), py(prob(n))
    d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=color)
    tw = d.textlength(label, font=cjk(28))
    lx = min(max(x - tw / 2, 120), 1080 - 120 - tw)
    d.text((lx, y - 52), label, font=cjk(28), fill=color)

# ---- number card ----
d.rounded_rectangle([70, 1330, 1010, 1620], radius=28, fill=CARD, outline=BORDER, width=2)
cw(d, "23 个人，能凑出 253 对", cjk(44), W // 2, 1370, YELLOW)
cw(d, "机会不是 23 次，是 253 次", cjk(32, bold=False), W // 2, 1470, GREY)
cw(d, "23人 50.7% · 40人 89% · 70人 99.9%", cjk(30), W // 2, 1530, GREEN)

capsule(d, W // 2, 1700, "每天一个可视化概念", cjk(44), YELLOW, YELLOW)
im.save("/home/hatch/workspace/imagine_media/birthday-cover-1080x1920.png")
print("cover saved:", im.size)
