#!/usr/bin/env node
// 数学可视化视频生产管线 CLI
// 用法：node cli.js <命令> [参数]
// 命令：list | render | cover | music | video | all | init | prompt
const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');
const { findFfmpeg } = require('./lib/ffmpeg');
const { buildPrompt } = require('./lib/prompt');

const ROOT = __dirname;
const CONFIG_PATH = path.join(ROOT, 'config.json');

function loadConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function log(msg) { console.log('  ' + msg); }
function ok(msg) { console.log('✓ ' + msg); }
function err(msg) { console.error('✗ ' + msg); }

function help() {
  console.log(`
数学可视化视频生产管线 CLI

用法: node cli.js <命令> [参数]

命令:
  list              列出所有动画选题和章节
  render <id>       渲染单个视频（截图→合成无音轨）
  cover [id...]     生成封面（默认全部，可指定 id）
  music <style>     生成配乐（style: lie/limit/e/sin/generic）
  video <id>        渲染 + 封面（一条龙）
  all               渲染所有短视频 + 生成所有封面
  init              检查环境依赖是否齐全
  prompt <主题>     生成新选题的动画制作提示词（交给 AI 产出 HTML）

示例:
  node cli.js list
  node cli.js render lie
  node cli.js cover lie limit e
  node cli.js prompt "正态分布为什么无处不在" --type short
  node cli.js all
`);
}

// 检查环境
function checkEnv() {
  console.log('环境检查：');
  // Node
  log(`Node.js: ${process.version}`);
  // Playwright
  try { require('playwright'); ok('playwright 已安装'); }
  catch { err('playwright 未安装，运行 npm install'); }
  // ffmpeg
  const ff = findFfmpeg();
  if (ff) ok(`ffmpeg: ${ff}`);
  else err('未找到 ffmpeg，请安装 imageio-ffmpeg 或设置 FFMPEG 环境变量');
  // Python
  try {
    const py = execSync('python --version 2>&1', { encoding: 'utf8' }).trim();
    ok(`Python: ${py}`);
  } catch { err('Python 未安装'); }
  // 配置文件
  if (fs.existsSync(CONFIG_PATH)) ok('config.json 存在');
  else err('config.json 缺失');
}

// 列出所有选题
function listTopics() {
  const cfg = loadConfig();
  console.log('\n短视频选题：');
  cfg.topics.forEach(t => console.log(`  [${t.id.padEnd(12)}] ${t.name}  (${t.frames}帧, ${t.file})`));
  console.log('\n长视频章节：');
  cfg.chapters.forEach(c => console.log(`  [${c.id.padEnd(12)}] ${c.name}  (${c.frames}帧, ${c.file})`));
}

// 渲染单个视频（截图 → 合成无音轨）
function renderVideo(id) {
  const cfg = loadConfig();
  const topic = cfg.topics.find(t => t.id === id) || cfg.chapters.find(c => c.id === id);
  if (!topic) { err(`未找到选题 "${id}"，用 list 查看`); return; }

  const { width, height, fps, crf, dir } = cfg.output;
  const ffmpeg = findFfmpeg();
  if (!ffmpeg) { err('未找到 ffmpeg'); return; }

  const outSub = path.join(dir, id);
  const outMp4 = path.join(dir, `${id}.mp4`);
  fs.mkdirSync(path.join(ROOT, outSub), { recursive: true });

  ok(`渲染 "${topic.name}" (${topic.frames} 帧)`);
  log('步骤 1/2: 逐帧截图...');
  const cap = spawnSync('node', ['export_capture.js', topic.file, String(topic.frames), id], { cwd: ROOT, stdio: 'inherit' });
  if (cap.status !== 0) { err('截图失败'); return; }

  log('步骤 2/2: ffmpeg 合成...');
  const pattern = path.join(outSub, 'frame_%04d.png');
  const cmd = [ffmpeg, '-y', '-framerate', String(fps), '-i', pattern, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', String(crf), '-preset', 'medium', '-an', outMp4];
  const mux = spawnSync(cmd[0], cmd.slice(1), { cwd: ROOT, stdio: 'inherit' });
  if (mux.status !== 0) { err('合成失败'); return; }

  ok(`完成: ${outMp4}`);
}

// 生成封面
function renderCover(ids) {
  const cfg = loadConfig();
  const all = cfg.covers.cover_topics;
  const targets = (ids && ids.length) ? ids : all;

  // 用 Playwright 渲染（复用 render_43_covers.js 的逻辑）
  const { chromium } = require('playwright');
  (async () => {
    const browser = await chromium.launch({ channel: 'chrome' });
    const outDir = path.join(ROOT, cfg.output.dir, 'covers');
    fs.mkdirSync(outDir, { recursive: true });

    for (const id of targets) {
      for (const s of cfg.covers.sizes) {
        const page = await browser.newPage({ viewport: { width: s.w, height: s.h } });
        const u = 'file://' + path.join(ROOT, 'cover_polish.html').replace(/\\/g, '/') + `?t=${id}&size=${s.id}`;
        await page.goto(u, { waitUntil: 'networkidle' });
        await page.waitForTimeout(300);
        const out = path.join(outDir, `cover_${id}_${s.id}.png`);
        await page.screenshot({ path: out });
        log(`封面 ${id}_${s.id} 完成`);
        await page.close();
      }
    }
    await browser.close();
    ok('全部封面完成');
  })();
}

// 生成配乐
function genMusic(style, duration) {
  const cfg = loadConfig();
  const d = duration || cfg.music.duration;
  const out = path.join(ROOT, cfg.output.dir, `bgm_${style}.wav`);
  const r = spawnSync('python', ['gen_music.py', out, String(d), style], { cwd: ROOT, stdio: 'inherit' });
  if (r.status === 0) ok(`配乐完成: ${out}`);
  else err('配乐生成失败');
}

// 生成新选题提示词
function genPrompt(topic, options = {}) {
  if (!topic) { err('用法: node cli.js prompt <主题> [--type short|chapter] [--duration 秒] [--notes 补充说明]'); return; }

  // 解析参数
  const type = options.type || 'short';
  const duration = parseFloat(options.duration || (type === 'short' ? 20 : 90));
  const notes = options.notes || '';

  const prompt = buildPrompt({ topic, type, duration, notes });
  console.log('\n========== 动画制作提示词 ==========\n');
  console.log(prompt);
  console.log('====================================\n');

  // 同时存成文件，方便复制
  const outFile = path.join(ROOT, `prompt_${Date.now()}.txt`);
  fs.writeFileSync(outFile, prompt, 'utf8');
  ok(`提示词已保存到: ${path.basename(outFile)}`);
  log('把上面提示词发给 AI（如 DSH），拿到 HTML 后放入项目目录，用 render 渲染成片');
}

// 主入口
const [cmd, ...args] = process.argv.slice(2);

// 解析 --key value 形式的参数
function parseOpts(argv) {
  const opts = {};
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const val = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      opts[key] = val;
    } else {
      rest.push(argv[i]);
    }
  }
  return { opts, rest };
}

switch (cmd) {
  case 'list': listTopics(); break;
  case 'render': renderVideo(args[0]); break;
  case 'cover': renderCover(args.length ? args : null); break;
  case 'music': genMusic(args[0], args[1] ? parseFloat(args[1]) : null); break;
  case 'video':
    if (args[0]) { renderVideo(args[0]); renderCover([args[0]]); }
    else err('用法: node cli.js video <id>');
    break;
  case 'all':
    for (const t of loadConfig().topics) renderVideo(t.id);
    renderCover(null);
    break;
  case 'prompt': {
    const { opts, rest } = parseOpts(args);
    genPrompt(rest.join(' '), opts);
    break;
  }
  case 'init': checkEnv(); break;
  default: help(); break;
}
