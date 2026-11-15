#!/usr/bin/env python3
"""Earth belt problem narration via raw_edge_tts (the working route on this VM).
Voice zh-CN-XiaoxiaoNeural, rate +10%. Segments kept short so each fits its
4s window (Xiaoxiao at +10% speaks ~4.3 chars/s, so <=18 chars per segment).
Math EXACT: C' - C = 2*pi*(r+1) - 2*pi*r = 2*pi = 6.283185... m -> 6.28 m;
the radius cancels, independent of Earth's size (r = 6371 km).
Retry note (2026-11-15): the edge-tts service drops connections
intermittently ("socket closed while reading"), so each segment retries
up to 5 times with backoff; already-generated segments are skipped."""
import os
import sys
import time

sys.path.insert(0, os.path.expanduser("~/workspace/imagine_media"))
from raw_edge_tts import synth

SEGMENTS = [
    "给地球系根腰带，离地一米。",
    "绳子要加长多少？",
    "只要六点二八米。",
    "和地球多大，没关系。",
    "周长差，就是二π。",
]

VOICE = "zh-CN-XiaoxiaoNeural"
OUT = os.path.expanduser("~/workspace/imagine_media/earthbelt-narration")
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
    assert len(text) <= 18, f"seg{i} too long: {len(text)} chars"
    gen(i, text)
print("all segments done")
