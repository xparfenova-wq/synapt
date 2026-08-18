import fs from 'node:fs';
export default async (page) => {
  const manifest = JSON.parse(fs.readFileSync(process.env.MANIFEST, 'utf8'));
  let done = 0;
  for (const it of manifest) {
    await page.setViewportSize({ width: it.w, height: it.h });
    await page.goto('file://' + it.html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    const st = await page.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.weight + ':' + f.status));
    const loaded = st.filter(x => x.endsWith('loaded'));
    if (!loaded.some(x => x.startsWith('Manrope')) || !loaded.some(x => x.startsWith('JetBrains'))) throw new Error('fonts not loaded for ' + it.html + ' ' + st.join(','));
    await page.screenshot({ path: it.png, clip: { x: 0, y: 0, width: it.w, height: it.h } });
    done++;
  }
  return 'ok ' + done;
};
