#!/usr/bin/env python3
"""Arithmetic follow-up card v3 (candidate, held for 24h data decision) for Douyin — exact same style as the Nov 14 post.
Recreation of the posted 图文 (video ID 7707846649754332058):
- 1:1 square, 1080x1080
- cream rice-paper background #F6F2E9, subtle grain, no border/shadow/logo
- three lines of black math serif (Liberation Serif = Times-like):
  variables italic bold, digits/operators upright bold, very large
- line 2 widest (~78% of width), all lines centered, big top/bottom margins
- top-right black rounded sticker, white outline, white bold "99% Fail"
- NO header, NO card, NO footer text inside the image
Problem: a^2 = 36, a + a*b = 42, find b^2. Answers 36 or 64 (verified: a=6,b=6; a=-6,b=-8).
"""
from PIL import Image, ImageDraw, ImageFont
import random

W = H = 1080
BG = (0xF6, 0xF2, 0xE9)
INK = (0x00, 0x00, 0x00)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle paper grain
random.seed(20261117)
grain = Image.effect_noise((W, H), 14).convert("L")
img = Image.composite(
    Image.new("RGB", (W, H), (0xEF, 0xEB, 0xE0)),
    img, grain.point(lambda v: 255 - min(255, max(0, (v - 128) // 6))),
)
d = ImageDraw.Draw(img)

# --- layout: one font size for all three lines, scaled so line 2 ~ 78% width
def make_fonts(size):
    return {
        "b": ImageFont.truetype(SERIF_B, size),
        "bi": ImageFont.truetype(SERIF_BI, size),
        "sup": ImageFont.truetype(SERIF_B, int(size * 0.58)),
    }

# segments: (text, font_key, dy_offset)
LINES = [
    [("a", "bi", 0), ("2", "sup", -58), (" = 36", "b", 0)],
    [("a", "bi", 0), (" + ", "b", 0), ("a", "bi", 0),
     (" \u00d7 ", "b", 0), ("b", "bi", 0), (" = 42", "b", 0)],
    [("b", "bi", 0), ("2", "sup", -58), (" = ?", "b", 0)],
]

def line_width(fonts, segs):
    total = 0
    for text, key, _ in segs:
        total += d.textlength(text, font=fonts[key])
    return total

size = 170
fonts = make_fonts(size)
w2 = line_width(fonts, LINES[1])
scale = 840 / w2
size = int(size * scale)
fonts = make_fonts(size)
sup_dy = -int(size * 0.34)
LINES = [
    [("a", "bi", 0), ("2", "sup", sup_dy), (" = 36", "b", 0)],
    [("a", "bi", 0), (" + ", "b", 0), ("a", "bi", 0),
     (" \u00d7 ", "b", 0), ("b", "bi", 0), (" = 42", "b", 0)],
    [("b", "bi", 0), ("2", "sup", sup_dy), (" = ?", "b", 0)],
]

def draw_line(y_top, segs):
    """Draw one line centered horizontally; y_top is the top of the main glyphs."""
    total = line_width(fonts, segs)
    x = (W - total) / 2
    for text, key, dy in segs:
        f = fonts[key]
        # anchor top via textbbox
        d.text((x, y_top + dy), text, font=f, fill=INK)
        x += d.textlength(text, font=f)

# three lines, big margins, block centered in the middle
pitch = 215
y0 = 270
for i, segs in enumerate(LINES):
    draw_line(y0 + i * pitch, segs)

# --- top-right "99% Fail" sticker: black rounded rect, white outline
sw, sh = 324, 104
sx, sy = W - 24 - sw, 24
d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=18,
                    fill=(0, 0, 0), outline=(255, 255, 255), width=3)
f_stick = ImageFont.truetype(SERIF_B, 58)
label = "99% Fail"
tw = d.textlength(label, font=f_stick)
bbox = d.textbbox((0, 0), label, font=f_stick)
th = bbox[3] - bbox[1]
d.text((sx + (sw - tw) / 2, sy + (sh - th) / 2 - bbox[1]), label,
       font=f_stick, fill=(255, 255, 255))

img.save("/home/hatch/workspace/imagine_media/arith-followup-03.png")
print("saved", size, "line2 width:", round(line_width(fonts, LINES[1])))
