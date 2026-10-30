"""Prepara el sitio para GitHub Pages: copia sitio/ a _site/ y agrega el prefijo del repositorio a las rutas
absolutas (/oficinas, /machotes, /landing, /tn-emblema), porque en Pages el sitio vive en /<repositorio>/.
La dirección raíz lleva a la portada de Costa Rica.

Uso:  python publicar_pages.py [/truly-nolen-costa-rica]
"""
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ORIGEN = RAIZ / "sitio"
DESTINO = RAIZ / "_site"
PREFIJO = (sys.argv[1] if len(sys.argv) > 1 else "/truly-nolen-costa-rica").rstrip("/")
# una ruta absoluta del sitio, justo después de una comilla, un paréntesis, un igual o un espacio (srcset, url(), data-src…)
RUTA = re.compile(r"""(?<=["'(=\s,])/(?=(oficinas|machotes|landing|tn-emblema)\b)""")
PORTADA = f"{PREFIJO}/oficinas/costa-rica/"


def main():
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEN, DESTINO, ignore=shutil.ignore_patterns("_elegir"))
    cambiados = 0
    for p in DESTINO.rglob("*"):
        if p.suffix.lower() in {".html", ".css", ".js", ".xml", ".json", ".svg"}:
            texto = p.read_text(encoding="utf-8")
            nuevo = RUTA.sub(PREFIJO + "/", texto)
            if nuevo != texto:
                p.write_text(nuevo, encoding="utf-8")
                cambiados += 1
    redireccion = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="robots" content="noindex,nofollow"/>
<meta http-equiv="refresh" content="0; url={PORTADA}"/><title>Truly Nolen Costa Rica</title></head>
<body><a href="{PORTADA}">Ir a Truly Nolen Costa Rica</a></body></html>
"""
    (DESTINO / "index.html").write_text(redireccion, encoding="utf-8")
    (DESTINO / "404.html").write_text(redireccion, encoding="utf-8")
    (DESTINO / ".nojekyll").write_text("", encoding="utf-8")          # sin Jekyll: publicar los archivos tal cual
    print(f"{cambiados} archivos con rutas ajustadas a {PREFIJO}/ en {DESTINO}")


if __name__ == "__main__":
    main()
