#!/usr/bin/env python3
"""Generate the 6 voiceover lines for Douyin AI video 02 (robot on Mercedes line).

Lines verbatim from plan-02.md. Voice zh-CN-XiaoxiaoNeural, rate +10%.
"""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "奔驰产线上来了个机器人",
    "分拣零件，成功率96%",
    "在匈牙利和德国的真产线上",
    "不过这数是厂商自己说的",
    "做了多少次，它没公布",
    "100次里错4次，产线还不敢全靠它",
]

OUT = os.path.expanduser("~/workspace/douyin-ai-video/tts2")
os.makedirs(OUT, exist_ok=True)

for i, text in enumerate(SEGMENTS, 1):
    path = os.path.join(OUT, f"seg{i}.mp3")
    n = synth(text, "zh-CN-XiaoxiaoNeural", path, rate="+10%")
    print(f"seg{i} OK: {len(text)} chars, {n} bytes -> {path}", flush=True)
