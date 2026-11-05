/** Public TNI franchise & service guidance with pre-chat lead capture and intent filter. */
(() => {
  if (document.querySelector('#tn-franchise-chat')) return;
  const lang = ['es', 'en', 'pt', 'ar'].includes(document.documentElement.lang) ? document.documentElement.lang : 'en';
  const en = lang !== 'es';
  const t = value => window.TNI_I18N?.[value] || value;
  const family = location.pathname.startsWith('/b/') ? 'b' : 'a';
  const basePrefix = location.pathname.startsWith('/b/') ? '/b' : location.pathname.startsWith('/a/') ? '/a' : '';
  const copy = en ? {
    title: 'Let’s talk Truly.', sub: 'Services, offices and franchising', open: 'Open the assistant', close: 'Close chat', intro: 'Welcome to Truly Nolen International. How can we help you?', service: 'I have a pest problem', support: 'I am a franchisee', new: 'I want to open a franchise', serviceMessage: 'I have a pest problem and I would like to know how you can help.', supportMessage: 'I am a Truly Nolen franchisee and need support.', newMessage: 'I would like to learn about opening a Truly Nolen franchise.', serviceTitle: 'Pest control service', supportTitle: 'Support for franchisees', newTitle: 'Explore a new franchise', change: 'Change topic', choose: 'Choose a topic to begin.', placeholder: 'Write your question…', send: 'Send message', thinking: 'Preparing your answer…', failed: 'We couldn’t connect just now. Please try again or use the official links below.', pending: 'The assistant is not available yet. You can use the franchise portal or explore the franchise model.', retry: 'Try again', portal: 'Franchise portal', apply: 'Explore franchising', privacy: 'Privacy', notice: 'AI guidance. Account-specific support continues in the secure franchise portal.', later: n => `Please try again in ${n} ${n === 1 ? 'minute' : 'minutes'}.`
  } : {
    title: 'Hablemos de Truly.', sub: 'Servicios, oficinas y franquicias', open: 'Abrir el asistente', close: 'Cerrar chat', intro: 'Bienvenido a Truly Nolen International. ¿En qué podemos ayudarle?', service: 'Tengo un problema de plagas', support: 'Ya soy franquiciado', new: 'Quiero abrir una franquicia', serviceMessage: 'Tengo un problema de plagas y quiero saber cómo pueden ayudarme.', supportMessage: 'Soy franquiciado de Truly Nolen y necesito soporte.', newMessage: 'Quiero conocer cómo abrir una franquicia de Truly Nolen.', serviceTitle: 'Servicio de control de plagas', supportTitle: 'Soporte para franquiciados', newTitle: 'Conozca una nueva franquicia', change: 'Cambiar tema', choose: 'Elija un tema para comenzar.', placeholder: 'Escriba su consulta…', send: 'Enviar mensaje', thinking: 'Preparando su respuesta…', failed: 'No pudimos conectar en este momento. Inténtelo de nuevo o use los enlaces oficiales de abajo.', pending: 'El asistente todavía no está disponible. Puede entrar al portal o conocer el modelo de franquicia.', retry: 'Reintentar', portal: 'Portal de franquiciados', apply: 'Conocer la franquicia', privacy: 'Privacidad', notice: 'Orientación con IA. El soporte de su cuenta continúa en el portal seguro de franquiciados.', later: n => `Puede intentarlo de nuevo en ${n} ${n === 1 ? 'minuto' : 'minutos'}.`
  };
  if (window.TNI_I18N) {
    for (const key of Object.keys(copy)) if (typeof copy[key] === 'string') copy[key] = t(copy[key]);
    copy.later = n => t('Please try again in {count} minutes.').replace('{count}', n);
  }
  Object.assign(copy, {
    es: {
      chatLabel: 'Chat', open: 'Abrir chat con Truly IA', title: 'Truly IA', sub: 'Chat de Truly Nolen',
      intro: 'Hola, soy Truly IA. Para hablar aquí en la web, compártanos sus datos breves abajo; o si prefiere, puede continuar directo por WhatsApp.',
      change: 'Cambiar filtro / tema', notice: 'Conversación con IA.', waOffer: 'También puede continuar por WhatsApp.',
      lockedPlaceholder: 'Complete los pasos de arriba para escribir…',
      step1Title: 'Paso 1 de 3 · Su WhatsApp o teléfono',
      waLabel: '¿Cuál es su número de WhatsApp?',
      phoneLabel: '¿Cuál es su número de teléfono?',
      phonePlaceholder: '+52 55 0000 0000',
      noWaToggle: 'No tengo WhatsApp, dejar mi número de teléfono',
      phoneError: 'Ingrese un número válido (mínimo 7 dígitos).',
      step2Title: 'Paso 2 de 3 · Sus datos para ayudarle mejor',
      nameLabel: 'Su nombre completo',
      namePlaceholder: 'Nombre y apellido',
      emailLabel: 'Su correo electrónico',
      emailPlaceholder: 'nombre@empresa.com',
      contactError: 'Ingrese su nombre y un correo electrónico válido.',
      step3Title: 'Paso 3 de 3 · ¿En qué podemos ayudarle?',
      filterPrompt: 'Seleccione el tema de su consulta:',
      optFranchise: 'Oportunidad de franquicia',
      optService: 'Servicio de control de plagas o sanitización',
      optSupport: 'Ya soy franquiciado (Soporte)',
      optOther: 'Otra consulta',
      nextBtn: 'Siguiente →',
      backBtn: '← Atrás',
      readyMsg: (name, filter) => `¡Gracias, ${name}! Hemos registrado su consulta bajo «${filter}». Ya puede escribir su mensaje aquí abajo.`
    },
    en: {
      chatLabel: 'Chat', open: 'Open chat with Truly IA', title: 'Truly IA', sub: 'Truly Nolen chat',
      intro: 'Hello, I’m Truly IA. To chat with me here on the website, please share a few quick details below — or continue directly on WhatsApp.',
      change: 'Change filter / topic', notice: 'Conversation with AI.', waOffer: 'You can also continue on WhatsApp.',
      lockedPlaceholder: 'Complete the steps above to start typing…',
      step1Title: 'Step 1 of 3 · Your WhatsApp or phone',
      waLabel: 'What is your WhatsApp number?',
      phoneLabel: 'What is your phone number?',
      phonePlaceholder: '+1 555 000 0000',
      noWaToggle: 'I don’t have WhatsApp — use my phone number',
      phoneError: 'Please enter a valid number (at least 7 digits).',
      step2Title: 'Step 2 of 3 · Your details to help you better',
      nameLabel: 'Your full name',
      namePlaceholder: 'First and last name',
      emailLabel: 'Your email address',
      emailPlaceholder: 'name@company.com',
      contactError: 'Please enter your name and a valid email address.',
      step3Title: 'Step 3 of 3 · How can we help you?',
      filterPrompt: 'Choose the topic of your inquiry:',
      optFranchise: 'Franchise opportunity',
      optService: 'Pest control or sanitization service',
      optSupport: 'I am a franchisee (Support)',
      optOther: 'Other inquiry',
      nextBtn: 'Next →',
      backBtn: '← Back',
      readyMsg: (name, filter) => `Thank you, ${name}! Your inquiry is filtered under “${filter}”. You can now write your message below.`
    },
    pt: {
      chatLabel: 'Chat', open: 'Abrir chat com Truly IA', title: 'Truly IA', sub: 'Chat da Truly Nolen',
      intro: 'Olá, sou a Truly IA. Para conversar aqui no site, informe seus dados rápidos abaixo; ou continue diretamente pelo WhatsApp.',
      change: 'Alterar filtro / assunto', notice: 'Conversa com IA.', waOffer: 'Você também pode continuar pelo WhatsApp.',
      lockedPlaceholder: 'Conclua as etapas acima para escrever…',
      step1Title: 'Etapa 1 de 3 · Seu WhatsApp ou telefone',
      waLabel: 'Qual é o seu número de WhatsApp?',
      phoneLabel: 'Qual é o seu número de telefone?',
      phonePlaceholder: '+55 11 90000 0000',
      noWaToggle: 'Não tenho WhatsApp — informar meu telefone',
      phoneError: 'Informe um número válido (mínimo de 7 dígitos).',
      step2Title: 'Etapa 2 de 3 · Seus dados para ajudá-lo melhor',
      nameLabel: 'Seu nome completo',
      namePlaceholder: 'Nome e sobrenome',
      emailLabel: 'Seu e-mail',
      emailPlaceholder: 'nome@empresa.com',
      contactError: 'Informe seu nome e um e-mail válido.',
      step3Title: 'Etapa 3 de 3 · Como podemos ajudar?',
      filterPrompt: 'Escolha o tema da sua consulta:',
      optFranchise: 'Oportunidade de franquia',
      optService: 'Serviço de controle de pragas ou sanitização',
      optSupport: 'Já sou franqueado (Suporte)',
      optOther: 'Outra consulta',
      nextBtn: 'Continuar →',
      backBtn: '← Voltar',
      readyMsg: (name, filter) => `Obrigado, ${name}! Sua consulta foi classificada em “${filter}”. Agora você já pode escrever sua mensagem abaixo.`
    },
    ar: {
      chatLabel: 'محادثة', open: 'افتح المحادثة مع Truly IA', title: 'Truly IA', sub: 'محادثة ترولي نولن',
      intro: 'مرحبًا، أنا Truly IA. للتحدث هنا عبر الموقع، يُرجى مشاركة بياناتك السريعة أدناه، أو يمكنك المتابعة مباشرة عبر واتساب.',
      change: 'تغيير الموضوع', notice: 'محادثة مع الذكاء الاصطناعي.', waOffer: 'يمكنك أيضًا المتابعة عبر واتساب.',
      lockedPlaceholder: 'أكمل الخطوات أعلاه للبدء بالكتابة…',
      step1Title: 'الخطوة 1 من 3 · رقم واتساب أو الهاتف',
      waLabel: 'ما هو رقم واتساب الخاص بك؟',
      phoneLabel: 'ما هو رقم هاتفك؟',
      phonePlaceholder: '+971 50 000 0000',
      noWaToggle: 'ليس لدي واتساب — سأدخل رقم هاتفي',
      phoneError: 'يُرجى إدخال رقم صحيح (7 أرقام على الأقل).',
      step2Title: 'الخطوة 2 من 3 · بياناتك لمساعدتك بشكل أفضل',
      nameLabel: 'الاسم الكامل',
      namePlaceholder: 'الاسم واللقب',
      emailLabel: 'البريد الإلكتروني',
      emailPlaceholder: 'name@company.com',
      contactError: 'يُرجى إدخال الاسم وبريد إلكتروني صحيح.',
      step3Title: 'الخطوة 3 من 3 · كيف يمكننا مساعدتك؟',
      filterPrompt: 'اختر موضوع استفسارك:',
      optFranchise: 'فرصة امتياز تجاري (فرنشايز)',
      optService: 'خدمة مكافحة الآفات أو التعقيم',
      optSupport: 'أنا صاحب امتياز حالي (الدعم)',
      optOther: 'استفسار آخر',
      nextBtn: 'التالي ←',
      backBtn: '→ رجوع',
      readyMsg: (name, filter) => `شكرًا لك يا ${name}! تم تصنيف استفسارك ضمن «${filter}». يمكنك الآن كتابة رسالتك أدناه.`
    }
  }[lang]);

  function element(tag, cls, text) { const n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; }
  function car(lights = false) {
    const n = new Image(); n.src = '/assets/mouse-car.png'; n.alt = ''; n.width = 92; n.height = 59; n.className = 'tn-chat-car';
    if (!lights || family !== 'a') return n;
    const scene = element('span', 'tn-chat-car-scene'); scene.setAttribute('aria-hidden', 'true'); scene.append(n);
    scene.append(element('span', 'tn-chat-lamp tn-chat-lamp-near'), element('span', 'tn-chat-lamp tn-chat-lamp-far')); return scene;
  }

  const launch = element('button', 'tn-chat-launcher'); launch.type = 'button'; launch.setAttribute('aria-label', copy.open); launch.setAttribute('aria-expanded', 'false'); launch.setAttribute('aria-controls', 'tn-franchise-chat'); launch.append(car(true));
  const cue = element('span', 'tn-chat-cue'); cue.setAttribute('aria-hidden', 'true');
  cue.append(element('span', 'tn-chat-cue-label', copy.chatLabel)); launch.append(cue);
  launch.title = copy.open;

  const panel = element('section'); panel.id = 'tn-franchise-chat'; panel.hidden = true; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-labelledby', 'tn-chat-title');
  const heading = element('div', 'tn-chat-heading'), identity = element('div', 'tn-chat-identity');
  const title = element('h2', '', copy.title); title.id = 'tn-chat-title'; const subtitle = element('p', '', copy.sub);
  const change = element('button', 'tn-chat-change', copy.change); change.type = 'button'; change.setAttribute('aria-expanded', 'false'); change.setAttribute('aria-controls', 'tn-chat-topics');
  identity.append(title, subtitle); const close = element('button', 'tn-chat-close', '×'); close.type = 'button'; close.setAttribute('aria-label', copy.close); heading.append(car(), identity, close);

  const log = element('div', 'tn-chat-log'); log.setAttribute('role', 'log'); log.setAttribute('aria-live', 'polite'); log.setAttribute('aria-relevant', 'additions'); log.setAttribute('aria-label', en ? t('Conversation') : 'Conversación');
  log.tabIndex = 0;

  const choices = element('div', 'tn-chat-choices'); choices.id = 'tn-chat-topics'; choices.hidden = true; choices.setAttribute('aria-label', en ? t('Choose a topic') : 'Elija un tema');
  const suggestions = element('div', 'tn-chat-suggestions'); suggestions.append(change, choices);

  const form = element('form', 'tn-chat-form'), input = element('input'); input.id = 'tn-chat-input'; input.type = 'text'; input.maxLength = 2000; input.placeholder = copy.placeholder; input.autocomplete = 'off';
  const label = element('label', 'tn-chat-sr', copy.placeholder); label.htmlFor = input.id;
  const submit = element('button', 'tn-chat-send', '↑'); submit.type = 'submit'; submit.disabled = true; submit.setAttribute('aria-label', copy.send); form.append(label, input, submit);

  const bottom = element('div', 'tn-chat-bottom'); const privacy = element('a', '', copy.privacy); privacy.href = `${basePrefix}/${lang}/privacy/`; if (family === 'b' && !en) privacy.href = '/b/en/privacy/'; bottom.append(element('p', '', copy.notice + ' ')); bottom.firstChild.append(privacy);
  const resources = element('nav', 'tn-chat-resources'); resources.setAttribute('aria-label', en ? t('Official resources') : 'Recursos oficiales');
  const portal = element('a', '', copy.portal); portal.href = 'https://www.trulynoleninternational.com/franchise/'; portal.target = '_blank'; portal.rel = 'noopener';
  const apply = element('a', '', copy.apply); apply.href = `${basePrefix}/${lang}/franchise/model/`; if (family === 'b' && !en) apply.href = '/b/en/franchise/model/'; resources.append(portal, apply); bottom.prepend(resources);

  // Pre-chat 3-step lead capture & intent filter
  const intake = element('div', 'tn-chat-intake');
  const content = element('div', 'tn-chat-content'); content.append(log, intake, suggestions, bottom);
  panel.append(heading, content, form); document.body.append(launch, panel);

  let busy = false, chatIntent = 'service', filterCategory = 'service', opener = launch, lastFailure = null;
  const history = [];

  const preview = !['trulynoleninternational.com', 'www.trulynoleninternational.com', 'site.trulynoleninternational.com', 'globaltni.com', 'www.globaltni.com'].includes(location.hostname);
  const sessionPrefix = preview ? 'tniweb-preview-' : 'tniweb-';
  const sessionId = (() => {
    const clave = preview ? 'tn-chat-sesion-preview' : 'tn-chat-sesion';
    try {
      const previa = sessionStorage.getItem(clave); if (previa) return previa;
      const nueva = sessionPrefix + (crypto.randomUUID ? crypto.randomUUID().slice(0, 18) : Math.random().toString(36).slice(2, 20));
      sessionStorage.setItem(clave, nueva); return nueva;
    } catch { return sessionPrefix + Math.random().toString(36).slice(2, 20); }
  })();
  const sourceRef = preview ? 'tni-site-preview' : 'tni-site';
  const pageOrigin = () => `${location.origin}${location.pathname}`;
  const track = (name, props = {}) => window.tniTrack?.(name, { intent: chatIntent, ...props });

  const LEAD_STORAGE_KEY = 'tn-chat-lead-v2';
  let leadData = null;

  const waCopy = {
    es: ['Continuar por WhatsApp', 'Hola, vengo del sitio de Truly Nolen y quisiera continuar mi consulta.'],
    en: ['Continue on WhatsApp', 'Hello, I came from the Truly Nolen website and would like to continue my inquiry.'],
    pt: ['Continuar pelo WhatsApp', 'Olá, vim do site da Truly Nolen e gostaria de continuar minha consulta.'],
    ar: ['المتابعة عبر واتساب', 'مرحبًا، وصلت من موقع Truly Nolen وأرغب في متابعة استفساري.']
  }[lang];
  const handoff = element('div', 'tn-chat-handoff'); handoff.hidden = true;
  const whatsapp = element('a', 'tn-chat-whatsapp', waCopy[0]);
  whatsapp.target = '_blank';
  whatsapp.rel = 'noopener noreferrer';
  handoff.append(whatsapp); panel.append(handoff);
  let whatsappNumber = '';
  function updateWhatsapp() {
    if (!whatsappNumber) return;
    whatsapp.dataset.intent = chatIntent;
    const leadLine = leadData ? `\nNombre: ${leadData.name}\n${leadData.phone_type === 'whatsapp' ? 'WhatsApp' : 'Tel'}: ${leadData.phone}\nEmail: ${leadData.email}\nTema: ${leadData.filter_label || filterCategory}` : '';
    whatsapp.href = 'https://wa.me/' + whatsappNumber + '?text=' + encodeURIComponent(waCopy[1] + leadLine + '\n' + pageOrigin() + '\n' + lang.toUpperCase() + ' · ' + filterCategory + '\n[ref:' + sourceRef + ']\nRef: ' + sessionId);
  }
  const siteConfigReady = fetch('/assets/site-config.json', { signal: AbortSignal.timeout(8000) }).then(r => r.ok ? r.json() : null).then(c => {
    if (c?.whatsapp?.enabled && /^[1-9]\d{6,14}$/.test(c.whatsapp.number)) {
      whatsappNumber = c.whatsapp.number; updateWhatsapp();
      handoff.hidden = false;
    }
  }).catch(() => {});
  const configReady = fetch('/assets/franchise-chat-config.json', { signal: AbortSignal.timeout(8000) }).then(r => r.ok ? r.json() : Promise.reject()).catch(() => ({ enabled: false }));
  const allowedHosts = new Set(['site.trulynoleninternational.com', 'www.trulynoleninternational.com', 'trulynoleninternational.com', 'globaltni.com', 'www.globaltni.com', 'trulyinternational.catalizadora.ai', 'vip.trulynoleninternational.com']);

  function bubble(text, role = 'assistant', links = []) {
    const wrap = element('div', 'tn-chat-message'); wrap.dataset.role = role;
    const paragraph = element('p', 'tn-chat-bubble');
    for (const part of (role === 'assistant' ? text.split(/(\*\*[^*\n]+\*\*)/g) : [text])) {
      paragraph.append(role === 'assistant' && /^\*\*[^*\n]+\*\*$/.test(part)
        ? element('strong', '', part.slice(2, -2)) : document.createTextNode(part));
    }
    wrap.append(paragraph);
    if (role === 'assistant' && Array.isArray(links)) {
      const nav = element('div', 'tn-chat-links');
      for (const link of links.slice(0, 3)) {
        try {
          const url = new URL(link.url); if (url.protocol !== 'https:' || !allowedHosts.has(url.hostname) || typeof link.label !== 'string') continue;
          const a = element('a', '', link.label); a.href = url.href; a.target = '_blank'; a.rel = 'noopener'; a.append(element('span', 'tn-chat-sr', en ? ' ' + t('(opens a new tab)') : ' (abre otra pestaña)')); nav.append(a);
        } catch { /* Ignore malformed link metadata. */ }
      }
      if (nav.children.length) wrap.append(nav);
    }
    log.append(wrap); scrollConversation(); return wrap;
  }

  const phone = matchMedia('(max-width:600px)');
  let fullViewportHeight = innerHeight, viewportWidth = innerWidth, viewportFrame = 0;
  function scrollConversation() {
    if (phone.matches) content.scrollTop = Math.max(0, log.offsetTop + log.offsetHeight - content.clientHeight + 12);
    else log.scrollTop = log.scrollHeight;
  }
  function syncViewport() {
    viewportFrame = 0;
    const viewport = window.visualViewport;
    const height = viewport?.height || innerHeight;
    const offset = viewport?.offsetTop || 0;
    if (panel.hidden || viewportWidth !== innerWidth) fullViewportHeight = innerHeight;
    else fullViewportHeight = Math.max(fullViewportHeight, innerHeight);
    viewportWidth = innerWidth;
    const keyboard = phone.matches && !panel.hidden && fullViewportHeight - height > 120;
    panel.dataset.keyboard = String(keyboard);
    panel.style.setProperty('--tn-chat-available-height', Math.max(0, height - 24) + 'px');
    panel.style.setProperty('--tn-chat-bottom', Math.max(12, innerHeight - offset - height + 12) + 'px');
  }
  function scheduleViewport() { if (!viewportFrame) viewportFrame = requestAnimationFrame(syncViewport); }
  window.visualViewport?.addEventListener('resize', scheduleViewport);
  window.visualViewport?.addEventListener('scroll', scheduleViewport);
  addEventListener('resize', scheduleViewport);
  input.addEventListener('focus', scheduleViewport);
  input.addEventListener('blur', scheduleViewport);
  phone.addEventListener('change', scheduleViewport);

  const welcome = bubble(copy.intro);

  // Build the 3-step pre-chat lead capture & filter UI
  let draftPhone = leadData?.phone || '';
  let draftNoWa = leadData?.phone_type === 'phone';
  let draftName = leadData?.name || '';
  let draftEmail = leadData?.email || '';

  function unlockComposer(lead, announce = false) {
    leadData = lead;
    filterCategory = lead.intent;
    chatIntent = ['new_franchise', 'service', 'support'].includes(lead.intent) ? lead.intent : 'service';
    updateWhatsapp();
    intake.hidden = true;
    form.hidden = false;
    bottom.hidden = false;
    if (whatsappNumber) handoff.hidden = false;
    suggestions.hidden = false;
    input.disabled = false;
    input.placeholder = copy.placeholder;
    submit.disabled = !input.value.trim();
    if (announce && lead.filter_label) {
      bubble(copy.readyMsg(lead.name.split(' ')[0], lead.filter_label), 'assistant');
    }
    if (!panel.hidden) input.focus({ preventScroll: true });
  }

  function renderIntakeStep(step) {
    intake.replaceChildren();
    const card = element('div', 'tn-chat-intake-card');

    if (step === 1) {
      const stepHeading = element('p', 'tn-chat-intake-step', copy.step1Title);
      const fieldLabel = element('label', 'tn-chat-intake-label', draftNoWa ? copy.phoneLabel : copy.waLabel);
      fieldLabel.htmlFor = 'tn-chat-lead-phone';
      const phoneInput = element('input', 'tn-chat-intake-input');
      phoneInput.id = 'tn-chat-lead-phone';
      phoneInput.type = 'tel';
      phoneInput.inputMode = 'tel';
      phoneInput.autocomplete = 'tel';
      phoneInput.placeholder = copy.phonePlaceholder;
      phoneInput.value = draftPhone;

      const toggleLabel = element('label', 'tn-chat-intake-toggle');
      const toggleBox = element('input');
      toggleBox.type = 'checkbox';
      toggleBox.checked = draftNoWa;
      toggleLabel.append(toggleBox, element('span', '', copy.noWaToggle));

      const err = element('p', 'tn-chat-intake-error');
      err.hidden = true;

      const actions = element('div', 'tn-chat-intake-actions');
      const next = element('button', 'tn-chat-intake-next', copy.nextBtn);
      next.type = 'button';
      actions.append(next);

      toggleBox.addEventListener('change', () => {
        draftNoWa = toggleBox.checked;
        fieldLabel.textContent = draftNoWa ? copy.phoneLabel : copy.waLabel;
        phoneInput.focus({ preventScroll: true });
      });

      const proceedStep1 = () => {
        const val = phoneInput.value.trim();
        if (val.replace(/\D/g, '').length < 7) {
          err.textContent = copy.phoneError;
          err.hidden = false;
          phoneInput.setAttribute('aria-invalid', 'true');
          phoneInput.focus();
          return;
        }
        draftPhone = val;
        renderIntakeStep(2);
      };

      next.addEventListener('click', proceedStep1);
      phoneInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') { e.preventDefault(); proceedStep1(); }
      });

      card.append(stepHeading, fieldLabel, phoneInput, toggleLabel, err, actions);
      intake.append(card);
      if (!panel.hidden) phoneInput.focus({ preventScroll: true });
    } else if (step === 2) {
      const stepHeading = element('p', 'tn-chat-intake-step', copy.step2Title);
      const nameLabel = element('label', 'tn-chat-intake-label', copy.nameLabel);
      nameLabel.htmlFor = 'tn-chat-lead-name';
      const nameInput = element('input', 'tn-chat-intake-input');
      nameInput.id = 'tn-chat-lead-name';
      nameInput.type = 'text';
      nameInput.autocomplete = 'name';
      nameInput.placeholder = copy.namePlaceholder;
      nameInput.value = draftName;

      const emailLabel = element('label', 'tn-chat-intake-label', copy.emailLabel);
      emailLabel.htmlFor = 'tn-chat-lead-email';
      const emailInput = element('input', 'tn-chat-intake-input');
      emailInput.id = 'tn-chat-lead-email';
      emailInput.type = 'email';
      emailInput.autocomplete = 'email';
      emailInput.placeholder = copy.emailPlaceholder;
      emailInput.value = draftEmail;

      const err = element('p', 'tn-chat-intake-error');
      err.hidden = true;

      const actions = element('div', 'tn-chat-intake-actions');
      const back = element('button', 'tn-chat-intake-back', copy.backBtn);
      back.type = 'button';
      const next = element('button', 'tn-chat-intake-next', copy.nextBtn);
      next.type = 'button';
      actions.append(back, next);

      back.addEventListener('click', () => {
        draftName = nameInput.value.trim();
        draftEmail = emailInput.value.trim();
        renderIntakeStep(1);
      });

      const proceedStep2 = () => {
        const nVal = nameInput.value.trim();
        const eVal = emailInput.value.trim();
        if (nVal.length < 2 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(eVal)) {
          err.textContent = copy.contactError;
          err.hidden = false;
          (nVal.length < 2 ? nameInput : emailInput).focus();
          return;
        }
        draftName = nVal;
        draftEmail = eVal;
        renderIntakeStep(3);
      };

      next.addEventListener('click', proceedStep2);
      emailInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') { e.preventDefault(); proceedStep2(); }
      });

      card.append(stepHeading, nameLabel, nameInput, emailLabel, emailInput, err, actions);
      intake.append(card);
      if (!panel.hidden) nameInput.focus({ preventScroll: true });
    } else if (step === 3) {
      const stepHeading = element('p', 'tn-chat-intake-step', copy.step3Title);
      const prompt = element('p', 'tn-chat-intake-label', copy.filterPrompt);
      const grid = element('div', 'tn-chat-intake-filters');

      const options = [
        ['new_franchise', copy.optFranchise],
        ['service', copy.optService],
        ['support', copy.optSupport],
        ['other', copy.optOther]
      ];

      for (const [intentKey, labelText] of options) {
        const btn = element('button', 'tn-chat-filter-btn', labelText);
        btn.type = 'button';
        btn.dataset.filterIntent = intentKey;
        btn.addEventListener('click', () => {
          const lead = {
            phone: draftPhone,
            phone_type: draftNoWa ? 'phone' : 'whatsapp',
            name: draftName,
            email: draftEmail,
            intent: intentKey,
            filter_label: labelText
          };
          try { sessionStorage.setItem(LEAD_STORAGE_KEY, JSON.stringify(lead)); } catch {}
          fetch('/api/chat-lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              name: lead.name,
              email: lead.email,
              phone: lead.phone,
              phone_type: lead.phone_type,
              intent: lead.intent,
              lang,
              page: location.pathname,
              session_id: sessionId
            })
          }).catch(() => {});
          unlockComposer(lead, true);
        });
        grid.append(btn);
      }

      const actions = element('div', 'tn-chat-intake-actions');
      const back = element('button', 'tn-chat-intake-back', copy.backBtn);
      back.type = 'button';
      back.addEventListener('click', () => renderIntakeStep(2));
      actions.append(back);

      card.append(stepHeading, prompt, grid, actions);
      intake.append(card);
      if (!panel.hidden) grid.firstChild?.focus({ preventScroll: true });
    }
  }

  if (leadData) {
    unlockComposer(leadData, false);
  } else {
    form.hidden = true;
    bottom.hidden = true;
    suggestions.hidden = true;
    input.disabled = true;
    submit.disabled = true;
    input.placeholder = copy.lockedPlaceholder;
    renderIntakeStep(1);
  }

  for (const [text, message, intent] of [[copy.new, copy.newMessage, 'new_franchise'], [copy.service, copy.serviceMessage, 'service'], [copy.support, copy.supportMessage, 'support']]) {
    const button = element('button', '', text); button.type = 'button';
    button.addEventListener('click', () => {
      if (busy || !leadData) return;
      chatIntent = intent;
      filterCategory = intent;
      leadData.intent = intent;
      try { sessionStorage.setItem(LEAD_STORAGE_KEY, JSON.stringify(leadData)); } catch {}
      updateWhatsapp();
      send(message, intent);
    });
    choices.append(button);
  }
  change.addEventListener('click', () => {
    if (busy || !leadData) return;
    choices.hidden = !choices.hidden;
    change.setAttribute('aria-expanded', String(!choices.hidden));
    if (!choices.hidden) {
      choices.firstChild.focus({ preventScroll: true });
      if (phone.matches) content.scrollTop = suggestions.offsetTop;
      else log.scrollTop = log.scrollHeight;
    }
  });

  function show(event) {
    if (panel.hidden) track('chat_open');
    opener = event?.currentTarget || launch;
    const menu = document.querySelector('.menu-toggle[aria-expanded=true]');
    if (menu) menu.click();
    panel.hidden = false;
    launch.setAttribute('aria-expanded', 'true');
    syncViewport();
    const firstInput = !intake.hidden ? intake.querySelector('input, button') : input;
    (firstInput || close).focus({ preventScroll: true });
  }
  function hide() {
    input.blur();
    panel.hidden = true;
    launch.setAttribute('aria-expanded', 'false');
    const visible = n => n?.isConnected && n.getClientRects().length && getComputedStyle(n).visibility !== 'hidden';
    const target = visible(opener) ? opener : visible(launch) ? launch : document.querySelector('.menu-toggle');
    target?.focus({ preventScroll: true });
  }
  launch.addEventListener('click', show);
  document.querySelectorAll('[data-franchise-chat-open]').forEach(n => n.addEventListener('click', show));
  close.addEventListener('click', hide);
  panel.addEventListener('keydown', e => { if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); hide(); } });
  input.addEventListener('input', () => submit.disabled = busy || !leadData || !chatIntent || !input.value.trim());
  form.addEventListener('submit', e => { e.preventDefault(); if (!leadData) return; send(input.value.trim(), chatIntent); });

  async function send(message, intent) {
    if (busy || !leadData || !message || !intent || message.length > 2000) return;
    panel.dataset.conversation = 'true'; suggestions.hidden = true;
    const returnToComposer = document.activeElement === input || document.activeElement === submit;
    track('chat_message_sent'); busy = true; submit.disabled = true; input.readOnly = true; change.disabled = true; choices.querySelectorAll('button').forEach(b => b.disabled = true); log.setAttribute('aria-busy', 'true');
    choices.hidden = true; input.value = ''; lastFailure?.remove();
    const user = bubble(message, 'user'); const status = element('p', 'tn-chat-status', copy.thinking); status.setAttribute('role', 'status'); log.append(status); scrollConversation();
    const controller = new AbortController(), timeout = setTimeout(() => controller.abort(), 25000);
    try {
      const [config] = await Promise.all([configReady, siteConfigReady]);
      if (!config?.enabled) { track('chat_error', { result: 'disabled' }); bubble(copy.pending); return; }
      const hub = config.brain === 'hub' && config.hub?.url && config.hub?.tenant_slug;
      if (!hub && !config.endpoint) { track('chat_error', { result: 'unconfigured' }); bubble(copy.pending); return; }
      const handoffContext = whatsappNumber ? `This chat has a persistent "${waCopy[0]}" button below the message field, opening the existing Truly IA WhatsApp channel +${whatsappNumber}. ` : '';
      const leadSummary = leadData ? ` · ${leadData.name} · ${leadData.phone_type === 'whatsapp' ? 'WhatsApp' : 'Tel'}: ${leadData.phone} · ${leadData.email} · Filtro: ${filterCategory}` : '';
      const leadContext = leadData ? `Visitor contact details already collected in pre-chat form: Name="${leadData.name}", Email="${leadData.email}", ${leadData.phone_type === 'whatsapp' ? 'WhatsApp' : 'Phone'}="${leadData.phone}", Selected Filter="${filterCategory}" (${leadData.filter_label || intent}). Do NOT ask the visitor for their name, email, or phone/WhatsApp number again. ` : '';
      const r = hub
        ? await fetch(config.hub.url, {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
            tenant_slug: config.hub.tenant_slug, session_id: sessionId, ref: sourceRef, greeting: welcome.innerText,
            message: `[Origen web: Sitio TNI${preview ? ' · Vista previa' : ''}${leadSummary} · ${pageOrigin()} · ${lang.toUpperCase()} · ${intent}]\n${message}`,
            page_context: `${handoffContext}${leadContext}${config.hub.site_label || 'Sitio TNI'} · ${preview ? 'Design preview' : 'Public website'} · ${document.title} · ${pageOrigin()} · Topic: ${intent}. Visitor language: ${lang}. Reply in ${{ es: 'Spanish', en: 'English', pt: 'Portuguese', ar: 'Modern Standard Arabic' }[lang]}. Corporate website figures approved by TNI: 65 countries; over 300 offices; over 80 years of experience.`
          }), signal: controller.signal
        })
        : await fetch(config.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message, lang, intent, session_id: sessionId, page: location.pathname, history: history.slice(-6).map(t => ({ role: t.role, content: t.content.slice(0, 2000) })) }), signal: controller.signal });
      const data = await r.json();
      if (!r.ok || data.error) {
        track('chat_error', { result: r.status === 429 ? 'rate_limited' : 'server_error' });
        if (typeof data.reply !== 'string' || !data.reply.trim()) throw Error('Invalid error response');
        const wait = r.status === 429 ? Number(r.headers.get('Retry-After')) : 0;
        bubble(data.reply + (wait > 0 ? ' ' + copy.later(Math.ceil(wait / 60)) : ''), 'assistant', data.links);
        if (r.status !== 429) addRetry(message, intent, user); return;
      }
      if (typeof data.reply !== 'string' || !data.reply.trim()) throw Error('No answer');
      track('chat_reply_received'); bubble(data.reply, 'assistant', data.links); history.push({ role: 'user', content: message }, { role: 'assistant', content: data.reply.slice(0, 2000) });
    } catch { track('chat_error', { result: controller.signal.aborted ? 'timeout' : 'network' }); bubble(copy.failed); addRetry(message, intent, user); }
    finally { clearTimeout(timeout); status.remove(); busy = false; log.removeAttribute('aria-busy'); input.readOnly = false; change.disabled = false; choices.querySelectorAll('button').forEach(b => b.disabled = false); submit.disabled = !input.value.trim(); if (returnToComposer && !panel.hidden) input.focus({ preventScroll: true }); scrollConversation(); }
  }
  function addRetry(message, intent, user) { const button = element('button', 'tn-chat-retry', copy.retry); button.type = 'button'; button.addEventListener('click', () => { if (busy) return; user.remove(); send(message, intent); }); log.append(button); lastFailure = button; }
})();
