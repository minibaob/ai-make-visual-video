# 终版合成：视频画面 + 情景配乐 + 钩子旁白
# 用法：python final_mix.py <原视频mp4> <情景bgm.wav> <旁白mp3> <输出mp4>
import sys, subprocess

FFMPEG = "C:/Users/茱莉蔻/.workbuddy/binaries/python/versions/3.13.12/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

def final_mix(video, bgm, voice, out):
    # 0=视频(取画面，丢弃原音频) 1=bgm 2=旁白
    cmd = [FFMPEG, "-y",
           "-i", video, "-i", bgm, "-i", voice,
           "-filter_complex",
           "[1:a]volume=0.55,afade=t=out:st=14:d=3[bgm];"      # 情景配乐音量+淡出
           "[2:a]volume=1.4,adelay=200|200[vo];"                # 旁白放大+延迟
           "[bgm][vo]amix=inputs=2:duration=first:dropout_transition=0[a]",
           "-map", "0:v", "-map", "[a]",
           "-c:v", "copy",
           "-c:a", "aac", "-b:a", "160k",
           "-shortest",
           out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("MIX ERROR:", r.stderr[-1500:])
        return False
    return True

if __name__ == '__main__':
    video, bgm, voice, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    ok = final_mix(video, bgm, voice, out)
    print("OK" if ok else "FAIL", out)
