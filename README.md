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

**竖屏短视频（1080×1920，抖音向，2026-11 起）**

| 文件 | 选题 | 时长 |
|---|---|---|
| `topic1_lie_v.mp4` | 微分的谎言（竖屏版） | 17s |
| `topic8_pi_v.mp4` | π 藏在弹珠碰撞里 | 20s |
| `topic9_benford_v.mp4` | 本福特定律：1 占了 30% | 22s |
| `topic9_benford_v_music.mp4` | 同上，带配乐 | 22s |

## 快速开始（开箱即用）

### 方式一：可视化配置台（推荐，无需记命令）

```bash
npm run config
# 或 node server.js
```

浏览器打开 `http://localhost:3000`，可视化选择选题、调参数、一键渲染视频和封面。

### 方式二：命令行 CLI

```bash
node cli.js list          # 列出所有选题
node cli.js render lie    # 渲染单个视频
node cli.js cover lie     # 生成封面
node cli.js music lie     # 生成配乐
node cli.js video lie     # 渲染+封面一条龙
node cli.js all           # 渲染所有短视频+生成所有封面
node cli.js init          # 检查环境依赖
node cli.js prompt "正态分布为什么无处不在" --type short   # 生成新选题提示词
```

### 生成全新选题

工具不会只局限在现有的 8 个动画。输入一个主题，生成一份「动画制作提示词」，拿着它交给任意大模型（如 DSH）产出 HTML 动画，放回项目目录即可渲染成片：

```
你 → 输入主题 → 工具生成提示词 → 发给 AI → AI 产出 HTML → 放入项目 → render 出片
```

```bash
# 短视频
node cli.js prompt "正态分布为什么无处不在" --type short

# 长视频章节
node cli.js prompt "中心极限定理" --type chapter --duration 90 --notes "用掷硬币演示"

# 配置台里也有「提示词生成器」卡片，可视化输入
```

生成的提示词会自动包含项目的全部技术规范（三幕结构、确定性帧驱动、配色、坐标轴刻度、导出模式），确保 AI 产出的 HTML 能直接接入截图→合成管线。

## 生产管线

```
写选题 HTML（三幕骨架）
  → 逐帧截图（export_capture.js，Playwright 复用系统 Chrome）
  → 合成视频（ffmpeg，自动探测路径）
  → 生成封面（cover_polish.html + render_43_covers.js）
```

CLI 工具（`cli.js`）把这些步骤串成一条命令；配置台（`server.js` + `config.html`）提供可视化界面。ffmpeg 路径自动探测（环境变量 → imageio-ffmpeg 包 → 系统 PATH），无需手动配置。

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
| `cli.js` | CLI 统一入口（list/render/cover/music/video/all/init/prompt） |
| `server.js` + `config.html` | 本地 Web 配置台 |
| `config.json` | 集中配置（选题列表、分辨率、封面尺寸等） |
| `lib/ffmpeg.js` | ffmpeg 路径自动探测 |
| `lib/prompt.js` | 新选题提示词生成器 |
| `export_capture.js` | 逐帧截图（写死 1920×1080，横屏用） |
| `tools/capture_any.js` | 逐帧截图（可指定宽高，竖屏用这个） |
| `tools/preview_v2.js` | 竖屏抽帧预览（1080×1920） |
| `build_video.py` | ffmpeg 合成帧序列 + 混入配乐 |
| `gen_music.py` | 代码生成多情景配乐（悬疑/逼近/生长/圆融） |
| `gen_music_benford.py` | 本福特专用配乐（80 BPM lo-fi，段落对齐时间轴） |
| `mix_voice.py` / `voice_only.py` | 混入/剥离旁白 |
| `final_mix.py` | 终版合成（画面+配乐+旁白） |
| `cover_polish.html` | 参数化封面生成器（4:3 横版 + 9:16 竖版） |
| `render_43_covers.js` | 批量渲染封面 |
| `cover_pi_v.html` / `cover_benford_v.html` | 竖版封面（1080×1920） |
| `cover_pi_h.html` / `cover_benford_h.html` | 横版封面（1440×1080，4:3） |
| `tools/render_pi_cover.js` / `render_benford_cover.js` | 渲染竖版封面 |
| `tools/render_h_covers.js` | 批量渲染横版封面 |

## 动画文件命名约定

- `topic*.html` — 短视频（17-23 秒，三幕结构）
- `ch*.html` — 长视频章节（40-120 秒）
- `derivative-tangent.html` — 最早的导数动画

每个动画 HTML 内置 `?export=1` 导出模式，配合 `export_capture.js` 逐帧截图。

## 制作规范

见 [制作规范](制作规范.md)，做新片前逐条对照。

### 排版字号（现行）

- **左上角文字一律采用现行字号**：没有特殊要求时，顶部标题 **42px**、状态行 **28px**（1080p 基准）。旧的 34 / 24 自 2026-11-01 起作废。
- 需要调大调小时，把整条字号阶梯统一定向上移或下移档位，**不要对单个元素单独改 px**，否则同一帧内的层级关系会乱。
- 字号放大后若两行显得挤压，只下移副标题 `y` 坐标补偿（如 138 → 150），不要回调字号。
- 现行阶梯：`11 / 13 / 14 / 15 / 16 / 17 / 18 / 20 / 22 / 24 / 26 / 28 / 30 / 34 / 40 / 42 / 44 / 46 / 48 / 50 / 52 / 56 / 60`

### 输出与平台（2026-11-01 起）

**主战场是抖音，默认出 9:16 竖屏 1080×1920。** 横屏 1920×1080 只作存档与 B 站分发。

- 底部预留 380px、顶部预留 240px 安全区，避开抖音字幕和按钮栏
- 开场第 0 帧就必须在动，**不要黑屏文字卡**（实测 2s 跳出率 54% 的头号原因）
- 逐帧截图用 `node tools/capture_any.js <html> <帧数> <目录> <宽> <高>`
- 竖屏样片参考：`topic1_lie_v.html`（正方形绘图区，避免 x/y 比例失真）

## 目录说明

- `export/` — 输出产物（视频、封面），已在 `.gitignore` 排除
- `长视频分镜脚本.md` — 10 分钟长视频的完整分镜 + 旁白文案

## License

MIT
