# 抖音 AI 视频 04 计划：Claude Code 上车全渠道合集（动画长版）

> 账号：小影数学（07050908kkk），AI 工具“能上车的全渠道合集”系列第 2 期。
> 发布：2026-11-28（11-27 不发，见 11-26 晚复核决定）。
> 方向：沿用 03B（用户 2026-11-26 13:30/13:31 定向）——横屏 1920×1080，动画图解为主体 + 真实素材混剪，米黄卡片、红字印章 verdict、烧录大字幕、全程配音，不限制时长，设计要精致。
> 工具：Remotion 4.0.543（复用 codex-long-remotion 项目结构，另起 claude-long-remotion 或复制后改名；勿用 /opt/meta-chromium/chrome）。

## 核实记录（2026-11-27 复核，来源见 research-04-claude-channels-verified.md）

- 官方价已复核，无变化：Pro $20/月（年付 $200，约 $17/月）、Max $100/月（5 倍 Pro 用量）、Ultra $200/月（每周 10 倍、无 5 小时限制，认证账号）、免费档 $0 不含 Claude Code、API Opus 5.5 $4/$20、Sonnet 5.5 $2/$10、Haiku 5.5 $0.10/$0.50 每百万 token。来源：Anthropic 定价页 claude.ai/pricing（搜索快照，11 小时前抓取）+ dev.to 2026-11-23 核对文，数字一致。新增细节（片中可不提）：Max/Ultra 含 Fable 模型（每周额度一半内）及 $100/$200 月 API credits。
- Antigravity 免费档 Claude 截止日已复核，仍是 2026-11-30：官方模型页 antigravity.google/docs/models（16 小时前抓取）表格脚注“* Will be removed on November 30, 2026”，对应 Claude Sonnet 4.6 / Opus 4.6；Pro $19.99/月含 Claude Sonnet 5.5 + Opus 5.5。播出日 11-28，片中说“只剩 2 天”成立。注意：该页正文另有一句把 Gemini 3.8 Flash 也列进 11-30 离场名单，与 tailkits“之后免费档剩 Gemini 3.8 Flash”的说法冲突——片中只讲“免费档的 Claude 11 月 30 日就没了”，不讲 3.8 Flash 的去留。
- Cursor 已复核，无变化：The X Subscription 之后新用户走 Premium $30/月起 + Claude 按 API 原价另付（预付 credit），Plus $8 / Free 用不了 Claude。来源：fastero 2026-11-12 核对、codersera 2026-10-26 核对，一致。
- Devin 计费口径冲突仍在，片中不写死任何 ACU 数字：continuumcode.ai（2026-08 实读定价页）称 ACU 已于 2026-03 取消，改为每日 + 每周 token 额度，Pro $20、Max $200；easyclaw / aicodingdir（2026-09-11 核实）/ toolacademy 仍写 Core $20 + $2.25/ACU、Team $500 含 250 ACU。处理：只说“$20 起，按用量另算，重度用下来几百美元”，不出现 $2.25/ACU、Team $500、Max $100/$200 这类数字；Devin 是独立自主 agent（自己接单干活、开 PR），不是 Claude Code 本体，讲的时候别说成“Claude Code 的一个入口”。
- Version 已决定去掉：两次搜索（英文 + 中文）均未找到名叫 Version、能接 Claude Code 的编程工具，阿星视频 05:16 章节可能是字幕/转录误差。本期为已核实的 8 个渠道（官方算 1 组 + 第三方 7 家），不要把没核实的名字放进视频。
- Kiro / GitHub Copilot / Kilo / Opencode 沿用 research-04 的 2026-11-26 核实结论（距今 1 天，不再逐项重查；制作前若时间允许可顺手复核 Copilot $10 档）。
- 汇率：1 美元 ≈ 6.66 元（沿用 research-03，2026-11-26）。

## 事实（已核实）

### 官方组

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档 Free | $0 | 0 元 | **不含 Claude Code** | 上不了 |
| Pro | $20/月，年付 $200（约 $17/月） | 约 133 元 | 含 Claude Code，默认 Opus 5.5；5 小时 + 每周限量 | **最值** |
| Max | $100/月 | 约 666 元 | Pro 用量的 5 倍 | 重度 |
| Ultra（原 Max 20x，2026-10 改名，价未变） | $200/月 | 约 1332 元 | 每周用量 10 倍 Pro，认证账号无 5 小时限制 | 土豪 |
| API 按量 | 无订阅，按 token | 用多少付多少 | Opus 5.5 $4/$20；Sonnet 5.5 $2/$10；Haiku 5.5 $0.10/$0.50 每百万 token | 灵活 |

### 第三方 7 家

| 渠道 | 价格 | 能得到什么 | verdict |
|---|---|---|---|
| Cursor | 新用户最低 $30/月（Premium）+ Claude 按 API 原价另付 | 以前 $20 包 Claude 已成过去；Plus $8 / Free 用不了 Claude | 变贵了 |
| Kiro（AWS） | 免费档 $0，每月 50 credits | 含 Claude Sonnet 4.5（老款）+ 开源模型，有限流；付费档 Pro $20/月起有 Opus 5.5 / Sonnet 5.5 | 0 元摸到 |
| GitHub Copilot | Pro $10/月 | 含 Claude Sonnet 5.5 / Haiku 5.5，不含 Opus 5.5；每月 1500 AI credits | 最便宜 |
| 谷歌 Antigravity | 免费档 $0；Pro $19.99/月 | 免费档 Claude Sonnet 4.6 / Opus 4.6 到 2026-11-30 就没了；付费 Pro 含 Claude 5.5 + Gemini 4 Neon | 只剩 2 天 |
| Devin | $20 起 | 独立自主 agent，自己接单干活开 PR；按用量另算 | 按量算 |
| Kilo Code | 工具 $0（开源 MIT） | 自带 Anthropic key 用 Claude，Kilo 不加价；另有免费模型、本地模型两条 0 元路 | 工具免费 |
| Opencode | 工具 $0（开源 MIT） | 接 200+ 供应商，Claude 需自带 API key；Go $10/月不含 Opus 5.5 / Sonnet 5.5 | 工具免费 |

- 国内直接能用吗：不能直连。Anthropic 官方支持名单无中国大陆、香港、澳门；订阅需境外支付。视频里只说“国内直连用不了”，不展开绕过方法。
- 和 Codex 最大的差别（本期钩子）：Codex 免费档能上，Claude Code 没有免费档——免费版 Claude 不含它，得先付 $20。
- 本期 3 个钩子（都已核实）：① Cursor 变贵了（$20 包 Claude 成过去，新用户最低 $30 还得按量另付）；② $10 就能摸到 Sonnet（Copilot Pro $10/月，最便宜的 Claude 入口；Opus 得加到 Pro+ $39）；③ 0 元路有两条（Kiro 免费档 Sonnet 4.5 + Kilo/Opencode 自带 key 工具 0 元），Antigravity 免费档的 Claude 只剩 2 天。

## 口播文案（约 51 句，口语化、去 AI 味；陈述句结尾，不提问；视频内无关注号召）

每句 ≤18 字。配音 zh-CN-XiaoxiaoNeural +10%，逐句核时长再拼。

| # | 文案 | 字数 | 场景 |
|---|---|---|---|
| L01 | Claude 上车，先说一句 | 14 | 0 开场钩子 |
| L02 | 免费档，上不了 | 7 | 0 开场钩子 |
| L03 | 跟 Codex 不一样 | 7 | 0 开场钩子 |
| L04 | 八个渠道，一次讲清楚 | 10 | 0 开场钩子 |
| L05 | 先看全景，八个渠道 | 9 | 1 总览图 |
| L06 | 免费零元，到两百美元 | 10 | 1 总览图 |
| L07 | 先看图，再一个一个讲 | 10 | 1 总览图 |
| L08 | 先说官方，免费档零元 | 10 | 2 官方 |
| L09 | 免费版，不含 Claude Code | 11 | 2 官方 |
| L10 | 想用它，先付二十美元 | 10 | 2 官方 |
| L11 | Pro 二十美元，普通人最值 | 12 | 2 官方 |
| L12 | Max 一百美元，用量五倍 | 11 | 2 官方 |
| L13 | Ultra 两百美元，十倍用量 | 12 | 2 官方 |
| L14 | 没五小时限制，随便造 | 10 | 2 官方 |
| L15 | 不想订月费，走 API 按量 | 11 | 2 官方 |
| L16 | 用多少，付多少 | 7 | 2 官方 |
| L17 | 再说 Cursor，变贵了 | 9 | 3 Cursor |
| L18 | 以前二十美元，全包了 | 10 | 3 Cursor |
| L19 | 现在最低三十美元起 | 10 | 3 Cursor |
| L20 | Claude 还得按量另付 | 10 | 3 Cursor |
| L21 | 八美元那档，根本用不了 | 11 | 3 Cursor |
| L22 | Kiro 免费档，零元能摸到 | 11 | 4 Kiro |
| L23 | 每月五十额度，Sonnet 老款 | 12 | 4 Kiro |
| L24 | 付费二十美元起，有新款 | 11 | 4 Kiro |
| L25 | 想白嫖，先从这儿试 | 9 | 4 Kiro |
| L26 | 最便宜的入口，是 Copilot | 11 | 5 Copilot |
| L27 | 十美元一个月，有 Sonnet | 11 | 5 Copilot |
| L28 | 要 Opus，得加到三十九 | 11 | 5 Copilot |
| L29 | 十美元摸 Sonnet，就它了 | 11 | 5 Copilot |
| L30 | 谷歌那个，免费档快没了 | 11 | 6 Antigravity |
| L31 | 免费的 Claude，只剩两天 | 11 | 6 Antigravity |
| L32 | 十一月三十号，就下线了 | 11 | 6 Antigravity |
| L33 | 付费十九块九，双模型 | 10 | 6 Antigravity |
| L34 | 一个价，两个模型拿 | 9 | 6 Antigravity |
| L35 | Devin 二十美元起 | 8 | 7 Devin |
| L36 | 它是自己干活的 agent | 10 | 7 Devin |
| L37 | 接单改代码，自己开 PR | 11 | 7 Devin |
| L38 | 按用量另算，用多付多 | 10 | 7 Devin |
| L39 | 最后两个，工具都不要钱 | 11 | 8 Kilo/Opencode |
| L40 | Kilo 开源，工具不要钱 | 13 | 8 Kilo/Opencode |
| L41 | 自带 key 就行，工具不加价 | 12 | 8 Kilo/Opencode |
| L42 | 轻量任务，走 API 更省 | 10 | 8 Kilo/Opencode |
| L43 | 八个渠道，都讲完了 | 9 | 9 汇总 |
| L44 | 只想试试，Kiro 免费档 | 10 | 9 汇总 |
| L45 | 十美元摸 Sonnet，就它 | 14 | 9 汇总 |
| L46 | 天天写代码，Pro 最值 | 10 | 9 汇总 |
| L47 | 免费档的 Claude，只剩两天 | 12 | 9 汇总 |
| L48 | 八个渠道，大陆都直连不了 | 12 | 9 汇总 |
| L49 | 订阅还得走境外支付 | 10 | 9 汇总 |
| L50 | 数据是官网定价，十一月 | 11 | 9 汇总 |

- L33 屏上字补全“每月 19.99 美元”；L28 屏上字补全“Pro+ $39/月含 Opus 5.5”；L42 屏上字补全“Haiku 5.5 每百万 token 只要 $0.10/$0.50”。
- 标题英文名重复教训（03B 已修）：场景标题只写“序号 · 名字”（如“03 · Cursor”），不要再加灰色小字英文名。

**标题：** Claude Code上车，免费档上不了

**发布文案（描述）：**
> Claude Code 没有免费档，免费版 Claude 不含它，得先付 $20：Pro 20 美元（约 133 元）普通人最值，Max 100 美元、Ultra 200 美元给重度用户，不想订阅就走 API 按量。第三方里 Cursor 变贵了（新用户最低 $30 还得按量另付），最便宜的 Sonnet 入口是 Copilot Pro $10，Kiro 免费档 0 元能摸到，Antigravity 免费档的 Claude 只剩 2 天。国内直连用不了，官方支持名单里没有中国大陆。

**标签：** #AI #Claude #ClaudeCode #人工智能 #编程

## 视觉设计（沿用 03B 阿星式，横屏 1920×1080）

- 底色：米黄 #F6EEDC；卡片：白 #FFFDF6，圆角 28px，柔和阴影；墨字 #2B2B26；红印章 #C0392B；黄高亮 #FFD93D；蓝点缀 #58C4DD；价格条用深蓝 #2E5E8C 填充。
- 顶栏（每场景常驻）：左侧青色胶囊“AI · 上车合集”+ 标题“Claude Code 全渠道”；右侧场景序号（如 3/9）。
- 渠道卡版式：左文右图。左侧：渠道名 + 价格大字 + 3 行要点 + 底部小字“大陆：直连用不了 · 订阅境外支付”；右上红印章 verdict（旋转 -5°，红框红字）；右侧：真实素材窗口（约 860×484，圆角 + 细边框）+ 下方小字“真实画面 · Anthropic 官方演示”。
- 官方场景（场景 2）是 5 行小表，不是单卡：免费 / Pro / Max / Ultra / API 各一行，Pro 那行黄色高亮 + “最值”小印章。
- 总览图：价格条（Free 0 / Pro 20 / Max 100 / Ultra 200 / API 按量 + 第三方 $0–$30 档），Pro 那根黄色高亮。
- 汇总：8 行对比表（渠道 | 价格 | verdict 印章）+ 底部大字“天天写代码，Pro 最值”+ 来源行“数据：Anthropic / 各家官网定价页，2026 年 11 月 · 画面：Anthropic 官方演示”。
- 烧录大字幕：白字黑边，48px，画面下方居中，与配音逐句同步切换。
- 字体：Noto Sans CJK SC（Regular/Bold），标题 Bold，正文 Regular。
- 动效：沿用 03B（卡片 spring 入场，价格条从 0 宽度生长，印章缩放盖下，场景间 12 帧淡入淡出）。

## 真实素材插入（每段几秒作证，来源片尾注明）

| 场景 | 素材 | 用法 |
|---|---|---|
| 2 官方 | Anthropic 官方 YouTube《Introducing Claude Code》（AJpK3YTTKZ4）终端实操段 | 右侧窗口；只用终端实操段，避开长篇 talking-head |
| 3 Cursor | cursor.com/pricing 真实截图（Premium $30 + 第三方按 API 价）或 Cursor 官方演示 | 右侧窗口；截图需制作当天现截 |
| 4 Kiro | kiro.dev/pricing 真实截图（Free 50 credits） | 右侧窗口 |
| 5 Copilot | GitHub Copilot 官方演示或定价页截图（Pro $10） | 右侧窗口 |
| 6 Antigravity | antigravity.google/models 真实截图（免费档 Claude 4.6 脚注 11-30 移除） | 右侧窗口；截图即证据 |
| 7 Devin | Devin 官方演示（自主 agent 开 PR 段） | 右侧窗口 |
| 8 Kilo/Opencode | 两家官网首页 / GitHub 页截图（开源 MIT 标识） | 右侧窗口 |
| 9 汇总 | 《Claude Code best practices》（gv0WHhKelSE）终端段点缀，或不用，汇总表为主 | 小窗点缀 |

- 素材下载：yt-dlp（android 客户端）下 Anthropic 官方 3 条（AJpK3YTTKZ4 / 6eBSHbLKuN0 / gv0WHhKelSE），只用终端实操段；下载后抽帧验内容。注意 03 号教训：YouTube 对本机出口限流 429 + 机器人验证时只能下到 360p，横屏窗口放大后抽帧验清晰度。
- 片尾来源行注明“画面：Anthropic 官方演示”。

## 制作参数

- Remotion 项目：复制 ~/workspace/douyin-ai-video/codex-long-remotion/ 为 claude-long-remotion/（node_modules 软链，chrome-headless-shell workaround 已就位；勿用 /opt/meta-chromium/chrome）；组件按 03B 的 CodexLong.tsx 改，标题行只留“序号 · 名字”。
- 构图：1920×1080，30fps；总时长 = 口播总时长 + 句间停顿（0.4s）+ 场景首尾留白，由 timeline.json 驱动；预计约 2.5–3 分钟。
- 配音：raw_edge_tts.py 逐句生成到 media/claude04/tts-long/seg01–seg50.mp3（TTS 必须用 ~/workspace/venvs/asr/bin/python）；ffprobe 核每句时长，写 timeline.json。
- 混音：Remotion 先渲静音版 → ffmpeg 混配音（按 timeline 偏移）+ bgm-mixkit.mp3 音量 0.5、尾部淡出；BGM 循环用输入级 -stream_loop 预处理，绝不在 filter graph 里循环（03 号死锁教训）；混音版与静音版分开命名。
- 封面：横屏 1920×1080，深色底 + 青色胶囊“AI · 上车合集”+ 大标题 Claude Code 上车 / 免费档上不了 + 三行价格条（Pro 黄色高亮）+ 底部黄色胶囊“每天一个可视化概念”；新做 claude-shangche-long-cover-1920x1080.png。
- 校验：ffprobe 规格与音频流；ASR 抽查配音；逐段抽帧看卡片、字幕、印章有无出画/遮挡；“好不好看”逐帧验收；确认渲染真的能播；发布后在公开页取消静音核对音频（03B 教训：浏览器读不到公开页音频，需她在手机上听一次）。

## 文件

- 策划：~/workspace/douyin-ai-video/plan-04-claude-animated.md（本文件）
- 调研：~/workspace/douyin-ai-video/research-04-claude-channels-verified.md、research-03-five-tools.md §2
- Remotion 项目：~/workspace/douyin-ai-video/claude-long-remotion/（制作时新建，复用 03B 结构）
- 配音：~/workspace/douyin-ai-video/media/claude04/tts-long/seg01–seg50.mp3（制作时生成）
- 成片（制作时）：~/workspace/imagine_media/claude-shangche-long-1920x1080.mp4（混音版）、-silent.mp4（静音版）
- 封面（制作时）：~/workspace/imagine_media/claude-shangche-long-cover-1920x1080.png

## 待核实清单（制作时）

- [x] 官方价 2026-11-27 复核，无变化（见上）
- [x] Antigravity 免费档 Claude 截止日 2026-11-27 复核，仍是 11-30（见上）
- [x] Cursor 2026-11-27 复核，无变化（见上）
- [x] Devin 冲突仍在，片中不写 ACU 数字（见上）
- [x] Version 去掉，8 个渠道（见上）
- [ ] 下载 Anthropic 官方 3 条片源并抽帧验内容，只用终端实操段
- [ ] 现截 Cursor / Kiro / Copilot / Antigravity 定价页截图作右侧窗口证据
- [ ] 每句 TTS 时长与 timeline 对齐；场景切换点不切在句中
- [ ] 360p 素材在 860×484 窗口里的清晰度抽帧验收
- [ ] 封面横屏版式验收
