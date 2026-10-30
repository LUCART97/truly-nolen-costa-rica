"""Genera el borrador del sitio de Truly Nolen Costa Rica desde ficha/costa-rica.json.

Usa como plantilla de diseño el borrador de Venezuela (plantilla/inicio.html y plantilla/detalle.html):
de ahí salen las hojas de estilo, los scripts y el chat. Todo el contenido sale de la ficha.

Uso:  uv run --python 3.12 python generar.py
"""
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
TODOS_ARTICULOS = sorted((json.loads(p.read_text(encoding="utf-8")) for p in (RAIZ / "ficha" / "blog").glob("*.json")),
                         key=lambda a: (a["fecha"], a["slug"]), reverse=True)
ARTICULOS = [a for a in TODOS_ARTICULOS if date.fromisoformat(a["fecha"]) <= HOY]


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
{estilos or (HEAD_INICIO if inicio else HEAD_DETALLE)}</head>
"""


SERV = FICHA["paginas"]["servicios"]
PLAG = FICHA["paginas"]["plagas"]


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
    f = FICHA["footer"]
    s = "".join(f'<a href="{BASE}servicios/{x["slug"]}/">{escape(x["titulo"])}</a>' for x in SERV)
    p = "".join(f'<a href="{BASE}plagas/{x["slug"]}/">{escape(x["titulo"])}</a>' for x in PLAG)
    return f"""<footer class="country-footer local-footer" aria-label="Pie de página">
<figure class="footer-place"><img src="{ASSETS}{f['file']}" alt="{escape(f['alt'])}" width="1774" height="887" loading="lazy" decoding="async"/><figcaption>{escape(f['caption'])}</figcaption></figure>
<div class="footer-intro"><a class="brand" href="{BASE}"><img src="/tn-emblema.png" alt=""/><span>Truly Nolen <small data-preview-office>{PAIS}</small></span></a><p>{T['footerLema']}</p><a class="text-link" href="{BASE}#contacto">Conversemos</a></div>
<div class="footer-columns">
<nav aria-label="Servicios del pie"><h2>Servicios</h2>{s}<a href="{BASE}#consulta">Otras consultas</a><a href="{BASE}#metodo">Cómo trabajamos</a></nav>
<nav aria-label="Guía de plagas del pie"><h2>Guía de plagas</h2>{p}<a href="{BASE}#consulta">Consultar por otra plaga</a></nav>
<nav aria-label="Truly Nolen"><h2>Truly Nolen {PAIS}</h2><a href="{BASE}#nosotros">Nuestra forma de cuidar</a><a href="{BASE}#metodo">Cómo trabajamos</a><a href="{BASE}#cobertura">Consultar cobertura</a><a href="{BASE}#preguntas">Preguntas frecuentes</a>{f'<a href="{BASE}blog/">Blog</a>' if ARTICULOS else ""}<a href="{BASE}#contacto">Solicitar atención</a></nav>
<div class="footer-office"><h2>Hablemos</h2><p data-preview-office>{PAIS}</p><a href="#contacto" data-abrir-chat>Escribir a Truly AI</a></div>
</div>
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
    return f'<section id="metodo" class="section method"><div class="section-heading"><p class="eyebrow">{eyebrow}</p><h2>Un siguiente paso claro, en cada momento.</h2></div><div class="method-grid">{items}</div></section>\n'


def faq(eyebrow, titulo, preguntas, ident='id="preguntas" '):
    items = "".join(f'<details><summary>{escape(q)}<span aria-hidden="true">+</span></summary><p>{escape(a)}</p></details>' for q, a in preguntas)
    return f'<section {ident}class="section faq"><div><p class="eyebrow">{eyebrow}</p><h2>{titulo}</h2></div><div>{items}</div></section>\n'


def contacto():
    return f"""<section id="contacto" class="section contact"><div><p class="eyebrow">Truly Nolen · {PAIS}</p><h2>{escape(T['contactoTitulo'])}</h2><p>{escape(T['contactoTexto'])}</p></div>
<div class="contact-channels" style="display:flex;flex-wrap:wrap;align-items:center;gap:16px 28px;align-self:end"><a class="button" href="#contacto" data-abrir-chat>Escribir en el chat</a><a class="text-link" href="{WA}" target="_blank" rel="noopener noreferrer">Escribir por WhatsApp</a></div></section>
"""


def tarjeta_servicio(i, x):
    return f'<a class="service" href="{BASE}servicios/{x["slug"]}/"><img src="{ASSETS}{x["imagen"]}" alt="" loading="lazy"/><div><span>{i:02d}</span><h3>{escape(x["titulo"])}</h3><p>{escape(x["resumen"])}</p><span class="service-action">Ver servicio</span></div></a>'


def tarjeta_plaga(x):
    return f'<a href="{BASE}plagas/{x["slug"]}/"><img src="{ASSETS}{x["imagen"]}" loading="lazy" alt=""/><h3>{escape(x["titulo"])}</h3><span>Conocer más</span></a>'


def bloque(b):
    tipo = b["tipo"]
    if tipo == "tarjetas":
        arts = ""
        for it in b["items"]:
            checks = "".join(f"<li>{escape(c)}</li>" for c in it.get("checks", []))
            arts += f'<article><h3>{escape(it["h"])}</h3><p>{escape(it["p"])}</p>{f"<ul class=\"checks\">{checks}</ul>" if checks else ""}</article>'
        texto = f'<p>{escape(b["texto"])}</p>' if b.get("texto") else ""
        nota = f'<p class="nota-bloque">{escape(b["nota"])}</p>' if b.get("nota") else ""
        return f'<section class="section detail-guidance"><div class="section-heading"><p class="eyebrow">{escape(b["eyebrow"])}</p><h2>{b["titulo"]}</h2>{texto}</div><div class="guidance-grid">{arts}</div>{nota}</section>\n'
    if tipo == "cifras":
        arts = "".join(f'<article><strong>{escape(it["valor"])}</strong><p>{escape(it["texto"])}</p><small>{escape(it["fuente"])}</small></article>' for it in b["items"])
        return f'<section class="section detail-stats"><div class="section-heading"><p class="eyebrow">{escape(b["eyebrow"])}</p><h2>{b["titulo"]}</h2></div><div class="stats">{arts}</div></section>\n'
    if tipo == "consulta":
        return consulta("Una pregunta es un buen comienzo", "¿Por dónde<br/>empezamos?", T["consultaDetalleTexto"], b["starters"])
    if tipo == "relacionadas":
        if b["lista"] == "plagas":
            items = "".join(tarjeta_plaga(x) for x in PLAG if x["slug"] in b["slugs"])
            return f'<section class="section pests"><div class="section-heading"><p class="eyebrow">{escape(b["eyebrow"])}</p><h2>{b["titulo"]}</h2></div><div class="pest-grid">{items}</div></section>\n'
        items = "".join(tarjeta_servicio(i, x) for i, x in enumerate(SERV, 1) if x["slug"] in b["slugs"])
        return f'<section class="section services"><div class="section-heading"><p class="eyebrow">{escape(b["eyebrow"])}</p><h2>{b["titulo"]}</h2></div><div class="service-grid">{items}</div></section>\n'
    raise ValueError(f"tipo de bloque desconocido: {tipo}")


def fuentes(lista):
    items = "".join(f'<li><a href="{escape(u)}" target="_blank" rel="noopener noreferrer">{escape(t)}</a></li>' for t, u in lista)
    return f'<section class="section detail-sources"><div><p class="eyebrow">Fuentes</p><h2>De dónde sale esta información.</h2><p class="nota">{escape(T["fuentesNota"])}</p></div><ol>{items}</ol></section>\n'


def pagina_detalle(x, ruta, tipo):
    descripcion = x.get("descripcion") or re.sub("<[^>]+>", " ", x["intro"])
    html = head(f'{x["titulo"]} · Truly Nolen {PAIS}', descripcion, ruta, migas=[(x["titulo"], ruta)])
    html += BODY_DETALLE + nav() + '<main id="contenido">'
    html += f"""<section class="section detail-hero"><a class="text-link" href="{BASE}">← Volver al inicio</a><div class="story"><div>
<p class="eyebrow">{escape(x['eyebrow'])} · {PAIS}</p><h1>{x['lema']}</h1><p>{escape(x['intro'])}</p><a class="button" href="#contacto">Conversemos</a></div>
<img src="{ASSETS}{x['imagen']}" alt="{escape(x['titulo'])}"/></div></section>
"""
    html += "".join(bloque(b) for b in x["bloques"])
    html += faq("Preguntas frecuentes", "Lo que más nos preguntan." if tipo == "servicio" else "Hablemos con claridad.", x.get("preguntas") or FICHA["faq"], ident="")
    html += metodo("Cómo trabajamos") + fuentes(x["fuentes"]) + contacto() + "</main>" + footer() + CHAT + "</body></html>\n"
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
<div><p class="eyebrow">{escape(a['tema'])}</p><h2><a href="{url}">{escape(a['title'])}</a></h2><p>{escape(a['excerpt'])}</p><a class="text-link" href="{url}">Leer guía →</a></div></article>"""


def pagina_blog():
    # El primero va ancho; los que sobran en una última fila incompleta de tres también van anchos (sin huecos al lado).
    sobran = (len(ARTICULOS) - 1) % 3
    anchas = {0} | set(range(len(ARTICULOS) - sobran, len(ARTICULOS)))
    html = head(f"Blog de control de plagas · Truly Nolen {PAIS}", f"Guías sobre las plagas de {PAIS}: zancudos, comején, zompopas, ratas y más, con cada dato respaldado por su fuente.",
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
        p = plagas[c["plaga"]]
        url = f"{BASE}plagas/{p['slug']}/"
        consejos += f"""<article class="blog-card"><a href="{url}" tabindex="-1" aria-hidden="true"><img src="{ASSETS}{p['imagen']}" alt="" loading="lazy" style="object-fit:contain;background:#f7f6f1;padding:12px 18%"/></a>
<div><p class="eyebrow">{escape(p['titulo'])}</p><h2><a href="{url}">{escape(c['titulo'])}</a></h2><p>{escape(c['texto'])}</p><p style="font-size:13px;color:var(--muted)">Fuente: {escape(c['fuente'])}</p><a class="text-link" href="{url}">Ver la guía de {escape(p['titulo'].lower())} →</a></div></article>"""
    if consejos:
        html += f"""<section class="section blog-lista"><div class="section-heading"><p class="eyebrow">Prevención · {PAIS}</p><h2>Cómo prevenir<br/>cada plaga.</h2>
<p>Un consejo concreto por plaga, sacado de fuentes de Costa Rica, para empezar hoy mismo en su casa o su negocio.</p></div><div class="blog-grid">{consejos}</div></section>
"""
    if FICHA["blog"].get("consulta"):
        html += consulta("¿Necesita eliminar una plaga?", "Empecemos<br/>por lo que ve.", T["consultaDetalleTexto"], FICHA["blog"]["consulta"])
    return html + contacto() + "</main>" + footer() + CHAT + "</body></html>\n"


def pagina_articulo(a):
    ruta = f"blog/{a['slug']}/"
    portada = f"{FICHA['url']}assets/{a['cover']}"
    posting = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["meta_description"],
               "datePublished": a["fecha"], "inLanguage": "es", "image": portada,
               "author": {"@type": "Organization", "name": f"Truly Nolen {PAIS}"}, "publisher": {"@type": "Organization", "name": "Truly Nolen"}}
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a["faqs"]]}
    html = head(f"{a['title']} · Truly Nolen {PAIS}", a["meta_description"], ruta, migas=[("Blog", "blog/"), (a["title"], ruta)],
                estilos=HEAD_BLOG, og_tipo="article", extra_ld=[posting, faqpage])
    credito = ""
    if a.get("credito"):
        credito = f'<p class="blog-meta"><a href="{escape(a["creditoUrl"])}" target="_blank" rel="noopener noreferrer">{escape(a["credito"])}</a></p>'
    html += BODY_INICIO + nav() + '<main id="contenido">'
    html += f"""<article class="section blog-articulo"><nav class="blog-migas" aria-label="Ruta"><a href="{BASE}">Inicio</a> · <a href="{BASE}blog/">Blog</a> · <span>{escape(a['tema'])}</span></nav>
<p class="eyebrow">{escape(a['tema'])}</p><h1>{escape(a['title'])}</h1><p class="blog-entrada">{escape(a['excerpt'])}</p>
<p class="blog-meta">Truly Nolen {PAIS} · {fecha_larga(a['fecha'])} · {a['minutos']} min de lectura</p>
<img class="blog-portada" src="{ASSETS}{a['cover']}" alt="{escape(a['og_alt_text'])}"/>{credito}
<div class="blog-cuerpo">{a['content_html']}</div></article>
"""
    html += faq(escape(a["tema"]), "Preguntas frecuentes", a["faqs"], ident="")
    html += fuentes(a["fuentes"])
    otros = [x for x in ARTICULOS if x["slug"] != a["slug"]][:2]
    if otros:
        html += f'<section class="section"><div class="section-heading"><p class="eyebrow">Blog</p><h2>Artículos relacionados</h2></div><div class="blog-grid">{"".join(tarjeta_articulo(x) for x in otros)}</div></section>\n'
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
    I, F = FICHA["inicio"], FICHA["fotos"]
    pel = FICHA["pelicula"]
    html = head(FICHA["seo"]["titulo"], FICHA["seo"]["descripcion"], "", inicio=True)
    html += f'<body class="country-site jardin" data-machote="{ID}" data-oficina="{ID}">' + nav() + '<main id="contenido">'
    html += f"""<section class="cinema" id="inicio"><div class="film"><picture><source media="(max-width:760px)" srcset="{ASSETS}{pel['poster']}"/><img src="{ASSETS}{pel['poster']}" alt=""/></picture>
{f'<video muted loop playsinline preload="none" aria-hidden="true" data-src="{ASSETS}{pel["video"]}"></video>' if pel.get("video") else ""}{carrito()}</div>
<div class="hero-text"><p class="eyebrow">Truly Nolen · <span data-preview-office>{PAIS}</span></p><h1>{escape(I['h1'])}</h1><p>{escape(I['intro'])}</p><a class="button" href="#contacto">{escape(I['cta'])}</a></div>
<a class="discover" href="#servicios">{escape(I['descubre'])}</a></section>
<section id="servicios" class="section services"><div class="section-heading"><p class="eyebrow">Truly Nolen · {PAIS}</p><h2>{escape(I['serviciosTitulo'])}</h2><p>{escape(I['serviciosTexto'])}</p></div>
<div class="service-grid">{"".join(tarjeta_servicio(i, x) for i, x in enumerate(SERV, 1))}</div></section>
"""
    benef = "".join(f'<article><img src="/oficinas/assets/{ic}" alt="" width="56" height="56" loading="lazy"/><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for ic, h, p in I["beneficios"])
    html += f"""<section id="nosotros" class="section local-benefits"><div class="section-heading"><p class="eyebrow">Truly Nolen · {PAIS}</p><h2>{escape(I['nosotrosTitulo'])}</h2><p>{escape(I['nosotrosTexto'])}</p></div>
<div class="benefits-layout"><img class="benefits-photo" src="{ASSETS}{F['nosotros']['file']}" alt="{escape(F['nosotros']['alt'])}" loading="lazy"/><div class="benefits-grid">{benef}</div></div></section>
"""
    zonas = "".join(f"<li><strong>{escape(a)}</strong><span>{escape(b)}</span></li>" for a, b in I["casaZonas"])
    b1, b2 = I["operacionBotones"]
    html += f"""<section class="section local-home"><div class="home-visual"><img src="{ASSETS}{F['casa']['file']}" alt="{escape(F['casa']['alt'])}" loading="lazy"/></div>
<div><p class="eyebrow">De adentro hacia afuera</p><h2>{escape(I['casaTitulo'])}</h2><p>{escape(I['casaTexto'])}</p><ol>{zonas}</ol><a class="text-link" href="{BASE}servicios/hogares/">{escape(I['casaLink'])}</a></div></section>
<section class="local-operation"><img src="{ASSETS}{F['operacion']['file']}" alt="{escape(F['operacion']['alt'])}" loading="lazy"/>
<div><p class="eyebrow">Comercio e industria</p><h2>{escape(I['operacionTitulo'])}</h2><p>{escape(I['operacionTexto'])}</p>
<div class="operation-actions"><a class="button" href="{BASE}servicios/comercios/">{escape(b1)}</a><a class="button" href="{BASE}servicios/industria/">{escape(b2)}</a></div></div></section>
<section id="plagas" class="section pests"><div class="section-heading"><p class="eyebrow">01 / Guía de plagas</p><h2>Reconozca las señales.</h2></div><div class="pest-grid">{"".join(tarjeta_plaga(x) for x in PLAG)}</div></section>
"""
    html += metodo("02 / Cómo trabajamos")
    html += f"""<section id="cobertura" class="section local-coverage"><div><p class="eyebrow">Aquí, en {PAIS}</p><h2>{escape(I['coberturaTitulo'])}</h2></div>
<div><p>{escape(I['coberturaTexto'])}</p><a class="text-link" href="#contacto" data-abrir-chat data-chat-prompt="{escape(I['coberturaPrompt'])}">Consultar mi zona</a></div></section>
"""
    html += faq("03 / Preguntas frecuentes", "Hablemos con claridad.", FICHA["faq"])
    html += consulta("Una pregunta es un buen comienzo", escape(I["consultaTitulo"]), I["consultaTexto"], I["consultaStarters"], ident='id="consulta" ')
    html += contacto() + "</main>" + footer() + CHAT + "</body></html>\n"
    return html


def escribir(ruta, html):
    destino = SITIO / "oficinas" / ID / ruta / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
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
    print(f"  blog ({HOY}): {len(ARTICULOS)} publicados" + (f", {len(pendientes)} en espera: " + ", ".join(f"{a['slug']} ({a['fecha']})" for a in pendientes) if pendientes else ""))
    for e in sorted(set(errores)):
        print("  ✗", e)
    for h in trato:
        print("  ⚠ trato:", h)
    if errores:
        sys.exit(1)
    print("  ✓ sin enlaces ni imágenes rotas")


if __name__ == "__main__":
    main()
