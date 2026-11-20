"""Uso: DEPLOY_DIR=pasta python3 scripts/deploy-cloudflare.py   (precisa: pip install blake3)
Deploy direto no Cloudflare Pages (mesmo fluxo do wrangler).
Chamadas com o token da conta passam pelo proxy (que injeta a chave).
Chamadas com o JWT de upload vão direto (--noproxy), senão o proxy troca o JWT pelo token."""
import base64, json, mimetypes, os, subprocess, sys
from blake3 import blake3

ACC = 'fb9c736ef68a52080340ac2abf7327e1'
PROJ = 'bravo-menswear'
ROOT = os.environ.get('DEPLOY_DIR', 'deploy')  # pasta pronta do site (sem admin e sem referencias)
API = 'https://api.cloudflare.com/client/v4'
TMP = '/tmp/cf_body.json'


def curl(args, direto=False):
    cmd = ['curl', '-sS'] + (['--noproxy', '*'] if direto else []) + args
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    d = json.loads(out)
    if not d.get('success'):
        sys.exit(f'ERRO {args[-1] if args else ""}: {d.get("errors")}')
    return d.get('result')


# 1. Arquivos + hash (blake3(base64 + extensão)[:32], igual ao wrangler)
arquivos = {}
for pasta, _, nomes in os.walk(ROOT):
    for n in nomes:
        full = os.path.join(pasta, n)
        rel = '/' + os.path.relpath(full, ROOT)
        conteudo = open(full, 'rb').read()
        b64 = base64.b64encode(conteudo).decode()
        ext = os.path.splitext(n)[1][1:]
        h = blake3((b64 + ext).encode()).hexdigest()[:32]
        tipo = mimetypes.guess_type(n)[0] or 'application/octet-stream'
        arquivos[rel] = {'hash': h, 'b64': b64, 'tipo': tipo}
print(len(arquivos), 'arquivos')

# 2. JWT de upload (via proxy, com o token da conta)
jwt = curl(['-H', 'Authorization: Bearer proxy-injected',
            f'{API}/accounts/{ACC}/pages/projects/{PROJ}/upload-token'])['jwt']
auth = ['-H', f'Authorization: Bearer {jwt}', '-H', 'Content-Type: application/json']

# 3. Quais faltam (direto)
hashes = sorted({a['hash'] for a in arquivos.values()})
json.dump({'hashes': hashes}, open(TMP, 'w'))
faltam = set(curl(auth + ['-X', 'POST', '--data-binary', '@' + TMP, f'{API}/pages/assets/check-missing'], direto=True))
print(len(faltam), 'para enviar')

# 4. Envio em lotes de ~8 MB (direto)
lote, tam = [], 0
def enviar(lote):
    json.dump(lote, open(TMP, 'w'))
    curl(auth + ['-X', 'POST', '--data-binary', '@' + TMP, f'{API}/pages/assets/upload'], direto=True)
ja = set()
for a in arquivos.values():
    if a['hash'] not in faltam or a['hash'] in ja:
        continue
    ja.add(a['hash'])
    lote.append({'key': a['hash'], 'value': a['b64'], 'metadata': {'contentType': a['tipo']}, 'base64': True})
    tam += len(a['b64'])
    if tam > 8_000_000:
        enviar(lote); lote, tam = [], 0
if lote:
    enviar(lote)
print('upload ok')

# 5. Marca os hashes (direto)
json.dump({'hashes': hashes}, open(TMP, 'w'))
curl(auth + ['-X', 'POST', '--data-binary', '@' + TMP, f'{API}/pages/assets/upsert-hashes'], direto=True)

# 6. Cria o deploy com o manifesto (via proxy)
manifesto = json.dumps({k: v['hash'] for k, v in arquivos.items()})
r = curl(['-H', 'Authorization: Bearer proxy-injected', '-X', 'POST',
          '-F', f'manifest={manifesto}', '-F', 'branch=main',
          f'{API}/accounts/{ACC}/pages/projects/{PROJ}/deployments'])
print('DEPLOY', r.get('id'), r.get('url'), r.get('latest_stage', {}).get('status'))
