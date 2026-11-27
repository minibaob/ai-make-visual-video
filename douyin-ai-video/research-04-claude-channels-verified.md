# 第 04 期 Claude Code：9 个渠道逐个核实（2026-11-26）

> 用途：11 月 28 日那期（合集系列第 04 期，Claude Code）制作前核对。格式沿用 03B：横屏 1920×1080 动画信息图 + 真实素材插图，不限时长。
> 核实时间：2026-11-26 晚。价格均为美元原价、不含税；人民币按约 6.65 折算，仅作口头参考。
> 原则：只写核实过的数，不照抄阿星视频的结论。阿星视频（2026-10-30，6 分 14 秒，2.5 万赞 / 1.9 万收藏）只取公式（合集盘点 + 逐个一句话 verdict + 汇总）。

## 官方价（已核实，沿用 research-03 的结论，多方交叉一致）

| 渠道 | 价格 | 能得到什么 | verdict |
|---|---|---|---|
| 官方 Claude Pro | $20/月（年付 $200，约 $17/月） | Claude Code，默认 Opus 5.5；5 小时 + 每周限量 | **最值** |
| 官方 Max | $100/月 | Pro 用量 5 倍 | 重度 |
| 官方 Ultra（原 Max 20x，2026-10 改名，价未变） | $200/月 | 每周用量 10 倍 Pro，认证账号无 5 小时限制 | 土豪 |
| 官方 API 按量 | 无订阅 | Opus 5.5 $4 输入 / $20 输出 每百万 token；Sonnet 5.5 $2/$10；Haiku 5.5 $0.10/$0.50 | 灵活 |
| 免费档 | $0 | **不含 Claude Code** | 上不了 |

来源：Anthropic 官网定价页，经 cloudzero 2026-11-24、faros.ai 2026-11-18、dev.to 2026-11-23 三家比价文交叉核对，数字一致。待办：制作前直接打开 claude.com/pricing 再复核一次（research-03 原注）。

## 第三方渠道（逐个核实结果）

### 1. Cursor —— ⚠️ 变了，阿星视频时的 $20 包 Claude 已成过去

- 2026-10-12 起 Cursor 并入 The X Subscription：Free $0 / Plus $8 / Premium $30 / Super $100 / Ultra $200（年付 $80/$300/$1000/$2000）。
- Claude、GPT、Gemini **不在任何档的包含额度里**：Premium 及以上按 API 原价另付（Opus 5.5 $4/$20），需先充 prepaid credit；Plus 和 Free 根本用不了 Claude。
- 老 Pro $20 / Pro+ $60 仅限老用户续用，新用户买不到。
- 结论：现在走 Cursor 用 Claude，最低门槛是 **$30/月 + 按量另付**，不是 $20 全包。这一条是本期最值得讲的变化——阿星视频 10 月 30 日发布，已在改制之后，片中 Cursor 那段需以新结构为准，不能照抄。
- 来源：fastero.com 2026-11-12 核对、tailkits.com 2026-11-23 实读 cursor.com/pricing、aibizhub.io 2026-10-19 核对，三家一致。

### 2. Kiro（AWS）—— 0 元能摸到 Claude

- Free $0：每月 50 credits，含 Claude Sonnet 4.5（老款）+ 开源模型，有限流。
- Pro $20/月（1000 credits）、Pro+ $40（2000）、Pro Max $100（5000）、Power $200（10000）；额外 credits $0.04/个。
- 付费档有 Claude Opus 5.5 / Sonnet 5.5：Opus 约 2 倍 credits、Sonnet 约 1.3 倍（以 Auto 为 1×）。
- 注意：Kiro 不支持自带 key；另外 Claude Code 的扩展能装进 Kiro 里（Kiro Free + Claude Pro $20 组合也成立）。
- 来源：tailkits.com 2026-10-21 实读 kiro.dev/pricing、enjoy.dev 2026-11-12 核对、caprock.dev 2026-10-10 核对，一致。

### 3. GitHub Copilot —— 最便宜的 Sonnet 入口 $10

- Pro $10/月：含 Claude Sonnet 5.5 / Haiku 5.5，**不含 Opus 5.5**；每月 1500 AI credits（1000 基础 + 500 flex）。
- Pro+ $39/月：含 Claude Opus 5.5、Fable 5.2；每月 7000 credits。Max $100/月：20000 credits。
- 2026-06-01 起全部按 AI credits 计费（1 credit = $0.01，按模型 token 价扣）。
- 来源：datastudios.org 2026-11-16 核对 GitHub 官方计划页、benchleader.com 2026-10-30 实读，一致。

### 4. 谷歌 Antigravity —— $20 双模型，但免费档的 Claude 11 月 30 日就没了

- 免费档 $0：每周额度；Claude Sonnet 4.6 / Opus 4.6 免费档可用到 **2026-11-30**，之后移除（日期已推迟过一次，11 月 2 日 → 11 月 18 日 → 11 月 30 日，以官方页为准）。
- Google AI Pro $19.99/月（须是付费订阅，试用版不算）：含 Claude Sonnet 5.5 + Opus 5.5，另有 Gemini 4 Neon（默认编排器）、Argon、Hydrogen。
- Ultra $99.99 / $199.99：5 倍 / 20 倍用量，另有 Gemini 4 Carbon。
- 结论：Pro $19.99 是“一个价同时拿到 Claude + Gemini 4 Neon”的档，适合和官方 Pro $20 对比着讲。
- 来源：tailkits.com 2026-11-23 实读 antigravity.google、pick-right.com 2026-11-03 核对、voyager.so 2026-10-20 核对，一致。

### 5. Devin —— $20 起，但计费方式有冲突，片中别写死 ACU 数字

- 入门都是 $20/月起（Core / Pro），Max $200/月。
- ⚠️ 计费口径冲突：2026 年 8 月一篇实读 Devin 定价页的文章称 ACU 已于 2026-03 取消，改为每日 + 每周 token 额度、超量按 API 原价；但 2026 年 9 月 1 日另一篇仍写 Core $20 + $2.25/ACU、Team $500/月含 250 ACU。
- 处理：片中只说“$20 起，按用量另算，重度用下来几百美元”，**不要出现 $2.25/ACU 或 Team $500 这类数字**；制作前打开 devin.ai/pricing 复核一次。
- 另注意：Devin 是独立的自主 agent（自己接单干活、开 PR），不是 Claude Code 本体，只是底层跑 Claude 模型——讲的时候别把它说成“Claude Code 的一个入口”。
- 来源：continuumcode.ai（2026-08-07 实读定价页）vs laracopilot.com（2026-09-01），结论冲突，已标注。

### 6. Kilo Code —— 0 元工具，只付模型钱

- 开源 MIT，VS Code / JetBrains / CLI 免费；自带 Anthropic key 用 Claude，Kilo 不加价（Opus 5.5 就是官方价 $4/$20）。
- 也可以走 Kilo Gateway（官方价，无加价，但充值收 5% 手续费）或 Kilo Pass $19/$49/$199 月付（送 bonus credits）。
- 另有免费模型、本地模型（Ollama / LM Studio）两条 0 元路；云端 agent 另按 $0.60–$1.20/小时收算力。
- 2026-07 Anaconda 收购了 Kilo，未来定价以官方页为准。
- 来源：testedintelligence.com 2026-11-07 实读官网、academy.techpresso.co 2026-11-09 核对、shortlisted.tools，一致。

### 7. Version —— ⚠️ 未能确认是哪款工具，制作前必须重看原视频

- 两次搜索（英文 + 中文）均未找到名叫 Version、能接 Claude Code 的编程工具。
- 阿星视频章节表（reference-axing-claudecode.md）写的是 05:16 Version，可能是原视频字幕/转录误差（候选：Vercel v0？Windsurf？某中转站？均无证据）。
- 处理：制作前重看原视频 05:16 处核对；确认不了就从本期去掉，改成 8 个已核实的渠道，**不要把没核实的名字放进视频**。

### 8. Opencode —— 0 元工具，Claude 按量付

- 开源 MIT，终端 / 桌面 / IDE 扩展免费；接 200+ 供应商，Claude 需自带 Anthropic API key，或走 OpenCode Console 按量（4.6% + $0.31 手续费）。
- OpenCode Go $10/月（含 33 个模型，其中 Haiku 5.5；**不含 Opus 5.5 / Sonnet 5.5**，那两个仍需自己付 API 钱）；Go Plus $40/月。
- 来源：dev.to 2026-11-25 核对（价格核对于 2026-11-09）、getorchestra.io（2026-09 核对）、opencode.asia，一致。

## 本期可用的 3 个钩子（都已核实）

1. **Cursor 变贵了**：以前 $20 包 Claude，现在新用户最低 $30/月还得按量另付——这是阿星视频之后最大的变化，也是本期最有信息量的点。
2. **$10 就能摸到 Sonnet**：GitHub Copilot Pro $10/月含 Sonnet 5.5，是 9 个渠道里最便宜的 Claude 入口；但 Opus 5.5 得加到 Pro+ $39。
3. **0 元路有两条**：Kiro 免费档（Sonnet 4.5）+ Kilo / Opencode 自带 key（工具 0 元，只付模型钱）；Antigravity 免费档的 Claude 只剩到 11 月 30 日，讲的时候要加一句“月底就没了”。

## 大陆用户注意（沿用 research-03 口径，制作前复核）

- Anthropic 官方支持名单无中国大陆、香港、澳门（2026-11-06 比对；2026-11-12 生效的 Supported Regions Policy 同样不含中国大陆）。官方订阅需境外支付。
- 各第三方渠道的大陆可用性与支付方式，阿星视频里按“是否支持大陆主流支付、能否脱离 harness、是否对大陆用户有限制”打分——本文件未逐项核实，片中涉及大陆支付的表述需制作时再核，或只讲价格、不讲支付。

## 待办（制作时）

- [ ] 打开 claude.com/pricing 复核官方三档价
- [ ] 打开 devin.ai/pricing 复核 Devin 当前计费（ACU 是否还在）
- [ ] 重看阿星原视频 05:16，确认 Version 是什么；确认不了就去掉
- [ ] 打开 antigravity.google/models 确认免费档 Claude 4.6 是否已于 11 月 30 日移除（本期 11 月 28 日发，播出时还剩 2 天，可讲“只剩 2 天”）
- [ ] 下载 Anthropic 官方 YouTube 片源（research-03 已定位 3 条：AJpK3YTTKZ4 / 6eBSHbLKuN0 / gv0WHhKelSE），只用终端实操段
