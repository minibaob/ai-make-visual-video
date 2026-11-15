#!/usr/bin/env python3
"""ASR-verify the Sierpinski narration segments with faster-whisper.
transcribe(path) is broken with the installed `av` (metadata_errors kwarg),
so decode with ffmpeg to s16le 16kHz mono and pass a numpy PCM array.
"""
import os
import subprocess

import numpy as np
from faster_whisper import WhisperModel

EXPECTED = [
    "一个三角形，挖掉中间。",
    "每次挖掉四分之一。",
    "再挖一次，还是这样。",
    "挖到第五次，只剩23.7%。",
    "无限挖下去，面积归零。",
]

DIR = os.path.expanduser("~/workspace/imagine_media/sierpinski-narration")
model = WhisperModel("small", device="cpu", compute_type="int8")

ok = True
for i, expected in enumerate(EXPECTED, 1):
    path = os.path.join(DIR, f"seg{i}.mp3")
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", path,
        "-f", "s16le", "-ac", "1", "-ar", "16000", "-",
    ])
    pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(pcm, language="zh")
    heard = "".join(s.text for s in segments).strip()
    # normalise punctuation/spacing for comparison
    norm = lambda s: (s.replace(" ", "").replace("，", ",").replace("。", ".")
                      .replace("%", "百分之").replace("23.7", "二十三点七"))
    match = norm(heard) in norm(expected) or norm(expected) in norm(heard)
    status = "OK " if match else "CHECK"
    if not match:
        ok = False
    print(f"seg{i} [{status}] expected={expected!r} heard={heard!r}")
print("ALL OK" if ok else "NEEDS REVIEW")
