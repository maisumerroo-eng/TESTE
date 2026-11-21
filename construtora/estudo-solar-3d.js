// estudo-solar-3d.js: maquete 3D com sol real e sombras guiado pelo scroll (assinatura para arquitetura/construção).
// Usa o progresso --p (0..1) que o motion.js escreve no [data-pin]. Three.js só é baixado perto da seção.
// Sem WebGL, com reduced motion ou saveData: nada acontece e a cena SVG/estática continua (fallback).
//
// <section data-pin ...><div data-pin-stage> ... <div class="solar3d" data-solar3d aria-hidden="true"></div> ... </div></section>
// Precisa do import map de three@0.187.0 no <head> (ver templates/base/index.html).
// Quando o 3D fica pronto, adiciona .is-3d no [data-pin] (CSS esconde o desenho 2D da casa).

const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

async function montar(box) {
  const pin = box.closest('[data-pin]');
  const THREE = await import('three');
  const mobile = matchMedia('(max-width: 699px)').matches;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, mobile ? 1.5 : 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;   // mantém o branco de maquete branco
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  box.append(renderer.domElement);

  const scene = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(28, 1, 0.1, 200);

  // ---------- maquete (tudo branco, estilo modelo de arquitetura) ----------
  const branco = new THREE.MeshStandardMaterial({ color: 0xf3efe8, roughness: 0.92 });
  const base = new THREE.MeshStandardMaterial({ color: 0xe6ddd0, roughness: 1 });
  const vidro = new THREE.MeshStandardMaterial({ color: 0x2f3438, roughness: 0.25, metalness: 0.1, emissive: 0xffb36b, emissiveIntensity: 0 });
  const agua = new THREE.MeshStandardMaterial({ color: 0x7fa3b0, roughness: 0.15, metalness: 0.2 });
  const g = new THREE.Group();
  const caixa = (w, h, d, x, y, z, m = branco) => {
    const me = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
    me.position.set(x, y + h / 2, z); me.castShadow = true; me.receiveShadow = true; g.add(me); return me;
  };
  const tabuleiro = caixa(16, 0.5, 12, 0, -0.5, 0, base); tabuleiro.castShadow = false;
  caixa(9.5, 0.25, 6.2, -0.6, 0, 0.2);                      // plinto
  caixa(7.2, 2.4, 4.4, -1.2, 0.25, 0.2);                    // volume principal
  caixa(11.6, 0.32, 6.6, -0.9, 2.65, 0.3);                  // laje em balanço
  caixa(1.7, 4.2, 2.6, 3.8, 0.25, -0.4);                    // bloco alto
  [-3.9, -2.0, -0.1, 1.8].forEach((x) => caixa(1.6, 1.9, 0.08, x, 0.45, 2.42, vidro)); // panos de vidro
  const piscina = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.06, 1.6), agua); piscina.position.set(-1.6, 0.03, 4.1); piscina.receiveShadow = true; g.add(piscina);
  // árvores de maquete (esferas brancas)
  [[-6.4, -3.6, 1.0], [-6.8, 3.4, 0.8], [6.2, 3.8, 1.1], [6.6, -3.2, 0.7]].forEach(([x, z, r]) => {
    const t = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 1.2, 8), branco); t.position.set(x, 0.6, z); t.castShadow = true; g.add(t);
    const c = new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), branco); c.position.set(x, 1.2 + r * 0.8, z); c.castShadow = true; c.receiveShadow = true; g.add(c);
  });
  scene.add(g);

  // ---------- luzes ----------
  const hemi = new THREE.HemisphereLight(0xdfe8f0, 0x9a8a78, 0.9); scene.add(hemi);
  const sol = new THREE.DirectionalLight(0xffffff, 3);
  sol.castShadow = true;
  sol.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(sol.shadow.camera, { left: -12, right: 12, top: 12, bottom: -12, near: 1, far: 80 });
  sol.shadow.bias = -0.0004; sol.shadow.normalBias = 0.02; sol.shadow.radius = 3;
  scene.add(sol, sol.target);

  // paleta do dia: [p, cor do sol, intensidade, céu (hemi), chão (hemi), hemi int, janelas]
  const DIA = [
    [0.00, 0xffb27a, 1.8, 0xd9cdc4, 0x8a7a6c, 0.9, 0],
    [0.28, 0xfffaf2, 3.0, 0xf2f6fa, 0xc4b8aa, 1.35, 0],
    [0.55, 0xffe2bd, 2.7, 0xf0e4d4, 0xb4a290, 1.2, 0],
    [0.80, 0xff8a4a, 1.3, 0x7d6b78, 0x3b2f2a, 0.45, 0.6],
    [1.00, 0x6f86c9, 0.35, 0x232a44, 0x1a1512, 0.32, 2.4],
  ];
  const cor = new THREE.Color(), c2 = new THREE.Color();
  function luzDoDia(p) {
    let k = 0; while (k < DIA.length - 2 && p > DIA[k + 1][0]) k++;
    const [a, b] = [DIA[k], DIA[k + 1]]; const t = clamp((p - a[0]) / (b[0] - a[0]), 0, 1);
    sol.color.copy(cor.setHex(a[1]).lerp(c2.setHex(b[1]), t)); sol.intensity = lerp(a[2], b[2], t);
    hemi.color.copy(cor.setHex(a[3]).lerp(c2.setHex(b[3]), t)); hemi.groundColor.copy(cor.setHex(a[4]).lerp(c2.setHex(b[4]), t)); hemi.intensity = lerp(a[5], b[5], t);
    vidro.emissiveIntensity = lerp(a[6], b[6], t);
    // trajetória do sol: nasce a leste (-x), culmina e se põe a oeste (+x); depois da entrega vira "lua"
    const dia = clamp(p / 0.86, 0, 1);
    const az = lerp(-Math.PI * 0.55, Math.PI * 0.55, dia);
    const el = Math.max(0.08, Math.sin(Math.PI * dia) * 1.05);
    sol.position.set(Math.sin(az) * 30, Math.sin(el) * 30, Math.cos(az) * 14 + 8);
    sol.target.position.set(0, 0, 0);
  }

  // ---------- câmera: casa à direita no desktop, embaixo no celular ----------
  function enquadra() {
    const w = box.clientWidth, h = box.clientHeight || 1;
    renderer.setSize(w, h, false);
    cam.aspect = w / h;
    const retrato = w / h < 1;
    cam.fov = retrato ? 38 : 24;
    const k = retrato ? 1.55 : 1.7;
    cam.position.set(16 * k, (retrato ? 14 : 10.5) * k, 22 * k);
    cam.lookAt(retrato ? 0.5 : -11.5, retrato ? 7.5 : 2.6, 0);
    cam.updateProjectionMatrix();
  }

  let pAtual = -1, raf = 0;
  const lerP = () => parseFloat(getComputedStyle(pin).getPropertyValue('--p')) || 0;
  function quadro() {
    raf = 0;
    const p = lerP();
    if (Math.abs(p - pAtual) < 0.0005) return;
    pAtual = p;
    luzDoDia(p);
    g.rotation.y = lerp(-0.18, 0.18, p);
    renderer.render(scene, cam);
  }
  const pedir = () => { if (!raf) raf = requestAnimationFrame(quadro); };
  addEventListener('scroll', pedir, { passive: true });
  new ResizeObserver(() => { enquadra(); pAtual = -1; pedir(); }).observe(box);
  enquadra(); luzDoDia(lerP());
  if (renderer.compileAsync) await renderer.compileAsync(scene, cam);   // compila shaders sem travar o scroll
  renderer.render(scene, cam); pAtual = lerP();
  pin.classList.add('is-3d');
}

function iniciar() {
  const boxes = document.querySelectorAll('[data-solar3d]');
  // aparelho fraco (pouca memória ou poucos núcleos) fica com a versão 2D: o 3D custa ~250 ms de CPU ao montar
  const fraco = (navigator.deviceMemory && navigator.deviceMemory < 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4);
  if (!boxes.length || reduz || fraco || navigator.connection?.saveData) return;
  try { const c = document.createElement('canvas'); if (!(c.getContext('webgl2') || c.getContext('webgl'))) return; } catch { return; }
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    io.unobserve(e.target);
    montar(e.target.__solar).catch((err) => console.warn('estudo solar 3D indisponível, mantendo 2D:', err.message));
  }), { rootMargin: '600px 0px' });
  boxes.forEach((b) => { const s = b.closest('[data-pin]'); if (!s) return; s.__solar = b; io.observe(s); });
}

iniciar();
