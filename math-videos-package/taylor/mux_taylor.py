#!/usr/bin/env python3
"""Mux Taylor narration segments onto the silent render.
Each segment sits at its 5 s window start (0/5/10/15/20/25).
Video re-encoded to the account spec (H.264 CRF 18 yuv420p, faststart);
audio AAC. Output: taylor-30s-1080x1920-voiced.mp4."""
import subprocess

SILENT = "/home/hatch/workspace/imagine_media/taylor-30s-1080x1920.mp4"
OUT = "/home/hatch/workspace/imagine_media/taylor-30s-1080x1920-voiced.mp4"
SEG = "/home/hatch/workspace/imagine_media/taylor-narration/seg{}.mp3"
STARTS = [0, 5, 10, 15, 20, 25]

inputs = ["ffmpeg", "-y", "-i", SILENT]
for i in range(1, 7):
    inputs += ["-i", SEG.format(i)]
filt = []
for i, st in enumerate(STARTS, 1):
    filt.append(f"[{i}:a]adelay={st * 1000}|{st * 1000}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(1, 7)) +
            "amix=inputs=6:normalize=0[aout]")
cmd = inputs + [
    "-filter_complex", ";".join(filt),
    "-map", "0:v", "-map", "[aout]",
    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k", "-t", "30",
    "-movflags", "+faststart", OUT,
]
print(" ".join(cmd), flush=True)
subprocess.run(cmd, check=True)
print("saved:", OUT, flush=True)
