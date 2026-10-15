// Xuất trang HTML sơ đồ tư duy ra PDF A3 ngang và PNG (khoảng 290 dpi).
// node render_mindmap.js <page.html> <out.pdf> <out.png>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [src, pdf, png] = process.argv.slice(2);
  const browser = await chromium.launch();
  // 420 mm x 297 mm ở 96 dpi = 1587 x 1123 px
  const page = await browser.newPage({ viewport: { width: 1587, height: 1123 }, deviceScaleFactor: 3 });
  await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 30000 });
  const overflow = await page.evaluate(() => {
    const p = document.getElementById('page');
    return { scrollH: p.scrollHeight, clientH: p.clientHeight, font: document.fonts.check('12px "Be Vietnam Pro"') };
  });
  console.log('layout', JSON.stringify(overflow));
  await page.screenshot({ path: png, clip: { x: 0, y: 0, width: 1587, height: 1123 } });
  await page.pdf({ path: pdf, width: '420mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
