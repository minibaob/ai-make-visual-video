# 通用：合成帧序列 + 混入配乐 -> 最终 MP4
# 用法：python build_video.py <帧目录> <输出mp4> <bgm.wav> [bgm音量]
import sys, subprocess, os

FFMPEG = "C:/Users/茱莉蔻/.workbuddy/binaries/python/versions/3.13.12/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

def build(frames_dir, out_mp4, bgm, bgm_vol=0.22):
    pattern = os.path.join(frames_dir, "frame_%04d.png")
    # 视频
    vf = ["-framerate", "30", "-i", pattern]
    # 音频（循环 bgm，音量调低，fade out）
    audio = ["-stream_loop", "-1", "-i", bgm]
    cmd = [FFMPEG, "-y", *vf, *audio,
           "-filter_complex",
           f"[1:a]volume={bgm_vol},afade=t=out:st=14:d=3[a]",
           "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
           "-c:a", "aac", "-b:a", "128k", "-shortest",
           out_mp4]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:", r.stderr[-1500:])
        return False
    return True

if __name__ == '__main__':
    frames_dir, out_mp4, bgm = sys.argv[1], sys.argv[2], sys.argv[3]
    vol = float(sys.argv[4]) if len(sys.argv) > 4 else 0.22
    ok = build(frames_dir, out_mp4, bgm, vol)
    print("OK" if ok else "FAIL", out_mp4)
    if ok:
        print(os.path.getsize(out_mp4), "bytes")
