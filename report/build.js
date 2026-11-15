// Renders report/report.html to FlipRate_report.pdf (US Letter, as in the Apart template).
// Usage: node report/build.js      (needs Playwright with Chromium)
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'report.html'));
  await page.evaluate(() => document.fonts.ready);
  const words = await page.evaluate(() => document.getElementById('abstract').innerText.trim().split(/\s+/).length);
  console.log('abstract words:', words);
  await page.pdf({
    path: path.join(__dirname, '..', 'FlipRate_report.pdf'), format: 'Letter', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-size:8pt;font-family:serif;color:#444"><span class="pageNumber"></span></div>',
  });
  await browser.close();
})();
