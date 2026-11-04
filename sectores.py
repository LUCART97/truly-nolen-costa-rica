"""Sectores de globaltni en Comercios e Industria (receta truly-inbound, paso 6c, 4-nov-2026). Se corre después de corporativo.py.
- Comercios: el bloque «sectores» de la ficha (4 sectores de https://globaltni.com/es/services/commercial/) va con el marcado ct-* del
  master (franja amarilla «Encuentre su sector», Salud en negro, alimentos en gris, logística con la línea amarilla, «Volver a los
  sectores ↑», «Cada industria merece atención.» y «Más formas de proteger su mundo.») después del primer bloque (la entrada).
- Industria: el mismo bloque con un solo sector, sin índice.
- Portada: las filas de «Comercio e industria» salen del bloque y bajan cada una a SU ancla (#sector-<id>); Industrias va a su página.
- CSS = plantilla/ct-commercial.css (commercial-editorial.css + reglas .ct-* de brand-2026.css de globaltni), incrustado en la página."""
import json, re, html, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent
F = json.loads((RAIZ / "ficha/costa-rica.json").read_text(encoding="utf-8"))
e = lambda s: html.escape(s or "", quote=True)
BASE = f"/oficinas/{F['id']}/"
A = f"{BASE}assets/"
CT_CSS = (RAIZ / "plantilla/ct-commercial.css").read_text(encoding="utf-8")
CLASE = {"salud": "ct-healthcare", "industria": "ct-industrial", "alimentos": "ct-food-processing", "carga": "ct-logistics"}
CARPETA = RAIZ / "sitio/oficinas" / F["id"]
ext = ' target="_blank" rel="noopener noreferrer"'
TEPS_URL = "https://globaltni.com/es/services/teps/"
MAS = {"Servicios residenciales": f"{BASE}servicios/hogares/", "Sanitización": f"{BASE}#sanitizacion", "Programa TEPS": f"{BASE}#teps"}


def resumen(s):
    """Fila de la portada: los primeros tres de «¿Quién se beneficia?» en una frase."""
    k = s.get("portada", [0, 1, 2])
    x = [s["benef"][k[0]]] + [s["benef"][i][0].lower() + s["benef"][i][1:] for i in k[1:]]
    return ", ".join(x[:-1]) + " y " + x[-1] + "."


def sector(b, s, indice):
    idd = f"sector-{s['id']}"
    figs = "".join(f'<figure><img src="{A}{x["imagen"]}" alt="{e(x["pie"])}" loading="lazy"/><figcaption>{e(x["pie"])}</figcaption></figure>' for x in s["fotos"])
    prosa = "".join(f"<p>{e(p)}</p>" for p in s["textos"])
    prosa += f'<a class="ct-link" href="{TEPS_URL}"{ext}>{e(s["teps"])}<span aria-hidden="true">→</span></a>'
    benef = "".join(f"<li>{e(x)}</li>" for x in s["benef"])
    volver = f' <a class="ct-back" href="#indice">{e(b["volver"])} <span aria-hidden="true">↑</span></a>' if indice else ""
    return (f'<section aria-labelledby="{idd}-title" class="ct-sector {CLASE[s["id"]]}" id="{idd}"><div class="ct-wrap">'
            f'<header class="ct-sector-heading"><p class="ct-kicker">{e(s["nombre"])}</p><h2 id="{idd}-title">{e(s["titulo"])}</h2></header>'
            f'<div class="ct-sector-layout"><div class="ct-documentary">{figs}</div><div class="ct-prose">{prosa}</div>'
            f'<aside aria-labelledby="{idd}-title {idd}-facilities" class="ct-facilities"><h3 id="{idd}-facilities">{e(b["benefTitulo"])}</h3><ul>{benef}</ul>'
            f'<button type="button" class="ct-link" data-abrir-chat>{e(b["contacto"])}<span aria-hidden="true">→</span></button></aside></div>{volver}</div></section>')


def bloque_html(b):
    """Devuelve (sectores, cierre): el cierre va al final de la página, como en el master."""
    indice = bool(b.get("indiceTitulo"))
    out = '<div class="ct-commercial">'
    if b.get("titulo"):
        out += (f'<section class="ct-wrap s-section ct-entrada"><p class="ct-kicker">{e(b["eyebrow"])}</p><h2>{e(b["titulo"])}</h2>'
                + (f'<p class="ct-intro">{e(b["texto"])}</p>' if b.get("texto") else "") + "</section>")
    if indice:
        nav = "".join(f'<a href="#sector-{s["id"]}">{e(s["nombre"])}<span aria-hidden="true">↓</span></a>' for s in b["sectores"])
        out += f'<nav aria-label="{e(b["indiceTitulo"])}" class="ct-sector-nav" id="indice"><div class="ct-wrap"><span>{e(b["indiceTitulo"])}</span><div>{nav}</div></div></nav>'
    out += "".join(sector(b, s, indice) for s in b["sectores"])
    if b.get("cierre"):   # «Cada industria merece atención.» cierra los sectores, como en el master
        t, tx, bt = b["cierre"]
        out += (f'<section class="ct-other ct-wrap"><h2>{e(t)}</h2><div><p>{e(b.get("otros", ""))}</p><p>{e(tx)}</p>'
                f'<button type="button" class="ct-link" data-abrir-chat>{e(bt)}<span aria-hidden="true">→</span></button></div></section>')
    out += "</div>"
    fin = '<div class="ct-commercial">'
    if False:
        t, tx, bt = b["cierre"]
        fin += (f'<section class="ct-other ct-wrap"><h2>{e(t)}</h2><div><p>{e(b.get("otros", ""))}</p><p>{e(tx)}</p>'
                f'<button type="button" class="ct-link" data-abrir-chat>{e(bt)}<span aria-hidden="true">→</span></button></div></section>')
    if b.get("mas"):
        t, links = b["mas"]
        fin += (f'<section class="ct-related ct-wrap"><h2>{e(t)}</h2><div>'
                + "".join(f'<a class="ct-link" href="{MAS[x]}">{e(x)}<span aria-hidden="true">→</span></a>' for x in links) + "</div></section>")
    return out, (fin + "</div>" if fin != '<div class="ct-commercial">' else "")


hechas = []
for slug in ("comercios", "industria"):
    pg = next(x for x in F["paginas"]["servicios"] if x["slug"] == slug)
    b = next((x for x in pg["bloques"] if x.get("tipo") == "sectores"), None)
    if not b:
        continue
    p = CARPETA / "servicios" / slug / "index.html"
    t = p.read_text(encoding="utf-8")
    if 'class="ct-commercial"' in t:
        continue
    m = re.search(r'<section class="wrap s-section s-lead-pair">.*?</section>', t, re.S)
    assert m, f"{slug}: sin la entrada (s-lead-pair)"
    cuerpo, cierre = bloque_html(b)
    t = t[:m.end()] + cuerpo + t[m.end():]
    if cierre:
        k = min(i for i in (t.find('<section class="wrap s-section s-preguntas"'), t.find('<section class="wrap s-section s-fuentes"'), t.find('<section id="contacto"')) if i > 0)
        t = t[:k] + cierre + t[k:]
    t = t.replace("</style>", CT_CSS + "</style>", 1)
    p.write_text(t, encoding="utf-8")
    hechas.append(f"{slug} ({len(b['sectores'])})")

# Portada: filas de «Comercio e industria» = los 4 sectores, cada uno a su ancla; Industrias a su página
com = next(x for x in F["paginas"]["servicios"] if x["slug"] == "comercios")
b = next((x for x in com["bloques"] if x.get("tipo") == "sectores"), None)
f = CARPETA / "index.html"
t = f.read_text(encoding="utf-8")
if b and 'data-sectores-6c' not in t:
    filas = ""
    for s in b["sectores"]:
        href = f"{BASE}servicios/industria/" if s["id"] == "industria" else f"{BASE}servicios/comercios/#sector-{s['id']}"
        filas += f'<a class="g-sector" href="{href}"><span><h3>{e(s["nombre"])}</h3><p>{e(resumen(s))}</p></span><span aria-hidden="true">→</span></a>'
    t, n = re.subn(r'<div class="g-sectores">.*?</div>(?=</div></section>)', lambda m: f'<div class="g-sectores" data-sectores-6c>{filas}</div>', t, count=1, flags=re.S)
    assert n == 1, "portada: no encontré las filas de Comercio e industria"
    f.write_text(t, encoding="utf-8")
    hechas.append("portada (4 filas)")
print("sectores de globaltni:", ", ".join(hechas))
