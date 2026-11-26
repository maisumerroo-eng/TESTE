// Recebe um frame da câmera (foto da TV com o jogo) e devolve dicas em JSON.
import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "node:fs";

// Padrão: Claude Haiku 5.5 via Vercel AI Gateway (crédito grátis da Vercel, sem chave).
// Se o usuário colar uma chave própria da Anthropic (sk-ant-...), vai direto na Anthropic.
const MODELO_GATEWAY = process.env.MODELO || "anthropic/claude-haiku-5.5";
const MODELO_ANTHROPIC = "claude-haiku-5-5";

// Banco de conhecimento do GTA VI (vai inteiro no prompt, com cache).
const BANCO = JSON.parse(readFileSync(new URL("../public/gta6.json", import.meta.url), "utf8"));
const BANCO_TXT = BANCO.itens
  .map((i) => `[${i.tipo}] ${i.nome}${i.tags?.length ? ` (${i.tags.join(", ")})` : ""}: ${i.texto}${i.confirmado === false ? " (NÃO CONFIRMADO)" : ""}`)
  .join("\n");

const SYSTEM = `Você é o "Copiloto", um parceiro de jogo que assiste a partida de GTA VI junto com o jogador.
O jogador apontou a câmera do celular para a TV/monitor. A imagem pode estar torta, com reflexo, moiré ou desfocada.

Como ler a tela:
- Use minimapa/radar, ícones, placas de rua, letreiros de lojas, praias, pântanos, skyline, veículo, roupa, horário e clima.
- O jogo se passa no estado de Leonida (inspirado na Flórida), com Vice City e regiões ao redor. Protagonistas: Lucia e Jason.
- Se não der pra ler algo, diga "parece" ou "não deu pra ver". NUNCA invente nome de missão, local exato ou mecânica que você não tem certeza. Prefira dicas gerais e verdadeiras a dicas específicas inventadas.

O que entregar:
- dica: 1 dica prática pro momento exato (combate, fuga da polícia, direção, missão, economia).
- curiosidade: 1 fato curto e interessante ligado ao que aparece (lugar real que inspirou, cultura da Flórida, detalhe da série GTA). Sem spoiler de história, a menos que o jogador permita.
- perto: até 3 coisas pra fazer por perto, baseadas no que aparece no minimapa/cenário (ícones, lojas, praia, água, estrada, eventos). Se não houver pistas, sugira atividades típicas do tipo de área.
- fala: 1 frase curta (máx 20 palavras), tom de parceiro de jogo, pra ser lida em voz alta.
- Não repita dicas já dadas (lista em "já falei").
- Se a imagem não for uma tela de jogo (ou for menu/carregamento), marque tela_de_jogo=false e use os campos pra uma dica curta geral.
- Use o BANCO DE CONHECIMENTO abaixo como fonte principal. Itens "NÃO CONFIRMADO" só com aviso.
Responda em português do Brasil, direto, sem enrolação. Responda SOMENTE com o JSON pedido.`;

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["tela_de_jogo", "local", "situacao", "dica", "curiosidade", "perto", "fala"],
  properties: {
    tela_de_jogo: { type: "boolean" },
    local: { type: "string", description: "Onde o jogador parece estar. Curto." },
    situacao: { type: "string", description: "O que está acontecendo. Curto." },
    dica: { type: "string" },
    curiosidade: { type: "string" },
    perto: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["titulo", "detalhe"],
        properties: { titulo: { type: "string" }, detalhe: { type: "string" } },
      },
    },
    fala: { type: "string" },
  },
};

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ erro: "Use POST" });

  const chaveUsuario = String(req.headers["x-user-key"] || "");
  const direto = chaveUsuario.startsWith("sk-ant-") || process.env.ANTHROPIC_API_KEY;
  const apiKey = direto
    ? chaveUsuario || process.env.ANTHROPIC_API_KEY
    : process.env.AI_GATEWAY_API_KEY || req.headers["x-vercel-oidc-token"] || process.env.VERCEL_OIDC_TOKEN;
  if (!apiKey) return res.status(401).json({ erro: "Sem acesso à IA. Publique na Vercel (AI Gateway) ou cole uma chave nas configurações." });

  const { imagem, historico = [], pergunta = "", spoilers = false, foco = "tudo" } = req.body || {};
  if (!imagem || typeof imagem !== "string") return res.status(400).json({ erro: "Faltou a imagem" });
  const data = imagem.replace(/^data:image\/\w+;base64,/, "");
  if (data.length > 6_000_000) return res.status(413).json({ erro: "Imagem grande demais" });

  const contexto = [
    `Foco do jogador: ${foco}.`,
    `Spoilers de história: ${spoilers ? "permitidos" : "proibidos"}.`,
    historico.length ? `Já falei: ${historico.slice(-8).map((h) => `- ${h}`).join("\n")}` : "Já falei: nada ainda.",
    pergunta ? `Pergunta do jogador (responda na dica e na fala): ${pergunta}` : "",
  ].filter(Boolean).join("\n");

  const client = direto
    ? new Anthropic({ apiKey })
    : new Anthropic({ apiKey, baseURL: "https://ai-gateway.vercel.sh" });
  try {
    const response = await client.messages.create({
      model: direto ? MODELO_ANTHROPIC : MODELO_GATEWAY,
      max_tokens: 4000,
      output_config: { effort: "low", format: { type: "json_schema", schema: SCHEMA } },
      system: [
        { type: "text", text: SYSTEM },
        { type: "text", text: "BANCO DE CONHECIMENTO GTA VI:\n" + BANCO_TXT, cache_control: { type: "ephemeral" } },
      ],
      messages: [
        {
          role: "user",
          content: [
            { type: "image", source: { type: "base64", media_type: "image/jpeg", data } },
            { type: "text", text: contexto },
          ],
        },
      ],
    });

    if (response.stop_reason === "refusal") return res.status(422).json({ erro: "A IA recusou esse frame. Tenta de novo." });
    if (response.stop_reason === "max_tokens") return res.status(502).json({ erro: "Resposta cortada. Tenta de novo." });

    const texto = response.content.filter((b) => b.type === "text").map((b) => b.text).join("");
    const json = JSON.parse(texto.slice(texto.indexOf("{"), texto.lastIndexOf("}") + 1));
    return res.status(200).json(json);
  } catch (e) {
    if (e instanceof Anthropic.AuthenticationError) return res.status(401).json({ erro: "Chave/acesso inválido." });
    if (e instanceof Anthropic.PermissionDeniedError || e?.status === 402) return res.status(402).json({ erro: "Crédito grátis do mês acabou. Volta no próximo ciclo ou aumenta o intervalo." });
    if (e instanceof Anthropic.RateLimitError) return res.status(429).json({ erro: "Muitas requisições. Aumenta o intervalo." });
    if (e instanceof Anthropic.APIError) {
      console.error(e.status, e.message);
      return res.status(502).json({ erro: `Erro da IA (${e.status ?? "rede"})` });
    }
    if (e instanceof SyntaxError) return res.status(502).json({ erro: "Resposta da IA veio quebrada." });
    console.error(e);
    return res.status(500).json({ erro: "Erro interno" });
  }
}

export const config = { api: { bodyParser: { sizeLimit: "8mb" } } };
