#!/usr/bin/env python3
"""Assemble Douyin AI video 04 (20s, 1080x1920): frames -> zoompan segments
-> concat -> TTS + BGM (input-level -stream_loop) -> mixed + silent."""
import os
import subprocess

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "workspace/douyin-ai-video/media/claude04")
FRAMES = os.path.join(BASE, "frames")
SEG_DIR = os.path.join(BASE, "segments")
TTS = os.path.join(BASE, "tts")
BGM = os.path.join(HOME, "workspace/imagine_media/bgm-mixkit.mp3")
OUT_DIR = os.path.join(HOME, "workspace/imagine_media")

DURS = [3, 3, 3, 4, 3, 4]  # 20.0s total
DUR = 20.0
# voiceover offsets (measured TTS durations fit their windows)
VO = [(0.15, 2.088), (3.15, 2.400), (6.15, 2.472),
      (9.15, 2.640), (13.15, 2.592), (16.15, 2.592)]


def run(cmd, label):
    r = subprocess.run(cmd)
    print(f"{label} rc={r.returncode}", flush=True)
    if r.returncode != 0:
        raise SystemExit(f"{label} failed")


# pass 1: each frame -> segment with a gentle 1.00 -> 1.03 Ken Burns zoom
seg_files = []
for i, dur in enumerate(DURS, 1):
    frames = dur * 30
    out = os.path.join(SEG_DIR, f"seg{i}.mp4")
    seg_files.append(out)
    vf = (f"zoompan=z='1+0.03*on/{frames - 1}':x='iw/2-(iw/zoom/2)':"
          f"y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30")
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30",
         "-i", os.path.join(FRAMES, f"frame{i}.png"),
         "-vf", vf, "-frames:v", str(frames),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
         "-crf", "20", "-preset", "medium", out], f"seg{i}")

concat_txt = os.path.join(SEG_DIR, "concat.txt")
with open(concat_txt, "w") as f:
    for p in seg_files:
        f.write(f"file '{p}'\n")
base = os.path.join(SEG_DIR, "base.mp4")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
     "-i", concat_txt, "-c", "copy", base], "concat")

# pass 2: audio (TTS + BGM baked in)
inputs = ["ffmpeg", "-y", "-v", "error", "-i", base]
for i in range(1, 7):
    inputs += ["-i", os.path.join(TTS, f"seg{i}.mp3")]
inputs += ["-stream_loop", "-1", "-i", BGM]

fc = []
for i, (start, _) in enumerate(VO):
    ms = int(start * 1000)
    fc.append(f"[{1 + i}:a]aresample=44100,aformat=channel_layouts=stereo,"
              f"adelay={ms}:all=1[vo{i + 1}]")
vo_mix = "".join(f"[vo{i + 1}]" for i in range(6))
fc.append(f"{vo_mix}amix=inputs=6:duration=longest:normalize=0[vo]")
fc.append(f"[7:a]atrim=0:{DUR},aresample=44100,aformat=channel_layouts=stereo,"
          "volume=0.5,afade=t=out:st=19.0:d=1.0[bgm]")
fc.append("[vo][bgm]amix=inputs=2:duration=longest:normalize=0,"
          "alimiter=limit=0.95[aout]")

mixed = os.path.join(OUT_DIR, "claude-shangche-20s-1080x1920.mp4")
silent = os.path.join(OUT_DIR, "claude-shangche-20s-1080x1920-silent.mp4")
run(inputs + ["-filter_complex", ";".join(fc),
              "-map", "0:v", "-map", "[aout]",
              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
              "-crf", "20", "-preset", "medium",
              "-c:a", "aac", "-b:a", "128k",
              "-t", str(DUR), "-movflags", "+faststart", mixed], "mixed")
run(["ffmpeg", "-y", "-v", "error", "-i", mixed,
     "-c:v", "copy", "-an", silent], "silent")
print("done:", mixed, "|", silent)
