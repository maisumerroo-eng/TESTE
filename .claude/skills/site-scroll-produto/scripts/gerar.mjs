#!/usr/bin/env node
// Gera imagem ou vídeo via fal.ai queue API. Uso: ver SKILL.md.
// node gerar.mjs <imagem|video> --modelo ID --prompt "..." [--imagem arquivo|url] [--saida caminho] [--extra '{"duration":"10"}']
import fs from 'node:fs';
import path from 'node:path';

const [tipo, ...rest] = process.argv.slice(2);
const args = {};
for (let i = 0; i < rest.length; i += 2) args[rest[i].replace(/^--/, '')] = rest[i + 1];
if (!['imagem', 'video'].includes(tipo) || !args.modelo || !args.prompt) {
  console.error('uso: gerar.mjs <imagem|video> --modelo ID --prompt "..." [--imagem arq|url] [--saida arq] [--extra JSON]');
  process.exit(1);
}
const KEY = process.env.FAL_KEY || 'proxy-injeta'; // proxy do ambiente pode injetar a chave
const H = { Authorization: `Key ${KEY}`, 'Content-Type': 'application/json' };

function toUrl(img) {
  if (!img) return undefined;
  if (/^https?:|^data:/.test(img)) return img;
  const ext = path.extname(img).slice(1).replace('jpg', 'jpeg') || 'png';
  return `data:image/${ext};base64,${fs.readFileSync(img).toString('base64')}`;
}

const body = { prompt: args.prompt, ...(args.extra ? JSON.parse(args.extra) : {}) };
const img = toUrl(args.imagem);
if (img) {
  if (args.modelo.includes('edit')) body.image_urls = [img];
  else body.image_url = img;
}

const sub = await fetch(`https://queue.fal.run/${args.modelo}`, { method: 'POST', headers: H, body: JSON.stringify(body) });
if (!sub.ok) { console.error('erro ao enviar', sub.status, await sub.text()); process.exit(1); }
const { status_url, response_url, request_id } = await sub.json();
console.error('job', request_id);

for (;;) {
  await new Promise(r => setTimeout(r, 4000));
  const s = await (await fetch(status_url, { headers: H })).json();
  process.stderr.write(`\r${s.status}${s.queue_position != null ? ' fila ' + s.queue_position : ''}   `);
  if (s.status === 'COMPLETED') break;
  if (s.status === 'FAILED' || s.error) { console.error('\nfalhou', JSON.stringify(s)); process.exit(1); }
}
const out = await (await fetch(response_url, { headers: H })).json();
const url = out.video?.url || out.images?.[0]?.url || out.image?.url;
if (!url) { console.log(JSON.stringify(out, null, 2)); process.exit(0); }
const saida = args.saida || `media/${tipo}-${request_id}${tipo === 'video' ? '.mp4' : '.png'}`;
fs.mkdirSync(path.dirname(saida), { recursive: true });
fs.writeFileSync(saida, Buffer.from(await (await fetch(url)).arrayBuffer()));
console.error('\nsalvo');
console.log(saida);
