#!/usr/bin/env python3
"""Buffon narration via raw_edge_tts (the working route on this VM;
edge-tts via aiohttp is broken here: egress proxy MITMs TLS and strips
the Connection: Upgrade header). Voice zh-CN-XiaoxiaoNeural, rate +10%.
Segments kept short so each fits its 4 s window (MC lesson: first draft
ran 27 s total). Final numbers are REAL: seed 20261112, N=1500 needles,
946 crossing, pi = 2*1500/946 = 3.1712 -> 3.17."""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "往地上扔针，也能算出圆周率。",
    "地上画满平行线，针随便扔。",
    "针压到线的概率，和派有关系。",
    "扔得越多，算得越准，越接近三点一四。",
    "布丰投针，1500针，算出3.17。",
]

VOICE = "zh-CN-XiaoxiaoNeural"
OUT = os.path.expanduser("~/workspace/imagine_media/buffon-narration")
os.makedirs(OUT, exist_ok=True)

for i, text in enumerate(SEGMENTS, 1):
    path = os.path.join(OUT, f"seg{i}.mp3")
    synth(text, VOICE, path, rate="+10%")
    print(f"seg{i} -> {path} ({os.path.getsize(path)} bytes)")
