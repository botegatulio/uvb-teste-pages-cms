# Teste do painel de conteúdo (Pages CMS)

Teste de 03/11/2026 da Kapybara Labs: o painel Pages CMS editando os
`content/*.json` direto no repositório, e cada salvamento publicando a página
pelo GitHub Pages.

Não é o site de nenhum cliente. Formatos e destinos seguem a estrutura real;
contatos, depoimentos e fotos são fictícios.

- `.pages.yml`: o painel (campos, rótulos e ajudas).
- `content/`: o conteúdo, no mesmo formato que o site lê.
- `montar.py`: gera `_site/index.html` a partir do conteúdo (só biblioteca padrão).
- `.github/workflows/publicar.yml`: monta e publica a cada commit na `main`.

Para apagar depois do teste: Settings, General, Delete this repository; e
desinstalar o app do Pages CMS em Settings, Applications, da conta.
