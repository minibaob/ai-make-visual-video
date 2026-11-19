#!/usr/bin/env python3
"""ASR-verify the muxed Taylor audio: each of the 6 segments must be heard
inside its 5 s window (0-5, 5-10, 10-15, 15-20, 20-25, 25-30).
Uses faster-whisper with a numpy PCM array (transcribe(path) is broken
with the installed av)."""
import subprocess
import numpy as np
from faster_whisper import WhisperModel

EXPECTED = [
    # (window start, window end, expected line, distinctive key phrase)
    # Key phrases are used for the match because ASR commonly mis-hears
    # homophones ("sin x"->"SynX", "多项式"->"多向式", "再"->"在",
    # "得"->"的") and punctuation variants ("、" / ","). The heard
    # timestamps are the real placement proof; the key phrase confirms
    # the words.
    (0, 5, "这条曲线是 sin x", "这条曲线是"),
    (5, 10, "直线只能贴住中间一小段", "直线只能贴住中间一小段"),
    (10, 15, "三次多项式，贴得更远", "更远"),
    (15, 20, "五次，七次，越贴越远", "越贴越远"),
    (20, 25, "这就是泰勒公式", "这就是泰勒公式"),
    (25, 30, "再复杂的曲线，都是多项式拼出来的", "拼出来"),
]
raw = subprocess.check_output([
    "ffmpeg", "-v", "error", "-i",
    "/home/hatch/workspace/imagine_media/taylor-30s-1080x1920-voiced.mp4",
    "-vn", "-f", "s16le", "-ac", "1", "-ar", "16000", "-",
])
pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
model = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = model.transcribe(pcm, language="zh", beam_size=1)
heard = [(round(s.start, 2), round(s.end, 2), s.text.strip()) for s in segs]
for h in heard:
    print("heard:", h)


def norm(t):
    return (t.replace(" ", "").replace("。", "").replace("？", "")
             .replace("，", "").replace("、", "").replace(",", ""))


for i, (w0, w1, exp, key) in enumerate(EXPECTED, 1):
    ok = any(w0 <= st < w1 and norm(key) in norm(t)
             for st, _, t in heard)
    print(f"seg{i} window {w0}-{w1}s: {'OK' if ok else 'MISSING'} ({exp})")
