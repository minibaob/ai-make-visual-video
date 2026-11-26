#!/usr/bin/env python3
"""Pass 2 for Douyin AI video 03: overlays + audio onto segments/base.mp4.

Fix vs build_video03.py: the first attempt hung (ffmpeg stalled in
futex wait, 0 CPU for 10+ min). Suspected cause: `-loop 1` infinite image
inputs + `-stream_loop -1` bgm inside the filter graph. This version uses
plain single-frame PNG inputs (overlay's default eof_action=repeat keeps
the still visible) and a finite bgm input (96.6s > 19.6s needed, no loop).
Adds -nostdin and a -progress log.
"""
import os
import subprocess

HOME = os.path.expanduser("~")
MEDIA = os.path.join(HOME, "workspace/douyin-ai-video/media/codex03")
TTS = os.path.join(MEDIA, "tts")
BGM = os.path.join(HOME, "workspace/imagine_media/bgm-mixkit.mp3")
OUT_DIR = os.path.join(HOME, "workspace/imagine_media")
OVER = os.path.join(MEDIA, "overlays")
SEG_DIR = os.path.join(MEDIA, "segments")

DUR = 19.6
base = os.path.join(SEG_DIR, "base.mp4")
hook_png = os.path.join(OVER, "hook.png")
sub_pngs = [os.path.join(OVER, f"sub{i}.png") for i in range(2, 6)]
stamp_pngs = [os.path.join(OVER, f"stamp{i}.png") for i in range(2, 6)]
stamp_w = [218, 218, 218, 218]  # measured below, overridden
big6_png = os.path.join(OVER, "big6.png")
src_png = os.path.join(OVER, "source.png")

from PIL import Image
for i, p in enumerate(stamp_pngs):
    stamp_w[i] = Image.open(p).size[0]

inputs = ["ffmpeg", "-y", "-nostdin", "-v", "error", "-i", base]
img_inputs = [hook_png] + sub_pngs + stamp_pngs + [big6_png, src_png]
for p in img_inputs:
    inputs += ["-i", p]
for i in range(1, 7):
    inputs += ["-i", os.path.join(TTS, f"seg{i}.mp3")]
inputs += ["-i", BGM]

# input indices: 0=base, 1=hook, 2..5=subs, 6..9=stamps, 10=big6,
# 11=source, 12..17=tts, 18=bgm
SUBS = [(3.2, 6.5), (6.5, 10.0), (10.0, 13.0), (13.0, 16.2)]
STAMPS = [(3.2, 6.5), (6.5, 10.0), (10.0, 13.0), (13.0, 16.2)]
fc = []
prev = "0:v"
fc.append(f"[{prev}][1:v]overlay=0:100:enable='between(t,0,3.2)'[v1]")
prev = "v1"
for i, (t0, t1) in enumerate(SUBS, 1):
    fc.append(f"[{prev}][{1 + i}:v]overlay=0:1340:enable='between(t,{t0},{t1})'[v{i + 1}]")
    prev = f"v{i + 1}"
n = 6
for j, (t0, t1) in enumerate(STAMPS):
    x = 1030 - stamp_w[j]
    fc.append(f"[{prev}][{6 + j}:v]overlay={x}:520:enable='between(t,{t0},{t1})'[v{n}]")
    prev = f"v{n}"
    n += 1
fc.append(f"[{prev}][10:v]overlay=0:180:enable='between(t,16.2,19.6)'[v{n}]")
prev = f"v{n}"
n += 1
fc.append(f"[{prev}][11:v]overlay=0:1540:enable='between(t,16.2,19.6)'[vout]")

VO = [(0.15, 2.424), (3.35, 2.232), (6.65, 2.568),
      (10.15, 2.448), (13.15, 2.760), (16.35, 2.400)]
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

mixed = os.path.join(OUT_DIR, "codex-shangche-20s-1080x1920.mp4")
silent = os.path.join(OUT_DIR, "codex-shangche-20s-1080x1920-silent.mp4")
progress = os.path.join(SEG_DIR, "pass2-progress.log")

cmd = inputs + ["-filter_complex", ";".join(fc),
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                "-crf", "20", "-preset", "medium",
                "-c:a", "aac", "-b:a", "128k",
                "-t", str(DUR), "-movflags", "+faststart",
                "-progress", progress, mixed]
print("running pass2...")
r = subprocess.run(cmd)
print("mixed rc:", r.returncode)
if r.returncode == 0:
    r2 = subprocess.run(["ffmpeg", "-y", "-nostdin", "-v", "error", "-i", mixed,
                         "-c:v", "copy", "-an", silent])
    print("silent rc:", r2.returncode)
print("done:", mixed, "|", silent)
