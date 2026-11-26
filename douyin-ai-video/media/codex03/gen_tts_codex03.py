import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    ("seg1", "Codex 零元就能上车"),
    ("seg2", "免费档在桌面 App 里"),
    ("seg3", "二十美元开网页命令行"),
    ("seg4", "一百美元没五小时限制"),
    ("seg5", "不想订阅就按量付 API"),
    ("seg6", "普通人二十美元最值"),
]

out_dir = os.path.expanduser("~/workspace/douyin-ai-video/media/codex03/tts")
os.makedirs(out_dir, exist_ok=True)
for name, text in SEGMENTS:
    path = os.path.join(out_dir, f"{name}.mp3")
    n = synth(text, "zh-CN-XiaoxiaoNeural", path, rate="+10%")
    print(f"{name} OK: {n} bytes -> {path}", flush=True)
