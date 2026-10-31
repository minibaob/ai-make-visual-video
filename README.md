# 数学可视化短视频生产管线

用 AI + 代码批量生产 3Blue1Brown 风格的数学科普短视频和长视频。从选题 → 动画 → 逐帧截图 → 合成 → 封面，全流程代码化、可复用。

## 已产出的内容

**短视频（17-23 秒，纯画面无音轨）**
- 导数就是切线的斜率
- 为什么微分是「谎言」
- 你被极限的定义骗了整个高中（ε-δ）
- e 为什么是复利之王
- sin 的导数藏在单位圆里
- 为什么放大后曲线变直（局部放大）
- 处处连续却处处不可导（魏尔斯特拉斯分形）
- 任何波形都是一堆正弦波（傅里叶分解）

**长视频（10 分钟）**
- 《微积分到底在解决什么？》——从切线到积分的完整直觉，7 章结构

## 生产管线

```
写选题 HTML（三幕骨架）
  → 逐帧截图（export_capture.js，Playwright 复用系统 Chrome）
  → 合成视频（ffmpeg）
  → 生成封面（cover_polish.html + render_43_covers.js）
```

## 环境依赖

### Node.js
- `playwright`（逐帧截图，复用系统 Chrome，无需下载内核）

```bash
npm install
```

### Python
- `numpy`（生成配乐用，可选）
- `edge-tts`（AI 配音，可选）
- `imageio-ffmpeg`（提供 ffmpeg 二进制，免单独安装）

```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ numpy edge-tts imageio-ffmpeg
```

### ffmpeg
由 `imageio-ffmpeg` 自带，路径见 `build_video.py` 中的 `FFMPEG` 变量。也可使用系统 ffmpeg。

## 核心脚本

| 文件 | 作用 |
|---|---|
| `export_capture.js` | 逐帧截图（`node export_capture.js <html> <帧数> <输出目录>`） |
| `build_video.py` | ffmpeg 合成帧序列 + 混入配乐 |
| `gen_music.py` | 代码生成多情景配乐（悬疑/逼近/生长/圆融） |
| `mix_voice.py` / `voice_only.py` | 混入/剥离旁白 |
| `final_mix.py` | 终版合成（画面+配乐+旁白） |
| `cover_polish.html` | 参数化封面生成器（4:3 横版 + 9:16 竖版） |
| `render_43_covers.js` | 批量渲染封面 |

## 动画文件命名约定

- `topic*.html` — 短视频（17-23 秒，三幕结构）
- `ch*.html` — 长视频章节（40-120 秒）
- `derivative-tangent.html` — 最早的导数动画

每个动画 HTML 内置 `?export=1` 导出模式，配合 `export_capture.js` 逐帧截图。

## 制作规范

见 [制作规范](制作规范.md)，做新片前逐条对照。

## 目录说明

- `export/` — 输出产物（视频、封面），已在 `.gitignore` 排除
- `长视频分镜脚本.md` — 10 分钟长视频的完整分镜 + 旁白文案

## License

MIT
