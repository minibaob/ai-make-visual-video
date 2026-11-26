import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    ("seg01", "Codex 上车，零元就能用"),
    ("seg02", "OpenAI 的编程助手"),
    ("seg03", "写代码改代码跑测试都行"),
    ("seg04", "五个渠道，一次讲清楚"),
    ("seg05", "先看全景，五个渠道"),
    ("seg06", "免费零元，最高五百美元"),
    ("seg07", "先看图，再一个一个讲"),
    ("seg08", "先说免费档，零元就能上"),
    ("seg09", "在桌面 App 里就能用"),
    ("seg10", "轻量模型，写点小东西够了"),
    ("seg11", "没有云端任务，额度也少"),
    ("seg12", "灰度开放，有人还看不到"),
    ("seg13", "白嫖党，先从这儿试"),
    ("seg14", "再说 Go，八美元一个月"),
    ("seg15", "还是只有桌面 App"),
    ("seg16", "额度比免费多一点"),
    ("seg17", "没有云端任务，性价比一般"),
    ("seg18", "只能说，凑合着用"),
    ("seg19", "重点来了，Plus 二十美元"),
    ("seg20", "网页命令行 IDE 全开"),
    ("seg21", "自动帮你审代码，还能接 Slack"),
    ("seg22", "手机上也能接着干"),
    ("seg23", "五小时窗口，量大了要续"),
    ("seg24", "普通人，选它最值"),
    ("seg25", "用得狠的，看 Pro"),
    ("seg26", "一百美元起步，分三档"),
    ("seg27", "没五小时限制，随便造"),
    ("seg28", "五百那档，还有极速模式"),
    ("seg29", "每天泡在代码里的，再考虑"),
    ("seg30", "不想订月费，走 API"),
    ("seg31", "用多少，付多少"),
    ("seg32", "输入十美元，输出五十"),
    ("seg33", "没有云端功能，审不了 PR"),
    ("seg34", "适合自己搭工具的人"),
    ("seg35", "五个渠道，都讲完了"),
    ("seg36", "只想试试，免费档就行"),
    ("seg37", "天天写代码，Plus 最值"),
    ("seg38", "靠它吃饭，再看 Pro"),
    ("seg39", "五个渠道，大陆都直连不了"),
    ("seg40", "订阅还得走境外支付"),
    ("seg41", "数据是官网定价，十一月"),
]

out_dir = os.path.expanduser("~/workspace/douyin-ai-video/media/codex03/tts-long")
os.makedirs(out_dir, exist_ok=True)
for name, text in SEGMENTS:
    path = os.path.join(out_dir, f"{name}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"{name} SKIP (exists)", flush=True)
        continue
    n = synth(text, "zh-CN-XiaoxiaoNeural", path, rate="+10%")
    print(f"{name} OK: {n} bytes -> {path}", flush=True)
print("ALL DONE", flush=True)
