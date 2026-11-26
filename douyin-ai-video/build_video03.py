#!/usr/bin/env python3
"""Build Douyin AI video 03: Codex 上车全渠道合集 (~20s, 1080x1920).

Real OpenAI official demo footage only. Layout = video 02 proven stack:
blurred background fills 1080x1920, 16:9 clip centered (1080x607, y=656),
PIL-rendered text PNG overlays, TTS + Mixkit bgm baked in.

Segment plan (verified against frames 2026-11-26):
- S1 0-3.2s    5UlRL 2.5-5.7s   purple brand opening (0-2.3s is white
  "With Codex", so hook starts at 2.5s where the purple block is in)
- S2 3.2-6.5s  5UlRL 8-11.3s    Event Operations / Sites workflow
- S3 6.5-10s   app-intro 29-32.5s phone+desktop same-screen UI
  (28s is still the AstroScope screen; phone scene runs 29-34s+)
- S4 10-13s    app-intro 178-181s Today's Progress task board
- S5 13-16.2s  5UlRL 15-18.2s   Sites input box typing animation
- S6 16.2-19.6s 5UlRL 36-39.4s  built-apps collage wall

Note: app-intro S3/S4 frames carry a small presenter PiP in the top-right
corner (part of the official demo; the plan's own reference frames app-30 /
app-180 show it). Verdict stamps are therefore placed in the top band
above the clip (y=520) instead of on the clip's top-right corner, so they
never sit on the presenter's face.
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

HOME = os.path.expanduser("~")
MEDIA = os.path.join(HOME, "workspace/douyin-ai-video/media/codex03")
TTS = os.path.join(MEDIA, "tts")
BGM = os.path.join(HOME, "workspace/imagine_media/bgm-mixkit.mp3")
OUT_DIR = os.path.join(HOME, "workspace/imagine_media")
OVER = os.path.join(MEDIA, "overlays")
SEG_DIR = os.path.join(MEDIA, "segments")
os.makedirs(OVER, exist_ok=True)
os.makedirs(SEG_DIR, exist_ok=True)

W, H = 1080, 1920
CLIP_W, CLIP_H = 1080, 607
CLIP_Y = (H - CLIP_H) // 2  # 656
DUR = 19.6

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
YELLOW = "#FFD93D"
RED = "#E5484D"
WHITE = "#F8FAFC"
GREY = "#8A94A6"


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def centered_segments(d, segments, y_baseline, x_center=W // 2):
    total = sum(text_w(d, s, f) for s, f, _ in segments)
    x = x_center - total / 2
    for s, f, c in segments:
        d.text((x, y_baseline), s, font=f, fill=c, anchor="ls")
        x += text_w(d, s, f)


# ---------------- text overlays (PIL) ----------------
# hook S1: big yellow 0 元上车 + white Codex 全渠道, top band
im = Image.new("RGBA", (W, 420), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.text((W // 2, 30), "0 元上车", font=font(BOLD, 200), fill=YELLOW, anchor="ma")
d.text((W // 2, 290), "Codex 全渠道", font=font(BOLD, 64), fill=WHITE, anchor="ma")
hook_png = os.path.join(OVER, "hook.png")
im.save(hook_png)

# big verdict S6: 普通人 Plus 最值 (最值 yellow), top band
im = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
centered_segments(d, [
    ("普通人 Plus ", font(BOLD, 96), WHITE),
    ("最值", font(BOLD, 96), YELLOW),
], 150)
big6_png = os.path.join(OVER, "big6.png")
im.save(big6_png)


def subtitle_png(name, lines):
    """lines: list of (text, size, color). Box 1080 x (96*len+44)."""
    f_list = [(t, font(BOLD, s), c) for t, s, c in lines]
    lh = 96
    h = lh * len(lines) + 44
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    maxw = max(d.textlength(t, font=f) for t, f, _ in f_list)
    bw, bh = int(maxw) + 72, h - 8
    bx = (W - bw) // 2
    d.rounded_rectangle([bx, 4, bx + bw, 4 + bh], radius=26, fill=(0, 0, 0, 165))
    y = 4 + 26
    for t, f, c in f_list:
        d.text((W // 2, y), t, font=f, fill=c, anchor="ma")
        y += lh
    p = os.path.join(OVER, name)
    im.save(p)
    return p, h


SUBS = [
    # (name, lines, t0, t1)
    ("sub2.png", [("免费 $0", 64, YELLOW), ("桌面 App 轻量尝鲜", 54, WHITE)], 3.2, 6.5),
    ("sub3.png", [("Plus $20/月 ≈ ¥133", 64, YELLOW), ("网页 + CLI + IDE", 54, WHITE)], 6.5, 10.0),
    ("sub4.png", [("Pro $100/月 ≈ ¥666", 64, YELLOW), ("没 5 小时限制", 54, WHITE)], 10.0, 13.0),
    ("sub5.png", [("API 按量", 64, YELLOW), ("Astra $10/$50 每百万 token", 50, WHITE)], 13.0, 16.2),
]
sub_pngs = []
for name, lines, _, _ in SUBS:
    sub_pngs.append(subtitle_png(name, lines))


def stamp_png(name, word):
    """Red stamp-style verdict, transparent bg, red outline."""
    f = font(BOLD, 56)
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tw = int(td.textlength(word, font=f))
    w, h = tw + 56, 104
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([3, 3, w - 3, h - 3], radius=16, outline=RED, width=5)
    d.text((w // 2, h // 2), word, font=f, fill=RED, anchor="mm")
    p = os.path.join(OVER, name)
    im.save(p)
    return p, w, h


STAMPS = [  # (png, word, t0, t1)
    ("stamp2.png", "能上", 3.2, 6.5),
    ("stamp3.png", "最值", 6.5, 10.0),
    ("stamp4.png", "重度", 10.0, 13.0),
    ("stamp5.png", "灵活", 13.0, 16.2),
]
stamp_pngs = []
for name, word, _, _ in STAMPS:
    stamp_pngs.append(stamp_png(name, word))

# source lines, bottom, shown during S6
f_src = font(REG, 34)
im = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.text((W // 2, 2), "数据：OpenAI 官网定价页，2026 年 11 月", font=f_src, fill=GREY, anchor="ma")
d.text((W // 2, 52), "画面：OpenAI 官方演示", font=f_src, fill=GREY, anchor="ma")
src_png = os.path.join(OVER, "source.png")
im.save(src_png)

# ---------------- pass 1: render each segment (bg blur + centered clip) ----------------
FIVE = os.path.join(MEDIA, "5UlRL_ImvQ0.mp4")
INTRO = os.path.join(MEDIA, "codex-app-intro.mp4")
SEGMENTS = [
    # (src, start, dur)
    (FIVE, 2.5, 3.2),
    (FIVE, 8.0, 3.3),
    (INTRO, 29.0, 3.5),
    (INTRO, 178.0, 3.0),
    (FIVE, 15.0, 3.2),
    (FIVE, 36.0, 3.4),
]
seg_files = []
for i, (src, start, dur) in enumerate(SEGMENTS, 1):
    out = os.path.join(SEG_DIR, f"seg{i}.mp4")
    seg_files.append(out)
    fc = ("[0:v]split=2[bg0][fg0];"
          "[bg0]scale=1080:1920:force_original_aspect_ratio=increase,"
          "crop=1080:1920,gblur=sigma=45,eq=brightness=-0.10:saturation=0.85[bg];"
          "[fg0]scale=1080:607,fps=30,format=yuv420p[fg];"
          f"[bg][fg]overlay=0:{CLIP_Y}[v]")
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-t", str(dur),
           "-i", src, "-filter_complex", fc, "-map", "[v]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
           "-crf", "20", "-preset", "medium", out]
    r = subprocess.run(cmd)
    print(f"seg{i} rc={r.returncode} src={os.path.basename(src)} {start}s +{dur}s")

# concat list
concat_txt = os.path.join(SEG_DIR, "concat.txt")
with open(concat_txt, "w") as f:
    for p in seg_files:
        f.write(f"file '{p}'\n")
base = os.path.join(SEG_DIR, "base.mp4")
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", concat_txt, "-c", "copy", base])
print("concat rc:", r.returncode)

# ---------------- pass 2: overlays + audio ----------------
inputs = ["ffmpeg", "-y", "-v", "error", "-i", base]
img_inputs = [hook_png] + [p for p, _ in sub_pngs] + \
             [p for p, _, _ in stamp_pngs] + [big6_png, src_png]
for p in img_inputs:
    inputs += ["-loop", "1", "-framerate", "30", "-i", p]
for i in range(1, 7):
    inputs += ["-i", os.path.join(TTS, f"seg{i}.mp3")]
inputs += ["-stream_loop", "-1", "-i", BGM]

# input indices: 0=base video, 1=hook, 2..5=subs, 6..9=stamps, 10=big6,
# 11=source, 12..17=tts, 18=bgm
fc = []
prev = "0:v"
fc.append(f"[{prev}][1:v]overlay=0:100:enable='between(t,0,3.2)'[v1]")
prev = "v1"
sub_y = 1340
for i, ((_, _, t0, t1), (p, h)) in enumerate(zip(SUBS, sub_pngs), 1):
    fc.append(f"[{prev}][{1 + i}:v]overlay=0:{sub_y}:enable='between(t,{t0},{t1})'[v{i + 1}]")
    prev = f"v{i + 1}"
n = len(SUBS) + 1  # next label index = 6
for j, ((_, _, t0, t1), (p, w, h)) in enumerate(zip(STAMPS, stamp_pngs)):
    idx = 6 + j
    x = 1030 - w
    fc.append(f"[{prev}][{idx}:v]overlay={x}:520:enable='between(t,{t0},{t1})'[v{n + 1}]")
    prev = f"v{n + 1}"
    n += 1
fc.append(f"[{prev}][10:v]overlay=0:180:enable='between(t,16.2,19.6)'[v{n + 1}]")
prev = f"v{n + 1}"
n += 1
fc.append(f"[{prev}][11:v]overlay=0:1540:enable='between(t,16.2,19.6)'[vout]")

# voiceover offsets (measured TTS durations all fit their windows)
VO = [
    (0.15, 2.424),
    (3.35, 2.232),
    (6.65, 2.568),
    (10.15, 2.448),
    (13.15, 2.760),
    (16.35, 2.400),
]
for i, (start, _) in enumerate(VO):
    ms = int(start * 1000)
    fc.append(f"[{12 + i}:a]aresample=44100,aformat=channel_layouts=stereo,"
              f"adelay={ms}:all=1[vo{i + 1}]")
vo_mix = "".join(f"[vo{i + 1}]" for i in range(6))
fc.append(f"{vo_mix}amix=inputs=6:duration=longest:normalize=0[vo]")
fc.append(f"[18:a]atrim=0:{DUR},aresample=44100,aformat=channel_layouts=stereo,"
          "volume=0.5,afade=t=out:st=18.6:d=1.0[bgm]")
fc.append("[vo][bgm]amix=inputs=2:duration=longest:normalize=0,"
          "alimiter=limit=0.95[aout]")

filter_complex = ";".join(fc)
mixed = os.path.join(OUT_DIR, "codex-shangche-20s-1080x1920.mp4")
silent = os.path.join(OUT_DIR, "codex-shangche-20s-1080x1920-silent.mp4")

cmd = inputs + ["-filter_complex", filter_complex,
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                "-crf", "20", "-preset", "medium",
                "-c:a", "aac", "-b:a", "128k",
                "-t", str(DUR), "-movflags", "+faststart", mixed]
r = subprocess.run(cmd)
print("mixed rc:", r.returncode)

r2 = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mixed,
                     "-c:v", "copy", "-an", silent])
print("silent rc:", r2.returncode)
print("done:", mixed, "|", silent)
