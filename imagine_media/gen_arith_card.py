#!/usr/bin/env python3
"""Arithmetic follow-up card for Douyin (same winning format as the Nov 14 post).
Problem: m^2 = 49, m - m*n = 56, find n^2.
m = 7  -> 7 - 7n = 56 -> n = -7 -> n^2 = 49
m = -7 -> -7 + 7n = 56 -> n = 9  -> n^2 = 81
Two valid answers: 49 or 81. Verified by hand.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
BG = (0xFB, 0xF8, 0xF1)
INK = (0x1F, 0x1B, 0x16)
TERRA = (0xC2, 0x70, 0x3D)
GRAY = (0x8A, 0x82, 0x76)
CARD = (0xFF, 0xFF, 0xFF)
BORDER = (0xE8, 0xE0, 0xD0)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text_center(y, s, font, fill=INK):
    box = d.textbbox((0, 0), s, font=font)
    w = box[2] - box[0]
    d.text(((W - w) / 2 - box[0], y), s, font=font, fill=fill)
    return box[3] - box[1]

# top label
f_label = ImageFont.truetype(FONT, 44)
text_center(96, "算  术  题", f_label, fill=TERRA)
d.line([(W // 2 - 60, 180), (W // 2 + 60, 180)], fill=TERRA, width=4)

# white card holding the problem
card_top, card_bottom = 250, 1010
d.rounded_rectangle([72, card_top, W - 72, card_bottom], radius=28, fill=CARD, outline=BORDER, width=3)

f_math = ImageFont.truetype(FONT, 118)
f_ask = ImageFont.truetype(FONT, 104)
y = 330
h = text_center(y, "m\u00b2 = 49", f_math)
y += h + 48
h = text_center(y, "m \u2212 m \u00d7 n = 56", f_math)
y += h + 64
d.line([(W // 2 - 180, y + 10), (W // 2 + 180, y + 10)], fill=BORDER, width=3)
y += 64
text_center(y, "\u6c42 n\u00b2 = \uff1f", f_ask, fill=TERRA)

# bottom hint
f_hint = ImageFont.truetype(FONT_R, 46)
text_center(1100, "\u7b54\u6848\u5199\u5728\u8bc4\u8bba\u533a", f_hint, fill=GRAY)

img.save("/home/hatch/workspace/imagine_media/arith-followup-01.png")
print("saved")
