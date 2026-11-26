# 抖音 AI 视频 02 号计划：机器人上奔驰产线

> 账号：小影数学（07050908kkk），AI 视频是新线，和数学内容并存。
> 形式纠正（用户 2026-11-26 12:24）：不要 Manim 画全片，找真实视频素材、像人一样剪辑。从 02 号起按这个做。
> 状态：成片已完成（2026-11-26），未发布，由主代理发布。来源行因一行超宽改为两行；混音曾因 amix duration=first 只剩 2.8 秒音频，已改 duration=longest 重建并 ASR 验过。

## 事实（已核实，2026-11-26 查）

| 事实 | 数值 | 来源 |
|---|---|---|
| Gemini Robotics 2.5 发布 | 2026 年 11 月 10 日，Google DeepMind 博客 | deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/（一级来源，原文已读） |
| 奔驰产线分拣成功率 | 96%（Apptronik Apollo 2 人形机器人，金属支架分拣进 sequencing tray） | DeepMind 博客原文："pick and pack automotive parts with a 96% success rate" |
| 产线地点 | 匈牙利凯奇凯梅特、德国辛德尔芬根，真产线（active production lines） | DeepMind 博客；the-decoder、interestingengineering、dev.to 交叉确认 |
| 200+ 任务 | 成功率比上一代高 30–100%，快 20–30% | DeepMind 博客 |
| 96% 的 caveat（片里必须说） | 厂商说法：未公布试验次数、未定义何为成功、奔驰未单独确认 | TechTimes、datastudios.org、robottesters.com 均指出；DeepMind 原文无试验次数 |
| 演示画面 2 倍速 | 工厂演示视频按 2 倍速播放 | Ars Technica（robottesters.com 引用）；素材右上角自带 "Autonomous 2x" 字样 |
| 合作方 | Apptronik Apollo 2（五指 SharpaWave 手，22 自由度）；ER 模型管流程，2.5 管手臂 | DeepMind 博客 |
| 部署状态 | 概念验证（proof-of-concept），只向合作伙伴 rollout，无公开 API | DeepMind 博客；dev.to |

## 素材（真实视频，全部有来源）

| 素材 | 内容 | 来源 | 授权/说明 |
|---|---|---|---|
| apollo-mercedes-official.webm | Google 官方演示：Apollo 2 在辛德尔芬根产线分拣，1920×1080，25.96 秒，VP9+Opus | the-decoder.com 嵌入的 Google 官方视频：https://the-decoder.com/wp-content/uploads/2026/11/GR_Apptronik_x_Mercedes_v1_1000k.webm | Google 官方发布素材，新闻转载用；片尾白底 logo 卡（约 20 秒起）不用，只用 0–19.3 秒实拍部分；画面右上角自带 "Autonomous 2x"，保留（诚实说明 2 倍速） |
| bgm-mixkit.mp3 | Mixkit《Smile》，音量 0.5 | 已有文件（1 号用过） | Mixkit 免费音乐 |

不用 Pexels B-roll：官方实拍 26 秒已够整条 20 秒片子，没必要拼通用素材。

## 分镜（竖版 1080×1920，约 20 秒，真实镜头剪辑）

版式：模糊背景填满 1080×1920（原片高斯模糊+压暗），16:9 实拍居中（1080×607），上方放大字、下方字幕——人剪新闻短视频的常规做法。
字幕克制：每段一句白字+半透明黑底，只在画面下方出现；大字只在钩子（96%）和结尾数字处出现。

| 时间 | 画面（实拍） | 屏上字 | 口播 |
|---|---|---|---|
| 0–3.2 秒 | 0.0–3.2s：机器人头部特写 → 伸手进蓝筐 | 大字 96%（黄）+ 奔驰产线 分拣成功率（白） | S1 |
| 3.2–6.5 秒 | 3.2–6.5s：手部特写，拿零件（带 Gemini Robotics 2.5 原片标题） | 无 | S2 |
| 6.5–10 秒 | 6.5–10s：全景，机器人把零件放进分拣盘 | 无 | S3 |
| 10–13 秒 | 10–13s：全景，另一轮拿取 | 小字：厂商说法 · 未公布试验次数 | S4 |
| 13–16.2 秒 | 13–16.2s：全景，伸手 | 无 | S5 |
| 16.2–19.6 秒 | 16.2–19.3s：全景，机器人继续工作（19.3 秒后是片尾 logo 卡，不用） | 小字：来源：Google DeepMind 2026.11.10 · 画面：官方演示（2倍速） | S6 |

## 口播文案（口语化，去 AI 味；陈述句结尾，不提问；视频内无关注号召）

| 段 | 文案 | 字数 |
|---|---|---|
| S1 | 奔驰产线上来了个机器人 | 11 字 |
| S2 | 分拣零件，成功率96% | 10 字 |
| S3 | 在匈牙利和德国的真产线上 | 12 字 |
| S4 | 不过这数是厂商自己说的 | 11 字 |
| S5 | 做了多少次，它没公布 | 10 字 |
| S6 | 100次里错4次，产线还不敢全靠它 | 15 字 |
| 合计 | | 69 字 |

- 96% → 100 次里错 4 次是算术换算（100−96=4），和 1 号算术题同款引擎，辩论点在评论区。
- S4/S5 的依据：TechTimes、datastudios、robottesters 均指出 DeepMind 未公布试验次数、成功定义、人工干预情况，奔驰未单独确认 96%。

**标题（14 字）：** 机器人进奔驰工厂，成功率96%

**发布文案（描述）：**
> Google DeepMind 11月10日发布 Gemini Robotics 2.5，Apptronik 的 Apollo 2 人形机器人在奔驰匈牙利和德国的真产线上分拣零件，成功率 96%。这是厂商公布的数字，做了多少次没公布，100 次里就是错 4 次。

**标签：** #AI #人形机器人 #人工智能 #奔驰 #Gemini

## 制作参数

- 剪辑：ffmpeg（模糊背景 + 居中实拍 + PIL 渲染的文字 PNG 叠加，不用 Manim 画全片；Manim 本条不用）
- 配音：6 句分别用 raw_edge_tts.py 生成（zh-CN-XiaoxiaoNeural，+10%），逐句核时长再拼
- 音乐：bgm-mixkit.mp3 音量 0.5，ffmpeg baked 进文件；静音版和混音版分开命名
- 校验：ffprobe 确认有音频流；ASR 听一遍口播；逐段抽帧看画面、字幕有无出画；总时长约 20 秒；第一帧就是机器人特写 + 96% 大字

## 文件

- 计划：~/workspace/douyin-ai-video/plan-02.md
- 素材：~/workspace/douyin-ai-video/media/robot02/apollo-mercedes-official.webm
- 配音：~/workspace/douyin-ai-video/tts2/seg1–6.mp3
- 成片：~/workspace/imagine_media/robot-mercedes-20s-1080x1920.mp4（混音版，发布用）、robot-mercedes-20s-1080x1920-silent.mp4（静音版）
- 封面：~/workspace/imagine_media/robot-mercedes-cover-1080x1920.png
- 制作脚本：~/workspace/douyin-ai-video/gen_tts2.py、build_video02.py、gen_cover02.py
