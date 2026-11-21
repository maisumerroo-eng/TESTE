// tres.js: cena 3D leve com Three.js para a skill site-nova-era.
// Só baixa o Three quando o bloco chega perto da tela (import dinâmico). Sem WebGL, com saveData
// ou erro: fica o poster (imagem) e nada quebra. Reduced motion: renderiza um quadro parado.
//
// No <head> (versão fixa):
// <script type="importmap">{ "imports": {
//   "three": "https://cdn.jsdelivr.net/npm/three@0.187.0/build/three.module.js",
//   "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.187.0/examples/jsm/" } }</script>
//
// Marcação:
// <div class="tres" data-tres data-src="assets/3d/modelo.glb" data-scroll="rotate" data-idle="0.15"
//      data-tilt data-exposure="1.1" role="img" aria-label="Descrição do objeto 3D">
//   <img class="tres__poster" src="assets/3d/poster.webp" alt="" width="800" height="800">
// </div>
// Sem data-src: forma procedural (data-shape="coin|knot|ico"), cor de --accent.

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
const saveData = navigator.connection?.saveData === true;

function webglOk() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch { return false; }
}

async function montar(el) {
  const THREE = await import('three');
  const { RoomEnvironment } = await import('three/addons/environments/RoomEnvironment.js');

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = parseFloat(el.dataset.exposure || 1);
  renderer.domElement.setAttribute('aria-hidden', 'true');
  renderer.domElement.className = 'tres__canvas';
  el.append(renderer.domElement);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(32, 1, 0.01, 100);
  camera.position.set(0, 0, 4);
  const pivot = new THREE.Group();
  scene.add(pivot);

  // ---------- conteúdo ----------
  let obj;
  if (el.dataset.src) {
    const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
    const { DRACOLoader } = await import('three/addons/loaders/DRACOLoader.js');
    const { MeshoptDecoder } = await import('three/addons/libs/meshopt_decoder.module.js');
    const draco = new DRACOLoader().setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.187.0/examples/jsm/libs/draco/gltf/');
    const loader = new GLTFLoader().setDRACOLoader(draco).setMeshoptDecoder(MeshoptDecoder);
    obj = (await loader.loadAsync(el.dataset.src)).scene;
    draco.dispose();
  } else {
    const accent = getComputedStyle(el).getPropertyValue('--accent').trim() || '#c8a34d';
    const mat = new THREE.MeshStandardMaterial({ color: accent, metalness: 1, roughness: 0.28 });
    const shape = el.dataset.shape || 'coin';
    const geo = shape === 'knot' ? new THREE.TorusKnotGeometry(0.8, 0.26, 220, 32)
      : shape === 'ico' ? new THREE.IcosahedronGeometry(1, 1)
      : new THREE.CylinderGeometry(1, 1, 0.14, 96).rotateX(Math.PI / 2);
    obj = new THREE.Mesh(geo, mat);
  }
  // centraliza e enquadra qualquer modelo
  const box = new THREE.Box3().setFromObject(obj);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  obj.position.sub(center);
  const fit = parseFloat(el.dataset.fit || 1.6) / Math.max(size.x, size.y, size.z);
  obj.scale.setScalar(fit);
  pivot.add(obj);

  // ---------- tamanho ----------
  const resize = () => {
    const w = el.clientWidth, h = el.clientHeight || w;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    render();
  };

  // ---------- interação ----------
  const idle = reduce ? 0 : parseFloat(el.dataset.idle || 0);
  let scrollP = 0, tiltX = 0, tiltY = 0, curX = 0, curY = 0, visible = false, raf = 0, last = 0, spin = 0;
  const lerToScroll = () => {
    const r = el.getBoundingClientRect();
    scrollP = Math.min(1, Math.max(0, 1 - (r.top + r.height) / (innerHeight + r.height)));
  };
  if (el.dataset.scroll && !reduce) addEventListener('scroll', lerToScroll, { passive: true });
  if ('tilt' in el.dataset && finePointer && !reduce) {
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      tiltY = ((e.clientX - r.left) / r.width - 0.5) * 0.6;
      tiltX = ((e.clientY - r.top) / r.height - 0.5) * 0.4;
    });
    el.addEventListener('pointerleave', () => { tiltX = tiltY = 0; });
  }

  function render() { renderer.render(scene, camera); }
  function frame(t) {
    const dt = Math.min(0.05, (t - last) / 1000 || 0); last = t;
    spin += idle * dt;
    curX += (tiltX - curX) * 0.08;
    curY += (tiltY - curY) * 0.08;
    const scrollRot = el.dataset.scroll === 'rotate' ? scrollP * Math.PI * 2 : 0;
    pivot.rotation.set(curX, spin + scrollRot + curY, 0);
    render();
    raf = requestAnimationFrame(frame);
  }
  const sync = () => {
    const run = visible && !document.hidden && !reduce;
    if (run && !raf) { last = performance.now(); raf = requestAnimationFrame(frame); }
    if (!run && raf) { cancelAnimationFrame(raf); raf = 0; }
  };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; sync(); }).observe(el);
  document.addEventListener('visibilitychange', sync);
  new ResizeObserver(resize).observe(el);

  pivot.rotation.set(0.15, -0.4, 0);
  lerToScroll();
  resize();
  el.classList.add('is-ready');
  el.dispatchEvent(new CustomEvent('tres:pronto'));
}

function iniciar() {
  const blocos = document.querySelectorAll('[data-tres]');
  if (!blocos.length || saveData || !webglOk()) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      montar(e.target).catch((err) => { console.warn('3D indisponível, mantendo poster:', err.message); e.target.classList.add('is-fallback'); });
    });
  }, { rootMargin: '300px 0px' });
  blocos.forEach((el) => io.observe(el));
}

iniciar();
