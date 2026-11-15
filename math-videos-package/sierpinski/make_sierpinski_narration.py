#!/usr/bin/env python3
"""Sierpinski triangle narration via raw_edge_tts (the working route on
this VM). Voice zh-CN-XiaoxiaoNeural, rate +10%. Segments kept short so
each fits its 4s window (<=18 chars). Numbers EXACT: remaining area
(3/4)^n: 100.0%, 75.0%, 56.3%, 42.2%, 31.6%, 23.7% after 5 iterations."""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "一个三角形，挖掉中间。",
    "每次挖掉四分之一。",
    "再挖一次，还是这样。",
    "挖到第五次，只剩23.7%。",
    "无限挖下去，面积归零。",
]

VOICE = "zh-CN-XiaoxiaoNeural"
OUT = os.path.expanduser("~/workspace/imagine_media/sierpinski-narration")
os.makedirs(OUT, exist_ok=True)

for i, text in enumerate(SEGMENTS, 1):
    path = os.path.join(OUT, f"seg{i}.mp3")
    synth(text, VOICE, path, rate="+10%")
    print(f"seg{i} -> {path} ({os.path.getsize(path)} bytes)")
