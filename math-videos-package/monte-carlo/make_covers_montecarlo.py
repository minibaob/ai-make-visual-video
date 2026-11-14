#!/usr/bin/env python3
"""Monte Carlo pi covers, same library spec as the Koch covers:
vertical 1080x1920, horizontal 1440x1080, palette BG #0A0A0F / blue #58C4DD /
yellow #FFD93D / green #83C167. Capsule '每天一个可视化概念' on covers only,
never in the video itself. Numbers (verified, seed 20261111):
1600 dots, 1260 inside the circle, pi estimate 3.15."""
import math, random
from PIL import Image, ImageDraw, ImageFont

BG = (10, 10, 15); BLUE = (88, 196, 221); YELLOW = (255, 217, 61)
GREEN = (131, 193, 103); WHITE = (248, 250, 252); GREY = (138, 148, 166)
CARD = (17, 20, 31); BORDER = (35, 43, 61); FILL = (14, 58, 88)
RED = (255, 107, 107)

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


def draw_montecarlo(d, cx, cy, hs):
    """Square + inscribed circle + scattered dots (same seed as the video)."""
    rng = random.Random(20261111)
    pts = []
    for _ in range(400):
        ux, uy = rng.uniform(-1, 1), rng.uniform(-1, 1)
        pts.append((ux, uy, ux * ux + uy * uy <= 1.0))
    d.rectangle([cx - hs, cy - hs, cx + hs, cy + hs], fill=CARD)
    d.ellipse([cx - hs, cy - hs, cx + hs, cy + hs], fill=FILL)
    for ux, uy, inside in pts:
        px, py = cx + ux * hs, cy + uy * hs
        r = 4
        d.ellipse([px - r, py - r, px + r, py + r], fill=BLUE if inside else RED)
    d.rectangle([cx - hs, cy - hs, cx + hs, cy + hs], outline=BLUE, width=4)
    d.ellipse([cx - hs, cy - hs, cx + hs, cy + hs], outline=YELLOW, width=4)


# ---------- vertical 1080x1920 ----------
W, H = 1080, 1920
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 110, "数学可视化 · 反常识", cjk(36), BLUE, BLUE)
cw(d, "随机撒点", cjk(72), W // 2, 250, WHITE)
cw(d, "居然算出 π", cjk(72), W // 2, 350, YELLOW)
draw_montecarlo(d, W // 2, 900, 330)
d.rounded_rectangle([70, 1330, 1010, 1620], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((110, 1355), "圆里点数 ÷ 总点数 × 4 ≈ π", font=cjk(40), fill=WHITE)
d.text((110, 1430), "1600 个点，1260 个落在圆里", font=cjk(40), fill=BLUE)
d.text((110, 1505), "π ≈ 3.15，离 3.1416 只差 0.01", font=cjk(40), fill=GREEN)
d.text((110, 1560), "这就是蒙特卡洛方法", font=cjk(30, bold=False), fill=GREY)
capsule(d, W // 2, 1700, "每天一个可视化概念", cjk(44), YELLOW, YELLOW)
im.save("/home/hatch/workspace/imagine_media/cover_montecarlo_vertical_9x16.png")
print("vertical", im.size)

# ---------- horizontal 1440x1080 ----------
W, H = 1440, 1080
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 64, "数学可视化 · 反常识", cjk(34), BLUE, BLUE)
d.text((90, 200), "随机撒点", font=cjk(64), fill=WHITE)
d.text((90, 290), "居然算出 π", font=cjk(64), fill=YELLOW)
d.rounded_rectangle([90, 420, 700, 780], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((120, 445), "圆里点数 ÷ 总点数 × 4 ≈ π", font=cjk(38), fill=WHITE)
d.text((120, 515), "1600 个点，1260 个落在圆里", font=cjk(38), fill=BLUE)
d.text((120, 585), "π ≈ 3.15，离 3.1416 只差 0.01", font=cjk(38), fill=GREEN)
d.text((120, 650), "这就是蒙特卡洛方法", font=cjk(30, bold=False), fill=GREY)
draw_montecarlo(d, 1080, 560, 320)
capsule(d, W // 2, 920, "每天一个可视化概念", cjk(42), YELLOW, YELLOW, h=84)
im.save("/home/hatch/workspace/imagine_media/cover_montecarlo_horizontal_4x3.png")
print("horizontal", im.size)
