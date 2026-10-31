# 把钩子旁白混入视频（旁白在开头，叠加在原有 BGM 上）
# 用法：python mix_voice.py <视频mp4> <旁白mp3> <输出mp4>
import sys, subprocess

FFMPEG = "C:/Users/茱莉蔻/.workbuddy/binaries/python/versions/3.13.12/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

def mix(video, voice, out):
    # 输入：0=视频（含bgm），1=旁白
    # 旁白音量调到 1.2，从 0 开始；视频原音频保留；用 amix 混合
    cmd = [FFMPEG, "-y", "-i", video, "-i", voice,
           "-filter_complex",
           "[1:a]volume=1.4,adelay=200|200[vo];"    # 旁白放大 + 延迟200ms
           "[0:a][vo]amix=inputs=2:duration=first:dropout_transition=0[a]",
           "-map", "0:v", "-map", "[a]",
           "-c:v", "copy",
           "-c:a", "aac", "-b:a", "160k",
           out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("MIX ERROR:", r.stderr[-1200:])
        return False
    return True

if __name__ == '__main__':
    video, voice, out = sys.argv[1], sys.argv[2], sys.argv[3]
    ok = mix(video, voice, out)
    print("OK" if ok else "FAIL", out)
