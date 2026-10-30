"""Revisa los artículos de ficha/blog/ con las reglas de revisar_oficina.py de la skill (sin la ficha de marca).

Uso:  uv run --python 3.12 python revisar_blog.py
"""
import glob
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
# palabra clave de cada artículo: tiene que salir en la entrada, en un H2 y en una pregunta frecuente
CLAVES = {
    "como-eliminar-el-comejen": "comejen",
    "dengue-y-zancudos-en-casa": "zancudos",
    "zompopas-en-el-jardin": "zompopas",
    "ratas-y-leptospirosis": "leptospirosis",
    "chinches-de-cama": "chinches de cama",
    "pulgas-y-garrapatas": "pulgas y garrapatas",
}


def sin_acentos(x):
    return unicodedata.normalize("NFD", x).encode("ascii", "ignore").decode().lower()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fallas = 0
    for f in sorted(glob.glob(str(RAIZ / "ficha" / "blog" / "*.json"))):
        a = json.loads(Path(f).read_text(encoding="utf-8"))
        clave = CLAVES.get(a["slug"], "")
        cuerpo = re.sub("<[^>]+>", " ", a["content_html"])
        texto = "\n".join([a["title"], a["meta_description"], a["excerpt"], cuerpo] + [q + " " + r for q, r in a["faqs"]])
        h = []
        if ";" in texto:
            h.append("punto y coma")
        if "—" in texto or "–" in texto:
            h.append("raya larga")
        if len(a["title"]) > 60:
            h.append(f"título {len(a['title'])}")
        if not 150 <= len(a["meta_description"]) <= 160:
            h.append(f"meta {len(a['meta_description'])}")
        if not clave:
            h.append("sin palabra clave en CLAVES")
        else:
            if clave not in sin_acentos(cuerpo[:400]):
                h.append("clave no está en la entrada")
            if not any(clave in sin_acentos(x) for x in re.findall("<h2>(.*?)</h2>", a["content_html"])):
                h.append("clave en 0 H2")
            if not any(clave in sin_acentos(q) for q, _ in a["faqs"]):
                h.append("ninguna FAQ con la clave")
        if not 3 <= len(a["faqs"]) <= 4:
            h.append(f"{len(a['faqs'])} FAQ")
        fallas += bool(h)
        print(f"{a['slug']} ({a['fecha']}) | {len(cuerpo.split())} palabras |", "✗ " + ", ".join(h) if h else "✓ limpio")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
