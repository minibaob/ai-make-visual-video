// 提示词生成器：根据用户输入的主题/章节，生成符合项目规范的动画制作提示词
// 用户拿着这份提示词交给任意大模型（如 DSH），产出符合规范的 HTML 动画

// 项目的技术规范（固化进提示词，确保 AI 生成的代码能直接接入管线）
const SPEC = `
## 必须遵守的技术规范

### 1. 三幕结构（用帧号控制时间轴）
- 片头钩子（约 75 帧 ≈ 2.5 秒）：反常识金句，白字 + 黄色高亮关键词
- 动画主体：核心概念的可视化演示
- 结尾定格卡（约 90 帧 ≈ 3 秒）：总结句 + 关注引导「每天一个可视化概念」

### 2. 确定性帧驱动（关键，否则逐帧截图会漂移）
- 不要用 requestAnimationFrame 的 dt 累加做动画
- 每帧由帧号 frame 精确算出所有状态（位置、角度、进度）
- 必须暴露 window.__renderFrame = (n) => { setFrame(n) }，供截图脚本调用
- 提供 ?export=1 导出模式：隐藏控制按钮和标签，stage 设为 1920×1080

### 3. 配色规范（统一视觉）
- 背景深黑 #0A0A0F，径向渐变提亮顶部
- 蓝色 #58C4DD（曲线/主体）
- 黄色 #FFD93D（切线/强调/高亮词）
- 红色 #FF6B6B（割线/误差/警告）
- 绿色 #83C167（公式/积分/正向）
- 等宽字体 "JetBrains Mono"

### 4. 坐标轴（必须标实数刻度）
- x/y 轴要画刻度数字，刻度步长取「整齐数」（1/2/5 × 10^n）
- 放大动画时步长要自适应（niceStep 算法），避免刻度糊成一团
- 刻度数字用 rgba(220,220,235,0.9)，字号约 15px

### 5. 画布与导出
- canvas id 必须是 "cv"，外层容器 id 建议 "stage"
- 代码自包含在一个 HTML 文件里，内联 CSS 和 JS，不依赖外部资源
- 曲线用高采样点（≥400 点）绘制，避免放大时出现折线

## 输出要求
- 只输出一个完整的 HTML 文件，用 \`\`\`html 代码块包裹
- 文件名建议：topicN_<英文关键词>.html
- 代码要能直接打开预览，也要能配合 export_capture.js 逐帧截图
`;

function buildPrompt(input) {
  const { topic, type, duration, notes } = input;
  const typeText = type === 'short' ? '短视频（17-23 秒，三幕结构）' : '长视频章节（40-120 秒，讲解结构）';
  const notesText = notes ? `\n\n## 补充要求\n${notes}` : '';

  return `你是一个数学可视化动画专家，擅长制作 3Blue1Brown 风格的科普动画。请用 HTML + Canvas 制作一个数学可视化动画。

## 选题信息
- 主题：${topic}
- 类型：${typeText}
- 时长：约 ${duration} 秒（30fps，即约 ${Math.round(duration * 30)} 帧）

${SPEC}${notesText}

请开始生成。
`;
}

module.exports = { buildPrompt };
