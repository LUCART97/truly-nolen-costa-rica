// Filtro de cobertura de una oficina: con la región elegida arma el primer mensaje y abre Truly AI con él escrito
// (chat.js lo pone en la caja; la persona lo envía). No manda nada solo ni guarda datos. Las etiquetas del mensaje
// vienen en data-t-* del formulario (oficinas de otro idioma); sin ellas, en español.
(function () {
  document.querySelectorAll('[data-zona]').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var v = function (n) { var x = f.elements[n]; return x ? String(x.value || '').trim() : ''; };
      var sep = f.dataset.tSep || ': ';  // en francés va un espacio fino antes de los dos puntos
      var partes = [f.dataset.n1 + sep + v('n1')];
      if (v('n2')) partes.push(f.dataset.n2 + sep + v('n2'));
      if (v('cp')) partes.push((f.dataset.tCp || 'Código postal') + sep + v('cp'));
      var esp = f.querySelector('input[name="espacio"]:checked');
      if (esp) partes.push((f.dataset.tEspacio || 'Espacio') + sep + esp.value);
      var b = f.querySelector('[data-zona-enviar]');
      b.dataset.chatPrompt = (f.dataset.tConsulta || 'Quiero consultar la cobertura.') + ' ' + partes.join(' · ');
      b.click();
    });
  });
})();

// Mensajes de validación en «usted» (el navegador los pondría en tú según su idioma).
(function () {
  document.querySelectorAll('[data-zona] select[required], [data-zona] input[required]').forEach(function (c) {
    c.addEventListener('invalid', function () { c.setCustomValidity(c.tagName === 'SELECT' ? 'Elija una provincia de la lista.' : 'Complete este campo.'); });
    c.addEventListener('input', function () { c.setCustomValidity(''); });
    c.addEventListener('change', function () { c.setCustomValidity(''); });
  });
})();
