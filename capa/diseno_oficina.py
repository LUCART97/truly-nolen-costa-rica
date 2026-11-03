# Diseño de las oficinas con el lenguaje de globaltni.com/es (aprobado por el dueño el 31-oct-2026).
# Lo aplica build-inbound-machotes.py a cada oficina DESPUÉS de armarla; el catálogo de machotes no se toca.
#   · Portada: cifras de la marca, programa por espacio, tres zonas con la casa, comercio por sectores, cómo
#     trabajamos, plagas en fila y blog + preguntas. La película pasa por dos escenas (carro → mundo), como globaltni.
#   · Hogares: columnas con divisores, tres zonas con la casa y una sola galería de plagas.
# Los textos fijos van de tú; una ficha de usted los cambia en «textos» (mismo mecanismo que el resto del molde).
import json, re, html
from pathlib import Path

e = lambda s: html.escape(s, quote=True)
br = lambda s: e(s).replace('\n', '<br/>')
CSS = (Path(__file__).with_name('diseno_oficina.css')).read_text(encoding='utf-8')
# Los íconos de línea del índice «Un programa para su espacio» son los SVG de globaltni.com (repo Catalizadora-Labs/tn-intl-design,
# site/a/index.html, sección #servicios, 3-nov-2026), tal cual: Comercial, Residencial y Sanitización. TEPS lleva el sello real.
INDICE_ICONO = {
    'comercial': '<path d="M4 21V6a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v15"/><path d="M12 21V11h7a1 1 0 0 1 1 1v9"/><path d="M3 21h18"/><path d="M7 9h2M7 13h2M7 17h2M15 15h2M15 18h2"/>',
    'residencial': '<path d="M4 11.5 12 4.5l8 7"/><path d="M6 10.5V20h12v-9.5"/><path d="M10 20v-5h4v5"/>',
    'sanitizacion': '<rect height="11" rx="2" width="7" x="9" y="10"/><path d="M11 10V6h3"/><path d="M14 6h-3"/><path d="M8 5H6M8 7.5H5.5M8 10H6"/>'}
# Orden y destino del master: cada tarjeta lleva a una sección de la misma portada (los id los pone portada(): teps, residencial, comercial, sanitizacion).
# (id de destino, rótulo, título, texto de apoyo [solo TEPS])
INDICE = [('teps', 'Monitoreo y control auditado', 'TEPS', 'Estándares globales, seguimiento y reportes.'),
          ('comercial', 'Programas según tu sector y actividad.', 'Comercial', ''),
          ('residencial', 'Inspección y cuidado en tres zonas.', 'Residencial', ''),
          ('sanitizacion', 'Control microbiano en interiores.', 'Sanitización', '')]
COLOR = ['rojo', 'amarillo', 'verde']
CASA = '/oficinas/assets/casa-tres-zonas.jpg'  # respaldo; cada oficina trae la suya en casaZonas


def casa(o):
    c = o.get('casaZonas') or {}
    return f"/oficinas/{o['id']}/assets/{c['file'].split('/')[-1]}" if c.get('file') else CASA
ALT_CASA = 'Casa vista desde arriba con el interior en rojo, el perímetro en amarillo y las áreas verdes en verde'


def _propios(x, acc):
    if isinstance(x, str): acc.add(x)
    elif isinstance(x, dict): [_propios(v, acc) for k, v in x.items() if k != 'textos']
    elif isinstance(x, list): [_propios(v, acc) for v in x]
    return acc


def _t(o, s):
    # En una oficina de otro idioma, un texto fijo del diseño que la ficha no traduce se anota en o['_faltan'] y el
    # generador frena. Lo que ya es contenido de la ficha (títulos de sus páginas, etc.) no se anota.
    v = o.get('textos', {}).get(s)
    if v is not None: return v
    if o.get('language', 'es') != 'es':
        if '_propios' not in o: o['_propios'] = _propios(o, set())
        if s not in o['_propios']: o.setdefault('_faltan', set()).add(s)
    return s


def _cab(o, ey, tit, txt=''):
    return (f'<header class="g-cab"><p class="g-ey">{e(_t(o, ey))}</p><h2>{br(_t(o, tit))}</h2>'
            + (f'<p class="g-intro">{e(_t(o, txt))}</p>' if txt else '') + '</header>')


def _seccion(t, idd):
    return re.search(r'<section[^>]*id="' + idd + r'"[^>]*>.*?</section>', t, re.S)


def _zonas(b):
    return b.get('filas') or [[[x[0], x[1]], x[2] if len(x) > 2 else []] for x in b['tarjetas']]


def _bloque_zonas(o, ruta):
    S = o['paginas']['servicios']
    z = next((b for b in S[0].get('bloques', []) if 'zona' in (b.get('titulo', '') + b.get('eyebrow', '')).lower()), None)
    if not z: return ''
    li = ''.join(f'<li class="g-z-{COLOR[i % 3]}"><h3>{e(f[0][0].split(" · ", 1)[-1])}</h3><p>{e(f[0][1])}</p></li>' for i, f in enumerate(_zonas(z)))
    enlace = f'<a class="g-link" href="/oficinas/{o["id"]}/servicios/{ruta("servicios", 0)}/">{e(_t(o, "Conoce el servicio para hogares"))}<span aria-hidden="true">→</span></a>' if ruta else ''
    return (f'<section id="residencial" class="section g g-zonas"><div class="g-zonas-grid"><figure class="g-zonas-fig"><img src="{casa(o)}" alt="{((o.get('casaZonas') or {}).get('alt') or _t(o, ALT_CASA))}" loading="lazy"/></figure>'
            f'<div>{_cab(o, z.get("eyebrow") or "Control residencial", z["titulo"], z.get("texto", ""))}<ul class="g-zonas-lista">{li}</ul>{enlace}</div></div></section>')


def _plagas(o, ruta, nota=''):
    base = f'/oficinas/{o["id"]}/'
    PL = o['paginas']['plagas']
    car = ''.join(
        f'<article><a class="g-pl-fig" href="{base}plagas/{ruta("plagas", i)}/"><img src="{base}assets/{p["imagen"]}" alt="" loading="lazy"/></a>'
        f'<h3>{e(p["titulo"])}</h3><p class="g-pl-sub">{e(p.get("eyebrow", ""))}</p>'
        f'<p>{e(re.split(r"(?<=[.])\s", p.get("resumen", p.get("intro", "")))[0])}</p>'
        f'<a class="g-mas" href="{base}plagas/{ruta("plagas", i)}/">{e(_t(o, "Ver la guía"))}<span aria-hidden="true">→</span></a></article>'
        for i, p in enumerate(PL) if p.get('imagen'))
    return car, len([p for p in PL if p.get('imagen')])


# ===== Secciones corporativas de la portada de globaltni.com/en (decisión del dueño, 3-nov-2026) =====
# Saneamiento · TEPS · red internacional · franquicia · historia (1938), con las clases y el orden del master. Texto de Truly Nolen International,
# no de la oficina: la clave es el español con tú y cada ficha lo traduce en `textos` (scripts/corporativas_textos.py). Sin fotos de globaltni:
# solo la capa común (el carro de la marca). Los botones van a globaltni.com con la ruta exacta (no existen páginas equivalentes en las oficinas).
EXTERNAS = [('Américas', [('Argentina', 'http://www.trulynolenargentina.com.ar'), ('Brasil', 'https://www.trulynolen.com.br')]),
            ('Europa', [('España', 'https://www.trulyespana.com/'), ('Francia', 'https://www.trulynolen.fr/')]),
            ('Asia', [('India', 'https://trulynolenindia.com/'), ('Filipinas', 'https://www.trulynolen.com.ph/')])]
PAIS_PROPIO = {'francia': 'Francia', 'venezuela': 'Venezuela', 'nicaragua': 'Nicaragua', 'panama': 'Panamá'}


def corporativas(o):
    """Devuelve las cinco secciones y el bloque de fuentes (HTML) en el orden del master."""
    T = lambda s: e(_t(o, s))
    gt = 'https://globaltni.com/' + ('en' if o.get('language', 'es') == 'fr' else 'es')  # globaltni no tiene /fr/: el francés enlaza a /en/
    ext = ' target="_blank" rel="noopener noreferrer"'
    boton = lambda ruta, s, cls='button': f'<a class="{cls}" href="{gt}{ruta}"{ext}>{T(s)}</a>'
    san = (f'<section class="sanitization wrap" id="sanitizacion"><div class="sanitization-copy"><span>{T("Virus, hongos y bacterias")}</span>'
           f'<h2>{T("Sanitización de ambientes interiores.")}</h2><p>{T("La sanitización reúne estrategias para prevenir y controlar la contaminación por virus, hongos y bacterias, según el tipo de ambiente interior.")}</p>'
           f'{boton("/services/sanitization/", "Conoce el servicio de sanitización →", "button button-line")}</div>'
           f'<div class="sanitization-visual"><h3>{T("Un protocolo según el ambiente.")}</h3><p>{T("Entrevista e identificación del entorno. Selección de producto, aplicación y tiempo de contacto. Medidas de prevención y control para cada instalación.")}</p></div></section>')
    pasos = [('Inspeccionar', 'Evaluamos la instalación y su entorno', 'Identificamos actividad de plagas, puntos de acceso, condiciones favorables y prácticas operativas para determinar las necesidades del programa.'),
             ('Desarrollar el programa', 'Un plan específico para la instalación', 'El entorno, la estacionalidad, la actividad observada, las prácticas de operación y las plagas identificadas determinan el programa.'),
             ('Registrar cada visita', 'El trabajo queda documentado', 'Después de cada servicio, el técnico registra las actividades realizadas y los hallazgos identificados en la instalación.'),
             ('Revisar las tendencias', 'Informes mensuales y recomendaciones', 'Los datos registrados sobre la actividad de plagas permiten analizar tendencias y dar seguimiento a las acciones.')]
    items = [('Capacitación personalizada', 'Formación para clientes y empleados, con el respaldo del equipo técnico internacional.'),
             ('Centro de formación virtual', 'Capacitación a distancia para profundizar en los conocimientos del programa y sus protocolos.'),
             ('Supervisión de calidad', 'Informe de auditoría y lista de verificación específica para el tipo de establecimiento, con un indicador de rendimiento.'),
             ('Educación para el cliente', 'Formación sobre manejo integrado de plagas, biología, ecología, aspectos regulatorios y soporte de auditoría.'),
             ('Protocolos específicos', 'Programas personalizados para las necesidades de cada cliente, especialmente instalaciones auditadas.'),
             ('Respuesta y seguimiento', 'Se definen umbrales de acción con la administración. Si se superan, se aplica un protocolo de escalamiento hasta establecer el control.')]
    # Sello oficial de TEPS: el mismo archivo de globaltni (repo Catalizadora-Labs/tn-intl-design,
    # site/assets/teps-seal-hd-20260924.webp, bajado el 3-nov-2026). Es marca de Truly: no se rehace con IA.
    teps = (f'<section class="teps wrap" id="teps"><div class="teps-intro">'
            '<img class="teps-seal" src="/oficinas/assets/teps-sello.webp" width="900" height="900" alt="" decoding="async" loading="lazy">'
            f'<div class="teps-heading"><span>{T("Truly Elite Protection System")}</span><h2>{T("TEPS: un programa con seguimiento.")}</h2></div>'
            f'<div class="teps-description"><p>{T("Inspección, plan de control, registro de cada visita y revisión de tendencias. Un programa de Manejo Integrado de Plagas con trazabilidad y estándares auditados.")}</p>'
            f'{boton("/services/teps/", "Explora el sistema TEPS →")}</div></div>'
            '<ol class="teps-flow">' + ''.join(f'<li><span>0{i + 1}</span><h3>{T(a)}</h3><strong>{T(b)}</strong><p>{T(c)}</p></li>' for i, (a, b, c) in enumerate(pasos)) + '</ol>'
            f'<details class="program-overview"><summary><span>{T("Formación, supervisión y respuesta durante el programa")}</span><span aria-hidden="true">+</span></summary><div class="program-items">'
            + ''.join(f'<div><h3>{T(a)}</h3><p>{T(b)}</p></div>' for a, b in items) + '</div></details></section>')
    propio = PAIS_PROPIO.get(o['id'])
    cols = ''
    for cont, pais in EXTERNAS:
        li = ''.join(f'<li><a href="{u}"{ext}>{T(n)} ↗</a></li>' for n, u in pais if n != propio)
        if li: cols += f'<div><h4>{T(cont)}</h4><ul>{li}</ul></div>'
    red = (f'<section class="network" id="oficinas"><div class="wrap network-layout"><div><span>{T("Una red internacional")}</span><h2>{T("Una red internacional. Atención en tu localidad.")}</h2>'
           f'<p>{T("Busca tu localidad en el directorio internacional. La oficina que atiende tu zona te ayudará a conocer el servicio y el programa adecuado para tu espacio.")}</p>'
           f'<div class="network-actions">{boton("/offices/", "Abrir el directorio de oficinas →")}{boton("/contact/#formulario", "Escríbenos desde el formulario de contacto →", "text-link")}</div>'
           f'<p class="network-brands">{T("La confianza de marcas reconocidas en todo el mundo.")}</p><p class="network-note">{T("Trabajamos con hogares y empresas a través de nuestra red internacional de oficinas.")}</p></div>'
           f'<div><h3>{T("Conecta con una oficina local.")}</h3><p>{T("Accesos a sitios locales del directorio internacional.")}</p><div class="network-links">{cols}</div>'
           f'{boton("/offices/", "Ver todos los países y contactos →", "text-link")}'
           f'<div class="network-stats"><p>{T("Alcance internacional")}</p><div><div><strong>65+</strong><span>{T("países")}</span></div><div><strong>300+</strong><span>{T("oficinas")}</span></div><div><strong>6</strong><span>{T("continentes")}</span></div></div></div></div></div></section>')
    fra = (f'<section class="franchise wrap" id="franquicias"><div class="franchise-head"><span>{T("Franquicias Truly Nolen International")}</span><h2>{T("Tu franquicia de control de plagas.")}</h2>'
           f'<p>{T("Desarrolla un negocio con formación permanente en Manejo Integrado de Plagas, protocolos de servicio y soporte internacional.")}</p></div>'
           f'<div class="franchise-layout"><div><h3>{T("Formación que continúa después de la apertura.")}</h3><p>{T("El aprendizaje combina conocimientos técnicos y trabajo de campo. Los equipos estudian la biología de las plagas, practican la identificación y aprenden a aplicar los protocolos del servicio.")}</p>'
           f'<div class="franchise-actions">{boton("/franchise/join/", "Quiero ser franquiciado →")}{boton("/franchise/model/", "Conoce el modelo de franquicia →", "text-link")}</div></div>'
           f'<ul class="franchise-points"><li><strong>{T("Formación continua")}</strong><p>{T("La formación comienza online con especialistas de Truly Nolen International y continúa con unos 10 días de práctica en tu país.")}</p></li>'
           f'<li><strong>{T("Soporte internacional")}</strong><p>{T("El equipo técnico internacional acompaña el aprendizaje y el desarrollo de protocolos.")}</p></li>'
           f'<li><strong>{T("Un sistema de servicio compartido")}</strong><p>{T("Manejo Integrado de Plagas, protocolo de tres zonas y los cinco pasos de Truly Care.")}</p></li></ul></div></section>')
    his = (f'<section class="history" id="nosotros"><div class="wrap history-layout"><div><span>{T("Más de 80 años de experiencia")}</span><h2>{T("Prevenir las plagas. Una idea desde 1938.")}</h2>'
           f'<p>{T("En 1938, Truly Wheatfield Nolen propuso proteger los edificios sellando las entradas de los roedores. La prevención estaba en el origen.")}</p>'
           f'<p>{T("Hoy, esa visión se expresa en formación, métodos de control y protocolos diseñados para reducir el impacto en el entorno.")}</p>'
           f'<div class="history-links">{boton("/company/story/", "Nuestra historia hasta ahora →", "text-link")}{boton("/company/team/", "Conoce a nuestro equipo →", "text-link")}</div></div>'
           # Foto real del carro de la marca, la misma de globaltni (tn-intl-design, site/assets/mouse-car.png): es marca, no se rehace con IA.
           f'<div class="history-visual"><a class="history-car-link" href="{gt}/company/story/"{ext}><img src="/oficinas/assets/carro-truly.png" width="600" height="386" alt="{T("El automóvil amarillo con orejas de ratón de Truly Nolen")}" loading="lazy"/></a>'
           f'<ol class="history-timeline"><li><strong>1938</strong><p>{T("Una idea centrada en la prevención.")}</p></li><li><strong>1987</strong><p>{T("La visión llega a Argentina.")}</p></li><li><strong>1989</strong><p>{T("Nace Truly Nolen International.")}</p></li></ol></div></div></section>')
    fr = o.get('language', 'es') == 'fr'
    fuentes = [('sanitizacion', 'Sanitización de ambientes interiores.'), ('teps', 'TEPS: un programa con seguimiento.'), ('oficinas', 'Una red internacional. Atención en tu localidad.'),
               ('nosotros', 'Prevenir las plagas. Una idea desde 1938.')]
    lista = ''.join(f'<li><a href="{gt}/#{a}"{ext}>Truly Nolen International · {T(h).rstrip(".")}{" (page en anglais)" if fr else ""}</a></li>' for a, h in fuentes)
    fte = f'<section class="wrap s-section s-fuentes" id="fuentes-corporativas"><h2>{T("Fuentes")}</h2><ol>{lista}</ol></section>'
    return san, teps, red, fra, his, fte


def portada(o, carpeta, ruta, pais):
    """Rehace la portada de la oficina entre la película y la consulta."""
    f = carpeta / 'index.html'
    t = f.read_text(encoding='utf-8')
    if 'g-cifras' in t: return
    base = f'/oficinas/{o["id"]}/'
    S = o['paginas']['servicios']
    s1 = (f'<section id="cifras" class="g-cifras" aria-label="{e(_t(o, "Truly Nolen en el mundo"))}"><div class="g-cifras-in">'
          f'<div><b>65</b> <span>{e(_t(o, "países"))}</span><small>{e(_t(o, "presencia internacional"))}</small></div>'
          f'<div><b>300+</b> <span>{e(_t(o, "oficinas"))}</span><small>{e(_t(o, "en el mundo"))}</small></div>'
          f'<div><b>80+</b> <span>{e(_t(o, "años"))}</span><small>{e(_t(o, "de experiencia"))}</small></div>'
          f'<div class="g-cifra-carro"><img src="/oficinas/assets/carro-truly.png" width="100" height="65" alt=""/><span>{e(_t(o, "una marca reconocible"))}<small>{e(_t(o, "nuestro carro emblemático"))}</small></span></div>'
          '</div></section>')
    # Índice «Un programa para su espacio» igual al de globaltni.com/es: cuatro tarjetas (TEPS, Comercial, Residencial, Sanitización) que bajan a su sección.
    # Industria no se pierde: sigue en «Comercio e industria» (#comercial) con sus botones.
    sello = '<img alt="" decoding="async" height="900" loading="lazy" src="/oficinas/assets/teps-sello.webp" width="900"/>'
    def tarjeta(d, r, tit, peq):
        icono = sello if d == 'teps' else f'<svg viewBox="0 0 24 24">{INDICE_ICONO[d]}</svg>'
        apoyo = f'<small>{e(_t(o, peq))}</small>' if peq else ''
        return f'<a href="#{d}"><span>{e(_t(o, r))}</span><strong>{e(_t(o, tit))}</strong><span aria-hidden="true">↓</span>{apoyo}<i aria-hidden="true" class="service-icon">{icono}</i></a>'
    fila = ''.join(tarjeta(*x) for x in INDICE)
    s2 = (f'<section id="servicios" class="section g g-programa">{_cab(o, "Truly Nolen · " + pais, "Un programa para tu espacio.", "De la inspección de una vivienda a los registros de una instalación auditada. Elige el servicio que necesitas conocer.")}'
          f'<div class="service-index">{fila}</div></section>')
    s3 = _bloque_zonas(o, ruta)
    c = S[1]
    sec = next((b for b in c.get('bloques', []) if b.get('tarjetas') and len(b['tarjetas']) >= 3 and not b.get('tipo')), {'tarjetas': []})
    sectores = [x for x in sec.get('tarjetas', [])][:4]
    benef = next((b for b in c.get('bloques', []) if b.get('tipo') == 'beneficia' and b.get('grupos')), None)
    if benef:  # sectores reales de la ficha (los que Truly Nolen International nombra), no las tarjetas genéricas
        sectores = [[g[0], ', '.join(_minus(g[1]))] for g in benef['grupos']][:4]
    rows = ''.join(f'<a class="g-sector" href="{base}servicios/{ruta("servicios", 1)}/"><span><h3>{e(x[0])}</h3><p>{e(x[1])}</p></span><span aria-hidden="true">→</span></a>' for x in sectores)
    rows += f'<a class="g-sector" href="{base}servicios/{ruta("servicios", 2)}/"><span><h3>{e(S[2]["titulo"])}</h3><p>{e(_primera(S[2].get("intro", "")))}</p></span><span aria-hidden="true">→</span></a>'
    foto = re.search(r'<section class="local-operation"><img src="([^"]+)"', t)
    s4 = (f'<section id="comercial" class="section g g-comercial">{_cab(o, "Comercio e industria", "Control de plagas para tu actividad.", _primera(c.get("intro", "")))}'
          f'<div class="g-com-grid"><a class="g-com-foto" href="{base}servicios/{ruta("servicios", 1)}/"><img src="{foto.group(1) if foto else ""}" alt="" loading="lazy"/><span><b>{e(_t(o, "La prevención es parte de tu operación."))}</b><em>{e(_t(o, "Conoce el servicio para comercios →"))}</em></span></a><div class="g-sectores">{rows}</div></div></section>')
    m = _seccion(t, 'metodo')
    pasos = re.findall(r'<h3>([^<]+)</h3>\s*<p>([^<]*)</p>', m.group(0)) if m else []
    s5 = (f'<section id="metodo" class="section g g-metodo">{_cab(o, "Cómo trabajamos", "Un siguiente paso claro,\nen cada momento.")}<div class="g-cols g-cols-4">'
          + ''.join(f'<article><span class="g-n">0{i + 1}</span><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i, (a, b) in enumerate(pasos)) + '</div></section>')
    car, n = _plagas(o, ruta)
    s6 = f'<section id="plagas" class="section g g-plagas">{_cab(o, "Guía de plagas", "Reconoce la plaga.\nEntiende sus hábitos.", "Las que más vemos en " + pais + ". Cada guía explica las señales y qué hacer, con fuentes.")}<div class="g-plagas-grid" style="--n:{n}">{car}</div></section>'
    blog = carpeta / 'blog/index.html'
    b = blog.read_text(encoding='utf-8') if blog.exists() else ''
    art = re.search(r'<article.*?</article>', b, re.S); a0 = art.group(0) if art else ''
    bt = re.search(r'<h[23][^>]*>\s*<a href="([^"]+)">([^<]+)</a>', a0); bimg = re.search(r'<img[^>]*src="([^"]+)"', a0)
    bp = re.search(r'<p[^>]*>([^<]{40,})</p>', a0); bf = re.search(r'<time[^>]*>([^<]+)</time>', a0)
    fq = _seccion(t, 'preguntas')
    qa = re.findall(r'<summary>(.*?)<span.*?</summary>\s*<p>(.*?)</p>', fq.group(0), re.S) if fq else []
    det = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}<span aria-hidden="true">+</span></summary><p>{r}</p></details>' for i, (q, r) in enumerate(qa))
    blog_html = ''
    if bt:
        img = f'<img src="{bimg.group(1)}" alt="" loading="lazy"/>' if bimg else ''
        blog_html = (f'<article class="g-blog"><div class="g-blog-top">{img}<p class="g-ey">{e(_t(o, "Del blog"))}{(" · " + bf.group(1)) if bf else ""}</p></div>'
                     f'<h3><a href="{bt.group(1)}">{bt.group(2)}</a></h3>{"<p>" + bp.group(1) + "</p>" if bp else ""}'
                     f'<a class="g-link" href="{bt.group(1)}">{e(_t(o, "Leer el artículo"))}<span aria-hidden="true">→</span></a>'
                     f'<a class="g-link g-link-2" href="{base}blog/">{e(_t(o, "Ver todo el blog"))}<span aria-hidden="true">→</span></a></article>')
    s7 = (f'<section class="section g g-ayuda">{_cab(o, "Blog y preguntas", "Prevención y respuestas\npara ti.", "Consejos para prevenir plagas y cómo trabajamos.")}<div class="g-ayuda-grid">'
          + blog_html + f'<div class="g-faq" id="preguntas"><h3>{e(_t(o, "Lo que más nos preguntan."))}</h3>{det}</div></div></section>')
    # según la base, «nosotros» y «local-home» vienen antes o después de servicios: se reemplaza desde la primera
    ini = min(t.index(x) for x in ('<section id="servicios"', '<section id="nosotros"', '<section class="section local-home"') if x in t); fin = t.index('<section id="consulta"')
    cob = _seccion(t, 'cobertura')
    san, teps, red, fra, his, fte = corporativas(o)
    # Sin la sección de franquicias: una oficina no vende franquicias (decisión del dueño, 3-nov-2026). corporativas() la sigue armando.
    t = t[:ini] + s1 + s2 + s3 + s4 + san + teps + s5 + red + his + s6 + s7 + fte + (cob.group(0) if cob else '') + t[fin:]
    t = _hero(t, o)
    f.write_text(_estilo(_escenas(t, o)), encoding='utf-8')


def _hero(t, o):
    """Hero como el master: botón con marca de ubicación, «Servicio premium · Visión internacional» y tres anclas (hogar, negocio, método)."""
    if 'hero-routes' in t: return t
    m = re.search(r'(<div class="hero-text">.*?<a class="button"[^>]*>)(.*?)(</a>)(</div>)\s*<a class="discover"[^>]*>.*?</a>', t, re.S)
    if not m: return t
    rutas = (f'<div class="hero-routes"><a href="#residencial">{e(_t(o, "Tu hogar"))} <span aria-hidden="true">↓</span></a>'
             f'<a href="#comercial">{e(_t(o, "Tu negocio"))} <span aria-hidden="true">↓</span></a>'
             f'<a href="#teps">{e(_t(o, "Programa TEPS"))} <span aria-hidden="true">↓</span></a></div>')
    nuevo = (m.group(1) + m.group(2) + ' <span class="office-mark" aria-hidden="true"></span>' + m.group(3)
             + f'<span class="hero-premium">{e(_t(o, "Servicio premium · Visión internacional"))}</span>' + m.group(4) + rutas)
    return t.replace(m.group(0), nuevo, 1)


def hogares(o, carpeta, ruta):
    """Hogares: tres pilares con divisores, las tres zonas con la casa y una sola galería de plagas."""
    f = carpeta / 'servicios' / ruta('servicios', 0) / 'index.html'
    if not f.exists(): return
    t = f.read_text(encoding='utf-8')
    if 'g-esperar' in t: return
    B = o['paginas']['servicios'][0]['bloques']
    secs = list(re.finditer(r'<section class="section detail-(?:guidance|tabla)".*?</section>', t, re.S))
    def por_titulo(b):
        clave = e(b['titulo'].split('\n')[0])
        return next((s for s in secs if clave in s.group(0)), None)
    rep = []
    b0 = B[0]
    if b0.get('tarjetas') and por_titulo(b0):
        col = ''.join(f'<article><span class="g-n">0{i + 1}</span><h3>{e(a)}</h3><p>{e(c)}</p></article>' for i, (a, c, *_) in enumerate(b0['tarjetas']))
        rep.append((por_titulo(b0), f'<section class="section g g-esperar">{_cab(o, b0.get("eyebrow", ""), b0["titulo"], b0.get("texto", ""))}<div class="g-cols g-cols-3">{col}</div>' + (f'<p class="g-nota">{e(b0["nota"])}</p>' if b0.get('nota') else '') + '</section>'))
    z = next((b for b in B if 'zona' in (b.get('titulo', '') + b.get('eyebrow', '')).lower()), None)
    if z and por_titulo(z):
        li = ''.join(f'<li class="g-z-{COLOR[i % 3]}"><h3>{e(f[0][0].split(" · ", 1)[-1])}</h3><p>{e(f[0][1])}</p><p class="g-z-det">{e(" · ".join(x.rstrip(".") for x in f[1]))}.</p></li>' for i, f in enumerate(_zonas(z)))
        rep.append((por_titulo(z), f'<section class="section g g-zonas"><div class="g-zonas-grid"><figure class="g-zonas-fig"><img src="{casa(o)}" alt="{((o.get('casaZonas') or {}).get('alt') or _t(o, ALT_CASA))}" loading="lazy"/></figure><div>{_cab(o, z.get("eyebrow", ""), z["titulo"], z.get("texto", ""))}<ul class="g-zonas-lista">{li}</ul></div></div></section>'))
    bp = next((b for b in B if b.get('tarjetas') and any(x[0] in [p['titulo'] for p in o['paginas']['plagas']] for x in b['tarjetas'])), None)
    if bp and por_titulo(bp):
        car, n = _plagas(o, ruta)
        nota = ''.join(f'<p class="g-plagas-nota"><strong>{e(x[0])}.</strong> {e(x[1])}</p>' for x in bp['tarjetas'] if x[0] not in [p['titulo'] for p in o['paginas']['plagas']])
        rep.append((por_titulo(bp), f'<section class="section g g-plagas">{_cab(o, bp.get("eyebrow", ""), bp["titulo"], bp.get("texto", ""))}<div class="g-plagas-grid" style="--n:{n}">{car}</div>{nota}</section>'))
    for m, nuevo in sorted(rep, key=lambda x: -x[0].start()):
        t = t[:m.start()] + nuevo + t[m.end():]
    if bp: t = re.sub(r'<section class="section pests".*?</section>', '', t, count=1, flags=re.S)
    f.write_text(_estilo(t), encoding='utf-8')


def _estilo(t):
    return t if 'g-cab{' in t else t.replace('</head>', '<style>' + CSS + '</style></head>', 1)


def _escenas(t, o=None):
    """Película en dos escenas como globaltni (carro → mundo 10 s → carro): lo hace /oficinas/assets/escenas.js."""
    if 'escenas.js' in t: return t
    # Cada archivo con su huella en la URL (?v=): al cambiar el mundo o escenas.js nadie se queda con el viejo en caché.
    import hashlib
    comun = Path(__file__).resolve().parents[1] / 'app/public/oficinas/assets'
    v = lambda n: hashlib.sha256((comun / n).read_bytes()).hexdigest()[:12]
    return t.replace('</body>', f'<script defer src="/oficinas/assets/escenas.js?v={v("escenas.js")}" '
                     f'data-mundo="/oficinas/assets/mundo-desktop.mp4?v={v("mundo-desktop.mp4")}" '
                     f'data-mundo-movil="/oficinas/assets/mundo-movil.mp4?v={v("mundo-movil.mp4")}"'
                     + (f' data-vueltas="{int(vu)}"' if (vu := ((o or {}).get('pelicula') or {}).get('vueltas')) else '')
                     + '></script></body>', 1)


def _cierre(t, interna):
    """Un solo cierre como globaltni: contacto + tarjeta de Truly AI + línea de cobertura en un bloque.
    Las anclas #consulta y #cobertura siguen existiendo dentro del bloque."""
    if 'local-consult g-cierre"' in t: return t
    ct = re.search(r'<section id="contacto" class="section contact"><div>(.*?)</div>(<div class="contact-channels".*?</div>)</section>', t, re.S)
    if not ct: return t
    cons = [m for m in re.finditer(r'<section (?:id="consulta" )?class="section local-consult">.*?</section>', t, re.S) if m.start() < ct.start()]
    k = cons[-1].group(0) if cons else ''
    card = k[k.index('<div class="marco-entry">'):-len('</section>')] if '<div class="marco-entry">' in k else ''
    cob = re.search(r'<section id="cobertura" class="section local-coverage">.*?<div><p>(.*?)</p>(<a .*?</a>)</div></section>', t, re.S)
    zona = f'<p class="g-cierre-zona">{cob.group(1)} {cob.group(2)}</p>' if cob else ''
    nuevo = (f'<section id="contacto" class="section local-consult g-cierre"><div><span id="consulta"></span><span id="cobertura"></span>'
             f'{ct.group(1)}{zona}{ct.group(2)}</div>{card}</section>')
    quitar = ([cons[-1]] if card else []) + ([cob] if cob else [])
    if interna: quitar += [m for m in [re.search(r'<section id="metodo" class="section method">.*?</section>', t, re.S)] if m]
    for m in sorted(quitar, key=lambda m: -m.start()):
        if m.start() < ct.start(): t = t[:m.start()] + t[m.end():]
    return t.replace(ct.group(0), nuevo, 1) if ct.group(0) in t else re.sub(r'<section id="contacto" class="section contact">.*?</div></section>', lambda _: nuevo, t, count=1, flags=re.S)


def _bloque(o, b, ruta):
    """Un bloque de la ficha con el diseño de la portada: columnas numeradas, dato con su fuente o plagas con foto."""
    tipo = b.get('tipo')
    cab = _cab(o, b.get('eyebrow', ''), b.get('titulo', ''), b.get('texto', ''))
    if tipo == 'cifras':
        fila = ''.join(f'<article><b>{e(c[0])}</b><p>{e(c[1])}</p>' + (f'<small>{e(c[2])}</small>' if len(c) > 2 else '') + '</article>' for c in b['cifras'])
        return f'<section class="section g g-dato">{cab}<div class="g-dato-fila">{fila}</div></section>'
    if tipo == 'relacionadas' and b.get('de') == 'plagas':
        PL = o['paginas']['plagas']
        sel = [(i, p) for i, p in enumerate(PL) if p['titulo'] in b.get('items', []) and p.get('imagen')]
        base = f'/oficinas/{o["id"]}/'
        car = ''.join(
            f'<article><a class="g-pl-fig" href="{base}plagas/{ruta("plagas", i)}/"><img src="{base}assets/{p["imagen"]}" alt="" loading="lazy"/></a>'
            f'<h3>{e(p["titulo"])}</h3><p class="g-pl-sub">{e(p.get("eyebrow", ""))}</p>'
            f'<p>{e(re.split(r"(?<=[.])\s", p.get("resumen", p.get("intro", "")))[0])}</p>'
            f'<a class="g-mas" href="{base}plagas/{ruta("plagas", i)}/">{e(_t(o, "Ver la guía"))}<span aria-hidden="true">→</span></a></article>'
            for i, p in sel)
        return f'<section class="section g g-plagas">{cab}<div class="g-plagas-grid">{car}</div></section>' if sel else ''
    if b.get('tarjetas') and not tipo:
        lista = any(len(x) > 2 and isinstance(x[2], list) for x in b['tarjetas'])
        cab_t = [_t(o, 'Tema'), _t(o, 'Qué significa')] + ([_t(o, 'Qué revisamos')] if lista else [])
        filas = ''.join(
            f'<tr><td class="g-t-n">{i + 1:02d}</td><th scope="row">{e(x[0])}</th><td data-col="{e(cab_t[1])}">{e(x[1])}</td>'
            + (f'<td data-col="{e(cab_t[2])}"><ul class="g-lista">' + ''.join(f'<li>{e(y)}</li>' for y in (x[2] if len(x) > 2 and isinstance(x[2], list) else [])) + '</ul></td>' if lista else '')
            + '</tr>' for i, x in enumerate(b['tarjetas']))
        tabla = (f'<div class="g-tabla-marco"><table class="g-tabla"><thead><tr><th scope="col" aria-label="{e(_t(o, "Número"))}"></th>'
                 + ''.join(f'<th scope="col">{e(h)}</th>' for h in cab_t) + f'</tr></thead><tbody>{filas}</tbody></table></div>')
        return (f'<section class="section g g-bloque">{cab}{tabla}'
                + (f'<p class="g-nota">{e(b["nota"])}</p>' if b.get('nota') else '') + '</section>')
    return ''


def internas(o, carpeta, ruta):
    """Servicios y plagas: cada bloque viejo del catálogo (guidance, stats, pests) pasa al diseño de la portada."""
    for clase in ('servicios', 'plagas'):
        for i, pg in enumerate(o['paginas'][clase]):
            f = carpeta / clase / ruta(clase, i) / 'index.html'
            if not f.exists() or not pg.get('bloques'): continue
            t = f.read_text(encoding='utf-8')
            rep = []
            for m in re.finditer(r'<section class="section (?:detail-guidance|detail-stats|pests)">.*?</section>', t, re.S):
                h = re.search(r'<h2>(.*?)</h2>', m.group(0), re.S)
                if not h: continue
                tit = re.sub(r'<br/?>', '\n', h.group(1))
                b = next((b for b in pg['bloques'] if e(b.get('titulo', '')) == tit), None)
                nuevo = _bloque(o, b, ruta) if b else ''
                if nuevo: rep.append((m, nuevo))
            if not rep: continue
            for m, nuevo in sorted(rep, key=lambda x: -x[0].start()):
                t = t[:m.start()] + nuevo + t[m.end():]
            f.write_text(_estilo(t), encoding='utf-8')


def _enlace_zona(t, o):
    """Si la oficina no tiene filtro de cobertura (sin territorio), el enlace del catálogo («Consultar mi zona») pasa al mismo texto que usan el menú y las otras oficinas."""
    return re.sub(r'(<p class="g-cierre-zona">.*?<a class="text-link"[^>]*>)[^<]*(</a>)', lambda m: m.group(1) + e(_t(o, 'Consultar cobertura')) + m.group(2), t, count=1, flags=re.S)


def _zona(t, terr, o=None):
    """Filtro de cobertura (app/src/inbound/territorios/<id>.json): región de una lista oficial, municipio, código postal
    opcional y tipo de espacio. /oficinas/assets/zona.js arma el mensaje y abre el chat con él escrito."""
    o = o or {}
    if not terr or 'data-zona' in t: return _enlace_zona(t, o) if 'data-zona' not in t else t
    m = re.search(r'<p class="g-cierre-zona">(.*?)\s*(<a [^>]*data-chat-prompt="([^"]*)"[^>]*>[^<]*</a>)</p>', t, re.S)
    if not m: return t
    n1, n2, cp = terr['nivel1'], terr['nivel2'], terr.get('codigoPostal')
    opciones = ''.join(f'<option>{e(x)}</option>' for x in terr['lista'])
    cp_html = (f'<label>{e(_t(o, "Código postal"))} <small>{e(_t(o, "(opcional)"))}</small><input name="cp" inputmode="numeric" maxlength="{cp}" '
               f'pattern="[0-9]{{{cp}}}" autocomplete="postal-code"/></label>') if cp else ''
    espacios = ''.join(f'<label class="g-zona-op"><input type="radio" name="espacio" value="{e(x)}"{" checked" if i == 0 else ""}/>{e(x)}</label>'
                       for i, x in enumerate(_t(o, s) for s in ('Hogar', 'Comercio', 'Industria')))
    # zona.js arma el mensaje con estas etiquetas; sin data-t-* usa el español de siempre.
    txt_zona = (f' data-t-cp="{e(_t(o, "Código postal"))}" data-t-espacio="{e(_t(o, "Espacio"))}"'
                f' data-t-consulta="{e(_t(o, "Quiero consultar la cobertura."))}"'
                + (' data-t-sep="\u00a0: "' if o.get('language') == 'fr' else '') if o.get('language', 'es') != 'es' else '')
    form = (f'<form class="g-zona" data-zona data-n1="{e(n1)}" data-n2="{e(n2)}"{txt_zona}><p class="g-zona-txt">{m.group(1)}</p>'
            f'<div class="g-zona-campos"><label>{e(n1)}<select name="n1" required><option value="">{e(_t(o, "Elegir"))}</option>{opciones}</select></label>'
            f'<label>{e(n2)}<input name="n2" autocomplete="address-level2"/></label>{cp_html}</div>'
            f'<fieldset class="g-zona-espacio"><legend>{e(_t(o, "Espacio"))}</legend>{espacios}</fieldset>'
            f'<div class="g-zona-acciones"><button type="submit" class="button">{e(_t(o, "Consultar cobertura"))}</button>{re.sub(r">[^<]*<", ">" + e(_t(o, "Prefiero escribirlo")) + "<", m.group(2), count=1)}</div>'
            f'<button type="button" hidden data-abrir-chat data-zona-enviar></button></form>')
    t = t.replace(m.group(0), form, 1)
    return t if 'zona.js' in t else t.replace('</body>', '<script defer src="/oficinas/assets/zona.js"></script></body>', 1)


def _pie_al_final(t):
    """Cierre como globaltni.com/es: la acuarela del lugar va al final del pie, después de las columnas y justo antes
    de la línea del ©, a todo el ancho (en el catálogo sigue arriba: esto es solo de las oficinas)."""
    m = re.search(r'<figure class="footer-place">.*?</figure>', t, re.S)
    if not m or '<div class="footer-legal">' not in t: return t
    if t.index(m.group(0)) > t.index('<div class="footer-columns">'): return t
    fig = m.group(0).replace(' loading="lazy"', '', 1)  # la acuarela carga siempre (con lazy quedaba un hueco gris en páginas cortas)
    t = t.replace(m.group(0), '', 1)
    return t.replace('<div class="footer-legal">', fig + '<div class="footer-legal">', 1)


def _pie(t):
    """Pie en acordeón como globaltni: cada columna de enlaces es un <details> abierto; /oficinas/assets/pie.js los
    cierra en celular (≤760 px) y en computadora no deja cerrarlos. «Hablemos» queda siempre a la vista."""
    if 'class="pie-col"' in t: return t
    m = re.search(r'<div class="footer-columns">.*?<div class="footer-office">', t, re.S)
    if not m: return t
    nuevo = re.sub(r'<nav aria-label="([^"]*)"><h2>([^<]*)</h2>(.*?)</nav>',
                   lambda x: f'<details class="pie-col" open><summary>{x.group(2)}</summary><nav aria-label="{x.group(1)}">{x.group(3)}</nav></details>',
                   m.group(0), flags=re.S)
    t = t.replace(m.group(0), nuevo, 1)
    return t if 'pie.js' in t else t.replace('</body>', '<script defer src="/oficinas/assets/pie.js"></script></body>', 1)


def _video_movil(t, o, carpeta):
    """Carro vertical en celular: si existe assets/<id>-movil.mp4, /oficinas/assets/video-movil.js (sin defer, justo
    después de la portada) cambia el data-src del video antes de que preview.js lo cargue."""
    mp4 = carpeta / 'assets' / f'{o["id"]}-movil.mp4'
    if not mp4.exists() or 'video-movil.js' in t: return t
    import hashlib
    v = hashlib.sha256(mp4.read_bytes()).hexdigest()[:12]
    t = re.sub(r'(<section class="cinema" id="inicio">.*?<video )', lambda m: m.group(1) + f'data-src-movil="/oficinas/{o["id"]}/assets/{o["id"]}-movil.mp4?v={v}" ', t, count=1, flags=re.S)
    i = t.find('</section>', t.find('id="inicio"'))
    return t[:i + 10] + '<script src="/oficinas/assets/video-movil.js"></script>' + t[i + 10:] if i > 0 else t


def _fuentes_relativas(t, f, carpeta):
    """Las letras (@font-face) van con ruta relativa a la página: en una subcarpeta (github.io/<repo>/…) la absoluta /oficinas/assets/… daba 404 y caía a Arial."""
    rel = '../' * (len(f.relative_to(carpeta).parent.parts) + 1)
    return t.replace('url(/oficinas/assets/montserrat-', f'url({rel}assets/montserrat-')


def cierres(carpeta, o=None):
    f_terr = Path(__file__).resolve().parents[1] / 'app/src/inbound/territorios' / f'{(o or {}).get("id", "")}.json'
    terr = json.loads(f_terr.read_text(encoding='utf-8')) if o and f_terr.exists() else None
    for f in carpeta.rglob('index.html'):
        if '/assets/' in str(f): continue
        t = f.read_text(encoding='utf-8')
        n = _pie_al_final(_pie(_zona(_cierre(t, f.parent != carpeta), terr, o or {})))
        n = _fuentes_relativas(n, f, carpeta)
        if o and f.parent == carpeta: n = _video_movil(n, o, carpeta)
        if n != t: f.write_text(_estilo(n), encoding='utf-8')


# ===== Páginas internas con la estructura del master (globaltni.com/en), vuelta 2 (3-nov-2026) =====
# Servicio: miga + título · par «título / prosa / foto / botón» · franjas de prosa · un solo cierre amarillo.
# Plaga: miga · cabecera con foto · barra de plagas · «En esta página» · prosa por sección · cierre.
# Artículo: miga · foto con pie · nota · «En este artículo» · cuerpo · preguntas · «Seguir leyendo» · cierre.
# Legal: miga + título · prosa · cierre. Todo el contenido sale de la ficha (o de la página ya armada): se reacomoda, no se inventa.
# Las tablas «Tema / Qué significa», las cifras sueltas y las galerías del catálogo pasan a prosa; las fuentes quedan en un bloque discreto al final.
def _linea(s): return re.sub(r'\s+', ' ', (s or '').replace('\n', ' ')).strip()


def _fin(s):
    s = s.strip()
    return s if s[-1:] in '.?!:…»' else s + '.'


def _plano(x):
    """Todos los textos de un dato, sea cadena o lista anidada (nunca se recorre una cadena letra por letra)."""
    if isinstance(x, str): return [x]
    return [s for y in (x or []) for s in _plano(y)]


def _fila(cols, f, omit=()):
    """Una fila de tabla de la ficha → un párrafo. Hay dos formas: [[título, breve], [detalles…]] (la de siempre) y
    [etiqueta, valor1, valor2…] con «columnas» (comparaciones y normas). En las planas cada campo va en su propia línea
    («Norma:», «Numeral:», «Qué pide:») y siempre en el mismo orden: primero de dónde sale (norma, numeral, referencia) y al final lo que pide.
    Los campos de «omit» (índices) se dicen una sola vez para todo el grupo (la misma referencia en tres filas seguidas)."""
    if all(isinstance(c, str) for c in f):
        names = cols[1:] if len(cols) == len(f) else [''] * (len(f) - 1)
        campos = [(n, v, k + 1) for k, (n, v) in enumerate(zip(names, f[1:])) if (k + 1) not in omit]
        cita = lambda n: re.search(r'norma|numeral|referencia|fuente', n, re.I)
        campos.sort(key=lambda c: 0 if cita(c[0]) else 1)
        # lo que no es una cita (tamaño, color, qué pide…) sigue a los dos puntos en minúscula, salvo siglas y nombres propios ya escritos con mayúscula interna
        cuerpo = lambda n, v: v if cita(n) or len(v) < 2 or not v[0].isupper() or v[1].isupper() else v[0].lower() + v[1:]
        lineas = ''.join('<span class="s-campo">' + (f'<em>{e(n)}:</em> ' if n else '') + e(cuerpo(n, v)) + '</span>' for n, v, _ in campos)
        return f'<p class="s-ficha"><strong>{e(_fin(f[0]))}</strong>{lineas}</p>'
    cab = _plano(f[0])
    det = _plano(f[1:])
    breve = ' '.join(_fin(x) for x in cab[1:])
    if len(det) >= 2:  # varios puntos: lista, como en las otras páginas (no un párrafo corrido de fragmentos)
        return f'<p><strong>{e(_fin(cab[0]))}</strong> {e(breve)}</p><ul>' + ''.join(f'<li>{e(x)}</li>' for x in det) + '</ul>'
    return f'<p><strong>{e(_fin(cab[0]))}</strong> {e(" ".join([breve] + [_fin(x) for x in det]).strip())}</p>'


def _primera(s):
    """Primera frase de un texto de la ficha (para no repetir el resumen que la tarjeta del programa ya muestra en la misma portada)."""
    m = re.match(r'(.+?[.!?])(\s|$)', (s or '').strip(), re.S)
    return m.group(1) if m else (s or '').strip()


def _minus(items):
    """Lista de sectores en una frase: solo el primero con mayúscula (salvo siglas y nombres propios, que ya traen otra mayúscula en la 2.ª letra)."""
    return [x if i == 0 or len(x) < 2 or not x[0].isupper() or x[1].isupper() else x[0].lower() + x[1:] for i, x in enumerate(items)]


def _parrafos(o, b, ruta):
    """Un bloque de la ficha como párrafos (lo que el master hace con su prosa)."""
    out = []
    if b.get('texto'): out.append(f'<p>{e(b["texto"])}</p>')
    tipo = b.get('tipo')
    if tipo == 'cifras':
        for c in b['cifras']:
            out.append(f'<p><strong>{e(c[0])}</strong> {e(c[1])}' + (f' <small class="s-fuente">{e(c[2])}</small>' if len(c) > 2 else '') + '</p>')
    elif tipo == 'beneficia':
        for g in b.get('grupos', []):
            out.append(f'<p><strong>{e(_fin(g[0]))}</strong> {e(", ".join(_minus(g[1])))}.</p>')
    elif tipo == 'tabla':
        filas, cols = b.get('filas', []), b.get('columnas') or []
        omit, notas = [set() for _ in filas], {}
        if len(filas) > 1 and cols and all(len(f) == len(cols) and all(isinstance(c, str) for c in f) for f in filas):
            for k in range(1, len(cols)):
                if not re.search(r'norma|numeral|referencia|fuente', cols[k], re.I): continue
                i = 0
                while i < len(filas):  # filas SEGUIDAS con la misma cita: se dice una vez para el grupo
                    j = i
                    while j + 1 < len(filas) and filas[j + 1][k] == filas[i][k]: j += 1
                    if j > i:
                        for r in range(i, j + 1): omit[r].add(k)
                        notas.setdefault(i, []).append(f'<p class="s-note"><em>{e(cols[k])}:</em> {e(filas[i][k])}</p>')
                    i = j + 1
        for idx, f in enumerate(filas):
            out.extend(notas.get(idx, []))
            out.append(_fila(cols, f, omit[idx]))
    elif tipo == 'relacionadas':
        base = f'/oficinas/{o["id"]}/'
        kind = b.get('de') if b.get('de') in ('servicios', 'plagas') else 'plagas'  # «de» dice a qué páginas enlaza (antes se asumía plagas y las de servicios se perdían)
        li = ''.join(f'<li><a href="{base}{kind}/{ruta(kind, i)}/">{e(p["titulo"])}</a></li>' for i, p in enumerate(o['paginas'][kind]) if p['titulo'] in b.get('items', []))
        if li: out.append(f'<ul class="s-enlaces">{li}</ul>')
    elif tipo == 'consulta':
        return []  # las opciones del chat viven en el cierre; el master no las repite en cada página
    elif b.get('tarjetas') or b.get('filas'):
        zona = 'zona' in (b.get('titulo', '') + b.get('eyebrow', '')).lower()
        for i, x in enumerate(_zonas(b) if zona else b['tarjetas']):
            if zona:
                tt, d = x[0][0].split(' · ', 1)[-1], x[0][1] + (' ' + ' · '.join(y.rstrip('.') for y in x[1]) + '.' if x[1] else '')
                out.append(f'<p class="s-zona s-zona-{COLOR[i % 3]}"><strong>{e(_fin(tt))}</strong> {e(d)}</p>')
            else:
                out.append(f'<p><strong>{e(_fin(x[0]))}</strong> {e(x[1])}</p>')
                if len(x) > 2 and isinstance(x[2], list): out.append('<ul>' + ''.join(f'<li>{e(y)}</li>' for y in x[2]) + '</ul>')
    if b.get('nota'): out.append(f'<p class="s-note">{e(b["nota"])}</p>')
    return out


def _cierre_master(o, portada_t):
    """Cierre de las páginas internas como el del master: título, una línea y tres salidas, en banda amarilla."""
    ct = re.search(r'<section id="contacto" class="section contact"><div>(.*?)</div>(<div class="contact-channels".*?</div>)</section>', portada_t, re.S)
    h2 = re.search(r'<h2>(.*?)</h2>', ct.group(1), re.S).group(1) if ct else e(_t(o, 'Cuéntanos qué necesitas proteger.'))
    txt = re.search(r'</h2><p>(.*?)</p>', ct.group(1), re.S) if ct else None
    ch = re.findall(r'<a [^>]*>.*?</a>', ct.group(2), re.S) if ct else []
    chat = re.sub(r'class="[^"]*"', 'class="button button-dark"', ch[0], count=1) if ch else ''
    wa = ''.join(re.sub(r'class="[^"]*"', 'class="text-link"', x, count=1) for x in ch[1:])  # WhatsApp, teléfono… lo que la oficina ya tenga
    cob = f'<a class="text-link" href="/oficinas/{o["id"]}/#consulta">{e(_t(o, "Consultar cobertura"))} →</a>'
    return (f'<section id="contacto" class="s-closing"><div class="wrap"><h2>{h2}</h2>' + (f'<p>{txt.group(1)}</p>' if txt else '')
            + f'<div class="s-closing-actions">{chat}{wa}{cob}</div></div></section>')


def _miga(o, items):
    return '<nav aria-label="' + e(_t(o, 'Ruta')) + '">' + '<span aria-hidden="true">/</span>'.join(items) + '</nav>'


def _pagina_main(t, main):
    return re.sub(r'<main id="contenido">.*?</main>', lambda _: '<main id="contenido">' + main + '</main>', t, count=1, flags=re.S)


def _preguntas_html(o, t_old, cls):
    fq = re.search(r'<section class="section faq">.*?</section>', t_old, re.S)
    if not fq: return '', ''
    tit = re.search(r'<h2>(.*?)</h2>', fq.group(0), re.S).group(1)
    qa = re.findall(r'<summary>(.*?)<span.*?</summary>\s*<p>(.*?)</p>', fq.group(0), re.S)
    det = ''.join(f'<details class="ux-answer"><summary><h3>{q}</h3></summary><article><p>{a}</p></article></details>' for q, a in qa)
    return tit, det


def _fuentes_html(t_old):
    fs = re.search(r'<section class="section detail-sources">.*?</section>', t_old, re.S)
    if not fs: return ''
    tit = re.search(r'<h2>(.*?)</h2>', fs.group(0), re.S).group(1)
    nota = re.search(r'<p class="nota">(.*?)</p>', fs.group(0), re.S)
    ol = re.search(r'<ol>.*?</ol>', fs.group(0), re.S)
    return (f'<section class="wrap s-section s-fuentes"><h2>{tit}</h2>' + (f'<p class="s-note">{nota.group(1)}</p>' if nota else '') + (ol.group(0) if ol else '') + '</section>')


def internas_master(o, carpeta, ruta, pais):
    base = f'/oficinas/{o["id"]}/'
    home = carpeta / 'index.html'
    portada_t = home.read_text(encoding='utf-8')
    inicio = f'<a href="{base}">{e(_t(o, "Inicio"))}</a>'
    cierre = _cierre_master(o, portada_t)
    # --- servicios y plagas
    for clase in ('servicios', 'plagas'):
        for i, pg in enumerate(o['paginas'][clase]):
            f = carpeta / clase / ruta(clase, i) / 'index.html'
            if not f.exists(): continue
            t = f.read_text(encoding='utf-8')
            if 's-closing' in t: continue
            hero = re.search(r'<section class="section detail-hero">.*?</section>', t, re.S)
            img = re.search(r'<img [^>]*/?>', hero.group(0)).group(0) if hero and '<img' in hero.group(0) else ''
            btn = re.search(r'<a class="button"[^>]*>.*?</a>', hero.group(0), re.S).group(0) if hero else ''
            bl = [b for b in pg.get('bloques', []) if b.get('tipo') != 'consulta']
            tit_fq, det = _preguntas_html(o, t, 'faq')
            fq = (f'<section class="wrap s-section s-preguntas"><h2>{tit_fq}</h2><div class="s-prose">{det}</div></section>' if det else '')
            fu = _fuentes_html(t)
            if clase == 'servicios':
                p0 = _parrafos(o, bl[0], ruta) if bl else []
                fig = f'<figure class="s-figure">{img}</figure>' if img else ''
                main = (f'<section class="wrap s-intro">{_miga(o, [inicio, e(_t(o, "Servicios")), e(pg.get("eyebrow", pg["titulo"]))])}<h1>{e(pg.get("eyebrow", pg["titulo"]))}</h1></section>'
                        f'<section class="wrap s-section s-lead-pair"><article class="s-prose"><h2>{e(_linea(pg.get("lema", pg["titulo"])))}</h2></article>'
                        f'<article class="s-prose"><p>{e(pg.get("intro", ""))}</p>{"".join(p0)}</article>{fig}{btn.replace("class=\"button\"", "class=\"button s-service-action\"").replace("</a>", " →</a>") if btn else ""}</section>')
                for b in bl[1:]:
                    ps = _parrafos(o, b, ruta)
                    if ps: main += f'<section class="wrap s-section s-flow"><h2>{e(_linea(b.get("titulo", "")))}</h2><article class="s-prose">{"".join(ps)}</article></section>'
            else:
                fam = ''.join(f'<a href="{base}plagas/{ruta("plagas", j)}/"' + (' aria-current="page"' if j == i else '') + f'>{e(p["titulo"])}</a>' for j, p in enumerate(o['paginas']['plagas']))
                secs, idx = [], []
                for n, b in enumerate(bl, 1):
                    ps = _parrafos(o, b, ruta)
                    if not ps: continue
                    if n == 1 and b.get('tarjetas') and not b.get('tipo'):
                        ps = [f'<h3>{e(x[0])}</h3><p>{e(x[1])}</p>' for x in b['tarjetas']]
                    tt = _linea(b.get('titulo', ''))
                    secs.append(f'<section class="pest-copy" id="guia-{n}"><h2 id="guia-{n}-title">{e(tt)}</h2>{"".join(ps)}</section>')
                    idx.append(f'<li><a href="#guia-{n}">{e(tt)}</a></li>')
                lema = ''  # el lema de la ficha ya no se repite: la cabecera lleva el nombre de la plaga y la entrada, como el master
                ficha = (f'<figure class="pest-figure pest-hero-figure">{img}</figure>') if img else ''
                main = (f'<div class="wrap pest-wrap"><nav class="pest-breadcrumb" aria-label="{e(_t(o, "Ruta"))}">{inicio}<span aria-hidden="true">/</span><span>{e(_t(o, "Guía de plagas"))}</span><span aria-hidden="true">/</span><span>{e(pg["titulo"])}</span></nav>'
                        f'<header class="pest-masthead"><div><p class="pest-eyebrow">{e(_t(o, "Guía de plagas"))}</p><h1>{e(pg["titulo"])}</h1><p class="pest-lead">{e(pg.get("intro", ""))}</p>'
                        f'<div class="pest-hero-actions">{btn.replace("</a>", " →</a>")}<a class="text-link" href="#guia-{0 if lema else 1}">{e(_t(o, "Explorar esta guía"))} ↓</a></div></div>{ficha}</header>'
                        f'<nav class="pest-families" aria-label="{e(_t(o, "Guía de plagas"))}">{fam}</nav>'
                        f'<div class="pest-layout"><aside class="pest-sidebar"><details class="pest-index" id="reading-index"><summary>{e(_t(o, "En esta página"))} <span>−</span></summary><ol>{"".join(idx)}</ol></details></aside>'
                        f'<div class="pest-content">{"".join(secs)}</div></div></div>' + fq + fu)
                fq = fu = ''
            main += fq + fu + cierre
            f.write_text(_estilo(_pagina_main(t, main)), encoding='utf-8')
    # --- artículos del blog
    for f in sorted((carpeta / 'blog').glob('*/index.html')):
        t = f.read_text(encoding='utf-8')
        if 's-closing' in t: continue
        art = re.search(r'<article class="section blog-articulo">.*?</article>', t, re.S)
        if not art: continue
        a = art.group(0)
        g = lambda rx: (re.search(rx, a, re.S) or [None, ''])[1]
        tema, h1, entrada, meta = g(r'<p class="eyebrow">(.*?)</p>'), g(r'<h1>(.*?)</h1>'), g(r'<p class="blog-entrada">(.*?)</p>'), g(r'<p class="blog-meta">(.*?)</p>')
        im = re.search(r'<img class="blog-portada" src="([^"]*)" alt="([^"]*)"', a)
        cuerpo = re.search(r'<div class="blog-cuerpo">(.*)</div></article>', a, re.S).group(1)
        n = iter(range(1, 99))
        cuerpo = re.sub(r'<h2>', lambda m: f'<h2 id="art-{(k := next(n))}">', cuerpo)
        idx = ''.join(f'<li><a href="#art-{i}">{h}</a></li>' for i, h in enumerate(re.findall(r'<h2 id="art-\d+">(.*?)</h2>', cuerpo, re.S), 1))
        tit_fq, det = _preguntas_html(o, t, 'faq')
        if det: cuerpo += f'<h2 class="sin-num">{tit_fq}</h2><div class="s-prose">{det}</div>'
        rels = re.findall(r'<article class="blog-card">.*?<h2><a href="([^"]+)">(.*?)</a></h2>', t, re.S)
        otros = ''.join(f'<li><a href="{h}">{x}</a></li>' for h, x in rels[1:])
        sig = (f'<section class="wrap closeout-blog-next"><div><p class="closeout-blog-eyebrow">{e(_t(o, "Seguir leyendo"))}</p><h2>{rels[0][1]}</h2>'
               f'<a class="text-link" href="{rels[0][0]}">{e(_t(o, "Leer el artículo"))} →</a>' + (f'<ul class="s-enlaces closeout-otros">{otros}</ul>' if otros else '')
               + f'</div><a class="text-link" href="{base}blog/">{e(_t(o, "Ver todos los artículos"))} →</a></section>') if rels else ''
        fig = (f'<figure class="s-figure"><img src="{im.group(1)}" alt="{im.group(2)}"/><figcaption>{im.group(2)}</figcaption></figure>') if im else ''
        main = (f'<section class="wrap s-intro">{_miga(o, [inicio, f"<a href=\"{base}blog/\">{e(_t(o, "Blog"))}</a>", e(tema)])}<h1>{h1}</h1>{fig}</section>'
                f'<section class="wrap s-section s-prose"><p class="s-note">{meta}</p><p class="s-entrada">{entrada}</p></section>'
                f'<nav class="wrap s-index ux-index" aria-label="{e(_t(o, "En este artículo"))}"><details><summary>{e(_t(o, "En este artículo"))}</summary><ul>{idx}</ul></details></nav>'
                f'<section class="wrap s-section s-article"><div class="article-body">{cuerpo}</div></section>' + _fuentes_html(t) + sig + cierre)
        f.write_text(_estilo(_pagina_main(t, main)), encoding='utf-8')
    # --- índice del blog: «Leer guía» del catálogo → el mismo «Leer el artículo →» de la portada, SOLO en los enlaces de las tarjetas
    fb = carpeta / 'blog' / 'index.html'
    if fb.exists():
        tb = fb.read_text(encoding='utf-8')
        card = lambda m: re.sub(r'(<a class="text-link"[^>]*>)[^<]*(</a>)', lambda x: x.group(1) + e(_t(o, 'Leer el artículo')) + ' →' + x.group(2), m.group(0))
        nb = re.sub(r'<article class="blog-card.*?</article>', card, tb, flags=re.S)
        if nb != tb: fb.write_text(nb, encoding='utf-8')
    # --- páginas legales
    for nombre in ('privacidad', 'terminos', 'accesibilidad'):
        f = carpeta / nombre / 'index.html'
        if not f.exists(): continue
        t = f.read_text(encoding='utf-8')
        if 's-closing' in t: continue
        lc = re.search(r'<section class="section legal-content">.*?</section>', t, re.S)
        if not lc: continue
        h1 = re.search(r'<h1>(.*?)</h1>', lc.group(0), re.S).group(1)
        ps = ''.join(re.findall(r'<(?:p|ul|ol)(?: [^>]*)?>.*?</(?:p|ul|ol)>', re.sub(r'<p class="eyebrow">.*?</p>', '', lc.group(0), flags=re.S), re.S))
        main = (f'<section class="wrap s-intro">{_miga(o, [inicio, h1])}<h1>{h1}</h1></section>'
                f'<section class="wrap s-section s-prose">{ps}</section>' + cierre)
        f.write_text(_estilo(_pagina_main(t, main)), encoding='utf-8')


def aplicar(o, carpeta, ruta, pais):
    portada(o, carpeta, ruta, pais)
    internas_master(o, carpeta, ruta, pais)
    hogares(o, carpeta, ruta)
    internas(o, carpeta, ruta)
    cierres(carpeta, o)
