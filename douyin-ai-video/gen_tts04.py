#!/usr/bin/env python3
"""Generate the 6 voiceover lines for Douyin AI video 04 (Claude Code, 20s).

Lines verbatim from plan-04-claude-20s.md. Voice zh-CN-XiaoxiaoNeural, rate +10%.
Run with ~/workspace/venvs/asr/bin/python (see plan-04-claude-20s.md).
"""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "免费档，上不了",
    "Pro 二十美元，最值",
    "Cursor 变贵了，三十起",
    "十美元，就能摸到 Sonnet",
    "免费的 Claude，只剩两天",
    "天天写代码，Pro 最值",
]

OUT = os.path.expanduser("~/workspace/douyin-ai-video/media/claude04/tts")
os.makedirs(OUT, exist_ok=True)

for i, text in enumerate(SEGMENTS, 1):
    path = os.path.join(OUT, f"seg{i}.mp3")
    n = synth(text, "zh-CN-XiaoxiaoNeural", path, rate="+10%")
    print(f"seg{i} OK: {len(text)} chars, {n} bytes -> {path}", flush=True)
