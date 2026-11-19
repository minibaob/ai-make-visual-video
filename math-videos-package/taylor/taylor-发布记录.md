# 泰勒公式 · 发布记录

抖音：小影数学（07050908kkk）

- 计划发布时间：2026-11-19 08:00（北京时间），公开。由主聊安排发布，本视频未自行发布。
- 视频：taylor-30s-1080x1920-voiced.mp4（Manim，30 秒，1080×1920，30fps，H.264 CRF 18 yuv420p，带旁白）；静音版 taylor-30s-1080x1920.mp4；竖版封面 taylor-cover-1080x1920.png（带「每天一个可视化概念」胶囊，视频内无胶囊、无关注引导）。
- 标题（建议）：每天一个可视化概念 sin x 拆成多项式（短版备用：sin x 也能拆成多项式）
- 正文（建议）：sin x 这条曲线，看着弯弯绕绕，其实就是 x − x³/6 + x⁵/120 − x⁷/5040，多项式一项一项往上加，贴得越来越远。七次就已经几乎分不出来了。你猜 cos x 拆开，第一项是什么？
- 话题（建议）：#数学 #高等数学 #泰勒公式
- 合集：「每天一个可视化概念——高数」第 14 集（接地球腰带第 13 集）。

## 数学（已验算，精确）

- sin x = x − x³/3! + x⁵/5! − x⁷/7! = x − x³/6 + x⁵/120 − x⁷/5040
- P1 = x；P3 = x − x³/6；P5 = x − x³/6 + x⁵/120；P7 = x − x³/6 + x⁵/120 − x⁷/5040
- 验算（x=1.0）：sin=0.841471，P1=1.000000，P3=0.833333，P5=0.841667，P7=0.841471（脚本内打印核对过）
- 画面：0 秒 sin 曲线 + 一次直线已在屏上；三次（绿）、五次（红）、七次（白）依次贴合，越贴越远；20–25 秒全式上屏；结尾定格公式 + “再复杂的曲线，都是多项式拼出来的”。

## 配音（6 段，晓晓 +10%，每段一个 5 秒窗口，已 ASR 验过）

1. 0–5s：这条曲线是 sin x（2.42s）
2. 5–10s：直线只能贴住中间一小段（2.64s）
3. 10–15s：三次多项式，贴得更远（2.62s）
4. 15–20s：五次，七次，越贴越远（2.81s）
5. 20–25s：这就是泰勒公式（1.94s）
6. 25–30s：再复杂的曲线，都是多项式拼出来的（3.43s）
- ASR 核查：6 段全部在其窗口内听到（ faster-whisper small；“sin x”听成 SynX、“多项式”听成“多向式”属同音误听，以时间戳和关键词为准）。

## 文件

- ~/workspace/imagine_media/taylor-30s-1080x1920-voiced.mp4（成片，30.000s）
- ~/workspace/imagine_media/taylor-30s-1080x1920.mp4（静音版）
- ~/workspace/imagine_media/taylor-cover-1080x1920.png（竖版封面）
- ~/workspace/imagine_media/taylor-manim-30s.py（Manim 脚本）
- ~/workspace/imagine_media/make_taylor_narration.py（旁白生成脚本）
- ~/workspace/imagine_media/taylor-narration/seg1–6.mp3（旁白分段）
- ~/workspace/imagine_media/mux_taylor.py（混音脚本）
- ~/workspace/imagine_media/verify_taylor_mux.py（ASR 核查脚本）
- ~/workspace/imagine_media/make_taylor_cover.py（封面生成脚本）

## 制作说明（供下次复用）

- 本机 texlive 已不在（VM 换过，`latex` 命令缺失），公式没用 MathTex，改用纯 Text + Unicode 上标（x³/x⁵/x⁷、−、≈），字形已验过能正常显示；fit_width 限宽 4.2u 防溢出。
- y 轴标签不要放轴顶正上方，会撞上副标题；已改到轴右侧下方（0.30, 1.30），t7 帧复核通过。
- 渲染：Manim 0.22.1，config.frame_width = 4.5，不传 -qm；成品 1080×1920、30.000s、H.264 + AAC 已 ffprobe 核对；t0/t7/t12/t17/t22/t24/t28 逐帧看过，曲线、多项式、公式、字幕均无裁切，首帧已有曲线+直线。

## 实际发布

- 2026-11-19 08:05 已发布，公开可见，审核约 1 分钟通过；抖音视频 ID `7709666859989208374`，链接 https://www.douyin.com/video/7709666859989208374；合集「每天一个可视化概念——高数」第 14 集；作品总数 33→34。
- 标题与话题按建议发布：标题「每天一个可视化概念 sin x 拆成多项式」，话题 #数学 #高等数学 #泰勒公式。
