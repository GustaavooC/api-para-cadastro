// Renderiza capas (e o carrossel completo de exemplo) em JPG 1080x1350.
// Uso: node render.js  (a partir de src/, com um servidor http na pasta curso-piercing)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE || 'http://127.0.0.1:8765/src/capas.html';
const OUT = path.join(__dirname, '..', 'capas');
const dados = JSON.parse(fs.readFileSync(path.join(__dirname, 'campanha.json'), 'utf8'));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const shots = dados.carrosseis.map(c => ({ q: `id=${c.id}`, file: `${c.id}-capa.jpg` }));
  const completos = dados.carrosseis.filter(c => dados.completo.includes(c.id));
  for (const comp of completos) {
    fs.mkdirSync(path.join(OUT, comp.id), { recursive: true });
    comp.slides.forEach((_, i) => {
      if (i === 0) return;
      shots.push({ q: `id=${comp.id}&slide=${i}`, file: `${comp.id}/${String(i + 1).padStart(2, '0')}.jpg` });
    });
  }
  for (const s of shots) {
    await page.goto(`${BASE}?${s.q}`);
    await page.waitForSelector('body[data-pronto="1"]');
    await page.waitForTimeout(150);
    await page.locator('.post').screenshot({ path: path.join(OUT, s.file), type: 'jpeg', quality: 90 });
    console.log(s.file);
  }
  for (const comp of completos) fs.copyFileSync(path.join(OUT, `${comp.id}-capa.jpg`), path.join(OUT, comp.id, '01.jpg'));
  await browser.close();
})();
