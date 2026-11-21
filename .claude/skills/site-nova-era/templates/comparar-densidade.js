// comparar-densidade.js: mede a "densidade de acabamento" de 2+ sites lado a lado (referência x nosso).
// Uso: node comparar-densidade.js <url-referencia> <url-nosso> [...]
// Lê: altura, seções, títulos, SVG (ícones/desenhos), imagens, links, formulários, regras CSS, keyframes,
// regras de hover, transições, clip-path, mask-image, gradientes, variáveis CSS, animações ativas, palavras, peso JS/CSS.
// Não é meta para copiar número: aponta ONDE falta acabamento (ícones, estados, microanimação, profundidade de conteúdo).
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for (const url of process.argv.slice(2)) {
 const p=await b.newPage({viewport:{width:1440,height:900}});
 const bytes={js:0,css:0};p.on('response',async r=>{try{const t=r.request().resourceType();if(t==='script'||t==='stylesheet'){const len=(await r.body()).length;bytes[t==='script'?'js':'css']+=len;}}catch{}});
 await p.goto(url,{waitUntil:'networkidle',timeout:60000});await p.waitForTimeout(2500);
 await p.evaluate(async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,80));}});
 const m=await p.evaluate(()=>{let kf=0,hover=0,trans=0,rules=0,vars=new Set(),media=0,clip=0,mask=0,grad=0;
  const walk=(rs)=>{for(const r of rs){rules++;if(r.type===7)kf++;if(r.type===4){media++;walk(r.cssRules);continue;}if(r.cssRules&&r.type!==7)walk(r.cssRules);const t=r.cssText||'';if(t.includes(':hover'))hover++;if(/transition\s*:/.test(t))trans++;if(/clip-path/.test(t))clip++;if(/mask-image/.test(t))mask++;if(/gradient\(/.test(t))grad++;(t.match(/--[\w-]+(?=\s*:)/g)||[]).forEach(v=>vars.add(v));}};
  for(const ss of document.styleSheets){try{walk(ss.cssRules)}catch(e){}}
  const q=s=>document.querySelectorAll(s).length;
  return {altura:document.documentElement.scrollHeight,secoes:q('main section, body > section'),h2:q('h2'),h3:q('h3'),svg:q('svg'),svgPaths:q('svg path, svg polygon, svg rect, svg circle'),img:q('img'),canvas:q('canvas'),video:q('video'),links:q('a'),botoes:q('button'),forms:q('form'),inputs:q('input,textarea,select'),
   regrasCSS:rules,keyframes:kf,regrasHover:hover,transicoes:trans,clipPath:clip,maskImage:mask,gradientes:grad,variaveis:vars.size,animacoesAtivasAgora:document.getAnimations().length,
   palavras:document.body.innerText.split(/\s+/).length,dataAttrs:[...new Set([...document.querySelectorAll('*')].flatMap(e=>[...e.attributes].map(a=>a.name).filter(n=>n.startsWith('data-'))))].length}});
 console.log('\n'+url.slice(0,45),JSON.stringify({...m,jsKB:Math.round(bytes.js/1024),cssKB:Math.round(bytes.css/1024)}));
 await p.close();}
await b.close();})();
