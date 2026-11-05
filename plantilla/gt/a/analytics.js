/** Explicit TNI events. No form values, chat text, contact details or URL queries. */
(() => {
  const allowed=new Set(['page_view','chat_open','chat_message_sent','chat_reply_received','chat_error','whatsapp_click','form_started','form_submitted','form_success','form_error','language_changed','office_contact_click','franchise_click','video_play']);
  const lang=document.documentElement.lang;
  // Where it runs: the live hosts send environment=production; any other address (pages.dev, local, staging) sends the build's environment.
  const PRODUCTION_HOSTS=new Set(['trulynoleninternational.com','www.trulynoleninternational.com','site.trulynoleninternational.com','globaltni.com','www.globaltni.com']);
  const queue=[];let sdk=null,enabled=false,optedOut=false,googleId=null;
  const TOKEN=/^[a-z0-9_-]{1,50}$/;
  // Each extra property has its own shape; anything else is dropped. referrer/referring_domain only come from this file (page_view).
  const safeKeys={intent:TOKEN,kind:TOKEN,result:TOKEN,target_language:TOKEN,channel:TOKEN,video:TOKEN,referrer:/^https?:\/\/[^?#\s]{1,200}$/,referring_domain:/^[a-z0-9.-]{1,100}$/};
  const properties={site:'tni-corporate',hostname:location.hostname,page_path:location.pathname,language:lang};
  window.tniTrack=(name,extras={})=>{
    if(optedOut||!allowed.has(name))return;
    const safe={...properties};
    for(const [k,v]of Object.entries(extras))if(safeKeys[k]&&typeof v==='string'&&safeKeys[k].test(v))safe[k]=v;
    if(enabled&&sdk)sdk.track(name,safe);
    else if(queue.length<40)queue.push([name,safe]);
  };
  const track=window.tniTrack;
  // Where the visit came from: the referring site's domain and path (never its query), only when it is another site.
  const pageView={};
  try{if(document.referrer){const r=new URL(document.referrer);if(r.hostname&&r.hostname!==location.hostname){pageView.referrer=r.origin+r.pathname;pageView.referring_domain=r.hostname.replace(/^www\./,'');}}}catch{}
  track('page_view',pageView);
  document.addEventListener('click',event=>{
    const a=event.target.closest('a[href]');if(!a)return;
    const url=new URL(a.href,location.href);
    if(a.hreflang)track('language_changed',{target_language:a.hreflang});
    else if(url.hostname==='wa.me')track('whatsapp_click',{intent:a.dataset.intent||'service'});
    else if(['tel:','mailto:'].includes(url.protocol))track('office_contact_click',{channel:url.protocol==='tel:'?'phone':'email'});
    else if(url.pathname.includes('/franchise/'))track('franchise_click');
  });
  document.querySelectorAll('form.tn-form').forEach(form=>form.addEventListener('focusin',()=>track('form_started',{kind:form.dataset.formKind||'customer'}),{once:true}));
  document.querySelectorAll('video').forEach(video=>video.addEventListener('play',()=>track('video_play',{video:video.classList.contains('car-video')?'hero':'content'}),{once:true}));
  // Preserve opt-out and do not initialize analytics under Global Privacy Control.
  try{optedOut=localStorage.getItem('tni-analytics-opt-out')==='1'}catch{}
  window.tniAnalyticsOptOut=()=>{optedOut=true;try{localStorage.setItem('tni-analytics-opt-out','1')}catch{};enabled=false;queue.length=0;sdk?.setOptOut(true);if(googleId)window['ga-disable-'+googleId]=true};
  document.querySelector('[data-analytics-opt-out]')?.addEventListener('click',event=>{window.tniAnalyticsOptOut();event.currentTarget.disabled=true;event.currentTarget.textContent={es:'Medición desactivada',en:'Analytics disabled',pt:'Medição desativada',ar:'تم تعطيل التحليلات'}[lang]||'Analytics disabled'});
  optedOut=optedOut||navigator.globalPrivacyControl===true;
  if(optedOut){queue.length=0;return;}
  // Where the visitor is: country and city as Cloudflare sees the connection (functions/api/geo.js). The IP is neither stored nor sent.
  const geo=(async()=>{
    try{
      const kept=sessionStorage.getItem('tni-geo');if(kept)return JSON.parse(kept);
      const r=await fetch('/api/geo',{signal:AbortSignal.timeout(4000)});if(!r.ok)return {};
      const g=await r.json();const where={};
      if(/^[A-Z]{2}$/.test(g.country||''))where.country=g.country;
      if(typeof g.city==='string'&&g.city&&g.city.length<=60)where.city=g.city;
      try{sessionStorage.setItem('tni-geo',JSON.stringify(where))}catch{}
      return where;
    }catch{return {}}
  })();
  // Google Analytics 4 (requested by Pablo, 10 Oct 2026): the standard gtag.js tag with the measurement ID from site-config.json.
  // Same gate as Amplitude (opt-out and Global Privacy Control stop it above) and only on the live hosts, so previews never count as traffic.
  const loadGoogle=id=>{
    if(!/^G-[A-Z0-9]{6,14}$/.test(id||'')||properties.environment!=='production')return;
    googleId=id;window.dataLayer=window.dataLayer||[];window.gtag=window.gtag||function(){window.dataLayer.push(arguments)};
    window.gtag('js',new Date());window.gtag('config',id);
    const tag=document.createElement('script');tag.async=true;tag.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(id);document.head.append(tag);
  };
  Promise.all([fetch('/assets/site-config.json',{signal:AbortSignal.timeout(8000)}).then(r=>r.ok?r.json():Promise.reject()),geo]).then(([config,where])=>{
    const a=config.analytics;
    properties.environment=PRODUCTION_HOSTS.has(location.hostname)?'production':(config.environment||'preview');
    loadGoogle(a?.google?.measurementId);
    if(!a?.enabled||!a.apiKey)return;
    Object.assign(properties,where);
    const script=document.createElement('script');script.async=true;
    script.src='https://cdn.amplitude.com/libs/analytics-browser-2.40.0-min.js.gz';
    script.onload=async()=>{
      if(!window.amplitude)return;
      sdk=window.amplitude;
      await sdk.init(a.apiKey,undefined,{serverZone:a.serverZone||'US',logLevel:0,autocapture:false,defaultTracking:false,remoteConfig:{fetchRemoteConfig:false},identityStorage:'sessionStorage',trackingOptions:{ipAddress:false},attribution:{disabled:true}}).promise;
      if(optedOut){sdk.setOptOut(true);return;}
      enabled=true;
      for(const [name,props]of queue.splice(0))sdk.track(name,{...props,...where,environment:properties.environment});
    };
    addEventListener('pagehide',()=>{if(enabled){sdk?.setTransport?.('beacon');sdk?.flush()}});
    script.onerror=()=>{queue.length=0};
    document.head.append(script);
  }).catch(()=>{queue.length=0});
})();
