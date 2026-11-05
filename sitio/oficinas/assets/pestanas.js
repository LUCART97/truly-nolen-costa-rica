// Pestañas de plagas en celular: la pestaña de la página actual se centra al cargar (4-nov-2026).
addEventListener("load", function () {
  var a = document.querySelector(".pest-families [aria-current]"); if (!a) return;
  var c = a.parentElement; if (c.scrollWidth <= c.clientWidth) return;
  var x = a.getBoundingClientRect().left - c.getBoundingClientRect().left + c.scrollLeft;
  c.scrollLeft = x - (c.clientWidth - a.offsetWidth) / 2;
});
