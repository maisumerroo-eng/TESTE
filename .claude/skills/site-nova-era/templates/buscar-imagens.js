// buscar-imagens.js: busca e baixa fotos de bancos públicos SEM chave (Openverse + Wikimedia Commons),
// só com licença que permite uso comercial e modificação, e registra os créditos.
// Uso: node buscar-imagens.js "caminhão estrada noite" [quantidade=6] [pasta=assets/img/banco] [--orient=wide|tall|square]
// Saída: imagens baixadas + creditos.md (atribuição exigida pela licença) + creditos.json
// Dica: buscar em inglês costuma render mais resultados ("truck highway night").
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const flags = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => a.slice(2).split('=')));
const [query, qtdArg, pastaArg] = args.filter((a) => !a.startsWith('--'));
if (!query) { console.error('uso: node buscar-imagens.js "<busca>" [qtd] [pasta] [--orient=wide|tall|square]'); process.exit(1); }
const qtd = Number(qtdArg || 6);
const pasta = pastaArg || 'assets/img/banco';
const UA = 'site-nova-era-skill/1.0 (image search script)';
const LIVRES = ['cc0', 'pdm'];                    // não exigem crédito
const OK = ['cc0', 'pdm', 'by', 'by-sa'];          // permitem uso comercial e edição (by/by-sa exigem crédito)

const slug = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50);
const orientOk = (w, h) => {
  if (!w || !h || !flags.orient) return true;
  const r = w / h;
  return flags.orient === 'wide' ? r >= 1.3 : flags.orient === 'tall' ? r <= 0.8 : r > 0.8 && r < 1.3;
};

async function openverse() {
  const u = new URL('https://api.openverse.org/v1/images/');
  u.search = new URLSearchParams({ q: query, page_size: String(Math.min(50, qtd * 4)), license_type: 'commercial,modification', mature: 'false' });
  const r = await fetch(u, { headers: { 'User-Agent': UA } });
  if (!r.ok) throw new Error('openverse ' + r.status);
  const d = await r.json();
  return d.results.filter((x) => OK.includes(x.license) && orientOk(x.width, x.height)).map((x) => ({
    fonte: 'openverse/' + x.source, titulo: x.title, url: x.url, pagina: x.foreign_landing_url,
    autor: x.creator || 'desconhecido', licenca: `CC ${x.license.toUpperCase()} ${x.license_version || ''}`.trim(),
    livre: LIVRES.includes(x.license), credito: x.attribution, w: x.width, h: x.height,
  }));
}

async function wikimedia() {
  const u = new URL('https://commons.wikimedia.org/w/api.php');
  u.search = new URLSearchParams({
    action: 'query', format: 'json', generator: 'search', gsrsearch: `${query} filetype:bitmap`, gsrnamespace: '6',
    gsrlimit: String(Math.min(40, qtd * 4)), prop: 'imageinfo', iiprop: 'url|size|extmetadata', iiurlwidth: '2000',
  });
  const r = await fetch(u, { headers: { 'User-Agent': UA } });
  if (!r.ok) throw new Error('wikimedia ' + r.status);
  const d = await r.json();
  return Object.values(d.query?.pages || {}).map((p) => {
    const ii = p.imageinfo?.[0]; if (!ii) return null;
    const m = ii.extmetadata || {};
    const lic = (m.LicenseShortName?.value || '').toLowerCase();
    const tipo = /cc0|public domain|domínio público/.test(lic) ? 'cc0' : /cc by-sa/.test(lic) ? 'by-sa' : /cc by(?!-n)/.test(lic) ? 'by' : null;
    if (!tipo || /nc|nd/.test(lic)) return null;
    const autor = (m.Artist?.value || 'desconhecido').replace(/<[^>]+>/g, '').trim();
    return {
      fonte: 'wikimedia', titulo: p.title.replace(/^File:/, ''), url: ii.thumburl || ii.url, pagina: ii.descriptionurl,
      autor, licenca: m.LicenseShortName?.value, livre: tipo === 'cc0', w: ii.thumbwidth || ii.width, h: ii.thumbheight || ii.height,
      credito: `"${p.title.replace(/^File:/, '')}" por ${autor}, ${m.LicenseShortName?.value}, via Wikimedia Commons (${ii.descriptionurl})`,
    };
  }).filter((x) => x && orientOk(x.w, x.h));
}

(async () => {
  const porFonte = [];
  for (const [nome, fn] of [['openverse', openverse], ['wikimedia', wikimedia]]) {
    try {
      const r = await fn();
      // dentro de cada fonte: livres de crédito primeiro, depois maiores
      r.sort((a, b) => (b.livre - a.livre) || ((b.w || 0) - (a.w || 0)));
      porFonte.push(r);
    } catch (e) { console.warn(`aviso: ${nome} falhou (${e.message})`); }
  }
  // intercala as fontes para variar estilo e autor
  const lista = [];
  for (let i = 0; i < Math.max(0, ...porFonte.map((f) => f.length)); i++) porFonte.forEach((f) => f[i] && lista.push(f[i]));
  fs.mkdirSync(pasta, { recursive: true });
  const salvos = [];
  const serie = (t) => slug(t || '').replace(/[0-9-]+/g, '').slice(0, 18); // mesma série de fotos = mesmo prefixo
  const porAutor = {};
  for (const it of lista) {
    if (salvos.length >= qtd) break;
    if (salvos.some((s) => serie(s.titulo) === serie(it.titulo))) continue;
    if ((porAutor[it.autor] || 0) >= 2) continue;
    try {
      const r = await fetch(it.url, { headers: { 'User-Agent': UA } });
      const tipo = r.headers.get('content-type') || '';
      if (!r.ok || !tipo.startsWith('image/')) continue;
      const ext = tipo.includes('png') ? 'png' : tipo.includes('webp') ? 'webp' : 'jpg';
      const nome = `${slug(query)}-${String(salvos.length + 1).padStart(2, '0')}.${ext}`;
      fs.writeFileSync(path.join(pasta, nome), Buffer.from(await r.arrayBuffer()));
      salvos.push({ arquivo: nome, ...it });
      porAutor[it.autor] = (porAutor[it.autor] || 0) + 1;
      console.log(`ok ${nome}  ${it.licenca}  ${it.fonte}`);
    } catch { /* imagem indisponível, tenta a próxima */ }
  }
  const md = ['# Créditos das imagens', '', `Busca: "${query}"`, ''];
  salvos.forEach((s) => md.push(`- \`${s.arquivo}\`: ${s.livre ? '(livre de crédito) ' : ''}${s.credito}  `, `  Fonte: ${s.pagina}`));
  fs.appendFileSync(path.join(pasta, 'creditos.md'), md.join('\n') + '\n\n');
  const jsonPath = path.join(pasta, 'creditos.json');
  const antigo = fs.existsSync(jsonPath) ? JSON.parse(fs.readFileSync(jsonPath, 'utf8')) : [];
  fs.writeFileSync(jsonPath, JSON.stringify([...antigo, ...salvos], null, 2));
  console.log(`${salvos.length}/${qtd} imagens em ${pasta} (créditos em creditos.md)`);
  if (salvos.some((s) => !s.livre)) console.log('ATENÇÃO: há imagens CC BY/BY-SA: o crédito precisa aparecer no site (rodapé ou página de créditos).');
})();
