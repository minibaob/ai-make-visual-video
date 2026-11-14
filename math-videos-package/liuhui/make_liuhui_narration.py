#!/usr/bin/env python3
"""Liu Hui 割圆术 narration via raw_edge_tts (the working route on this VM).
Voice zh-CN-XiaoxiaoNeural, rate +10%. Segments kept short so each fits its
4s window. Numbers EXACT: inscribed n-gon pi ~ n*sin(pi/n):
6 -> 3.0000, 12 -> 3.1058, 24 -> 3.1326, 48 -> 3.1394, 96 -> 3.1410."""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "拿多边形，也能逼近圆周率。",
    "六边形，周长除以直径，等于3。",
    "边数翻倍，越来越像圆。",
    "切到96边，算出3.1410。",
    "割之弥细，所失弥少。",
]

VOICE = "zh-CN-XiaoxiaoNeural"
OUT = os.path.expanduser("~/workspace/imagine_media/liuhui-narration")
os.makedirs(OUT, exist_ok=True)

for i, text in enumerate(SEGMENTS, 1):
    path = os.path.join(OUT, f"seg{i}.mp3")
    synth(text, VOICE, path, rate="+10%")
    print(f"seg{i} -> {path} ({os.path.getsize(path)} bytes)")
