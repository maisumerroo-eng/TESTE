#!/usr/bin/env python3
"""paleta-da-imagem.py: mede a paleta real de uma imagem (screenshot, mockup, foto da marca) em vez de chutar cores.
Uso: python3 paleta-da-imagem.py imagem.png [n=8]
Saída: cores dominantes (hex, % da área, papel provável) + tokens CSS prontos para colar em :root.
"""
import sys
from PIL import Image

def lum(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (c(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def sat(rgb):
    mx, mn = max(rgb), min(rgb)
    return 0 if mx == 0 else (mx - mn) / mx

def main(caminho, n=8):
    im = Image.open(caminho).convert('RGB')
    im.thumbnail((400, 400))
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: n * 3]
    contagem = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in contagem)
    cores = [((pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]), c / total) for c, i in contagem]
    hexa = lambda rgb: '#%02x%02x%02x' % rgb
    fundo = cores[0][0]
    acento = max(cores, key=lambda x: sat(x[0]) * (0.3 + x[1]))[0]
    escuro = min(cores, key=lambda x: lum(x[0]))[0]
    claro = max(cores, key=lambda x: lum(x[0]))[0]
    print('cor        área   papel provável')
    for rgb, p in cores:
        papel = 'fundo' if rgb == fundo else 'acento' if rgb == acento else 'texto/escuro' if rgb == escuro else 'claro' if rgb == claro else 'neutro'
        print(f'{hexa(rgb)}  {p*100:5.1f}%  {papel}')
    print('\n:root {')
    print(f'  --fundo: {hexa(fundo)};\n  --acento: {hexa(acento)};\n  --escuro: {hexa(escuro)};\n  --claro: {hexa(claro)};')
    neutros = [hexa(rgb) for rgb, _ in cores if rgb not in (fundo, acento, escuro, claro)][:3]
    for k, h in enumerate(neutros, 1):
        print(f'  --neutro-{k}: {h};')
    print('}')
    print('\nConferir contraste texto/fundo com auditar-contraste.js depois de aplicar.')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8)
