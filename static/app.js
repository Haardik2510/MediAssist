const $=(s,r=document)=>r.querySelector(s),app=$('#app');let user=null;
const api=async(p,o={})=>{const h={'X-Requested-With':'fetch'};let b=o.body;if(b&&!(b instanceof FormData)){h['Content-Type']='application/json';b=JSON.stringify(b)}
 try{const r=await fetch('/api'+p,{method:o.method||(b?'POST':'GET'),headers:h,body:b});const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error(d.error||'Something went wrong. Try again.');return d}
 catch(e){if(e instanceof TypeError)throw new Error('Network error. Check your connection.');throw e}};
// analytics + error tracking (client): privacy-friendly, only if configured
fetch('/config.json').then(r=>r.ok?r.json():{}).then(c=>{if(c.plausible){const s=document.createElement('script');s.defer=1;s.dataset.domain=c.plausible;s.src='https://plausible.io/js/script.js';document.head.append(s)}}).catch(()=>{});
addEventListener('error',e=>navigator.sendBeacon&&navigator.sendBeacon('/api/log',JSON.stringify({m:e.message})));
// mouse effects: spotlight glow + per-card hover light + magnetic buttons
addEventListener('mousemove',e=>{const g=$('#glow');g.style.left=e.clientX+'px';g.style.top=e.clientY+'px';
 const c=e.target.closest?.('.card');if(c){const r=c.getBoundingClientRect();c.style.setProperty('--x',e.clientX-r.left+'px');c.style.setProperty('--y',e.clientY-r.top+'px')}});
addEventListener('scroll',()=>{$('#bar').style.width=scrollY/(document.body.scrollHeight-innerHeight)*100+'%'});
function motion(){ // scroll-triggered Anime.js reveals + text split
 const h=$('.hero h1');if(h&&!h.dataset.s){h.dataset.s=1;h.innerHTML=h.textContent.split(' ').map(w=>`<span class=w>${w}</span>`).join(' ');anime({targets:'.hero .w',opacity:[0,1],translateY:[30,0],delay:anime.stagger(90),easing:'easeOutExpo',duration:900});anime({targets:'.hero p,.hero .btn',opacity:[0,1],translateY:[20,0],delay:anime.stagger(120,{start:500})})}
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.unobserve(e.target);anime({targets:e.target,opacity:1,translateY:0,duration:800,easing:'easeOutCubic',delay:+e.target.dataset.d||0})}}),{threshold:.15});
 document.querySelectorAll('.rev').forEach((el,i)=>{el.dataset.d=(i%4)*80;io.observe(el)});
 document.querySelectorAll('.count').forEach(el=>io.observe(el))}
const nav=()=>$('#nav').innerHTML=user?`<a href=#/dash>Dashboard</a><button class="btn ghost" id=lo>Log out</button>`:`<a class=hide href=#/login>Log in</a><a class=btn href=#/signup>Get started</a>`;
const slides=[['Scan','Upload a photo or use your camera. The image is cleaned and read with OCR.'],['Understand','Notations like 1-0-1, OD, BD and TDS become a plain daily schedule.'],['Confirm','You always review and correct what was read before anything is saved.'],['Remember','Browser notifications at each dose time with Taken, Snooze and Skip.'],['Locate','Online pharmacy links and a map of stores near you.']];
const landing=()=>`<section class=hero><h1>Never misread a prescription or miss a dose again</h1><p>MediAssist scans your prescription, builds a clear schedule, reminds you on time and shows where to buy each medicine.</p><p><a class=btn href=#/signup>Create free account</a></p></section>
<section><h2 class=rev>How it works</h2><div class=slider id=sl>${slides.map((s,i)=>`<div class="card rev"><small>Step ${i+1}</small><h3>${s[0]}</h3><p>${s[1]}</p></div>`).join('')}</div><div class=ctrl><button class="btn ghost" data-sl=-1>Previous</button><button class="btn ghost" data-sl=1>Next</button></div></section>
<section><h2 class=rev>Built around the problem</h2><div class=grid><div class="card rev"><h3>Handwriting is hard</h3><p>Abbreviations are easy to misread. MediAssist expands them and asks you to confirm.</p></div><div class="card rev"><h3>Doses get missed</h3><p>Scheduled reminders with one-tap logging keep treatment on track.</p></div><div class="card rev"><h3>Finding medicine takes time</h3><p>Nearby store map and online pharmacy search in one place.</p></div></div></section>`;
const form=(id,fields,btn,extra='')=>`<section><h1>${id}</h1><form id=f novalidate>${fields.map(([n,l,t])=>`<label>${l}<input name=${n} type=${t} required autocomplete=${n==='password'?(id==='Log in'?'current-password':'new-password'):'email'}></label>`).join('')}<div class=err id=err role=alert></div><button class=btn id=sb>${btn}</button></form>${extra}</section>`;
function bind(fn){const f=$('#f');f.onsubmit=async e=>{e.preventDefault();const b=$('#sb'),er=$('#err'),d=Object.fromEntries(new FormData(f));er.textContent='';
 if(d.email!==undefined&&!/^\S+@\S+\.\S+$/.test(d.email))return er.textContent='Enter a valid email address.';
 if(d.password!==undefined&&d.password.length<8)return er.textContent='Password must be at least 8 characters.';
 b.disabled=true;b.innerHTML='<span class=spin></span>';try{await fn(d)}catch(x){er.textContent=x.message}b.disabled=false;b.textContent=b.dataset.t||'Submit'}}
const routes={
 '':()=>{app.innerHTML=landing();motion();$('[data-sl="-1"]').onclick=()=>$('#sl').scrollBy({left:-340,behavior:'smooth'});$('[data-sl="1"]').onclick=()=>$('#sl').scrollBy({left:340,behavior:'smooth'});
  const s=$('#sl');let dn=0,sx=0;s.onmousedown=e=>{dn=1;sx=e.pageX+s.scrollLeft};addEventListener('mouseup',()=>dn=0);s.onmousemove=e=>{if(dn)s.scrollLeft=sx-e.pageX}},
 signup:()=>{app.innerHTML=form('Create account',[['email','Email','email'],['password','Password (8+ characters)','password']],'Sign up','<p>Have an account? <a href=#/login>Log in</a></p>');bind(async d=>{const res=await api('/register',{body:d});$('#f').innerHTML=`<p class=ok>${res.message||'Check your inbox for a verification link, then log in.'}</p>`})},
 login:()=>{app.innerHTML=form('Log in',[['email','Email','email'],['password','Password','password']],'Log in','<p><a href=#/forgot>Forgot password?</a> | <a href=#/signup>Create account</a></p>');bind(async d=>{await api('/login',{body:d});localStorage.setItem('ma_auth','1');await boot();location.hash='#/dash'})},
 forgot:()=>{app.innerHTML=form('Reset password',[['email','Email','email']],'Send link');bind(async d=>{await api('/forgot',{body:d});$('#f').innerHTML='<p class=ok>If that email has an account, a reset link is on its way.</p>'})},
 reset:t=>{app.innerHTML=form('New password',[['password','New password','password']],'Save password');bind(async d=>{await api('/reset',{body:{...d,token:t}});location.hash='#/login'})},
 verify:async t=>{app.innerHTML='<section><span class=spin></span> Verifying...</section>';try{await api('/verify',{body:{token:t}});app.innerHTML='<section><h1>Email verified</h1><a class=btn href=#/login>Log in</a></section>'}catch(e){app.innerHTML=`<section><h1>Verification failed</h1><p class=err>${e.message}</p></section>`}},
 dash:async()=>{
  if(!user){
    app.innerHTML='<section><span class=spin></span> Checking session...</section>';
    try{user=(await api('/me')).user}catch{user=null}
    nav();
  }
  if(!user)return location.hash='#/login';
  app.innerHTML='<section><span class=spin></span> Loading...</section>';let m=[];try{m=await api('/medicines')}catch(e){app.innerHTML=`<section class=err>${e.message}</section>`;return}
  const todayStr=new Date().toISOString().slice(0,10);
  app.innerHTML=`<section><h1>Your medicines</h1>
  <div class=card><h3>Scan a prescription</h3><input type=file id=img accept="image/*" capture=environment><div class=err id=serr></div><div id=draft></div></div>

  <h2>AI Consumption & Timing Summary</h2>
  <div class=card id=ai-summary-box>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <span class="badge" id=ai-badge style="background:#0284c7;color:#fff">AI Clinical Guidance</span>
      <button class="btn ghost sm" id=btn-reload-summary>Refresh Summary</button>
    </div>
    <div id=ai-summary-body><span class=spin></span> Analyzing your medications and consumption timing...</div>
  </div>

  <h2>Timeline & History Calendar</h2>
  <div class=card>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px">
      <button class="btn ghost sm" id=cal-prev>&lt; Previous</button>
      <input type=date id=cal-date value="${todayStr}" style="width:auto;min-width:160px;padding:8px 12px">
      <button class="btn ghost sm" id=cal-next>Next &gt;</button>
      <button class="btn sm" id=cal-today>Today</button>
    </div>
    <div id=timeline-content><span class=spin></span> Loading timeline...</div>
  </div>

  <h2>Schedule</h2>
  ${m.length?`
  <div id=batch-bar style="display:none;margin-bottom:12px;padding:10px 14px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:8px;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
    <span id=batch-count style="font-weight:600">0 medicines selected</span>
    <button class="btn danger sm" id=batch-del-btn>Delete Selected Medicines</button>
  </div>
  <div class=card style="overflow-x:auto"><table>
    <tr>
      <th style="width:36px;text-align:center"><input type=checkbox id=select-all title="Select all medicines"></th>
      <th>Medicine</th><th>Frequency</th><th>Times</th><th>Days</th><th>Buy Online</th><th>Action</th>
    </tr>
    ${m.map(x=>`<tr data-mid="${x.id}">
      <td style="text-align:center"><input type=checkbox class=med-cb data-id="${x.id}"></td>
      <td><b>${esc(x.name)}</b> ${esc(x.strength)}</td>
      <td>${esc(x.freq)}</td>
      <td>${x.times.join(', ')}</td>
      <td>${x.days}d</td>
      <td><a href="https://www.1mg.com/search/all?name=${encodeURIComponent(x.name)}" target=_blank rel="noopener">1mg</a> · <a href="https://www.netmeds.com/catalogsearch/result/${encodeURIComponent(x.name)}/all" target=_blank rel="noopener">Netmeds</a></td>
      <td><button class="btn danger sm del-med" data-id="${x.id}">Delete</button></td>
    </tr>`).join('')}
  </table></div>`:'<div class=empty>No medicines yet. Scan your first prescription above.</div>'}

  <h2>Nearby pharmacies</h2>
  <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
    <a class="btn" style="background:#4285f4;color:#fff;text-decoration:none" href="https://www.google.com/maps/search/pharmacies+near+me/" target=_blank rel=noopener id=gmaps-start>Open Google Maps Nearby</a>
    <button class="btn ghost" id=loc>Use my GPS location</button>
    <div style="display:flex;gap:8px;flex:1;min-width:260px">
      <input type=text id=area placeholder="Or enter city / area / pincode (e.g. Delhi, 110001)" style="flex:1">
      <button class="btn" id=search-btn>Search Area</button>
    </div>
  </div>
  <div id=map hidden></div>
  <div id=map-status></div>
  <h2>Account</h2><button class="btn danger" id=del>Delete my account</button></section>`;

  $('#img').onchange=scan;$('#loc').onclick=nearby;
  const sBtn=$('#search-btn');
  if(sBtn){
    sBtn.onclick=()=>{ searchArea($('#area').value); };
    $('#area').onkeydown=e=>{ if(e.key==='Enter'){ e.preventDefault(); searchArea($('#area').value); } };
  }

  const updateBatchState=()=>{
    const cbs=Array.from(document.querySelectorAll('.med-cb'));
    const checked=cbs.filter(c=>c.checked);
    const bBar=$('#batch-bar');
    const bCount=$('#batch-count');
    const selAll=$('#select-all');
    if(selAll)selAll.checked=cbs.length>0&&checked.length===cbs.length;
    if(bBar){
      if(checked.length>0){
        bBar.style.display='flex';
        bCount.textContent=checked.length+' medicine'+(checked.length>1?'s':'')+' selected';
      }else{
        bBar.style.display='none';
      }
    }
  };

  const selAll=$('#select-all');
  if(selAll){
    selAll.onchange=()=>{
      document.querySelectorAll('.med-cb').forEach(c=>c.checked=selAll.checked);
      updateBatchState();
    };
  }

  document.querySelectorAll('.med-cb').forEach(c=>{
    c.onchange=updateBatchState;
  });

  const bDelBtn=$('#batch-del-btn');
  if(bDelBtn){
    bDelBtn.onclick=async()=>{
      const selected=Array.from(document.querySelectorAll('.med-cb:checked')).map(c=>+c.getAttribute('data-id'));
      if(!selected.length)return;
      if(confirm('Delete '+selected.length+' selected medicine'+(selected.length>1?'s':'')+' and all upcoming doses?')){
        bDelBtn.disabled=true;
        bDelBtn.textContent='Deleting...';
        try{
          await api('/medicines/batch-delete',{body:{ids:selected}});
          routes.dash();
        }catch(err){
          alert(err.message||'Failed to delete selected medicines.');
          bDelBtn.disabled=false;
          bDelBtn.textContent='Delete Selected Medicines';
        }
      }
    };
  }

  document.querySelectorAll('.del-med').forEach(btn=>{
    btn.onclick=async()=>{
      const mid=btn.getAttribute('data-id');
      if(confirm('Are you sure you want to delete this medicine and its upcoming doses?')){
        btn.disabled=true;
        try{
          await api('/medicines/'+mid,{method:'DELETE'});
          routes.dash();
        }catch(err){
          alert(err.message||'Failed to delete medicine.');
          btn.disabled=false;
        }
      }
    };
  });

  const loadTimeline=async(dStr)=>{
    const box=$('#timeline-content');
    if(!box)return;
    box.innerHTML='<span class=spin></span> Loading doses...';
    try{
      const data=await api('/timeline?date='+dStr);
      const doses=data.doses||[];
      if(!doses.length){
        box.innerHTML='<p class="empty" style="padding:20px">No scheduled doses for '+esc(dStr)+'.</p>';
        return;
      }
      box.innerHTML=doses.map(d=>{
        const timePart=(d.due||'').split(' ')[1]||d.due;
        let badgeClass='badge pending';
        let statusLabel='Pending';
        if(d.status==='taken'){badgeClass='badge taken';statusLabel='Taken';}
        else if(d.status==='skipped'){badgeClass='badge skipped';statusLabel='Skipped';}
        const actions=d.status==='pending'?`<div style="display:flex;gap:6px"><button class="btn sm log-dose-btn" data-id="${d.id}" data-st="taken">Take Dose</button><button class="btn ghost sm log-dose-btn" data-id="${d.id}" data-st="skipped">Skip</button></div>`:`<span class="${badgeClass}">${statusLabel}</span>`;
        return `<div class=timeline-item><div><span class="badge" style="background:#1e293b;color:#cbd5e1;margin-right:8px;font-family:monospace">${esc(timePart)}</span><b>${esc(d.name)}</b> <span style="color:var(--mut)">${esc(d.strength||'')}</span></div><div>${actions}</div></div>`;
      }).join('');
      box.querySelectorAll('.log-dose-btn').forEach(b=>{
        b.onclick=async()=>{
          const did=b.getAttribute('data-id');
          const st=b.getAttribute('data-st');
          b.disabled=true;
          try{
            await api('/doses/'+did,{body:{status:st}});
            loadTimeline($('#cal-date').value);
          }catch(e){
            alert(e.message);
            b.disabled=false;
          }
        };
      });
    }catch(err){box.innerHTML=`<p class=err>${err.message}</p>`}
  };

  const cInput=$('#cal-date');
  if(cInput){
    cInput.onchange=()=>loadTimeline(cInput.value);
    $('#cal-today').onclick=()=>{ cInput.value=todayStr; loadTimeline(todayStr); };
    $('#cal-prev').onclick=()=>{
      const d=new Date(cInput.value||todayStr);
      d.setDate(d.getDate()-1);
      cInput.value=d.toISOString().slice(0,10);
      loadTimeline(cInput.value);
    };
    $('#cal-next').onclick=()=>{
      const d=new Date(cInput.value||todayStr);
      d.setDate(d.getDate()+1);
      cInput.value=d.toISOString().slice(0,10);
      loadTimeline(cInput.value);
    };
    loadTimeline(todayStr);
  }

  const loadSummary=async()=>{
    const box=$('#ai-summary-body');
    if(!box)return;
    box.innerHTML='<span class=spin></span> Generating clinical timing regimen...';
    try{
      const data=await api('/medicines/summary');
      if(!data.total_medications){
        box.innerHTML='<p class="empty" style="padding:16px">No active medicines scheduled. Scan or enter a prescription to see smart consumption instructions.</p>';
        return;
      }
      const badge=$('#ai-badge');
      if(badge&&data.source&&data.source.includes('Gemini')){
        badge.textContent='Google Gemini 1.5 Flash (Live AI)';
        badge.style.background='#10b981';
      }
      let html=`<p style="font-size:15px;line-height:1.6;margin-bottom:14px"><b>Regimen Overview:</b> ${esc(data.summary)}</p>`;
      const slots=data.slots||{};
      const slotDefs=[
        {key:'morning',title:'Morning (Breakfast / Empty Stomach)',color:'#0284c7'},
        {key:'afternoon',title:'Afternoon (Lunch)',color:'#0f766e'},
        {key:'evening',title:'Evening (Dinner)',color:'#b45309'},
        {key:'night',title:'Night (Bedtime)',color:'#6366f1'}
      ];
      html+='<div class=grid style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px">';
      slotDefs.forEach(s=>{
        const items=slots[s.key]||[];
        if(items.length){
          html+=`<div class=slot-card style="border-left:4px solid ${s.color}"><b style="color:${s.color};display:block;margin-bottom:6px">${s.title}</b>${items.map(it=>`<div style="font-size:14px;margin-bottom:6px"><b>${esc(it.name)}</b> <span style="font-family:monospace;color:var(--mut)">(${esc(it.time)})</span><br><span style="color:var(--mut);font-size:12px">${esc(it.hint)}</span></div>`).join('')}</div>`;
        }
      });
      html+='</div>';
      if(data.guidelines&&data.guidelines.length){
        html+='<div style="margin-top:14px"><b style="font-size:14px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em">Doctor Instructions & Precautions</b><div style="margin-top:8px;display:grid;gap:8px">';
        data.guidelines.forEach(g=>{
          html+=`<div style="padding:10px 12px;background:rgba(255,255,255,0.02);border:1px solid var(--bd);border-radius:8px"><b>${esc(g.medicine)}:</b> <span style="color:#2dd4bf">${esc(g.timing)}</span> - ${esc(g.instructions)} <i style="color:var(--mut)">(${esc(g.note)})</i></div>`;
        });
        html+='</div></div>';
      }
      box.innerHTML=html;
    }catch(err){box.innerHTML=`<p class=err>${err.message}</p>`}
  };

  const btnReload=$('#btn-reload-summary');
  if(btnReload)btnReload.onclick=loadSummary;
  loadSummary();

  $('#del').onclick=async()=>{if(confirm('Permanently delete your account and all data?')){await api('/account',{method:'DELETE'});user=null;nav();location.hash='#/'}};
  if(!user.onboarded)onboard();remind()},
 privacy:()=>doc('Privacy Policy',['What we collect','Your email, hashed password, uploaded prescription text and your medicine schedule. Images are processed in memory and not stored.','How we use it','Only to run your account, scan prescriptions and send reminders. We do not sell data.','Your rights','You can delete your account and all associated data at any time from the dashboard.','Contact','Add your contact email here before launch.']),
 terms:()=>doc('Terms of Service',['Assistive tool','MediAssist helps you organise medicines. It is not medical advice and does not replace a doctor or pharmacist.','Accuracy','OCR can be wrong. You must confirm every medicine and dose before saving.','Use','Do not misuse the service. We may suspend abusive accounts.','Liability','The service is provided as is. Have these terms reviewed by a lawyer before launch.'])};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const doc=(t,p)=>{app.innerHTML=`<section class=doc><h1>${t}</h1>${p.map((x,i)=>i%2?`<p>${x}</p>`:`<h2>${x}</h2>`).join('')}</section>`};
async function scan(e){const f=e.target.files[0];if(!f)return;const fd=new FormData();fd.append('image',f);$('#serr').textContent='';$('#draft').innerHTML='<span class=spin></span> Reading prescription...';
 try{const d=await api('/scan',{body:fd});if(!d.medicines.length){$('#draft').innerHTML='';$('#serr').textContent='No medicines detected. Try a clearer, well-lit photo.';return}
  $('#draft').innerHTML=`<p>Review and correct before saving:</p>${d.medicines.map((x,i)=>`<div class=grid style="margin:8px 0"><input value="${esc(x.name)}" data-i=${i} data-k=name><input value="${esc(x.strength)}" data-i=${i} data-k=strength placeholder=strength><input value="${x.times.join(',')}" data-i=${i} data-k=times><input type=number min=1 max=365 value=${x.days} data-i=${i} data-k=days></div>`).join('')}<button class=btn id=save>Confirm and save</button>`;
  $('#save').onclick=async()=>{const meds=d.medicines.map((x,i)=>{const g=k=>$(`[data-i="${i}"][data-k=${k}]`).value;return{...x,name:g('name'),strength:g('strength'),times:g('times').split(',').map(s=>s.trim()),days:+g('days')}});
   try{await api('/prescriptions',{body:{raw:d.raw,medicines:meds}});routes.dash()}catch(x){$('#serr').textContent=x.message}}}catch(x){$('#draft').innerHTML='';$('#serr').textContent=x.message}}
let _mp = null;

const gmapsBtn = (q, label) => {
  const query = q || 'pharmacies+near+me';
  return `<div style="margin-top:12px"><a class="btn" style="background:#4285f4;color:#fff;text-decoration:none;display:inline-block" href="https://www.google.com/maps/search/pharmacies+near+${encodeURIComponent(query)}" target=_blank rel=noopener>Open "${esc(label || query)}" in Google Maps</a></div>`;
};

async function renderMapWithPharmacies(lat, lon, locationName){
  const m = $('#map');
  const errBox = $('#map-status');
  m.hidden = false;
  errBox.innerHTML = '<p class=ok><span class=spin></span> Loading nearby medical stores...</p>';

  if(_mp){ _mp.remove(); _mp = null; }
  try {
    _mp = L.map('map').setView([lat, lon], 14);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'OpenStreetMap',
      maxZoom: 19
    }).addTo(_mp);
    L.marker([lat, lon]).addTo(_mp).bindPopup(`<b>${esc(locationName || 'Selected Location')}</b>`).openPopup();
  } catch(e) {
    console.error('Map init error:', e);
  }

  const query = `[out:json][timeout:15];node[amenity=pharmacy](around:3500,${lat},${lon});out 30;`;
  const endpoints = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter'
  ];

  let found = 0;
  for(const ep of endpoints){
    try {
      const ctrl = new AbortController();
      const tid = setTimeout(() => ctrl.abort(), 6000);
      const r = await fetch(ep, {method: 'POST', body: query, signal: ctrl.signal});
      clearTimeout(tid);
      if(!r.ok) continue;
      const data = await r.json();
      if(data && data.elements && data.elements.length){
        data.elements.forEach(n => {
          if(_mp){
            const name = n.tags?.name || 'Medical Store / Pharmacy';
            const street = n.tags?.['addr:street'] || n.tags?.['addr:full'] || '';
            L.marker([n.lat, n.lon]).addTo(_mp).bindPopup(`<b>${esc(name)}</b>${street ? '<br>' + esc(street) : ''}`);
          }
        });
        found = data.elements.length;
        break;
      }
    } catch(e) {}
  }

  const queryLabel = locationName || `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
  if(found > 0){
    errBox.innerHTML = `<p class=ok>Found ${found} pharmacies within 3.5 km of ${esc(queryLabel)}.</p>${gmapsBtn(`${lat},${lon}`, queryLabel)}`;
  } else {
    errBox.innerHTML = `<p class=err>No pharmacy data returned from OpenStreetMap for this specific area.</p>${gmapsBtn(`${lat},${lon}`, queryLabel)}`;
  }
}

async function searchArea(query){
  if(!query || !query.trim()){
    alert('Please enter an area, city, or pincode.');
    return;
  }
  const q = query.trim();
  const m = $('#map');
  const errBox = $('#map-status');
  errBox.innerHTML = `<p class=ok><span class=spin></span> Searching for "${esc(q)}"...</p>`;

  try {
    const geoUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}&limit=1`;
    const res = await fetch(geoUrl, { headers: { 'Accept': 'application/json' } });
    const places = await res.json();
    if(!places || !places.length){
      errBox.innerHTML = `<p class=err>Could not find coordinates for "${esc(q)}".</p>${gmapsBtn(q, q)}`;
      return;
    }
    const lat = parseFloat(places[0].lat);
    const lon = parseFloat(places[0].lon);
    await renderMapWithPharmacies(lat, lon, places[0].display_name.split(',')[0]);
  } catch(e) {
    errBox.innerHTML = `<p class=err>Network error searching area.</p>${gmapsBtn(q, q)}`;
  }
}

async function nearby(){
  const m = $('#map');
  const errBox = $('#map-status');
  errBox.innerHTML = '<p class=ok><span class=spin></span> Requesting GPS location permission...</p>';

  if(!navigator.geolocation){
    errBox.innerHTML = `<p class=err>Geolocation is not supported by your browser. Use the manual search box above.</p>${gmapsBtn(null, 'your area')}`;
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async p => {
      await renderMapWithPharmacies(p.coords.latitude, p.coords.longitude, 'Your Location');
    },
    err => {
      let guide = '';
      if(err.code === 1){
        guide = `
          <div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;padding:12px;margin:10px 0">
            <b style="color:#ef4444">Location Permission is Blocked in Browser</b>
            <p style="margin:6px 0;font-size:14px">Your browser has blocked location access for <code>http://localhost:5000</code>.</p>
            <p style="margin:4px 0;font-size:13px"><b>How to unblock in Chrome / Edge:</b></p>
            <ol style="margin:4px 0 8px 20px;font-size:13px;padding:0">
              <li>Click the <b>View site information / Tune icon</b> (left of the address bar next to <code>localhost:5000</code>).</li>
              <li>Change <b>Location</b> from <i>Block</i> to <b>Allow</b>.</li>
              <li>Refresh the page and click <i>Use my GPS location</i> again.</li>
            </ol>
            <p style="margin:0;font-size:13px"><i>Or simply enter your city or pincode in the search box above!</i></p>
          </div>
        `;
      } else if(err.code === 2){
        guide = `<p class=err>Location position unavailable. Please enable Windows Location in Windows Settings or use the manual search box above.</p>`;
      } else {
        guide = `<p class=err>Location request timed out. Use the manual search box above.</p>`;
      }
      errBox.innerHTML = guide + gmapsBtn(null, 'your current area');
    },
    { timeout: 8000, enableHighAccuracy: true }
  );
}
function onboard(){const st=['Scan a prescription photo.','Confirm the medicines it found.','Allow notifications to get reminders.'];let i=0;const d=document.createElement('div');d.className='modal';
 const r=()=>{d.innerHTML=`<div class=card><small>Step ${i+1} of 3</small><h2>${st[i]}</h2><button class=btn id=nx>${i<2?'Next':'Finish'}</button></div>`;$('#nx',d).onclick=async()=>{if(++i>2){await api('/onboarded',{method:'POST',body:{}});d.remove();user.onboarded=1;Notification?.requestPermission?.()}else r()}};r();document.body.append(d)}
let rt;function remind(){clearInterval(rt);const tick=async()=>{try{for(const x of await api('/reminders/due')){if(Notification.permission==='granted'){new Notification('Time for '+x.name,{body:'Open MediAssist to log this dose.'})}
 if(!$('#r'+x.id)){app.insertAdjacentHTML('afterbegin',`<div class=card id=r${x.id} style="margin:16px 5vw">${esc(x.name)} due ${x.due.slice(11)} <button class=btn data-a=taken>Taken</button> <button class="btn ghost" data-a=snooze>Snooze 10m</button> <button class="btn ghost" data-a=skipped>Skip</button></div>`);$('#r'+x.id).onclick=async e=>{const a=e.target.dataset.a;if(a){await api('/doses/'+x.id,{body:{status:a}});$('#r'+x.id).remove()}}}}}catch{}};tick();rt=setInterval(tick,30000)}
async function boot(){try{user=(await api('/me')).user;if(user)localStorage.setItem('ma_auth','1');else localStorage.removeItem('ma_auth')}catch{user=null}nav();const lo=$('#lo');if(lo)lo.onclick=async()=>{localStorage.removeItem('ma_auth');await api('/logout',{method:'POST',body:{}});user=null;nav();location.hash='#/'}}
async function route(){const[,p,a]=location.hash.split('/');scrollTo(0,0);if(!user&&localStorage.getItem('ma_auth')==='1'){try{user=(await api('/me')).user}catch{user=null}}(routes[p||'']||(()=>app.innerHTML='<section><h1>404</h1><a href=/>Home</a></section>'))(a);nav();const lo=$('#lo');if(lo)lo.onclick=async()=>{localStorage.removeItem('ma_auth');await api('/logout',{method:'POST',body:{}});user=null;nav();location.hash='#/'}}
addEventListener('hashchange',route);boot().then(route);
