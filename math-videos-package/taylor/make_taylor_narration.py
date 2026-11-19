#!/usr/bin/env python3
"""Taylor (sin x) narration via raw_edge_tts (the working route on this VM).
Voice zh-CN-XiaoxiaoNeural, rate +10%. Six segments, one per 5 s window
(0-5, 5-10, 10-15, 15-20, 20-25, 25-30); at +10% Xiaoxiao speaks
~4.3 chars/s, so each line stays <= 20 chars (<= ~4.7 s).
Math EXACT: sin x = x - x^3/6 + x^5/120 - x^7/5040.
Retry note: the edge-tts service drops connections intermittently
("socket closed while reading"), so each segment retries up to 5 times
with backoff; already-generated segments are skipped."""
import os
import sys
import time

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "这条曲线是 sin x",
    "直线只能贴住中间一小段",
    "三次多项式，贴得更远",
    "五次，七次，越贴越远",
    "这就是泰勒公式",
    "再复杂的曲线，都是多项式拼出来的",
]

VOICE = "zh-CN-XiaoxiaoNeural"
OUT = os.path.expanduser("~/workspace/imagine_media/taylor-narration")
os.makedirs(OUT, exist_ok=True)


def gen(i, text):
    path = os.path.join(OUT, f"seg{i}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"seg{i} exists, skip ({os.path.getsize(path)} bytes)", flush=True)
        return
    for attempt in range(1, 6):
        try:
            synth(text, VOICE, path, rate="+10%")
            print(f"seg{i} -> {path} ({os.path.getsize(path)} bytes) "
                  f"[attempt {attempt}]", flush=True)
            return
        except Exception as e:
            print(f"seg{i} attempt {attempt} failed: {e}", flush=True)
            if os.path.exists(path):
                os.remove(path)
            if attempt < 5:
                time.sleep(15 * attempt)


for i, text in enumerate(SEGMENTS, 1):
    print(f"seg{i}: {text} ({len(text)} chars)", flush=True)
    assert len(text) <= 20, f"seg{i} too long: {len(text)} chars"
    gen(i, text)
print("all segments done")
