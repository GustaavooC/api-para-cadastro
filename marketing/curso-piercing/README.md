# Plantão Piercing

Campanha de newsjacking para o curso de body piercing (ticket R$250), out–nov/2026.

- `plantao-piercing.html`: plano completo (espelho de pauta, roteiros, legendas, funil, regras).
- `capas/`: capas 1080×1350 prontas para postar; `capas/c01/` (briga dos R$120) e `capas/c10/` (Carnaval) são carrosséis completos.
- `fotos/`: foto do profissional tratada em vermelho sangue e preto (3 recortes × 2 tratamentos).
- `src/`: fonte do conteúdo e dos renderizadores.

## Regerar

```sh
cd marketing/curso-piercing
python3 -I src/editar_foto.py <foto-original.jpg> fotos      # tratamento da foto
python3 -I src/campanha.py                                    # textos -> src/campanha.json
python3 -m http.server 8765 --bind 127.0.0.1 &                # o renderizador lê via http
NODE_PATH=$(npm root -g) node src/render.js                   # capas e carrossel (Playwright)
python3 -I src/build_pagina.py                                # plantao-piercing.html
```

Para editar um texto, mude `src/campanha.py` e rode os três últimos comandos.
