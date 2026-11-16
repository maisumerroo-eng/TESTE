# Análise da cena BR de rap geek (16/11/2026)

Fontes: páginas de vídeos dos canais (títulos, durações, thumbnails recentes), Last.fm, ouvirmusica, Viberate.
**Limite:** não dá para assistir os vídeos daqui. Montagem e ritmo de edição vêm do conhecimento geral do
gênero, não de análise quadro a quadro. Canal "Chrono rapper" não foi encontrado; o nome só aparece
como participação em faixas da AniRap ("Daarui Chrono").

## Títulos

| canal | formato | exemplos de estrutura |
|---|---|---|
| AniRap | `♪ Personagem (Obra) \| Título \| AniRap` | muitos feats, temas com vários personagens ("Controle", "Adaptação") |
| M4rkim | `M4rkim - TÍTULO EM CAIXA ALTA (Personagem)` | foco em Blue Lock, JoJo, Bleach; títulos de 1–2 palavras fortes |
| Henrique Mendonça | `Personagem (Obra) - Título \| Henrique Mendonça` | lado melódico/emotivo, também acústico ao vivo |
| 7 Minutoz | `7 Minutoz - TÍTULO \| Personagem (Obra)` | séries numeradas com vários personagens ("... 3"), terror, The Boys, duelos "X VS Y" |

**Adotado no Kagerima:** `Personagem (Obra) - TÍTULO EM CAIXA ALTA | Kagerima` (+ `ft.` quando tiver).

## Duração
Quase tudo entre **4 e 6 min** (alguns de 8–12 min em séries/cyphers). Música de 2 min destoa da cena.

## Temas
- Primeira pessoa do personagem, contando o arco dele (origem → conflito → virada → clímax).
- Títulos curtos com o conceito central do personagem (uma palavra ou expressão em caixa alta).
- Formatos fortes: **solo**, **VS** (dois lados), **série com vários personagens** (numerada), **desabafo**.
- Obras em alta nos canais agora: Jujutsu Kaisen, Blue Lock, One Piece, Dragon Ball, The Boys, terror.

## Thumbnails (padrão claríssimo nos 4 canais)
- **Arte ilustrada em tela cheia** (não print do anime), muito saturada, luz forte, olhos brilhando.
- Personagem em close ou vários personagens empilhados (séries).
- **Quase sem texto**. O que identifica o canal é o **logo no canto** (M4, HM, "Nerd Hits").
→ Thumbnail do Kagerima refeita nesse padrão: arte em tela cheia + bloom + selo [影] KAGERIMA.

## Vídeo
Gênero = estilo AMV: cenas do anime editadas na música, letra em destaque, cortes no ritmo,
momentos-chave do personagem casados com a letra. É exatamente o que o planner faz com as cenas
que você fornecer.

## O que muda na pipeline
- Título e descrição no formato da cena (ficha técnica: voz, beat, mix, edição, arte; letra; aviso curto).
- Thumbnail art-first sem texto por padrão.
- `project.yaml` ganhou `feats` e `credits` (beat, mix, edit, thumb_art).
