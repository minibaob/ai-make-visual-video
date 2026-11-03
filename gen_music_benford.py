# 为本福特竖屏视频生成配乐（lo-fi / ambient，80 BPM）
# 用法：python gen_music_benford.py <输出wav> [时长秒]
#
# 结构对齐视频时间轴：
#   0.0 - 3.0   钩子段：只有 pad + 低音，渐入
#   3.0 - 16.4  主体：加琶音与轻鼓，每小节推进
#   4.4 / 8.4 / 12.4  三组数据灌入点，各加一记清脆的叮
#   16.4 - 22.0 收尾：鼓撤掉，pad 长音渐弱
import sys, wave
import numpy as np

SR = 44100
BPM = 80.0
BEAT = 60.0 / BPM          # 0.75s
BAR = BEAT * 4             # 3.0s

# 时间锚点（秒），与视频严格对齐
T_HOOK_END = 3.0
T_DATA = [4.4, 8.4, 12.4]
T_FREEZE = 16.4
T_OUTRO = 18.3


def env_adsr(n, a, d, s_level, r):
    a_n = int(a * SR)
    d_n = int(d * SR)
    r_n = int(r * SR)
    s_n = max(n - a_n - d_n - r_n, 0)
    parts = []
    if a_n > 0:
        parts.append(np.linspace(0, 1, a_n, endpoint=False))
    if d_n > 0:
        parts.append(np.linspace(1, s_level, d_n, endpoint=False))
    if s_n > 0:
        parts.append(np.full(s_n, s_level))
    if r_n > 0:
        parts.append(np.linspace(s_level, 0, r_n))
    e = np.concatenate(parts) if parts else np.array([1.0])
    if len(e) < n:
        e = np.pad(e, (0, n - len(e)))
    return e[:n]


def tone(f, dur, amp=1.0, harmonics=(1.0, 0.3, 0.12), detune=0.0015):
    """带轻微失谐的谐波叠加，模拟温暖的合成音色"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for i, h in enumerate(harmonics):
        if h <= 0:
            continue
        shift = 1.0 + detune * (i + 1)
        x += h * np.sin(2 * np.pi * f * (i + 1) * shift * t)
    return x * amp


def add(buf, start, sig, gain=1.0):
    s = int(start * SR)
    if s >= len(buf):
        return
    e = min(s + len(sig), len(buf))
    buf[s:e] += sig[:e - s] * gain


def kick(dur=0.38, amp=0.55):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 112.0 * np.exp(-t * 17) + 44.0
    phase = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(phase) + 0.25 * np.sin(2 * phase)
    return x * np.exp(-t * 10.5) * amp


def hat(dur=0.07, amp=0.10, seed=7):
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.RandomState(seed)
    noise = np.diff(rng.randn(n + 1))          # 简易高通
    return noise * np.exp(-t * 62) * amp


def ding(f=1046.5, dur=0.75, amp=0.20):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.01 * t) \
        + 0.18 * np.sin(2 * np.pi * f * 3.02 * t)
    return x * np.exp(-t * 5.2) * amp


def reverb(x, taps=((0.031, 0.26), (0.047, 0.19), (0.071, 0.13), (0.113, 0.08))):
    out = x.copy()
    for d, g in taps:
        n = int(d * SR)
        if n < len(x):
            out[n:] += x[:-n] * g
    return out


def build(dur=22.0):
    N = int(dur * SR)
    pad_bus = np.zeros(N)
    arp_bus = np.zeros(N)
    drum_bus = np.zeros(N)
    fx_bus = np.zeros(N)

    # Am7 - Fmaj7 - C - G，七小节走完
    chords = [
        (0.0,  (110.00, 261.63, 329.63, 392.00)),
        (3.0,  ( 87.31, 220.00, 261.63, 329.63)),
        (6.0,  (130.81, 329.63, 392.00, 523.25)),
        (9.0,  ( 98.00, 246.94, 293.66, 392.00)),
        (12.0, (110.00, 261.63, 329.63, 392.00)),
        (15.0, ( 87.31, 220.00, 261.63, 329.63)),
        (18.0, (130.81, 329.63, 392.00, 523.25)),
    ]

    for t0, notes in chords:
        bar_len = min(BAR * 1.35, dur - t0)          # 让相邻和弦叠一点
        if bar_len <= 0:
            continue

        # 段落音量：开头弱、主体满、收尾渐落
        if t0 < T_HOOK_END:
            lvl = 0.55
        elif t0 < T_FREEZE:
            lvl = 1.0
        else:
            lvl = 0.45

        # Pad：慢起慢落
        for i, f in enumerate(notes[1:]):
            dur_p = bar_len
            a = 0.55 + i * 0.06
            sig = tone(f, dur_p, amp=0.175 * lvl, harmonics=(1.0, 0.26, 0.09), detune=0.0022)
            sig *= env_adsr(len(sig), a=a, d=0.5, s_level=0.72, r=1.1)
            add(pad_bus, t0, sig)

        # 低音根音：每半小节一次
        root = notes[0]
        for half in (0.0, BAR * 0.5):
            sig = tone(root, BAR * 0.55, amp=0.27 * lvl, harmonics=(1.0, 0.22), detune=0.001)
            sig *= env_adsr(len(sig), a=0.03, d=0.24, s_level=0.55, r=0.32)
            add(pad_bus, t0 + half, sig)

        # 琶音：八分音符，只在主体段
        if T_HOOK_END <= t0 < T_FREEZE:
            arp_notes = notes[1:] + (notes[1] * 2,)
            step = BEAT / 2
            k = 0
            tt = t0
            while tt < t0 + bar_len - 0.1:
                f = arp_notes[k % len(arp_notes)]
                sig = tone(f, step * 0.95, amp=0.095 * lvl, harmonics=(1.0, 0.18), detune=0.0)
                sig *= env_adsr(len(sig), a=0.008, d=0.16, s_level=0.25, r=0.42)
                add(arp_bus, tt, sig)
                tt += step
                k += 1

    # 鼓：3.0s 起，到定格前收
    tt = T_HOOK_END
    bar_i = 0
    while tt < T_FREEZE:
        # kick 在一、三拍
        add(drum_bus, tt, kick(amp=0.34), 1.0)
        add(drum_bus, tt + BEAT * 2, kick(amp=0.28), 1.0)
        # hihat 走八分
        for j in range(8):
            h = hat(amp=0.062 if j % 2 == 0 else 0.040, seed=11 + j)
            add(drum_bus, tt + j * BEAT / 2, h, 1.0)
        tt += BAR
        bar_i += 1

    # 数据灌入点：一记叮 + 极轻的低频撞击
    for i, td in enumerate(T_DATA):
        add(fx_bus, td, ding(f=880.0 * (2 ** (i / 12.0)) * 1.5, amp=0.17))

    # 结尾：一记柔和的下行音，收束
    add(fx_bus, T_OUTRO, ding(f=523.25, dur=1.4, amp=0.15))
    add(fx_bus, T_OUTRO + 0.18, ding(f=392.00, dur=1.6, amp=0.11))

    # 混音
    pad_bus = reverb(pad_bus, taps=((0.041, 0.30), (0.067, 0.21), (0.103, 0.13)))
    arp_bus = reverb(arp_bus, taps=((0.037, 0.22), (0.059, 0.14)))
    fx_bus = reverb(fx_bus, taps=((0.053, 0.28), (0.089, 0.17)))

    mix = pad_bus * 1.0 + arp_bus * 0.9 + drum_bus * 0.85 + fx_bus * 1.0

    # 整体包络：0.6s 淡入，最后 3s 淡出
    n_in = int(0.6 * SR)
    mix[:n_in] *= np.linspace(0, 1, n_in)
    n_out = int(3.0 * SR)
    if n_out < len(mix):
        mix[-n_out:] *= np.linspace(1, 0, n_out) ** 1.6

    # 柔和限幅 + 归一化
    mix = np.tanh(mix * 1.15) * 0.92
    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.72
    return mix


def stereo(x):
    n = len(x)
    st = np.zeros((n, 2))
    st[:, 0] = x
    st[:, 1] = np.roll(x, int(0.0075 * SR)) * 0.96
    # 轻微左右差，避免完全单声道
    st[:, 0] *= 1.0
    st[:, 1] *= 1.0
    return (np.clip(st, -1, 1) * 32767).astype(np.int16)


if __name__ == '__main__':
    path = sys.argv[1]
    dur = float(sys.argv[2]) if len(sys.argv) > 2 else 22.0
    audio = build(dur)
    pcm = stereo(audio)
    with wave.open(path, 'w') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"written: {path} ({dur}s, {BPM:.0f} BPM)")
