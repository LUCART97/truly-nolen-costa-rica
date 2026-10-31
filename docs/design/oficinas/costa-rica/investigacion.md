# Investigación del país · Costa Rica (paso 2 de la receta truly-inbound)

Fecha: 31-oct-2026 · id: `costa-rica` · Idioma: español · Trato en el sitio: usted
Estado: **borrador del investigador; falta la «Comprobación propia» y el ok del dueño.**

Regla de este archivo: cada dato lleva su dirección y una cita corta de la fuente, abierta hoy (31-oct-2026).
Lo que no pude abrir o comprobar está en «Lo que no encontré». Este archivo reemplaza a `docs/investigacion.md`
(30-oct), que tenía dos errores: decía que el sitio de la oficina «no publica correo ni WhatsApp» (sí los publica,
ver 1.1) y citaba 5.302 casos de dengue (cifra vieja; la vigente está en 3.1).

---

## 1. Contacto y lo que el sitio nuevo tiene que hacer mejor

### 1.1 Contacto que la oficina pone al frente (sitio trulynolencr.com)

| Canal | Dato | Dónde aparece | Cita / prueba |
|---|---|---|---|
| Teléfono (central) | **2258-0608** | Cabecera de todas las páginas, enlace `tel:` | https://www.trulynolencr.com/ — `<a href="tel:2258-0608" … aria-label="Telefono: 2258-0608">` |
| WhatsApp | **+506 6303-3868** (`wa.me/50663033868`) | Botón de cabecera «SOLICITA TU INSPECCION» en todas las páginas | https://www.trulynolencr.com/ — `<button … onclick="window.open('https://wa.me/50663033868', '_blank');" > SOLICITA TU INSPECCION` |
| Correo | **info@trulynolencr.com** | Solo al pie de 2 páginas | https://www.trulynolencr.com/in2care/ y https://www.trulynolencr.com/servicio-especializado-de-sanitizacion/ — «Contáctenos: Telefono: 2258-0608 Whatsapp: https://wa.me/5066303868 Email: info@trulynolencr.com» |
| Redes | Facebook `facebook.com/trulynolencr/`, Instagram `@trulynolen.cr`, X `twitter.com/TrulyNolencr`, YouTube (canal UC9ARwLs2pBO5boOIWmMF04A) | Barra de íconos | https://www.trulynolencr.com/ (enlaces `href` en el HTML) |
| Dirección física | **No la publica** | — | Ninguna de las 11 páginas bajadas a `sitio-actual/` la tiene |
| Horario | **No lo publica** | — | Ídem |
| Legales | Solo **Políticas de Privacidad** | https://www.trulynolencr.com/politicas-de-privacidad/ | «El presente Política de Privacidad establece los términos…». `/terminos-y-condiciones/` responde **404** (probado hoy con curl). No hay página de accesibilidad. |

El registro interno `app/src/datos/franquicias.ts` no se pudo revisar (sin acceso al repo).

### 1.2 Lo que el sitio nuevo tiene que hacer mejor (todo comprobado hoy)

1. **WhatsApp roto en dos páginas.** En /in2care/ y /servicio-especializado-de-sanitizacion/ el enlace es
   `https://wa.me/5066303868` (le falta un dígito; WhatsApp lo abre como `phone=5066303868`, un número que no existe).
   El correcto, el del botón de cabecera, es `wa.me/50663033868`.
2. **El botón principal no es un enlace.** «SOLICITA TU INSPECCION» es un `<button>` que abre WhatsApp con
   JavaScript (`onclick="window.open(…)"`). En el sitio nuevo tiene que ser un enlace normal `https://wa.me/50663033868`.
3. **El correo está escondido**: solo sale al pie de dos páginas de producto (1.1).
4. **«Cotizar en línea» no funciona.** https://www.trulynolencr.com/cotizar-en-linea/ muestra el código crudo del
   formulario en vez del formulario: «[contact-form-7 id=»499″ title=»Sin título»]».
5. **«Contáctenos» no tiene ningún dato de contacto.** https://www.trulynolencr.com/contactenos/ solo trae el bloque
   genérico «La satisfacción del cliente es nuestro principal objetivo…».
6. **Página vacía:** https://www.trulynolencr.com/servicios-de-limpieza/ solo tiene el título y el bloque genérico.
7. **«Buscador de Plagas»**: el menú apunta a https://www.trulynolencr.com/buscador-de-plagas/roedores/ (abre, 200),
   pero la página madre https://www.trulynolencr.com/buscador-de-plagas/ da **404**.
8. **Cifras viejas y que se contradicen:**
   - Inicio: «Nos respaldan 78 años de experiencia como fumigadora» (1938 + 78 = 2016) y «actualmente se encuentra en
     57 países» — https://www.trulynolencr.com/
   - Quiénes somos: «a Diciembre del 2016 operan 209 oficinas en 61 países» — https://www.trulynolencr.com/quienes-somos/
9. **Error en el enlace de la casa matriz:** el texto dice «www.tulynoleninternational.com» (sin la r); el `href` sí es
   `https://www.trulynoleninternational.com`, que hoy redirige a `https://globaltni.com/` — https://www.trulynolencr.com/quienes-somos/
10. **Sanitización desactualizada y con otra marca:** la página es casi toda sobre COVID («Recomendaciones COVID»,
    «QUÉDATE EN CASA. SALVA VIDAS.») y promete en nombre de otra empresa: «Clean Service, garantiza todos sus servicios al
    100%… le devolvemos su dinero», mientras el inicio promete «una política de CALLBACK SIN COSTO» —
    https://www.trulynolencr.com/servicio-especializado-de-sanitizacion/ y https://www.trulynolencr.com/
11. **Blog parado desde 2020.** La API del sitio da como artículo más reciente el del 3-mar-2020:
    https://www.trulynolencr.com/wp-json/wp/v2/posts?per_page=3 → `"date":"2020-03-03T12:03:45"` (controle-lo-insectos-voladores-en-casa).
    La página News enlaza además una página de Facebook vieja, «Green-Side-of-Truly-Nolen» — https://www.trulynolencr.com/news/
12. **Faltas de ortografía visibles** (para no copiarlas): «lideres», «valuarte», «PREVENSION», «Telefono», «el cliente no
    esta satisfecho» — quienes-somos, sanitización, inicio.
13. **Falta lo que el sitio nuevo debe tener:** dirección y horario (pedirlos a la oficina; no inventarlos), términos y
    condiciones, accesibilidad.

---

## 2. Trato: cómo escribe LA OFICINA

Citas textuales de sus propias páginas:

1. «Llámenos y le haremos un plan de Manejo Integral de Plagas a la medida de sus necesidades. Llámenos será un gusto poder servirle.» — https://www.trulynolencr.com/soluciones-comerciales/
2. «Es el interior de su hogar donde es esencial un protocolo de servicio discreto pero efectivo.» — https://www.trulynolencr.com/soluciones-residenciales/
3. «¡Sanitice su Oficina, Local comercial e Industria! En Truly Nolen le ofrecemos Servicio Especializado de Sanitización» — https://www.trulynolencr.com/servicio-especializado-de-sanitizacion/
4. «La Compañía Fumigadora y de Control de Plagas más Comprometida con SU Seguridad y Satisfacción» — https://www.trulynolencr.com/
5. «Disfrute de nuestras noticias, tips, recomendaciones, lanzamiento de productos y mucho más.» — https://www.trulynolencr.com/news/
6. «si usted sospecha que le picó una garrapata a su mascota, obsérvelo atentamente» · «Le recomendamos: Revise diariamente a sus mascotas» — https://www.trulynolencr.com/prevenga-garrapatas-en-su-mascota/ (3-mar-2020)
7. «le recomendamos y enfatizamos revisar continuamente esta página» — https://www.trulynolencr.com/politicas-de-privacidad/

**Conclusión: usted.** No apareció voseo (busqué «vos», «tenés», «podés» en los 11 `.txt`: cero).

**Excepciones en tú (no copiarlas):**
- Botón de cabecera en todas las páginas: «SOLICITA TU INSPECCION» (además sin tilde). En el sitio nuevo: «Solicite su inspección».
- Bloque COVID copiado en sanitización: «LLAMA si tienes síntomas».
- Un artículo de 2020: «Asegúrate de que estas sustancias están selladas… No te sorprendas si te encuentras cucarachas en el fregadero» — https://www.trulynolencr.com/no-mas-cucarachas/
- Texto técnico del reproductor: «Tu navegador no soporta el elemento video» — inicio.

---

## 3. Plagas con nombre local y fuente del país

Nombres científicos comprobados hoy en GBIF (`https://api.gbif.org/v1/species/match?name=…`; todos «ACCEPTED», coincidencia exacta).

| # | Plaga (nombre en el sitio) | Nombre científico (GBIF) | Por qué importa en CR (cifra y año) | Fuente del país y cita |
|---|---|---|---|---|
| 1 | **Zancudos** | *Aedes aegypti* (Linnaeus, 1762), GBIF 1651891 | **5.814** casos de dengue a la semana 40 de 2026, frente a **3.798** a la misma semana de 2025; Grecia, el cantón con más casos (683); además 923 casos de chikungunya | Ministerio de Salud, Boletín Epidemiológico N.º 39 (23-oct-2026): «A la semana epidemiológica 40 del año 2026 se notifican 5814 casos acumulados de dengue» · «Para la semana epidemiológica 40 del año 2025 se reportaron 3798 casos» · «Grecia 683 casos» · «923 casos de chikungunya» — https://www.ministeriodesalud.go.cr/index.php/biblioteca-de-archivos-left/documentos-ministerio-de-salud/material-informativo/material-publicado/boletines/boletines-vigilancia-vs-enfermedades-de-transmision-vectorial/boletines-epidemiologicos-2026/11248-boletin-epidemiologico-n-39-4/file · Dónde están los criaderos: «el 90% de los criaderos están dentro de las viviendas» (Ministerio de Salud, 26-ago-2025) — https://www.ministeriodesalud.go.cr/index.php/prensa/62-noticias-2025/2224-dia-internacional-del-dengue-82-menos-casos-de-dengue-pero-la-lucha-continua |
| 2 | **Ratas y ratones** | *Rattus rattus* (GBIF 2439270), *Rattus norvegicus* (2439261), *Mus musculus* (7429082) | **52,6 %** de los casos sospechosos de leptospirosis estudiados (cinco regiones, 2004-2008) reportó roedores | Acta Médica Costarricense 54(4), 2012: «El 52,6% de los casos reporta presencia de roedores» — https://www.scielo.sa.cr/pdf/amc/v54n4/art06v54n4.pdf · Ministerio de Salud (2002), reservorios de leptospirosis: «los más frecuentes son: ratas, perros» — https://www.binasss.sa.cr/opac-ms/media/digitales/Leptospirosis%20-%20Protocolo%20para%20Prevenci%c3%b3n%20y%20Control.pdf |
| 3 | **Cucarachas** | *Periplaneta americana* (GBIF 2000152), *Blattella germanica* (1997215) | **68 %** de 80 pacientes alérgicos severos de CR reaccionó a algún extracto de cucaracha; **61,3 %** a la americana (estudio de Calderón y otros, 1992) | Calderón, O. «Las cucarachas domésticas como inductoras de alergia», Rev. Costarricense de Salud Pública 2(2): «61,3% fue reactivo a Periplaneta americana. 68% de la población estudiada reaccionó a por lo menos uno de los extractos» — https://www.binasss.sa.cr/revistas/rcsp/v2n2/art9.pdf |
| 4 | **Hormigas y zompopas** | *Atta cephalotes* (Linnaeus, 1758), GBIF 5035748 | La zompopa más común del país; un investigador la llama «posiblemente la más común en el país» (2026) | Observador.cr (14-jun-2026): «constituyen una plaga de gran relevancia, posiblemente la más común en el país» — https://observador.cr/cada-vez-hay-mas-zompopas-en-las-ciudades-asi-influyen-el-cambio-climatico-y-la-deforestacion/ · Longino, Ants of Costa Rica: «This is the most common species of Atta in Costa Rica» — https://ants.biology.utah.edu/genera/atta/species/cephalotes/cephalotes.html |
| 5 | **Comején** | *Cryptotermes brevis* (Walker, 1853), GBIF 2007322 | La termita de madera seca es «el problema más frecuente en nuestras construcciones»; en 2006, maderas del Teatro Nacional «fuertemente dañadas» | Kurú: Revista Forestal (TEC), 2006: «ya que son el problema más frecuente en nuestras construcciones» · «el caso del Teatro Nacional en San José… se encuentran fuertemente dañadas por termitas de madera seca» — https://dialnet.unirioja.es/descarga/articulo/5123386.pdf · Nombre local: «Costa Rican Spanish uses them interchangeably, and comején more commonly» (Tico Times, 23-feb-2007, citando al Museo de Insectos de la UCR) — https://ticotimes.net/2007/02/23/who-are-these-guys-anyway |
| 6 | **Alacranes** | *Centruroides margaritatus* (GBIF 6894223) y *Tityus pachyurus* (6893843) — ver nota | De **24** picaduras en 1992 a **405** en 1999; los alacranes ticos no son letales | CRHoy (27-ene-2017), estudio del Instituto Clodomiro Picado con datos del Centro Nacional de Intoxicaciones: «en 1992 se reportaron 24 casos… y en 1999 la cifra se duplicó a 405» · «en nuestro país no son letales» — https://crhoy.com/ciencia/les-tiene-miedo-los-alacranes-ticos-no-son-letales/ |
| 7 | **Chinches de cama** | *Cimex lectularius* Linnaeus, 1758, GBIF 2021062 | Primera confirmación molecular de la especie en Centroamérica, en un apartamento de Heredia (UCR, 2020) | Kimuk/CONARE (UCR): «the first molecular confirmation of C. lectularius in Central America. Specimens were obtained from an apartment located in Heredia, Costa Rica» — https://kimuk.conare.ac.cr/Record/KUCR_26f9e992aae36e101786d7e40a925321 |
| 8 | **Moscas** | *Musca domestica* (GBIF 1524843); *Stomoxys calcitrans* (1526081), «mosca de la piña» o «del establo» | Emergencia sanitaria por la mosca del establo en **10** cantones (Decreto 39902-MAG, 2016); Salmonella en moscas domésticas de San José (UCR, 1959) | Semanario Universidad (12-oct-2016): «una emergencia sanitaria al menos por un año en diez de los 81 cantones del país» · «La mosca Stomoxys calcitrans… Decreto N° 39902-MAG» — https://semanariouniversidad.com/pais/brote-moscas-hematofagas-genera-emergencia-sanitaria/ · Bolaños (1959), Rev. Biología Tropical 7(2): ficha del artículo — https://archivo.revistas.ucr.ac.cr//index.php/rbt/article/view/29946 (ver «Lo que no encontré» sobre el 24 %) |
| 9 | **Pulgas y garrapatas** | *Rhipicephalus sanguineus* (GBIF 2183597), *Ctenocephalides felis* (1419472) | La garrapata del perro es «la principal transmisora de enfermedades en Costa Rica» (2026) | Teletica (18-jul-2026): «la garrapata del perro (Rhipicephalus sanguineus) es la principal transmisora de enfermedades en Costa Rica» · «Ehrlichiosis canina: provoca fiebre, hemorragias y daño en distintos órganos» — https://www.teletica.com/mascoticas/nuevo-virus-detectado-en-garrapatas-en-costa-rica-como-afecta-a-sus-mascotas_413680 |
| — | **Abejas (no va)** | *Apis mellifera* (GBIF 1341976) | La Ley 9929 declara la apicultura de interés público y manda los enjambres a SENASA y a Bomberos (ver 4.3). La ley **no prohíbe** expresamente a las fumigadoras; se descarta por coherencia con la ley y porque el país ya tiene a quién llamar. | Ley 9929, art. 3: «Al Servicio Nacional de Salud Animal (SENASA) le corresponderá la recuperación y el manejo de enjambres y colmenas silvestres» — https://bufetedecostarica.com/wp-content/uploads/2026/10/ley-9929_declaracion-de-interes-publico-de-la-apicultura-como-activid.pdf |

Notas:
- Alacranes: los nombres científicos son de géneros/especies presentes en CR según el reportaje («la especie Tityus
  pachyurus… en Costa Rica existe, pero no es letal»); *Centruroides margaritatus* no está citado en esa fuente: si se
  usa en el sitio, falta fuente del país.
- Otras plagas que la oficina ya trata en su sitio y que podrían sumarse: arañas, avispas, ácaros, insectos de granos,
  polilla, aves (lista del «Buscador de Plagas»: https://www.trulynolencr.com/buscador-de-plagas/roedores/ — «Cucaracha
  Oriental Cucaracha Germánica Termitas Moscas Aves Hormigas Garrapatas Avispas Polilla de la ropa Pulgas Araña Insectos
  de granos»). No les busqué fuente del país.

**Recomendación para el menú del dueño (6):** zancudos, ratas y ratones, cucarachas, comején, hormigas y zompopas,
chinches de cama. Son las que tienen la fuente más fuerte y más reciente del país (2026 para zancudos y zompopas; UCR
para chinches) y las que más pesan para negocios (cocinas, hoteles, bodegas). Alacranes, moscas y pulgas/garrapatas
quedan de reserva: sus cifras son de 1999, 1959/2016 o de mascotas.

---

## 4. Normas

### 4.1 Decreto Ejecutivo 38335-S-MTSS (La Gaceta 6-may-2014)
«Reglamento para regular la actividad de control de plagas mediante la aplicación de plaguicidas de uso doméstico y
profesional». Texto: https://www.binasss.sa.cr/opac-ms/media/digitales/Regulaci%c3%b3n%20de%20la%20actividad%20de%20control%20de%20plagas%20mediante%20la%20aplicaci%c3%b3n%20de%20plaguicidas%20de%20uso%20dom%c3%a9stico%20y%20profesional.pdf
(misma copia en FAOLEX: https://faolex.fao.org/docs/pdf/cos137379.pdf)

- **Art. 2 (a quién aplica):** «a todas las personas físicas y jurídicas que se dediquen al control de plagas… en áreas
  o espacios interiores exteriores de viviendas, edificios, instalaciones públicas y privadas, industrias, comercios…»
- **Art. 5 (permiso):** para el permiso sanitario de funcionamiento deben cumplir este reglamento «y lo establecido en el
  "Reglamento General para el Otorgamiento de Permisos Sanitarios de Funcionamiento del Ministerio de Salud"».
- **Art. 6 (lo que se presenta con la solicitud del permiso):** inciso a) «Un listado de los plaguicidas a utilizar
  indicando nombre genérico y nombre comercial y el número de registro del Ministerio de Salud»; inciso b) **la hoja de
  servicio**, que debe contener: «Nombre de la empresa controladora de plagas · Representante legal · Dirección de la
  empresa y número de teléfono · Fecha de la aplicación de los productos · Medidas de seguridad que se deben adoptar
  antes, durante y después de la aplicación… · Indicar el tiempo de reingreso al área tratada · Anotar el nombre
  comercial y nombre genérico de los plaguicidas aplicados». Y: «El original se debe entregar al cliente y la copia la
  debe guardar la empresa como comprobante del servicio prestado».
- **Art. 7 (vigencia):** «el permiso sanitario de funcionamiento… tendrá una vigencia de un año».
- **Art. 20 (rótulos):** en áreas donde confluyen personas y mayores de 500 m², «debe colocar rótulos y pictogramas que
  prohíban el paso… hasta que se cumplan los periodos de reingreso».
- **Art. 21.2 (técnicos):** «debe contar con el curso de manejo de plaguicidas de uso doméstico y profesional».
- **Art. 4 k) y l):** plaguicida doméstico = categoría IV OMS; profesional = categorías II, III o IV, «Solo pueden ser
  aplicados por personal autorizado y capacitado».

### 4.2 Reglamento de permisos sanitarios del Ministerio de Salud
- El 38335 cita el **Decreto 34728-S (2008)**. El reglamento general vigente hoy es el **Decreto 43432-S del 9-mar-2022**,
  «Reglamento General para permisos sanitarios de funcionamiento, permisos de habilitación y autorizaciones para eventos
  temporales de concentración masiva de personas», publicado «en el Alcance 60 a La Gaceta No. 56 del 23 de marzo del
  2022» (así lo cita el Ministerio en su propuesta de reforma MS-AJ-RC-CB-1899-2025:
  https://ministeriodesalud.go.cr/index.php/biblioteca-de-archivos-left/documentos-ministerio-de-salud/ministerio-de-salud/legislacion-sanitaria/consulta-publica/2025/9505-propuesta-al-reformar-los-articulos-14-y-48-inciso-d-del-decreto-ejecutivo-no-43432-s-del-09-de-marzo-del-2022-reglamento-general-para-permisos-sanitarios-de-funcionamiento/file).
- Ese documento dice por qué todo negocio necesita permiso: «por disposición de los artículos 222, 298, 323, 324 y 328
  de la Ley No. 5395… "Ley General de Salud" es obligación de toda persona física o jurídica que desarrolle una actividad
  comercial, industrial y de servicios contar con el Permiso Sanitario de Funcionamiento vigente».
- **Art. 14 del 43432-S (declaración jurada):** «El cumplimiento de las condiciones previas citadas en el Artículo 8°…
  deben ser declaradas por el interesado de la actividad bajo fe de juramento» (texto propuesto en la reforma de 2025;
  no confirmé si ya se publicó).
- **¿Menciona plagas el 43432-S?** No lo sé: no pude abrir el texto completo del decreto (ver «Lo que no encontré»).

### 4.3 Ley 9929 (abejas), 2021
«Declaración de interés público de la apicultura… y declaratoria del Día Nacional de las Abejas y otros Polinizadores».
Texto (copia de Bufete de Costa Rica): https://bufetedecostarica.com/wp-content/uploads/2026/10/ley-9929_declaracion-de-interes-publico-de-la-apicultura-como-activid.pdf
- **Art. 1:** «Se declara de interés publico la apicultura».
- **Art. 3:** «Al Servicio Nacional de Salud Animal (SENASA) le corresponderá la recuperación y el manejo de enjambres y colmenas silvestres».
- **Art. 4:** «El Benemérito Cuerpo de Bomberos responderá cuando se presenten ataques de abejas a personas y animales».
- **Art. 4 bis:** Bomberos «podrá liberar la colonia o el enjambre… en una zona con abundante naturaleza alejada de zonas urbanas».
- **La ley no menciona el control de plagas ni a las fumigadoras.** Lo que dice el sitio debe ser: ante un enjambre,
  llamar a Bomberos o SENASA; no «fumigamos abejas».

### 4.4 Otras
- **Decreto 39902-MAG (2016)**, emergencia por la mosca del establo en 10 cantones (citado en Semanario Universidad, 3.8).
  Es una norma agrícola, no de control de plagas urbanas.
- **Decreto 41435-S** reformó el reglamento de permisos de 2016 (39472-S): https://faolex.fao.org/docs/pdf/cos191027.pdf
  (abre; es el texto «DECRETO EJECUTIVO N° 41435-S»). Histórico; no menciona plagas (búsqueda de «plaga» en el texto: 0).

---

## 5. Negocios típicos y división territorial

### 5.1 Negocios
- **Los que la oficina ya atiende:** «Hoteles · Restaurantes · Hospitales · Supermercados · Plantas de Procesamiento de
  Alimentos · Bodegas · Fabricas» — https://www.trulynolencr.com/soluciones-comerciales/ ; y para sanitización:
  «Restaurantes. Oficinas. Bodegas. Gimnasios. Fabricas. Locales Comerciales. Colegios. Clínicas y hospitales.
  Farmacias. Universidades» — https://www.trulynolencr.com/servicio-especializado-de-sanitizacion/
- **Pulperías:** «In Costa Rica, there are an estimated 18.000 pulperias throughout the country» (Q Costa Rica,
  22-nov-2013) — https://qcostarica.com/costa-rica-pulperias-remain-despite-increase-in-supermarkets-and-convenience-stores ;
  «50% of shopping in Costa Rica is done at pulperías and small neighborhood stores» (Tico Times, 17-abr-2020, citando a
  la asociación de detallistas) — https://ticotimes.net/2020/04/17/the-coronavirus-crisis-and-the-resurgence-of-the-pulperia
- **Sodas** (fondas de comida casera), categoría que el Ministerio de Salud usa al dar permisos: «los bares podrán
  reabrir sus puertas, pero ahora como sodas y restaurantes. Esto luego de una reforma aprobada por el Ministerio de
  Salud» (Observador, 1-sep-2020) — https://observador.cr/bares-podran-reabrir-pero-convertidos-en-sodas-y-restaurantes-tras-permiso-dado-por-salud/
- Palabra local confirmada en fuente oficial: **canoas** (canales del techo): «limpiar periódicamente las canoas»
  (Ministerio de Salud, brote de dengue en Orotina, 2026) — https://ministeriodesalud.go.cr/index.php/prensa/67-noticias-2026/2494-salud-continua-trabajos-en-atencion-al-brote-de-dengue-en-orotina

### 5.2 División territorial
- **7 provincias** (San José, Alajuela, Cartago, Heredia, Guanacaste, Puntarenas, Limón).
- **84 cantones:** «Puerto Jiménez es oficialmente el cantón número 84 del país» (Observador, 8-abr-2022) —
  https://observador.cr/puerto-jimenez-es-oficialmente-el-canton-84-de-costa-rica/
- **Distritos: cifra sin confirmar en fuente oficial.** Wikipedia en español dice «7 provincias, 84 cantones y 488
  distritos» — https://es.wikipedia.org/wiki/Organizaci%C3%B3n_territorial_de_Costa_Rica — otras fuentes dicen 489 o 490.
  La declaratoria oficial vigente es el **Decreto 44882-MGP** (Alcance 12, La Gaceta 17, 28-ene-2025), en el SNIT:
  https://www.snitcr.go.cr/fe/http/Home/public/pdfs/leyes/DE%2044882-MGP%20Declaratoria%20Oficial%20DTA%20(Alcance%2012%20Gaceta%2017%20del%2028%2001%202025).pdf
  — **no abrió** (ver abajo). En el sitio, mientras tanto, no publicar número de distritos.
- Cobertura sugerida en el sitio (`localArea`): provincia y cantón (como ya está en la ficha).

---

## 6. Lugares para la portada (Anexo B: ícono visible · asfalto despejado · calle en diagonal de abajo-izquierda a arriba-derecha con el ícono a un lado)

Licencias comprobadas hoy en la página de cada foto en Wikimedia Commons (bloque «Licensing»). Las miniaturas se
revisaron a ojo. **Ninguna foto real encontrada cumple los tres criterios al 100 %.** Las mejores:

| # | Lugar | Foto (página con licencia) | Licencia y autor | Ícono | Asfalto despejado | Diagonal ↗ con ícono a un lado | Veredicto |
|---|---|---|---|---|---|---|---|
| A | Carretera hacia La Fortuna con el **Volcán Arenal** | https://commons.wikimedia.org/wiki/File:Volcan_Arenal_-_panoramio.jpg (2048×1536) | CC BY-SA 3.0 · Hiram Montiel Calderón | ✓ cono del Arenal a la derecha | Parcial: poste de luz, rótulo de velocidad, «KPH 40» pintado y un carro lejano | ✗ la calle se aleja hacia arriba-izquierda | **Mejor referencia del lugar**; falla 3 y parte de 2 |
| B | **Volcán Arenal** visto desde la carretera (2024) | https://commons.wikimedia.org/wiki/File:Volc%C3%A1n_Arenal_en_Costa_Rica.jpg y https://commons.wikimedia.org/wiki/File:Volc%C3%A1n_Arenal_en_Costa_Rica_01.jpg (2608×4624) | CC BY-SA 4.0 · Pequeño mar | ✓ cono limpio | ✓ franja de asfalto sin tráfico ni rótulos | Parcial: el borde sube de izquierda a derecha, pero el volcán queda al centro | Cumple 1 y 2; **foto vertical**, no sirve tal cual para 16:10 |
| C | **Puente de la Amistad** sobre el río Tempisque (Guanacaste) | https://commons.wikimedia.org/wiki/File:Puente_de_la_Amistad,_R%C3%ADo_Tempisque,_Guanacaste,_Costa_Rica._-_panoramio.jpg (3264×2448); vista aérea: https://commons.wikimedia.org/wiki/File:Puente_Tempisque_07_2015_CRI_3848.jpg | CC BY-SA 3.0 · Peloy (Allan H.M.); aérea CC BY-SA 4.0 · Mariordo | ✓ pilones y cables rojos | ✓ | ✗ a nivel de calle el puente va casi horizontal y el pilón queda al centro; en la aérea sí va en diagonal ↗, pero es cenital | Ícono fuerte de Guanacaste; falla 3 |
| D | **Volcán Arenal desde el lago** (fondo de referencia) | https://commons.wikimedia.org/wiki/File:Volc%C3%A1n_Arenal_desde_el_lago_Arenal.jpeg (4678×3099) | CC BY-SA 4.0 · Andresqsz | ✓ el mejor cono | ✗ no hay carretera | ✗ | Solo como referencia del fondo para Midjourney |
| E | Ruta 32 en el Parque Nacional Braulio Carrillo | https://commons.wikimedia.org/wiki/File:Carretera_San_Jos%C3%A9_-_Lim%C3%B3n,_Costa_Rica.jpg (640×480) | CC BY 3.0 · MadriCR | ✗ el «ícono» es un rótulo | ✗ rótulo grande y un carro | ✓ la calle va de abajo-izquierda a arriba-derecha | **Falla 1 y 2** |
| F | Ruta 27 (San José-Caldera) | https://commons.wikimedia.org/wiki/File:San_Jose_Caldera_Ruta_27.JPG | CC BY-SA 4.0 · Lex.mercurio | ✗ | ✗ peaje, rótulos verdes, tráfico | ✗ | **Falla los tres** |
| G | Camino al Volcán Irazú | https://commons.wikimedia.org/wiki/File:BMW_i3_Irazu_volcano_CRI_09_2022_8369.jpg y https://commons.wikimedia.org/wiki/File:Volc%C3%A1n_Iraz%C3%BA_-_panoramio_(4).jpg | CC BY-SA 4.0 · Mariordo; CC BY 3.0 · kajikawa | ✗ no se ve el cráter | ✗ carro / camión, cables | ✗ | **Falla** |
| H | Panamericana en Guanacaste / Papagayo (Ocotal-Coco) | https://commons.wikimedia.org/wiki/File:Carretera_Panamericana_en_Gunacaste_Costa_Rica.jpg (CC0 · Ll1324); https://commons.wikimedia.org/wiki/File:Road_from_Ocotal_to_Coco_(25560076957).jpg (CC BY-SA 2.0) | — | ✗ sin ícono | Panamericana ✓ salvo una moto; Ocotal ✗ casas y cables | ✗ calle al centro | **Falla 1 y 3** |

Lo que no encontré para la portada:
- **Costanera Sur (Ruta 34) con el mar**: en Commons la categoría «National Route 34 (Costa Rica)» solo tiene 5 fotos
  (río Tárcoles y un puente en Dominical); ninguna muestra asfalto y mar juntos.
- **Volcán Poás** con carretera: nada útil (la «Poas Volcano 16» es un sendero de tierra).
- **Pexels**: busqué «arenal volcano», «arenal road», «costa rica road volcano», «guanacaste road», «costa rica coastal
  road»: las carreteras que salen son de Brasil, Nicaragua, El Salvador o sin lugar; las del Arenal no tienen carretera
  (p. ej. https://www.pexels.com/photo/forest-and-volcano-mountain-in-costa-rica-19344663/ , «Free to use»).
- **Unsplash**: la búsqueda pide inicio de sesión (respuesta 401); no la pude revisar.

**Recomendación al dueño (3, fotos solas, lado a lado):** A (Arenal desde la carretera), B (Arenal 2024, vertical) y
C (Puente de la Amistad). El lugar recomendado sigue siendo el **Volcán Arenal** (es el `landmark` que ya tiene la
ficha): ninguna foto lo trae con la calle en la diagonal correcta, así que la imagen del carro tendrá que poner el
Arenal a la derecha del fondo y conservar la carretera de la base del carro (Anexo B, método probado). Todas las
licencias son CC BY o CC BY-SA: piden crédito al autor (y, en BY-SA, compartir igual); anotar el crédito en
`creditosFotos`.

---

## 7. Comprobación propia

Abierta por el autor de la receta (no por el agente investigador), 31-oct-2026, leyendo el texto de cada fuente:

| Dato que va al sitio | Fuente abierta | Lo que dice la fuente (textual) | Resultado |
|---|---|---|---|
| 5.814 casos de dengue a la semana 40 de 2026; 3.798 en 2025 | Ministerio de Salud, Boletín Epidemiológico N.º 39 (PDF) | «se notifican 5814 casos acumulados de dengue» · «para la semana epidemiológica 40 del año 2025 se reportaron 3798 casos» | ✓ |
| Grecia 683 casos; Orotina, tasa 2.182,2 por 100.000 | mismo boletín | «Grecia 683 839,2 … Orotina 555 2182,2» | ✓ |
| 923 casos de chikungunya | mismo boletín | «se notifica un total de 923 casos de chikungunya» | ✓ |
| El 90 % de los criaderos está dentro de las viviendas (2025) | Ministerio de Salud, nota del 26-ago-2025 | «el 90% de los criaderos están dentro de las viviendas» | ✓ |
| Roedores en el 52,6 % de los casos de leptospirosis | Acta Médica Costarricense v54n4 (SciELO) | «El 52,6% de los casos reporta presencia de roedores» | ✓ |
| Alacranes: 24 picaduras en 1992 y 405 en 1999; no son letales | CRHoy | «en 1992 se reportaron 24 casos … en 1999 la cifra se duplicó a 405» · «Los alacranes ticos no son letales» | ✓ |
| Ley 9929: enjambres a SENASA, ataques de abejas a Bomberos | Ley 9929 (PDF) | «Servicio Nacional de Salud Animal (SENASA)» · «El Benemérito Cuerpo de Bomberos responderá cuando se presenten ataques de abejas» | ✓ |
| WhatsApp de la oficina wa.me/50663033868 y enlace roto wa.me/5066303868 | trulynolencr.com (inicio, /in2care/, /servicio-especializado-de-sanitizacion/) | enlaces en el HTML de cada página | ✓ |
| 68 % y 61,3 % de alérgicos a cucaracha (estudio de 1992) | Revista Costarricense de Salud Pública (BINASSS) | ya comprobado el 30/31-oct en esta sesión (corrección del dueño) | ✓ |
| Termita de madera seca, «el problema más frecuente»; Teatro Nacional | Kurú (TEC, 2006) | ya comprobado el 30/31-oct en esta sesión | ✓ |
| Zompopa «posiblemente la más común en el país» | Observador.cr (14-jun-2026) | «una plaga de gran relevancia, posiblemente la más común en el país» | ✓ |

Sin comprobar todavía (no van al sitio hasta que se comprueben o se quitan): la nota de El Mundo CR sobre pulgas y garrapatas
(no abrió: 403), el 24 % de Salmonella en moscas (Bolaños, 1959; no se abrió el PDF), el texto completo del Decreto 43432-S
y el número oficial de distritos.

## 8. Lo que no encontré

1. **«Zancudo» en una fuente oficial del país.** El Ministerio de Salud escribe «mosquito Aedes aegypti» (boletín 39,
   nota de Orotina 2026, nota del 26-ago-2025). El nombre «zancudo» es de uso común pero hoy no lo encontré en una
   fuente costarricense abierta. Sugerencia: título «Zancudos (mosquito del dengue)».
2. **El 24 % de Salmonella en moscas (Bolaños, 1959)** que usa la ficha: la página del artículo abre, pero el resumen
   visible no trae la cifra; no abrí el PDF. Comprobar en https://archivo.revistas.ucr.ac.cr/index.php/rbt/article/view/29946/29946 antes de publicarla.
3. **El Mundo CR no abrió** (403 con curl y con WebFetch; archive.org dio 429): ni la nota de la UNA sobre pulgas y
   garrapatas en época seca (https://elmundo.cr/tendencias/pulgas-y-garrapatas-proliferan-en-verano-senala-escuela-veterinaria-de-la-una/),
   que la ficha usa, ni la del decreto de permisos en un día. Las frases de la ficha que dependen de ella («tienden a
   propagarse más en la época seca», «muy común a nivel nacional») quedan **sin comprobar hoy**.
4. **Texto completo del Decreto 43432-S** (reglamento de permisos vigente): no lo encontré abierto en SCIJ ni en
   FAOLEX; solo las citas del propio Ministerio. No sé si menciona plagas ni en qué grupo de riesgo queda una fumigadora.
5. **SCIJ (Sistema Costarricense de Información Jurídica)**: no pude confirmar ahí el texto vigente de la Ley 9929 ni
   reformas posteriores al Decreto 38335-S-MTSS (la página respondió, pero sin el texto). La Ley 9929 se leyó en la
   copia de Bufete de Costa Rica; el reglamento de esa ley en el MAG da 404
   (https://www.mag.go.cr/acerca_del_mag/estructura/oficinas/Legal/REGLAMENTO_LEY_9929.pdf).
6. **Número oficial de distritos**: el Decreto 44882-MGP en el SNIT no abrió (curl sin respuesta; WebFetch «socket hang
   up»). El PDF del TSE (https://tse.go.cr/2024/docus/DTE-Digital2024.pdf) da 404.
7. **Buenas prácticas de manufactura (RTCA) y reglamento de servicios de alimentación** con su artículo de control de
   plagas: no los busqué a fondo; no hay artículo exacto.
8. **Cifras de sodas y pulperías recientes y oficiales** (INEC, MEIC): no encontré; las de pulperías son de 2013 y 2020,
   de medios en inglés.
9. **Dirección, horario, términos y accesibilidad de la oficina**: no están publicados; pedirlos a la oficina.
10. **`franquicias.ts`**: sin acceso al repo.
11. **Fotos de portada** que cumplan los tres criterios: no hay (sección 6).

---
## Decisiones del dueño (paso 2 y 3, 31-oct-2026)
- Trato: **usted**.
- Plagas (6): zancudos, ratas y ratones, cucarachas, comején, hormigas y zompopas, chinches de cama. Salen alacranes, moscas y pulgas y garrapatas.
- Lugar de la portada: **B · Volcán Arenal (2024)**, https://commons.wikimedia.org/wiki/File:Volc%C3%A1n_Arenal_en_Costa_Rica.jpg (CC BY-SA 4.0, Pequeño mar). Anotado en la ficha: `landmark` y `ruta.aprobado.portada = 2026-10-31`.
