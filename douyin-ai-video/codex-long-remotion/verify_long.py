#!/usr/bin/env python3
"""Verify the Codex long video: ffprobe specs + ASR spot-check of the
voiceover + frame extraction across all 8 scenes for visual review.
"""
import json
import os
import subprocess
import sys

import numpy as np

HOME = os.path.expanduser("~")
MIXED = os.path.join(HOME, "workspace/imagine_media/codex-shangche-long-1920x1080.mp4")
SILENT = os.path.join(HOME, "workspace/imagine_media/codex-shangche-long-1920x1080-silent.mp4")
OUT = "/tmp/cl_verify"
os.makedirs(OUT, exist_ok=True)

# 1. ffprobe both files
for p in (SILENT, MIXED):
    print("=" * 60)
    print(p)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=codec_type,codec_name,width,height,r_frame_rate",
                        "-show_entries", "format=duration,size",
                        "-of", "default=noprint_wrappers=1", p],
                       capture_output=True, text=True)
    print(r.stdout)

# 2. ASR spot-check: decode mixed audio to PCM and transcribe with faster-whisper
print("=" * 60)
print("ASR spot-check on mixed audio ...")
sys.path.insert(0, os.path.expanduser("~/workspace/venvs/asr/lib/python3.12/site-packages"))
from faster_whisper import WhisperModel
raw = subprocess.check_output([
    "ffmpeg", "-v", "error", "-i", MIXED,
    "-f", "s16le", "-ac", "1", "-ar", "16000", "-",
])
pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
model = WhisperModel("tiny", device="cpu", compute_type="int8")
segments, _info = model.transcribe(pcm, language="zh", beam_size=1)
lines = []
for s in segments:
    lines.append((round(s.start, 1), round(s.end, 1), s.text.strip()))
    print(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}")
print(f"ASR segments: {len(lines)} (expect ~41 voiceover lines)")

# 3. Frame extraction: mid-scene frames for visual review
tl = open(os.path.join(HOME, "workspace/douyin-ai-video/codex-long-remotion/src/timeline.ts"),
          encoding="utf-8").read()
scenes = json.loads(tl.split("export const SCENES = ")[1].split(";\n")[0])
for s in scenes:
    mid = (s["start"] + s["end"]) // 2
    t = mid / 30.0
    out = os.path.join(OUT, f"{s['id']}-{mid}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t),
                    "-i", MIXED, "-frames:v", "1", out], check=True)
    print(f"frame {s['id']} @ {t:.1f}s -> {out}")
print("verify done")
