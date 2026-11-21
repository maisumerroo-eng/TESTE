#!/usr/bin/env python3
"""gate-texto.py: gate de texto antes de mostrar o site (skill site-nova-era, references/anti-vicio-ia.md).
Lê só o texto VISÍVEL dos .html (sem scripts/estilos/tags) e acusa:
  travessões, palavras de estoque, construções "não é só X, é Y", atribuições vagas,
  finais grandiosos, palavras entregadoras e emojis.
Dispositivo de marca deliberado (trio desenhado, staccato planejado no dna.md) é ofício: pode ficar.
Uso: python3 gate-texto.py [pasta=.]   → sai com código 1 se achar algo.
"""
import glob, html, re, sys

PADROES = {
    'travessão': r'—|–',
    'estoque': r'\b(alavanc\w*|robust\w*|empoder\w*|destrav\w*|acionáve\w*|orientad\w* a dados|soluç(?:ão|ões)( completas| inovadoras)?|sinergi\w*|escaláve\w*|inovador\w*|excelência|próximo nível|transform\w* seu|tecnologia de ponta|bem-vindo ao nosso|entre em contato conosco|sua melhor escolha|saiba mais|clique aqui)\b',
    'não é só X, é Y': r'não (?:é|são) (?:só|apenas|somente)\b[^.]{0,80}?\b(?:é|são)\b',
    'atribuição vaga': r'\b(?:muitos|vários|diversos) (?:especialistas|estudos|clientes dizem)\b',
    'final grandioso': r'\bo futuro (?:é|será)\b|\bnunca foi tão\b',
    'entregadoras': r'\b(?:testamento|panorama|mergulh\w*|elevar|eleve)\b',
    'emoji': '[\U0001F300-\U0001FAFF☀-➿]',
}

def visivel(t):
    t = re.sub(r'<(script|style|template)[\s\S]*?</\1>', ' ', t, flags=re.I)
    t = re.sub(r'<!--[\s\S]*?-->', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t))

def main(pasta):
    achou = 0
    for f in sorted(glob.glob(f'{pasta}/**/*.html', recursive=True)):
        bruto = open(f, encoding='utf-8').read()
        # variantes de personalização (<template>) também são texto visível: checar separadamente
        partes = [visivel(bruto)] + [visivel(m) for m in re.findall(r'<template[^>]*>([\s\S]*?)</template>', bruto, re.I)]
        texto = ' '.join(partes)
        for nome, pad in PADROES.items():
            m = sorted({x.group(0) for x in re.finditer(pad, texto, re.I)})
            if m:
                achou += len(m)
                print(f'{f}: {nome}: {", ".join(m[:8])}')
    print('gate de texto limpo' if not achou else f'{achou} ocorrência(s): reescrever como afirmação direta e rodar de novo')
    return 1 if achou else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
