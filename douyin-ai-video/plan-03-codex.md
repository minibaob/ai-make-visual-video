# 抖音 AI 视频 03 号计划：Codex 上车全渠道合集

> 账号：小影数学（07050908kkk），AI 视频是新线，和数学内容并存。
> 系列：AI 工具“能上车的全渠道合集”，每期一个工具。参考阿星《ClaudeCode能上车的全渠道合集》的公式（合集盘点 + 逐个一句话 verdict + 汇总），形式按本账号规矩来：~20 秒竖版、真实素材 + 烧录大字幕 + 配音，一期只讲 3–4 个渠道，钩子开头先给结论。阿星原片是 6 分 14 秒动画信息图，不照搬。
> 五个工具的完整调研见 research-03-five-tools.md。本期是系列第 1 期（用户点名顺序 Codex 在先）。
> 状态：**成片已剪完（2026-11-26）**，待发布。混音版 ~/workspace/imagine_media/codex-shangche-20s-1080x1920.mp4（19.6s，1080×1920，h264+aac）、静音版 -silent.mp4、封面 codex-shangche-cover-1080x1920.png；构建脚本 build_video03.py + build_video03_pass2.py，封面 gen_cover03.py。
> 分镜执行时三处调整（已逐帧核对）：① 钩子不用 5UlRL 0–3.2s（0–2.3s 是白底 "With Codex"，紫色块 2.3s 才入画），改用 2.5–5.7s，第一帧即紫色开场；② Plus 段不用 app-intro 28–31.5s（28s 还是 AstroScope 界面），改用 29–32.5s，全程手机+桌面同屏；③ app-intro 两段（29–32.5s、178–181s）右上角都有官方演示自带的小窗真人（计划引用的 app-30/app-180 预览帧里就有），红字印章改放在画面上方右角（y=520），不压在真人小窗上；来源行加了深色底衬，浅色背景上也可读。

## 事实（已核实，2026-11-26 查）

| 事实 | 数值 | 来源 |
|---|---|---|
| Codex 没有单独售价 | 包含在 ChatGPT 订阅里 | OpenAI 官网 openai.com/codex 原话 "Codex is included in your ChatGPT plan"（2026-11-26 已读，一级来源） |
| 免费档 Free | $0，桌面 App，GPT-6 Luna 标准速度，轻量，灰度开放 | OpenAI 官网定价页，经 layer3labs / faros.ai / vdf.ai / devhunt 四家比价文交叉核对（最新核对 2026-11-24，数字一致） |
| Plus | $20/月，约 133 元 | 同上；含网页 + CLI + IDE 插件 + iOS，GPT-6.1 Sol/Luna，自动审 PR、Slack 集成；5 小时窗口限量，可买 credits 续 |
| Pro | $100/$200/$500/月，约 666/1332/3330 元 | 同上；目前无 5 小时限制；$500 档独有 Ultrafast 模式 |
| API 按量 | GPT-6 Astra $10 输入 / $50 输出 每百万 token；无云端功能（无 GitHub 审 PR） | faros.ai / layer3labs 引 OpenAI API 定价页 |
| 国内直接能用吗 | 不能直连 | OpenAI 官方支持名单 208 国无中国大陆/港澳；帮助中心称名单外使用可能封号；chatgpt.com 大陆直连打不开（proxy302 2026-11-06 比对官方名单；ipjudge/sunsetbrowser 2026-10 核查） |
| 汇率 | 1 美元 ≈ 6.66 元（2026-11-26） | XE/Finnhub 中间价 6.663–6.672 |

**一句话讲清的事实：** Codex 不用单买，跟 ChatGPT 订阅走——0 元免费档就能上，Plus 20 美元（约 133 元）开全渠道，Pro 100 美元（约 666 元）起、没 5 小时限制，不想订阅就走 API 按量付。

**本期不讲的：** Go $8 档（只有桌面 App、GPT-6 Luna，介于免费和 Plus 之间，20 秒塞不下，见研究文件）；12 月起 Plus/Pro/Business 共享额度的新规（faros 称已宣布，视频里不提，免得说错）；第三方代充/绕过地区限制的方法（只说“国内直连用不了”，不展开）。

## 素材（真实视频，已下载到本地）

| 素材 | 内容 | 来源 | 授权/说明 |
|---|---|---|---|
| `media/codex03/codex-app-intro.mp4` | OpenAI 官方《Introducing the Codex app》（HFM3se4lNiw），261 秒，640×360，含音频 | OpenAI 官方 YouTube（developers.openai.com 视频页链接） | OpenAI 官方发布素材，新闻/评测转载用；片尾注明“画面：OpenAI 官方演示”；前 ~10 秒是真人出镜开场，剪辑时避开，只用 UI 段 |
| `media/codex03/5UlRL_ImvQ0.mp4` | OpenAI 官方《Build and share apps in Codex》，46.5 秒，640×360 | OpenAI 官方 YouTube | 最干净的一条：全是产品 UI/动效，无真人出镜；主 B-roll 用这条 |
| `media/codex03/y5hogSW2mqU.mp4` | OpenAI 官方《Prep for sales meetings faster with Codex》，212.6 秒，640×360 | OpenAI 官方 YouTube | 备用 B-roll |
| `media/codex03/fK_bm84N7bs.mp4` | OpenAI 官方《Build beautiful frontends with OpenAI Codex》，509 秒，640×360 | OpenAI 官方 YouTube | 备用；含真人出镜段，慎用 |
| `bgm-mixkit.mp3` | Mixkit《Smile》，音量 0.5 | 已有文件（01、02 号用过） | Mixkit 免费音乐 |

- 下载方式：yt-dlp + `--extractor-args "youtube:player_client=android"`（本机出口直连 YouTube 限流 429 + 机器人验证，默认客户端下不到，android 客户端可绕过；720p 分离流拿不到，只有 360p format 18）。
- **画质注意：素材只有 640×360，竖版放大后偏软——按 02 号做法用模糊背景 + 16:9 实拍居中，抽帧验清晰度；不要全屏硬拉。**
- 预览抽帧在 `media/preview/`（app-*.png、apps-*.png），分镜时段已按抽帧核对，剪辑时再逐段看一遍确认。

## 分镜（竖版 1080×1920，约 20 秒，真实镜头剪辑）

版式：模糊背景填满 1080×1920（原片高斯模糊+压暗），16:9 实拍居中（1080×607），上方放大字、下方字幕——02 号同款做法。
字幕克制：每段一句白字+半透明黑底，只在画面下方出现；大字只在钩子（0 元）和结尾 verdict 处出现；红字印章式 verdict（能上/最值/重度/灵活）放在每段画面右上角，小字。

| 时间 | 画面（实拍，来源文件 + 时段） | 屏上字 | 口播 |
|---|---|---|---|
| 0–3.2 秒 | 5UlRL 0–3.2s：紫色品牌开场 | 大字 0 元上车（黄）+ Codex 全渠道（白） | S1 |
| 3.2–6.5 秒 | 5UlRL 8–11.5s：Event Operations / Sites 工作流界面（抽帧 apps-10.png 附近） | 免费 $0 / 桌面 App 轻量尝鲜；印章：能上 | S2 |
| 6.5–10 秒 | codex-app-intro 28–31.5s：桌面端 + 手机端同屏 UI（抽帧 app-30.png 附近） | Plus $20/月 ≈ ¥133 / 网页+CLI+IDE；印章：最值 | S3 |
| 10–13 秒 | codex-app-intro 178–181s：Today's Progress 任务板（抽帧 app-180.png 附近） | Pro $100/月 ≈ ¥666 / 没 5 小时限制；印章：重度 | S4 |
| 13–16.2 秒 | 5UlRL 15–18.2s："Sites — Build a KPI dashboard" 输入框（抽帧 apps-17.png 附近） | API 按量 / Astra $10/$50 每百万 token；印章：灵活 | S5 |
| 16.2–19.6 秒 | 5UlRL 36–39.4s：建成应用拼贴墙（抽帧 apps-38.png 附近） | 大字：普通人 Plus 最值；小字：数据：OpenAI 官网定价页，2026 年 11 月 · 画面：OpenAI 官方演示 | S6 |

## 口播文案（口语化，去 AI 味；陈述句结尾，不提问；视频内无关注号召）

| 段 | 文案 | 字数 |
|---|---|---|
| S1 | Codex 零元就能上车 | 9 字 |
| S2 | 免费档在桌面 App 里 | 10 字 |
| S3 | 二十美元开网页命令行 | 11 字 |
| S4 | 一百美元没五小时限制 | 11 字 |
| S5 | 不想订阅就按量付 API | 11 字 |
| S6 | 普通人二十美元最值 | 10 字 |
| 合计 | | 62 字 |

- S3 的“网页命令行”是 Plus 的网页 + CLI（另有 IDE 插件和 iOS，口播里略去，屏上字写全）。
- S4 的依据：Pro 目前无 5 小时限制（OpenAI 定价页，多家比价文一致）。
- S5 的依据：API 按量 GPT-6 Astra $10 输入 / $50 输出 每百万 token（屏上字给精确数，口播只说按量付）。
- 辩论点放在标题和评论区（免费档够不够用、Plus 值不值），口播结尾是陈述句，不提问。

**标题（10 字）：** Codex上车，0元就能用

**发布文案（描述）：**
> Codex 不用单买，跟 ChatGPT 订阅走：免费档桌面 App 轻量用，Plus 20 美元（约 133 元）开网页、命令行和 IDE，Pro 100 美元（约 666 元）起没 5 小时限制，不想订阅就走 API 按量付。普通人 Plus 最值。国内直连用不了，官方支持名单里没有中国大陆。

**标签：** #AI #Codex #人工智能 #ChatGPT #编程

## 封面（1080×1920，深色，和号里数学视频封面同一套）

- 顶上青色胶囊：AI · 上车合集（对标数学封面的「数学可视化 · 反常识」）
- 大标题白字 + 黄字：Codex 上车 / 0 元就能用（数字黄色放大）
- 中间：三行价格条（免费 $0 / Plus $20 / Pro $100），Plus 那行黄色高亮
- 底部深色卡片，三行短字：免费档桌面 App 就能用 / Plus 二十美元开全渠道 / 普通人 Plus 最值
- 底部黄色胶囊：每天一个可视化概念（只放封面，视频内不放）
- 底图：5UlRL 38 秒处应用拼贴墙压暗，或 codex-app-intro 30 秒处桌面 UI 压暗，二选一

## 制作参数

- 剪辑：ffmpeg（模糊背景 + 居中实拍 + PIL 渲染的文字 PNG 叠加，不用 Manim 画全片；Manim 本条不用）
- 配音：6 句分别用 raw_edge_tts.py 生成（zh-CN-XiaoxiaoNeural，+10%），逐句核时长再拼
- 音乐：bgm-mixkit.mp3 音量 0.5，ffmpeg baked 进文件；静音版和混音版分开命名
- 校验：ffprobe 确认有音频流；ASR 听一遍口播；逐段抽帧看画面、字幕有无出画、360p 放大后是否可接受；总时长约 20 秒；第一帧就是紫色开场 + 0 元大字

## 文件

- 计划：~/workspace/douyin-ai-video/plan-03-codex.md
- 调研（5 个工具）：~/workspace/douyin-ai-video/research-03-five-tools.md
- 参考分析：~/workspace/douyin-ai-video/reference-axing-claudecode.md
- 素材：~/workspace/douyin-ai-video/media/codex03/（4 个 mp4）；预览抽帧：~/workspace/douyin-ai-video/media/preview/
- 成片（待制作）：~/workspace/imagine_media/codex-shangche-20s-1080x1920.mp4（混音版，发布用）、-silent.mp4（静音版）
- 封面（待制作）：~/workspace/imagine_media/codex-shangche-cover-1080x1920.png

## 待核实清单

- [ ] 官方定价页直读复核：本次价格引自 4 家第三方比价文（均称核对过 OpenAI 官网定价页，最新 2026-11-24），剪之前在浏览器里打开 OpenAI 官方定价页逐项复核一次（openai.com/codex 已读，只确认了“包含在 ChatGPT 订阅里”）。
- [ ] 免费档灰度开放（subject to rollout）：有的用户可能暂时看不到免费档——描述里不写，口播里不提；如评论区有人问再回。
- [ ] 分镜时段复核：剪辑时逐段看一遍，确认 5UlRL 各段和 app-intro 28–31.5s、178–181s 的画面内容与屏上字对得上，避开真人出镜开场。
- [ ] 360p 放大清晰度：抽帧验，模糊背景 + 居中裁切后是否可接受；不可接受则改用截图 Ken Burns 推镜补。
- [ ] 封面底图二选一：5UlRL 38s 拼贴墙 vs app-intro 30s 桌面 UI，压暗后看哪个干净。
