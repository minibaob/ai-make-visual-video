# 合成：视频画面 + 旁白（无配乐），方便用户自己叠音乐
# 用法：python voice_only.py <原视频mp4> <旁白mp3> <输出mp4>
import sys, subprocess

FFMPEG = "C:/Users/茱莉蔻/.workbuddy/binaries/python/versions/3.13.12/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

def voice_only(video, voice, out):
    # 0=视频(取画面，丢原音频) 1=旁白
    cmd = [FFMPEG, "-y",
           "-i", video, "-i", voice,
           "-filter_complex",
           "[1:a]volume=1.4,adelay=200|200[a]",
           "-map", "0:v", "-map", "[a]",
           "-c:v", "copy",
           "-c:a", "aac", "-b:a", "160k",
           "-shortest",
           out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR:", r.stderr[-1200:])
        return False
    return True

if __name__ == '__main__':
    video, voice, out = sys.argv[1], sys.argv[2], sys.argv[3]
    ok = voice_only(video, voice, out)
    print("OK" if ok else "FAIL", out)
