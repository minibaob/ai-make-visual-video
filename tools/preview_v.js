// 竖屏预览：指定 html + 帧号，按 1080x1920 截图
// 用法：node tools/preview_v.js <html> <输出目录> <帧号...>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const htmlFile = process.argv[2];
const outDir = process.argv[3];
const frames = process.argv.slice(4).map(Number);
const W = 1080, H = 1920;

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const fileUrl = 'file://' + path.join(__dirname, '..', htmlFile).replace(/\\/g, '/') + '?export=1';
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => typeof window.__renderFrame === 'function');
  const canvas = await page.$('#cv');
  for (const f of frames) {
    await page.evaluate((n) => window.__renderFrame(n), f);
    const out = path.join(outDir, `${path.basename(htmlFile, '.html')}_f${f}.png`);
    await canvas.screenshot({ path: out });
    console.log(out);
  }
  await browser.close();
})();
