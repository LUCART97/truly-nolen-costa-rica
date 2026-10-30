# Investigación del país · Costa Rica (F0, paso 3)

Fecha: 30-oct-2026 · Estado: **borrador, falta el ok del dueño**

## 1. ¿Tiene oficina?
- Hay un sitio público de Truly Nolen en el país: **trulynolencr.com** («Fumigadora Truly Nolen Costa Rica»), con teléfono **2258-0608**, Facebook, Instagram (@trulynolen.cr), X y YouTube. Anuncia certificaciones HACCP, ISO 22000 y BPM.
- No publica dirección, horario, correo ni WhatsApp.
- **Decisión del borrador:** `contacto: "truly-ai"` hasta que la oficina confirme sus canales. Ningún dato de esa página se puso en el sitio (regla 2 de la skill).
- Pendiente: revisar `franquicias.ts` del repo (nivel y «dudosa») y confirmar con la oficina.

## 2. Idioma y trato
- Español. **Trato: usted** (el machote del catálogo ya está en usted y es el uso habitual en el comercio costarricense).
- Ojo: trulynolencr.com mezcla tú («Solicita tu inspección») y usted («su seguridad»). **El dueño debe confirmar el trato.**
- `tratoVetado`: tú y voseo (tu, tus, tienes, puedes, te, vos, tenés, podés…). El generador los revisa en cada página.

## 3. Plagas (6) y su nombre local
| Plaga | Nombre local | Dato clave | Fuente |
|---|---|---|---|
| Zancudos | zancudo (*Aedes aegypti*) | 5.302 casos de dengue en las primeras 37 semanas de 2026, +38,6 % frente a 2025 (3.256) | Delfino.cr, 2-oct-2026, citando el boletín del Ministerio de Salud · OMS |
| Ratas y ratones | ratas, ratones | Las ratas están entre los reservorios más frecuentes de la leptospirosis; se transmite por la orina | Ministerio de Salud, Protocolo de leptospirosis (2002) |
| Cucarachas | cucaracha | Las más frecuentes: *P. americana*, *P. australasiae*, *B. germanica*, *Leucophaea maderae*; 68 % de 80 pacientes alérgicos severos reaccionó | Calderón, Rev. Costarricense de Salud Pública vol. 2 n.º 2 (año sin confirmar) |
| Hormigas y zompopas | **zompopa** (*Atta cephalotes*) | «posiblemente la más común en el país»; avanza en la ciudad | Observador.cr, 14-jun-2026 · CATIE, Varón Devia 2006 |
| Comején | **comején** = termitas | *Cryptotermes brevis*, el problema más frecuente en las construcciones; daños en el Teatro Nacional | Kurú: Revista Forestal 3(8), 2006 |
| Alacranes | alacrán | Los de Costa Rica no son letales (Instituto Clodomiro Picado, UCR); 405 casos en 1999 frente a 24 en 1992 | CRHoy, 27-ene-2017 |

**Para preguntar al dueño:** ¿falta alguna plaga importante (chinches de cama, murciélagos, palomas)? ¿Sobra alguna?

## 4. Norma
- **Decreto Ejecutivo 38335-S-MTSS** (La Gaceta, 6-may-2014): «Reglamento para regular la actividad de control de plagas mediante la aplicación de plaguicidas de uso doméstico y profesional».
  - Art. 5: permiso sanitario de funcionamiento del Ministerio de Salud.
  - Art. 6: hoja de servicio con fecha, plaguicidas, medidas de seguridad y tiempo de reingreso; el original es para el cliente.
  - Art. 7: el permiso dura un año.
- Fuente: BINASSS, https://www.binasss.sa.cr/opac-ms/media/digitales/Regulaci%c3%b3n%20de%20la%20actividad%20de%20control%20de%20plagas%20mediante%20la%20aplicaci%c3%b3n%20de%20plaguicidas%20de%20uso%20dom%c3%a9stico%20y%20profesional.pdf
- Falta revisar si ha tenido reformas después de 2014.

## 5. Negocios y territorio
- Negocios típicos: sodas, restaurantes, panaderías, pulperías, supermercados, hoteles, oficinas, beneficios de café y agroindustria.
- Cobertura (`localArea`): **provincia y cantón**.
- Palabras locales usadas: canoas, verjas, pilas, cielorraso, refrigeradora, tarimas.

## 6. Imágenes
- Portada y footer: los del **machote oficial de Costa Rica** del catálogo (Volcán Arenal).
- Técnico (Nosotros) y supermercado: catálogo Truly Inbound.
- Cocinas, industria e ilustraciones de plagas: tomadas del borrador de Venezuela (son neutras). **Provisionales.**
