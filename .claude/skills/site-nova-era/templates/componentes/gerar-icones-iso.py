#!/usr/bin/env python3
"""gerar-icones-iso.py: gera um sprite de ícones isométricos (3 tons + acento) a partir de primitivas.
Edite PALETA e ICONES e rode: python3 gerar-icones-iso.py saida.svg
Primitivas: box(x,y,z,w,h,d, acento=False), disco(x,y,z,r) (sol/ponto no topo), traco(pontos 3D) (brilho/linha).
Eixos: x vai para a direita-baixo, z para a esquerda-baixo, y para cima. Unidade ~ 1px*S.
"""
import math, sys

PALETA = {  # Meridiano: carvão, pedra, terracota
    'top': '#4a443d', 'esq': '#2a2622', 'dir': '#1f1c19', 'traco': '#5f574c',
    'acento': '#c4703f', 'acento_dir': '#8f4a24', 'acento_esq': '#a95c31', 'brilho': '#f1b98f',
}
S = 1.0
OX, OY = 40, 46
C, SN = math.cos(math.radians(30)), math.sin(math.radians(30))

def P(x, y, z):
    return (OX + (x - z) * C * S, OY + (x + z) * SN * S - y * S)

def pts(*ps):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in (P(*p) for p in ps))

class Icone:
    def __init__(self): self.formas = []  # (chave_ordem, svg)
    def box(self, x, y, z, w, h, d, acento=False):
        t = PALETA
        topo = t['acento'] if acento else t['top']
        esq = t['acento_esq'] if acento else t['esq']
        dir_ = t['acento_dir'] if acento else t['dir']
        y1 = y + h
        f_top = f'<polygon fill="{topo}" points="{pts((x,y1,z),(x+w,y1,z),(x+w,y1,z+d),(x,y1,z+d))}"/>'
        f_dir = f'<polygon fill="{dir_}" points="{pts((x+w,y,z),(x+w,y,z+d),(x+w,y1,z+d),(x+w,y1,z))}"/>'
        f_esq = f'<polygon fill="{esq}" points="{pts((x,y,z+d),(x+w,y,z+d),(x+w,y1,z+d),(x,y1,z+d))}"/>'
        self.formas.append(((x + w / 2) + (z + d / 2) + y * 0.01, f_dir + f_esq + f_top))
        return self
    def disco(self, x, y, z, r, cor=None):
        cx, cy = P(x, y, z)
        self.formas.append((999, f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r:.1f}" fill="{cor or PALETA["acento"]}" stroke="none"/>'))
        return self
    def traco(self, *p3, cor=None, w=1.6):
        d = 'M' + ' L'.join(f'{a:.1f} {b:.1f}' for a, b in (P(*p) for p in p3))
        self.formas.append((1000, f'<path d="{d}" fill="none" stroke="{cor or PALETA["brilho"]}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'))
        return self
    def svg(self, ident):
        corpo = ''.join(s for _, s in sorted(self.formas, key=lambda f: f[0]))
        return (f'<symbol id="{ident}" viewBox="0 0 80 72"><g stroke="{PALETA["traco"]}" stroke-width="1.2" stroke-linejoin="round">'
                f'{corpo}</g></symbol>')

def ICONES():
    I = {}
    # estudo solar: lote + sol + arco
    i = Icone(); i.box(-14, 0, -14, 28, 4, 28).box(-6, 4, -4, 12, 8, 10, acento=True)
    arco = [(-18 + 36 * t, 8 + 22 * math.sin(math.pi * t), 14 - 28 * t) for t in [k / 12 for k in range(13)]]
    i.traco(*arco, cor=PALETA['brilho'], w=1.1); i.disco(*arco[4], 4.5); I['sol-lote'] = i
    # projeto: pilha de plantas
    i = Icone(); [i.box(-16, k * 7, -12, 32, 3, 24, acento=(k == 2)) for k in range(3)]
    i.traco((-8, 17, -6), (8, 17, -6)).traco((-8, 17, 0), (2, 17, 0)); I['plantas'] = i
    # estrutura: pilares + laje
    i = Icone()
    for (a, b) in [(-12, -12), (8, -12), (-12, 8), (8, 8)]: i.box(a, 0, b, 4, 18, 4)
    i.box(-16, 18, -16, 32, 4, 32, acento=True); i.traco((-10, 22, -12), (10, 22, -12)); I['estrutura'] = i
    # cronograma: barras crescentes
    i = Icone()
    i.box(-20, 0, -12, 40, 2, 24)
    for k, h in enumerate([8, 13, 19, 26]): i.box(-17 + k * 9, 2, -4, 6, h, 8, acento=(k == 3))
    I['cronograma'] = i
    # casa/entrega: volume + laje em balanço
    i = Icone(); i.box(-14, 0, -10, 22, 14, 20).box(-18, 14, -14, 34, 3, 28, acento=True).box(8, 0, -10, 6, 20, 8)
    i.traco((-12, 17, -12), (6, 17, -12)); I['casa'] = i
    # régua/nível
    i = Icone(); i.box(-20, 0, -5, 40, 7, 10).box(-7, 7, -2, 14, 3, 4, acento=True)
    i.traco((-1, 10, -1), (3, 10, -1), cor='#fff3e6', w=1.6); I['nivel'] = i
    # janela/esquadria
    i = Icone(); i.box(-16, 0, -6, 32, 2, 12)
    i.box(-14, 2, -2, 28, 28, 3).box(-11, 5, 1, 10, 22, 1, acento=True).box(1, 5, 1, 10, 22, 1, acento=True); I['esquadria'] = i
    # bloco de concreto
    i = Icone(); i.box(-12, 0, -12, 24, 16, 24).box(-12, 16, -12, 24, 3, 24, acento=True)
    i.traco((-6, 19, -8), (6, 19, -8)).traco((-6, 19, -2), (2, 19, -2)); I['bloco'] = i
    # garantia: placa com check
    i = Icone(); i.box(-14, 0, -14, 28, 6, 28).box(-14, 6, -14, 28, 2, 28, acento=True)
    i.traco((-6, 8, 2), (-1, 8, 6), (9, 8, -6), cor='#fff3e6', w=2.2); I['garantia'] = i
    # grua
    i = Icone(); i.box(-14, 0, -14, 28, 2, 28).box(-2, 2, -2, 5, 26, 5).box(-14, 28, -1, 28, 3, 4, acento=True).box(-16, 22, -2, 5, 6, 6).box(10, 18, 0, 1, 10, 1); I['grua'] = i
    # região: placa + pino
    i = Icone(); i.box(-16, 0, -16, 32, 3, 32).box(-2, 3, -2, 4, 14, 4, acento=True); i.disco(0, 22, 0, 6); i.disco(0, 22.5, 0, 2.2, cor='#fff3e6'); I['regiao'] = i
    # impermeabilização: placa + gota
    i = Icone(); i.box(-16, 0, -16, 32, 4, 32).box(-16, 4, -16, 32, 2, 32, acento=True)
    cx, cy = P(0, 18, 0); I['agua'] = i
    i.formas.append((1001, f'<path d="M{cx:.1f} {cy-9:.1f} C{cx+6:.1f} {cy-1:.1f} {cx+5:.1f} {cy+5:.1f} {cx:.1f} {cy+5:.1f} C{cx-5:.1f} {cy+5:.1f} {cx-6:.1f} {cy-1:.1f} {cx:.1f} {cy-9:.1f}Z" fill="{PALETA["brilho"]}" stroke="none"/>'))
    # diário de obra: tablet
    i = Icone(); i.box(-18, 0, -14, 36, 3, 28).box(-15, 3, -11, 30, 1, 22, acento=True)
    i.traco((-9, 4, -5), (9, 4, -5)).traco((-9, 4, 1), (3, 4, 1)).traco((-9, 4, 7), (5, 4, 7)); I['diario'] = i
    return I

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'icones.svg'
    syms = ''.join(ic.svg(k) for k, ic in ICONES().items())
    open(out, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none">{syms}</svg>\n')
    print('ok', out, len(ICONES()), 'ícones')
