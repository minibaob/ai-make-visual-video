# 抖音 AI 视频 03B 计划：Codex 上车全渠道合集（动画长版）

> 账号：小影数学（07050908kkk），AI 工具“能上车的全渠道合集”系列第 1 期。
> 方向（用户 2026-11-26 13:30 定向 + 13:31 两次修正，最终版）：
> - **横屏 1920×1080**（16:9），不是竖版；封面也按横屏做。
> - **动画图解为主体 + 真实素材混剪**：米黄底卡片、价格条/对比表、红字印章 verdict、烧录大字幕、全程配音；每个渠道段落里混进几秒真实素材作插图/作证（已下载的 4 条 OpenAI 官方演示 + 真实界面截图），主体叙事仍由动画卡片承担。
> - **不限制时长、不注水**，按内容自然定；本期约 2 分钟（41 句口播）。
> - **设计要精致**：配色排版仔细对齐，字号层级、留白、印章位置都要讲究；“好不好看”是验收项。
> - 20 秒真实素材版（codex-shangche-20s-1080x1920.mp4，19.6 秒，已验证）保留作备用，不要动。
> - 工具：Remotion 4.0.543 首选；Manim 只在 Remotion 做不了时考虑；Motion Canvas 无 headless 渲染，不用。
> - 事实与标题/描述/标签复用 plan-03-codex.md；5 渠道价格与 verdict 复用 research-03-five-tools.md §1。

## 事实（已核实，2026-11-26 查；来源见 plan-03-codex.md）

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档 Free | $0 | 0 元 | 桌面 App 轻量用，GPT-6 Luna 标准速度，灰度开放；无云端任务 | 能上 |
| Go | $8/月 | 约 53 元 | 同免费档，额度稍多，仍只有桌面 App、GPT-6 Luna；无云端任务 | 凑合 |
| Plus | $20/月 | 约 133 元 | 网页 + CLI + IDE 插件 + iOS 全开，GPT-6.1 Sol/Luna，自动审 PR、Slack 集成；5 小时窗口限量，可买 credits 续 | **最值** |
| Pro | $100 / $200 / $500/月 | 约 666 / 1332 / 3330 元 | Plus 全部 + 更高额度；目前无 5 小时限制；$500 档独有 Ultrafast 模式 | 重度 |
| API key 按量 | 无订阅，按 token | 用多少付多少 | GPT-6 Astra $10 输入 / $50 输出 每百万 token；无云端功能（无 GitHub 审 PR）；CLI/SDK/IDE 插件里填 key 即用 | 灵活 |

- Codex 没有单独售价，跟 ChatGPT 订阅走（OpenAI 官网原话 "Codex is included in your ChatGPT plan"）。
- 国内直接能用吗：不能直连。OpenAI 官方支持名单 208 国无中国大陆/港澳；订阅需境外支付。视频里只说“国内直连用不了”，不展开绕过方法。
- 不讲的：12 月起共享额度新规（免得说错）；第三方代充（不展开）。
- 汇率：1 美元 ≈ 6.66 元（2026-11-26）。

## 口播文案（41 句，口语化、去 AI 味；陈述句结尾，不提问；视频内无关注号召）

每句 ≤18 字。配音 zh-CN-XiaoxiaoNeural +10%，逐句核时长再拼。

| # | 文案 | 字数 | 场景 |
|---|---|---|---|
| L01 | Codex 上车，零元就能用 | 11 | 0 开场钩子 |
| L02 | OpenAI 的编程助手 | 10 | 0 开场钩子 |
| L03 | 写代码改代码跑测试都行 | 12 | 0 开场钩子 |
| L04 | 五个渠道，一次讲清楚 | 10 | 0 开场钩子 |
| L05 | 先看全景，五个渠道 | 9 | 1 总览图 |
| L06 | 免费零元，最高五百美元 | 11 | 1 总览图 |
| L07 | 先看图，再一个一个讲 | 10 | 1 总览图 |
| L08 | 先说免费档，零元就能上 | 11 | 2 免费 |
| L09 | 在桌面 App 里就能用 | 10 | 2 免费 |
| L10 | 轻量模型，写点小东西够了 | 13 | 2 免费 |
| L11 | 没有云端任务，额度也少 | 11 | 2 免费 |
| L12 | 灰度开放，有人还看不到 | 11 | 2 免费 |
| L13 | 白嫖党，先从这儿试 | 9 | 2 免费 |
| L14 | 再说 Go，八美元一个月 | 11 | 3 Go |
| L15 | 还是只有桌面 App | 9 | 3 Go |
| L16 | 额度比免费多一点 | 9 | 3 Go |
| L17 | 没有云端任务，性价比一般 | 12 | 3 Go |
| L18 | 只能说，凑合着用 | 8 | 3 Go |
| L19 | 重点来了，Plus 二十美元 | 11 | 4 Plus |
| L20 | 网页命令行 IDE 全开 | 10 | 4 Plus |
| L21 | 自动帮你审代码，还能接 Slack | 16 | 4 Plus |
| L22 | 手机上也能接着干 | 9 | 4 Plus |
| L23 | 五小时窗口，量大了要续 | 11 | 4 Plus |
| L24 | 普通人，选它最值 | 8 | 4 Plus |
| L25 | 用得狠的，看 Pro | 8 | 5 Pro |
| L26 | 一百美元起步，分三档 | 10 | 5 Pro |
| L27 | 没五小时限制，随便造 | 10 | 5 Pro |
| L28 | 五百那档，还有极速模式 | 11 | 5 Pro |
| L29 | 每天泡在代码里的，再考虑 | 13 | 5 Pro |
| L30 | 不想订月费，走 API | 9 | 6 API |
| L31 | 用多少，付多少 | 7 | 6 API |
| L32 | 输入十美元，输出五十 | 11 | 6 API |
| L33 | 没有云端功能，审不了 PR | 12 | 6 API |
| L34 | 适合自己搭工具的人 | 10 | 6 API |
| L35 | 五个渠道，都讲完了 | 9 | 7 汇总 |
| L36 | 只想试试，免费档就行 | 10 | 7 汇总 |
| L37 | 天天写代码，Plus 最值 | 10 | 7 汇总 |
| L38 | 靠它吃饭，再看 Pro | 9 | 7 汇总 |
| L39 | 五个渠道，大陆都直连不了 | 12 | 7 汇总 |
| L40 | 订阅还得走境外支付 | 10 | 7 汇总 |
| L41 | 数据是官网定价，十一月 | 11 | 7 汇总 |

- L32 屏上字补全“每百万 token”；L21 的 Slack 即 plan-03 已核实的 Slack 集成。

**标题：** Codex上车，0元就能用（复用 20 秒版）

**发布文案（描述，复用 20 秒版，微调）：**
> Codex 不用单买，跟 ChatGPT 订阅走：免费档桌面 App 轻量用，Plus 20 美元（约 133 元）开网页、命令行和 IDE，Pro 100 美元（约 666 元）起没 5 小时限制，不想订阅就走 API 按量付。普通人 Plus 最值。国内直连用不了，官方支持名单里没有中国大陆。

**标签：** #AI #Codex #人工智能 #ChatGPT #编程

## 视觉设计（阿星式，横屏 1920×1080）

- 底色：米黄 #F6EEDC；卡片：白 #FFFDF6，圆角 28px，柔和阴影；墨字 #2B2B26；红印章 #C0392B；黄高亮 #FFD93D；蓝点缀 #58C4DD；价格条用深蓝 #2E5E8C 填充。
- 顶栏（每场景常驻）：左侧青色胶囊“AI · 上车合集”+ 标题“Codex 全渠道”；右侧场景序号（如 2/7）。
- 渠道卡版式：左文右图。左侧：渠道名 + 价格大字（$0 / $8 / $20 / $100起 / 按量）+ 3 行要点 + 底部小字“大陆：直连用不了 · 订阅境外支付”；右上红印章 verdict（旋转 -5°，红框红字）；右侧：真实素材窗口（约 860×484，圆角 + 细边框）+ 下方小字“真实画面 · OpenAI 官方演示”。
- 总览图：5 根横向价格条（Free 0 / Go 8 / Plus 20 / Pro 100–500 / API 按量），Plus 那根黄色高亮 + “最值”小印章。
- 汇总：5 行对比表（渠道 | 价格 | verdict 印章）+ 底部大字“普通人 Plus 最值”+ 来源行“数据：OpenAI 官网定价页，2026 年 11 月 · 画面：OpenAI 官方演示”。
- 烧录大字幕：白字黑边，48px，画面下方居中，与配音逐句同步切换。
- 字体：Noto Sans CJK SC（Regular/Bold），标题 Bold，正文 Regular。
- 动效：卡片 spring 入场（Remotion spring），价格条从 0 宽度生长，印章缩放盖下（带轻微旋转），场景间 12 帧淡入淡出；不花哨，以“稳、干净”为主。

## 真实素材插入（每段几秒作证，来源片尾注明）

| 场景 | 素材 | 时段 | 用法 |
|---|---|---|---|
| 2 免费 | 5UlRL_ImvQ0.mp4 | 8–11.3s（Event Operations / Sites 界面） | 右侧窗口循环/播放一次，桌面 App 真实界面 |
| 3 Go | y5hogSW2mqU.mp4 | 待抽帧确认一段真实 Codex 工作流（剪辑时抽帧验内容） | 右侧窗口 |
| 4 Plus | codex-app-intro.mp4 | 29–32.5s（桌面端 + 手机端同屏 UI） | 右侧窗口；注：右上角有官方演示自带的小窗真人，20 秒版已接受，沿用 |
| 5 Pro | codex-app-intro.mp4 | 178–181s（Today's Progress 任务板） | 右侧窗口；同上，小窗真人沿用 |
| 6 API | 5UlRL_ImvQ0.mp4 | 15–18.2s（Sites 输入框打字动画） | 右侧窗口 |
| 7 汇总 | 5UlRL_ImvQ0.mp4 | 36–39.4s（建成应用拼贴墙） | 小窗点缀或不用，汇总表为主 |

- 素材均 640×360，横屏窗口约 860×484 放大，20 秒版已验证该放大倍率可接受；抽帧验清晰度。
- 片尾来源行注明“画面：OpenAI 官方演示”。

## 制作参数

- Remotion 项目：~/workspace/douyin-ai-video/codex-long-remotion/（从 remotion-test 复制，node_modules 软链，chrome-headless-shell workaround 已就位；勿用 /opt/meta-chromium/chrome）。
- 构图：1920×1080，30fps；总时长 = 口播总时长 + 句间停顿（0.4s）+ 场景首尾留白，由 timeline.json 驱动。
- 配音：raw_edge_tts.py 逐句生成到 media/codex03/tts-long/seg01–seg41.mp3；ffprobe 核每句时长，写 timeline.json。
- 混音：Remotion 先渲静音版 → ffmpeg 混配音（按 timeline 偏移）+ bgm-mixkit.mp3 音量 0.5、尾部淡出；混音版与静音版分开命名。
- 封面：横屏 1920×1080，深色底 + 青色胶囊“AI · 上车合集”+ 大标题 Codex 上车 / 0 元就能用 + 三行价格条（Plus 黄色高亮）+ 底部黄色胶囊“每天一个可视化概念”；新做 codex-shangche-long-cover-1920x1080.png（不复用竖版封面）。
- 校验：ffprobe 规格与音频流；ASR 抽查配音；逐段抽帧看卡片、字幕、印章有无出画/遮挡；“好不好看”逐帧验收；确认渲染真的能播。

## 文件

- 策划：~/workspace/douyin-ai-video/plan-03b-codex-animated.md（本文件）
- Remotion 项目：~/workspace/douyin-ai-video/codex-long-remotion/
- 配音：~/workspace/douyin-ai-video/media/codex03/tts-long/seg01–seg41.mp3
- 时间轴：~/workspace/douyin-ai-video/codex-long-remotion/src/timeline.ts（由 timeline.json 生成）
- 成片：~/workspace/imagine_media/codex-shangche-long-1920x1080.mp4（混音版）、-silent.mp4（静音版）
- 封面：~/workspace/imagine_media/codex-shangche-long-cover-1920x1080.png
- 20 秒备用版（勿动）：~/workspace/imagine_media/codex-shangche-20s-1080x1920.mp4

## 待核实清单

- [x] Go 段真实素材：y5hogSW2mqU 58–62s，Codex 聊天界面（会议纪要准备），抽帧确认可用。
- [x] 每句 TTS 时长与 timeline 对齐；场景切换点不切在句中（timeline.json 由实测时长生成）。
- [x] 360p 素材在 860×484 窗口里的清晰度抽帧验收（8 场景逐段验过，可接受）。
- [x] 封面横屏版式验收（codex-shangche-long-cover-1920x1080.png，双栏版式，Plus 高亮）。

## 成片记录（2026-11-26）

- 成片：~/workspace/imagine_media/codex-shangche-long-1920x1080.mp4（混音版，129.6 秒，1920×1080，30fps，h264+aac，8.69MB）、-silent.mp4（静音版，6.48MB）；封面 codex-shangche-long-cover-1920x1080.png。
- 校验：ffprobe 规格与音频流 OK；ASR 抽查 41 句配音全部在正确时间点出现（tiny 模型同音字/英文误听是模型局限，配音按原文案生成）；8 场景逐段抽帧：卡片、字幕、印章无出画/遮挡；钩子开场修正过一处（去掉与顶栏重复的居中胶囊）；渲染全程可播（混音版 8 个时间点抽帧均正常解码）。
- 制作教训：TTS 必须用 ~/workspace/venvs/asr/bin/python（系统 python3 没有 edge_tts）；BGM 循环用输入级 -stream_loop 预处理成 bgm-long.mp3，不要在 filter graph 里循环（20 秒版死锁教训）；Remotion 全片渲染约 13 分钟（3887 帧，含 3 条真实素材解码）。

## 修复记录（2026-11-26 16:14–16:25，重名修复 + 重渲染）

- 问题：各渠道场景标题把英文名重复显示（主代理抽帧确认：Go 场景“02 · Go Go”、Pro 场景“04 · Pro Pro”）。
- 根因：`src/CodexLong.tsx` 渠道卡片标题行同时渲染了 `{card.index} · {card.name}` 和灰色小字 `{card.en}`；名字本身就是英文的渠道（Go、Plus、Pro）以及 API（name“API 按量”+ en“API”）就重复了。
- 修复：只改 `CodexLong.tsx` 标题行一处，删掉 `{card.en}` 的灰色小字 span，标题统一为“序号 · 名字”（“01 · 免费档”“02 · Go”“03 · Plus”“04 · Pro”“05 · API 按量”）。`timeline.ts` 的 `en` 字段留着未动（数据不动，只改渲染）；字号、颜色、印章、排版其他一律未动。封面不用重做。
- 重渲染：同一套 Remotion 项目，`npx remotion render CodexLong` → 静音版，再跑 `mix_audio_long.py` 混音（41 句配音 + BGM，配音文件和时间轴未变）。渲染约 8.8 分钟（RENDER_EXIT=0），覆盖原文件：混音版 `codex-shangche-long-1920x1080.mp4`（129.57 秒，1920×1080，h264+aac，8.65MB）、静音版 `-silent.mp4`（129.57 秒，6.48MB）。
- 校验（重渲染后）：ffprobe 规格与音频流 OK（混音版 1920×1080、129.57 秒、h264+aac；静音版同规格无音频流）；抽帧 6 帧亲眼确认——免费档 32s“01 · 免费档”、Go 49s“02 · Go”、Plus 66s“03 · Plus”、Pro 84s“04 · Pro”、API 100s“05 · API 按量”、汇总 119s 对比表，全部单名无重复、无其他文字错位、无出画/遮挡。
