// Progressive enhancement: every sector and anchor is available without JS.
(() => {
  const root = document.querySelector('.ct-commercial');
  if (!root) return;
  const links = [...root.querySelectorAll('.ct-sector-nav a')];
  const sectors = [...root.querySelectorAll('.ct-sector')];
  let scheduled = false;
  function update() {
    scheduled = false;
    const readingLine = Math.max(innerHeight * .3, (document.querySelector('.site-header')?.getBoundingClientRect().bottom || 0) + 32);
    const active = sectors.find(section => {
      const box = section.getBoundingClientRect();
      return box.top <= readingLine && box.bottom > readingLine;
    });
    for (const link of links) {
      if (active && link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }
  function schedule() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  update();
  // On small screens the franchise car lives with the franchise links, outside
  // the long service text. Header/menu/footer entry buttons still open the chat.
  const launcher = document.querySelector('.tn-chat-launcher');
  const franchiseLinks = document.querySelector('[data-footer-group="franchisees"] .footer-links');
  if (launcher && franchiseLinks) {
    document.body.classList.add('ct-commercial-page');
    franchiseLinks.append(launcher);
  }
})();
