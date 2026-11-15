#!/usr/bin/env python3
"""Second-opinion ASR check for the Sierpinski narration segments that the
small model flagged, using the base model. Normalisation handles Whisper
artifacts that are NOT audio errors: traditional chars, digit words
(五 vs 5), % spoken as 百分之, punctuation."""
import os
import subprocess

import numpy as np
from faster_whisper import WhisperModel

EXPECTED = {
    3: "再挖一次，还是这样。",
    4: "挖到第五次，只剩23.7%。",
    5: "无限挖下去，面积归零。",
}

TRAD = str.maketrans({"無": "无", "線": "线", "面": "面", "積": "积",
                      "歸": "归", "挖": "挖", "晚": "晚"})
NUM = str.maketrans({"零": "0", "一": "1", "二": "2", "三": "3", "四": "4",
                     "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"})


def norm(s):
    s = s.translate(TRAD)
    s = s.replace("百分之二十三点七", "23.7%").replace("二十三点七", "23.7")
    s = s.translate(NUM)
    for a, b in [(" ", ""), ("，", ","), ("。", "."), ("百分之", "%"),
                 ("％", "%")]:
        s = s.replace(a, b)
    return s


DIR = os.path.expanduser("~/workspace/imagine_media/sierpinski-narration")
model = WhisperModel("base", device="cpu", compute_type="int8")

for i, expected in EXPECTED.items():
    path = os.path.join(DIR, f"seg{i}.mp3")
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", path,
        "-f", "s16le", "-ac", "1", "-ar", "16000", "-",
    ])
    pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(pcm, language="zh")
    heard = "".join(s.text for s in segments).strip()
    match = norm(heard) == norm(expected)
    print(f"seg{i} [{'OK ' if match else 'CHECK'}] expected={expected!r} "
          f"heard={heard!r} norm_heard={norm(heard)!r} norm_exp={norm(expected)!r}")
