const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const url = 'file://' + path.join(__dirname, '..', 'cover_benford_v.html').replace(/\\/g, '/');
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(__dirname, '..', 'export', 'covers', 'cover_benford_v.png') });
  console.log('ok');
  await b.close();
})();
