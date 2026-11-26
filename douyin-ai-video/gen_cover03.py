#!/usr/bin/env python3
"""Cover for Douyin AI video 03: Codex 上车，0元就能用. 1080x1920.

Layout follows gen_cover02.py (account cover set):
cyan outline pill top, white headline + yellow numbers, dark card with
three short lines, yellow "每天一个可视化概念" pill at the bottom.
Middle: three price rows, Plus row highlighted yellow.
Background: real still from the official 5UlRL footage (38s collage wall),
darkened heavily, dot grid on top.
Colors: bg #0A0A0F, cyan #58C4DD, yellow #FFD93D, card #11141F,
white #F8FAFC, grey #8A94A6, dot #181B28.
"""
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HOME = os.path.expanduser("~")
MEDIA = os.path.join(HOME, "workspace/douyin-ai-video/media/codex03")

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


# background: real still, 5UlRL 38s collage wall, scaled to cover + darkened
still_path = os.path.join(MEDIA, "cover-still.png")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "38",
                "-i", os.path.join(MEDIA, "5UlRL_ImvQ0.mp4"),
                "-frames:v", "1", still_path], check=True)
still = Image.open(still_path).convert("RGB")
still = still.resize((1080, 1920))  # 640x360 -> stretch to cover, then darken hard
still = ImageEnhance.Brightness(still).enhance(0.28)
still = ImageEnhance.Color(still).enhance(0.6)
im = still.convert("RGB")
# dark veil for text legibility
veil = Image.new("RGB", (W, H), (10, 10, 15))
im = Image.blend(im, veil, 0.45)
d = ImageDraw.Draw(im, "RGBA")

# dot grid
for x in range(45, W, 90):
    for y in range(45, H, 90):
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=DOT)

# top pill: cyan outline
pill(d, "AI · 上车合集", font(BOLD, 46), CYAN, 140)

# headline
draw_centered_segments(d, [
    ("Codex 上车", font(BOLD, 92), WHITE),
], 470)
draw_centered_segments(d, [
    ("0", font(BOLD, 150), YELLOW),
    (" 元就能用", font(BOLD, 100), WHITE),
], 640)

# middle: price rows card (Plus row yellow highlight)
d.rounded_rectangle([70, 720, 1010, 1137], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
rows = [
    ("免费", "$0", WHITE, False),
    ("Plus", "$20/月", YELLOW, True),
    ("Pro", "$100/月", WHITE, False),
]
y = 790
for label, price, color, hl in rows:
    if hl:
        d.rounded_rectangle([90, y - 62, 990, y + 8], radius=18,
                            fill=(255, 217, 61, 26), outline=YELLOW, width=2)
    d.text((110, y), label, font=font(BOLD, 56), fill=color, anchor="ls")
    d.text((970, y), price, font=font(BOLD, 56), fill=color, anchor="rs")
    y += 108

# bottom dark card, three short lines
d.rounded_rectangle([70, 1210, 1010, 1470], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
card_lines = [
    ("免费档桌面 App 就能用", WHITE),
    ("Plus 二十美元开全渠道", CYAN),
    ("普通人 Plus 最值", YELLOW),
]
y = 1260
for text, color in card_lines:
    d.text((110, y), text, font=font(BOLD, 48), fill=color, anchor="ls")
    y += 78

# small source note under the card
d.text((W // 2, 1520), "数据：OpenAI 官网定价页，2026 年 11 月",
       font=font(REG, 34), fill=GREY, anchor="ma")

# bottom pill: yellow outline, cover only
pill(d, "每天一个可视化概念", font(BOLD, 48), YELLOW, 1740)

out = os.path.join(HOME, "workspace/imagine_media/codex-shangche-cover-1080x1920.png")
im.save(out)
print("cover saved:", out)
