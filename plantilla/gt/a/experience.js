(() => {
  if (document.documentElement.dataset.aExperience) return;
  document.documentElement.dataset.aExperience = 'ready';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const running = new Set();
  const header = document.querySelector('.site-header');
  let headerFrame=0;
  const reflectScroll=()=>{headerFrame=0;header?.classList.toggle('is-scrolled',scrollY>18)};
  addEventListener('scroll',()=>{if(!headerFrame)headerFrame=requestAnimationFrame(reflectScroll)},{passive:true});
  reflectScroll();

  function respond(element, distance = 6) {
    if (reduced.matches || !element.animate) return;
    const animation = element.animate([
      { opacity: .78, transform: `translateY(-${distance}px)` },
      { opacity: 1, transform: 'translateY(0)' }
    ], { duration: 180, easing: 'cubic-bezier(.2,.65,.3,1)' });
    running.add(animation);
    animation.finished.catch(() => {}).finally(() => running.delete(animation));
  }
  // main.js alone changes hidden/open/aria-expanded; this layer only observes it.
  const observer = new MutationObserver(records => {
    for (const { target, attributeName } of records) {
      if (attributeName === 'hidden' && !target.hidden) respond(target);
      if (attributeName === 'open' && target.open) respond(target, 8);
      if (attributeName === 'class' && target.classList.contains('is-open')) respond(target);
    }
  });
  document.querySelectorAll('.mega').forEach(panel => observer.observe(panel, { attributes: true, attributeFilter: ['hidden'] }));
  const navigation = document.querySelector('#navigation');
  if (navigation) observer.observe(navigation, { attributes: true, attributeFilter: ['class'] });
  const search = document.querySelector('.search-dialog');
  if (search) observer.observe(search, { attributes: true, attributeFilter: ['open'] });

  // One quiet photographic settle; no border sweep or loading metaphor.
  const photo = document.querySelector('.photographic-hero .hero-photo');
  function settlePhoto() {
    if (reduced.matches || !photo?.animate || !photo.naturalWidth) return;
    const rect = photo.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > innerHeight) return;
    const animation = photo.animate([{ transform: 'scale(1.012)' }, { transform: 'scale(1)' }],
      { duration: 900, easing: 'cubic-bezier(.2,.65,.3,1)' });
    running.add(animation);
    animation.finished.catch(() => {}).finally(() => running.delete(animation));
  }
  if (photo?.complete) requestAnimationFrame(settlePhoto);
  else photo?.addEventListener('load', settlePhoto, { once: true });
  reduced.addEventListener('change', () => { if (reduced.matches) for (const animation of running) animation.cancel(); });

  // Tonal correction of the faint official scan: white stays white, ink gains contrast.
  if (document.querySelector('.flea-specimen')) {
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
    svg.setAttribute('aria-hidden', 'true'); svg.style.position = 'absolute';
    const filter = document.createElementNS(ns, 'filter'); filter.id = 'a-specimen-ink';
    filter.setAttribute('color-interpolation-filters', 'sRGB');
    const transfer = document.createElementNS(ns, 'feComponentTransfer');
    ['R','G','B'].forEach(channel => { const curve = document.createElementNS(ns, `feFunc${channel}`);
      curve.setAttribute('type', 'gamma'); curve.setAttribute('amplitude', '1'); curve.setAttribute('exponent', '2.6'); curve.setAttribute('offset', '0'); transfer.append(curve); });
    filter.append(transfer); svg.append(filter); document.body.append(svg);
  }

  // Preserve native details and original prose; move only the open reading panel.
  const compactTeam = matchMedia('(max-width:760px)');
  document.querySelectorAll('.c-team-grid').forEach(grid => {
    const people = [...grid.querySelectorAll(':scope > .c-person')];
    const records = people.map((person, index) => {
      const details = person.querySelector('details'), prose = details?.querySelector('.c-prose');
      if (!details || !prose) return null;
      const marker = document.createComment('Biography original position');
      prose.before(marker);
      const summary = details.querySelector('summary'), heading = person.querySelector('h3');
      const row = document.createElement('section'); row.className = 'c-biography-row';
      row.id = `${person.id}-biography`;
      heading.id ||= `${person.id}-name`;
      row.setAttribute('aria-labelledby', heading.id);
      const place = () => {
        const end = compactTeam.matches ? index : Math.min(people.length-1, Math.floor(index/2)*2+1);
        people[end].after(row);
      };
      const close = () => { marker.after(prose); row.remove(); summary.removeAttribute('aria-controls'); details.open = false; };
      details.addEventListener('toggle', () => {
        if (!details.open) { marker.after(prose); row.remove(); summary.removeAttribute('aria-controls'); return; }
        records.forEach(record => { if (record && record.details !== details && record.details.open) record.close(); });
        row.append(prose); place(); summary.setAttribute('aria-controls', row.id);
      });
      prose.querySelectorAll(`a[href="#${person.id}"]`).forEach(link => link.addEventListener('click', event => {
        event.preventDefault(); close(); person.scrollIntoView({ block:'start', behavior:'instant' }); summary.focus({ preventScroll:true });
      }));
      return { details, close, place };
    });
    compactTeam.addEventListener('change', () => records.forEach(record => { if (record?.details.open) record.place(); }));
  });

  // Video collection in-page modal player + clickable thumbnail & title
  const videos = [...document.querySelectorAll('.s-video:not([data-video-bound])')];
  if (videos.length) {
    let modal = null;
    const closeLabel = { es: 'Cerrar video', pt: 'Fechar vídeo', ar: 'إغلاق الفيديو', en: 'Close video' }[document.documentElement.lang] || 'Close video';
    function openVideo(ytId, titleText) {
      if (!modal) {
        modal = document.createElement('dialog');
        modal.className = 'tn-video-modal';
        modal.innerHTML = `<div class="tn-video-modal-bar"><p class="tn-video-modal-title"></p><div class="tn-video-modal-actions"><a class="tn-video-modal-ext" target="_blank" rel="noopener">YouTube ↗</a><button type="button" class="tn-video-modal-close" aria-label="${closeLabel}">×</button></div></div><div class="tn-video-modal-frame"></div>`;
        document.body.append(modal);
        modal.querySelector('.tn-video-modal-close').addEventListener('click', () => modal.close());
        modal.addEventListener('click', e => { if (e.target === modal) modal.close(); });
        modal.addEventListener('close', () => { modal.querySelector('.tn-video-modal-frame').replaceChildren(); });
      }
      modal.querySelector('.tn-video-modal-title').textContent = titleText || 'Truly Nolen International';
      modal.querySelector('.tn-video-modal-ext').href = `https://www.youtube.com/watch?v=${ytId}`;
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube.com/embed/${ytId}?autoplay=1&rel=0&origin=${encodeURIComponent(location.origin)}`;
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      iframe.title = titleText || 'Truly Nolen International video';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      iframe.allowFullscreen = true;
      modal.querySelector('.tn-video-modal-frame').replaceChildren(iframe);
      modal.showModal();
    }
    videos.forEach(card => {
      card.dataset.videoBound = 'true';
      const link = card.querySelector('a[href*="youtube.com"], a[href*="youtu.be"]');
      if (!link) return;
      link.target = '_blank';
      link.rel = 'noopener';
      const m = link.href.match(/(?:v=|youtu\.be\/)([A-Za-z0-9_-]{11})/);
      if (!m) return;
      const ytId = m[1];
      const title = card.querySelector('h3')?.textContent?.trim() || '';
      const fig = card.querySelector('.s-figure');
      const h3 = card.querySelector('h3');
      [fig, h3].forEach(el => {
        if (!el) return;
        el.tabIndex = 0;
        el.setAttribute('role', 'button');
        el.setAttribute('aria-label', title);
        el.addEventListener('click', () => openVideo(ytId, title));
        el.addEventListener('keydown', e => {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openVideo(ytId, title); }
        });
      });
      link.addEventListener('click', e => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        openVideo(ytId, title);
      });
    });
  }
})();
