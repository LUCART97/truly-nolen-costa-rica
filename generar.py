"""Genera el borrador del sitio de Truly Nolen Costa Rica desde ficha/costa-rica.json.

Usa como plantilla de diseño el borrador de Venezuela (plantilla/inicio.html y plantilla/detalle.html):
de ahí salen las hojas de estilo, los scripts y el chat. Todo el contenido sale de la ficha.

Uso:  uv run --python 3.12 python generar.py
"""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FICHA = json.loads((RAIZ / "ficha" / "costa-rica.json").read_text(encoding="utf-8"))
SITIO = RAIZ / "sitio"
ID = FICHA["id"]
BASE = f"/oficinas/{ID}/"
ASSETS = f"{BASE}assets/"
PAIS = FICHA["country"]
WA = f"https://wa.me/{FICHA['whatsappTrulyAI']}"
T = FICHA["textos"]


def leer(nombre):
    return (RAIZ / "plantilla" / nombre).read_text(encoding="utf-8")


def entre(texto, ini, fin):
    a = texto.index(ini)
    b = texto.index(fin, a) + len(fin)
    return texto[a:b]


INICIO_TPL = leer("inicio.html")
DETALLE_TPL = leer("detalle.html")
CSP = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*/>', INICIO_TPL).group(0)
HEAD_INICIO = INICIO_TPL[INICIO_TPL.index('<link rel="stylesheet" href="/machotes/assets/countries.css'):INICIO_TPL.index("</head>")]
HEAD_DETALLE = DETALLE_TPL[DETALLE_TPL.index('<link rel="stylesheet" href="/machotes/assets/countries.css'):DETALLE_TPL.index("</head>")]
# Las páginas de detalle traen estilos propios (cifras, notas) dentro del <body>: se suben al <head>.
HEAD_DETALLE += "".join(re.findall(r"<style>.*?</style>", DETALLE_TPL[DETALLE_TPL.index("</head>"):], flags=re.S))
# Bloque «tabla» de la receta: marco blanco, encabezado oscuro con letra amarilla; en el celular cada fila se apila con su etiqueta.
HEAD_DETALLE += """<style>.detail-tabla .tabla-marco{margin-top:36px;background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.tabla-tn{width:100%;border-collapse:collapse;font-size:16px;line-height:1.5}
.tabla-tn thead th{background:var(--ink);color:var(--yellow);text-align:left;font-size:13px;letter-spacing:.08em;text-transform:uppercase;padding:14px 22px}
.tabla-tn tbody tr+tr>*{border-top:1px solid var(--line)}
.tabla-tn tbody th,.tabla-tn td{padding:18px 22px;text-align:left;vertical-align:top}
.tabla-tn tbody th{width:34%;font-weight:400}.tabla-tn tbody th strong{display:block;font-size:18px;color:var(--ink)}
.tabla-tn tbody th span{display:block;margin-top:4px;color:var(--muted)}.tabla-tn td{color:var(--muted)}
.tabla-tn ul{list-style:none;margin:0;padding:0}.tabla-tn li{position:relative;padding:3px 0 3px 20px}
.tabla-tn li::before{content:"";position:absolute;left:0;top:12px;width:8px;height:8px;border-radius:50%;background:var(--yellow);box-shadow:0 0 0 1px var(--ink)}
@media(max-width:760px){.tabla-tn thead{display:none}.tabla-tn tr,.tabla-tn tbody th,.tabla-tn td{display:block;width:auto}
.tabla-tn tbody th,.tabla-tn td{padding:12px 18px}.tabla-tn tbody tr+tr>th{border-top:1px solid var(--line)}.tabla-tn tbody tr>td,.tabla-tn tbody tr+tr>td{border-top:0;padding-top:0}
.tabla-tn [data-label]::before{content:attr(data-label);display:block;margin-bottom:4px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);font-weight:700}
.tabla-tn tbody th[data-label]::before{color:var(--muted)}
.detail-hero h1 br,.section-heading h2 br{display:none}}</style>"""
BODY_DETALLE = re.search(r"<body[^>]*>", DETALLE_TPL).group(0).replace("venezuela", ID)
BODY_INICIO = f'<body class="country-site jardin" data-machote="{ID}" data-oficina="{ID}">'


def estilos_de(tpl):
    """<link>, <script> y <style> del <head> de una plantilla, más los <style> que trae dentro del <body>."""
    cabeza = tpl[tpl.index('<link rel="stylesheet" href="/machotes/assets/countries.css'):tpl.index("</head>")]
    return cabeza + "".join(re.findall(r"<style>.*?</style>", tpl[tpl.index("</head>"):], flags=re.S))


# El blog usa los estilos del artículo de Venezuela más los que el listado agrega aparte.
HEAD_BLOG = estilos_de(leer("articulo.html"))
HEAD_BLOG += "".join(s for s in re.findall(r"<style>.*?</style>", leer("blog.html"), flags=re.S) if s not in HEAD_BLOG)

# Goteo del blog: solo sale lo que tiene fecha de hoy o anterior, en hora de Costa Rica (UTC-6).
HOY = date.fromisoformat(os.environ["FECHA_HOY"]) if os.environ.get("FECHA_HOY") else (datetime.now(timezone.utc) - timedelta(hours=6)).date()
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
# Artículos con "excluido" (retirados por el dueño) no salen ni cuentan en el goteo; su archivo se conserva.
TODOS_ARTICULOS = sorted((a for a in (json.loads(p.read_text(encoding="utf-8")) for p in (RAIZ / "ficha" / "blog").glob("*.json")) if not a.get("excluido")),
                         key=lambda a: (a["fecha"], a["slug"]), reverse=True)
# Pausa del goteo (decisión del dueño): con blog.pausadoHasta no sale nada con fecha posterior, aunque llegue su día.
PAUSA = date.fromisoformat(FICHA["blog"]["pausadoHasta"]) if FICHA["blog"].get("pausadoHasta") else None
ARTICULOS = [a for a in TODOS_ARTICULOS if date.fromisoformat(a["fecha"]) <= (min(HOY, PAUSA) if PAUSA else HOY)]


def fecha_larga(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def chat():
    bloque = entre(INICIO_TPL, "<!-- immersive:start -->", "<!-- immersive:end -->")
    textos = json.loads(re.search(r'<script id="tia-textos" type="application/json">(.*?)</script>', bloque, re.S).group(1))
    textos.update({
        "saludo": T["chatSaludo"], "campo": T["chatCampo"], "invitaSub": T["chatInvitaSub"],
        "caido": T["chatCaido"], "trabado": T["chatCaido"], "atajos": T["chatAtajos"],
    })
    bloque = re.sub(r'(<script id="tia-textos" type="application/json">).*?(</script>)',
                    lambda m: m.group(1) + json.dumps(textos, ensure_ascii=False) + m.group(2), bloque, flags=re.S)
    bloque = re.sub(r'(<script id="tia-contexto" type="text/plain">).*?(</script>)',
                    lambda m: m.group(1) + escape(FICHA["chatContexto"], quote=False) + m.group(2), bloque, flags=re.S)
    atajos = "".join(f'<button type="button" class="tia-atajo">{escape(a)}</button>' for a in T["chatAtajos"])
    bloque = re.sub(r'<div class="tia-atajos" data-atajos>.*?</div>', f'<div class="tia-atajos" data-atajos>{atajos}</div>', bloque, flags=re.S)
    reemplazos = {
        'data-storage-scope="oficina-venezuela"': f'data-storage-scope="oficina-{ID}"',
        "Escríbele a Truly AI…": T["chatCampo"],
        "Truly AI te responde al instante": T["chatInvitaSub"],
        "<small>Conversa aquí</small>": f"<small>{T['fabSub']}</small>",
        "https://wa.me/15202145675": WA,
    }
    for a, b in reemplazos.items():
        bloque = bloque.replace(a, b)
    return bloque


CHAT = chat()


SOCIAL = f"{FICHA['url']}assets/{FICHA['seo']['imagen']}"


def head(titulo, descripcion, ruta, migas=None, inicio=False, estilos=None, og_tipo="website", extra_ld=()):
    """migas: lista de (nombre, ruta) después de «Inicio»; la última es esta página."""
    url = FICHA["url"] + ruta
    org = {"@context": "https://schema.org", "@type": "Organization", "name": f"Truly Nolen {PAIS}", "url": FICHA["url"],
           "logo": "https://trulyinbound.ai/tn-emblema.png", "image": SOCIAL, "areaServed": {"@type": "Country", "name": PAIS}}
    ld = [org]
    if inicio:
        ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": f"Truly Nolen {PAIS}", "url": FICHA["url"], "inLanguage": "es"})
    ld += list(extra_ld)
    if migas:
        items = [("Inicio", "")] + list(migas)
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": FICHA["url"] + r} for i, (n, r) in enumerate(items, 1)]})
    t, d = escape(titulo), escape(descripcion)
    alt = escape(FICHA["seo"]["imagenAlt"])
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="robots" content="noindex,nofollow"/>{CSP}
<title>{t}</title><meta name="description" content="{d}"/><link rel="canonical" href="{url}"/><link rel="icon" href="/tn-emblema.png"/>
<meta property="og:type" content="{og_tipo}"/><meta property="og:site_name" content="Truly Nolen {PAIS}"/><meta property="og:locale" content="{FICHA['locale']}"/>
<meta property="og:url" content="{url}"/><meta property="og:title" content="{t}"/><meta property="og:description" content="{d}"/>
<meta property="og:image" content="{SOCIAL}"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/><meta property="og:image:alt" content="{alt}"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="{t}"/><meta name="twitter:description" content="{d}"/><meta name="twitter:image" content="{SOCIAL}"/>
{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
{estilos or (HEAD_INICIO if inicio else HEAD_DETALLE)}{R2_CSS}</head>
"""


SERV = FICHA["paginas"]["servicios"]
PLAG = FICHA["paginas"]["plagas"]
# Receta nueva (31-oct-2026): solo las plagas que eligió el dueño; las demás quedan en la ficha, sin página.
_ELEGIDAS = FICHA.get("decisionesReceta2", {}).get("plagas")
if _ELEGIDAS:
    PLAG = [x for x in PLAG if x["slug"] in _ELEGIDAS]
R2 = FICHA.get("receta2", {})
_FP = RAIZ / "docs" / "design" / "oficinas" / ID / "fotos-plagas.json"
FOTOS_PLAGAS = {f["plaga"]: f for f in json.loads(_FP.read_text(encoding="utf-8"))} if _FP.exists() else {}


def foto_plaga(x):
    """Foto real de la plaga (receta: nunca ilustración); si no hay, la imagen de la ficha."""
    f = FOTOS_PLAGAS.get(x["slug"])
    return f["file"].split("/assets/")[-1] if f else x["imagen"]


# Diseño de las oficinas: el CSS del molde oficial (copiado de la página de Venezuela) más dos ajustes propios.
R2_CSS = "<style>" + re.sub(r"/\*.*?\*/", "", leer("diseno-oficina.css"), flags=re.S) + """
.r2-credito{font-size:12px;color:var(--muted);margin:8px 0 0;overflow-wrap:anywhere}
body.country-site[data-oficina] .local-footer .footer-place img{mix-blend-mode:normal}
@media(min-width:901px){.g-plagas-grid[style*="--n:4"]{grid-template-columns:repeat(2,minmax(0,1fr))}.g-plagas-grid[style*="--n:2"]{grid-template-columns:repeat(2,minmax(0,1fr))}
.blog-consejos{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
.g-zonas-lista .g-lista{margin-top:10px}
/* Ojo de diseño (1-nov-2026) */
""" + leer("molde-1nov.css") + """
h1,h2,h3{text-wrap:balance}
@media(min-width:901px){.blog-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.g-zonas-grid{align-items:start}.g-zonas-fig{position:sticky;top:140px}}
@media(max-width:760px){.service-grid[style]{grid-template-columns:1fr!important}}
.service-grid>a.service{display:flex;flex-direction:column}.service-grid>a.service>div{display:flex;flex-direction:column;flex:1}.service-grid>a.service .service-action{margin-top:auto;align-self:flex-start}
.legal-content h2{font-size:clamp(24px,2.4vw,32px)}
@media(min-width:901px){.blog-grid.n2{grid-template-columns:repeat(2,minmax(0,1fr))!important}.blog-grid.n1{grid-template-columns:1fr!important}
.detail-hero h1{font-size:clamp(44px,4.6vw,68px)}}
.blog-consejos .text-link{white-space:normal}
</style>"""


def nav():
    s = "".join(f'<a href="{BASE}servicios/{x["slug"]}/">{escape(x["titulo"])}</a>' for x in SERV)
    p = "".join(f'<a href="{BASE}plagas/{x["slug"]}/">{escape(x["titulo"])}</a>' for x in PLAG)
    return f"""<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site-nav"><a class="brand" href="{BASE}"><img src="/tn-emblema.png" alt=""/><span>Truly Nolen <small data-preview-office>{PAIS}</small></span></a>
<button class="menu-toggle country-menu-toggle" type="button" aria-expanded="false" aria-controls="country-navigation">Menú <span aria-hidden="true">☰</span></button>
<nav id="country-navigation" aria-label="Navegación">
<div class="truly-portals" aria-label="Portales Truly"><a class="my-truly-access" href="https://vip.trulynoleninternational.com/" target="_blank" rel="noopener noreferrer">My Truly</a><a class="inside-truly-access" href="https://www.trulynoleninternational.com/TrulyInside/index.asp?lng=1" target="_blank" rel="noopener noreferrer">Inside Truly</a></div>
<details class="nav-menu"><summary>Servicios <span aria-hidden="true">⌄</span></summary><div class="country-dropdown"><a href="{BASE}#servicios">Ver servicios</a>{s}<a href="{BASE}#metodo">Cómo trabajamos</a></div></details>
<details class="nav-menu"><summary>Plagas <span aria-hidden="true">⌄</span></summary><div class="country-dropdown"><a href="{BASE}#plagas">Ver guía de plagas</a>{p}<a href="{BASE}#consulta">No sé qué plaga es</a></div></details>
<a href="{BASE}#cobertura">Cobertura</a><a href="{BASE}#nosotros">Nosotros</a>{f'<a href="{BASE}blog/">Blog</a>' if ARTICULOS else ""}<a href="{BASE}#contacto">Contacto</a><a class="mobile-contact" href="{BASE}#preguntas">Preguntas frecuentes</a>
</nav><a class="button" href="{BASE}#contacto">Solicitar atención</a></header>
"""


def footer():
    f = {**FICHA["footer"], **({"file": R2["footer"]["file"].split("/assets/")[-1], "alt": R2["footer"]["alt"]} if R2.get("footer") else {})}
    s = "".join(f'<a href="{BASE}servicios/{x["slug"]}/">{escape(x["titulo"])}</a>' for x in SERV)
    p = "".join(f'<a href="{BASE}plagas/{x["slug"]}/">{escape(x["titulo"])}</a>' for x in PLAG)
    return f"""<footer class="country-footer local-footer" aria-label="Pie de página">
<div class="footer-intro"><a class="brand" href="{BASE}"><img src="/tn-emblema.png" alt=""/><span>Truly Nolen <small data-preview-office>{PAIS}</small></span></a><p>{T['footerLema']}</p><a class="text-link" href="{BASE}#contacto">Conversemos</a></div>
<div class="footer-columns">
<details class="pie-col" open><summary>Servicios</summary><nav aria-label="Servicios del pie">{s}<a href="{BASE}#consulta">Otras consultas</a><a href="{BASE}#metodo">Cómo trabajamos</a></nav></details>
<details class="pie-col" open><summary>Guía de plagas</summary><nav aria-label="Guía de plagas del pie">{p}<a href="{BASE}#consulta">Consultar por otra plaga</a></nav></details>
<details class="pie-col" open><summary>Truly Nolen {PAIS}</summary><nav aria-label="Truly Nolen"><a href="{BASE}#nosotros">Nuestra forma de cuidar</a><a href="{BASE}#metodo">Cómo trabajamos</a><a href="{BASE}#cobertura">Consultar cobertura</a><a href="{BASE}#preguntas">Preguntas frecuentes</a>{f'<a href="{BASE}blog/">Blog</a>' if ARTICULOS else ""}<a href="{BASE}#contacto">Solicitar atención</a></nav></details>
<div class="footer-office"><h2>Hablemos</h2><p data-preview-office>{PAIS}</p><a href="#contacto" data-abrir-chat>Escribir a Truly AI</a></div>
</div>
<figure class="footer-place"><img src="{ASSETS}{f['file']}" alt="{escape(f['alt'])}" width="1414" height="558" loading="lazy" decoding="async"/><figcaption>{escape(f['caption'])}</figcaption></figure>
<div class="footer-legal"><p>© Truly Nolen · {PAIS}</p><nav aria-label="Información legal"><a href="{BASE}privacidad/">Privacidad</a><a href="{BASE}terminos/">Términos de uso</a><a href="{BASE}accesibilidad/">Accesibilidad</a></nav></div>
</footer>
"""


def starters(lista):
    return "".join(f'<a href="#contacto" data-abrir-chat data-chat-prompt="{escape(pr)}">{escape(lb)}<span aria-hidden="true">→</span></a>' for lb, pr in lista)


def consulta(eyebrow, titulo, texto, lista, ident=""):
    return f"""<section {ident}class="section local-consult"><div><p class="eyebrow">{eyebrow}</p><h2>{titulo}</h2><p>{escape(texto)}</p></div>
<div class="marco-entry"><div class="marco-entry-heading"><img src="/oficinas/assets/truly-carrito-asistente.svg" alt="" width="72" height="48" loading="lazy"/><div><h3>Truly AI</h3><p>Asistente virtual · {PAIS}</p></div></div>
<p class="marco-entry-label">¿Por dónde empezamos?</p><div class="marco-starts">{starters(lista)}</div><p class="marco-entry-note">{escape(T['nota'])}</p></div></section>
"""


def metodo(eyebrow):
    items = "".join(f"<article><span>{i:02d}</span><h3>{escape(h)}</h3><p>{escape(p)}</p></article>" for i, (h, p) in enumerate(FICHA["metodo"], 1))
    return f'<section id="metodo" class="section method"><div class="section-heading"><p class="eyebrow">{eyebrow}</p><h2>Cuatro pasos, de la consulta al seguimiento.</h2></div><div class="method-grid">{items}</div></section>\n'


def faq(eyebrow, titulo, preguntas, ident='id="preguntas" '):
    items = "".join(f'<details><summary>{escape(q)}<span aria-hidden="true">+</span></summary><p>{escape(a)}</p></details>' for q, a in preguntas)
    return f'<section {ident}class="section faq"><div><p class="eyebrow">{eyebrow}</p><h2>{titulo}</h2></div><div>{items}</div></section>\n'


def contacto(lista=None):
    """Cierre único de cada página (molde): datos y canales, línea de cobertura y tarjeta de Truly AI."""
    I = FICHA["inicio"]
    lista = lista or I["consultaStarters"]
    return f"""<section id="contacto" class="section local-consult g-cierre"><div><span id="consulta"></span><span id="cobertura"></span><p class="eyebrow">Truly Nolen · {PAIS}</p><h2>{escape(T['contactoTitulo'])}</h2><p>{escape(T['contactoTexto'])}</p>
{zona_form()}
<div class="contact-channels" style="display:flex;flex-wrap:wrap;align-items:center;gap:16px 28px;align-self:end"><a class="button" href="#contacto" data-abrir-chat>Escribir en el chat</a><a class="text-link" href="{WA}" target="_blank" rel="noopener noreferrer">Escribir por WhatsApp</a></div></div>
<div class="marco-entry"><div class="marco-entry-heading"><img src="/oficinas/assets/truly-carrito-asistente.svg" alt="" width="72" height="48" loading="lazy"/><div><h3>Truly AI</h3><p>Asistente virtual · {PAIS}</p></div></div>
<p class="marco-entry-label">Cuéntele a Truly AI qué está viendo</p><div class="marco-starts">{starters(lista)}</div><p class="marco-entry-note">{escape(T['nota'])}</p></div></section>
"""


PROVINCIAS = ["San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas", "Limón"]   # las 7 provincias (INEC)


def zona_form():
    """Filtro de cobertura del molde (zona.js): arma el primer mensaje y abre Truly AI; no envía nada solo."""
    ops = "".join(f"<option>{p}</option>" for p in PROVINCIAS)
    return (f'<form class="g-zona" data-zona data-n1="Provincia" data-n2="Cantón"><p class="g-zona-txt">{escape(FICHA["inicio"]["coberturaTexto"])}</p>'
            f'<div class="g-zona-campos"><label>Provincia<select name="n1" required><option value="">Elegir</option>{ops}</select></label>'
            '<label>Cantón<input name="n2" autocomplete="address-level2"/></label>'
            '<label>Código postal<input name="cp" placeholder="Opcional" inputmode="numeric" maxlength="5" pattern="[0-9]{5}" autocomplete="postal-code"/></label></div>'
            '<fieldset class="g-zona-espacio"><legend>Espacio</legend><label class="g-zona-op"><input type="radio" name="espacio" value="Hogar" checked/>Hogar</label>'
            '<label class="g-zona-op"><input type="radio" name="espacio" value="Comercio"/>Comercio</label><label class="g-zona-op"><input type="radio" name="espacio" value="Industria"/>Industria</label></fieldset>'
            f'<div class="g-zona-acciones"><button type="submit" class="button">Consultar cobertura</button><a class="text-link" href="#contacto" data-abrir-chat data-chat-prompt="{escape(FICHA["inicio"]["coberturaPrompt"])}">Prefiero escribirlo</a></div>'
            '<button type="button" hidden data-abrir-chat data-zona-enviar></button></form>')


def tarjeta_servicio(i, x):
    return f'<a class="service" href="{BASE}servicios/{x["slug"]}/"><img src="{ASSETS}{x["imagen"]}" alt="" loading="lazy"/><div><span>{i:02d}</span><h3>{escape(x["titulo"])}</h3><p>{escape(x["resumen"])}</p><span class="service-action">Ver servicio</span></div></a>'


def g_cab(eyebrow, titulo, texto=""):
    intro = f'<p class="g-intro">{escape(texto)}</p>' if texto else ""
    return f'<header class="g-cab"><p class="g-ey">{escape(eyebrow)}</p><h2>{titulo}</h2>{intro}</header>'


def g_tabla(eyebrow, titulo, columnas, filas, texto="", nota="", tema="Tema"):
    """Tabla del molde: número · tema · columnas (texto o lista de puntos)."""
    cab = "".join(f'<th scope="col">{escape(c)}</th>' for c in [tema, *columnas])
    cuerpo = ""
    for i, (nombre, *celdas) in enumerate(filas, 1):
        tds = "".join(f'<td data-col="{escape(c)}">' + (f'<ul class="g-lista">{"".join(f"<li>{escape(x)}</li>" for x in v)}</ul>' if isinstance(v, list) else escape(v)) + "</td>"
                      for c, v in zip(columnas, celdas))
        cuerpo += f'<tr><td class="g-t-n">{i:02d}</td><th scope="row">{escape(re.sub(r"^\d+\s*·\s*", "", nombre))}</th>{tds}</tr>'
    nota = nota_html(nota)
    return (f'<section class="section g g-bloque">{g_cab(eyebrow, titulo, texto)}<div class="g-tabla-marco"><table class="g-tabla"><thead><tr>'
            f'<th scope="col" aria-label="Número"></th>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></div>{nota}</section>\n')


def g_plagas(eyebrow, titulo, texto, lista, textos=None, nota=""):
    textos = textos or {}
    arts = ""
    for x in lista:
        url = f"{BASE}plagas/{x['slug']}/"
        arts += (f'<article><a class="g-pl-fig" href="{url}"><img src="{ASSETS}{foto_plaga(x)}" alt="" loading="lazy"/></a><h3>{escape(x["titulo"])}</h3>'
                 f'<p class="g-pl-sub">{escape(x["eyebrow"])}</p><p>{escape(textos.get(x["slug"]) or x.get("resumenCorto") or primera_frase(x["intro"]))}</p>'
                 f'<a class="g-mas" href="{url}">Ver la guía<span aria-hidden="true">→</span></a></article>')
    nota = nota_html(nota)
    return f'<section id="plagas" class="section g g-plagas">{g_cab(eyebrow, titulo, texto)}<div class="g-plagas-grid" style="--n:{len(lista)}">{arts}</div>{nota}</section>\n'


def nota_html(n):
    if not n:
        return ""
    m = re.match(r"^([^:.]{3,60}):\s+(.)(.*)$", n, flags=re.S)
    if m:
        return f'<p class="g-nota"><strong>{escape(m.group(1))}.</strong> {escape(m.group(2).upper() + m.group(3))}</p>'
    return f'<p class="g-nota">{escape(n)}</p>'


def primera_frase(texto):
    texto = re.sub("<[^>]+>", " ", texto).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", texto)
    return m.group(1) if m else texto


def g_zonas(detalle=None):
    """detalle: filas de la tabla de zonas de Hogares ([nombre, subtítulo], [puntos]); si viene, la casa lleva el detalle."""
    I = FICHA["inicio"]
    casa_img = R2["casaZonas"]["file"].split("/assets/")[-1] if R2.get("casaZonas") else FICHA["fotos"]["casa"]["file"]
    casa_alt = R2["casaZonas"]["alt"] if R2.get("casaZonas") else FICHA["fotos"]["casa"]["alt"]
    colores = ["g-z-rojo", "g-z-amarillo", "g-z-verde"]
    if detalle:
        zonas = "".join(f'<li class="{c}"><h3>{escape(re.sub(r"^\d+\s*·\s*", "", f[0][0]))}</h3><p>{escape(f[0][1])}</p><ul class="g-lista">{"".join(f"<li>{escape(x)}</li>" for x in f[1])}</ul></li>'
                        for c, f in zip(colores, detalle))
    else:
        zonas = "".join(f'<li class="{c}"><h3>{escape(a)}</h3><p>{escape(b)}</p></li>' for c, (a, b) in zip(colores, I["casaZonas"]))
    return (f'<section class="section g g-zonas"><div class="g-zonas-grid{" g-zonas-detalle" if detalle else ""}"><figure class="g-zonas-fig"><img src="{ASSETS}{casa_img}" alt="{escape(casa_alt)}" loading="lazy"/></figure>'
            f'<div>{g_cab("Tres zonas para revisar", escape(I["casaTitulo"]), I["casaTexto"])}<ul class="g-zonas-lista">{zonas}</ul>'
            f'<a class="g-link" href="{BASE}servicios/hogares/">{escape(I["casaLink"])}<span aria-hidden="true">→</span></a></div></div></section>\n')


def bloque(b):
    tipo = b["tipo"]
    if tipo == "tarjetas" and b["eyebrow"].startswith("Qué puede esperar"):
        arts = "".join(f'<article><span class="g-n">{i:02d}</span><h3>{escape(it["h"])}</h3><p>{escape(it["p"])}</p></article>' for i, it in enumerate(b["items"], 1))
        nota = f'<p class="g-nota">{escape(b["nota"])}</p>' if b.get("nota") else ""
        return f'<section class="section g g-esperar">{g_cab(b["eyebrow"], b["titulo"], b.get("texto", ""))}<div class="g-cols g-cols-3">{arts}</div>{nota}</section>\n'
    por_titulo = {x["titulo"]: x for x in PLAG}
    if tipo == "tarjetas" and sum(it["h"] in por_titulo for it in b["items"]) >= 2:
        # tarjetas que hablan de plagas con página propia: van como tarjetas con foto, con su texto
        lista = [por_titulo[it["h"]] for it in b["items"] if it["h"] in por_titulo]
        textos = {por_titulo[it["h"]]["slug"]: it["p"] for it in b["items"] if it["h"] in por_titulo}
        resto = " ".join(f'{it["h"]}: {it["p"]}' for it in b["items"] if it["h"] not in por_titulo)
        return g_plagas(b["eyebrow"], b["titulo"], b.get("texto", ""), lista, textos, resto).replace('id="plagas" ', 'data-plagas-propias ')
    if tipo == "tarjetas":
        filas = [[it["h"], it["p"], it["checks"]] if it.get("checks") else [it["h"], it["p"]] for it in b["items"]]
        columnas = ["Qué significa", "Qué revisamos"] if any(it.get("checks") for it in b["items"]) else ["Qué significa"]
        return g_tabla(b["eyebrow"], b["titulo"], columnas, filas, b.get("texto", ""), b.get("nota", ""))
    if tipo == "tabla":
        cols = b["columnas"]
        if len(cols) == 2 and all(isinstance(f[0], list) and isinstance(f[1], list) for f in b["filas"]):
            # listas de puntos: [título, subtítulo] + puntos → tema · qué significa · qué revisamos
            filas = [[f[0][0], f[0][1], f[1]] for f in b["filas"]]
            return g_tabla(b["eyebrow"], b["titulo"], ["Detalle", cols[1]], filas, b.get("texto", ""), b.get("nota", ""), tema=cols[0])
        filas = [[f[0][0] if isinstance(f[0], list) else f[0], *f[1:]] for f in b["filas"]]
        return g_tabla(b["eyebrow"], b["titulo"], cols[1:], filas, b.get("texto", ""), b.get("nota", ""))
    if tipo == "cifras":
        arts = "".join(f'<article><b>{escape(it["valor"])}</b><p>{escape(it["texto"])}</p><small>{escape(it["fuente"])}</small></article>' for it in b["items"])
        return f'<section class="section g g-dato">{g_cab(b["eyebrow"], b["titulo"])}<div class="g-dato-fila">{arts}</div></section>\n'
    if tipo == "sectores":
        return ""   # lo arma sectores.py con el diseño de globaltni (receta 6c)
    if tipo == "consulta":
        return ""   # un solo cierre por página (receta): sus atajos van en la tarjeta de Truly AI del cierre
    if tipo == "relacionadas":
        if b["lista"] == "plagas":
            return g_plagas(b["eyebrow"], b["titulo"], "", [x for x in PLAG if x["slug"] in b["slugs"]]).replace('id="plagas" ', "")
        elegidos = [x for x in SERV if x["slug"] in b["slugs"]]
        items = "".join(tarjeta_servicio(i, x) for i, x in enumerate(elegidos, 1))
        cols = f' style="grid-template-columns:repeat({len(elegidos)},minmax(0,1fr))"' if len(elegidos) < 3 else ""
        return f'<section class="section services"><div class="section-heading"><p class="eyebrow">{escape(b["eyebrow"])}</p><h2>{b["titulo"]}</h2></div><div class="service-grid"{cols}>{items}</div></section>\n'
    raise ValueError(f"tipo de bloque desconocido: {tipo}")


def fuentes(lista):
    items = "".join(f'<li><a href="{escape(u)}" target="_blank" rel="noopener noreferrer">{escape(t)}</a></li>' for t, u in lista)
    return f'<section class="section detail-sources"><div><p class="eyebrow">Fuentes</p><h2>De dónde sale esta información</h2><p class="nota" style="margin-top:16px">{escape(T["fuentesNota"])}</p></div><ol>{items}</ol></section>\n'


def imagen_hero(x, tipo):
    if tipo == "plaga" and x["slug"] in FOTOS_PLAGAS:
        f = FOTOS_PLAGAS[x["slug"]]
        return f'<figure style="margin:0"><img src="{ASSETS}{foto_plaga(x)}" alt="{escape(f["alt"])}"/></figure>'
    return f'<img src="{ASSETS}{x["imagen"]}" alt="{escape(x["titulo"])}"/>'


def pagina_detalle(x, ruta, tipo):
    descripcion = x.get("descripcion") or re.sub("<[^>]+>", " ", x["intro"])
    html = head(f'{x["titulo"]} · Truly Nolen {PAIS}', descripcion, ruta, migas=[(x["titulo"], ruta)])
    html += BODY_DETALLE + nav() + '<main id="contenido">'
    html += f"""<section class="section detail-hero"><a class="text-link" href="{BASE}">← Volver al inicio</a><div class="story"><div>
<p class="eyebrow">{escape(x['eyebrow'])} · {PAIS}</p><h1>{x['lema']}</h1><p>{escape(x['intro'])}</p><a class="button" href="#contacto">Conversemos</a></div>
{imagen_hero(x, tipo)}</div></section>
"""
    bloques = [bloque(b) for b in x["bloques"]]
    if any("data-plagas-propias" in h for h in bloques):
        bloques = [h for h, b in zip(bloques, x["bloques"]) if not (b["tipo"] == "relacionadas" and b["lista"] == "plagas")]
    if tipo == "servicio" and x["slug"] == "hogares":
        k = next((i for i, b in enumerate(x["bloques"]) if b["tipo"] == "tabla" and "zonas" in b["eyebrow"].lower()), None)
        if k is not None:
            bloques[k] = g_zonas(x["bloques"][k]["filas"])
        else:
            bloques.insert(1, g_zonas())
    html += "".join(bloques)
    html += faq("Preguntas frecuentes", "Lo que más nos preguntan.", x.get("preguntas") or FICHA["faq"], ident="")
    atajos = next((b["starters"] for b in x["bloques"] if b["tipo"] == "consulta"), None)
    html += fuentes(x["fuentes"]) + contacto(atajos) + "</main>" + footer() + CHAT + "</body></html>\n"
    return html


def pagina_legal(clave, titulo):
    descripcion = FICHA.get("legalesDescripcion", {}).get(clave, FICHA["legales"][clave])
    html = head(f"{titulo} · Truly Nolen {PAIS}", descripcion, f"{clave}/", migas=[(titulo, f"{clave}/")])
    html += BODY_DETALLE + nav()
    creditos = ""
    if clave == "terminos" and FICHA.get("creditosFotos"):
        # Las fotos con licencia CC BY / CC BY-SA exigen nombrar al autor y la licencia.
        items = "".join(f'<li><a href="{escape(u)}" target="_blank" rel="noopener noreferrer">{escape(t)}</a></li>' for t, u in FICHA["creditosFotos"])
        creditos = f'<h2 style="margin-top:40px">Créditos de las fotos</h2><p>Algunas fotos de este sitio se usan con licencia libre:</p><ul style="overflow-wrap:anywhere">{items}</ul>'
    html += f'<main id="contenido"><section class="section legal-content"><p class="eyebrow">Truly Nolen · {PAIS}</p><h1>{titulo}</h1><p>{escape(FICHA["legales"][clave])}</p>{creditos}<a class="button" href="{BASE}">← Volver al sitio</a></section>'
    # Con su sección de contacto, «Escribir a Truly AI» del pie abre el chat aquí mismo en vez de llevar al inicio
    return html + contacto() + "</main>" + footer() + CHAT + "</body></html>\n"


def tarjeta_articulo(a, destacada=False):
    url = f"{BASE}blog/{a['slug']}/"
    return f"""<article class="blog-card{' blog-featured' if destacada else ''}"><a href="{url}" tabindex="-1" aria-hidden="true"><img src="{ASSETS}{a['cover']}" alt="" loading="lazy"/></a>
<div><p class="eyebrow">{escape(a['tema'])}</p><h2><a href="{url}">{escape(a['title'])}</a></h2><p>{escape(a['excerpt'])}</p><a class="text-link" href="{url}">Leer el artículo →</a></div></article>"""


def pagina_blog():
    # El primero va ancho; los que sobran en una última fila incompleta de tres también van anchos (sin huecos al lado).
    sobran = (len(ARTICULOS) - 1) % 3
    anchas = {0} | set(range(len(ARTICULOS) - sobran, len(ARTICULOS)))
    html = head(f"Blog de control de plagas · Truly Nolen {PAIS}", f"Guías sobre las plagas de {PAIS}: alacranes, chinches de cama, zompopas, ratas y más, con cada dato respaldado por su fuente.",
                "blog/", migas=[("Blog", "blog/")], estilos=HEAD_BLOG)
    html += BODY_INICIO + nav() + '<main id="contenido">'
    html += f"""<section class="section blog-head"><a class="text-link" href="{BASE}">← Volver al inicio</a><p class="eyebrow">Blog · {PAIS}</p><h1>Blog de control de plagas</h1>
<p>Guías sobre las plagas de aquí, con cada dato respaldado por su fuente.</p></section>
<section class="section blog-lista"><div class="blog-grid">{"".join(tarjeta_articulo(a, i in anchas) for i, a in enumerate(ARTICULOS))}</div></section>
"""
    # Consejos de prevención: una tarjeta por plaga, con su dibujo, su fuente y el enlace a su guía
    plagas = {p["slug"]: p for p in PLAG}
    consejos = ""
    for c in FICHA["blog"].get("consejos", []):
        if c["plaga"] not in plagas:
            continue
        p = plagas[c["plaga"]]
        url = f"{BASE}plagas/{p['slug']}/"
        consejos += f"""<article class="blog-card"><a href="{url}" tabindex="-1" aria-hidden="true"><img src="{ASSETS}{foto_plaga(p)}" alt="" loading="lazy"/></a>
<div><p class="eyebrow">{escape(p['titulo'])}</p><h2><a href="{url}">{escape(c['titulo'])}</a></h2><p>{escape(c['texto'])}</p><p style="font-size:13px;color:var(--muted)">Fuente: {escape(c['fuente'])}</p><a class="text-link" href="{url}">Ver la guía de {escape(p['titulo'].lower())}&nbsp;→</a></div></article>"""
    if consejos:
        html += f"""<section class="section blog-lista"><div class="section-heading"><p class="eyebrow">Prevención · {PAIS}</p><h2>Cómo prevenir<br/>cada plaga.</h2>
<p>Un consejo concreto por plaga, con su fuente, para empezar hoy mismo en su casa o su negocio.</p></div><div class="blog-grid blog-consejos">{consejos}</div></section>
"""
    return html + contacto(FICHA["blog"].get("consulta")) + "</main>" + footer() + CHAT + "</body></html>\n"


def pagina_articulo(a):
    ruta = f"blog/{a['slug']}/"
    portada = f"{FICHA['url']}assets/{a['cover']}"
    posting = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["meta_description"],
               "datePublished": a["fecha"], "inLanguage": "es", "image": portada,
               "author": {"@type": "Organization", "name": f"Truly Nolen {PAIS}"}, "publisher": {"@type": "Organization", "name": "Truly Nolen"}}
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a["faqs"]]}
    html = head(a['title'] if len(a['title']) > 48 else f"{a['title']} · Truly Nolen {PAIS}", a["meta_description"], ruta, migas=[("Blog", "blog/"), (a["title"], ruta)],
                estilos=HEAD_BLOG, og_tipo="article", extra_ld=[posting, faqpage])
    credito = ""
    if a.get("credito"):
        texto, licencia = a["credito"], ""
        if a.get("licencia") and texto.endswith(a["licencia"][0]):   # la licencia CC BY exige enlazarla
            texto = texto[: -len(a["licencia"][0])].rstrip()
            licencia = f' <a href="{escape(a["licencia"][1])}" target="_blank" rel="noopener noreferrer license">{escape(a["licencia"][0])}</a>'
        credito = f'<p class="blog-meta"><a href="{escape(a["creditoUrl"])}" target="_blank" rel="noopener noreferrer">{escape(texto)}</a>{licencia}</p>'
    html += BODY_INICIO + nav() + '<main id="contenido">'
    html += f"""<article class="section blog-articulo"><nav class="blog-migas" aria-label="Ruta"><a href="{BASE}">Inicio</a> · <a href="{BASE}blog/">Blog</a> · <span>{escape(a['tema'])}</span></nav>
<p class="eyebrow">{escape(a['tema'])}</p><h1>{escape(a['title'])}</h1><p class="blog-entrada">{escape(a['excerpt'])}</p>
<p class="blog-meta">Truly Nolen {PAIS} · {fecha_larga(a['fecha'])} · {a['minutos']} min de lectura</p>
<img class="blog-portada" src="{ASSETS}{a['cover']}" alt="{escape(a['og_alt_text'])}"/>{credito}
<div class="blog-cuerpo">{a['content_html']}</div></article>
"""
    html += faq(escape(a["tema"]), "Preguntas frecuentes", a["faqs"], ident="")
    html += fuentes(a["fuentes"])
    otros = [x for x in ARTICULOS if x["slug"] != a["slug"]][:3]
    if otros:
        html += f'<section class="section"><div class="section-heading"><p class="eyebrow">Blog</p><h2>Artículos relacionados</h2></div><div class="blog-grid n{len(otros)}">{"".join(tarjeta_articulo(x, len(otros) == 1) for x in otros)}</div></section>\n'
    return html + contacto() + "</main>" + footer() + CHAT + "</body></html>\n"


def carrito():
    """Carrito de Truly fijo en la esquina superior izquierda de la portada, rodando en su sitio:
    ruedas que giran (tira de 4 cuadros), motor que vibra, baches suaves, líneas de velocidad y sombra."""
    c = FICHA.get("carrito")
    if not c:
        return ""
    lineas = "".join(f'<i style="top:{t}%;width:{w}%;animation-delay:{d}s"></i>' for t, w, d in [(30, 70, 0), (52, 95, .22), (70, 60, .45), (86, 80, .12)])
    return f"""<style>
.hero-carrito{{position:absolute;z-index:3;top:{c['arriba']};left:{c['izquierda']};width:{c['ancho']};aspect-ratio:656/469;pointer-events:none;
animation:hc-llega 1.9s cubic-bezier(.15,.75,.3,1) both,hc-bache 1.7s ease-in-out 1.9s infinite}}
@media(min-width:761px){{body.country-site #inicio .hero-text{{position:relative;top:{c['bajarTexto']}}}}}
.hero-carrito .hc-carro{{position:absolute;inset:0;background:url({ASSETS}{c['tira']}) 0 0/400% 100% no-repeat;filter:drop-shadow(0 6px 6px rgba(0,0,0,.35));
animation:hc-ruedas .2s steps(4) infinite,hc-motor .09s ease-in-out infinite alternate}}
.hero-carrito .hc-sombra{{position:absolute;left:2%;right:4%;bottom:-5%;height:16%;background:radial-gradient(ellipse at center,rgba(0,0,0,.55),rgba(0,0,0,0) 70%);animation:hc-sombra 1.7s ease-in-out infinite}}
.hero-carrito .hc-lineas{{position:absolute;right:88%;top:22%;width:42%;height:62%;overflow:hidden;transform:rotate(-7deg)}}
.hero-carrito .hc-lineas i{{position:absolute;right:0;height:2px;border-radius:2px;background:linear-gradient(to left,rgba(255,255,255,.75),rgba(255,255,255,0));animation:hc-linea .7s linear infinite}}
@keyframes hc-llega{{0%{{transform:translateX(-135%);opacity:0}}12%{{opacity:1}}72%{{transform:translateX(5%) rotate(1.4deg)}}84%{{transform:translateX(-1.5%) rotate(-.6deg) translateY(-2px)}}93%{{transform:translateX(.5%) rotate(.2deg)}}100%{{transform:none;opacity:1}}}}
@keyframes hc-ruedas{{to{{background-position-x:133.333%}}}}
@keyframes hc-motor{{from{{transform:translateY(0)}}to{{transform:translateY(-.8px)}}}}
@keyframes hc-bache{{0%,100%{{transform:translateY(0) rotate(0)}}45%{{transform:translateY(-2px) rotate(-.5deg)}}60%{{transform:translateY(.5px) rotate(.2deg)}}}}
@keyframes hc-sombra{{0%,100%{{transform:scaleX(1);opacity:1}}45%{{transform:scaleX(.95);opacity:.85}}}}
@keyframes hc-linea{{from{{transform:translateX(30%);opacity:0}}25%{{opacity:1}}to{{transform:translateX(-120%);opacity:0}}}}
@media(max-width:760px){{.hero-carrito{{width:{c['anchoCelular']};top:{c['arribaCelular']};left:{c['izquierdaCelular']}}}}}
@media(prefers-reduced-motion:reduce){{.hero-carrito,.hero-carrito *{{animation:none!important}}.hero-carrito .hc-lineas{{display:none}}}}
</style><div class="hero-carrito" role="img" aria-label="{escape(c['alt'])}" data-pared="{c['pared']}" data-maximo="{c['maximo']}" data-minimo="{c['minimo']}" data-margen="{c['margen']}"><span class="hc-lineas" aria-hidden="true">{lineas}</span><span class="hc-sombra" aria-hidden="true"></span><span class="hc-carro" aria-hidden="true"></span></div><script defer src="{ASSETS}carrito.js"></script>"""


def pagina_inicio():
    I = FICHA["inicio"]
    pel = FICHA["pelicula"]
    html = head(FICHA["seo"]["titulo"], FICHA["seo"]["descripcion"], "", inicio=True).replace("</head>", '<script defer src="/oficinas/assets/escenas.js"></script></head>')
    html += f'<body class="country-site jardin" data-machote="{ID}" data-oficina="{ID}">' + nav() + '<main id="contenido">'
    # 1 · película (carro y mundo, escenas.js)
    html += f"""<section class="cinema" id="inicio"><div class="film" style="--poster:url({ASSETS}{pel['poster']}?v={version(ASSETS + pel['poster'])})"><picture><source media="(max-width:760px)" srcset="{ASSETS}{pel['poster']}"/><img src="{ASSETS}{pel['poster']}" alt=""/></picture>{f'<video muted loop playsinline preload="none" aria-hidden="true" data-src-movil="{ASSETS}costa-rica-movil.mp4" data-src="{ASSETS}{pel["video"]}"></video><script src="/oficinas/assets/video-movil.js"></script>' if pel.get("video") else ""}</div>
<div class="hero-text"><p class="eyebrow">Truly Nolen · <span data-preview-office>{PAIS}</span></p><h1>{escape(I['h1'])}</h1><p>{escape(I['intro'])}</p><a class="button" href="#contacto">{escape(I['cta'])}</a></div><a class="discover" href="#servicios">{escape(I['descubre'])}</a></section>
"""
    # 2 · cifras de la marca (globaltni.com/es)
    cif = "".join(f'<div><b>{escape(a)}</b> <span>{escape(b)}</span><small>{escape(c)}</small></div>' for a, b, c in I["cifrasMarca"])
    html += f'<section class="g-cifras" aria-label="Truly Nolen en el mundo"><div class="g-cifras-in">{cif}<div class="g-cifra-carro"><img src="/oficinas/assets/truly-carrito-asistente.svg" alt=""/><span>una marca reconocible<small>nuestro carro emblemático</small></span></div></div></section>\n'
    # 3 · el programa: los 3 servicios
    iconos = ['<path d="M4 11.5 12 5l8 6.5M6.5 10v9h11v-9M10 19v-5h4v5"/>',
              '<path d="M4 9h16l-1.5-4h-13zM5 9v10h14V9M9 19v-5h6v5M4 9a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0"/>',
              '<path d="M3 20V10l5 3V10l5 3V10l5 3V5h3v15zM7 17h2M12 17h2M17 17h2"/>']
    prog = "".join(f'<a class="g-prog{" g-prog-1" if i == 0 else ""}" href="{BASE}servicios/{x["slug"]}/"><span class="g-prog-ico"><svg viewBox="0 0 24 24" aria-hidden="true">{iconos[i]}</svg></span>'
                   f'<h3>{escape(x["titulo"])}</h3><p>{escape(x["resumen"])}</p><span class="g-flecha" aria-hidden="true">↓</span></a>' for i, x in enumerate(SERV[:3]))
    html += f'<section id="servicios" class="section g g-programa">{g_cab(f"Truly Nolen · {PAIS}", escape(I["programaTitulo"]), I["programaTexto"])}<div class="g-prog-fila">{prog}</div></section>\n'
    # 4 · las 3 zonas de la casa
    html += g_zonas()
    # 5 · comercio e industria
    com = next(x for x in SERV if x["slug"] == "comercios"); ind = next(x for x in SERV if x["slug"] == "industria")
    esperar = next(b for b in com["bloques"] if b["tipo"] == "tarjetas" and b["eyebrow"].startswith("Qué puede esperar"))
    sect = "".join(f'<a class="g-sector" href="{BASE}servicios/comercios/"><span><h3>{escape(it["h"])}</h3><p>{escape(it["p"])}</p></span><span aria-hidden="true">→</span></a>' for it in esperar["items"])
    sect += f'<a class="g-sector" href="{BASE}servicios/industria/"><span><h3>{escape(ind["titulo"])}</h3><p>{escape(ind["intro"])}</p></span><span aria-hidden="true">→</span></a>'
    F = FICHA["fotos"]["operacion"]
    html += (f'<section class="section g g-comercial">{g_cab("Comercio e industria", escape(I["comercialTitulo"]), com["intro"])}<div class="g-com-grid">'
             f'<a class="g-com-foto" href="{BASE}servicios/comercios/"><img src="{ASSETS}{F["file"]}" alt="" loading="lazy"/><span><b>{escape(I["comercialFrase"])}</b><em>{escape(I["operacionBotones"][0])} →</em></span></a>'
             f'<div class="g-sectores">{sect}</div></div></section>\n')
    # 6 · cómo trabajamos
    pasos = "".join(f'<article><span class="g-n">{i:02d}</span><h3>{escape(h)}</h3><p>{escape(t)}</p></article>' for i, (h, t) in enumerate(FICHA["metodo"], 1))
    html += f'<section id="metodo" class="section g g-metodo"><span id="nosotros"></span>{g_cab("Cómo trabajamos", "Cuatro pasos, de la consulta<br/>al seguimiento.")}<div class="g-cols g-cols-4">{pasos}</div></section>\n'
    # 7 · guía de plagas
    html += g_plagas("Guía de plagas", "Reconozca la plaga.<br/>Entienda sus hábitos.", I["plagasTexto"], PLAG)
    # 8 · blog y preguntas
    faqs = "".join(f'<details{" open" if i == 0 else ""}><summary>{escape(q)}<span aria-hidden="true">+</span></summary><p>{escape(a)}</p></details>' for i, (q, a) in enumerate(FICHA["faq"]))
    blog = ""
    if ARTICULOS:
        a = ARTICULOS[0]
        url = f"{BASE}blog/{a['slug']}/"
        blog = (f'<article class="g-blog"><div class="g-blog-top"><img src="{ASSETS}{a["cover"]}" alt="" loading="lazy"/><p class="g-ey">Del blog · {fecha_larga(a["fecha"])}</p></div>'
                f'<h3><a href="{url}">{escape(a["title"])}</a></h3><p>{escape(a["excerpt"])}</p><a class="g-link" href="{url}">Leer el artículo<span aria-hidden="true">→</span></a>'
                f'<a class="g-link g-link-2" href="{BASE}blog/">Ver todo el blog<span aria-hidden="true">→</span></a></article>')
    html += (f'<section class="section g g-ayuda">{g_cab("Blog y preguntas", "Prevención y respuestas<br/>para usted.", I["ayudaTexto"])}<div class="g-ayuda-grid">{blog}'
             f'<div class="g-faq" id="preguntas"><h3>Lo que más nos preguntan.</h3>{faqs}</div></div></section>\n')
    # 9 · cierre
    html += contacto() + "</main>" + footer() + CHAT + "</body></html>\n"
    return html


_VERSIONES = {}
def version(url):
    if url not in _VERSIONES:
        archivo = SITIO / url.lstrip("/")
        _VERSIONES[url] = hashlib.sha256(archivo.read_bytes()).hexdigest()[:10] if archivo.exists() else "0"
    return _VERSIONES[url]


def escribir(ruta, html):
    destino = SITIO / "oficinas" / ID / ruta / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Un espacio antes de cada salto en los títulos: en el celular los saltos se ocultan y las palabras no se pegan.
    html = re.sub(r"<(h[12])\b[^>]*>.*?</\1>", lambda m: re.sub(r"(?<! )<br/>", " <br/>", m.group(0)), html, flags=re.S)
    # Marca de versión según el contenido (?v=…): si una foto o el video cambian con el mismo nombre,
    # el navegador baja el nuevo en vez de mostrar el que tenía guardado.
    html = re.sub(r'((?:src|srcset|data-src|data-src-movil)=")(' + re.escape(ASSETS) + r'[^"?#\s]+)"', lambda m: f'{m.group(1)}{m.group(2)}?v={version(m.group(2))}"', html)
    html = html.replace("</body>", '<script defer src="/oficinas/assets/zona.js"></script><script defer src="/oficinas/assets/pie.js"></script></body>', 1)
    destino.write_text(html, encoding="utf-8")
    return destino


def revisar_trato(paginas):
    """Busca formas de tú/vos en el texto visible y en los atributos (equivale a tratoVetado)."""
    veto = re.compile(r"\b(" + "|".join(map(re.escape, FICHA["tratoVetado"])) + r")\b", re.I)
    hallazgos = []
    for ruta, html in paginas:
        sin_script = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
        visible = re.sub(r"<style.*?</style>", " ", sin_script, flags=re.S)
        texto = re.sub(r"<[^>]+>", " ", visible) + " ".join(re.findall(r'(?:alt|title|content|data-chat-prompt)="([^"]*)"', visible))
        for m in veto.finditer(texto):
            hallazgos.append(f"{ruta or 'inicio'}: «{texto[max(0, m.start() - 40):m.end() + 40].strip()}»")
    return hallazgos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    carpeta = SITIO / "oficinas" / ID
    for hija in carpeta.iterdir():
        if hija.is_dir() and hija.name != "assets":
            shutil.rmtree(hija)
    paginas = [("", pagina_inicio())]
    paginas += [(f"servicios/{x['slug']}/", pagina_detalle(x, f"servicios/{x['slug']}/", "servicio")) for x in SERV]
    paginas += [(f"plagas/{x['slug']}/", pagina_detalle(x, f"plagas/{x['slug']}/", "plaga")) for x in PLAG]
    paginas += [(f"{c}/", pagina_legal(c, t)) for c, t in [("privacidad", "Privacidad"), ("terminos", "Términos de uso"), ("accesibilidad", "Accesibilidad")]]
    # Goteo: nunca más de blog.porDia artículos con la misma fecha.
    por_dia = FICHA["blog"]["porDia"]
    fechas = [a["fecha"] for a in TODOS_ARTICULOS]
    excedidas = sorted({f for f in fechas if fechas.count(f) > por_dia})
    if excedidas:
        sys.exit(f"✗ goteo: más de {por_dia} artículos el {', '.join(excedidas)}")
    if ARTICULOS:
        paginas.append(("blog/", pagina_blog()))
        paginas += [(f"blog/{a['slug']}/", pagina_articulo(a)) for a in ARTICULOS]
    for ruta, html in paginas:
        escribir(ruta, html)
    urls = "".join(f"<url><loc>{FICHA['url']}{r}</loc></url>" for r, _ in paginas)
    (carpeta / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")

    # Imágenes que no existen y enlaces internos rotos
    errores = []
    for ruta, html in paginas:
        for ref in re.findall(r'(?:src|href|data-src|srcset)="(/[^"#?]*)', html):
            local = SITIO / ref.lstrip("/")
            if ref.endswith("/"):
                local = local / "index.html"
            if not local.exists():
                errores.append(f"{ruta or 'inicio'}: no existe {ref}")
    trato = revisar_trato(paginas)
    print(f"{len(paginas)} páginas generadas en {carpeta}")
    pendientes = [a for a in TODOS_ARTICULOS if a not in ARTICULOS]
    print(f"  blog ({HOY}{f", goteo pausado hasta {PAUSA}" if PAUSA else ""}): {len(ARTICULOS)} publicados" + (f", {len(pendientes)} en espera: " + ", ".join(f"{a['slug']} ({a['fecha']})" for a in pendientes) if pendientes else ""))
    for e in sorted(set(errores)):
        print("  ✗", e)
    for h in trato:
        print("  ⚠ trato:", h)
    if errores:
        sys.exit(1)
    print("  ✓ sin enlaces ni imágenes rotas")


if __name__ == "__main__":
    main()
