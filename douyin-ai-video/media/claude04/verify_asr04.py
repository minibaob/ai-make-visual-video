import subprocess, numpy as np
from faster_whisper import WhisperModel
mp4 = "/home/hatch/workspace/imagine_media/claude-shangche-20s-1080x1920.mp4"
raw = subprocess.run(["ffmpeg","-v","error","-i",mp4,"-vn","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768.0
model = WhisperModel("base", device="cpu", compute_type="int8")
segs, _ = model.transcribe(pcm, language="zh", beam_size=5, word_timestamps=True)
lines = list(segs)
for s in lines:
    print(f"{s.start:5.2f}-{s.end:5.2f}  {s.text.strip()}")
    for w in (s.words or []):
        pass
