#!/usr/bin/env python3
"""Cover for Douyin AI video 04: Claude Code 上车，免费档上不了. 1080x1920.

Follows gen_cover03.py: dark bg, cyan outline pill top, white headline +
yellow verdict, price rows card (Pro row yellow highlight), bottom dark
card with three short lines, yellow '每天一个可视化概念' pill at bottom.
Background: the real claude.com pricing screenshot, heavily darkened.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HOME = os.path.expanduser("~")
SHOTS = os.path.join(HOME, "workspace/douyin-ai-video/media/claude04/shots")

W, H = 1080, 1920
BG = "#0A0A0F"
CYAN = "#58C4DD"
YELLOW = "#FFD93D"
CARD = "#11141F"
CARD_EDGE = "#232839"
WHITE = "#F8FAFC"
GREY = "#8A94A6"
DOT = "#181B28"

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def draw_centered_segments(draw, segments, y_baseline, x_center=W // 2):
    total = sum(text_w(draw, s, f) for s, f, _ in segments)
    x = x_center - total / 2
    for s, f, c in segments:
        draw.text((x, y_baseline), s, font=f, fill=c, anchor="ls")
        x += text_w(draw, s, f)
    return total


def pill(draw, text, f, fg, y, pad_x=44, height=88, width=4):
    w = text_w(draw, text, f) + 2 * pad_x
    x0 = (W - w) / 2
    draw.rounded_rectangle([x0, y, x0 + w, y + height], radius=height // 2,
                           outline=fg, width=width)
    draw.text((W / 2, y + height / 2), text, font=f, fill=fg, anchor="mm")
    return y + height


# background: real claude.com pricing screenshot, scaled to cover + darkened
still = Image.open(os.path.join(SHOTS, "claude-free.png")).convert("RGB")
still = still.resize((1080, int(1080 * still.height / still.width)))
still = still.crop((0, 0, 1080, 1920)) if still.height >= 1920 else still.resize((1080, 1920))
still = ImageEnhance.Brightness(still).enhance(0.22)
still = ImageEnhance.Color(still).enhance(0.5)
im = still.convert("RGB")
veil = Image.new("RGB", (W, H), (10, 10, 15))
im = Image.blend(im, veil, 0.55)
d = ImageDraw.Draw(im, "RGBA")

for x in range(45, W, 90):
    for y in range(45, H, 90):
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=DOT)

pill(d, "AI · 上车合集", font(BOLD, 46), CYAN, 140)

draw_centered_segments(d, [
    ("Claude Code 上车", font(BOLD, 92), WHITE),
], 470)
draw_centered_segments(d, [
    ("免费档", font(BOLD, 100), WHITE),
    ("上不了", font(BOLD, 110), YELLOW),
], 640)

d.rounded_rectangle([70, 720, 1010, 1137], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
rows = [
    ("免费", "$0", WHITE, False),
    ("Pro", "$20/月", YELLOW, True),
    ("Max", "$100/月", WHITE, False),
]
y = 790
for label, price, color, hl in rows:
    if hl:
        d.rounded_rectangle([90, y - 62, 990, y + 8], radius=18,
                            fill=(255, 217, 61, 26), outline=YELLOW, width=2)
    d.text((110, y), label, font=font(BOLD, 56), fill=color, anchor="ls")
    d.text((970, y), price, font=font(BOLD, 56), fill=color, anchor="rs")
    y += 108

d.rounded_rectangle([70, 1210, 1010, 1470], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
card_lines = [
    ("免费档不含 Claude Code", WHITE),
    ("Pro 二十美元普通人最值", CYAN),
    ("Antigravity 免费档只剩 2 天", YELLOW),
]
y = 1260
for text, color in card_lines:
    d.text((110, y), text, font=font(BOLD, 48), fill=color, anchor="ls")
    y += 78

d.text((W // 2, 1520), "数据：Claude / Cursor / Antigravity 官网，2026 年 11 月",
       font=font(REG, 34), fill=GREY, anchor="ma")

pill(d, "每天一个可视化概念", font(BOLD, 48), YELLOW, 1740)

out = os.path.join(HOME, "workspace/imagine_media/claude-shangche-20s-cover-1080x1920.png")
im.save(out)
print("cover saved:", out)
