"""Páginas internas como globaltni.com/en (paquete de alumnos, 3-nov-2026): se corre DESPUÉS de generar.py.

Reconstruye servicios, plagas, artículos y páginas legales con las mismas clases del master (s-intro, s-lead-pair,
s-flow, pest-*, article-body, s-closing) y en PROSA: nada de tablas, franjas de cifras ni tarjetas del molde viejo.
Todo sale de la ficha y del HTML ya generado (preguntas, fuentes, imágenes); no se inventa texto.
Uso: uv run --python 3.12 python master.py
"""
import html, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent
F = json.loads((RAIZ / "ficha" / "costa-rica.json").read_text(encoding="utf-8"))
CARPETA = RAIZ / "sitio" / "oficinas" / F["id"]
BASE = f"/oficinas/{F['id']}/"
e = lambda s: html.escape(s or "", quote=True)
COLOR = ["rojo", "amarillo", "verde"]


def plano(s):
    """Texto de la ficha sin <br/> ni etiquetas, en una línea."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def tit(s):
    """Titulo de la ficha escapado, conservando sus <br/> (el gate compara el dato completo)."""
    return "<br/>".join(e(re.sub(r"<[^>]+>", " ", x).strip()) for x in re.split(r"<br\s*/?>", s or ""))


def fin(s):
    s = s.strip()
    return s if s[-1:] in ".?!:…»" else s + "."


def titulos(clase):
    return {x["slug"]: x["titulo"] for x in F["paginas"][clase]}


def parrafos(b):
    """Un bloque de la ficha como prosa."""
    out, tipo = [], b.get("tipo")
    if b.get("texto"):
        out.append(f"<p>{e(b['texto'])}</p>")
    if tipo == "cifras":
        for c in b.get("items", []):
            out.append(f"<p><strong>{e(c['valor'])}</strong> {e(c['texto'])}"
                       + (f" <small class=\"s-fuente\">{e(c['fuente'])}</small>" if c.get("fuente") else "") + "</p>")
    elif tipo == "tarjetas":
        for it in b.get("items", []):
            out.append(f"<p><strong>{e(fin(it['h']))}</strong> {e(it['p'])}</p>")
            if it.get("checks"):
                out.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in it["checks"]) + "</ul>")
    elif tipo == "tabla":
        zona = "zona" in (b.get("eyebrow", "") + b.get("titulo", "")).lower()
        for i, f in enumerate(b.get("filas", [])):
            cab = f[0] if isinstance(f[0], list) else [f[0]]
            det = f[1] if len(f) > 1 and isinstance(f[1], list) else [x for x in f[1:] if isinstance(x, str)]
            tt = re.sub(r"^\d+\s*·\s*", "", cab[0])
            breve = " ".join(fin(x) for x in cab[1:])
            cls = f' class="s-zona s-zona-{COLOR[i % 3]}"' if zona else ""
            if len(det) >= 2 and re.match(r"^arts?\.\s", det[-1].strip()):   # la cita del artículo va pegada a su frase
                det = det[:-2] + [det[-2].rstrip(". ") + f" ({det[-1].strip()})."]
            if len(det) >= 2:
                out.append(f"<p{cls}><strong>{e(fin(tt))}</strong> {e(breve)}</p><ul>" + "".join(f"<li>{e(x)}</li>" for x in det) + "</ul>")
            else:
                out.append(f"<p{cls}><strong>{e(fin(tt))}</strong> {e(' '.join([breve] + [fin(x) for x in det]).strip())}</p>")
    elif tipo == "relacionadas":
        clase = b.get("lista", "plagas")
        ts = titulos(clase)
        li = "".join(f'<li><a href="{BASE}{clase}/{s}/">{e(ts[s])}</a></li>' for s in b.get("slugs", []) if s in ts and (CARPETA / clase / s / "index.html").exists())
        if li:
            out.append(f'<ul class="s-enlaces">{li}</ul>')
    elif tipo in ("consulta", "sectores"):
        return []
    if b.get("nota"):
        out.append(f'<p class="s-note">{e(b["nota"])}</p>')
    return out


def tomar(rx, t, g=0):
    m = re.search(rx, t, re.S)
    return m.group(g) if m else ""


def preguntas(t):
    fq = tomar(r'<section class="section faq">.*?</section>', t)
    if not fq:
        return ""
    tit = tomar(r"<h2>(.*?)</h2>", fq, 1)
    qa = re.findall(r"<summary>(.*?)<span.*?</summary>\s*<p>(.*?)</p>", fq, re.S)
    det = "".join(f'<details class="ux-answer"><summary><h3>{q}</h3></summary><article><p>{a}</p></article></details>' for q, a in qa)
    return f'<section class="wrap s-section s-preguntas"><h2>{tit}</h2><div class="s-prose">{det}</div></section>' if det else ""


def fuentes(t):
    fs = tomar(r'<section class="section detail-sources">.*?</section>', t)
    if not fs:
        return ""
    tit = tomar(r"<h2>(.*?)</h2>", fs, 1)
    nota = tomar(r'<p class="nota"[^>]*>(.*?)</p>', fs, 1)
    ol = tomar(r"<ol>.*?</ol>", fs)
    return f'<section class="wrap s-section s-fuentes"><h2>{tit}</h2>' + (f'<p class="s-note">{nota}</p>' if nota else "") + ol + "</section>"


def cierre():
    """Cierre del master: banda amarilla con título, una línea y tres salidas (chat, WhatsApp, cobertura)."""
    T = F.get("textos", {})
    wa = F.get("whatsappTrulyAI", "15202145675")
    return ('<section id="contacto" class="s-closing"><div class="wrap"><h2>Cuéntenos qué necesita proteger.</h2>'
            "<p>Escríbale a Truly AI aquí mismo o por WhatsApp y le orienta en el siguiente paso.</p>"
            '<div class="s-closing-actions"><a class="button button-dark" href="#contacto" data-abrir-chat>Escribir en el chat</a>'
            f'<a class="text-link" href="https://wa.me/{e(str(wa))}" target="_blank" rel="noopener noreferrer">Escribir por WhatsApp</a>'
            f'<a class="text-link" href="{BASE}#consulta">Consultar cobertura →</a></div></div></section>')


def miga(items):
    return '<nav aria-label="Ruta">' + '<span aria-hidden="true">/</span>'.join(items) + "</nav>"


def poner_main(t, main):
    return re.sub(r'<main id="contenido">.*?</main>', lambda _: '<main id="contenido">' + main + "</main>", t, count=1, flags=re.S)


INICIO = f'<a href="{BASE}">Inicio</a>'
CIERRE = cierre()
hechas = []

# ---------- servicios ----------
for pg in F["paginas"]["servicios"]:
    f = CARPETA / "servicios" / pg["slug"] / "index.html"
    if not f.exists():
        continue
    t = f.read_text(encoding="utf-8")
    hero = tomar(r'<section class="section detail-hero">.*?</section>', t)
    img = tomar(r"<img [^>]*/?>", hero)
    bl = [b for b in pg.get("bloques", []) if b.get("tipo") != "consulta"]
    p0 = parrafos(bl[0]) if bl else []
    nombre = re.sub(r"\s*·.*$", "", pg.get("eyebrow", pg["titulo"]))
    main = (f'<section class="wrap s-intro">{miga([INICIO, "Servicios", e(pg["titulo"])])}<h1>{e(pg["titulo"])}</h1></section>'
            f'<section class="wrap s-section s-lead-pair"><article class="s-prose"><h2>{tit(pg.get("lema", pg["titulo"]))}</h2></article>'
            f'<article class="s-prose"><p>{e(pg.get("intro", ""))}</p>{"".join(p0)}</article>'
            + (f'<figure class="s-figure">{img}</figure>' if img else "")
            + f'<a class="button s-service-action" href="#contacto" data-abrir-chat>Consultar por este servicio →</a></section>')
    for b in bl[1:]:
        ps = parrafos(b)
        if ps:
            main += f'<section class="wrap s-section s-flow"><h2>{tit(b.get("titulo", ""))}</h2><article class="s-prose">{"".join(ps)}</article></section>'
    main += preguntas(t) + fuentes(t) + CIERRE
    main = re.sub(r"\((arts?\.[^()<]{1,14})\)", lambda m: "(" + m.group(1).replace(" ", "&nbsp;") + ")", main)   # «(art. 6)» sin partirse
    f.write_text(poner_main(t, main), encoding="utf-8"); hechas.append(f"servicios/{pg['slug']}")

# ---------- plagas ----------
publicadas = [p for p in F["paginas"]["plagas"] if (CARPETA / "plagas" / p["slug"] / "index.html").exists()]
for pg in publicadas:
    f = CARPETA / "plagas" / pg["slug"] / "index.html"
    t = f.read_text(encoding="utf-8")
    hero = tomar(r'<section class="section detail-hero">.*?</section>', t)
    img = tomar(r"<img [^>]*/?>", hero)
    fam = "".join(f'<a href="{BASE}plagas/{p["slug"]}/"' + (' aria-current="page"' if p is pg else "") + f">{e(p['titulo'])}</a>" for p in publicadas)
    secs, idx, n = [], [], 0
    for b in pg.get("bloques", []):
        ps = parrafos(b)
        if not ps:
            continue
        n += 1
        tt = plano(b.get("titulo", ""))
        secs.append(f'<section class="pest-copy" id="guia-{n}"><h2 id="guia-{n}-title">{tit(b.get("titulo", ""))}</h2>{"".join(ps)}</section>')
        idx.append(f'<li><a href="#guia-{n}">{e(tt)}</a></li>')
    main = (f'<div class="wrap pest-wrap"><nav class="pest-breadcrumb" aria-label="Ruta">{INICIO}<span aria-hidden="true">/</span><span>Guía de plagas</span>'
            f'<span aria-hidden="true">/</span><span>{e(pg["titulo"])}</span></nav>'
            f'<header class="pest-masthead"><div><p class="pest-eyebrow">Guía de plagas</p><h1>{e(pg["titulo"])}</h1><p class="pest-lead">{e(pg.get("intro", ""))}</p>'
            f'<div class="pest-hero-actions"><a class="button" href="#contacto" data-abrir-chat>Pedir ayuda →</a><a class="text-link" href="#guia-1">Explorar esta guía ↓</a></div></div>'
            + (f'<figure class="pest-figure pest-hero-figure">{img}</figure>' if img else "") + "</header>"
            f'<nav class="pest-families" aria-label="Guía de plagas">{fam}</nav>'
            f'<div class="pest-layout"><aside class="pest-sidebar"><details class="pest-index" id="reading-index"><summary>En esta página <span>−</span></summary><ol>{"".join(idx)}</ol></details></aside>'
            f'<div class="pest-content">{"".join(secs)}</div></div></div>' + preguntas(t) + fuentes(t) + CIERRE)
    f.write_text(poner_main(t, main), encoding="utf-8"); hechas.append(f"plagas/{pg['slug']}")

# ---------- artículos ----------
for f in sorted((CARPETA / "blog").glob("*/index.html")):
    t = f.read_text(encoding="utf-8")
    a = tomar(r'<article class="section blog-articulo">.*?<div class="blog-cuerpo">.*?</div></article>', t)
    if not a:
        continue
    tema, h1 = tomar(r'<p class="eyebrow">(.*?)</p>', a, 1), tomar(r"<h1>(.*?)</h1>", a, 1)
    entrada, meta = tomar(r'<p class="blog-entrada">(.*?)</p>', a, 1), tomar(r'<p class="blog-meta">(.*?)</p>', a, 1)
    im = re.search(r'<img class="blog-portada" src="([^"]*)" alt="([^"]*)"', a)
    cuerpo = tomar(r'<div class="blog-cuerpo">(.*)</div></article>', a, 1)
    k = iter(range(1, 99))
    cuerpo = re.sub(r"<h2>", lambda m: f'<h2 id="art-{next(k)}">', cuerpo)
    idx = "".join(f'<li><a href="#art-{i}">{h}</a></li>' for i, h in enumerate(re.findall(r'<h2 id="art-\d+">(.*?)</h2>', cuerpo, re.S), 1))
    fq = tomar(r'<section class="section faq">.*?</section>', t)
    if fq:
        qa = re.findall(r"<summary>(.*?)<span.*?</summary>\s*<p>(.*?)</p>", fq, re.S)
        if qa:
            cuerpo += f'<h2 class="sin-num">{tomar(r"<h2>(.*?)</h2>", fq, 1)}</h2><div class="s-prose">' + "".join(
                f'<details class="ux-answer"><summary><h3>{q}</h3></summary><article><p>{r}</p></article></details>' for q, r in qa) + "</div>"
    rels = re.findall(r'<article class="blog-card">.*?<h2><a href="([^"]+)">(.*?)</a></h2>', t, re.S)
    otros = "".join(f'<li><a href="{h}">{x}</a></li>' for h, x in rels[1:])
    sig = (f'<section class="wrap closeout-blog-next"><div><p class="closeout-blog-eyebrow">Seguir leyendo</p><h2>{rels[0][1]}</h2>'
           f'<a class="text-link" href="{rels[0][0]}">Leer el artículo →</a>' + (f'<ul class="s-enlaces closeout-otros">{otros}</ul>' if otros else "")
           + f'</div><a class="text-link" href="{BASE}blog/">Ver todos los artículos →</a></section>') if rels else ""
    fig = f'<figure class="s-figure"><img src="{im.group(1)}" alt="{im.group(2)}"/><figcaption>{im.group(2)}</figcaption></figure>' if im else ""
    main = (f'<section class="wrap s-intro">{miga([INICIO, f"<a href=\"{BASE}blog/\">Blog</a>", tema])}<h1>{h1}</h1>{fig}</section>'
            f'<section class="wrap s-section s-prose"><p class="s-note">{meta}</p><p class="s-entrada">{entrada}</p></section>'
            f'<nav class="wrap s-index ux-index" aria-label="En este artículo"><details><summary>En este artículo</summary><ul>{idx}</ul></details></nav>'
            f'<section class="wrap s-section s-article"><div class="article-body">{cuerpo}</div></section>' + fuentes(t) + sig + CIERRE)
    f.write_text(poner_main(t, main), encoding="utf-8"); hechas.append("blog/" + f.parent.name)

# ---------- legales ----------
for nombre in ("privacidad", "terminos", "accesibilidad"):
    f = CARPETA / nombre / "index.html"
    if not f.exists():
        continue
    t = f.read_text(encoding="utf-8")
    lc = tomar(r'<section class="section legal-content">.*?</section>', t)
    if not lc:
        continue
    h1 = tomar(r"<h1>(.*?)</h1>", lc, 1)
    cuerpo = re.sub(r'<p class="eyebrow">.*?</p>|<h1>.*?</h1>|<a class="button"[^>]*>.*?</a>', "", lc[lc.index(">") + 1:lc.rindex("</section>")], flags=re.S)
    main = f'<section class="wrap s-intro">{miga([INICIO, h1])}<h1>{h1}</h1></section><section class="wrap s-section s-prose">{cuerpo}</section>' + CIERRE
    f.write_text(poner_main(t, main), encoding="utf-8"); hechas.append(nombre)

# ---------- portada: hero del master (botón con marca, línea premium y tres rutas) ----------
fp = CARPETA / "index.html"
t = fp.read_text(encoding="utf-8")
if 'class="hero-routes"' not in t:
    t = t.replace('<section class="section g g-zonas"', '<section id="residencial" class="section g g-zonas"', 1)
    t = t.replace('<section class="section g g-comercial"', '<section id="comercial" class="section g g-comercial"', 1)
    marca = ('<span class="office-mark" aria-hidden="true"><svg viewBox="0 0 24 28"><path d="M12 25S3 17 3 10a9 9 0 1 1 18 0c0 7-9 15-9 15Z"></path>'
             '<circle cx="12" cy="10" r="3"></circle></svg></span>')
    m = re.search(r'(<div class="hero-text">.*?<a class="button"[^>]*>)(.*?)(</a>)(</div>)\s*<a class="discover"[^>]*>.*?</a>', t, re.S)
    if m:
        rutas = ('<div class="hero-routes" aria-label="Explore nuestros servicios"><a href="#residencial">Su hogar <span aria-hidden="true">↓</span></a>'
                 '<a href="#comercial">Su negocio <span aria-hidden="true">↓</span></a><a href="#teps">Programa TEPS <span aria-hidden="true">↓</span></a></div>')
        t = t.replace(m.group(0), m.group(1) + m.group(2) + " " + marca + m.group(3)
                      + '<span class="hero-premium">Servicio premium · Visión internacional</span>' + m.group(4) + rutas, 1)
        hechas.append("portada (hero)")
    fp.write_text(t, encoding="utf-8")

# ---------- técnica en el cierre amarillo de todas las páginas internas (como el técnico del master) ----------
foto = F["fotos"].get("nosotros", {})
if foto.get("file"):
    fig = (f'<figure class="s-closing-figure"><img src="{BASE}assets/{foto["file"]}" alt="{e(foto.get("alt", ""))}" loading="lazy"/></figure>')
    for f in CARPETA.rglob("index.html"):
        t = f.read_text(encoding="utf-8")
        if 's-closing"><div class="wrap">' in t and 'class="s-closing-figure"' not in t:
            t = t.replace('<div class="s-closing-actions">', '<div class="s-closing-actions">', 1)
            t = re.sub(r'(<section id="contacto" class="s-closing"><div class="wrap">)(.*?</div>)(</div></section>)',
                       lambda m: m.group(1) + '<div class="s-closing-text">' + m.group(2) + "</div>" + fig + m.group(3), t, count=1, flags=re.S)
            f.write_text(t, encoding="utf-8")

print(f"{len(hechas)} páginas con la estructura del master:", ", ".join(hechas))
