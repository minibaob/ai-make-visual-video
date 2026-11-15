#!/usr/bin/env python3
"""ASR-verify earthbelt narration segments with faster-whisper.
transcribe(path) is broken with the installed av, so decode with ffmpeg
to s16le 16kHz mono and pass a numpy PCM array instead."""
import os
import subprocess

import numpy as np
from faster_whisper import WhisperModel

SEGMENTS = [
    "给地球系根腰带，离地一米。",
    "绳子要加长多少？",
    "只要六点二八米。",
    "和地球多大，没关系。",
    "周长差，就是二π。",
]
DIR = os.path.expanduser("~/workspace/imagine_media/earthbelt-narration")

model = WhisperModel("small", device="cpu", compute_type="int8")
for i, expected in enumerate(SEGMENTS, 1):
    path = os.path.join(DIR, f"seg{i}.mp3")
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", path,
        "-f", "s16le", "-ac", "1", "-ar", "16000", "-",
    ])
    pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    segs, _ = model.transcribe(pcm, language="zh", beam_size=1)
    heard = "".join(s.text for s in segs).strip()
    print(f"seg{i} expected: {expected}")
    print(f"seg{i} heard:    {heard}")
    print(f"seg{i} match: {heard.replace(' ', '') == expected.replace(' ', '').replace('。', '').replace('？', '') or expected.replace('。', '').replace('？', '') in heard.replace(' ', '').replace('。', '').replace('？', '')}")
