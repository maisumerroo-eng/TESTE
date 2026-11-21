# Economia: tokens, créditos e revisão cirúrgica sem perder qualidade

Princípio: **gastar onde muda o resultado, economizar em todo o resto.** Qualidade vem de decisões boas e verificação dirigida, não de reler e regerar tudo.

## 1. Tokens do Claude

| Fazer | Evitar |
|---|---|
| `Grep`/`Glob` para achar o trecho; `Read` com `offset`/`limit` | ler arquivos inteiros "para entender" |
| `Edit` com o trecho exato; vários `Edit` no mesmo turno | reescrever arquivo inteiro com `Write` para mudar 5 linhas |
| Partir dos `templates/base/` (já testados) e trocar placeholders | escrever do zero o que o template já faz |
| Chamadas independentes em paralelo no mesmo turno | uma ferramenta por vez quando não há dependência |
| Salvar análises em arquivo (`casos/*.md`, `auditoria.md`, `dna.md`) e reler o resumo | refazer crawl, auditoria ou pesquisa já feita |
| Screenshot de **um elemento** (`locator(...).screenshot()`) ou folha de contato com várias telas reduzidas | dezenas de screenshots de página inteira em alta resolução |
| `deviceScaleFactor: 1` em prints só para o Claude ver | DPR 2 em verificação interna |
| Saída de comando filtrada (`| tail`, `grep`, `head`) | despejar logs inteiros |
| Não reler arquivo logo após editar (o Edit já falha se der errado) | Read de confirmação depois de cada Edit |
| Subagente só quando o usuário pedir ou a busca for enorme | subagente para tarefa que 2 greps resolvem |
| Regras longas em `references/` lidas sob demanda | colar referência inteira no contexto sem precisar |

Projeto com CLAUDE.md grande: backup e `npx -y claude-token-optimizer measure` → `prune --yes` (preferência do usuário).

## 2. Créditos de geração (imagem, vídeo, voz, 3D)

1. **Decidir antes de gerar:** prompt-mestre aprovado no `dna.md`, lista fechada de assets (ex.: 1 hero, 3 frentes, 1 textura). Nada de "gerar para ver".
2. **Rascunho barato, final caro:** variações de composição no modelo mais barato (Figma `gemini-3.1-flash-lite-image`; muapi `flux-schnell-image`/`nano-banana-2-lite`), escolher com o usuário, e só então o modelo bom (`gpt-image-2.5-sunburst`, `gpt-image-2.6`, `midjourney-v8`) **uma vez**.
3. **Editar em vez de regerar:** ajuste pontual via image-to-image/edit (`*-image-to-image`, `flux-kontext-*-i2i`, `qwen-image-edit`) ou `generate_image` com `nodeId` substituindo a imagem.
4. **Upscale em vez de gerar grande:** gerar em 1024 e usar `ai-image-upscale`/`upscale_image` só na imagem aprovada que precisa de mais resolução.
5. **Expandir em vez de regerar formato:** `ai-image-extension`/`outpaint_image` para virar 16:9 ou 9:16.
6. **Vídeo a partir da imagem aprovada** (image-to-video), duração mínima útil (4 a 6 s em loop), modelo "fast" primeiro.
7. **Voz:** `estimate_only: true`, roteiro fechado antes, 1 geração (o padrão já entrega 2 takes); trocar voz no próprio fluxo em vez de nova chamada.
8. **3D:** procedural, Poly Haven ou 3D Jutsu (grátis) antes de imagem→3D pago; "standard" antes de "detailed".
9. **Grátis primeiro quando a qualidade empata:** bancos públicos para textura/fundo, `search_logo` para logos, ícones procedurais em SVG.
10. **Nunca regerar por timeout:** consultar status/ID; repetir cobra de novo.
10a. **Gates do mais barato ao mais caro:** storyboard aprovado (grátis) → quadro/imagem (barato) → vídeo (caro). Um "sim" antes de gastar vale mais que três takes depois.
10b. **Consertar sem regerar:** final de vídeo ruim → corte de cauda no último quadro estável; costura visível → `xfade`; enquadramento → expandir/editar.
10c. **Comparar modelos com o mesmo pedido:** o preço da mesma tomada já variou ~5x entre o topo e um intermediário de qualidade. Mostrar os números e deixar o usuário escolher.
10d. **Três falhas no mesmo conceito:** trocar o conceito, não reescrever o prompt pela quarta vez.
11. **Manifesto de assets** em `assets/manifesto.json`: arquivo, ferramenta, modelo, prompt, seed/ID, custo, aprovado (sim/não). Antes de gerar, conferir se já existe algo reaproveitável.

```json
[{ "arquivo": "assets/img/hero.webp", "ferramenta": "figma.generate_image", "modelo": "gpt-image-2.5-sunburst",
   "prompt": "ref: dna.md#prompt-mestre + caminhão na estrada ao amanhecer", "id": "123:456", "custo": "créditos Figma", "aprovado": true }]
```

## 3. Revisão só no que mudou

1. **Escopo pelo diff:** `git diff --stat` e `git diff -U3 -- <arquivo>`; revisar só os hunks alterados e o que eles tocam (seletor, função, componente).
2. **Mapa de impacto rápido:** mudou CSS de um componente → testar só as seções que usam a classe (`grep -n "classe" index.html`). Mudou `motion.js` → testar reveal, pin e marquee. Mudou texto → rodar só o detector anti-vício.
3. **Verificação visual dirigida:** screenshot só das seções afetadas, em 390 e 1440 (`page.locator('#secao').screenshot()`), não da página inteira.
4. **Ferramentas de revisão no nível certo:** `/code-review low` ou `medium` no diff para mudança pequena; `high` só em entrega final ou mudança grande. `/simplify` só nos arquivos alterados.
5. **Auditoria completa só em marcos:** primeira versão, antes do deploy e depois de mudança grande. Entre marcos, testes focados.
6. **Corrigir pela prioridade do relatório:** `auditoria.md` lista P1 → P3. Resolver P1 e P2; P3 só se for barato. Rodar a auditoria de novo só para confirmar os itens corrigidos.

## 4. Otimização inteligente do site (ciclo)

```
medir → priorizar → corrigir o maior gargalo → medir de novo → parar quando bater a meta
```

1. **Medir:** `node templates/auditar-site.js <url> auditoria` (celular, 4G lento, CPU 4x). Lê LCP, CLS, bloqueio, peso, maiores arquivos, código não usado, imagens grandes/antigas/sem dimensão, fontes, terceiros, SEO e a11y básica.
2. **Priorizar pelo impacto no usuário:** erro de console e quebra de layout → LCP → CLS → bloqueio de JS → peso → SEO/a11y fino.
3. **Correções de maior retorno (fazer nesta ordem):**
   - Imagem do LCP: AVIF/WebP no tamanho certo (`otimizar-imagens.sh`), `fetchpriority="high"`, sem `loading="lazy"`, `<link rel="preload">` se for fundo CSS.
   - Preloader/cortina: só 1ª visita, ≤ 2,5 s; nunca esconder a hero atrás de JS.
   - Fontes: woff2 subset, ≤ 4 variações, `preload` só a do H1, `font-display: swap`, `size-adjust` no fallback para não pular.
   - JS: `type="module"`, import dinâmico do que é pesado (3D, carrossel, mapa), nada de biblioteca para o que CSS faz.
   - CSS: crítico inline só se o CSS passar de ~50 KB; remover regras mortas apontadas pela cobertura.
   - Terceiros: análise e pixel só após consentimento; self-host de fontes e ícones.
   - 3D/vídeo: `otimizar-3d.sh`, vídeo ≤ 2 MB com poster, nada disso na primeira dobra do mobile sem necessidade.
   - Cache: arquivos com hash no nome + `Cache-Control: immutable` (no `vercel.json`).
4. **Parar** quando as metas de `qualidade.md` forem atingidas. Otimização além da meta só se o usuário pedir.

### `vercel.json` de cache (modelo)
```json
{ "headers": [
  { "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
  { "source": "/(.*)\\.(js|css)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] }
] }
```
Usar só com nomes versionados (`main.3f2a.js`); sem hash, prefira `max-age=3600`.
