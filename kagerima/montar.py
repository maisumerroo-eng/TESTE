#!/usr/bin/env python3
"""montar.py: gera o index.html da KAGERIMA a partir de dados.json.
Quando o canal enviar os dados oficiais (links, números, letras), atualizar dados.json e rodar: python3 montar.py"""
import json, html
D = json.load(open('dados.json'))
S = D['sombras']
WA = D.get('whatsapp', '5500000000000')
YT = D.get('youtube', 'https://www.youtube.com/results?search_query=kagerima')
SP = D.get('spotify', 'https://open.spotify.com/search/kagerima')
IG = D.get('instagram', 'https://www.instagram.com/')
e = html.escape
ANIMES = [('naruto', 'Naruto'), ('jujutsu-kaisen', 'Jujutsu Kaisen'), ('one-piece', 'One Piece'), ('bleach', 'Bleach'), ('dragon-ball', 'Dragon Ball')]

def pic(nome, alt, w=640, cls='', lazy=True, sizes='(min-width: 900px) 25vw, 50vw'):
    return (f'<picture class="{cls}"><source type="image/avif" srcset="assets/img/capas/{nome}-320.avif 320w, assets/img/capas/{nome}-640.avif 640w" sizes="{sizes}">'
            f'<img src="assets/img/capas/{nome}-640.webp" srcset="assets/img/capas/{nome}-320.webp 320w, assets/img/capas/{nome}-640.webp 640w" sizes="{sizes}" width="640" height="640" alt="{e(alt)}"{" loading=\"lazy\"" if lazy else ""} decoding="async"></picture>')

def icone(n):
    return f'<svg viewBox="0 0 80 72" aria-hidden="true"><use href="assets/icons/icones-kagerima.svg#{n}"/></svg>'

LINHA = {
    'gojo': 'O mais forte não pede licença: cada verso fecha o domínio e deixa o adversário sem espaço.',
    'goku': 'Um treino que nunca acaba: o beat sobe de nível junto com a transformação.',
    'ichigo': 'A espada ganha nome no refrão: quando o grave entra, a liberação acontece.',
    'luffy': 'Liberdade em forma de rima: o sonho do chapéu de palha virando refrão de navio.',
    'sasuke': 'Olhos que copiam tudo e um caminho de vingança contado verso a verso.',
    'megumi': 'Dez sombras, dez rimas: cada shikigami entra no beat como uma invocação.',
}
DURA = ['3:42', '4:05', '3:58', '4:21', '3:36', '4:12', '3:49', '4:30', '3:27', '4:08', '3:55', '4:16']

# ---------- blocos ----------
faixa_obras = ''.join(
    f'<li><a href="#sombra-{s["id"]}" data-anime-link="{s["slug"]}" style="--cor:{s["cor"]}">{pic(s["id"] + "-1", "", sizes="120px", cls="obra__capa")}'
    f'<span class="obra__k" style="--cor:{s["cor"]}" aria-hidden="true">{s["k1"]}{s["k2"]}</span>'
    f'<h3>{e(s["personagem"])}</h3><p>{e(s["anime"])} · {e(s["termo"])}</p></a></li>' for s in S)

passos = ''.join(
    f'<li data-step id="sombra-{s["id"]}" style="--cor:{s["cor"]}">'
    f'<p class="sel__meta">Sombra {i + 1:02d} · {e(s["anime"])}</p>'
    f'<p class="sel__kanji" aria-hidden="true"><span data-decrypt>{s["k1"]}</span><span data-decrypt>{s["k2"]}</span></p>'
    f'<h3>{e(s["personagem"])}<span class="sel__termo">{e(s["termo"])}</span></h3>'
    f'<p>{e(LINHA[s["id"]])}</p>'
    f'<p class="sel__acoes"><a class="lnk-yt" href="{YT}" data-cta="sel-{s["id"]}"><svg aria-hidden="true"><use href="#i-yt"/></svg>Ouvir no YouTube</a>'
    f'<a class="lnk-sp" href="{SP}"><svg aria-hidden="true"><use href="#i-sp"/></svg>Spotify</a></p></li>' for i, s in enumerate(S))
sel_pontos = ''.join(f'<a class="sel__ponto" href="#sombra-{s["id"]}" data-ir="{i}" style="--cor:{s["cor"]}"><span class="sr">Sombra {i + 1}: {e(s["personagem"])}</span><b aria-hidden="true">{s["k1"]}</b></a>' for i, s in enumerate(S))
sel_capas = ''.join(f'<li data-sel-capa="{i}">{pic(s["id"] + "-1", "Capa do rap de " + s["personagem"], sizes="(min-width: 1000px) 34vw, 70vw")}</li>' for i, s in enumerate(S))

# faixas que citam arcos recentes: capa velada até o fã aceitar
SPOILER = {'Domínio da Sombra': 'arco de Shibuya', 'Gear Cinco': 'arco de Wano', 'Laços Cortados': 'Shippuden'}
cards = []
n = 0
for s in S:
    for j, f in enumerate(s['faixas']):
        sp = SPOILER.get(f)
        cards.append(
            f'<li class="faixa" data-anime="{s["slug"]}" data-dur="{DURA[n]}"' + (' data-nova' if n < 2 else '') + (f' data-spoiler="{e(sp)}"' if sp else '') + f' style="--cor:{s["cor"]}">'
            f'<button type="button" class="faixa__play" data-player="{e(s.get("yt", [""] * 2)[j] if s.get("yt") else "")}" aria-label="Tocar {e(f)}, rap de {e(s["personagem"])}">'
            f'{pic(s["id"] + "-" + str(j + 1), "Capa da faixa " + f)}<span class="faixa__btn" aria-hidden="true"><svg><use href="#i-play"/></svg></span></button>'
            f'<div class="faixa__info"><p class="faixa__meta">{e(s["anime"])} · {DURA[n]}' + ('<span class="faixa__nova">Nova</span>' if n < 2 else '') + '</p>' f'<h3>{e(f)}</h3><p class="faixa__pers">{e(s["personagem"])}</p>'
            f'<p class="faixa__links"><a href="{YT}" aria-label="{e(f)} no YouTube"><svg aria-hidden="true"><use href="#i-yt"/></svg></a>'
            f'<a href="{SP}" aria-label="{e(f)} no Spotify"><svg aria-hidden="true"><use href="#i-sp"/></svg></a></p></div></li>')
        n += 1
cards = ''.join(cards)
filtros_extra = '<button type="button" class="spoiler-toggle" aria-pressed="false" data-spoiler-toggle>Mostrar spoilers</button>'
filtros = '<button type="button" class="filtro" aria-pressed="true" data-filtro="todos">Todos</button>' + ''.join(
    f'<button type="button" class="filtro" aria-pressed="false" data-filtro="{a}">{e(t)}</button>' for a, t in ANIMES)
chips = ''.join(f'<button type="button" class="chip" data-anime-choose="{a}" aria-pressed="false">{e(t)}</button>' for a, t in ANIMES)

letras = ''.join(
    f'<li><a href="#letra-{s["id"]}" class="letra" data-letra="{s["id"]}">{pic("letra-" + s["id"], "", sizes="300px")}'
    f'<span class="letra__corpo"><span class="letra__cat">{e(s["anime"])}</span><h3>Rap de {e(s["personagem"].split()[0] if s["id"] != "luffy" else "Luffy")}: letra e referências</h3>'
    f'<span class="letra__ler">Ver letra</span></span></a></li>' for s in S)

grafico = json.dumps({"titulo": "Plays por sombra (exemplo, aguardando números oficiais)", "rotulos": [s['personagem'].split()[-1] if s['id'] != 'luffy' else 'Luffy' for s in S],
                      "series": [{"nome": "YouTube", "cor": "#c2fb39", "valores": [9.4, 7.1, 5.2, 8.3, 6.6, 4.8]}, {"nome": "Spotify", "cor": "#3aa4fa", "valores": [3.1, 2.4, 1.9, 2.7, 2.2, 1.6]}],
                      "unidade": " mi", "max": 10.5, "nota": "Toque, passe o mouse ou use o teclado nas barras. Valores de exemplo até o canal enviar os dados reais."}, ensure_ascii=False)


# ---------- dicionário dos kanjis (12, na ordem do banner) ----------
KANJIS = [
    ('gojo', '無', 'mu', 'vazio, nada', 'Primeiro kanji de 無量空処, o domínio de Gojo: o Vazio Infinito.'),
    ('goku', '超', 'chō', 'além, super', 'O 超 de Super Saiyajin: passar do próprio limite.'),
    ('ichigo', '卍', 'ban (manji)', 'giro, símbolo budista', 'Metade de 卍解, Bankai. Símbolo budista de sorte, sem relação com o símbolo nazista.'),
    ('luffy', '海', 'kai / umi', 'mar', 'Abre 海賊王, Rei dos Piratas: o sonho do chapéu de palha.'),
    ('sasuke', '写', 'sha', 'copiar', 'Abre 写輪眼, Sharingan: o olho que copia qualquer técnica.'),
    ('megumi', '伏', 'fushi', 'esconder-se, abaixar', 'Abre 伏黒, Fushiguro: o sobrenome de quem invoca as Dez Sombras.'),
    ('gojo', '処', 'sho', 'lugar', 'Fecha 無量空処: o lugar onde a informação não acaba.'),
    ('goku', '超', 'chō', 'além, super', 'O 超 de Dragon Ball Super, título da série que continua a saga.'),
    ('ichigo', '解', 'kai', 'liberar, soltar', 'Fecha 卍解: a liberação final da zanpakutō.'),
    ('luffy', '王', 'ō', 'rei', 'Fecha 海賊王: o título que Luffy quer conquistar.'),
    ('sasuke', '眼', 'gan', 'olho', 'Fecha 写輪眼: o olho que carrega a história do clã Uchiha.'),
    ('megumi', '子', 'ko', 'filho', 'Megumi é filho de Toji Fushiguro: a coluna fecha com a linhagem.'),
]
SID = {s['id']: s for s in S}
dic = ''.join(
    f'<li class="dic__card" data-s="{sid}" style="--cor:{SID[sid]["cor"]}" tabindex="0">'
    f'<span class="dic__aura" aria-hidden="true"></span><span class="dic__k" aria-hidden="true">{k}</span>'
    f'<span class="dic__n">{i + 1:02d} · {e(SID[sid]["anime"])}</span>'
    f'<h3><span class="sr">Kanji {k}, </span>{e(sig.capitalize())}</h3>'
    f'<p class="dic__leit">Leitura: <b>{e(leit)}</b></p><p class="dic__orig">{e(orig)}</p></li>' for i, (sid, k, leit, sig, orig) in enumerate(KANJIS))

# ---------- estúdio: 4 camadas ----------
CAMADAS = [
    ('beat', 'Beat', 'O chão da luta', 'O instrumental define o arco: épico para a virada, sombrio para a vilania, acelerado para a batalha. O beat muda de clima quando o personagem muda.', ['BPM de 80 a 150', 'Samples com timbre oriental', 'Grave que entra na revelação']),
    ('flow', 'Flow', 'A técnica do personagem', 'O jeito de rimar imita o personagem: Gojo rima tranquilo e por cima do beat, Goku acelera a cada transformação, Sasuke corta as frases curtas e frias.', ['Cadência por personagem', 'Pausas antes do golpe', 'Refrão fácil de cantar']),
    ('letra', 'Letra', 'A história respeitada', 'Cada verso tem fonte: episódio, capítulo ou cena. A referência que o fã reconhece vale mais que a lista de poderes.', ['Pesquisa do arco completo', 'Aviso de spoiler', 'Nota de referência por verso']),
    ('mix', 'Mix', 'O acabamento', 'Voz na frente, grave controlado e brilho para o fone. A faixa é masterizada para soar bem no YouTube, no Spotify e na caixinha do celular.', ['Master para streaming', 'Teste em fone e celular', 'Versão curta para Reels']),
]
est_tabs = ''.join(f'<button type="button" role="tab" id="tab-{c}" aria-controls="pn-{c}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" class="estudio__tab" data-camada="{c}"><span class="estudio__n">0{i + 1}</span>{n}</button>' for i, (c, n, *_ ) in enumerate(CAMADAS))
est_pn = ''.join(f'<div class="estudio__painel" role="tabpanel" id="pn-{c}" aria-labelledby="tab-{c}" data-camada="{c}"{"" if i == 0 else " hidden"}><h3>{e(t)}</h3><p>{e(txt)}</p><ul>' + ''.join(f'<li>{e(x)}</li>' for x in lst) + '</ul></div>' for i, (c, n, t, txt, lst) in enumerate(CAMADAS))

# ---------- votação (prévia de demonstração) ----------
VOTOS = [('sukuna', 'Ryomen Sukuna', 'Jujutsu Kaisen', '#3aa4fa', 31), ('itachi', 'Itachi Uchiha', 'Naruto', '#e0263a', 24), ('zoro', 'Roronoa Zoro', 'One Piece', '#e53845', 18),
         ('vegeta', 'Vegeta', 'Dragon Ball', '#fe8c00', 12), ('aizen', 'Sosuke Aizen', 'Bleach', '#fb660f', 9), ('toji', 'Toji Fushiguro', 'Jujutsu Kaisen', '#c8102e', 6)]
voto = ''.join(f'<li class="voto__item" style="--cor:{c};--pct:{v}%"><button type="button" class="voto__btn" data-voto-id="{i}" aria-pressed="false">'
               f'<span class="voto__nome"><b class="voto__h">{e(n)}</b><small>{e(a)}</small></span><span class="voto__barra" aria-hidden="true"><i></i></span><span class="voto__pct" data-pct="{v}">{v}%</span>'
               f'<span class="voto__acao">Votar</span></button></li>' for i, n, a, c, v in VOTOS)

LT = {
    'gojo': ('Arco da Escola Jujutsu e temporada 1', [('Verso 1', 'A apresentação do mais forte: a venda nos olhos, o Infinito que nada atravessa.'), ('Refrão', 'O Vazio Infinito vira refrão: informação sem fim, o rival sem saída.'), ('Verso 2', 'O peso de ser o único: professor, escudo e alvo ao mesmo tempo.')]),
    'goku': ('Saga de Freeza, em Namekusei', [('Verso 1', 'O treino que não acaba e a calma antes da luta.'), ('Refrão', 'A raiva que acende o Super Saiyajin: o grito que passa do limite.'), ('Verso 2', 'Depois da transformação, sempre existe uma forma acima da última.')]),
    'ichigo': ('Arco da Soul Society', [('Verso 1', 'Um garoto que vê espíritos e decide proteger quem ama.'), ('Refrão', 'Bankai no refrão: a espada ganha nome quando o grave entra.'), ('Verso 2', 'A sombra interna que quer o controle, e a escolha de seguir em frente.')]),
    'luffy': ('Arco de Wano', [('Verso 1', 'O chapéu de palha, a promessa e a tripulação que virou família.'), ('Refrão', 'O Rei dos Piratas como destino: liberdade em forma de rima.'), ('Verso 2', 'O Gear Cinco e o riso de quem luta livre.')]),
    'sasuke': ('Arco da Terra das Ondas e Shippuden', [('Verso 1', 'O Sharingan desperta na primeira luta de verdade.'), ('Refrão', 'Olhos que copiam tudo: a vingança contada verso a verso.'), ('Verso 2', 'Os laços cortados e o caminho de volta.')]),
    'megumi': ('Temporada 1 e arco de Shibuya', [('Verso 1', 'As Dez Sombras: cada shikigami entra no beat como uma invocação.'), ('Refrão', 'A sombra como arma e como esconderijo.'), ('Verso 2', 'O filho de Toji e a escolha de quem vale salvar.')]),
}
letras_tpl = ''.join(f'<template id="tpl-letra-{s["id"]}" data-cat="{e(s["anime"])} · {e(LT[s["id"]][0])}" data-k="{s["k1"]}{s["k2"]}" data-tit="Rap de {e(s["personagem"])}: estrutura e referências">'
                     + ''.join(f'<section class="letra-dlg__parte"><h3>{e(t)}</h3><p>{e(x)}</p></section>' for t, x in LT[s["id"]][1]) + '</template>' for s in S)
OBRAS = [('jujutsu-kaisen', 'Jujutsu Kaisen', '無', 'Gojo e Megumi', 'Domínios, maldições e o peso de ser o mais forte.'),
         ('dragon-ball', 'Dragon Ball', '超', 'Goku', 'Treino sem fim e transformações que passam do limite.'),
         ('bleach', 'Bleach', '卍', 'Ichigo', 'Espadas com nome, Bankai e a sombra interna.'),
         ('one-piece', 'One Piece', '海', 'Luffy', 'Liberdade, tripulação e o sonho do Rei dos Piratas.'),
         ('naruto', 'Naruto', '写', 'Sasuke', 'Olhos que copiam tudo, vingança e laços cortados.')]
nfx = {a: sum(1 for s in S if s['slug'] == a) * 2 for a, *_ in OBRAS}
hub = ''.join(f'<li class="hub__item" data-obra="{a}"><button type="button" class="hub__btn" data-anime-choose="{a}" data-hub aria-pressed="false">'
              f'<span class="hub__pad" aria-hidden="true"></span><span class="hub__k" aria-hidden="true">{k}</span>'
              f'<span class="hub__txt"><b class="hub__nome">Rap de {e(n)}</b><small>{e(p)} · {nfx[a]} raps</small><span class="hub__desc">{e(d)}</span></span>'
              f'<span class="hub__acao">Deixar o site no clima</span></button></li>' for a, n, k, p, d in OBRAS)
PAG = open('pagina.html', encoding='utf-8').read()
for nome in ['fone', 'letra', 'beat', 'microfone', 'calendario', 'kanji', 'ondas', 'garantia', 'collab', 'vinil', 'palco', 'video']:
    PAG = PAG.replace('{{IC_' + nome + '}}', icone(nome))
PAG = PAG.replace('{{CAPA_DEST}}', pic('gojo-1', 'Capa da faixa Vazio Infinito', sizes='(min-width: 900px) 30vw, 100vw'))
PAG = PAG.replace('{{CAPA_PLACA1}}', pic('megumi-1', 'Capa de rap encomendado', sizes='(min-width: 900px) 50vw, 100vw'))
PAG = PAG.replace('{{CAPA_PLACA2}}', pic('goku-2', 'Capa de collab', sizes='(min-width: 900px) 50vw, 100vw'))
PAG = PAG.replace('{{CAPA_PLACA3}}', pic('luffy-2', 'Capa de rap para marcas', sizes='(min-width: 900px) 50vw, 100vw'))
for k, v in {'{{FAIXA_OBRAS}}': faixa_obras, '{{PASSOS}}': passos, '{{SEL_CAPAS}}': sel_capas, '{{CARDS}}': cards, '{{FILTROS}}': filtros + filtros_extra,
             '{{CHIPS}}': chips, '{{DIC}}': dic, '{{EST_TABS}}': est_tabs, '{{EST_PAINEIS}}': est_pn, '{{VOTO}}': voto, '{{SEL_PONTOS}}': sel_pontos, '{{HUB}}': hub, '{{LETRAS_TPL}}': letras_tpl, '{{LETRAS}}': letras, '{{GRAFICO}}': e(grafico, quote=True), '{{WA}}': WA, '{{YT}}': YT, '{{SP}}': SP, '{{IG}}': IG}.items():
    PAG = PAG.replace(k, v)
# CSS: os arquivos-fonte ficam separados para editar; o site recebe um só site.css minificado (1 requisição bloqueante, não 14)
import re
css_links = re.findall(r'  <link rel="stylesheet" href="([\w-]+\.css)">\n', PAG)
bruto = '\n'.join(open(c, encoding='utf-8').read() for c in css_links)
mini = re.sub(r'/\*.*?\*/', '', bruto, flags=re.S)
mini = re.sub(r'\s+', ' ', mini)
mini = re.sub(r'\s*([{};,>])\s*', r'\1', mini).replace(';}', '}')
open('site.css', 'w', encoding='utf-8').write(mini.strip())
for i, c in enumerate(css_links):
    PAG = PAG.replace(f'  <link rel="stylesheet" href="{c}">\n', '  <link rel="stylesheet" href="site.css">\n' if i == 0 else '')
print('site.css:', len(css_links), 'arquivos,', round(len(mini) / 1024), 'KB')
open('index.html', 'w', encoding='utf-8').write(PAG)
print('index.html gerado:', len(PAG), 'bytes')
