#!/usr/bin/env python3
"""Cover for Douyin AI video 02 (robot on Mercedes line), 1080x1920.

Layout follows the account's cover set (gen_cover.py / video 01):
outline pills top/bottom, white headline + yellow numbers, dark card
with three short lines. Middle band is a real still from the official
Google footage (frame-5.png), not a drawn illustration.
Colors sampled from cover_earthbelt_vertical_9x16.png:
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

# dot grid
for x in range(45, W, 90):
    for y in range(45, H, 90):
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=DOT)

# top pill: cyan outline
pill(d, "AI · 机器人", font(BOLD, 46), CYAN, 140)

# headline
draw_centered_segments(d, [
    ("机器人进奔驰工厂", font(BOLD, 92), WHITE),
], 470)
draw_centered_segments(d, [
    ("成功率 ", font(BOLD, 100), WHITE),
    ("96%", font(BOLD, 150), YELLOW),
], 640)

# middle: real still from the official footage (frame-5: wide shot,
# robot + Mercedes-Benz Sindelfingen banner). Center-crop 1080x500.
still = Image.open("/home/hatch/workspace/douyin-ai-video/media/robot02/frame-5.png")
still = still.crop((420, 250, 1500, 750)).resize((900, 417))
im.paste(still, (90, 720))
d.rectangle([90, 720, 990, 1137], outline=CARD_EDGE, width=3)

# bottom dark card, three short lines
d.rounded_rectangle([70, 1210, 1010, 1470], radius=28, fill=CARD,
                    outline=CARD_EDGE, width=2)
card_lines = [
    ("奔驰真产线，匈牙利 + 德国", WHITE),
    ("分拣零件，成功率 96%", CYAN),
    ("100 次里错 4 次，厂商说法", YELLOW),
]
y = 1260
for text, color in card_lines:
    d.text((110, y), text, font=font(BOLD, 48), fill=color, anchor="ls")
    y += 78

# small source note under the card
d.text((W // 2, 1520), "画面：Google DeepMind 官方演示", font=font(REG, 34),
       fill=GREY, anchor="ma")

# bottom pill: yellow outline, cover only
pill(d, "每天一个可视化概念", font(BOLD, 48), YELLOW, 1740)

im.save("/home/hatch/workspace/imagine_media/robot-mercedes-cover-1080x1920.png")
print("cover saved: 1080x1920")
