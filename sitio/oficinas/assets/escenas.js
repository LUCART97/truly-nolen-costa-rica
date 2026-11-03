// Película de la portada en dos escenas, como globaltni.com/es: el carro corre ~10 s (dos vueltas si su video es corto,
// como el de 5 s de globaltni; una si dura 8 s o más), el mundo entra encima con un fundido de 0,8 s, corre 10 s y se
// desvanece dejando el carro desde el inicio. Nunca se ve el salto del bucle.
// En celular (≤760 px) el mundo es el vertical (2160×3840).
// El video del mundo se crea aquí (después de preview.js) para que preview.js no lo arranque ni lo ponga en bucle.
(function () {
  var film = document.querySelector('#inicio .film');
  var carro = film && film.querySelector('video');
  if (!carro || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var FUNDIDO = 0.8, MUNDO = 10, vueltas = 0;
  var movil = matchMedia('(max-width:760px)').matches;
  var mundo = document.createElement('video');
  mundo.muted = true; mundo.playsInline = true; mundo.preload = 'none';
  mundo.setAttribute('aria-hidden', 'true'); mundo.dataset.escena = 'mundo';
  mundo.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity ' + FUNDIDO + 's linear;z-index:1';
  film.appendChild(mundo);
  var enMundo = false, cambiando = false;
  // El generador pone en el <script> las direcciones del mundo con su huella (?v=), para que nadie vea el viejo en caché.
  var yo = document.querySelector('script[src*="/oficinas/assets/escenas.js"]'), d = (yo && yo.dataset) || {};
  function cargar() { if (!mundo.getAttribute('src')) { mundo.src = movil ? (d.mundoMovil || '/oficinas/assets/mundo-movil.mp4') : (d.mundo || '/oficinas/assets/mundo-desktop.mp4'); mundo.load(); } }
  function aMundo() {
    if (enMundo || cambiando) return; cambiando = true; cargar();
    mundo.currentTime = 0; var p = mundo.play(); if (p && p.catch) p.catch(function () {});
    mundo.style.opacity = '1';
    setTimeout(function () { carro.pause(); enMundo = true; cambiando = false; }, FUNDIDO * 1000);
  }
  function aCarro() {
    if (!enMundo || cambiando) return; cambiando = true;
    vueltas = 0; antes = 0; carro.currentTime = 0; var p = carro.play(); if (p && p.catch) p.catch(function () {});
    mundo.style.opacity = '0';
    setTimeout(function () { mundo.pause(); enMundo = false; cambiando = false; }, FUNDIDO * 1000);
  }
  function total() { return d.vueltas ? +d.vueltas : (carro.duration < 8 ? 2 : 1); }  // vueltas del carro antes del mundo (la ficha puede fijarlas: pelicula.vueltas)
  var antes = 0;
  carro.addEventListener('playing', function () { carro.loop = true; });
  carro.addEventListener('timeupdate', function () {
    if (enMundo || !carro.duration) { antes = carro.currentTime; return; }
    if (carro.currentTime + 0.3 < antes) vueltas++;  // el bucle volvió al inicio
    antes = carro.currentTime;
    if (vueltas >= total() - 1 && carro.currentTime >= carro.duration - FUNDIDO) aMundo();
  });
  mundo.addEventListener('timeupdate', function () {
    var fin = Math.min(MUNDO, mundo.duration || MUNDO);
    if (enMundo && mundo.currentTime >= fin - FUNDIDO) aCarro();
  });
  setTimeout(cargar, 4000);
})();
