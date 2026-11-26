# AI 工具“能上车的全渠道合集”系列调研（5 个工具）

> 调研日期：2026-11-26。汇率：1 美元 ≈ 6.66 元人民币（2026-11-26，XE/Finnhub 中间价 6.663–6.672，取 6.66 折算；片中只出现约数时写“约××元”）。
> 系列定位（2026-11-26 13:30 用户改向，supersede 下文旧定位）：合集系列按阿星式动画信息图做——米黄卡片、图表、红字印章 verdict、烧录大字幕、配音；不限制时长、不强制真实素材；每期一个工具，盘点全部渠道 + 逐个一句话 verdict + 最后汇总。旧定位（~20 秒竖版、真实素材、一期 3–4 个渠道）只保留在 03 号 20 秒版成片里作备用，不再是系列方向。
> 参考视频分析见 reference-axing-claudecode.md（阿星 6 分 14 秒动画信息图，盘点 9 渠道，2.5 万赞、1.9 万收藏；形式不照搬，只取“合集盘点 + 逐个一句话 verdict + 汇总”的公式）。
> 中国大陆可用性统一口径：四家官方支持名单（OpenAI/Anthropic/Google）均无中国大陆；核对来源为 proxy302.com 2026-11-06 对四份官方名单的比对 + OpenAI 帮助中心。Grok/Muse 见各节。

## 1. Codex（OpenAI 的编程 agent）——第 03 期，已立项

**是什么：** OpenAI 的 AI 编程助手，写代码、跑测试、改仓库、自动审 PR；入口有桌面 App、网页、CLI、IDE 插件、云端任务。官网原话：“Codex is included in your ChatGPT plan”（openai.com/codex，2026-11-26 已读）。

**上车渠道（按便宜/方便排，价格为美元原价，不含税）：**

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档 Free | $0 | 0 元 | 桌面 App 里轻量用，GPT-6 Luna 标准速度，灰度开放（subject to rollout） | 能上 |
| Go | $8/月 | 约 53 元 | 同免费档，额度稍多，仍只有桌面 App、GPT-6 Luna | 凑合 |
| Plus | $20/月 | 约 133 元 | 网页 + CLI + IDE 插件 + iOS 全开，GPT-6.1 Sol/Luna，自动审 PR、Slack 集成；5 小时窗口限量，可买 credits 续 | **最值** |
| Pro | $100 / $200 / $500/月 | 约 666 / 1332 / 3330 元 | Plus 全部 + 更高额度；目前无 5 小时限制；$500 档独有 Ultrafast 模式 | 重度 |
| API key 按量 | 无订阅，按 token | 用多少付多少 | GPT-6 Astra $10 输入 / $50 输出 每百万 token；无云端功能（无 GitHub 审 PR）；CLI/SDK/IDE 插件里填 key 即用 | 灵活 |

**核心事实（3 个）：**
1. Codex 没有单独售价，跟 ChatGPT 订阅走——已经付 Plus 的人等于白得一个编程 agent。
2. 0 元免费档真实存在（桌面 App、GPT-6 Luna、轻量），是全系列最强的钩子。
3. Plus $20 是普通人最值的一档；Pro 起步 $100，主要差别是去掉 5 小时限制。

**国内直接能用吗：** 不能直连。OpenAI 官方支持名单 208 个国家/地区，中国大陆、香港、澳门均不在列；OpenAI 帮助中心写明在名单外使用“可能导致账号被封或停用”；chatgpt.com 从大陆直连打不开。订阅需境外支付（常见走法是境外 Apple ID 走 App Store，第三方代充有封号风险——视频里不展开，只说“国内直连用不了”）。

**价格来源：** OpenAI 官网定价页经 4 家第三方比价文交叉核对（layer3labs、faros.ai、vdf.ai、devhunt，最新核对 2026-11-24，数字一致：Free $0 / Go $8 / Plus $20 / Pro $100·200·500；API Astra $10/$50）。**待核实：未直接打开 openai.com 定价页逐项复核，剪之前主代理应在浏览器里打开官方定价页复核一次。** 另：faros 称 OpenAI 已宣布 2026 年 12 月起 Plus/Pro/Business 将共享 ChatGPT+Codex 额度——视频里不提，免得说错。

**素材：✅ 齐全（已下载到本地）。** 4 条 OpenAI 官方 YouTube 演示视频，用 yt-dlp（android 客户端）下载，`~/workspace/douyin-ai-video/media/codex03/`：
- `codex-app-intro.mp4`（Introducing the Codex app，HFM3se4lNiw，261 秒）
- `5UlRL_ImvQ0.mp4`（Build and share apps in Codex，46.5 秒，最干净，全是产品 UI/动效，无真人出镜）
- `y5hogSW2mqU.mp4`（Prep for sales meetings faster with Codex，212.6 秒）
- `fK_bm84N7bs.mp4`（Build beautiful frontends with OpenAI Codex，509 秒，含真人出镜段，慎用）
- 授权/署名：OpenAI 官方发布素材，新闻/评测转载用；片尾注明“画面：OpenAI 官方演示”。
- **缺口/注意：只能下到 360p（format 18；YouTube 对本机出口限流 429 + 机器人验证，720p 分离流拿不到），竖版放大后偏软——按 02 号做法用模糊背景 + 16:9 居中，抽帧验清晰度。** 另：app-intro 前 ~10 秒是真人出镜开场，剪辑时避开，只用 UI 段。

**第 03 期完整策划：见 plan-03-codex.md。**

## 2. Claude Code（Anthropic 的编程 agent）——第 04 期

**是什么：** Anthropic 的 agentic 编程工具，在终端里读代码库、改文件、跑命令；另有 IDE、桌面 App、浏览器入口。默认模型 Opus 5.5。

**上车渠道（官方订阅 + API，美元原价，不含税）：**

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档 Free | $0 | 0 元 | **不含 Claude Code**（官网定价页明确） | 上不了 |
| Pro | $20/月，或 $200/年（约 $17/月） | 约 133 元 | 含 Claude Code；与网页/桌面/手机聊天共享额度；5 小时 + 每周限量；Fable 模型只走用量 credits | **最值** |
| Max | $100/月 | 约 666 元 | Pro 用量的 5 倍 | 重度 |
| Ultra（原 Max 20x，2026 年 10 月改名，价格未变） | $200/月 | 约 1332 元 | 每周用量 10 倍 Pro，认证账号无 5 小时限制；Max/Ultra 含 $100/$200 月 API credits（不能用于 Claude Code） | 土豪 |
| API key 按量 | 无订阅，按 token | 用多少付多少 | Opus 5.5 $4 输入 / $20 输出 每百万 token；Sonnet 5.5 $2/$10；Haiku 5.5 $0.10/$0.50；无会话限量 | 灵活 |

**核心事实（3 个）：**
1. Claude Code 没有免费档——免费版 Claude 不含它，这是和 Codex 最大的差别（Codex 免费能上，Claude 得先付 $20）。
2. 入门价和 Codex 一样是 $20/月，但 Pro 月用量按 API 价折算约值 $707（第三方实测 134 个账号，2026-11-16–23），Max 约 $3,657——订阅制比按量划算得多。
3. API 路线的便宜模型是 Haiku 5.5（$0.10/$0.50），轻量任务走 API 可能比订阅还省。

**国内直接能用吗：** 不能直连。Anthropic 官方支持名单无中国大陆、香港、澳门（proxy302 2026-11-06 比对官方名单）。订阅需境外支付。

**第三方渠道（阿星视频里盘点的 9 个）：** Cursor、Kiro、GitHub Copilot、谷歌 Antigravity、Devin、Kilo、Version、Opencode——**本文件未逐一核实各家是否接入 Claude、什么价，04 期策划时再逐个核实，不照抄阿星的结论。** 阿星视频自报的官方价（Pro $20 / Max 5x $100 / Max 20x $200；API $4/$20）与本文件核实结果一致，可作交叉印证。

**价格来源：** Anthropic 官网定价页经 3 家第三方比价文交叉核对（cloudzero 2026-11-24、faros.ai 2026-11-18、dev.to 2026-11-23，数字一致）。**待核实：未直接打开 claude.com/pricing 逐项复核，04 期策划前复核。**

**素材：⚠️ 有官方片源，待下载。** Anthropic 官方 YouTube（@claude）：
- 《Introducing Claude Code》（AJpK3YTTKZ4，2025-02-24，官方 launch 演示，团队出镜 + 真实终端会话，约 58.6 万播放）
- 《Mastering Claude Code in 30 minutes》（6eBSHbLKuN0，官方 30 分钟全程 tour）
- 《Claude Code best practices》（gv0WHhKelSE，官方，约 45.6 万播放）
- 下载方式与 Codex 相同（yt-dlp android 客户端可绕过 429），04 期制作时下载并抽帧验内容；只用终端实操段，避开长篇 talking-head。

## 3. Muse（Meta 的个人 AI 助手）——第 05 期

**是什么：** Meta 2026-09-08 发布的个人 AI agent，不止聊天——能替你发邮件、订票、填表、比价下单，在自己的安全云电脑里干活。模型 Muse Spark（免费档）/ Muse Wonder（付费档）。**注意：它不是编程 agent，是生活办事 agent——本期角度是“有个 AI 帮你跑腿”，别按编程工具讲。**

**上车渠道（美元原价，不含税）：**

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档 | $0 | 0 元 | 完整 agent 功能，每周 100M tokens 额度（Meta 官方说法）；App（iOS/Android）+ 网页 muse.ai + WhatsApp 里都能用 | **能上** |
| Power | $20/月 | 约 133 元 | 每周 500M Muse tokens，首批用上 Wonder 模型 | 加量 |
| Maximum | $100/月 | 约 666 元 | 每周 3B Muse tokens，每天 20 通电话 | 重度 |
| API 按量 | 按 token | 用多少付多少 | Spark 1.3 $1.25 输入 / $4.25 输出 每百万 token；Wonder $4/$20（第三方 aitoolapp 数据，待核实） | 开发者 |

**核心事实（3 个）：**
1. 五个工具里唯一一个免费档就给完整 agent 的——不用付费就能让它替你办事（每周 100M tokens 额度内）。
2. 2026-09-08 才上线，11 周下载量破 1000 万（aitoolapp 2026-11-25 更新），是五个里最“新”的。
3. 付费档 $20/$100 和别人一样，但买的是用量不是功能——免费和付费功能差别小。

**国内直接能用吗：** 不能。截至 2026-11-24 仅在美国、加拿大、日本、新加坡、澳大利亚、英国上线（aitoolapp 2026-11-25）；中国大陆不在列，需 18 岁以上。订阅走 muse.ai / App 内购，需境外支付。

**价格来源：** Meta 发布日报道（CNBC、TradingView/道琼斯 2026-09-29）+ aitoolapp 2026-11-25 更新（Power $20/500M tokens 周、Maximum $100/3B tokens 周）；免费档 100M tokens/周引自 Meta 官方说法（经 openaimaster 转述）。**待核实：Meta 未公布完整定价页分项，05 期策划前复核 muse.ai/pricing（以官方页为准）。**

**素材：⚠️ 待找。** 未检索到可直接下载的 Meta 官方演示视频；05 期制作时先查 Meta 新闻中心 / Muse 官方 YouTube 是否有演示片，无官方片则用 App 界面真实截图 + Ken Burns 推镜（不生成 AI 画面）。**缺口：目前无已下载素材。**

## 4. Grok（xAI）——第 06 期

**是什么：** xAI 的 AI 助手，入口在 X 内、grok.com 独立站、iOS/Android App；有聊天、语音、图片/视频生成（Imagine）、Build（做东西）、Cursor 编程 agent 联动。

**上车渠道（2026-10-12 改制后的 X Subscription，美元原价，不含税；老 SuperGrok 仅老用户可保留，新用户买不到）：**

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档 | $0 | 0 元 | grok.com / App / X 内有限聊天、Imagine、Build，Cursor 编程 agent 起步额度 | 能上 |
| Plus | $8/月（年付 $80） | 约 53 元 | 基础额度；Grok 聊天/语音/Imagine/Build、API 入口、Cursor、X Premium 蓝标 | 入门 |
| Premium | $30/月（年付 $300） | 约 200 元 | Plus 的 4 倍用量；最新 Grok 模型、图片/视频生成、Grok Bot、云端 agent | **最值** |
| Super | $100/月（年付 $1000） | 约 666 元 | 15 倍用量；1080p 视频、高峰优先 | 重度 |
| Ultra | $200/月（年付 $2000） | 约 1332 元 | 50 倍用量；最强聊天模型、最先体验新品 | 土豪 |
| API 按量 | 按 token | 用多少付多少 | Grok 4.7 $2 输入 / $6 输出 每百万 token；Grok Build 0.1 $1 输入起 | 灵活 |

**核心事实（3 个）：**
1. 2026-10-12 改制后 Grok 不再单卖——新用户买的是 X Subscription，一份钱捆绑 Grok + Cursor + X Premium 权益；老 SuperGrok（$30/月）只有老用户能留着。
2. 免费档真实存在，grok.com 不用 X 会员也能聊（有限额）。
3. 入门 $8 是五个工具里付费档最低的（和 Codex Go 同价），Premium $30 是 xAI 自己推荐给新用户的档。

**国内直接能用吗：** X 在国内打不开；grok.com 独立站是否可直连**未核实到 xAI 官方口径**（xAI 未像 OpenAI 那样公布支持国家名单），视频里只说“要上 X、得先解决网络”，不编具体说法。订阅需境外支付。

**价格来源：** xAI 官方定价页（x.ai/pricing、docs.x.ai）经 3 家第三方比价文交叉核对（ai-toolbox.co 2026-10-25、thepricer.org 2026-10-26、techpilot.ai 2026-11-13，数字一致：Free $0 / Plus $8 / Premium $30 / Super $100 / Ultra $200；API Grok 4.7 $2/$6）。注意：2026 年 8 月及以前的旧文（SuperGrok $30、Heavy $300）已过时，以 10 月改制为准。**待核实：未直接打开 x.ai/pricing 逐项复核，06 期策划前复核。**

**素材：⚠️ 待找。** 未检索官方演示视频下载源；06 期制作时查 xAI/Grok 官方 YouTube、X 官方账号视频，或用 grok.com 真实界面录屏（需可访问的账号环境——主代理定）。**缺口：目前无已下载素材。**

## 5. Gemini（Google）——第 07 期

**是什么：** Google 的 AI 助手，入口在 Gemini App、Google 搜索 AI Mode、Gmail/Docs 里；另有 Gemini API（Google AI Studio）给开发者。模型分档：免费档 Flash-Lite，付费档 Gemini 4 Argon/Carbon 等。

**上车渠道（美元原价，不含税）：**

| 渠道 | 价格 | 约人民币 | 能得到什么 | verdict |
|---|---|---|---|---|
| 免费档（Gemini App） | $0 | 0 元 | Flash-Lite 模型，有限额度；聊天、搜图、基础功能 | 能上 |
| Google AI Plus | $4.99/月 | 约 33 元 | 免费档 2 倍用量，400GB 存储，Gmail/Vids 里用 Gemini | 便宜 |
| Google AI Pro | $19.99/月（年付 $199.99） | 约 133 元 | 免费档 4 倍用量，全部模型（含 Gemini 4 Argon），1M token 上下文，5TB 存储，Deep Research，1000 Flow credits | **最值** |
| Google AI Ultra | $99.99/月 | 约 666 元 | Pro 的 5 倍用量，20TB 存储，Deep Think、Gemini Spark agent、YouTube Premium | 重度 |
| Google AI Ultra（高档） | $199.99/月 | 约 1332 元 | Pro 的 20 倍用量，Project Genie，25000 Flow credits | 土豪 |
| Gemini API 免费档（AI Studio） | $0 | 0 元 | 无需绑卡：Gemini 3.8 Flash、3.6 Flash、Flash-Lite、Gemini 4 Hydrogen 免费 token（按项目限流）；顶级模型（Carbon/Argon/Neon）不在免费档 | **白嫖** |
| Gemini API 按量 | 按 token | 用多少付多少 | 最便宜 3.1 Flash-Lite $0.25 输入 / $1.50 输出 每百万 token；Carbon/Argon $2/$10（2026-11-30 前），**12 月 1 日起涨到 $4/$20** | 灵活 |

**核心事实（3 个）：**
1. Gemini 是五个里免费路子最多的：App 免费档 + API 免费档（AI Studio 不绑卡就能调 Flash 模型）两条 0 元路。
2. Pro $19.99 是五个里同档最便宜的旗舰订阅（和 Codex Plus、Claude Pro 同价，但附 5TB 存储 + YouTube Premium Lite）。
3. **有时效的钩子：Gemini 最强模型 Carbon/Argon 12 月 1 日涨价一倍（$2/$10 → $4/$20）**——07 期若在 12 月 1 日前发，可用“涨价倒计时”当钩子；12 月 1 日后发则改说“已经涨了”。

**国内直接能用吗：** 个人版不能直连。Google 服务在大陆不可用；官方名单比对（proxy302 2026-11-06）：Gemini 网页 App 在中国大陆仅 Workspace（企业版）列出，个人版不在列；Gemini API 与 AI Studio 名单无中国大陆。订阅需境外支付。

**价格来源：** Google 官方（I/O 2026 博客 2026-05-19：Ultra $99.99 新增、顶档 $249.99→$199.99）+ Google One 计划页经 3 家第三方交叉核对（datastudios.org 2026-11-14、gmelius、kurums 2026-11 月，数字一致）；API 免费档与价目经 apidog/techpilot/datastudios 核对 Google 定价页（2026-10-22 / 11-19 / 11-20，数字一致）。**待核实：未直接打开 Google One 计划页与 Gemini API 定价页逐项复核，07 期策划前复核；12 月 1 日涨价后需重新核对 Carbon/Argon 价格。**

**素材：⚠️ 待找。** 未检索官方演示视频下载源；07 期制作时查 Google/DeepMind 官方 YouTube（如 Gemini Robotics 2.5 演示片曾成功下载，可复用同路子）或用 Gemini App 真实界面录屏。**缺口：目前无已下载素材。**

## 系列排期建议（供主代理定）

| 期 | 工具 | 状态 | 备注 |
|---|---|---|---|
| 03 | Codex | 策划完成，素材已下载 | 先做这期，见 plan-03-codex.md |
| 04 | Claude Code | 调研完成，素材待下载 | 官方 YouTube 片源已定位，制作时下载 |
| 05 | Muse | 调研完成，素材缺口 | 需先找官方演示片或真实截图 |
| 06 | Grok | 调研完成，素材缺口 | 需先找官方演示片或真实录屏 |
| 07 | Gemini | 调研完成，素材缺口 | 有涨价倒计时钩子，注意 12 月 1 日这个时间点 |

**通用待核实（每期制作前）：** 各家官方定价页直接复核一次（本次多为第三方比价文交叉核对，未逐项直读官方页）；各期涉及的“国内直连用不了”只在描述/口播里提一句，不展开讲绕过方法。
