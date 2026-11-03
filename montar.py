#!/usr/bin/env python3
"""Página de teste: lê os content/*.json e grava _site/index.html com as fotos.

Não é o site da Uma Viagem Bárbara: só prova a corrente do painel, em que
salvar no Pages CMS vira commit, o commit dispara o GitHub Actions e a página
publicada muda. Só biblioteca padrão, como o build.py do site.
"""
import html
import json
import os
import shutil
from datetime import datetime, timezone
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, '_site')


def ler(nome):
    with open(os.path.join(RAIZ, 'content', f'{nome}.json'), encoding='utf-8') as f:
        return json.load(f)


def e(texto):
    return html.escape(str(texto or ''))


def main():
    site, formatos, destinos, relatos = ler('site'), ler('servicos'), ler('destinos'), ler('depoimentos')
    nomes = {d['slug']: d['nome'] for d in destinos}
    regiao = {'asia': 'Ásia', 'extra': 'Extras'}
    presenca = {'pagina': 'Tem página própria', 'mencao': 'Só no mapa e na lista'}
    wa = f'https://wa.me/{e(site.get("whatsapp"))}'

    partes = ['<h2>Formatos</h2>']
    for f in sorted(formatos, key=lambda x: x.get('ordem') or 99):
        partes.append(
            f'<article><h3>{e(f["nome"])}</h3><p>{e(f.get("frase"))}</p>'
            f'<p><b>{e(f.get("preco"))}</b></p><p>{e(f.get("legenda"))}</p>'
            f'<a href="{wa}?text={quote(f.get("mensagem_whatsapp") or "")}">Falar no WhatsApp</a></article>'
        )
    partes.append('<h2>Destinos</h2><div class="grade">')
    for d in sorted(destinos, key=lambda x: x.get('ordem') or 99):
        foto = f'<img src="{e(d["foto"])}" alt="{e(d["nome"])}" width="240">' if d.get('foto') else ''
        frase = (d.get('mapa') or {}).get('d')
        partes.append(
            f'<figure>{foto}<figcaption><b>{e(d["nome"])}</b> ({e(regiao.get(d.get("regiao"), d.get("regiao")))}, '
            f'{e(presenca.get(d.get("status"), d.get("status")))})<br><i>{e(frase)}</i></figcaption></figure>'
        )
    partes.append('</div><h2>Depoimentos (só os autorizados)</h2>')
    for r in relatos:
        if not r.get('ok_publicacao'):
            continue
        partes.append(
            f'<blockquote>{e(r["texto"])}<footer>{e(r["autor"])}, {e(nomes.get(r.get("destino"), r.get("destino")))}</footer></blockquote>'
        )

    agora = datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')
    commit = os.environ.get('GITHUB_SHA', 'local')[:7]
    pagina = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Teste do painel</title>
<style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:0 auto;padding:16px;line-height:1.5}}
.grade{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}}
img{{max-width:100%;height:auto}} article,blockquote{{border-top:1px solid #ccc;padding:8px 0}}</style>
</head><body>
<p><small>Página de teste do painel de conteúdo. Montada em {agora}, commit {e(commit)}.</small></p>
{''.join(partes)}
</body></html>
'''
    shutil.rmtree(SAIDA, ignore_errors=True)
    shutil.copytree(os.path.join(RAIZ, 'content', 'fotos'), os.path.join(SAIDA, 'fotos'))
    with open(os.path.join(SAIDA, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina)
    print(f'_site/index.html: {len(formatos)} formatos, {len(destinos)} destinos, '
          f'{sum(1 for r in relatos if r.get("ok_publicacao"))} depoimento(s) autorizado(s)')


if __name__ == '__main__':
    main()
