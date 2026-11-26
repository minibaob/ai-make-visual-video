#!/usr/bin/env python3
"""Generate the 6 voiceover lines for Douyin AI video 01 (price war).

Lines verbatim from plan-01.md. Voice zh-CN-XiaoxiaoNeural, rate +10%.
"""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "同样一套题，第一名花了二十六块五毛四",
    "第二名只花了四块，分数还差三分",
    "单价明明一样，都是八美元",
    "贵就贵在它话太多，费的词多",
    "这数是第三方榜单实测的",
    "三分，多花二十二块",
]

OUT = os.path.expanduser("~/workspace/douyin-ai-video/tts")
os.makedirs(OUT, exist_ok=True)

for i, text in enumerate(SEGMENTS, 1):
    path = os.path.join(OUT, f"seg{i}.mp3")
    n = synth(text, "zh-CN-XiaoxiaoNeural", path, rate="+10%")
    print(f"seg{i} OK: {len(text)} chars, {n} bytes -> {path}", flush=True)
