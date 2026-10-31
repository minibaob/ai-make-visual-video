// 渲染封面：6 选题 × 2 尺寸（横版 4:3 + 竖版 9:16）
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const topics = ['tangent', 'lie', 'limit', 'e', 'sin', 'zoom', 'weierstrass', 'fourier', 'calculus'];
const sizes = [
  { name: '43',  w: 1440, h: 1080 },  // 横版 4:3
  { name: '916', w: 1080, h: 1920 },  // 竖版 9:16
];

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const outDir = path.join(__dirname, 'export', 'covers');
  fs.mkdirSync(outDir, { recursive: true });

  for (const t of topics) {
    for (const s of sizes) {
      const page = await browser.newPage({ viewport: { width: s.w, height: s.h } });
      const u = 'file://' + path.join(__dirname, 'cover_polish.html').replace(/\\/g,'/') + `?t=${t}&size=${s.name}`;
      await page.goto(u, { waitUntil: 'networkidle' });
      await page.waitForTimeout(300);
      const out = path.join(outDir, `cover_${t}_${s.name}.png`);
      await page.screenshot({ path: out });
      console.log(`  ${t}_${s.name} ok`);
      await page.close();
    }
  }
  await browser.close();
  console.log('ALL_COVERS_DONE');
})();
