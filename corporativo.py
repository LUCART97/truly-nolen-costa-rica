"""Portada completa como globaltni (receta truly-inbound, Réplica · vueltas 8 y 9, 3-nov-2026). Se corre después de master.py.
- Índice «Un programa para su espacio»: 4 tarjetas (TEPS con sello, Comercial, Residencial, Sanitización) que bajan a su sección.
- Secciones corporativas de Truly Nolen International con los textos oficiales de globaltni.com/es (usted): sanitización y TEPS
  después de «Comercio e industria»; red internacional e historia después de «Cómo trabajamos»; sin franquicia; fuentes al final.
- Carro real de la marca (carro-truly.png) en cifras, historia, chat y caja de Truly AI; nada del carrito dibujado.
Todo sale de capa/diseno_oficina.py y capa/corporativas_textos.py del paquete oficial (sin cambiar sus textos)."""
import json, re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "capa"))
import diseno_oficina as D, corporativas_textos as CT
sys.stdout.reconfigure(encoding="utf-8")
F = json.loads((RAIZ / "ficha/costa-rica.json").read_text(encoding="utf-8"))
CARPETA = RAIZ / "sitio/oficinas" / F["id"]
o = {"id": F["id"], "language": "es", "textos": dict(F.get("textos", {}))}
for tu, usted, _fr in CT.T:                         # usted = texto oficial de globaltni.com/es
    if usted is not None: o["textos"].setdefault(tu, usted)
# Corrección de estilo de los textos de globaltni (revisión del 4-nov-2026): español correcto, sin calcos del inglés.
o["textos"].update({
    "Inspección, plan de control, registro de cada visita y revisión de tendencias. Un programa de Manejo Integrado de Plagas con trazabilidad y estándares auditados.":
        "Inspección, plan de control, registro de cada visita y revisión de tendencias. Un programa de manejo integrado de plagas con trazabilidad y estándares auditados.",
    "Formación sobre manejo integrado de plagas, biología, ecología, aspectos regulatorios y soporte de auditoría.":
        "Formación sobre manejo integrado de plagas, biología, ecología, aspectos normativos y apoyo en auditorías.",
    "Programas personalizados para las necesidades de cada cliente, especialmente instalaciones auditadas.":
        "Programas personalizados para las necesidades de cada cliente, especialmente para instalaciones auditadas.",
    "Una red internacional": "Presencia mundial",
    "Conecta con una oficina local.": "Comuníquese con una oficina local.",
    "El automóvil amarillo con orejas de ratón de Truly Nolen": "El carro amarillo con orejas de ratón de Truly Nolen",
    "Busca tu localidad en el directorio internacional. La oficina que atiende tu zona te ayudará a conocer el servicio y el programa adecuado para tu espacio.":
        "Busque su localidad en el directorio internacional. La oficina que atiende su zona le ayudará a conocer el servicio y el programa adecuados para su espacio.",
    "Nuestra historia hasta ahora →": "Conozca nuestra historia →",
})
san, teps, red, _fra, his, fte = D.corporativas(o)  # franquicia no va en una oficina (vuelta 9)
f = CARPETA / "index.html"; t = f.read_text(encoding="utf-8")
if 'id="teps"' not in t:
    # índice de 4 tarjetas
    sello = '<img alt="" decoding="async" height="900" loading="lazy" src="/oficinas/assets/teps-sello.webp" width="900"/>'
    def tarjeta(d, r, tit, peq):
        icono = sello if d == "teps" else f'<svg viewBox="0 0 24 24">{D.INDICE_ICONO[d]}</svg>'
        apoyo = f"<small>{D.e(D._t(o, peq))}</small>" if peq else ""
        return f'<a href="#{d}"><span>{D.e(D._t(o, r))}</span><strong>{D.e(D._t(o, tit))}</strong><span aria-hidden="true">↓</span>{apoyo}<i aria-hidden="true" class="service-icon">{icono}</i></a>'
    prog = (f'<section id="servicios" class="section g g-programa">{D._cab(o, "Truly Nolen · Costa Rica", "Un programa para tu espacio.", "De la inspección de una vivienda a los registros de una instalación auditada. Elige el servicio que necesitas conocer.")}'
            f'<div class="service-index">{"".join(tarjeta(*x) for x in D.INDICE)}</div></section>')
    t, n = re.subn(r'<section id="servicios" class="section g g-programa">.*?</section>', lambda m: prog, t, count=1, flags=re.S); assert n == 1, "programa"
    def tras(idd_re, html):
        global t
        m = re.search(r'<section[^>]*' + idd_re + r'[^>]*>.*?</section>', t, re.S); assert m, idd_re
        t = t[:m.end()] + html + t[m.end():]
    tras(r'class="section g g-comercial"', san + teps)
    tras(r'class="section g g-metodo"', red + his)
    tras(r'class="section g g-ayuda"', fte)
# carro real en lugar del carrito dibujado (vuelta 9)
hechas = 0
for p in CARPETA.rglob("*.html"):
    s = p.read_text(encoding="utf-8")
    s2 = s.replace('<img src="/oficinas/assets/truly-carrito-asistente.svg" alt=""/>', '<img src="/oficinas/assets/carro-truly.png" width="100" height="65" alt=""/>')
    s2 = s2.replace("/oficinas/assets/truly-carrito-asistente.svg", "/oficinas/assets/carro-truly.png")
    if p == f: s2 = s2 if 'id="teps"' in s2 else s2
    if s2 != s: hechas += 1
    p.write_text(s2 if p != f else s2, encoding="utf-8")
# pestañas de plagas en celular: la activa se centra al cargar (receta: blancos táctiles y pestañas visibles)
CENTRAR = '<script src="/oficinas/assets/pestanas.js" defer></script>'
for p in CARPETA.glob("plagas/*/index.html"):
    s = p.read_text(encoding="utf-8")
    if 'class="pest-families"' in s and "pestanas.js" not in s:
        p.write_text(s.replace("</body>", CENTRAR + "</body>", 1), encoding="utf-8")
if 'id="teps"' in t:
    t = t.replace('<span id="nosotros"></span>', '')   # «Nosotros» del menú lleva a la historia, como en globaltni
    t = t.replace("/oficinas/assets/truly-carrito-asistente.svg", "/oficinas/assets/carro-truly.png")
    t = t.replace('<img src="/oficinas/assets/carro-truly.png" alt=""/>', '<img src="/oficinas/assets/carro-truly.png" width="100" height="65" alt=""/>')
    f.write_text(t, encoding="utf-8")
# blog: consejos de prevención sin foto (la foto de la plaga ya sale arriba o en su guía)
b = CARPETA / "blog/index.html"
if b.exists():
    bt = b.read_text(encoding="utf-8")
    i = bt.find('class="blog-grid blog-consejos"')
    if i > 0:
        j = bt.find("</section>", i)
        trozo = re.sub(r'<a href="[^"]+" tabindex="-1" aria-hidden="true"><img [^>]*></a>\s*', "", bt[i:j])
        b.write_text(bt[:i] + trozo + bt[j:], encoding="utf-8")
print("portada con índice de 4 tarjetas, sanitización, TEPS, red, historia y fuentes; carro real en", hechas, "páginas")
