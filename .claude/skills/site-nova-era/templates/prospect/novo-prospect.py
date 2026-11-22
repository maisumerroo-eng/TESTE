#!/usr/bin/env python3
"""novo-prospect.py: cria a ficha de um lead para a página por prospect a partir das IMAGENS dele (logo/print do Instagram).
Mede a paleta da imagem e gera prospects/<slug>.json + copia o logo. Só dados públicos do negócio (nome fantasia, cidade,
serviços, logo, fotos publicadas por ele); nada de dado pessoal de pessoa física.
Uso: python3 novo-prospect.py <pasta-do-site> --nome "Padaria Sol" --cidade Campinas --nicho padaria --logo logo.png
       [--foto foto1.jpg --foto foto2.jpg] [--frase "..."] [--whatsapp-agencia 5519...]
"""
import argparse, json, re, shutil, unicodedata
from pathlib import Path
from PIL import Image

def slugify(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def lum(c):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])

def paleta(caminho):
    im = Image.open(caminho).convert('RGBA'); im.thumbnail((300, 300))
    fundo = Image.new('RGBA', im.size, (255, 255, 255, 255)); fundo.alpha_composite(im); im = fundo.convert('RGB')
    q = im.quantize(colors=8, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:24]
    cores = [(pal[i*3], pal[i*3+1], pal[i*3+2]) for _, i in sorted(q.getcolors(), reverse=True)]
    sat = lambda c: 0 if max(c) == 0 else (max(c) - min(c)) / max(c)
    vivas = [c for c in cores if sat(c) > 0.25 and 0.05 < lum(c) < 0.75] or cores
    acento = max(vivas, key=sat)
    claro = tuple(min(255, int(v + (255 - v) * 0.35)) for v in acento)
    escuro = tuple(int(v * 0.62) for v in acento)
    hx = lambda c: '#%02x%02x%02x' % c
    return {'accent': hx(acento), 'accent-claro': hx(claro), 'accent-escuro': hx(escuro), 'sol': hx(acento), 'sol-claro': hx(claro), 'sol-ink': hx(escuro)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('site'); ap.add_argument('--nome', required=True); ap.add_argument('--cidade', default='')
    ap.add_argument('--nicho', default=''); ap.add_argument('--logo', required=True); ap.add_argument('--foto', action='append', default=[])
    ap.add_argument('--frase', default=''); ap.add_argument('--whatsapp-agencia', default='')
    a = ap.parse_args()
    slug = slugify(a.nome); base = Path(a.site) / 'prospects'; pasta = base / slug; pasta.mkdir(parents=True, exist_ok=True)
    logo = pasta / ('logo' + Path(a.logo).suffix.lower()); shutil.copy(a.logo, logo)
    fotos = []
    for k, f in enumerate(a.foto, 1):
        dest = pasta / f'foto-{k}{Path(f).suffix.lower()}'; shutil.copy(f, dest); fotos.append(str(dest.relative_to(a.site)))
    ficha = {'slug': slug, 'nome': a.nome, 'cidade': a.cidade, 'nicho': a.nicho, 'logo': str(logo.relative_to(a.site)), 'fotos': fotos,
             'frase': a.frase, 'cores': paleta(a.logo), 'whatsappAgencia': a.whatsapp_agencia,
             'mensagem': f'Olá! Vi a página que vocês montaram para a {a.nome} e quero conversar.'}
    (base / f'{slug}.json').write_text(json.dumps(ficha, ensure_ascii=False, indent=2))
    print(f'ok: prospects/{slug}.json  cores={ficha["cores"]["accent"]}')
    print(f'link do lead: <url-do-site>/?para={slug}   (página com noindex; versão padrão continua sem parâmetro)')

if __name__ == '__main__':
    main()
