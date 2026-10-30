"""Arma la página para elegir imágenes: sitio/_elegir/index.html

Lee opciones/opciones.json (fotos con licencia libre) y opciones/catalogo.json (fotos de Truly del catálogo).
Cada espacio muestra la imagen actual y las opciones recortadas en la proporción en que se verán en el sitio.
El dueño marca una por espacio y copia el resultado (p. ej. «portada: b · hogar: a») para pegarlo en el chat.

Uso:  uv run --python 3.12 python elegir.py
"""
import json
import shutil
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
OPC = RAIZ / "opciones"
DESTINO = RAIZ / "sitio" / "_elegir"
ACTUALES = "/oficinas/costa-rica/assets/"

# espacio: (título, dónde sale, proporción ancho/alto, imagen actual)
ESPACIOS = {
    "hogar": ("Cocina · tarjeta Hogares", "Tarjeta de servicio 01 y portada de la página de Hogares.", "4/3", "cr-hogar-cocina.webp"),
    "casa": ("Cocina · «Su casa es más que cuatro paredes»", "Foto cuadrada de la sección de las tres zonas de la casa.", "1/1", "cr-casa-cocina-jardin.webp"),
    "comercio": ("Comercios", "Tarjeta de servicio 02 y portada de la página de Comercios.", "4/3", "cr-comercio-supermercado.webp"),
    "industria": ("Industria", "Tarjeta de servicio 03 y portada de la página de Industria.", "4/3", "cr-industria-planta.webp"),
    "chinches": ("Plaga nueva: chinches de cama", "Tarjeta de chinches en la guía de plagas y portada de su artículo del blog.", "3/2", None),
}


def cargar(nombre):
    p = OPC / nombre
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def main():
    opciones = cargar("opciones.json") + cargar("catalogo.json")
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    (DESTINO / "img").mkdir(parents=True)
    secciones = []
    for clave, (titulo, donde, prop, actual) in ESPACIOS.items():
        mias = sorted((o for o in opciones if o["slot"] == clave), key=lambda o: o["file"])
        tarjetas = []
        if actual:
            tarjetas.append(f"""<label class="op actual"><input type="radio" name="{clave}" value="actual" checked/>
<div class="marco" style="aspect-ratio:{prop}"><img src="{ACTUALES}{actual}" alt=""/></div>
<b>Actual</b><small>La que tiene hoy el sitio.</small></label>""")
        for o in mias:
            letra = Path(o["file"]).stem.rsplit("-", 1)[-1]
            src = OPC / o["file"]
            if not src.exists():
                continue
            shutil.copy(src, DESTINO / "img" / src.name)
            lic = f'<a href="{escape(o["source_page"])}" target="_blank" rel="noopener">{escape(o.get("license", ""))} · {escape(o.get("author", ""))}</a>'
            tarjetas.append(f"""<label class="op"><input type="radio" name="{clave}" value="{letra}"{'' if actual or tarjetas else ' checked'}/>
<div class="marco" style="aspect-ratio:{prop}"><img src="img/{src.name}" alt="" loading="lazy"/></div>
<b>Opción {letra.upper()}</b><small>{escape(o.get("note", ""))}</small><small class="lic">{lic}</small></label>""")
        if len(tarjetas) <= (1 if actual else 0):
            continue
        secciones.append(f'<section><h2>{escape(titulo)}</h2><p>{escape(donde)}</p><div class="ops">{"".join(tarjetas)}</div></section>')

    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Elegir imágenes · Truly Nolen Costa Rica</title><link rel="icon" href="/tn-emblema.png"/>
<style>
:root{{--paper:#f7f6f1;--ink:#18222b;--muted:#5d6b66;--yellow:#ffe000}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,Segoe UI,sans-serif}}
header{{padding:32px 16px 8px;max-width:1240px;margin:auto}}h1{{margin:0 0 8px;font-size:clamp(28px,4vw,44px)}}
header p{{color:var(--muted);max-width:70ch;margin:0}}
section{{max-width:1240px;margin:auto;padding:28px 16px;border-top:1px solid #d9dcd3}}h2{{margin:0}}section>p{{margin:4px 0 16px;color:var(--muted)}}
.ops{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}}
.op{{display:flex;flex-direction:column;gap:4px;background:#fff;border:3px solid transparent;border-radius:8px;padding:10px;cursor:pointer}}
.op:has(input:checked){{border-color:var(--yellow);box-shadow:0 0 0 1px var(--ink)}}
.op input{{position:absolute;opacity:0}}.marco{{width:100%;overflow:hidden;border-radius:4px;background:#e8e7e0}}
.marco img{{width:100%;height:100%;object-fit:cover;display:block}}.op small{{color:var(--muted)}}.lic a{{color:var(--muted)}}
.actual b::after{{content:" ✓ en el sitio";font-weight:400;color:var(--muted)}}
footer{{position:sticky;bottom:0;background:var(--ink);color:#fff;padding:14px 16px}}
footer div{{max-width:1240px;margin:auto;display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
footer output{{flex:1;min-width:200px;font-family:ui-monospace,Consolas,monospace;font-size:14px}}
button{{background:var(--yellow);color:var(--ink);border:0;border-radius:4px;padding:10px 18px;font-weight:700;cursor:pointer}}
</style></head><body>
<header><h1>Elija las imágenes de Truly Nolen Costa Rica</h1>
<p>Toque una opción en cada espacio. Al final copie su elección y péguela en el chat. Las fotos con licencia libre llevan su autor y licencia; las de uniforme Truly salen del catálogo de Truly Inbound.</p></header>
{"".join(secciones)}
<footer><div><output id="sel"></output><button type="button" id="copiar">Copiar mi elección</button></div></footer>
<script>
const out=document.getElementById('sel');
function leer(){{const v=[...document.querySelectorAll('section')].map(s=>{{const i=s.querySelector('input:checked');return i?i.name+': '+i.value:''}}).filter(Boolean);out.textContent=v.join(' · ');return out.textContent}}
document.addEventListener('change',leer);leer();
document.getElementById('copiar').onclick=async()=>{{try{{await navigator.clipboard.writeText(leer());document.getElementById('copiar').textContent='¡Copiado!'}}catch(e){{prompt('Copie este texto:',leer())}}}};
</script></body></html>
"""
    (DESTINO / "index.html").write_text(html, encoding="utf-8")
    print(f"{len(secciones)} espacios en {DESTINO / 'index.html'}")


if __name__ == "__main__":
    main()
