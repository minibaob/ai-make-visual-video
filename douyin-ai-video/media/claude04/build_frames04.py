#!/usr/bin/env python3
"""Build Douyin AI video 04: Claude Code 上车全渠道合集 (20s, 1080x1920).

Format: cream #F6EEDC background, white cards, red-seal verdicts (-5 deg),
burned-in subtitles (white, black outline, 48px). Evidence windows are
same-day real screenshots of the official pricing pages (see shots/):
claude.com/pricing (Free $0), cursor.com/pricing (Premium $30),
antigravity.google/pricing (free-tier Claude 4.6 + footnote 4, Nov 30 2026).

Segments (20.0s total): S1 0-3, S2 3-6, S3 6-9, S4 9-13, S5 13-16, S6 16-20.
TTS: media/claude04/tts/seg1-6.mp3 (zh-CN-XiaoxiaoNeural, +10%).
BGM: bgm-mixkit.mp3 (Mixkit "Smile"), volume 0.5, baked in; BGM looped at
input level with -stream_loop (never inside the filter graph).
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "workspace/douyin-ai-video/media/claude04")
SHOTS = os.path.join(BASE, "shots")
TTS = os.path.join(BASE, "tts")
BGM = os.path.join(HOME, "workspace/imagine_media/bgm-mixkit.mp3")
OUT_DIR = os.path.join(HOME, "workspace/imagine_media")
FRAMES = os.path.join(BASE, "frames")
SEG_DIR = os.path.join(BASE, "segments")
os.makedirs(FRAMES, exist_ok=True)
os.makedirs(SEG_DIR, exist_ok=True)

W, H = 1080, 1920
CREAM = (246, 238, 220)
WHITE = (255, 255, 255)
INK = (31, 27, 22)
GREY = (138, 127, 106)
RED = (229, 72, 77)
YELLOW = (255, 217, 61)
CARD_EDGE = (227, 217, 194)

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def centered_segments(d, segments, y_baseline, x_center=W // 2):
    """segments: [(text, font, color, highlight_bool)]"""
    total = sum(text_w(d, s, f) for s, f, _, _ in segments)
    x = x_center - total / 2
    for s, f, c, hl in segments:
        if hl:
            w = text_w(d, s, f)
            d.rounded_rectangle([x - 8, y_baseline - f.size - 6,
                                 x + w + 8, y_baseline + 14],
                                radius=12, fill=YELLOW)
        d.text((x, y_baseline), s, font=f, fill=c, anchor="ls")
        x += text_w(d, s, f)


def stamp(text, size):
    """Red stamp-style verdict, transparent bg, red outline, rotated -5 deg."""
    f = font(BOLD, size)
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tw = int(td.textlength(text, font=f))
    w, h = tw + 72, size + 72
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w - 4, h - 4], radius=20,
                        outline=RED + (255,), width=6)
    d.text((w // 2, h // 2), text, font=f, fill=RED + (255,), anchor="mm")
    return im.rotate(-5, expand=True, resample=Image.BICUBIC)


def paste_centered(base, im, cx, cy):
    base.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)


def fit_image(path, max_w, max_h):
    im = Image.open(path).convert("RGB")
    s = min(max_w / im.width, max_h / im.height)
    return im.resize((int(im.width * s), int(im.height * s)),
                     Image.LANCZOS)


def subtitle(d, text, y=1560):
    f = font(BOLD, 48)
    d.text((W // 2, y), text, font=f, fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(0, 0, 0), anchor="ma")


def source_line(d, text, y=1700):
    d.text((W // 2, y), text, font=font(REG, 30), fill=GREY, anchor="ma")


def new_frame():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im, "RGBA")
    # white card
    d.rounded_rectangle([70, 400, 1010, 1460], radius=32, fill=WHITE,
                        outline=CARD_EDGE, width=2)
    return im, d


def card_image(im, d, path, max_w=860, max_h=960, cy=930):
    pic = fit_image(path, max_w, max_h)
    x0 = (W - pic.width) // 2
    y0 = int(cy - pic.height / 2)
    d.rectangle([x0 - 3, y0 - 3, x0 + pic.width + 3, y0 + pic.height + 3],
                outline=(221, 210, 188), width=2)
    im.paste(pic, (x0, y0))
    return y0 + pic.height


# ---------------- S1: 免费档，上不了 ----------------
im, d = new_frame()
paste_centered(im, stamp("上不了", 150), W // 2, 235)
card_image(im, d, os.path.join(SHOTS, "ev-s1-free.png"), cy=930)
subtitle(d, "免费档，上不了")
source_line(d, "来源：claude.com/pricing · 2026-11-28")
im.save(os.path.join(FRAMES, "frame1.png"))

# ---------------- S2: Pro 二十美元，最值 ----------------
im, d = new_frame()
centered_segments(d, [("Pro ", font(BOLD, 120), INK, False),
                      ("$20", font(BOLD, 120), INK, True)], 300)
# price card inside white card
cx = W // 2
d.text((cx, 520), "Pro", font=font(BOLD, 64), fill=INK, anchor="ma")
d.text((cx, 640), "$20/月", font=font(BOLD, 110), fill=INK, anchor="ma")
d.line([230, 800, 850, 800], fill=CARD_EDGE, width=3)
lines2 = [("年付 $200，约 $17/月", INK), ("含 Claude Code，默认 Opus 5.5", INK),
          ("普通人最值", RED)]
y = 900
for t, c in lines2:
    d.text((cx, y), t, font=font(BOLD, 48), fill=c, anchor="ma")
    y += 92
paste_centered(im, stamp("最值", 64), 900, 500)
subtitle(d, "Pro 二十美元，最值")
source_line(d, "来源：claude.com/pricing · 2026-11-28")
im.save(os.path.join(FRAMES, "frame2.png"))

# ---------------- S3: Cursor 变贵了，三十起 ----------------
im, d = new_frame()
centered_segments(d, [("$30", font(BOLD, 150), RED, False),
                      (" 起", font(BOLD, 110), INK, False)], 300)
card_image(im, d, os.path.join(SHOTS, "ev-s3-premium.png"), cy=930)
subtitle(d, "Cursor 变贵了，三十起")
source_line(d, "来源：cursor.com/pricing · 2026-11-28")
im.save(os.path.join(FRAMES, "frame3.png"))

# ---------------- S4: 十美元，就能摸到 Sonnet ----------------
im, d = new_frame()
d.text((W // 2, 150), "$10", font=font(BOLD, 170), fill=RED, anchor="ma")
d.text((cx, 520), "GitHub Copilot", font=font(BOLD, 56), fill=GREY,
       anchor="ma")
d.text((cx, 640), "Pro $10/月", font=font(BOLD, 100), fill=INK, anchor="ma")
d.line([230, 800, 850, 800], fill=CARD_EDGE, width=3)
lines4 = [("含 Claude Sonnet 5.5", INK), ("不含 Opus 5.5，Pro+ $39 才有", INK),
          ("最便宜的 Sonnet 入口", RED)]
y = 900
for t, c in lines4:
    d.text((cx, y), t, font=font(BOLD, 48), fill=c, anchor="ma")
    y += 92
subtitle(d, "十美元，就能摸到 Sonnet")
source_line(d, "来源：GitHub Copilot 官网 · 2026-11-27 复核")
im.save(os.path.join(FRAMES, "frame4.png"))

# ---------------- S5: 免费的 Claude，只剩两天 ----------------
im, d = new_frame()
paste_centered(im, stamp("只剩 2 天", 120), W // 2, 235)
pic = fit_image(os.path.join(SHOTS, "ev-s5-models.png"), 860, 470)
x0 = (W - pic.width) // 2
im.paste(pic, (x0, 470))
d.rectangle([x0 - 3, 467, x0 + pic.width + 3, 470 + pic.height + 3],
            outline=(221, 210, 188), width=2)
d.line([230, 1010, 850, 1010], fill=CARD_EDGE, width=3)
d.text((W // 2, 1060), "免费档的 Claude 4.6，脚注 ④：",
       font=font(BOLD, 44), fill=INK, anchor="ma")
fn = fit_image(os.path.join(SHOTS, "ev-s5-footnote.png"), 860, 160)
fx0 = (W - fn.width) // 2
# light red strip behind footnote
d.rounded_rectangle([fx0 - 16, 1130, fx0 + fn.width + 16, 1130 + fn.height + 32],
                    radius=16, fill=(253, 236, 236))
im.paste(fn, (fx0, 1146))
subtitle(d, "免费的 Claude，只剩两天")
source_line(d, "来源：antigravity.google/pricing · 2026-11-28")
im.save(os.path.join(FRAMES, "frame5.png"))

# ---------------- S6: 天天写代码，Pro 最值 ----------------
im, d = new_frame()
d.text((W // 2, 120), "天天写代码，", font=font(BOLD, 92), fill=INK,
       anchor="ma")
centered_segments(d, [("Pro ", font(BOLD, 92), INK, False),
                      ("最值", font(BOLD, 92), INK, True)], 340)
rows = [
    ("官方免费档", "$0", "上不了", RED),
    ("官方 Pro", "$20/月", "最值", RED),
    ("Cursor", "$30/月起", "变贵了", INK),
    ("Copilot Pro", "$10/月", "最便宜", INK),
    ("Antigravity 免费档", "$0", "只剩 2 天", RED),
    ("Kiro 免费档", "$0", "能摸到", INK),
]
d.text((110, 480), "渠道", font=font(BOLD, 40), fill=GREY, anchor="ls")
d.text((560, 480), "价格", font=font(BOLD, 40), fill=GREY, anchor="ls")
d.text((970, 480), "结论", font=font(BOLD, 40), fill=GREY, anchor="rs")
d.line([110, 500, 970, 500], fill=CARD_EDGE, width=3)
y = 580
for label, price, verdict, vc in rows:
    d.text((110, y), label, font=font(BOLD, 46), fill=INK, anchor="ls")
    d.text((560, y), price, font=font(BOLD, 46), fill=INK, anchor="ls")
    d.text((970, y), verdict, font=font(BOLD, 46), fill=vc, anchor="rs")
    y += 140
    if label != rows[-1][0]:
        d.line([110, y - 28, 970, y - 28], fill=(238, 232, 214), width=2)
subtitle(d, "天天写代码，Pro 最值")
source_line(d, "数据：Claude / Cursor / Antigravity 官网，2026-11-28")
im.save(os.path.join(FRAMES, "frame6.png"))

print("frames done:", [f"frame{i}.png" for i in range(1, 7)])
