// 通用逐帧截图（可指定画布尺寸，支持竖屏）
// 用法：node tools/capture_any.js <html> <总帧数> <输出子目录> <宽> <高>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const htmlFile = process.argv[2];
const TOTAL_FRAMES = parseInt(process.argv[3] || '510', 10);
const subdir = process.argv[4] || 'frames';
const W = parseInt(process.argv[5] || '1920', 10);
const H = parseInt(process.argv[6] || '1080', 10);

(async () => {
  const OUT_DIR = path.join(__dirname, '..', 'export', subdir);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: W, height: H } });

  const fileUrl = 'file://' + path.join(__dirname, '..', htmlFile).replace(/\\/g, '/') + '?export=1';
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => typeof window.__renderFrame === 'function');

  const canvas = await page.$('#cv');
  for (let n = 0; n < TOTAL_FRAMES; n++) {
    await page.evaluate((f) => window.__renderFrame(f), n);
    const out = path.join(OUT_DIR, `frame_${String(n).padStart(4, '0')}.png`);
    await canvas.screenshot({ path: out });
    if (n % 90 === 0) console.log(`  ${htmlFile} ${n}/${TOTAL_FRAMES}`);
  }
  await browser.close();
  console.log(`done: ${htmlFile} -> ${OUT_DIR} (${W}x${H})`);
})();
