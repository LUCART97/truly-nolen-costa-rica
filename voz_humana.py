"""Paso «Voz humana» de la receta: junta el texto visible de TODAS las páginas generadas en docs/voz-humana/corpus.md
y corre el medidor de MAGIA (writing-metrics.mjs). Uso: python voz_humana.py [carpeta del medidor]"""
import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from bs4 import BeautifulSoup

RAIZ = Path(__file__).resolve().parent
SITIO = RAIZ / "sitio" / "oficinas" / "costa-rica"
SALIDA = RAIZ / "docs" / "voz-humana" / "corpus.md"
MEDIDOR = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / ".claude/skills/truly-inbound/voz-humana") / "writing-metrics.mjs"
BLOQUES = ["h1", "h2", "h3", "p", "li", "summary", "th", "td", "figcaption", "blockquote", "small"]

partes = []
for html in sorted(SITIO.rglob("index.html")):
    sopa = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser")
    for t in sopa(["script", "style", "noscript", "template", "svg"]):
        t.decompose()
    ruta = "/" + html.parent.relative_to(SITIO.parent.parent).as_posix() + "/"
    lineas, vistos = [], set()
    for el in sopa.body.find_all(BLOQUES):
        if el.find(BLOQUES):          # solo los bloques de más adentro, para no repetir texto
            continue
        texto = " ".join(el.get_text(" ", strip=True).split())
        if len(texto) < 2 or texto in vistos:
            continue
        vistos.add(texto)
        lineas.append(("#" * int(el.name[1]) + " " if el.name in ("h1", "h2", "h3") else "") + texto)
    partes.append(f"<!-- {ruta} -->\n\n" + "\n\n".join(lineas))
SALIDA.write_text("\n\n".join(partes) + "\n", encoding="utf-8")
print(f"{len(partes)} páginas, {sum(len(p.split()) for p in partes)} palabras → {SALIDA.relative_to(RAIZ)}")
r = subprocess.run(["node", str(MEDIDOR), str(SALIDA)], capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-6000:], r.stderr[-1500:])
print("medidor: exit", r.returncode)
sys.exit(r.returncode)
