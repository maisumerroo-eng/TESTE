// Copiloto IA — câmera do celular -> frame -> /api/analisar -> dicas na tela + voz.
const $ = (id) => document.getElementById(id);
const video = $("video"), canvas = $("canvas"), ctx = canvas.getContext("2d");

const LS = {
  get(k, d) { try { const v = localStorage.getItem("cop:" + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("cop:" + k, JSON.stringify(v)); } catch {} },
};

const cfg = {
  intervalo: LS.get("intervalo", 15),
  foco: LS.get("foco", "tudo"),
  spoilers: LS.get("spoilers", false),
  pular: LS.get("pular", true),
  chave: LS.get("chave", ""),
  voz: LS.get("voz", true),
};

let historico = [];
let ultimaMiniatura = null;
let ocupado = false;
let pausado = false;
let timer = null;
let wakeLock = null;
let perguntaPendente = "";

function status(txt, tipo = "") {
  const el = $("status");
  el.className = "status " + tipo;
  el.querySelector("span").textContent = txt;
}

// ---------- Câmera ----------
async function ligarCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: "environment" }, width: { ideal: 1920 }, height: { ideal: 1080 } },
      audio: false,
    });
    video.srcObject = stream;
    await video.play();
    $("inicio").hidden = true;
    $("app").hidden = false;
    pedirWakeLock();
    agendar(1500);
  } catch (e) {
    alert("Não deu pra abrir a câmera. Libera a permissão e abre o site em HTTPS.\n\n" + e.message);
  }
}

async function pedirWakeLock() {
  try { wakeLock = await navigator.wakeLock?.request("screen"); } catch {}
}
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible" && !$("app").hidden) pedirWakeLock();
});

// ---------- Frame ----------
function capturar() {
  const w = video.videoWidth, h = video.videoHeight;
  if (!w || !h) return null;
  const escala = Math.min(1, 1280 / Math.max(w, h));
  canvas.width = Math.round(w * escala);
  canvas.height = Math.round(h * escala);
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/jpeg", 0.72);
}

// Miniatura 32x18 em cinza pra saber se a tela mudou.
const mini = document.createElement("canvas");
mini.width = 32; mini.height = 18;
const mctx = mini.getContext("2d", { willReadFrequently: true });
function mudouBastante() {
  mctx.drawImage(video, 0, 0, 32, 18);
  const px = mctx.getImageData(0, 0, 32, 18).data;
  const cinza = new Uint8Array(32 * 18);
  for (let i = 0; i < cinza.length; i++) cinza[i] = (px[i * 4] + px[i * 4 + 1] + px[i * 4 + 2]) / 3;
  if (!ultimaMiniatura) { ultimaMiniatura = cinza; return true; }
  let soma = 0;
  for (let i = 0; i < cinza.length; i++) soma += Math.abs(cinza[i] - ultimaMiniatura[i]);
  const diff = soma / cinza.length;
  if (diff > 10) { ultimaMiniatura = cinza; return true; }
  return false;
}

// ---------- Ciclo ----------
function agendar(ms) {
  clearTimeout(timer);
  if (pausado || cfg.intervalo === 0) return;
  timer = setTimeout(() => analisar(false), ms ?? cfg.intervalo * 1000);
}

async function analisar(forcado) {
  if (ocupado) return;
  if (!forcado && !perguntaPendente && cfg.pular && !mudouBastante()) {
    status("Tela parada, esperando…", "ok");
    return agendar();
  }
  if (forcado) mudouBastante(); // atualiza a referência
  const imagem = capturar();
  if (!imagem) return agendar(1000);

  ocupado = true;
  status(perguntaPendente ? "Pensando na pergunta…" : "Lendo a tela…", "lendo");
  const pergunta = perguntaPendente;
  perguntaPendente = "";

  try {
    const headers = { "Content-Type": "application/json" };
    if (cfg.chave) headers["x-user-key"] = cfg.chave;
    const r = await fetch("/api/analisar", {
      method: "POST",
      headers,
      body: JSON.stringify({ imagem, historico, pergunta, spoilers: cfg.spoilers, foco: cfg.foco }),
    });
    const dados = await r.json().catch(() => ({ erro: "Resposta inválida do servidor" }));
    if (!r.ok) throw new Error(dados.erro || "Erro " + r.status);
    mostrar(dados, pergunta);
    historico.push(dados.dica, dados.curiosidade);
    historico = historico.slice(-12);
    status("Atualizado " + new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }), "ok");
  } catch (e) {
    status("Erro", "erro");
    mostrarErro(e.message);
  } finally {
    ocupado = false;
    agendar();
  }
}

// ---------- UI ----------
function card(tipo, titulo, conteudo) {
  const el = document.createElement("article");
  el.className = "card " + tipo;
  const b = document.createElement("b");
  b.textContent = titulo;
  el.append(b);
  if (Array.isArray(conteudo)) {
    const ul = document.createElement("ul");
    for (const item of conteudo) {
      const li = document.createElement("li");
      const strong = document.createElement("strong");
      strong.textContent = item.titulo;
      li.append(strong, " — " + item.detalhe);
      ul.append(li);
    }
    el.append(ul);
  } else {
    const p = document.createElement("p");
    p.textContent = conteudo;
    el.append(p);
  }
  return el;
}

function mostrar(d, pergunta) {
  $("local").textContent = d.tela_de_jogo ? (d.local || "Local desconhecido") : "Não vi o jogo na tela";
  const cards = $("cards");
  cards.replaceChildren();
  if (d.situacao) cards.append(card("situacao", "Agora", d.situacao));
  if (d.dica) cards.append(card("dica", pergunta ? "Resposta" : "Dica", d.dica));
  if (d.perto?.length) cards.append(card("perto", "Por perto", d.perto.slice(0, 3)));
  if (d.curiosidade) cards.append(card("curiosidade", "Curiosidade", d.curiosidade));
  $("painel").scrollTop = 0;
  falar(d.fala);
}

function mostrarErro(msg) {
  $("cards").replaceChildren(card("erro", "Ops", msg));
}

// ---------- Voz ----------
let vozPt = null;
function escolherVoz() {
  const vozes = speechSynthesis.getVoices();
  vozPt = vozes.find((v) => v.lang === "pt-BR") || vozes.find((v) => v.lang.startsWith("pt")) || null;
}
if ("speechSynthesis" in window) {
  escolherVoz();
  speechSynthesis.onvoiceschanged = escolherVoz;
}
function falar(txt) {
  if (!cfg.voz || !txt || !("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(txt);
  u.lang = "pt-BR";
  if (vozPt) u.voice = vozPt;
  u.rate = 1.08;
  speechSynthesis.speak(u);
}

// ---------- Controles ----------
$("btnIniciar").addEventListener("click", () => {
  // Desbloqueia a voz no iOS (precisa de gesto do usuário).
  if ("speechSynthesis" in window) speechSynthesis.speak(new SpeechSynthesisUtterance(""));
  ligarCamera();
});

$("btnAgora").addEventListener("click", () => analisar(true));

$("formPergunta").addEventListener("submit", (e) => {
  e.preventDefault();
  const q = $("inputPergunta").value.trim();
  if (!q) return;
  perguntaPendente = q;
  $("inputPergunta").value = "";
  $("inputPergunta").blur();
  analisar(true);
});

const btnVoz = $("btnVoz");
function syncVoz() { btnVoz.setAttribute("aria-pressed", String(cfg.voz)); btnVoz.textContent = cfg.voz ? "🔊" : "🔇"; }
btnVoz.addEventListener("click", () => {
  cfg.voz = !cfg.voz; LS.set("voz", cfg.voz); syncVoz();
  if (!cfg.voz) speechSynthesis?.cancel();
});
syncVoz();

$("btnPausa").addEventListener("click", () => {
  pausado = !pausado;
  $("btnPausa").textContent = pausado ? "▶" : "⏸";
  $("btnPausa").setAttribute("aria-label", pausado ? "Continuar" : "Pausar");
  if (pausado) { clearTimeout(timer); status("Pausado", "pausado"); } else agendar(300);
});

const dlg = $("config");
$("btnConfig").addEventListener("click", () => {
  $("cfgIntervalo").value = String(cfg.intervalo);
  $("cfgFoco").value = cfg.foco;
  $("cfgSpoilers").checked = cfg.spoilers;
  $("cfgPular").checked = cfg.pular;
  $("cfgChave").value = cfg.chave;
  dlg.showModal();
});
dlg.addEventListener("close", () => {
  cfg.intervalo = Number($("cfgIntervalo").value);
  cfg.foco = $("cfgFoco").value;
  cfg.spoilers = $("cfgSpoilers").checked;
  cfg.pular = $("cfgPular").checked;
  cfg.chave = $("cfgChave").value.trim();
  for (const k of ["intervalo", "foco", "spoilers", "pular", "chave"]) LS.set(k, cfg[k]);
  agendar();
});
