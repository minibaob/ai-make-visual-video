#!/usr/bin/env python3
"""Build Douyin AI video 02 (robot on Mercedes line) from real footage.

Layout (human-editor vertical repost): blurred background fills 1080x1920,
the 16:9 official clip sits centered (1080x607), big hook text on top,
one-line subtitles at the bottom. Text overlays are PIL-rendered PNGs
(no Manim, no drawtext escaping pain). Music + narration baked in.
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

HOME = os.path.expanduser("~")
SRC = os.path.join(HOME, "workspace/douyin-ai-video/media/robot02/apollo-mercedes-official.webm")
TTS = os.path.join(HOME, "workspace/douyin-ai-video/tts2")
BGM = os.path.join(HOME, "workspace/imagine_media/bgm-mixkit.mp3")
OUT_DIR = os.path.join(HOME, "workspace/imagine_media")
OVER = os.path.join(HOME, "workspace/douyin-ai-video/media/robot02/overlays")
os.makedirs(OVER, exist_ok=True)

W, H = 1080, 1920
CLIP_W, CLIP_H = 1080, 607
CLIP_Y = (H - CLIP_H) // 2  # 656
DUR = 19.3

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
YELLOW = "#FFD93D"
CYAN = "#58C4DD"
WHITE = "#F8FAFC"
GREY = "#8A94A6"


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def save_overlay(name, draw_fn, size=(W, 520)):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw_fn(d, *size)
    p = os.path.join(OVER, name)
    im.save(p)
    return p


# --- hook: big 96% + line, top area ---
def hook_draw(d, w, h):
    f_big = font(BOLD, 230)
    f_sub = font(BOLD, 62)
    d.text((w // 2, 30), "96%", font=f_big, fill=YELLOW, anchor="ma")
    d.text((w // 2, 300), "奔驰产线 分拣成功率", font=f_sub, fill=WHITE, anchor="ma")


hook_png = save_overlay("hook.png", hook_draw, (W, 420))


# --- subtitles: white bold on semi-transparent rounded box ---
def subtitle_png(name, lines, y_extra=0):
    """lines: list of (text, size, color). One PNG 1080x(90*len+40)."""
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
    ("奔驰产线上来了个机器人", 0.10, 2.95),
    ("分拣零件，成功率96%", 3.05, 6.45),
    ("在匈牙利和德国的真产线上", 6.55, 9.65),
    ("不过这数是厂商自己说的", 9.75, 12.60),
    ("做了多少次，它没公布", 12.55, 15.20),
    ("100次里错4次，产线还不敢全靠它", 15.25, 19.05),
]
sub_pngs = []
for i, (text, _, _) in enumerate(SUBS, 1):
    if i == 4:
        p, h = subtitle_png(f"sub{i}.png", [
            ("厂商说法 · 未公布试验次数", 40, YELLOW),
            (text, 54, WHITE),
        ])
    else:
        p, h = subtitle_png(f"sub{i}.png", [(text, 54, WHITE)])
    sub_pngs.append((p, h))

# --- source line, two centered lines, bottom (one line overflowed 1080px) ---
f_src = font(REG, 34)
src_lines = ["来源：Google DeepMind 2026.11.10", "画面：官方演示（2倍速）"]
im = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.text((W // 2, 2), src_lines[0], font=f_src, fill=GREY, anchor="ma")
d.text((W // 2, 52), src_lines[1], font=f_src, fill=GREY, anchor="ma")
src_png = os.path.join(OVER, "source.png")
im.save(src_png)

# --- voiceover offsets (measured TTS durations) ---
# seg: start, duration
VO = [
    (0.15, 2.664),
    (3.10, 3.240),
    (6.60, 2.928),
    (9.80, 2.688),
    (12.60, 2.472),
    (15.30, 3.624),
]

# --- build ffmpeg command ---
inputs = ["ffmpeg", "-y", "-v", "error",
          "-i", SRC]
# overlay images as looped inputs
img_inputs = [hook_png] + [p for p, _ in sub_pngs] + [src_png]
for p in img_inputs:
    inputs += ["-loop", "1", "-framerate", "30", "-i", p]
# audio inputs: 6 TTS + bgm
for i in range(1, 7):
    inputs += ["-i", os.path.join(TTS, f"seg{i}.mp3")]
inputs += ["-stream_loop", "-1", "-i", BGM]

# input indices: 0=video, 1=hook, 2..7=subs, 8=source, 9..14=tts, 15=bgm
fc = []
fc.append("[0:v]trim=0:19.3,setpts=PTS-STARTPTS,split=2[bg_src][fg_src]")
fc.append("[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
          "crop=1080:1920,gblur=sigma=45,eq=brightness=-0.10:saturation=0.85[bg]")
fc.append("[fg_src]scale=1080:607,fps=30[fg]")
fc.append(f"[bg][fg]overlay=0:{CLIP_Y}[base]")
prev = "base"
# hook
fc.append(f"[{prev}][1:v]overlay=0:100:enable='between(t,0,3.1)'[v1]")
prev = "v1"
# subtitles
sub_y = 1340
for i, ((_, t0, t1), (p, h)) in enumerate(zip(SUBS, sub_pngs), 1):
    y = 1270 if i == 4 else sub_y  # two-line box must stay below the clip (ends 1263)
    fc.append(f"[{prev}][{1 + i}:v]overlay=0:{y}:enable='between(t,{t0},{t1})'[v{i + 1}]")
    prev = f"v{i + 1}"
# source line
fc.append(f"[{prev}][8:v]overlay=0:1540:enable='between(t,15.25,19.3)'[vout]")

# audio: delay each TTS, mix, add bgm
for i, (start, _) in enumerate(VO):
    ms = int(start * 1000)
    fc.append(f"[{9 + i}:a]aresample=44100,aformat=channel_layouts=stereo,"
              f"adelay={ms}:all=1[vo{i + 1}]")
vo_mix = "".join(f"[vo{i + 1}]" for i in range(6))
fc.append(f"{vo_mix}amix=inputs=6:duration=longest:normalize=0[vo]")
fc.append("[15:a]atrim=0:19.3,aresample=44100,aformat=channel_layouts=stereo,"
          "volume=0.5,afade=t=out:st=18.3:d=1.0[bgm]")
fc.append("[vo][bgm]amix=inputs=2:duration=longest:normalize=0,"
          "alimiter=limit=0.95[aout]")

filter_complex = ";".join(fc)
silent = os.path.join(OUT_DIR, "robot-mercedes-20s-1080x1920-silent.mp4")
mixed = os.path.join(OUT_DIR, "robot-mercedes-20s-1080x1920.mp4")

base_cmd = inputs + ["-filter_complex", filter_complex,
                     "-map", "[vout]", "-map", "[aout]",
                     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                     "-crf", "20", "-preset", "medium",
                     "-c:a", "aac", "-b:a", "128k",
                     "-t", str(DUR), "-movflags", "+faststart", mixed]
print("MIXED:", " ".join(base_cmd[:6]), "...")
r = subprocess.run(base_cmd)
print("mixed rc:", r.returncode)

silent_cmd = ["ffmpeg", "-y", "-v", "error", "-i", mixed,
              "-c:v", "copy", "-an", silent]
r2 = subprocess.run(silent_cmd)
print("silent rc:", r2.returncode)
print("done:", mixed, "|", silent)
