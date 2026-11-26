#!/usr/bin/env python3
"""Landscape cover for Douyin AI video 03B (Codex long animated version).
1920x1080. Same visual language as the 20s vertical cover (gen_cover03.py):
dark bg from the real 5UlRL collage still, cyan outline pill, white headline
+ yellow numbers, price rows card (Plus highlighted), bottom dark card,
yellow "每天一个可视化概念" pill. Two-column landscape layout.
"""
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HOME = os.path.expanduser("~")
MEDIA = os.path.join(HOME, "workspace/douyin-ai-video/media/codex03")

W, H = 1920, 1080
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


def pill_left(draw, text, f, fg, x, y, pad_x=40, height=84, width=4):
    w = text_w(draw, text, f) + 2 * pad_x
    draw.rounded_rectangle([x, y, x + w, y + height], radius=height // 2,
                           outline=fg, width=width)
    draw.text((x + w / 2, y + height / 2), text, font=f, fill=fg, anchor="mm")
    return w


def pill_center(draw, text, f, fg, y, pad_x=44, height=84, width=4):
    w = text_w(draw, text, f) + 2 * pad_x
    x0 = (W - w) / 2
    draw.rounded_rectangle([x0, y, x0 + w, y + height], radius=height // 2,
                           outline=fg, width=width)
    draw.text((W / 2, y + height / 2), text, font=f, fill=fg, anchor="mm")


# background: real still, 5UlRL 38s collage wall (640x360 = 16:9, exact fit)
still_path = os.path.join(MEDIA, "cover-still.png")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "38",
                "-i", os.path.join(MEDIA, "5UlRL_ImvQ0.mp4"),
                "-frames:v", "1", still_path], check=True)
still = Image.open(still_path).convert("RGB")
still = still.resize((W, H))
still = ImageEnhance.Brightness(still).enhance(0.28)
still = ImageEnhance.Color(still).enhance(0.6)
im = still.convert("RGB")
veil = Image.new("RGB", (W, H), (10, 10, 15))
im = Image.blend(im, veil, 0.45)
d = ImageDraw.Draw(im, "RGBA")

# dot grid
for x in range(45, W, 90):
    for y in range(45, H, 90):
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=DOT)

LX = 110  # left column x

# top-left pill
pill_left(d, "AI · 上车合集", font(BOLD, 44), CYAN, LX, 92)

# headline (left column)
d.text((LX, 300), "Codex 上车", font=font(BOLD, 110), fill=WHITE, anchor="ls")
d.text((LX, 470), "0", font=font(BOLD, 190), fill=YELLOW, anchor="ls")
d.text((LX + text_w(d, "0", font(BOLD, 190)) + 12, 470), "元就能用",
       font=font(BOLD, 110), fill=WHITE, anchor="ls")

# bottom-left dark card, three short lines
d.rounded_rectangle([LX, 560, 1010, 830], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
card_lines = [
    ("免费档桌面 App 就能用", WHITE),
    ("Plus 二十美元开全渠道", CYAN),
    ("普通人 Plus 最值", YELLOW),
]
y = 622
for text, color in card_lines:
    d.text((LX + 40, y), text, font=font(BOLD, 50), fill=color, anchor="ls")
    y += 76

# right column: price rows card
RX0, RX1 = 1090, 1810
d.rounded_rectangle([RX0, 200, RX1, 830], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
d.text((RX0 + 44, 300), "五个渠道，价格一次看清",
       font=font(BOLD, 48), fill=WHITE, anchor="ls")
rows = [
    ("免费", "$0", WHITE, False),
    ("Plus", "$20 / 月", YELLOW, True),
    ("Pro", "$100 / 月起", WHITE, False),
    ("API", "按量付费", WHITE, False),
]
y = 420
for label, price, color, hl in rows:
    if hl:
        d.rounded_rectangle([RX0 + 20, y - 66, RX1 - 20, y + 6], radius=18,
                            fill=(255, 217, 61, 26), outline=YELLOW, width=2)
    d.text((RX0 + 44, y), label, font=font(BOLD, 52), fill=color, anchor="ls")
    d.text((RX1 - 44, y), price, font=font(BOLD, 52), fill=color, anchor="rs")
    y += 100

# source note + bottom pill
d.text((W // 2, 902), "数据：OpenAI 官网定价页，2026 年 11 月",
       font=font(REG, 32), fill=GREY, anchor="ma")
pill_center(d, "每天一个可视化概念", font(BOLD, 44), YELLOW, 948)

out = os.path.join(HOME, "workspace/imagine_media/codex-shangche-long-cover-1920x1080.png")
im.save(out)
print("cover saved:", out)
