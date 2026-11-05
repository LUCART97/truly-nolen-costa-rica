"""Réplica 1:1 de globaltni.com/es para Costa Rica (receta truly-inbound del 5-nov-2026, reglas R1-R19).
Se corre al final (después de sectores.py). Usa el HTML, las hojas y el main.js REALES de globaltni (plantilla/gt/, bajados
de globaltni.com el 5-nov-2026) y cambia solo lo que es de Costa Rica:
  - portada  = /es/ de globaltni  (hero con el video de Costa Rica, plagas y blog del país, cierre de la oficina, sin franquicia)
  - Hogares  = /es/services/residential/  tal cual (R17), con los enlaces llevados a la oficina
  - Comercios= /es/services/commercial/   tal cual (R17)
  - el resto (Industria, plagas, blog, legales): su contenido + el encabezado y el pie de globaltni (R1)
Encabezado: franja gris (lema, Adentro de Truly, My Truly, redes), barra amarilla, menú con desplegables (R18), lupa
(.gt-buscar, R4), «Hablemos →»; sin franquicias ni idiomas (R4). Pie: ilustración y lema de globaltni (R11).
Chat: el de Truly AI con el carrito del tamaño de globaltni (R8). Siempre de usted (R3)."""
import html, json, re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parent
GT = R / "plantilla/gt"
F = json.loads((R / "ficha/costa-rica.json").read_text(encoding="utf-8"))
C = R / "sitio/oficinas" / F["id"]
B = f"/oficinas/{F['id']}/"
G = "/oficinas/gt/"
A = f"{B}assets/"
GTX = "https://globaltni.com/es/"
EXT = ' target="_blank" rel="noopener"'
WA = "https://wa.me/" + re.sub(r"\D", "", F.get("whatsappTrulyAI") or "15202145675")
e = lambda s: html.escape(s or "", quote=True)
PLAGAS = [p for p in F["paginas"]["plagas"] if (C / "plagas" / p["slug"] / "index.html").exists()]
PAG = lambda s: f"{B}plagas/{s}/"

# ---------- 1 · archivos de globaltni en el sitio ----------
dst = R / "sitio/oficinas/gt"
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(GT / "a", dst / "a"); shutil.copytree(GT / "assets", dst / "assets")
if (GT / "en").exists(): shutil.copytree(GT / "en", dst / "en")
for f in list((dst / "a").glob("*.css")) + list((dst / "assets").glob("*.css")):
    t = f.read_text(encoding="utf-8")
    t = t.replace("url('/assets/", f"url('{G}assets/").replace('url("/assets/', f'url("{G}assets/').replace("url(/assets/", f"url({G}assets/")
    t = t.replace("url('/a/", f"url('{G}a/")
    f.write_text(t, encoding="utf-8")
# main.js: índice de búsqueda de Costa Rica, lupa .gt-buscar (R4) y sin directorio de oficinas de globaltni
mj = (GT / "a/main.js").read_text(encoding="utf-8")
idx = [{"url": B, "en": "Home", "es": "Inicio", "category": "Overview", "categoryEs": "Inicio", "keywords": "inicio costa rica truly nolen"}]
for s in F["paginas"]["servicios"]:
    idx.append({"url": f"{B}servicios/{s['slug']}/", "en": s["titulo"], "es": s["titulo"], "category": "Services", "categoryEs": "Servicios",
                "keywords": " ".join([s["titulo"], s.get("intro", "")]).lower()})
for p in PLAGAS:
    idx.append({"url": PAG(p["slug"]), "en": p["titulo"], "es": p["titulo"], "category": "Pests", "categoryEs": "Guía de plagas",
                "keywords": " ".join([p["titulo"], p.get("intro", "")]).lower()})
for a in sorted((C / "blog").glob("*/index.html")):
    t = a.read_text(encoding="utf-8"); h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    if h1: idx.append({"url": f"{B}blog/{a.parent.name}/", "en": re.sub("<[^>]+>", "", h1.group(1)), "es": re.sub("<[^>]+>", "", h1.group(1)),
                       "category": "Journal", "categoryEs": "Blog", "keywords": a.parent.name.replace("-", " ")})
idx.append({"url": f"{B}blog/", "en": "Blog", "es": "Blog", "category": "Journal", "categoryEs": "Blog", "keywords": "blog consejos prevención"})
i0 = mj.index("const routeIndex = ["); i1 = mj.index("// END GENERATED A ROUTE INDEX")
mj = mj[:i0] + "const routeIndex = " + json.dumps(idx, ensure_ascii=False, indent=1) + ";\n  " + mj[i1:]
mj = mj.replace("searchIndex.push([english ? t('International contact') : 'Contacto internacional', 'oficina corporativa orlando representante internacional international contact', `${prefix}/${locale}/contact/international/`, english ? t('Contact') : 'Contacto']);",
                f"searchIndex.push(['Escribir a Truly AI', 'contacto chat whatsapp consulta cobertura', '{B}#contacto', 'Contacto']);")
mj = mj.replace("if (!locationsReady) locationsReady = fetch('/assets/a-search-locations.json')", "if (!locationsReady) locationsReady = Promise.reject()")
mj = mj.replace("document.querySelector('.search-open')", "document.querySelector('.gt-buscar')")
(dst / "a/main.js").write_text(mj, encoding="utf-8")
# car-hero.js: el carro de Costa Rica y el mundo común de las oficinas
ch = (GT / "a/car-hero.js").read_text(encoding="utf-8")
ch = re.sub(r"desktop: `/a/media/car/car-desktop\.mp4\?v=\$\{carVersion\}`", f"desktop: `{A}costa-rica-desktop.mp4`", ch)
ch = re.sub(r"mobile: `/a/media/car/car-mobile\.mp4\?v=\$\{carVersion\}`", f"mobile: `{A}costa-rica-movil.mp4`", ch)
ch = re.sub(r"desktop: `/a/media/world/world-desktop\.mp4\?v=\$\{worldVersion\}`", "desktop: `/oficinas/assets/mundo-desktop.mp4`", ch)
ch = re.sub(r"mobile: `/a/media/world/world-mobile\.mp4\?v=\$\{worldVersion\}`", "mobile: `/oficinas/assets/mundo-movil.mp4`", ch)
ch = ch.replace("desktop: `/a/media/world/world-desktop.webp?v=${worldVersion}`", "desktop: `/oficinas/assets/mundo-desktop.webp`").replace("mobile: `/a/media/world/world-mobile.webp?v=${worldVersion}`", "mobile: `/oficinas/assets/mundo-movil.webp`")
assert "mundo-desktop.webp" in ch
assert "costa-rica-desktop.mp4" in ch and "mundo-movil.mp4" in ch, "car-hero.js: no encontré las fuentes del video"
(dst / "a/car-hero.js").write_text(ch, encoding="utf-8")

# ---------- 2 · piezas comunes ----------
def gtpage(n): return (GT / f"{n}.html").read_text(encoding="utf-8")
HOME = gtpage("home")
SVG = dict(re.findall(r'aria-label="(Facebook|Instagram|LinkedIn)"[^>]*>(<svg.*?</svg>)', HOME, re.S))
ICO_BUSCAR = re.search(r'class="search-open"><span>Buscar</span>(<svg.*?</svg>)', HOME, re.S).group(1)
ICO_CHEV = '<svg aria-hidden="true" viewBox="0 0 12 12"><path d="m 2 4 4 4 4-4"></path></svg>'
OFFICE = re.search(r'<span aria-hidden="true" class="office-mark">(<svg.*?</svg>)</span>', HOME, re.S).group(1)
REDES = [("Facebook", "https://www.facebook.com/TrulyNolenINT"), ("Instagram", "https://www.instagram.com/trulynoleninternational/"),
         ("LinkedIn", "https://www.linkedin.com/company/truly-nolen-international/")]
PORTALES = [("Adentro de Truly", "https://www.trulynoleninternational.com/TrulyInside/index.asp?lng=2"), ("My Truly", "https://vip.trulynoleninternational.com/")]
SERV = [("Sistema TEPS", "Evaluación, documentación y seguimiento.", f"{B}#teps"),
        ("Comercial", "Protección para los retos de cada sector.", f"{B}servicios/comercios/"),
        ("Sanitización", "Control microbiano en ambientes interiores.", f"{B}#sanitizacion"),
        ("Residencial", "Un programa para toda su casa.", f"{B}servicios/hogares/")]


def mega(idd, titulo, frase, link_txt, link_href, items):
    li = "".join(f'<a href="{h}"><strong>{e(a)}</strong><span>{e(b)}</span></a>' for a, b, h in items)
    return (f'<div class="nav-item"><button aria-controls="{idd}" aria-expanded="false" class="nav-trigger">{e(titulo)}{ICO_CHEV}</button>'
            f'<div class="mega" hidden="" id="{idd}"><div class="mega-intro"><p>{e(frase)}</p><a class="text-link" href="{link_href}">{e(link_txt)} '
            f'<span aria-hidden="true">→</span></a></div><div class="mega-links">{li}</div></div></div>')


def cabecera():
    redes = "".join(f'<a aria-label="{n}" href="{u}"{EXT}>{SVG[n]}</a>' for n, u in REDES)
    port = "".join(f'<a href="{u}"{EXT}>{e(n)}</a>' for n, u in PORTALES)
    nos = [("Nuestra historia", "De una idea en 1938 a una visión internacional.", f"{B}#nosotros"),
           ("Preguntas frecuentes", "Respuestas para conocer nuestros servicios.", f"{B}#preguntas"),
           ("Blog", "Consejos sobre plagas en Costa Rica.", f"{B}blog/"),
           ("Industria", "Programas para plantas y bodegas.", f"{B}servicios/industria/")]
    pl = [(p["titulo"], "Información e identificación de la plaga.", PAG(p["slug"])) for p in PLAGAS]
    nav = (mega("nav-services", "Servicios", "Cuidar comienza por entender su espacio.", "Explorar servicios", f"{B}#servicios", SERV)
           + mega("nav-company", "Sobre nosotros", "Una historia que sigue en movimiento.", "Conocer Truly Nolen", f"{B}#nosotros", nos)
           + mega("nav-pests", "Plagas", "Conozca a los visitantes que no invitó.", "Ver guías de plagas", f"{B}#plagas", pl)
           + f'<a class="nav-office" href="{B}#oficinas">Oficinas</a>'
           + f'<button aria-label="Buscar en el sitio" class="search-open gt-buscar" type="button"><span>Buscar</span>{ICO_BUSCAR}</button>'
           + f'<a class="button nav-cta" href="#contacto" data-abrir-chat>Hablemos <span aria-hidden="true">→</span></a>'
           + f'<div class="mobile-portals"><div aria-labelledby="mobile-access-label" class="mobile-access-group" role="group"><p class="mobile-group-label" id="mobile-access-label">Accesos</p>{port}</div>'
           + f'<div aria-label="Redes sociales" class="feedback-social">{redes}</div></div>')
    return (f'<header class="site-header"><div class="utility"><span>Experiencia internacional. Servicio local.</span><div>{port}</div>'
            f'<div aria-label="Redes sociales" class="feedback-social">{redes}</div></div>'
            f'<div class="nav-shell"><a aria-label="Truly Nolen Costa Rica, inicio" class="brand" href="{B}"><img alt="Truly Nolen International" height="512" loading="eager" src="{G}assets/global-link-logo.png" width="512"/>'
            f'<span aria-hidden="true" class="brand-name">Truly Nolen<small>Costa Rica</small></span></a>'
            f'<button aria-controls="navigation" aria-expanded="false" class="menu-toggle"><span>Menú</span><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M 3 7h 18M 3 17h 18"></path></svg></button>'
            f'<nav aria-label="Navegación principal" class="navigation" id="navigation">{nav}</nav></div></header>')


def pie():
    grupo = lambda t, links: f'<details open=""><summary>{e(t)}</summary><div class="footer-links">{links}</div></details>'
    a = lambda n, h, ext=False: f'<a href="{h}"{EXT if ext else ""}>{e(n)}</a>'
    serv = "".join(a(n, h) for n, _, h in SERV) + a("Industria", f"{B}servicios/industria/")
    tn = a("Nuestra historia", f"{GTX}company/story/", True) + a("Nuestro equipo", f"{GTX}company/team/", True) + a("Preguntas frecuentes", f"{B}#preguntas") + a("Blog", f"{B}blog/")
    pl = "".join(a(p["titulo"], PAG(p["slug"])) for p in PLAGAS)
    acc = "".join(a(n, u, True) for n, u in PORTALES)
    con = (f'<a href="#contacto" data-abrir-chat>Escribir a Truly AI</a><a href="{WA}"{EXT}>WhatsApp</a>'
           + "".join(a(n, u, True) for n, u in REDES))
    return (f'<footer class="footer footer-paper"><div class="wrap"><div class="footer-top"><a class="footer-brand" href="{B}"><img alt="Truly Nolen International" height="85" loading="eager" src="{G}assets/global-link-logo.png" width="200"/></a>'
            f'<p>Control de plagas.<br/>Control microbiológico.<br/>Una visión internacional.</p><a class="footer-contact" href="#page-top">Volver al inicio <span aria-hidden="true">↑</span></a></div>'
            f'<div class="footer-grid">{grupo("Servicios", serv)}{grupo("Truly Nolen", tn)}{grupo("Guía de plagas", pl)}{grupo("Accesos", acc)}{grupo("Conecte con nosotros", con)}</div></div>'
            f'<figure class="footer-landscape"><img alt="Comunidad ilustrada con viviendas, comercios, jardines y un coche amarillo de servicio" height="887" loading="lazy" src="{G}assets/footer-community-a.webp" width="1774"/></figure>'
            f'<div class="wrap footer-tail"><div class="footer-bottom"><span>© 2026 Truly Nolen Costa Rica</span>'
            f'<a href="{B}privacidad/">Privacidad</a><a href="{B}terminos/">Términos de uso</a><a href="{B}accesibilidad/">Accesibilidad</a></div></div></footer>')


BUSCAR = ('<dialog aria-labelledby="search-title" class="search-dialog"><div class="search-heading"><h2 id="search-title">¿Qué está buscando?</h2>'
          '<button aria-label="Cerrar búsqueda" class="search-close">×</button></div><label for="site-search">Busque servicios, plagas o artículos</label>'
          '<input autocomplete="off" id="site-search" placeholder="Por ejemplo: zancudos o comercios" type="search"/><p aria-live="polite" class="search-count"></p><ul class="search-results"></ul></dialog>')

CIERRE = (f'<section aria-labelledby="contact-title" class="contact-band" id="contacto"><div class="wrap contact-layout"><div class="contact-intro">'
          f'<h2 id="contact-title">Cuéntenos qué <br/>necesita proteger.</h2><p>Truly AI le orienta en el siguiente paso, aquí mismo o por WhatsApp.</p></div>'
          f'<div class="contact-actions"><a class="button button-dark" href="#contacto" data-abrir-chat>Escribir a Truly AI <span aria-hidden="true">→</span></a>'
          f'<a class="text-link" href="{WA}"{EXT}>Escribir por WhatsApp <span aria-hidden="true">→</span></a></div></div></section>')

# chat de Truly AI (el de la portada actual) y su hoja
INDEX = (C / "index.html").read_text(encoding="utf-8")


def bloque_div(t, inicio):
    i = t.find(inicio); assert i >= 0, inicio
    n, j = 0, i
    for m in re.finditer(r"<(/?)div\b", t[i:]):
        n += -1 if m.group(1) else 1
        if n == 0: j = i + m.end(); break
    return t[i:t.index(">", j) + 1]


CHAT = bloque_div(INDEX, '<div class="tia"')
CHAT_SCRIPTS = "".join(re.findall(r'<script defer src="/landing/chat\.js[^"]*"></script>', INDEX))
CHAT_CSS = "".join(re.findall(r'<link rel="stylesheet" href="/landing/chat\.css[^"]*"/>', INDEX))
assert CHAT_SCRIPTS and CHAT_CSS, "no encontré chat.js o chat.css en la portada"
# carrito del chat igual al de globaltni (R8): 112×108 a 16/12 px; celular 88×89 a 10/10; carro 108×70; globo 68×36
CARRITO = """<style>
body.a-site .tia{right:16px!important;bottom:12px!important}
body.a-site .tia-fab{width:112px!important;height:108px!important;padding:0!important;display:flex!important;align-items:flex-end!important;justify-content:center!important;background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;filter:drop-shadow(0 2px 3px #01000729);position:relative}
body.a-site .tia-fab .tia-carro{width:108px!important;height:70px!important;object-fit:contain}
body.a-site .tia-fab>svg{display:none!important}
body.a-site .tia-fab-txt{position:absolute!important;top:0;right:0;left:auto;min-width:68px;height:36px;padding:0 13px!important;margin:0!important;display:flex!important;align-items:center;justify-content:center;background:#ffd800!important;color:#010007!important;border:1px solid #010007!important;border-radius:12px!important;font:700 14px/1 Montserrat,system-ui,sans-serif!important;box-shadow:none!important}
body.a-site .tia-fab-txt::before{content:"Chat";font:700 14px/1 Montserrat,system-ui,sans-serif}
body.a-site .tia-fab-txt{font-size:0!important}
body.a-site .tia-fab-txt>*{display:none!important}
body.a-site .tia-fab-txt::after{content:"";position:absolute;right:19px;bottom:-6px;width:9px;height:9px;background:#ffd800;border-right:1px solid #010007;border-bottom:1px solid #010007;transform:skewY(-38deg)}
body.a-site .tia--on .tia-fab{display:none!important}
@media(max-width:600px){body.a-site .tia{right:10px!important;bottom:10px!important}
body.a-site .tia-fab{width:88px!important;height:89px!important}
body.a-site .tia-fab .tia-carro{width:86px!important;height:56px!important}
body.a-site .tia-fab-txt{height:32px;min-width:62px;padding:0 10px!important;border-radius:10px!important;font-size:0!important}
body.a-site .tia-fab-txt::before{font-size:13px}
body.a-site .tia--on{left:0!important;right:0!important;bottom:0!important;top:77px!important;align-items:stretch!important}
body.a-site .tia--on .tia-panel{width:100%!important;height:100%!important;max-height:none!important;border-radius:16px 16px 0 0!important}}
body.a-site .tia-panel{max-height:calc(100dvh - 150px)}
</style>"""
# listas de sectores en celular: globaltni parte «Supermercado/s» a mitad de palabra; aquí se silabea en español (única diferencia a propósito)
CARRITO += "<style>@media(max-width:620px){.ct-facilities li{-webkit-hyphens:manual!important;hyphens:manual!important;overflow-wrap:normal!important}}</style>"

HOJAS = re.findall(r'<link href="(/a/[^"?]+\.css)[^"]*" rel="stylesheet"/>|<link href="(/assets/franchise-chat\.css)[^"]*" rel="stylesheet"/>', HOME)


def cabeza(t_gt, t_cr, extra_css=""):
    """<head> de globaltni (hojas y scripts) con el SEO, la CSP y el chat de la página de Costa Rica."""
    hojas = re.findall(r'<link href="/a/([^"?]+\.css)[^"]*" rel="stylesheet"/>', t_gt)
    js = [j for j in re.findall(r'<script defer="[^"]*" src="/a/([^"?]+\.js)[^"]*"></script>', t_gt) if j not in ("analytics.js",)]
    head_cr = t_cr[t_cr.find("<head>") + 6:t_cr.find("</head>")]
    seo = "".join(re.findall(r'<title>.*?</title>|<meta (?:name|property)="(?:description|robots|og:[^"]*|twitter:[^"]*)"[^>]*>|<link rel="(?:canonical|icon)"[^>]*>|<script type="application/ld\+json">.*?</script>|<meta http-equiv="Content-Security-Policy"[^>]*>', head_cr, re.S))
    return ('<head><meta charset="utf-8"/><meta content="only light" name="color-scheme"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta content="#FFD800" name="theme-color"/>'
            + seo + f'<link as="font" crossorigin="" href="{G}assets/montserrat-latin-900-normal.woff2" rel="preload" type="font/woff2"/>'
            + "".join(f'<link href="{G}a/{h}" rel="stylesheet"/>' for h in hojas)
            + "".join(f'<script defer src="{G}a/{j}"></script>' for j in js)
            + CHAT_CSS + CHAT_SCRIPTS + CARRITO + extra_css + "</head>")


def fin_body():
    return BUSCAR + CHAT


def links_gt(t):
    """Enlaces de globaltni llevados a la oficina (o a globaltni si la oficina no tiene esa página)."""
    m = {"/es/services/residential/": f"{B}servicios/hogares/", "/es/services/commercial/": f"{B}servicios/comercios/",
         "/es/contact/": "#contacto", "/es/contact/#formulario": "#contacto", "/es/contact/international/": "#contacto",
         "/es/offices/": "#contacto", "/es/": B, "/es/journal/": f"{B}blog/"}
    def r(mm):
        h = mm.group(1); base, _, frag = h.partition("#")
        if h in m: return f'href="{m[h]}"' + (" data-abrir-chat" if m[h] == "#contacto" else "")
        if base in m and frag: return f'href="{m[base]}#{frag}"'
        if h.startswith("/es/"): return f'href="https://globaltni.com{h}"{EXT}'
        return mm.group(0)
    t = re.sub(r'href="(/es/[^"]*)"', r, t)
    t = t.replace('src="/assets/', f'src="{G}assets/').replace('src="/en/', f'src="{G}en/').replace('srcset="/assets/', f'srcset="{G}assets/')
    return t


def pagina(t_gt, t_cr, main, body_cls, extra_css=""):
    body = re.search(r"<body([^>]*)>", t_gt).group(1)
    body = re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} {body_cls}"'.strip(), body)
    return ('<!DOCTYPE html>\n<html lang="es">' + cabeza(t_gt, t_cr, extra_css) + f"<body{body}>" + cabecera() + main + pie() + fin_body() + "</body></html>\n")


# ---------- 3 · portada ----------
I = F["inicio"]
main = HOME[HOME.find("<main"):HOME.find("</main>") + 7]
# hero: el carro de Costa Rica
poster_d = f"{A}costa-rica-desktop.webp"; poster_m = f"{A}costa-rica-movil.webp" if (C / "assets/costa-rica-movil.webp").exists() else poster_d
main = re.sub(r'<picture class="car-poster">.*?</picture>',
              f'<picture class="car-poster"><source media="(max-width:1023px)" srcset="{poster_m}"/><img alt="El carro amarillo de Truly Nolen en una carretera junto al volcán Arenal, Costa Rica" fetchpriority="high" height="2160" loading="eager" src="{poster_d}" width="3840"/></picture>', main, 1, re.S)
h1 = I["h1"].replace("en casa, ", "en casa,<br/>").replace("Pura vida en casa,<br/>sin plagas.", "Pura vida en casa,<br/>sin plagas.")
main = re.sub(r'<p class="car-kicker">.*?</p><h1 id="hero-title">.*?</h1>', f'<p class="car-kicker">Truly Nolen · Costa Rica</p><h1 id="hero-title">{h1}</h1>', main, 1, re.S)
main = re.sub(r'<p class="car-description">.*?</p>', f'<p class="car-description"><span class="car-phrase">{e(I["intro"])}</span></p>', main, 1, re.S)
main = re.sub(r'<a class="button" href="/es/offices/">Encuentre su oficina <span aria-hidden="true" class="office-mark">.*?</span></a>',
              lambda m: f'<a class="button" href="#contacto" data-abrir-chat>{e(I["cta"])} <span aria-hidden="true" class="office-mark">{OFFICE}</span></a>', main, 1, re.S)
main = main.replace("Servicio premium · Experiencia internacional", "Servicio de primera calidad · Experiencia internacional")
# sin franquicia (vuelta 9)
main = re.sub(r'<section class="franchise wrap".*?</section>', "", main, 1, re.S)
# plagas de Costa Rica (fotos reales)
cards = ""
for p in PLAGAS[:5]:
    foto = next((f for f in (f"cr-plaga-{p['slug']}-foto.webp",) if (C / "assets" / f).exists()), None)
    frase = re.split(r"(?<=\.)\s", p.get("intro", ""))[0]
    sub = p.get("eyebrow", "").replace("Guía de ", "").capitalize()
    cards += (f'<a href="{PAG(p["slug"])}"><img alt="{e(p["titulo"])}" class="editorial-specimen" height="560" loading="lazy" src="{A}{foto}" width="840"/>'
              f'<div><h3>{e(p["titulo"])}</h3><strong>En Costa Rica</strong><p>{e(frase)}</p><span class="pest-guide-link">Ver la guía <span aria-hidden="true">→</span></span></div></a>')
main = re.sub(r'(<div class="pest-list">).*?(</div></section>)', lambda m: m.group(1) + cards + m.group(2), main, 1, re.S)
main = main.replace("Un primer vistazo a especies comunes. Las guías amplían sus características y la oficina local puede ayudar con la identificación.",
                    I.get("plagasTexto", "Las que más vemos en Costa Rica. Cada guía explica las señales y qué hacer, con fuentes."))
# blog de Costa Rica + preguntas de la oficina
arts = sorted((C / "blog").glob("*/index.html"))
a0 = arts[0].read_text(encoding="utf-8")
t_art = re.sub("<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", a0, re.S).group(1)).strip()
img = re.search(r'<img[^>]*src="([^"]+)"[^>]*>', a0[a0.find("<main"):]).group(1)
ent = re.sub("<[^>]+>", "", (re.search(r'<p class="s-entrada">(.*?)</p>', a0, re.S) or re.search(r"<p>(.{60,}?)</p>", a0, re.S)).group(1))[:260]
story = (f'<article class="knowledge-story"><div class="story-meta"><img alt="" height="459" loading="lazy" src="{img}" style="aspect-ratio:422 / 459;height:auto;object-fit:cover;object-position:center" width="422"/>'
         f'<div><span>Del blog de Truly Nolen Costa Rica</span></div></div><h3>{e(t_art)}</h3><p>{e(ent)}</p>'
         f'<a class="text-link" href="{B}blog/{arts[0].parent.name}/">Leer el artículo <span aria-hidden="true">→</span></a>'
         f'<a class="text-link resource-archive-link" href="{B}blog/">Ver todo el blog<span aria-hidden="true">→</span></a></article>')
faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(r)}</p></details>' for i, (q, r) in enumerate(F["faq"][:3]))
faqb = (f'<div class="knowledge-faq" id="preguntas"><h3>Lo que más nos preguntan.</h3><p class="faq-intro">Respuestas sobre cómo trabajamos en Costa Rica.</p>{faq}'
        f'<a class="text-link" href="#contacto" data-abrir-chat>Hacer otra pregunta <span aria-hidden="true">→</span></a></div>')
main = re.sub(r'<article class="knowledge-story">.*?</article>', lambda m: story, main, 1, re.S)
main = re.sub(r'<div class="knowledge-faq">.*?</div>(?=</div></div></section>)', lambda m: faqb, main, 1, re.S)
# red internacional: el directorio de oficinas es el de globaltni
main = re.sub(r'<section class="network".*?</section>', lambda m: m.group(0).replace('href="/es/offices/"', f'href="{GTX}offices/"{EXT}').replace('href="/es/contact/#formulario">Escríbanos desde el formulario de contacto', 'href="#contacto">Escríbale a Truly AI'), main, 1, re.S)
# cierre de la oficina
main = re.sub(r'<section aria-labelledby="contact-title" class="contact-band">.*?</section>', lambda m: CIERRE, main, 1, re.S)
main = links_gt(main)
(C / "index.html").write_text(pagina(HOME, INDEX, main, ""), encoding="utf-8")

# ---------- 4 · Hogares y Comercios = páginas de globaltni (R17) ----------
for slug, n in (("hogares", "residential"), ("comercios", "commercial")):
    t_gt = gtpage(n); f = C / "servicios" / slug / "index.html"; t_cr = f.read_text(encoding="utf-8")
    m = t_gt[t_gt.find("<main"):t_gt.find("</main>") + 7]
    m = links_gt(m)
    m = re.sub(r'<section aria-labelledby="contact-title" class="contact-band">.*?</section>', lambda x: CIERRE, m, 1, re.S)
    m = m.replace("<main", f"<!--gt-pagina:{n}--><main", 1)
    (f).write_text(pagina(t_gt, t_cr, m, ""), encoding="utf-8")

# ---------- 5 · resto de páginas: su contenido + encabezado y pie de globaltni ----------
RES = gtpage("residential")
hechas = 0


def css_reforzado(ruta):
    """Las reglas .ct-* de globaltni con más peso (html body.gt-interna.gt-interna …) para ganarle al molde viejo
    (body.country-site[data-oficina] h2 …) sin cambiar ni un valor."""
    c = re.sub(r"/\*.*?\*/", "", ruta.read_text(encoding="utf-8"), flags=re.S)
    def bloque(t):
        out, i = [], 0
        while True:
            j = t.find("{", i)
            if j < 0: return "".join(out)
            sel = t[i:j].strip()
            if sel.startswith("@"):
                d, k = 1, j + 1
                while d: d += (t[k] == "{") - (t[k] == "}"); k += 1
                dentro = bloque(t[j + 1:k - 1])
                if dentro: out.append(f"{sel}{{{dentro}}}")
                i = k; continue
            k = t.find("}", j)
            if ".ct-" in sel:
                out.append(",".join(f"html body.gt-interna.gt-interna {s.strip()}" for s in sel.split(",")) + t[j:k + 1])
            i = k + 1
    return bloque(c)
_pl = (C / "plagas/cucarachas/index.html").read_text(encoding="utf-8")
CIERRE_INTERNO = re.search(r'<section id="contacto" class="s-closing">.*?</section>', _pl, re.S).group(0).replace('/oficinas/costa-rica/#consulta"', '/oficinas/costa-rica/#contacto"')
for f in C.rglob("index.html"):
    rel = str(f.parent.relative_to(C)).replace("\\", "/")
    if rel in (".", "servicios/hogares", "servicios/comercios"): continue
    t = f.read_text(encoding="utf-8")
    m = re.search(r"<main\b.*?</main>", t, re.S).group(0)
    m = m.replace('/oficinas/costa-rica/#consulta"', '/oficinas/costa-rica/#contacto"')   # la portada nueva cierra con #contacto
    mas = ""
    if rel == "servicios/industria":   # mismo sector que Comercios: las fotos reales de globaltni y su hoja de estilos
        for viejo, gt in (("cr-sector4-industria-almacen.webp", "industrial-storage.png"), ("cr-sector4-industria-lab.webp", "industrial-laboratory.png"),
                          ("cr-sector4-industria-planta.webp", "industrial-operations.png")):
            assert f"{A}{viejo}" in m, viejo; m = m.replace(f"{A}{viejo}", f"{G}en/services/media/{gt}")
        m, n = re.subn(r'(cr-industria-unsplash-[^"]*" alt=")Industria"', r'\1Personal caminando por el pasillo de una bodega con estanterías"', m)
        assert n == 1, "industria: foto de arriba"
        mas = f'<link rel="stylesheet" href="{G}a/commercial-editorial.css"/><style>{css_reforzado(GT / "a/commercial-editorial.css")}{css_reforzado(GT / "a/brand-2026.css")}{(R / "plantilla/ajuste-industria.css").read_text(encoding="utf-8")}</style>'
    # «Proteja su casa o su negocio»: dos enlaces sueltos → dos filas con texto y flecha, como el menú de globaltni
    m = m.replace(f'<ul class="s-enlaces"><li><a href="{B}servicios/hogares/">Hogares</a></li><li><a href="{B}servicios/comercios/">Comercios</a></li></ul>',
                  f'<div class="gt-destinos"><a href="{B}servicios/hogares/"><strong>Hogares</strong><span>Un programa para toda su casa, en tres zonas.</span><i aria-hidden="true">→</i></a>'
                  f'<a href="{B}servicios/comercios/"><strong>Comercios</strong><span>Protección para los retos de cada sector.</span><i aria-hidden="true">→</i></a></div>')
    if rel == "blog":   # el blog cerraba con el formulario viejo y el chat abierto en línea: mismo cierre que las demás internas
        i = m.find('<section id="contacto" class="section local-consult'); assert i > 0, "blog: cierre viejo"
        m = m[:i] + CIERRE_INTERNO + "</main>"
    estilo = "".join(re.findall(r"<style>.*?</style>", t[t.find("<head>"):t.find("</head>")], re.S))
    extra = "".join(re.findall(r'<script src="/oficinas/assets/pestanas\.js" defer></script>', t))
    # el molde viejo agrega 64 px vacíos tras cada sección; en computadora el espacio sale doble con el CSS de globaltni
    # (en celular se queda: la receta lo pide para que el globo del chat no tape enlaces)
    estilo += "<style>body.gt-interna .gt-destinos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px;margin-top:24px;border-top:1px solid #dddcd3}body.gt-interna .gt-destinos a{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 16px;align-items:center;padding:22px 0;border-bottom:1px solid #dddcd3;color:#010007;text-decoration:none;min-height:44px}body.gt-interna .gt-destinos strong{font:700 22px/1.2 Montserrat,system-ui,sans-serif}body.gt-interna .gt-destinos span{grid-column:1;color:#4c4c4c;font-size:16px;line-height:1.5;text-align:left}body.gt-interna .gt-destinos i{grid-column:2;grid-row:1/span 2;font-style:normal;font-size:22px;transition:transform .2s}body.gt-interna .gt-destinos a:hover i{transform:translateX(4px)}@media(max-width:760px){body.gt-interna .gt-destinos{grid-template-columns:minmax(0,1fr)}}</style>"
    estilo += "<style>@media(min-width:761px){body.gt-interna main>:is(section,article,div,nav)::after{content:none!important;display:none!important}}body.gt-interna main>section.section{width:min(1312px,100% - 128px);margin-inline:auto}body.gt-interna main>section.s-intro>figure.s-figure{width:min(100%,760px)!important;max-width:100%!important;margin:28px 0 0!important}body.gt-interna main>section.s-intro>figure.s-figure img{border-radius:6px}@media(max-width:760px){body.gt-interna main>section.section{width:calc(100% - 44px)}}</style>"
    out = pagina(RES, t, m, "country-site gt-interna", estilo + extra + mas)
    out = out.replace("<body", '<body data-oficina="costa-rica"', 1)
    f.write_text(out, encoding="utf-8"); hechas += 1
print("réplica de globaltni: portada, hogares y comercios copiados;", hechas, "páginas con el encabezado y el pie de globaltni")

# ---------- 6 · texto: los calcos y errores de los textos de globaltni se corrigen al copiarlos (revisión del 4-nov-2026) ----------
# Cada par debe aparecer en alguna página; si no aparece, el script falla (nada se calla). El marcado no cambia.
CORR = [
    # portada
    ('alt="El auto emblemático de Truly Nolen"', 'alt="El carro emblemático de Truly Nolen"'),
    ("<span>nuestro auto emblemático</span>", "<span>nuestro carro emblemático</span>"),
    ('alt="El automóvil amarillo con orejas de ratón de Truly Nolen"', 'alt="El carro amarillo con orejas de ratón de Truly Nolen"'),
    ("jardines y un coche amarillo de servicio", "jardines y un carro amarillo de servicio"),
    ("<strong><bdi>65</bdi> <small>países</small>", "<strong><bdi>65+</bdi> <small>países</small>"),
    ("turismo, educación, fabricación y catering, entre muchos otros sectores", "turismo, educación, manufactura y servicios de alimentación para eventos, entre muchos otros sectores"),
    ("Un programa de Manejo Integrado de Plagas con trazabilidad", "Un programa de manejo integrado de plagas con trazabilidad"),
    ("aspectos regulatorios y soporte de auditoría.", "aspectos normativos y apoyo en auditorías."),
    ("cada cliente, especialmente instalaciones auditadas.", "cada cliente, especialmente para instalaciones auditadas."),
    ("<h2>Una red internacional. <br/>", "<h2>Presencia mundial. <br/>"),
    ("el servicio y el programa adecuado para su espacio.", "el servicio y el programa adecuados para su espacio."),
    ("<h3>Conecte con una oficina local.</h3>", "<h3>Comuníquese con una oficina local.</h3>"),
    ("Nuestra historia hasta ahora <span", "Conozca nuestra historia <span"),
    ("<summary>Conecte con nosotros</summary>", "<summary>Comuníquese con nosotros</summary>"),
    # hogares (el texto de globaltni sale dos veces en la página, igual que en el original)
    ("<p>Con el fin de brindar el servicio de control de plagas más efectivo posible, TNI ofrece un Programa de Protocolo de 3 zonas. La inspección y el tratamiento se realizará en toda la casa.</p>",
     "<p>Para brindar el control de plagas más eficaz posible, TNI ofrece un protocolo de tres zonas. La inspección y el tratamiento abarcan toda la casa.</p>"),
    ("<p>La propiedad se dividirá en tres zonas:</p>", "<p>La propiedad se divide en tres zonas:</p>"),
    ("<p>– La zona roja (Interior de la casa)</p>", "<p>– La zona roja (el interior de la casa).</p>"),
    ("<p>– La zona amarilla (perímetro inmediato de la casa)</p>", "<p>– La zona amarilla (el perímetro inmediato de la casa).</p>"),
    ("<p>– La zona verde (Las áreas verdes, como césped, macizos de flores).</p>", "<p>– La zona verde (las áreas verdes, como el césped y los macizos de flores).</p>"),
    ("<p>En cada una de estas áreas, Truly Nolen International implementará los protocolos correctos. Esto proporcionará al cliente una solución única a sus problemas de plagas.</p>",
     "<p>En cada zona, Truly Nolen International aplica el protocolo que corresponde. Así, el cliente recibe una solución completa para sus problemas de plagas.</p>"),
    ("<p>¿Interesado? Haga clic en el enlace de abajo para contactarnos y recibir más información.</p>", "<p>¿Le interesa? Escríbanos con el botón de abajo y le daremos más información.</p>"),
    ("<h2>Hable con su oficina local.</h2><p>Encuentre el equipo que atiende su zona o consulte a Truly Nolen International.</p>",
     "<h2>Hable con nuestro equipo en Costa Rica.</h2><p>Cuéntenos qué necesita y le orientamos en el siguiente paso.</p>"),
    ("data-abrir-chat>Encontrar una oficina →</a>", "data-abrir-chat>Escribir a Truly AI →</a>"),
    ('<a class="text-link" href="#contacto" data-abrir-chat>Solicitar un servicio →</a>', f'<a class="text-link" href="{WA}"{EXT}>Escribir por WhatsApp →</a>'),
    ('<a class="text-link" href="https://globaltni.com/es/franchise/join/" target="_blank" rel="noopener">Conocer las franquicias →</a>',   # sin franquicia en una oficina (vuelta 9)
     f'<a class="text-link" href="{GTX}offices/"{EXT}>Ver la red internacional →</a>'),
    ("data-abrir-chat>Contacto internacional →</a>", "data-abrir-chat>Hacer una consulta →</a>"),
    # comercios
    ("Su industria.<br/>Su mundo, protegido.", "Su sector,<br/>protegido."),
    ("Truly Nolen International ofrece sus servicios de control de plagas para clientes de todo el mundo en una gran variedad de sectores. A continuación, encontrará cuatro sectores clave en los que tenemos una gran presencia en cuanto al servicio comercial de control de plagas</p>",
     "Truly Nolen International ofrece control de plagas a clientes de todo el mundo y en sectores muy variados. Estos son cuatro sectores clave en los que tiene más presencia.</p>"),
    (">Encuentre su oficina<span", ">Hable con nosotros<span"),
    ("Los profesionales sanitarios que dirigen instalaciones de atención medica a largo plazo, centros de atención médica de emergencia e instalaciones de rehabilitación física o mental, enfrentan muchos desafíos para garantizar que se cumpla con el nivel más alto de saneamiento mientras atienden a grupos vulnerables de la población.",
     "Quienes dirigen centros de atención prolongada, servicios de emergencias y centros de rehabilitación física o mental deben mantener el más alto nivel de higiene mientras atienden a personas vulnerables."),
    ("instalaciones de atención médica donde los servicios deben ir más allá del control.", "instalaciones de atención médica en las que el servicio debe ir más allá del control."),
    ("cumple con toda la documentación y registros requeridos", "cumple con toda la documentación y los registros requeridos"),
    ("las normas regulatorias de la industria y / o los requisitos", "las normas del sector o los requisitos"),
    ("¿Quién se beneficia con este programa?", "¿Quién se beneficia de este programa?"),
    (">Centros de asistencia prolongada.<", ">Centros de atención prolongada<"),
    (">Instalaciones de atención / tratamiento de pacientes<", ">Instalaciones de atención y tratamiento de pacientes<"),
    (">Suministros médicos / Almacenes<", ">Suministros médicos y almacenes<"),
    (">Almacenamiento y distribución de alimentos.<", ">Almacenamiento y distribución de alimentos<"),
    (">Envasado y re envasado de alimentos<", ">Envasado y reenvasado de alimentos<"),
    (">Catering<", ">Servicios de alimentación para eventos<"),
    ("Servicios de alimentación y hospitalidad.", "Servicios de alimentación y hotelería."),
    ("Las instalaciones de venta minorista de alimentos se encuentran entre las más difíciles en cuanto al desarrollo de estrategias de saneamiento y manejo de plagas. Es primordial garantizar que suministren productos seguros en un entorno limpio y libre de plagas.",
     "En la venta minorista de alimentos, diseñar estrategias de higiene y manejo de plagas es especialmente difícil. Es primordial ofrecer productos seguros en un entorno limpio."),
    ("servicios que van más allá de solamente control.", "servicios que van más allá del simple control."),
    ("servicios que van más allá de solamente el control.", "servicios que van más allá del simple control."),
    ("Cualquier corporación que se involucre en la logística del traslado diario de bienes y servicios. Ya sea que exporte o importe de diferentes países o transfiera productos de un lugar a otro, Truly Nolen International está aquí para asegurarse de que no tenga ninguna contaminación por plagas.",
     "Para cualquier empresa que se encargue del traslado diario de mercadería, ya sea que exporte, importe o mueva productos de un lugar a otro, Truly Nolen International ayuda a evitar la contaminación por plagas."),
    ("fue desarrollado para corporaciones que requieren", "se desarrolló para empresas que requieren"),
    (">Campos de Logística<", ">Centros logísticos<"),
    ("Si usted no se encuentra dentro de estos sectores, ¡no se preocupe! Truly Nolen International también tiene clientes en turismo, educación, fabricación, catering y mucho más.",
     "Si su actividad no está entre estos sectores, no se preocupe: Truly Nolen International también tiene clientes en turismo, educación, manufactura, servicios de alimentación para eventos y mucho más."),
    ("Contáctenos para obtener más información accediendo al siguiente enlace.", "Escríbanos y le daremos más información."),
    (">Contactar a TNI<span", ">Escribir a Truly AI<span"),
    ("<p>Encuentre el equipo de su país para conversar sobre sus instalaciones y el servicio que necesita.</p>", "<p>Converse con nuestro equipo en Costa Rica sobre sus instalaciones y el servicio que necesita.</p>"),
    ("<h2>Más formas de proteger su mundo.</h2>", "<h2>Más formas de proteger su negocio.</h2>"),
]
textos = {f: f.read_text(encoding="utf-8") for f in C.rglob("index.html")}
faltan = []
for a, b in CORR:
    n = 0
    for f, t in textos.items():
        if a in t: n += t.count(a); textos[f] = t.replace(a, b)
    if not n: faltan.append(a[:70])
for f, t in textos.items(): f.write_text(t, encoding="utf-8")
assert not faltan, "textos de globaltni no encontrados: " + " | ".join(faltan)
print("texto:", len(CORR), "correcciones de estilo aplicadas")

# ---------- 7 · listas de sectores: guiones suaves en las palabras largas (en celular globaltni las parte a mitad de palabra) ----------
SILABAS = {"Almacenamiento": "Almace&shy;namiento", "almacenamiento": "almace&shy;namiento", "Supermercados": "Super&shy;mercados",
           "procesamiento": "procesa&shy;miento", "farmacéuticos": "farma&shy;céuticos", "reenvasado": "reen&shy;vasado",
           "alimentación": "alimen&shy;tación", "distribución": "distri&shy;bución", "alimentaria": "alimen&shy;taria",
           "Hipermercados": "Hiper&shy;mercados", "transportistas": "transpor&shy;tistas", "rehabilitación": "rehabili&shy;tación",
           "Instalaciones": "Instala&shy;ciones", "adquisiciones": "adquisi&shy;ciones", "Laboratorios": "Labora&shy;torios"}
def con_silabas(t):
    def lista(m):
        x = m.group(0)
        for a, b in SILABAS.items(): x = re.sub(rf"(?<=[\s>]){a}(?=[\s<,.])", b, x)
        return x
    return re.sub(r'<aside[^>]*class="ct-facilities".*?</aside>', lista, t, flags=re.S)
n = 0
for f in C.rglob("index.html"):
    t = f.read_text(encoding="utf-8"); t2 = con_silabas(t)
    if t2 != t: f.write_text(t2, encoding="utf-8"); n += 1
print("listas de sectores con guiones suaves en", n, "páginas")
