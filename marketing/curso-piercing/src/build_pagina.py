"""Gera plantao-piercing.html (plano da campanha) a partir de campanha.json.

Uso: python3 -I build_pagina.py   (rodar dentro de src/)
"""
import json, os, re, html

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
D = json.load(open(os.path.join(AQUI, "campanha.json"), encoding="utf-8"))
CS = D["carrosseis"]

def esc(s):
    return html.escape(s, quote=True)

def marca(s):
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]", r"<b>\1</b>", s)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)

def limpa(s):
    return re.sub(r"[\[\]]", "", re.sub(r"\*([^*]+)\*", r"\1", s))

def chip(c):
    if c["impulsionar"]:
        return '<span class="chip ok">Pode impulsionar</span>'
    return '<span class="chip no">Só orgânico</span>'

# ---------- espelho ----------
linhas = "\n".join(
    f'<tr><td class="num">{c["data"]}</td><td class="dia">{c["dia"]}</td>'
    f'<td><a href="#{c["id"]}">{esc(c["nome"])}</a></td><td>{c["publico"]}</td><td>{chip(c)}</td></tr>'
    for c in CS)

# ---------- pautas ----------
def pauta(c):
    slides = "".join(f"<li>{marca(s)}</li>" for s in c["slides"])
    fontes = "".join(f'<li><a href="{esc(f["u"])}" target="_blank" rel="noopener">{esc(f["t"])}</a></li>' for f in c["fontes"])
    leg_id = f'leg-{c["id"]}'
    return f'''
<article class="pauta" id="{c["id"]}">
  <a class="capa" href="capas/{c["id"]}-capa.jpg" target="_blank" rel="noopener"><img src="capas/{c["id"]}-capa.jpg" alt="Capa: {esc(limpa(c["head"]))}" loading="lazy" width="1080" height="1350"></a>
  <div class="corpo">
    <p class="meta"><span class="data">{c["data"]} · {c["dia"]}</span><span>{c["publico"]}</span>{chip(c)}</p>
    <h3>{esc(c["nome"])}</h3>
    <p class="nota">{esc(c["nota_impulso"])}</p>
    <h4>Roteiro dos slides</h4>
    <ol class="slides">{slides}</ol>
    <div class="leg-cab"><h4>Legenda</h4><button type="button" class="copiar" data-alvo="{leg_id}">Copiar legenda</button></div>
    <pre class="legenda" id="{leg_id}">{esc(c["legenda"])}</pre>
    <h4>Fontes da notícia</h4>
    <ul class="fontes">{fontes}</ul>
  </div>
</article>'''

pautas = "\n".join(pauta(c) for c in CS)

comp = next(c for c in CS if c["id"] == D["completo"])
tira = "".join(
    f'<a href="capas/{comp["id"]}/{i:02d}.jpg" target="_blank" rel="noopener"><img src="capas/{comp["id"]}/{i:02d}.jpg" alt="Slide {i} de {len(comp["slides"])}" loading="lazy" width="1080" height="1350"></a>'
    for i in range(1, len(comp["slides"]) + 1))

FOTOS = [("cena", "Sala inteira: descarte, EPI, bancada"), ("atendimento", "Piercer e cliente"), ("piercer", "Close do profissional")]
fotos = "".join(
    f'<figure><a href="fotos/{n}-{m}.jpg" target="_blank" rel="noopener"><img src="fotos/{n}-{m}.jpg" alt="{esc(t)}, tratamento {m}" loading="lazy" width="1080" height="1350"></a>'
    f'<figcaption><span class="mono">{n}-{m}.jpg</span>{esc(t)}</figcaption></figure>'
    for n, t in FOTOS for m in ("sangue", "noir"))

anuncios = "".join(
    f'<div class="anuncio"><p class="mono">ANÚNCIO · {esc(a["nome"]).upper()}</p><h4>{esc(a["titulo"])}</h4>'
    f'<pre class="legenda" id="ad-{i}">{esc(a["texto"])}</pre>'
    f'<p class="peq">Imagem: {("fotos/" + a["foto"] + ".jpg") if a["foto"] else "capa tipográfica do c07 sem o título"}</p>'
    f'<button type="button" class="copiar" data-alvo="ad-{i}">Copiar texto</button></div>'
    for i, a in enumerate(D["anuncios"]))

reels = "".join(f'<li><strong>“{esc(r["gancho"])}”</strong><span>{esc(r["nota"])}</span></li>' for r in D["reels"])

PAGINA = f'''<meta charset="utf-8">
<title>Plantão Piercing</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&family=IBM+Plex+Mono:wght@500&family=Unbounded:wght@700;900&display=swap">
<style>
/* Layout: espelho de pauta de redação. Calendário em tabela, cada pauta com capa à esquerda e roteiro à direita. */
:root {{
  --preto: #0b0707;
  --painel: #150c0c;
  --linha: #2c1a1a;
  --osso: #f1e9e6;
  --cinza: #b6a4a2;
  --sangue: #8e0710;
  --sangue-vivo: #ec2a33;
  --verde: #6fcf8e;
  --display: 'Unbounded', 'Arial Black', sans-serif;
  --texto: 'Archivo', 'Helvetica Neue', Arial, sans-serif;
  --mono: 'IBM Plex Mono', ui-monospace, 'SFMono-Regular', monospace;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--preto); color: var(--osso); font: 400 16px/1.6 var(--texto); }}
.pagina {{ max-width: 1120px; margin: 0 auto; padding-inline: 20px; padding-block: 40px 80px; display: grid; gap: 72px; }}
a {{ color: var(--osso); text-decoration-color: var(--sangue-vivo); text-underline-offset: 3px; }}
a:focus-visible, button:focus-visible {{ outline: 2px solid var(--sangue-vivo); outline-offset: 3px; }}
h1, h2, h3, h4 {{ text-wrap: balance; margin: 0; }}
h2 {{ font: 900 clamp(22px, 3.2vw, 30px)/1.15 var(--display); text-transform: uppercase; letter-spacing: -.005em; }}
h3 {{ font: 800 24px/1.2 var(--texto); }}
h4 {{ font: 600 13px/1.3 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--cinza); }}
p {{ margin: 0; }}
.mono {{ font: 500 12px/1.4 var(--mono); letter-spacing: .1em; color: var(--cinza); }}
.peq {{ font-size: 14px; color: var(--cinza); }}
.secao {{ display: grid; gap: 24px; }}
.secao > header {{ display: grid; gap: 8px; max-width: 68ch; }}
.secao > header p {{ color: var(--cinza); }}

/* topo */
.topo {{ display: grid; gap: 20px; padding-bottom: 32px; border-bottom: 1px solid var(--linha); }}
.olho {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
.live {{ display: inline-flex; align-items: center; gap: 8px; background: var(--sangue); color: var(--osso); font: 800 12px/1 var(--texto); letter-spacing: .16em; padding: 8px 12px; }}
.live i {{ width: 7px; height: 7px; border-radius: 50%; background: var(--osso); }}
h1 {{ font: 900 clamp(40px, 8vw, 84px)/.95 var(--display); text-transform: uppercase; letter-spacing: -.02em; }}
h1 em {{ font-style: normal; color: var(--sangue-vivo); }}
.lede {{ font-size: 19px; max-width: 62ch; color: var(--osso); }}
.numeros {{ display: flex; flex-wrap: wrap; gap: 10px 28px; font: 500 14px/1.4 var(--mono); color: var(--cinza); }}
.numeros strong {{ color: var(--osso); font-weight: 500; }}
.aviso {{ border-left: 3px solid var(--sangue-vivo); padding: 10px 14px; background: var(--painel); max-width: 70ch; font-size: 15px; }}

/* espelho */
.tabela {{ overflow-x: auto; border: 1px solid var(--linha); }}
table {{ border-collapse: collapse; width: 100%; min-width: 560px; font-size: 15px; }}
th, td {{ text-align: left; padding: 11px 14px; border-bottom: 1px solid var(--linha); vertical-align: middle; }}
th {{ font: 500 11px/1.2 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--cinza); background: var(--painel); }}
tr:last-child td {{ border-bottom: 0; }}
td.num {{ font: 500 14px/1 var(--mono); font-variant-numeric: tabular-nums; }}
td.dia {{ color: var(--cinza); font-size: 14px; }}
.chip {{ display: inline-block; font: 600 11px/1 var(--mono); letter-spacing: .06em; text-transform: uppercase; padding: 6px 8px; border: 1px solid; white-space: nowrap; }}
.chip.ok {{ color: var(--verde); border-color: color-mix(in srgb, var(--verde) 45%, transparent); }}
.chip.no {{ color: var(--sangue-vivo); border-color: color-mix(in srgb, var(--sangue-vivo) 55%, transparent); }}

/* pautas */
.pautas {{ display: grid; gap: 28px; }}
.pauta {{ display: grid; grid-template-columns: minmax(0, 340px) minmax(0, 1fr); gap: 28px; padding: 24px; background: var(--painel); border: 1px solid var(--linha); scroll-margin-top: 16px; }}
.capa img {{ display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; max-width: 100%; }}
.corpo {{ display: grid; gap: 14px; align-content: start; min-width: 0; }}
.meta {{ display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; font: 500 13px/1.3 var(--mono); color: var(--cinza); }}
.meta .data {{ color: var(--osso); }}
.nota {{ color: var(--cinza); font-size: 15px; }}
.slides {{ margin: 0; padding-left: 26px; display: grid; gap: 6px; font-size: 15px; }}
.slides li::marker {{ font: 500 12px var(--mono); color: var(--sangue-vivo); }}
.slides em, h1 em {{ font-style: normal; color: var(--sangue-vivo); }}
.slides b {{ font-weight: 800; }}
.leg-cab {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }}
pre.legenda {{ margin: 0; white-space: pre-wrap; font: 400 15px/1.55 var(--texto); background: var(--preto); border: 1px solid var(--linha); padding: 14px; }}
.copiar {{ font: 600 12px/1 var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--osso); background: var(--sangue); border: 0; padding: 9px 12px; cursor: pointer; }}
.copiar:hover {{ background: #a50a14; }}
.fontes {{ margin: 0; padding-left: 18px; font-size: 14px; display: grid; gap: 4px; }}

/* carrossel completo */
.tira {{ display: grid; grid-auto-flow: column; grid-auto-columns: minmax(220px, 260px); gap: 12px; overflow-x: auto; padding-bottom: 10px; scroll-snap-type: x mandatory; }}
.tira a {{ scroll-snap-align: start; }}
.tira img {{ display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; }}

/* fotos */
.fotos {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr)); gap: 16px; }}
.fotos figure {{ margin: 0; display: grid; gap: 8px; }}
.fotos img {{ display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; }}
.fotos figcaption {{ display: grid; gap: 2px; font-size: 14px; color: var(--cinza); }}

/* funil e números */
.duas {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 28px; }}
.passos {{ margin: 0; padding: 0; list-style: none; counter-reset: p; display: grid; gap: 16px; }}
.passos li {{ counter-increment: p; display: grid; grid-template-columns: 40px 1fr; gap: 12px; }}
.passos li::before {{ content: counter(p, decimal-leading-zero); font: 900 20px/1.2 var(--display); color: var(--sangue-vivo); }}
.passos strong {{ display: block; }}
.contas {{ display: grid; gap: 0; border: 1px solid var(--linha); }}
.contas div {{ display: flex; justify-content: space-between; gap: 16px; padding: 12px 14px; border-bottom: 1px solid var(--linha); }}
.contas div:last-child {{ border-bottom: 0; }}
.contas dt {{ color: var(--cinza); font-size: 15px; }}
.contas dd {{ margin: 0; font: 500 15px/1.4 var(--mono); font-variant-numeric: tabular-nums; text-align: right; }}

/* anúncios */
.anuncios {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 16px; }}
.anuncio {{ display: grid; gap: 10px; align-content: start; padding: 18px; border: 1px solid var(--linha); background: var(--painel); }}
.anuncio .copiar {{ justify-self: start; }}
.reels {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 12px; }}
.reels li {{ display: grid; gap: 2px; padding-bottom: 12px; border-bottom: 1px solid var(--linha); }}
.reels span {{ color: var(--cinza); font-size: 14px; }}

/* regras */
.regras {{ margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 16px; }}
.regras li {{ padding: 16px; border-top: 3px solid var(--sangue); background: var(--painel); display: grid; gap: 6px; font-size: 15px; }}
.regras strong {{ font-size: 16px; }}

@media (max-width: 720px) {{
  .pauta {{ grid-template-columns: 1fr; padding: 16px; }}
  .capa {{ max-width: 420px; }}
  .pagina {{ gap: 56px; padding-block: 28px 60px; padding-inline: 16px; }}
}}
@media (prefers-reduced-motion: no-preference) {{
  .live i {{ animation: pisca 1.6s ease-in-out infinite; }}
  @keyframes pisca {{ 50% {{ opacity: .25; }} }}
}}
</style>

<main class="pagina">
  <header class="topo">
    <p class="olho"><span class="live"><i></i>PLANTÃO</span><span class="mono">CURSO DE BODY PIERCING · TICKET R$250 · 08/10 → 30/11/2026</span></p>
    <h1>Plantão <em>Piercing</em></h1>
    <p class="lede">Onze pautas de newsjacking com notícias reais desta semana até a Black Friday, com capas prontas em 1080×1350 na paleta vermelho sangue e preto, usando a foto do profissional tratada.</p>
    <p class="numeros"><span><strong>11</strong> capas prontas</span><span><strong>1</strong> carrossel completo</span><span><strong>6</strong> versões da foto</span><span><strong>3</strong> anúncios de venda</span><span><strong>5</strong> ganchos de Reels</span></p>
    <p class="aviso">Antes de postar: troque <strong>@seu.perfil</strong> e a marca <strong>BP</strong> pelo seu @ e logo. Dados de eleição e famosos foram conferidos em 08/10/2026; confira de novo no dia da postagem.</p>
  </header>

  <section class="secao" id="espelho">
    <header><h2>Espelho de pauta</h2><p>Ordem de postagem. Três carrosséis por semana; o do umbigo (13/11) é o melhor candidato a anúncio.</p></header>
    <div class="tabela"><table>
      <thead><tr><th>Data</th><th>Dia</th><th>Pauta</th><th>Público</th><th>Mídia paga</th></tr></thead>
      <tbody>{linhas}</tbody>
    </table></div>
    <p class="peq">Pauta reativa: no dia 26/10, com o resultado do 2º turno, poste um slide único e neutro: “Segunda-feira. O seu cliente continua precisando de alguém que fure certo.” Deixe pronto antes, sem citar quem ganhou.</p>
  </section>

  <section class="secao" id="pautas">
    <header><h2>As pautas</h2><p>Toque na capa para abrir em tamanho real e salvar. Os slides internos seguem o modelo do carrossel completo logo abaixo.</p></header>
    <div class="pautas">{pautas}</div>
  </section>

  <section class="secao" id="completo">
    <header><h2>Carrossel completo: {esc(comp["nome"])}</h2><p>Os {len(comp["slides"])} slides prontos. Use o mesmo modelo (número grande, régua vermelha, texto em bloco) para montar os slides internos das outras pautas.</p></header>
    <div class="tira">{tira}</div>
  </section>

  <section class="secao" id="fotos">
    <header><h2>Foto do profissional, tratada</h2><p>Três recortes 4:5 em dois tratamentos. “Sangue” é duotone vermelho e preto; “noir” é preto e branco duro com luz vermelha.</p></header>
    <div class="fotos">{fotos}</div>
    <p class="aviso">O cliente aparece no rosto nos recortes “cena” e “atendimento”. Peça autorização de uso de imagem por escrito antes de postar, ou use o recorte “piercer”. A estampa de marca na camiseta do cliente fica coberta pelo degradê nas capas; evite essa área em anúncio pago.</p>
  </section>

  <section class="secao" id="funil">
    <header><h2>Funil e números</h2><p>Ticket baixo só fecha a conta com volume e custo por venda controlado. O orgânico atrai, o anúncio converte quem já te conhece.</p></header>
    <div class="duas">
      <ol class="passos">
        <li><div><strong>Orgânico</strong>As pautas do espelho, três por semana, mais Reels com os ganchos abaixo.</div></li>
        <li><div><strong>Impulsionar</strong>Só pautas marcadas “pode impulsionar”, e só as que tiverem mais salvamentos e compartilhamentos nas primeiras 48h. Público frio: 18 a 40 anos, interesses em piercing, tatuagem, body art, estética e renda extra.</div></li>
        <li><div><strong>Retargeting</strong>Quem engajou com o perfil nos últimos 30 dias ou visitou a página de vendas recebe os 3 anúncios de venda.</div></li>
        <li><div><strong>Recuperação</strong>Carrinho abandonado: mensagem no WhatsApp ou e-mail em até 1 hora.</div></li>
      </ol>
      <dl class="contas">
        <div><dt>Preço</dt><dd>R$250 ou 12x de ~R$25</dd></div>
        <div><dt>Líquido por venda (taxa ~10%, confira a sua)</dt><dd>~R$225</dd></div>
        <div><dt>Custo por venda de empate</dt><dd>~R$225</dd></div>
        <div><dt>Custo por venda alvo</dt><dd>até R$75</dd></div>
        <div><dt>Troque o criativo se passar de</dt><dd>R$110 por 3 dias</dd></div>
        <div><dt>Teste inicial</dt><dd>R$50/dia × 7 dias</dd></div>
        <div><dt>Order bump sugerido</dt><dd>R$27 a R$47</dd></div>
      </dl>
    </div>
    <p class="peq">Order bump: kit de modelos (ficha de anamnese, termo de consentimento, tabela de preços). Concorrência: encontrei curso online de body piercing a R$297 (12x de R$29,64). Seu R$250 fica abaixo; venda como “o preço de uns 2 furos” e nunca cite concorrente no anúncio.</p>
  </section>

  <section class="secao" id="anuncios">
    <header><h2>Anúncios de venda e Reels</h2><p>Os anúncios rodam só no retargeting. Os ganchos de Reels são para gravar com o profissional da foto.</p></header>
    <div class="anuncios">{anuncios}</div>
    <h3>Ganchos de Reels</h3>
    <ul class="reels">{reels}</ul>
  </section>

  <section class="secao" id="regras">
    <header><h2>Regras do jogo</h2><p>Agressivo na capa, correto nos fatos. Isso é o que evita post derrubado, anúncio reprovado e processo.</p></header>
    <ul class="regras">
      <li><strong>Eleição só no orgânico</strong>As pautas 01 e 05 não podem ser impulsionadas. A Lei 9.504/97 (art. 57-C) só permite impulsionar conteúdo eleitoral a candidatos, partidos e coligações, e a Meta exige autorização para anúncio sobre política. Cite os dois candidatos ou nenhum.</li>
      <li><strong>Nada de foto de famoso ou político</strong>Uso comercial de imagem sem autorização gera indenização (Código Civil, art. 20; STJ, Súmula 403). Por isso as capas usam tipografia ou a foto do próprio profissional.</li>
      <li><strong>Renda sempre como exemplo</strong>Mostre a conta com custos e asterisco. Nunca “você vai ganhar”. A Meta reprova anúncio com promessa de ganho.</li>
      <li><strong>Saúde sem promessa</strong>Nada de “zero risco” ou “não inflama”. Nada de foto de ferida, sangue, infecção ou suspensão em anúncio.</li>
      <li><strong>Curso não é alvará</strong>Deixe claro na página de vendas que atender exige alvará sanitário. A Anvisa classifica piercing como atividade de alto risco.</li>
      <li><strong>Menores de idade</strong>Autorização e presença dos responsáveis, e confira a lei do seu estado e município.</li>
    </ul>
  </section>

  <section class="secao" id="formula">
    <header><h2>Como fazer a próxima pauta em 2 horas</h2><p>Quando sair uma notícia nova, passe por estas cinco etapas, nesta ordem. Se a ponte com piercing precisar ser forçada, descarte a notícia.</p></header>
    <ol class="passos">
      <li><div><strong>Fato</strong>Notícia real com menos de 72 horas. Fonte e data no rodapé da capa.</div></li>
      <li><div><strong>Tensão</strong>O que o público sente com ela: medo, raiva, inveja ou pressa.</div></li>
      <li><div><strong>Ponte</strong>A ligação honesta entre a notícia e piercing.</div></li>
      <li><div><strong>Lição</strong>Um ensinamento de técnica ou de mercado, em 3 a 5 slides.</div></li>
      <li><div><strong>Oferta</strong>O curso no último slide e na legenda.</div></li>
    </ol>
    <p class="peq">Fontes de regras: <a href="https://www.planalto.gov.br/ccivil_03/leis/l9504.htm" target="_blank" rel="noopener">Lei 9.504/97</a> · <a href="https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm" target="_blank" rel="noopener">Código Civil</a> · <a href="https://www.gov.br/anvisa/pt-br/assuntos/servicosdesaude/saloes-tatuagens-creches/tatuagem-e-piercing" target="_blank" rel="noopener">Anvisa: tatuagem e piercing</a> · <a href="https://www.portalinsights.com.br/perguntas-frequentes/quanto-um-body-piercer-ganha" target="_blank" rel="noopener">preço de curso concorrente</a></p>
  </section>
</main>

<script>
document.querySelectorAll('.copiar').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    var alvo = document.getElementById(btn.dataset.alvo);
    var texto = alvo.textContent;
    var original = btn.textContent;
    function marcar() {{
      var r = document.createRange(); r.selectNodeContents(alvo);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      btn.textContent = 'Texto selecionado';
      setTimeout(function () {{ btn.textContent = original; }}, 1800);
    }}
    try {{
      navigator.clipboard.writeText(texto).then(function () {{
        btn.textContent = 'Copiado';
        setTimeout(function () {{ btn.textContent = original; }}, 1800);
      }}, marcar);
    }} catch (e) {{ marcar(); }}
  }});
}});
</script>
'''

with open(os.path.join(RAIZ, "plantao-piercing.html"), "w", encoding="utf-8") as f:
    f.write(PAGINA)
print("ok", os.path.join(RAIZ, "plantao-piercing.html"))
