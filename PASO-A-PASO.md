# Truly Nolen Costa Rica · borrador y pasos para terminar

## Cómo ver el borrador
Doble clic en **abrir-sitio.bat**. Se abre http://127.0.0.1:8790/oficinas/costa-rica/

## Cómo corregir
1. Cambiar el texto en `ficha/costa-rica.json` (todo el contenido está ahí).
2. Correr `uv run --python 3.12 python generar.py`. Ese comando rehace las 13 páginas y revisa enlaces, imágenes y trato de usted.
3. Recargar el navegador.

## Qué está hecho
- [x] Investigación del país con fuentes (`docs/investigacion.md`)
- [x] Ficha del país (`ficha/costa-rica.json`) con el formato de la skill
- [x] Inicio, 3 servicios (hogares, comercios, industria), 6 plagas y 3 páginas legales, todo en trato de usted
- [x] Portada (película) y footer del machote oficial de Costa Rica (Volcán Arenal)
- [x] Chat de Truly AI con contexto de Costa Rica (usted, sin datos inventados de oficina)
- [x] SEO básico: título, descripción, canonical, Open Graph, datos estructurados y `sitemap.xml`
- [x] Revisión a 1280 y 390 px: sin desbordes ni enlaces rotos
- [x] **Blog** (`/blog/`) con 4 artículos verificados, en goteo de 2 por día (`ficha/blog/*.json`):
  - 30-oct: «Cómo eliminar el comején» y «Dengue en Costa Rica: cómo acabar con los zancudos en casa»
  - 31-oct: «Zompopas en el jardín» y «Ratas y leptospirosis»
  - Solo sale lo que tiene fecha de hoy o anterior (hora de Costa Rica). `abrir-sitio.bat` regenera al abrirse, así que el 31 aparecen solos.
  - Cada artículo trae migas, fecha, minutos de lectura, FAQ, fuentes visibles y artículos relacionados, más BlogPosting, FAQPage y BreadcrumbList.
- [x] 30-oct: 3 plagas nuevas (chinches de cama, moscas, pulgas y garrapatas), fuentes nuevas en el blog (boletín oficial del Ministerio de Salud N.º 39, TEC, UCR, CCSS, Acta Médica) y 2 artículos más para el 1-nov. Abejas quedó fuera: la Ley 9929 asigna los enjambres a SENASA y Bomberos.
- [x] 30-oct: fotos elegidas por el dueño en `/_elegir/` (hogar c, casa h, comercio c, industria e, chinches a). Sus créditos de licencia están en Términos de uso. Para cambiar otra vez: `uv run --python 3.12 python elegir.py` y abrir http://127.0.0.1:8790/_elegir/
- [x] **Ronda de pulido 1 (30-oct):** 23 páginas a 1280 y 390 px, chat, enlaces, anclas, imágenes, consola y SEO.
  - Hallazgos corregidos: 7 descripciones de Google de más de 160 caracteres, enlaces de los créditos que se salían en celular, foto vertical de Comercios (recortada a 4:3) y hueco junto al segundo artículo del blog.
  - Blog: se agregaron «Cómo prevenir cada plaga» (9 consejos con dibujo y fuente) y un bloque de consulta.
  - Segunda pasada: 0 hallazgos. Enlaces externos que bloquean programas automáticos pero abren en el navegador: CDC, Q Costa Rica, Utah. CATIE caído temporalmente (522).
  - Auditoría: `tools/auditoria.py` en el scratchpad de la sesión (Playwright con Edge).
- [x] 30-oct: carrito de Truly fijo en la esquina superior izquierda de la portada, «rodando en su sitio».
  - Ruedas que giran (tira de 4 cuadros `cr-carrito-truly-rueda.webp`), vibración de motor, baches suaves, líneas de velocidad y sombra.
  - Sale de `Desktop/carrito-truly/carro-con-bigotes-cuadro1.jpg`. Esa carpeta dice «PRÁCTICA, no se publica»: **confirmar con Roger o Pablo antes de publicar**.
  - Posición y tamaño en `ficha/costa-rica.json` → `carrito`.
- [x] **Ronda de pulido 2 (30-oct):** auditoría completa con 0 hallazgos y los 6 artículos limpios. Revisiones nuevas: texto, archivos sin usar, movimiento reducido y carrito en 9 tamaños de pantalla.
  - Corregido: se borraron dos archivos sin usar (`footer-costa-rica.png` de 2,8 MB y el carrito viejo). En pantallas muy bajas, como 1280 × 720, el carrito se oculta en vez de tapar el texto. El blog no deja huecos con 2, 4 o 6 artículos.
  - Falso positivo: «Rattus rattus» es el nombre científico.
- [ ] Ronda de pulido 3 (mínimo; se termina cuando una ronda completa sale sin hallazgos)
- [x] Imagen para redes 1200×630 (`costa-rica-social.jpg`) con `og:image` en todas las páginas, y favicon

## Lo que falta (en orden)
1. **Confirmar con el dueño** la investigación: trato (usted), la lista de 6 plagas y la portada.
2. **Oficina:** confirmar si la oficina de Costa Rica (trulynolencr.com, 2258-0608) quiere sus canales en el sitio. Si dice que sí: `contacto: "oficina"`, el bloque `oficina{}` y los `legales` de la oficina.
3. **Portada propia con el carrito de Truly** (método de la skill, «Portada con el carrito»). Pide Midjourney y ffmpeg (`winget install Gyan.FFmpeg`).
4. **Fotos propias de Costa Rica (paso 6):** técnicos costarricenses con el emblema real; cocina, comercio e industria nuevos; ilustración de zompopa.
5. **Imagen para redes:** hoy sale de la portada del catálogo. Cuando exista la portada con el carrito, rehacerla desde el cuadro 0 del video.
6. **Portadas del blog:** comején, zancudos y ratas son fotos reales de Truly (las de zancudos y ratas son de EE. UU.). La de zompopas es de Wikimedia Commons (Hans Hillewaert, CC BY-SA 4.0, con crédito visible en el artículo). Lo ideal es reemplazarlas por fotos de la oficina de Costa Rica.
7. **Más artículos:** seguir el goteo de 2 por día (temas sugeridos: cucarachas y alergias, alacranes, permiso sanitario para negocios). Para agregar uno, se crea otro `ficha/blog/<slug>.json` con su `fecha`.
8. **Repo oficial:** pedir acceso a `Catalizadora-Labs/truly-inbound` y el paquete de la capa de oficinas a Roger. Pasar la ficha al generador oficial y correr `gate-oficinas.mjs`.
9. **Rondas de pulido:** 3 o 4, hasta que una ronda completa salga sin hallazgos.
10. **Publicar:** PR en borrador y publicación solo con el ok de Roger.

## Avisos
- El chat se ve, pero desde `127.0.0.1` puede no responder: el servidor de Truly AI solo atiende a dominios autorizados.
- El texto interno del chat (`chat/es.json`) viene en tú. Es un límite conocido de la skill.
