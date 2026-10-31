# 生成多情景配乐：每种情绪基调不同
# 用法：python gen_music.py <输出wav> <时长秒> <情景名>
# 情景：lie(悬疑) limit(逼近) e(复利生长) sin(圆融流动) generic(通用)
import sys, math, wave
import numpy as np

SR = 44100

def env_adsr(tt, dur, a=0.05, r=0.6):
    e = np.minimum(tt/a, 1.0) * np.minimum((dur-tt)/r, 1.0)
    return np.clip(e, 0, 1)

def add_tone(audio, start, dur, freq, amp, harmonics=(1.0,), detune=0.0):
    n = int(dur*SR)
    tt = np.arange(n)/SR
    seg = np.zeros(n)
    for i,h in enumerate(harmonics):
        if h==0: continue
        seg += amp*h*np.sin(2*np.pi*freq*(i+1)*tt + detune)
    e = env_adsr(tt, dur)
    seg *= e
    s = int(start*SR)
    e_end = min(s+n, len(audio))
    audio[s:e_end] += seg[:e_end-s]

def norm(audio, peak=0.3):
    m = np.max(np.abs(audio))
    if m>0: audio = audio/m*peak
    return audio

def gen_lie(dur):
    # 悬疑：Am 小调，缓慢，带增四度不协和
    audio = np.zeros(int(dur*SR))
    add_tone(audio, 0, dur, 55.0, 0.5, harmonics=(1,0.3,0.1))
    chord = [220.0, 311.13]  # A3 和 D#4（三全音，不协和）
    seg_len = 3.0
    for t in np.arange(0, dur, seg_len):
        for f in chord:
            add_tone(audio, t, seg_len, f, 0.22, harmonics=(1,0.2))
    add_tone(audio, 2.0, 1.5, 880.0, 0.10)
    add_tone(audio, 8.0, 2.0, 987.77, 0.08)
    return norm(audio)

def gen_limit(dur):
    # 逼近：稳定脉冲节奏，音程逐渐收窄
    audio = np.zeros(int(dur*SR))
    beat = 60/78.0
    for i in range(int(dur/beat)):
        t = i*beat
        add_tone(audio, t, 0.15, 50.0, 0.5, harmonics=(1,))
    C = [261.63, 329.63, 392.0]
    seg = 4.0
    for t in np.arange(0, dur, seg):
        for f in C:
            add_tone(audio, t, seg, f, 0.15, harmonics=(1,0.15))
    for i, t in enumerate(np.arange(0, dur, 2.0)):
        ratio = 1 - i/(dur/2.0)
        f2 = 440 * (1 + 0.06*max(ratio,0))
        add_tone(audio, t, 1.0, 440.0, 0.12)
        add_tone(audio, t, 1.0, f2, 0.12)
    return norm(audio)

def gen_e(dur):
    # 复利生长：大调上行琶音，渐强
    audio = np.zeros(int(dur*SR))
    arp = [261.63, 329.63, 392.0, 523.25]
    step = 0.8
    n_steps = int(dur/step)
    for i in range(n_steps):
        t = i*step
        oct_shift = min(i//8, 2) * 2
        f = arp[i % 4] * (2**oct_shift)
        vol = 0.10 + 0.20*(i/n_steps)
        add_tone(audio, t, step*0.9, f, vol, harmonics=(1,0.3))
    add_tone(audio, 0, dur, 130.81, 0.3, harmonics=(1,0.2))
    return norm(audio)

def gen_sin(dur):
    # 圆融流动：匀速循环和弦，柔和
    audio = np.zeros(int(dur*SR))
    chords = [
        [261.63, 329.63, 392.0],
        [196.0, 246.94, 392.0],
        [220.0, 261.63, 329.63],
        [174.61, 220.0, 261.63],
    ]
    seg = 4.25
    for i, t in enumerate(np.arange(0, dur, seg)):
        for f in chords[i % 4]:
            add_tone(audio, t, seg, f, 0.18, harmonics=(1,0.25,0.1))
    beat = 60/72.0
    for i in range(int(dur/beat)):
        add_tone(audio, i*beat, 0.3, 1046.5, 0.06, harmonics=(1,))
    return norm(audio)

def gen_generic(dur):
    audio = np.zeros(int(dur*SR))
    chords = [[110,164.81,220],[87.31,130.81,174.61],[130.81,164.81,196],[98,146.83,196]]
    seg = 60/76.0*8
    for ci,ch in enumerate(chords):
        t = ci*seg
        if t>=dur: break
        for f in ch:
            add_tone(audio, t, min(seg,dur-t), f, 0.28, harmonics=(1,0.15))
    return norm(audio)

GEN = {'lie':gen_lie,'limit':gen_limit,'e':gen_e,'sin':gen_sin,'generic':gen_generic}

def stereo(audio):
    n = len(audio)
    L = audio
    R = np.roll(audio, int(0.006*SR))
    st = np.zeros((n,2))
    st[:,0]=L; st[:,1]=R
    return (st*32767).astype(np.int16)

if __name__=='__main__':
    path = sys.argv[1]
    dur = float(sys.argv[2])
    style = sys.argv[3] if len(sys.argv)>3 else 'generic'
    a = GEN.get(style, gen_generic)(dur)
    pcm = stereo(a)
    with wave.open(path,'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"music({style}) written: {path} ({dur}s)")
