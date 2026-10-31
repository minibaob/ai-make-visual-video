// 通用逐帧截图脚本
// 用法：node export_capture.js <html文件名> <总帧数> [输出子目录]
// 例：node export_capture.js topic1.html 510 topic1
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const htmlFile = process.argv[2] || 'derivative-tangent.html';
const TOTAL_FRAMES = parseInt(process.argv[3] || '510', 10);
const subdir = process.argv[4] || 'frames';
const W = 1920, H = 1080;

(async () => {
  const OUT_DIR = path.join(__dirname, 'export', subdir);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: W, height: H } });

  const fileUrl = 'file://' + path.join(__dirname, htmlFile).replace(/\\/g, '/') + '?export=1';
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => typeof window.__renderFrame === 'function');

  const canvas = await page.$('#cv');
  for (let n = 0; n < TOTAL_FRAMES; n++) {
    await page.evaluate((f) => window.__renderFrame(f), n);
    const out = path.join(OUT_DIR, `frame_${String(n).padStart(4, '0')}.png`);
    await canvas.screenshot({ path: out });
    if (n % 60 === 0) console.log(`  ${htmlFile} frame ${n}/${TOTAL_FRAMES}`);
  }

  await browser.close();
  console.log(`done: ${htmlFile} -> ${OUT_DIR}`);
})();
