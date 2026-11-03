"""Comercios por sector como /es/services/commercial/ de globaltni (3-nov-2026, opción B del dueño). Se corre después de corporativo.py.
Reemplaza «Cada punto del proceso.» por la barra amarilla de sectores y un bloque por sector (fotos documentales, prosa,
«¿Quién se beneficia con este programa?»). Todo el texto sale de la ficha (bloque «Por tipo de negocio»); nada inventado.
El CSS va en plantilla/sectores.css y se agrega al <style> de la página."""
import json, re, html, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent
F = json.loads((RAIZ / "ficha/costa-rica.json").read_text(encoding="utf-8"))
e = lambda s: html.escape(s or "", quote=True)
c = next(p for p in F["paginas"]["servicios"] if p["slug"] == "comercios")
b = next(x for x in c["bloques"] if x.get("tipo") == "tabla" and x.get("titulo") == "Cada punto del proceso.")
FOTOS = F.get("sectoresFotos", {})
A = f"/oficinas/{F['id']}/assets/"
ID = ["restaurantes", "comercio-alimentos", "hoteles-oficinas"]
CSS = (RAIZ / "plantilla/sectores.css").read_text(encoding="utf-8")


def lista(nombre):
    partes = re.split(r",\s*|\s+y\s+", nombre)
    return [p[0].upper() + p[1:] for p in partes if p]


def minus(s):
    return s[0].lower() + s[1:]


nav, secs = [], []
for i, f in enumerate(b["filas"]):
    nombre, breve = f[0][0], f[0][1]
    puntos = f[1]
    idd = ID[i]
    nav.append(f'<a href="#{idd}">{e(nombre)}<span aria-hidden="true">↓</span></a>')
    figs = "".join(f'<figure><img src="{A}{x["file"]}" alt="{e(x["alt"])}" width="{x["w"]}" height="{x["h"]}" loading="lazy"/>'
                   f'<figcaption>{e(x["alt"])}</figcaption></figure>' for x in FOTOS.get(idd, []))
    frase = "; ".join(minus(p.rstrip(".")) for p in puntos) + "."
    prosa = (f'<p>En la inspección se revisan sus puntos críticos: {e(frase)}</p>'
             '<button type="button" class="ct-link" data-abrir-chat>Consultar por su negocio<span aria-hidden="true">→</span></button>')
    quien = "".join(f"<li>{e(x)}</li>" for x in lista(nombre))
    oscuro = " ct-oscuro" if i == 1 else ""
    secs.append(f'<section class="ct-sector{oscuro}" id="{idd}" aria-labelledby="{idd}-title"><div class="wrap">'
                f'<header class="ct-sector-heading"><p class="ct-kicker">{e(nombre)}</p><h2 id="{idd}-title">{e(breve)}</h2></header>'
                f'<div class="ct-sector-layout"><div class="ct-documentary">{figs}</div><div class="ct-prose">{prosa}</div>'
                f'<aside class="ct-facilities" aria-labelledby="{idd}-fac"><h3 id="{idd}-fac">¿Quién se beneficia con este programa?</h3>'
                f'<ul>{quien}</ul></aside></div></div></section>')
bloque = (f'<section class="wrap s-section s-flow" id="sectores"><h2>{e(b["titulo"])}</h2><article class="s-prose"><p>{e(b["texto"])}</p></article></section>'
          f'<nav class="ct-sector-nav" aria-label="Sectores"><div class="wrap"><span>Elija su tipo de negocio</span><div>{"".join(nav)}</div></div></nav>'
          + "".join(secs))
p = RAIZ / "sitio/oficinas" / F["id"] / "servicios/comercios/index.html"
t = p.read_text(encoding="utf-8")
if 'class="ct-sector' not in t:
    t, n = re.subn(r'<section class="wrap s-section s-flow"><h2>Cada punto del proceso\.</h2>.*?</section>', lambda m: bloque, t, count=1, flags=re.S)
    assert n == 1, "no encontré «Cada punto del proceso.»"
    t = t.replace("</style>", CSS + "</style>", 1)
    p.write_text(t, encoding="utf-8")
print("comercios por sector:", len(secs), "sectores,", sum(len(v) for v in FOTOS.values()), "fotos")
