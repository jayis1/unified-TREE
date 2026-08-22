const state={nodes:[],topology:null,role:'all',domain:'all',query:''};
const $=s=>document.querySelector(s);
const roleCopy={observe:'Acquire calibrated measurements and physical events.',reason:'Fuse signals and produce findings or commands.',act:'Perform guarded physical work with local feedback.',coordinate:'Connect people, history, policy, and fleets.'};

function renderRoles(){
  const counts=Object.fromEntries(['observe','reason','act','coordinate'].map(r=>[r,state.nodes.filter(n=>n.roles.includes(r)).length]));
  $('#role-map').innerHTML=['observe','reason','act','coordinate'].map((r,i)=>`<button class="role ${state.role===r?'active':''}" data-role="${r}"><span class="num">0${i+1} / ${counts[r]} NODES</span><h3>${r}</h3><p>${roleCopy[r]}</p></button>`).join('');
  document.querySelectorAll('.role').forEach(el=>el.onclick=()=>{state.role=state.role===el.dataset.role?'all':el.dataset.role;render()});
}
function renderFilters(){
  const domains=['all',...new Set(state.nodes.map(n=>n.domain))];
  $('#filters').innerHTML=domains.map(d=>`<button class="filter ${state.domain===d?'active':''}" data-domain="${d}">${d.replaceAll('-',' ')}</button>`).join('');
  document.querySelectorAll('.filter').forEach(el=>el.onclick=()=>{state.domain=el.dataset.domain;renderNodes();renderFilters()});
}
function renderNodes(){
  const q=state.query.toLowerCase();
  const nodes=state.nodes.filter(n=>(state.role==='all'||n.roles.includes(state.role))&&(state.domain==='all'||n.domain===state.domain)&&(`${n.id} ${n.title||''} ${n.system||''} ${n.collection||''} ${n.domain} ${n.roles.join(' ')}`.toLowerCase().includes(q)));
  $('#node-grid').innerHTML=nodes.map(n=>`<article class="node"><div><span class="domain">${n.collection||'SoC Device Inventions'} · ${n.domain.replaceAll('-',' ')}</span><h3>${(n.title||n.id).replaceAll('-',' ')}</h3>${n.system?`<small>${n.system}</small>`:''}</div><div class="tags">${n.roles.map(r=>`<span class="tag">${r}</span>`).join('')}</div></article>`).join('');
  $('#empty').hidden=nodes.length>0;
}
function render(){renderRoles();renderFilters();renderNodes()}
async function boot(){
  try{
    let nodes,topology,summary;
    try{
      [nodes,topology,summary]=await Promise.all(['./api/nodes','./api/topology','./api/summary'].map(u=>fetch(u).then(r=>{if(!r.ok)throw new Error(r.status);return r.json()})));
      nodes={devices:nodes.nodes};
    }catch(_apiUnavailable){
      const [soc,systems,tree]=await Promise.all(['./devices.json','./systems.json','./platform.json'].map(u=>fetch(u).then(r=>{if(!r.ok)throw new Error(r.status);return r.json()})));
      topology=tree;
      nodes={devices:[...soc.devices.map(n=>({...n,collection:'SoC Device Inventions',system:null})),...systems.systems.flatMap(s=>s.nodes.map(n=>({id:`${s.id}/${n.id}`,title:n.id,domain:s.domain,roles:n.roles,collection:'Devices',system:s.title}))) ]};
      summary={nodes:nodes.devices.length,systems:systems.systems.length,domains:Object.fromEntries([...new Set(nodes.devices.map(n=>n.domain))].map(d=>[d,nodes.devices.filter(n=>n.domain===d).length]))};
    }
    state.nodes=nodes.devices;state.topology=topology;
    $('#node-count').textContent=summary.nodes;$('#system-count').textContent=summary.systems;$('#domain-count').textContent=Object.keys(summary.domains).length;
    render();
  }catch(error){$('#system-state').textContent='CONTROL PLANE OFFLINE';console.error(error)}
}
let installPrompt;
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installPrompt=event;$('#install-app').hidden=false});
$('#install-app').addEventListener('click',async()=>{if(!installPrompt)return;installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;$('#install-app').hidden=true});
window.addEventListener('appinstalled',()=>{$('#install-app').hidden=true});
if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js'));
$('#search').addEventListener('input',e=>{state.query=e.target.value;renderNodes()});boot();
