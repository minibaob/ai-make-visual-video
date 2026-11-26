"""Build src/timeline.ts for the Codex long animated video from measured TTS durations.

Reads media/codex03/tts-long/segNN.mp3 durations via ffprobe, lays out
8 scenes (hook / overview / 5 channels / summary) and emits timeline.ts
with frame-accurate line starts/ends. Run after TTS generation finishes.
"""
import json
import math
import os
import subprocess

FPS = 30
GAP = 12        # frames between lines
LEAD = 12       # frames of card entrance before first line of a scene
TRAIL = 18      # frames held after last line of a scene
HOME = os.path.expanduser("~")
TTS_DIR = os.path.join(HOME, "workspace/douyin-ai-video/media/codex03/tts-long")
OUT = os.path.join(HOME, "workspace/douyin-ai-video/codex-long-remotion/src/timeline.ts")

LINES = [
    # (seg, text, scene)
    ("seg01", "Codex 上车，零元就能用", "hook"),
    ("seg02", "OpenAI 的编程助手", "hook"),
    ("seg03", "写代码改代码跑测试都行", "hook"),
    ("seg04", "五个渠道，一次讲清楚", "hook"),
    ("seg05", "先看全景，五个渠道", "overview"),
    ("seg06", "免费零元，最高五百美元", "overview"),
    ("seg07", "先看图，再一个一个讲", "overview"),
    ("seg08", "先说免费档，零元就能上", "free"),
    ("seg09", "在桌面 App 里就能用", "free"),
    ("seg10", "轻量模型，写点小东西够了", "free"),
    ("seg11", "没有云端任务，额度也少", "free"),
    ("seg12", "灰度开放，有人还看不到", "free"),
    ("seg13", "白嫖党，先从这儿试", "free"),
    ("seg14", "再说 Go，八美元一个月", "go"),
    ("seg15", "还是只有桌面 App", "go"),
    ("seg16", "额度比免费多一点", "go"),
    ("seg17", "没有云端任务，性价比一般", "go"),
    ("seg18", "只能说，凑合着用", "go"),
    ("seg19", "重点来了，Plus 二十美元", "plus"),
    ("seg20", "网页命令行 IDE 全开", "plus"),
    ("seg21", "自动帮你审代码，还能接 Slack", "plus"),
    ("seg22", "手机上也能接着干", "plus"),
    ("seg23", "五小时窗口，量大了要续", "plus"),
    ("seg24", "普通人，选它最值", "plus"),
    ("seg25", "用得狠的，看 Pro", "pro"),
    ("seg26", "一百美元起步，分三档", "pro"),
    ("seg27", "没五小时限制，随便造", "pro"),
    ("seg28", "五百那档，还有极速模式", "pro"),
    ("seg29", "每天泡在代码里的，再考虑", "pro"),
    ("seg30", "不想订月费，走 API", "api"),
    ("seg31", "用多少，付多少", "api"),
    ("seg32", "输入十美元，输出五十", "api"),
    ("seg33", "没有云端功能，审不了 PR", "api"),
    ("seg34", "适合自己搭工具的人", "api"),
    ("seg35", "五个渠道，都讲完了", "summary"),
    ("seg36", "只想试试，免费档就行", "summary"),
    ("seg37", "天天写代码，Plus 最值", "summary"),
    ("seg38", "靠它吃饭，再看 Pro", "summary"),
    ("seg39", "五个渠道，大陆都直连不了", "summary"),
    ("seg40", "订阅还得走境外支付", "summary"),
    ("seg41", "数据是官网定价，十一月", "summary"),
]

SCENE_ORDER = ["hook", "overview", "free", "go", "plus", "pro", "api", "summary"]
SCENE_TITLES = {
    "hook": "开场",
    "overview": "总览",
    "free": "免费档",
    "go": "Go",
    "plus": "Plus",
    "pro": "Pro",
    "api": "API 按量",
    "summary": "汇总",
}

# Static card data per channel scene.
CHANNELS = {
    "free": {
        "index": "01", "name": "免费档", "en": "Free",
        "price": "$0", "priceSub": "0 元",
        "bullets": ["桌面 App 里轻量用", "GPT-6 Luna 标准速度", "没有云端任务，额度也少"],
        "verdict": "能上",
        "chip": "已有 ChatGPT 账号直接试",
        "clip": {"file": "5UlRL_ImvQ0.mp4", "from": 8.0, "to": 11.3},
    },
    "go": {
        "index": "02", "name": "Go", "en": "Go",
        "price": "$8", "priceSub": "约 53 元 / 月",
        "bullets": ["桌面 App，GPT-6 Luna", "额度比免费多一点", "没有云端任务"],
        "verdict": "凑合",
        "chip": "只比免费多一点额度",
        "clip": {"file": "y5hogSW2mqU.mp4", "from": 58.0, "to": 62.0},
    },
    "plus": {
        "index": "03", "name": "Plus", "en": "Plus",
        "price": "$20", "priceSub": "约 133 元 / 月",
        "bullets": ["网页 + CLI + IDE + iOS 全开", "自动审 PR，Slack 集成", "5 小时窗口，量大了要续"],
        "verdict": "最值",
        "chip": "已有 Plus 等于白得",
        "clip": {"file": "codex-app-intro.mp4", "from": 29.0, "to": 32.5},
    },
    "pro": {
        "index": "04", "name": "Pro", "en": "Pro",
        "price": "$100", "priceSub": "约 666 元 / 月起",
        "bullets": ["Plus 全部 + 更高额度", "没 5 小时限制", "$500 档独有极速模式"],
        "verdict": "重度",
        "chip": "重度用户再考虑",
        "clip": {"file": "codex-app-intro.mp4", "from": 178.0, "to": 181.0},
    },
    "api": {
        "index": "05", "name": "API 按量", "en": "API",
        "price": "按量", "priceSub": "用多少付多少",
        "bullets": ["GPT-6 Astra 按量计费", "输入 $10 / 输出 $50 每百万 token", "无云端功能，审不了 PR"],
        "verdict": "灵活",
        "chip": "不订阅也能用",
        "clip": {"file": "5UlRL_ImvQ0.mp4", "from": 15.0, "to": 18.2},
    },
}

OVERVIEW_BARS = [
    {"label": "免费档", "price": "$0", "value": 0, "highlight": False},
    {"label": "Go", "price": "$8", "value": 8, "highlight": False},
    {"label": "Plus", "price": "$20", "value": 20, "highlight": True},
    {"label": "Pro", "price": "$100 起", "value": 100, "highlight": False},
    {"label": "API", "price": "按量", "value": 10, "highlight": False},
]

SUMMARY_ROWS = [
    {"name": "免费档", "price": "$0", "one": "先试试水，零元上车", "verdict": "能上"},
    {"name": "Go", "price": "$8 / 月", "one": "额度多一点，依然凑合", "verdict": "凑合"},
    {"name": "Plus", "price": "$20 / 月", "one": "普通人最值", "verdict": "最值"},
    {"name": "Pro", "price": "$100 起 / 月", "one": "靠它吃饭再考虑", "verdict": "重度"},
    {"name": "API 按量", "price": "按 token", "one": "不想订阅，按量付", "verdict": "灵活"},
]


def probe_dur(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path,
    ]).decode().strip()
    return float(out)


def ts_str(v):
    return json.dumps(v, ensure_ascii=False, indent=2)


def main():
    # Measure every TTS segment.
    durs = {}
    for seg, _text, _scene in LINES:
        p = os.path.join(TTS_DIR, f"{seg}.mp3")
        if not os.path.exists(p):
            raise SystemExit(f"missing TTS file: {p}")
        durs[seg] = probe_dur(p)
    total_voice = sum(durs.values())
    print(f"voice total: {total_voice:.1f}s over {len(LINES)} lines")

    # Lay out frames scene by scene.
    lines_out = []
    scenes_out = []
    frame = 0
    by_scene = {s: [] for s in SCENE_ORDER}
    for seg, text, scene in LINES:
        by_scene[scene].append((seg, text))
    for si, scene in enumerate(SCENE_ORDER):
        s_start = frame
        frame += LEAD
        for li, (seg, text) in enumerate(by_scene[scene]):
            dur_f = int(math.ceil(durs[seg] * FPS)) + 3  # +0.1s breathing room
            lines_out.append({
                "id": seg, "text": text, "scene": scene,
                "start": frame, "end": frame + dur_f,
            })
            frame += dur_f
            if li < len(by_scene[scene]) - 1:
                frame += GAP
        frame += TRAIL
        s_end = frame
        sc = {"id": scene, "kind": scene, "title": SCENE_TITLES[scene],
              "num": si + 1, "start": s_start, "end": s_end}
        if scene in CHANNELS:
            sc["card"] = CHANNELS[scene]
        scenes_out.append(sc)
    total_frames = frame
    print(f"total: {total_frames} frames = {total_frames / FPS:.1f}s")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("export const FPS = 30;\n\n")
        f.write(f"export const TOTAL_FRAMES = {total_frames};\n\n")
        f.write(f"export const LINES = {ts_str(lines_out)};\n\n")
        f.write(f"export const SCENES = {ts_str(scenes_out)};\n\n")
        f.write(f"export const OVERVIEW_BARS = {ts_str(OVERVIEW_BARS)};\n\n")
        f.write(f"export const SUMMARY_ROWS = {ts_str(SUMMARY_ROWS)};\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
