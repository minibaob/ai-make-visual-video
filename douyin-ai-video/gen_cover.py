#!/usr/bin/env python3
"""Cover for Douyin AI video 01 (price war), 1080x1920.

Layout follows the account's math-video cover
(~/workspace/imagine_media/cover_earthbelt_vertical_9x16.png):
outline pills top/bottom, white headline + yellow numbers, dark card
with three short lines. Colors sampled from that file:
bg #0A0A0F, cyan #58C4DD, yellow #FFD93D, card #11141F,
white #F8FAFC, grey #8A94A6, dot #181B28.
"""
from PIL import Image, ImageDraw, ImageFont

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
    """segments: list of (text, font, color). Draw on one baseline, centered."""
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


im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)

# dot grid, same as the video background
for x in range(45, W, 90):
    for y in range(45, H, 90):
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=DOT)

# top pill: cyan outline
pill(d, "AI · 算账", font(BOLD, 46), CYAN, 140)

# headline, numbers yellow and larger
draw_centered_segments(d, [
    ("第一名 ", font(BOLD, 100), WHITE),
    ("65", font(BOLD, 140), YELLOW),
    (" 分", font(BOLD, 100), WHITE),
], 480)
draw_centered_segments(d, [
    ("做套题花 ", font(BOLD, 100), WHITE),
    ("26", font(BOLD, 140), YELLOW),
    ("块", font(BOLD, 100), YELLOW),
    ("5", font(BOLD, 140), YELLOW),
], 640)


def bar_row(y_name, y_bar, name, value, color, length, max_len=640):
    d.text((90, y_name), name, font=font(REG, 36), fill=GREY, anchor="ls")
    d.rectangle([90, y_bar, 90 + length, y_bar + 54], fill=color)
    d.text((90 + length + 16, y_bar + 27), value, font=font(BOLD, 48),
           fill=color, anchor="lm")


# mini chart 1: scores
d.text((90, 730), "智力指数", font=font(BOLD, 40), fill=GREY, anchor="ls")
bar_row(790, 815, "Claude Fable 5.2", "65", CYAN, 640)
bar_row(920, 945, "GPT-6.2 Astra", "62", GREY, 610)

# mini chart 2: cost per set
d.text((90, 1080), "一套题花费", font=font(BOLD, 40), fill=GREY, anchor="ls")
bar_row(1140, 1165, "Claude Fable 5.2", "$26.54", YELLOW, 640)
bar_row(1270, 1295, "GPT-6.2 Astra", "$4.00", CYAN, 96)

# bottom dark card, three short lines
d.rounded_rectangle([70, 1420, 1010, 1680], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
card_lines = [
    ("单价一样，都是 8 美元", WHITE),
    ("一个花 26 块 5，一个花 4 块", CYAN),
    ("3 分，多花 22 块 5 毛 4", YELLOW),
]
y = 1470
for text, color in card_lines:
    d.text((110, y), text, font=font(BOLD, 48), fill=color, anchor="ls")
    y += 78

# bottom pill: yellow outline, cover only
pill(d, "每天一个可视化概念", font(BOLD, 48), YELLOW, 1740)

im.save("/home/hatch/workspace/imagine_media/ai-price-war-cover-1080x1920.png")
print("cover saved: 1080x1920")
