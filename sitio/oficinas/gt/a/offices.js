(()=>{
 const query=document.querySelector('#office-query');if(!query)return;
 const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const markets=[...document.querySelectorAll('[data-market]')];const counter=document.querySelector('#office-count');const initial=counter.textContent;const empty=document.querySelector('.s-office-empty');const resets=[...document.querySelectorAll('[data-office-reset]')];
 const ALIASES={
  'arabia-saudita':'saudi-arabia saudi arabia ksa riyadh jeddah',
  'belice':'belize',
  'brazil':'brasil brazil sao paulo rio',
  'egipto':'egypt cairo',
  'espana':'spain espana madrid barcelona',
  'filipinas':'philippines manila cebu',
  'francia':'france paris',
  'islas-turcas-y-caicos':'turks-caicos turks and caicos',
  'jordania':'jordan amman',
  'kazajistan':'kazakhstan almaty',
  'libano':'lebanon beirut',
  'macedonia-del-norte':'north-macedonia north macedonia skopje',
  'malasia':'malaysia kuala lumpur',
  'nueva-zelanda':'new-zealand new zealand auckland',
  'paises-bajos':'netherlands benelux holland holanda amsterdam',
  'republica-democratica-del-congo':'democratic-republic-of-congo drc congo kinshasa',
  'republica-dominicana':'dominican-republic dominican republic santo domingo',
  'tailandia':'thailand bangkok',
  'turquia':'turkey turkiye istanbul',
  'ucrania':'ukraine kyiv'
 };
 const SLUG_TO_ID={
  'saudi-arabia':'arabia-saudita','belize':'belice','brasil':'brazil','egypt':'egipto','spain':'espana',
  'philippines':'filipinas','france':'francia','turks-caicos':'islas-turcas-y-caicos','jordan':'jordania',
  'kazakhstan':'kazajistan','lebanon':'libano','north-macedonia':'macedonia-del-norte','malaysia':'malasia',
  'new-zealand':'nueva-zelanda','netherlands':'paises-bajos','benelux':'paises-bajos',
  'democratic-republic-of-congo':'republica-democratica-del-congo','dominican-republic':'republica-dominicana',
  'thailand':'tailandia','turkey':'turquia','turkiye':'turquia','ukraine':'ucrania'
 };
 function filter(){
  const value=normalize(query.value.trim());let total=0,regions=0;
  for(const market of markets){
   const alias=ALIASES[market.id]||'';
   let visible=0;
   for(const card of market.querySelectorAll('[data-office]')){
    const show=!value||normalize(market.querySelector('summary').textContent+' '+alias+' '+card.textContent).includes(value);
    card.hidden=!show;if(show)visible++;
   }
   const show=!value||visible>0||(!market.querySelector('[data-office]')&&normalize(market.textContent+' '+alias).includes(value));
   market.hidden=!show;market.open=!!value&&show;
   if(show){regions++;total+=visible;}
  }
  counter.textContent=value?(document.body.dataset.countTemplate||'').replace('{offices}',total).replace('{markets}',regions).replace('{officeWord}',total===1?document.body.dataset.officeOne:document.body.dataset.officeMany).replace('{marketWord}',regions===1?document.body.dataset.marketOne:document.body.dataset.marketMany):initial;
  empty.hidden=regions>0;resets[0].hidden=!value;
 }
 query.addEventListener('input',filter);for(const button of resets)button.addEventListener('click',()=>{query.value='';filter();query.focus();});
 function hash(){
  let id;try{id=decodeURIComponent(location.hash.slice(1)).toLowerCase()}catch{return;}
  if(!id)return;
  const resolved=SLUG_TO_ID[id]||id;
  const market=markets.find(m=>m.id===resolved||m.id===id);
  if(market){market.hidden=false;market.open=true;market.scrollIntoView({block:'start'});}
 }
 addEventListener('hashchange',hash);if(location.hash)requestAnimationFrame(hash);
})();
