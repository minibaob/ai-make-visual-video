#!/usr/bin/env python3
"""Mix voiceover + BGM onto the Remotion silent render (Codex long version).

Pattern copied from build_video03_pass2.py (proven on the 20s version):
each TTS segment adelayed to its timeline offset, amix; BGM at 0.5 with
tail fade; alimiter. BGM is pre-looped to cover the 129.6s video with a
separate input-level -stream_loop pass (never -stream_loop inside the
filter graph -- that deadlocked the 20s build).
"""
import json
import os
import re
import subprocess

HOME = os.path.expanduser("~")
PROJ = os.path.join(HOME, "workspace/douyin-ai-video/codex-long-remotion")
TTS_DIR = os.path.join(HOME, "workspace/douyin-ai-video/media/codex03/tts-long")
BGM = os.path.join(HOME, "workspace/imagine_media/bgm-mixkit.mp3")
OUT_DIR = os.path.join(HOME, "workspace/imagine_media")
SILENT = os.path.join(OUT_DIR, "codex-shangche-long-1920x1080-silent.mp4")
MIXED = os.path.join(OUT_DIR, "codex-shangche-long-1920x1080.mp4")
BGM_LONG = os.path.join(PROJ, "bgm-long.mp3")

# Read line offsets + total duration from timeline.ts
tl = open(os.path.join(PROJ, "src/timeline.ts"), encoding="utf-8").read()
total_frames = int(re.search(r"TOTAL_FRAMES = (\d+)", tl).group(1))
DUR = total_frames / 30.0
lines = json.loads(tl.split("export const LINES = ")[1].split(";\n")[0])
VO = [(l["start"] / 30.0, l["id"]) for l in lines]
print(f"duration {DUR:.2f}s, {len(VO)} voiceover segments")

# 1. Pre-loop BGM to cover the video (input-level loop only).
subprocess.run([
    "ffmpeg", "-y", "-nostdin", "-v", "error",
    "-stream_loop", "1", "-i", BGM, "-t", str(DUR + 5), BGM_LONG,
], check=True)

# 2. Mix.
inputs = ["ffmpeg", "-y", "-nostdin", "-v", "error", "-i", SILENT]
for _start, seg in VO:
    inputs += ["-i", os.path.join(TTS_DIR, f"{seg}.mp3")]
inputs += ["-i", BGM_LONG]
# input indices: 0=silent video, 1..41=tts, 42=bgm
fc = []
for i, (start, _seg) in enumerate(VO):
    ms = int(start * 1000)
    fc.append(
        f"[{1 + i}:a]aresample=44100,aformat=channel_layouts=stereo,"
        f"adelay={ms}:all=1[vo{i + 1}]"
    )
vo_mix = "".join(f"[vo{i + 1}]" for i in range(len(VO)))
fc.append(f"{vo_mix}amix=inputs={len(VO)}:duration=longest:normalize=0[vo]")
fc.append(
    f"[42:a]atrim=0:{DUR:.3f},aresample=44100,aformat=channel_layouts=stereo,"
    f"volume=0.5,afade=t=out:st={DUR - 1.5:.2f}:d=1.5[bgm]"
)
fc.append("[vo][bgm]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[aout]")

cmd = inputs + ["-filter_complex", ";".join(fc),
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "128k",
                "-t", f"{DUR:.3f}", "-movflags", "+faststart", MIXED]
print("running mix...")
r = subprocess.run(cmd)
print("mix rc:", r.returncode)
print("done:", MIXED)
