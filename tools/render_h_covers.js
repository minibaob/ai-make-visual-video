const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const outDir = path.join(__dirname, '..', 'export', 'covers');
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch({ channel: 'chrome' });
  const jobs = [['cover_benford_h.html', 'cover_benford_4x3.png'], ['cover_pi_h.html', 'cover_pi_4x3.png']];
  for (const [src, out] of jobs) {
    const p = await b.newPage({ viewport: { width: 1440, height: 1080 } });
    await p.goto('file://' + path.join(__dirname, '..', src).replace(/\\/g, '/'), { waitUntil: 'networkidle' });
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(outDir, out) });
    console.log(out);
    await p.close();
  }
  await b.close();
})();
