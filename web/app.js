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
  const nodes=state.nodes.filter(n=>(state.role==='all'||n.roles.includes(state.role))&&(state.domain==='all'||n.domain===state.domain)&&(`${n.id} ${n.domain} ${n.roles.join(' ')}`.includes(q)));
  $('#node-grid').innerHTML=nodes.map(n=>`<article class="node"><div><span class="domain">${n.domain.replaceAll('-',' ')}</span><h3>${n.id.replaceAll('-',' ')}</h3></div><div class="tags">${n.roles.map(r=>`<span class="tag">${r}</span>`).join('')}</div></article>`).join('');
  $('#empty').hidden=nodes.length>0;
}
function render(){renderRoles();renderFilters();renderNodes()}
async function boot(){
  try{
    const [nodes,topology,summary]=await Promise.all(['/api/nodes','/api/topology','/api/summary'].map(u=>fetch(u).then(r=>r.json())));
    state.nodes=nodes.devices;state.topology=topology;
    $('#node-count').textContent=summary.nodes;$('#domain-count').textContent=Object.keys(summary.domains).length;
    render();
  }catch(error){$('#system-state').textContent='CONTROL PLANE OFFLINE';console.error(error)}
}
$('#search').addEventListener('input',e=>{state.query=e.target.value;renderNodes()});boot();
