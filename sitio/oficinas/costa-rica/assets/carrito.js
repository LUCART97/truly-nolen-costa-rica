// Centra el carrito de Truly en el espacio libre de la esquina superior izquierda de la portada
// (entre el menú, el texto de la portada y el borde del panel oscuro de la foto) y lo hace
// tan grande como quepa. Solo en pantallas de más de 760 px; en celular manda el CSS.
(function () {
  var carro = document.querySelector('.hero-carrito');
  if (!carro) return;
  var foto = document.querySelector('#inicio .film img');
  var menu = document.querySelector('.site-nav');
  var texto = document.querySelector('#inicio .eyebrow');
  var pared = parseFloat(carro.dataset.pared || '0.3');   // borde del panel oscuro, en fracción del ancho de la foto
  var maximo = parseFloat(carro.dataset.maximo || '300');
  var minimo = parseFloat(carro.dataset.minimo || '120');
  var margen = parseFloat(carro.dataset.margen || '10');
  var proporcion = 656 / 469;

  function ubicar() {
    if (window.innerWidth <= 760 || !foto || !foto.naturalWidth) {
      carro.style.left = carro.style.top = carro.style.width = '';
      return;
    }
    var film = carro.parentElement.getBoundingClientRect();
    var r = foto.getBoundingClientRect();
    var escala = Math.max(r.width / foto.naturalWidth, r.height / foto.naturalHeight);
    var bordePared = r.left - film.left + (r.width - foto.naturalWidth * escala) / 2 + pared * foto.naturalWidth * escala;
    var arriba = menu.getBoundingClientRect().bottom - film.top + margen;
    var abajo = texto.getBoundingClientRect().top - film.top - margen;
    var ancho = Math.min(maximo, bordePared - 2 * margen * 2, (abajo - arriba) * proporcion);
    // Si ni el tamaño mínimo cabe (pantallas muy bajas), el carrito no se muestra para no tapar el texto
    carro.style.display = ancho < minimo ? 'none' : '';
    if (ancho < minimo) return;
    var alto = ancho / proporcion;
    carro.style.width = ancho + 'px';
    carro.style.left = Math.max(margen, (bordePared - ancho) / 2) + 'px';
    carro.style.top = (arriba + Math.max(0, (abajo - arriba - alto) / 2)) + 'px';
  }

  if (foto && !foto.complete) foto.addEventListener('load', ubicar);
  window.addEventListener('resize', ubicar);
  ubicar();
  setTimeout(ubicar, 1200); // el texto de la portada tiene su propia animación de entrada: se vuelve a medir al terminar
})();
