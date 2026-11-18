import re
svg = open('../../marcas/skull/skull-logo.svg').read()
inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
inner = re.sub(r'<title>.*?</title>', '', inner)
js = open('../../marcas/skull/gerar-svg.js').read()
L = re.search(r'const L = \[(.*?)\];', js, re.S).group(1)
pts = set()
for x, y in re.findall(r'(\d+) (\d+)', L):
    x, y = int(x), int(y)
    for xx in (x, 720 - x):
        pts.add((round(200 + xx/3, 1), round(95 + y/3, 1)))
ghost = re.sub(r' id="[^"]*"', '', re.search(r'(<g id="simbolo".*?</g>\s*</g>)', inner, re.S).group(1) + re.search(r'<path id="nome"[^>]*/>', inner).group(0))
circ = ''.join(f'<circle cx="{x}" cy="{y}" r="2.6"/>' for x, y in sorted(pts))
logo = f'<svg viewBox="80 70 480 500" xmlns="http://www.w3.org/2000/svg">{inner}<g class="fantasma">{ghost}</g><g class="pontos">{circ}</g></svg>'
open('index.html', 'w').write(open('fonte.html').read().replace('<!--LOGO-->', logo))
print(len(pts), 'pontos')
