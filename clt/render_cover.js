// 生成《中心极限定理》封面：横版 16:9 + 竖版 9:16
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const outDir = path.join(__dirname, '..', 'export', 'covers');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome' });
  const jobs = [
    { id: '16x9', w: 1920, h: 1080, q: '' },
    { id: '9x16', w: 1080, h: 1920, q: '?size=916' }
  ];
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    const url = 'file://' + path.join(__dirname, 'clt_cover.html').replace(/\\/g, '/') + j.q;
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);
    const out = path.join(outDir, `cover_clt_${j.id}.png`);
    await page.screenshot({ path: out });
    console.log(out);
    await page.close();
  }
  await browser.close();
})();
