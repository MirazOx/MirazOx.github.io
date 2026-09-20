import re

with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

# 1. Fix Storage Logic
old_storage = '''async function save(){ try{ await window.storage.set(KEY, JSON.stringify(STATE)); }catch(e){} }
async function load(){
  try{ const r = await window.storage.get(KEY); if(r && r.value){ STATE = JSON.parse(r.value); } }catch(e){}
  if(!STATE.stats) STATE.stats={}; if(!STATE.log) STATE.log=[]; ready=true;
}'''

new_storage = '''function save(){ try{ localStorage.setItem(KEY, JSON.stringify(STATE)); }catch(e){} }
function load(){
  try{ const r = localStorage.getItem(KEY); if(r){ STATE = JSON.parse(r); } }catch(e){}
  if(!STATE.stats) STATE.stats={}; if(!STATE.log) STATE.log=[]; if(!STATE.focus) STATE.focus=null; ready=true;
}'''
html = html.replace(old_storage, new_storage)

# 2. Fix Await Calls
html = html.replace('await save()', 'save()')
html = html.replace('await load()', 'load()')

# 3. Add Focus mode to DOM in Learn view
# Locate: <span id="p-active">Active: 0</span>
# We'll change it to have a button to clear focus if active.
html = html.replace('<span id="p-active">Active: 0</span>', '<span id="p-active">Active: 0</span> <button id="btn-clear-focus" style="display:none; background:none; border:1px solid var(--accent); color:var(--accent); padding:2px 6px; font-size:0.6rem; margin-left:10px; cursor:pointer;">EXIT FOCUS</button>')

# 4. Modify `pick()`
old_pick = '''function pick(){
  let pool=[], tot=0;
  for(let i=0;i<N;i++){ const w=weight(i); if(w>0){ pool.push([i,w]); tot+=w; } }
  if(!pool.length) return null;
  let r=Math.random()*tot;
  for(const [i,w] of pool){ r-=w; if(r<=0) return i; }
  return pool[pool.length-1][0];
}'''

new_pick = '''function pick(){
  let pool=[], tot=0;
  for(let i=0;i<N;i++){
    const s=st(i);
    let valid = false;
    if(STATE.focus === 'nem') {
       if(s.wrong + s.confused >= 4 && !s.mastered) valid = true;
    } else if(STATE.focus === 'shk') {
       if(s.wrong + s.confused >= 1 && s.wrong + s.confused <= 3 && !s.mastered) valid = true;
    } else if(STATE.focus === 'unt') {
       if(s.seen === 0 && !s.mastered) valid = true;
    } else {
       if(!s.mastered) valid = true;
    }
    
    if(valid){
        const w=weight(i); 
        if(w>0){ pool.push([i,w]); tot+=w; }
    }
  }
  if(!pool.length) return null;
  let r=Math.random()*tot;
  for(const [i,w] of pool){ r-=w; if(r<=0) return i; }
  return pool[pool.length-1][0];
}

function setFocus(f) {
  STATE.focus = f;
  save();
  switchView('learn');
  loadNext();
}

function clearFocus() {
  STATE.focus = null;
  save();
  loadNext();
}
'''
html = html.replace(old_pick, new_pick)

# 5. Modify UpdateProg to show Focus
old_update_prog = '''function updateProg(){
  let mas=0,active=0;
  for(let i=0;i<N;i++){ const s=STATE.stats[i]; if(s&&s.mastered)mas++; }
  active=N-mas;
  el('p-active').textContent='ACTIVE: '+active;
  el('p-txt').textContent=mas+' / '+N+' MASTERED';
  el('p-bar').style.width=(mas/N*100)+'%';
}'''

new_update_prog = '''function updateProg(){
  let mas=0,active=0;
  for(let i=0;i<N;i++){ const s=STATE.stats[i]; if(s&&s.mastered)mas++; }
  active=N-mas;
  if(STATE.focus) {
      const labels = {nem: 'NEMESIS', shk: 'SHAKY', unt: 'UNTOUCHED'};
      el('p-active').innerHTML = `FOCUS: ${labels[STATE.focus]}`;
      el('btn-clear-focus').style.display = 'inline-block';
  } else {
      el('p-active').textContent='ACTIVE: '+active;
      if(el('btn-clear-focus')) el('btn-clear-focus').style.display = 'none';
  }
  el('p-txt').textContent=mas+' / '+N+' MASTERED';
  el('p-bar').style.width=(mas/N*100)+'%';
}'''
html = html.replace(old_update_prog, new_update_prog)

# 6. Add Practice buttons to Deck headers
# e.g. <h3><span>[ NEMESIS ] <span class="c">Wrong 4+ times</span></span><span class="c" id="d-nem-c">0</span></h3>
# We can inject a button right next to the title or inside the body.
# Let's inject a "Practice this deck" at the top of the body of each deck.
old_fillDeck = '''function fillDeck(bodyId,cntId,arr,meta,plain){
  el(cntId).textContent=arr.length;
  const body=el(bodyId);
  if(!arr.length){ body.innerHTML='<div class="empty">Empty</div>'; return; }
  body.innerHTML=arr.map(i=>{'''

new_fillDeck = '''function fillDeck(bodyId,cntId,arr,meta,plain){
  el(cntId).textContent=arr.length;
  const body=el(bodyId);
  if(!arr.length){ body.innerHTML='<div class="empty">Empty</div>'; return; }
  
  let h = '';
  if(bodyId !== 'd-mas') {
     let type = bodyId.replace('d-', '');
     h += `<button style="background:var(--fg); color:var(--bg); border:none; padding:8px 16px; margin-bottom:1rem; font-family:var(--font-mono); font-size:0.7rem; text-transform:uppercase; cursor:pointer;" onclick="setFocus('${type}')">Practice This Deck (${arr.length} words)</button>`;
  }
  
  body.innerHTML = h + arr.map(i=>{'''
html = html.replace(old_fillDeck, new_fillDeck)

# 7. Bind clearFocus
# e.g. el('btn-reset').onclick=resetAll;
html = html.replace("el('btn-reset').onclick=resetAll;", "el('btn-reset').onclick=resetAll;\nif(el('btn-clear-focus')) el('btn-clear-focus').onclick=clearFocus;")

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied logic fixes.")
