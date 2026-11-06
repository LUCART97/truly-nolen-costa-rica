(() => {
  const locale = document.documentElement.lang;
  const english = locale !== 'es';
  const t = value => window.TNI_I18N?.[value] || value;
  // Keep the translated counterpart reachable before opening the mobile menu.
  const setLangCookie = targetLang => {
    if (['es', 'en', 'pt', 'ar'].includes(targetLang)) {
      try { document.cookie = `tni_lang=${targetLang}; path=/; max-age=31536000; SameSite=Lax`; } catch {}
    }
  };
  document.querySelectorAll('a[hreflang], .utility a[lang], .mobile-languages-group a[lang], .languages a[lang]').forEach(link => {
    link.addEventListener('click', () => setLangCookie(link.getAttribute('hreflang') || link.getAttribute('lang')));
  });
  const languageMenuButton = document.querySelector('.menu-toggle');
  const languageSources = [...document.querySelectorAll('.utility a[lang]')];
  if (languageMenuButton && languageSources.length) {
    const shortcut = document.createElement('select');
    shortcut.className = 'mobile-language-shortcut';
    shortcut.setAttribute('aria-label', english ? t('Languages') : 'Idiomas');
    for (const source of languageSources) {
      const option = document.createElement('option');
      option.value = source.getAttribute('href');
      option.dataset.lang = source.lang;
      option.textContent = source.lang === 'ar' ? 'عربي' : source.lang.toUpperCase();
      option.selected = source.lang === locale;
      shortcut.append(option);
    }
    shortcut.addEventListener('change', () => {
      const selected = shortcut.selectedOptions?.[0];
      if (selected?.dataset?.lang) setLangCookie(selected.dataset.lang);
      location.href = shortcut.value;
    });
    languageMenuButton.before(shortcut);
  }

  // BEGIN GENERATED A ROUTE INDEX
  const routeIndex = [
 {
  "url": "/oficinas/costa-rica/",
  "en": "Home",
  "es": "Inicio",
  "category": "Overview",
  "categoryEs": "Inicio",
  "keywords": "inicio costa rica truly nolen"
 },
 {
  "url": "/oficinas/costa-rica/servicios/hogares/",
  "en": "Hogares",
  "es": "Hogares",
  "category": "Services",
  "categoryEs": "Servicios",
  "keywords": "hogares desde la cocina hasta el patio. revisamos su casa o apartamento para encontrar dónde está la actividad de plagas y qué la favorece, cuidando a su familia y a sus mascotas."
 },
 {
  "url": "/oficinas/costa-rica/servicios/comercios/",
  "en": "Comercios",
  "es": "Comercios",
  "category": "Services",
  "categoryEs": "Servicios",
  "keywords": "comercios control de plagas para restaurantes, supermercados, hoteles, hospitales y empresas de logística en costa rica, con el programa teps."
 },
 {
  "url": "/oficinas/costa-rica/servicios/industria/",
  "en": "Industria",
  "es": "Industria",
  "category": "Services",
  "categoryEs": "Servicios",
  "keywords": "industria control de plagas para plantas de alimentos, bodegas, centros de distribución y agroindustria, con la hoja de servicio que pide el decreto 38335-s-mtss."
 },
 {
  "url": "/oficinas/costa-rica/plagas/zancudos/",
  "en": "Zancudos",
  "es": "Zancudos",
  "category": "Pests",
  "categoryEs": "Guía de plagas",
  "keywords": "zancudos el zancudo del dengue, aedes aegypti, se cría en los recipientes donde se guarda agua. en costa rica, los casos de dengue aumentaron en 2026, según el ministerio de salud."
 },
 {
  "url": "/oficinas/costa-rica/plagas/ratas-y-ratones/",
  "en": "Ratas y ratones",
  "es": "Ratas y ratones",
  "category": "Pests",
  "categoryEs": "Guía de plagas",
  "keywords": "ratas y ratones las ratas y los ratones buscan comida, agua y refugio en la casa o el negocio. en costa rica, las ratas están entre los reservorios más frecuentes de la leptospirosis."
 },
 {
  "url": "/oficinas/costa-rica/plagas/cucarachas/",
  "en": "Cucarachas",
  "es": "Cucarachas",
  "category": "Pests",
  "categoryEs": "Guía de plagas",
  "keywords": "cucarachas varios autores señalan que las cucarachas más frecuentes en las casas del país son la americana, la australiana, la alemana y la de madeira."
 },
 {
  "url": "/oficinas/costa-rica/plagas/hormigas-y-zompopas/",
  "en": "Hormigas y zompopas",
  "es": "Hormigas y zompopas",
  "category": "Pests",
  "categoryEs": "Guía de plagas",
  "keywords": "hormigas y zompopas además de las hormigas que entran a la cocina, aquí hay zompopas, las hormigas cortadoras de hojas que pueden dejar pelado un jardín."
 },
 {
  "url": "/oficinas/costa-rica/plagas/comejen/",
  "en": "Comején",
  "es": "Comején",
  "category": "Pests",
  "categoryEs": "Guía de plagas",
  "keywords": "comején en costa rica se les dice comején a las termitas. trabajan en silencio dentro de la madera de la casa, los muebles y los objetos decorativos."
 },
 {
  "url": "/oficinas/costa-rica/plagas/chinches-de-cama/",
  "en": "Chinches de cama",
  "es": "Chinches de cama",
  "category": "Pests",
  "categoryEs": "Guía de plagas",
  "keywords": "chinches de cama en 2017 se encontraron chinches de cama en un apartamento de heredia, y la universidad de costa rica identificó el hallazgo como el primer caso confirmado con métodos moleculares en centroamérica."
 },
 {
  "url": "/oficinas/costa-rica/blog/alacranes-en-costa-rica/",
  "en": "Alacranes en Costa Rica: qué tan peligrosos son y qué hacer",
  "es": "Alacranes en Costa Rica: qué tan peligrosos son y qué hacer",
  "category": "Journal",
  "categoryEs": "Blog",
  "keywords": "alacranes en costa rica"
 },
 {
  "url": "/oficinas/costa-rica/blog/chinches-de-cama/",
  "en": "Chinches de cama: cómo saber si las tiene y qué hacer",
  "es": "Chinches de cama: cómo saber si las tiene y qué hacer",
  "category": "Journal",
  "categoryEs": "Blog",
  "keywords": "chinches de cama"
 },
 {
  "url": "/oficinas/costa-rica/blog/ratas-y-leptospirosis/",
  "en": "Ratas y leptospirosis: cómo proteger su casa en Costa Rica",
  "es": "Ratas y leptospirosis: cómo proteger su casa en Costa Rica",
  "category": "Journal",
  "categoryEs": "Blog",
  "keywords": "ratas y leptospirosis"
 },
 {
  "url": "/oficinas/costa-rica/blog/zompopas-en-el-jardin/",
  "en": "Zompopas en el jardín: por qué hay más y cómo controlarlas",
  "es": "Zompopas en el jardín: por qué hay más y cómo controlarlas",
  "category": "Journal",
  "categoryEs": "Blog",
  "keywords": "zompopas en el jardin"
 },
 {
  "url": "/oficinas/costa-rica/blog/",
  "en": "Blog",
  "es": "Blog",
  "category": "Journal",
  "categoryEs": "Blog",
  "keywords": "blog consejos prevención"
 }
];
  // END GENERATED A ROUTE INDEX
  const menuLabel = english ? t('Menu') : 'Menú';
  const closeLabel = english ? t('Close') : 'Cerrar';
  const menuButton = document.querySelector('.menu-toggle');
  const menuIconPath = menuButton?.querySelector('svg path');
  const closedIconD = 'M 3 7h 18M 3 17h 18';
  const openIconD = 'M 6 6L 18 18M 18 6L 6 18';
  const navigation = document.querySelector('#navigation');
  const triggers = [...document.querySelectorAll('.nav-trigger')];
  const closePanels = (except = null) => triggers.forEach(trigger => {
    if (trigger === except) return;
    trigger.setAttribute('aria-expanded', 'false');
    document.getElementById(trigger.getAttribute('aria-controls')).hidden = true;
  });
  const closeMenu = () => {
    navigation.classList.remove('is-open');
    document.documentElement.classList.remove('a-menu-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.querySelector('span').textContent = menuLabel;
    if (menuIconPath) menuIconPath.setAttribute('d', closedIconD);
    closePanels();
  };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('is-open', open);
    document.documentElement.classList.toggle('a-menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.querySelector('span').textContent = open ? closeLabel : menuLabel;
    if (menuIconPath) menuIconPath.setAttribute('d', open ? openIconD : closedIconD);
    if (!open) closePanels();
  });
  triggers.forEach(trigger => trigger.addEventListener('click', () => {
    const open = trigger.getAttribute('aria-expanded') !== 'true';
    closePanels(trigger);
    trigger.setAttribute('aria-expanded', String(open));
    document.getElementById(trigger.getAttribute('aria-controls')).hidden = !open;
  }));
  navigation.querySelectorAll('a, [data-franchise-chat-open]').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) {
      if (navigation.classList.contains('is-open') && !event.target.closest('.search-dialog')) closeMenu();
      else closePanels();
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Tab' && navigation.classList.contains('is-open') && !document.querySelector('.search-dialog').open) {
      const controls = [...document.querySelector('.site-header').querySelectorAll('a[href],button,select')].filter(el => el.getClientRects().length);
      const first = controls[0], last = controls.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault();last.focus({preventScroll:true}); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault();first.focus({preventScroll:true}); }
    }
    if (event.key !== 'Escape') return;
    if (document.querySelector('.search-dialog').open) {
      event.preventDefault();
      document.querySelector('.search-dialog').close();
      return;
    }
    if (navigation.classList.contains('is-open')) { closeMenu();menuButton.focus({preventScroll:true});return; }
    const openTrigger = triggers.find(trigger => trigger.getAttribute('aria-expanded') === 'true');
    if (openTrigger) { closePanels(); openTrigger.focus(); }
  });
  matchMedia('(min-width: 960px)').addEventListener('change', closeMenu);

  // Complete local navigation; generated by scripts/wire-a-routes.py.
  const prefix = location.pathname.startsWith('/a/') ? '/a' : '';
  const localizeRoute = url => {
    if (!prefix) return url.replace(/^\/a\/en\//, `/${locale}/`);
    return english ? url.replace('/a/en/', `/a/${locale}/`) : url === '/a/en/' ? '/a/' : url.replace('/a/en/', '/a/es/');
  };
  const searchIndex = routeIndex.map(page => [
    english ? t(page.en) : page.es,
    page.keywords + ' ' + page.en + ' ' + page.es,
    localizeRoute(page.url),
    english ? t(page.category) : page.categoryEs
  ]);
  searchIndex.push(['Escribir a Truly AI', 'contacto chat whatsapp consulta cobertura', '/oficinas/costa-rica/#contacto', 'Contacto']);
  document.querySelectorAll('.mobile-portals a').forEach(link => {
    if (!/^https?:/.test(link.href) || link.getAttribute('lang')) return;
    if (!/vip\.trulynoleninternational|TrulyInside|www\.trulynoleninternational\.com\/franchise/.test(link.href)) return;
    if (searchIndex.some(item => item[2] === link.href)) return;
    searchIndex.push([link.textContent.trim(), 'login account portal acceso cuenta', link.href,
      english ? t('Account portals') : 'Portales de acceso']);
  });
  const dialog = document.querySelector('.search-dialog');
  const searchInput = document.querySelector('#site-search');
  const results = document.querySelector('.search-results');
  const count = document.querySelector('.search-count');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f\u064b-\u065f\u0670]/g, '').replace(/[أإآ]/g,'ا').toLowerCase();
  const renderResults = () => {
    const query = normalize(searchInput.value.trim());
    const terms = query.split(/\s+/).filter(Boolean);
    const score = item => {
      const title = normalize(item[0]), category = normalize(item[3]);
      const haystack = normalize(item[0]+' '+item[1]+' '+item[3]);
      if (!terms.every(term => haystack.includes(term))) return -1;
      if (!query) return item[3] === (english ? t('Office directory') : 'Directorio de oficinas') ? -1 : 0;
      return title === query ? 100 : title.startsWith(query) ? 80 : title.includes(query) ? 60 : category.includes(query) ? 40 : 10;
    };
    const matched = searchIndex.map((item,index) => ({item,index,rank:score(item)}))
      .filter(row => row.rank >= 0).sort((a,b) => b.rank-a.rank || a.index-b.index).map(row=>row.item);
    results.replaceChildren();
    matched.forEach(([title,,url,category]) => {
      const li = document.createElement('li');
      const anchor = document.createElement('a');
      const label = document.createElement('span');
      const type = document.createElement('small');
      label.textContent = title;
      type.textContent = category + (/^https?:/.test(url) ? ' ↗' : locale === 'ar' ? ' ←' : ' →');
      anchor.href = url;
      anchor.append(label, type);
      li.append(anchor);
      results.append(li);
    });
    count.textContent = matched.length ? (english ? t('{count} matching pages and portals').replace('{count}', matched.length) : `${matched.length} páginas y accesos encontrados`) : (english ? t('No matches. Try a service, pest or office.') : 'No encontramos coincidencias. Pruebe con un servicio, una plaga u «oficina».');
  };
  let locationsReady;
  function loadLocations() {
    if (!locationsReady) locationsReady = Promise.reject()
      .then(response => { if (!response.ok) throw Error('Directory unavailable'); return response.json(); })
      .then(markets => { for (const market of markets) searchIndex.push([
        english ? t(market.en) : market.es, market.en+' '+market.es+' '+market.keywords,
        `${prefix}/${locale}/offices/#${market.esId || market.id}`,
        english ? t('Office directory') : 'Directorio de oficinas'
      ]); renderResults(); })
      .catch(() => { locationsReady=null; });
  }
  document.querySelector('.gt-buscar').addEventListener('click', () => {
    closePanels();
    renderResults();
    loadLocations();
    dialog.showModal();
    searchInput.focus();
  });
  document.querySelector('.search-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  searchInput.addEventListener('input', renderResults);
  searchInput.addEventListener('keydown', event => {
    const links = [...results.querySelectorAll('a')];
    if (!links.length) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      (event.key === 'ArrowDown' ? links[0] : links.at(-1)).focus();
    } else if (event.key === 'Enter') {
      event.preventDefault();
      links[0].click();
    }
  });
  results.addEventListener('keydown', event => {
    if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
    const links = [...results.querySelectorAll('a')];
    const index = links.indexOf(document.activeElement);
    if (index < 0) return;
    event.preventDefault();
    const next = index + (event.key === 'ArrowDown' ? 1 : -1);
    if (next < 0 || next >= links.length) searchInput.focus();
    else links[next].focus();
  });
  dialog.addEventListener('close', () => document.querySelector('.gt-buscar').focus());
})();

// Native mobile footer accordions; complete visible sitemap on larger screens.
(() => {
  const compact = matchMedia('(max-width: 959px)');
  const groups = [...document.querySelectorAll('.footer-grid > details')];
  const sync = () => groups.forEach(group => {
    group.open = !compact.matches;
    group.querySelector('summary').tabIndex = compact.matches ? 0 : -1;
  });
  groups.forEach(group => group.querySelector('summary').addEventListener('click', event => {
    if (!compact.matches) event.preventDefault();
  }));
  compact.addEventListener('change', sync);
  sync();
})();

// Phone steps use native disclosure; all four remain visible on wider layouts.
(() => {
  const compact = matchMedia('(max-width:620px)');
  const steps = [...document.querySelectorAll('.teps-step')];
  const sync = () => steps.forEach((step,index) => {
    step.open = !compact.matches || index === 0;
    step.querySelector('summary').tabIndex = compact.matches ? 0 : -1;
  });
  steps.forEach(step => step.querySelector('summary').addEventListener('click',event => {
    if (!compact.matches) event.preventDefault();
  }));
  compact.addEventListener('change',sync);sync();
})();
