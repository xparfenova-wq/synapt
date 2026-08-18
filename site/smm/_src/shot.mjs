// Рендер HTML-слайдов в PNG и SVG (текст остаётся текстом, переносы строк как в браузере)
// запуск: MANIFEST=…/manifest.json node <browser-automation>/browser.mjs about:blank --script shot.mjs
import fs from 'node:fs';
import path from 'node:path';

const extract = () => {
  const NS = 'http://www.w3.org/2000/svg';
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const num = v => Math.round(v * 100) / 100;
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  const out = [];
  const canvas = document.createElement('canvas'); const ctx = canvas.getContext('2d');
  const ascCache = {};
  const ascent = (fam, weight, size) => {
    const k = fam + '|' + weight + '|' + size;
    if (!(k in ascCache)) { ctx.font = `${weight} ${size}px "${fam}"`; ascCache[k] = ctx.measureText('Hxg').fontBoundingBoxAscent; }
    return ascCache[k];
  };
  const fam = ff => /jetbrains/i.test(ff) ? 'JetBrains Mono' : 'Manrope';
  const color = c => {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return { hex: c, a: 1 };
    const p = m[1].split(',').map(x => parseFloat(x));
    const hex = '#' + p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
    return { hex, a: p.length > 3 ? p[3] : 1 };
  };
  const rectEl = (r, cs) => {
    const bg = color(cs.backgroundColor);
    const bw = parseFloat(cs.borderTopWidth) || 0, bl = parseFloat(cs.borderLeftWidth) || 0;
    const rad = Math.min(parseFloat(cs.borderTopLeftRadius) || 0, r.width / 2, r.height / 2);
    if (bg.a > 0) out.push(`<rect x="${num(r.left)}" y="${num(r.top)}" width="${num(r.width)}" height="${num(r.height)}" rx="${num(rad)}" fill="${bg.hex}"${bg.a < 1 ? ` fill-opacity="${bg.a}"` : ''}/>`);
    if (bw > 0 && bl > 0) {
      const bc = color(cs.borderTopColor);
      if (bc.a > 0) out.push(`<rect x="${num(r.left + bw / 2)}" y="${num(r.top + bw / 2)}" width="${num(r.width - bw)}" height="${num(r.height - bw)}" rx="${num(Math.max(0, rad - bw / 2))}" fill="none" stroke="${bc.hex}"${bc.a < 1 ? ` stroke-opacity="${bc.a}"` : ''} stroke-width="${bw}"/>`);
    } else if (bl > 0) {
      const bc = color(cs.borderLeftColor);
      if (bc.a > 0) out.push(`<rect x="${num(r.left)}" y="${num(r.top)}" width="${bl}" height="${num(r.height)}" fill="${bc.hex}"/>`);
    }
  };
  const textNode = (n) => {
    const el = n.parentElement; const cs = getComputedStyle(el);
    if (!n.data.trim()) return;
    const size = parseFloat(cs.fontSize), weight = cs.fontWeight, f = fam(cs.fontFamily);
    const ls = cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing);
    const asc = ascent(f, weight, size);
    const fill = color(cs.color);
    const lines = []; // {top, cells:[{ch,left,right}]}
    const range = document.createRange();
    for (let i = 0; i < n.data.length; i++) {
      range.setStart(n, i); range.setEnd(n, i + 1);
      const rs = range.getClientRects(); if (!rs.length) continue;
      const r = rs[0]; if (r.width === 0 && /\s/.test(n.data[i])) continue;
      let L = lines.find(l => Math.abs(l.top - r.top) < 2);
      if (!L) { L = { top: r.top, cells: [] }; lines.push(L); }
      L.cells.push({ ch: n.data[i], left: r.left, right: r.right });
    }
    for (const L of lines) {
      // пробелы по краям строки не считаем: координата строки от первого глифа
      const cells = L.cells.slice();
      while (cells.length && /\s/.test(cells[0].ch)) cells.shift();
      while (cells.length && /\s/.test(cells[cells.length - 1].ch)) cells.pop();
      if (!cells.length) continue;
      const t = cells.map(c => c.ch).join('').replace(/\s+/g, ' ');
      L.left = Math.min(...cells.map(c => c.left)); L.right = Math.max(...cells.map(c => c.right));
      const style = `font-family="${f}" font-size="${size}" font-weight="${weight}"${ls ? ` letter-spacing="${num(ls)}"` : ''} fill="${fill.hex}"${fill.a < 1 ? ` fill-opacity="${fill.a}"` : ''}`;
      const prev = out[out.length - 1];
      // соседний фрагмент той же строки и того же стиля (nowrap-спаны) склеиваем в одну строку
      if (prev && typeof prev === 'object' && prev.style === style && Math.abs(prev.top - L.top) < 2 && L.left - prev.right < size * 0.8 && L.left >= prev.right - 1) {
        prev.text += (L.left - prev.right > size * 0.12 ? ' ' : '') + t; prev.right = L.right; continue;
      }
      out.push({ text: t, style, top: L.top, left: L.left, right: L.right, y: L.top + asc });
    }
  };
  const walk = (el) => {
    if (el instanceof SVGSVGElement) {
      const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
      const vb = el.viewBox.baseVal; const s = r.height / vb.height;
      const op = cs.opacity !== '1' ? ` opacity="${cs.opacity}"` : '';
      const fill = el.getAttribute('fill') === 'currentColor' ? color(cs.color).hex : null;
      const inner = [...el.children].map(c => c.outerHTML).join('');
      out.push(`<g transform="translate(${num(r.left)},${num(r.top)}) scale(${num(s)})"${fill ? ` fill="${fill}"` : ''}${op}>${inner.replace(/ class="[^"]*"/g, '')}</g>`);
      return;
    }
    if (!(el instanceof HTMLElement)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return;
    if (el !== document.body && el !== document.documentElement) rectEl(el.getBoundingClientRect(), cs);
    for (const c of el.childNodes) {
      if (c.nodeType === 3) textNode(c); else if (c.nodeType === 1) walk(c);
    }
  };
  walk(document.body);
  const flat = out.map(o => typeof o === 'string' ? o : `<text x="${num(o.left)}" y="${num(o.y)}" ${o.style}>${esc(o.text)}</text>`);
  return `<svg xmlns="${NS}" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">\n` + flat.join('\n') + '\n</svg>\n';
};

export default async (page) => {
  const manifest = JSON.parse(fs.readFileSync(process.env.MANIFEST, 'utf8'));
  const only = process.env.ONLY ? new RegExp(process.env.ONLY) : null;
  let done = 0;
  for (const it of manifest) {
    if (only && !only.test(it.html)) continue;
    await page.setViewportSize({ width: it.w, height: it.h });
    await page.goto('file://' + it.html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const st = await page.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.weight + ':' + f.status));
    const loaded = st.filter(x => x.endsWith('loaded'));
    if (!loaded.some(x => x.startsWith('Manrope')) || !loaded.some(x => x.startsWith('JetBrains'))) throw new Error('fonts not loaded for ' + it.html + ' ' + st.join(','));
    if (process.env.NO_PNG !== '1') await page.screenshot({ path: it.png, clip: { x: 0, y: 0, width: it.w, height: it.h } });
    if (it.svg) {
      const svg = await page.evaluate(extract);
      fs.mkdirSync(path.dirname(it.svg), { recursive: true });
      fs.writeFileSync(it.svg, svg);
    }
    done++;
  }
  return 'ok ' + done;
};
