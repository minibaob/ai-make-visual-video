#!/usr/bin/env python3
"""Earth belt problem covers, same library spec as the Liu Hui covers:
vertical 1080x1920, horizontal 1440x1080, palette BG #0A0A0F / blue #58C4DD /
yellow #FFD93D / green #83C167. Capsule '每天一个可视化概念' on covers only,
never in the video itself. Math EXACT: C' - C = 2*pi*(r+1) - 2*pi*r = 2*pi
= 6.283185... m -> 6.28 m; radius cancels, independent of Earth's size."""
import math
from PIL import Image, ImageDraw, ImageFont

BG = (10, 10, 15); BLUE = (88, 196, 221); YELLOW = (255, 217, 61)
GREEN = (131, 193, 103); WHITE = (248, 250, 252); GREY = (138, 148, 166)
CARD = (17, 20, 31); BORDER = (35, 43, 61)
OCEAN = (36, 116, 190); LAND = (131, 193, 103)

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


def draw_earth(d, cx, cy, r):
    """Earth disc + rope ring, same geometry as the video."""
    earth = Image.new("RGBA", d._image.size, (0, 0, 0, 0))
    de = ImageDraw.Draw(earth)
    de.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN + (255,))
    blobs = [
        (-110, -160, 120, 70), (60, -80, 150, 80), (-70, 90, 130, 60),
        (110, 140, 90, 50), (20, -180, 70, 40), (-160, 0, 80, 55),
    ]
    for bx, by, bw, bh in blobs:
        de.ellipse([cx + bx - bw / 2, cy + by - bh / 2,
                    cx + bx + bw / 2, cy + by + bh / 2], fill=LAND + (255,))
    for (ax, ay, aw, ah, a0, a1) in [
        (-70, -100, 260, 90, 200, 330), (60, 120, 240, 80, 20, 150),
        (0, -160, 200, 70, 300, 60),
    ]:
        de.arc([cx + ax - aw / 2, cy + ay - ah / 2,
                cx + ax + aw / 2, cy + ay + ah / 2],
               a0, a1, fill=(255, 255, 255, 110), width=6)
    de.ellipse([cx - r, cy - r, cx + r, cy + r],
               outline=(120, 170, 220, 255), width=3)
    mask = Image.new("L", d._image.size, 0)
    dm = ImageDraw.Draw(mask)
    dm.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    clipped = Image.composite(earth, Image.new("RGBA", d._image.size, (0, 0, 0, 0)), mask)
    d._image.paste(clipped, (0, 0), clipped)
    d.ellipse([cx - r - 55, cy - r - 55, cx + r + 55, cy + r + 55],
              outline=YELLOW, width=7)


# ---------- vertical 1080x1920 ----------
W, H = 1080, 1920
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 110, "数学可视化 · 反常识", cjk(36), BLUE, BLUE)
cw(d, "给地球系根腰带", cjk(72), W // 2, 250, WHITE)
cw(d, "只要 6.28 米", cjk(72), W // 2, 350, YELLOW)
draw_earth(d, W // 2, 900, 330)
d.rounded_rectangle([70, 1330, 1010, 1620], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((110, 1355), "绳子离地 1 米", font=cjk(40), fill=WHITE)
d.text((110, 1430), "加长 2π ≈ 6.28 米", font=cjk(40), fill=BLUE)
d.text((110, 1505), "半径 r 直接抵消", font=cjk(40), fill=GREEN)
d.text((110, 1560), "换成篮球也一样", font=cjk(30, bold=False), fill=GREY)
capsule(d, W // 2, 1700, "每天一个可视化概念", cjk(44), YELLOW, YELLOW)
im.save("/home/hatch/workspace/imagine_media/cover_earthbelt_vertical_9x16.png")
print("vertical", im.size)

# ---------- horizontal 1440x1080 ----------
W, H = 1440, 1080
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im, "RGBA")
dots_bg(d, W, H)
pill(d, W // 2, 64, "数学可视化 · 反常识", cjk(34), BLUE, BLUE)
d.text((90, 200), "给地球系根腰带", font=cjk(64), fill=WHITE)
d.text((90, 290), "只要 6.28 米", font=cjk(64), fill=YELLOW)
d.rounded_rectangle([90, 420, 700, 780], radius=28, fill=CARD, outline=BORDER, width=2)
d.text((120, 445), "绳子离地 1 米", font=cjk(38), fill=WHITE)
d.text((120, 515), "加长 2π ≈ 6.28 米", font=cjk(38), fill=BLUE)
d.text((120, 585), "半径 r 直接抵消", font=cjk(38), fill=GREEN)
d.text((120, 650), "换成篮球也一样", font=cjk(30, bold=False), fill=GREY)
draw_earth(d, 1080, 560, 300)
capsule(d, W // 2, 920, "每天一个可视化概念", cjk(42), YELLOW, YELLOW, h=84)
im.save("/home/hatch/workspace/imagine_media/cover_earthbelt_horizontal_4x3.png")
print("horizontal", im.size)
