/* Real browser checks of discovery and mobile usability. */
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const root = path.resolve(process.env.FREE_TOOLS_SITE_ROOT || path.join(__dirname, '../docs'));
const data = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json')));
const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404); res.end(); return; }
  const mime = {'.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.json':'application/json', '.svg':'image/svg+xml'};
  res.setHeader('Content-Type', mime[path.extname(file)] || 'text/plain'); res.end(fs.readFileSync(file));
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? {executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE} : {})});
    const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.goto(`http://127.0.0.1:${server.address().port}/`, {waitUntil:'networkidle'});
    assert.equal(await page.locator('#provider-count').innerText(), String(data.providers.length));
    assert.equal(await page.locator('.provider').count(), 20);
    await page.locator('#next').click(); assert.match(await page.locator('#page-number').innerText(), /Page 2/);
    await page.locator('#search').fill('deepgram');
    assert.equal(await page.locator('.provider').count(), 1);
    assert.match(await page.locator('.allowance').innerText(), /\$200/);
    await page.locator('details summary').click(); assert.match(await page.locator('details').innerText(), /No card required/);
    await page.locator('#offer').selectOption('recurring'); assert.equal(await page.locator('.provider').count(), 0);
    assert.equal(await page.locator('#pagination').isVisible(), false);
    await page.locator('#reset').click(); await page.locator('#free-only').check();
    const freeCount = data.providers.filter(p => ['recurring','trial','grant','open_source'].includes(p.offer.kind)).length;
    assert.equal(await page.locator('#result-count').innerText(), `${freeCount} providers`);
    await page.locator('#reset').click(); await page.locator('#mcp-only').check();
    const mcpCount = data.providers.filter(p => ['official','community'].includes(p.mcp.support)).length;
    assert.equal(await page.locator('.provider').count(), mcpCount);
    assert.equal(await page.locator('a').filter({hasText:'MCP setup ↗'}).count(), mcpCount);
    await page.reload({waitUntil:'networkidle'}); assert.equal(await page.locator('#mcp-only').isChecked(), true);
    await page.locator('#reset').click();
    if (process.argv[2]) await page.screenshot({path:process.argv[2], fullPage:true});
    await page.setViewportSize({width:390,height:844});
    await page.locator('#category-mobile').selectOption('speech');
    assert.equal(await page.locator('.provider').count(), data.providers.filter(p => p.categories.includes('speech')).length);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, 'Mobile page overflows');
    assert.equal(await page.locator('#category-mobile').isVisible(), true);
    await page.locator('#search').fill('no-such-capability'); assert.equal(await page.locator('.empty').count(), 1);
    assert.deepEqual(errors, []);
    console.log('Passed: browser search, offer eligibility, pagination, free/MCP filters, URL restore and mobile layout');
  } finally {
    if (browser) await browser.close(); server.close();
  }
})().catch(e => {console.error(e); process.exitCode = 1;});
