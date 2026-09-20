with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

# 1. HTML Injections
html = html.replace('<div class="ipa" id="q-ipa"></div>', '<div class="ipa" id="q-ipa"></div>\n      <div id="q-mcq" style="display:none; width: 100%;"></div>')

btns_back = '''      <div class="btns" id="q-btns-back" style="display:none">
        <button data-r="correct">Got it</button>
        <button class="b-miss" data-r="miss">Missed</button>
        <button data-r="confused">Confused</button>
      </div>'''

btns_next = '''      <div class="btns" id="q-btns-back" style="display:none">
        <button data-r="correct">Got it</button>
        <button class="b-miss" data-r="miss">Missed</button>
        <button data-r="confused">Confused</button>
      </div>
      <div class="btns" id="q-btns-next" style="display:none">
        <button id="btn-next" style="grid-column: 1 / -1;">Next Word</button>
      </div>'''
html = html.replace(btns_back, btns_next)

# 2. CSS Injection
css_inj = '''
  .mcq-opts { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 2rem; width: 100%; }
  .mcq-btn { background: transparent; border: 1px solid var(--border); color: var(--fg); font-family: var(--font-mono); font-size: 0.8rem; padding: 1.25rem; text-align: left; cursor: pointer; transition: 0.15s ease; text-transform: uppercase; letter-spacing: 0.05em; }
  .mcq-btn:hover { border-color: var(--muted); }
  .mcq-btn.correct { background: var(--fg); color: var(--bg); border-color: var(--fg); }
  .mcq-btn.wrong { background: var(--accent); color: var(--bg); border-color: var(--accent); }
</style>'''
html = html.replace('</style>', css_inj)

# 3. JS Modifications in loadNext()
old_loadNext = '''  if(studyMode === 'word') {
      el('q-word').style.fontSize = '3.5rem';
      el('q-word').textContent = W.word;
      el('q-pos').textContent = W.pos;
      el('q-ipa').textContent = W.ipa || '';
      el('q-pos').style.display = 'inline-block';
      el('q-ipa').style.display = 'inline-block';
      document.querySelector('.prompt').textContent = 'Recall the meaning';
      el('q-ex').innerHTML = esc(W.ex);
  } else {
      el('q-word').style.fontSize = '1.35rem';
      el('q-pos').style.display = 'none';
      el('q-ipa').style.display = 'none';
      
      // Blank out the word (and basic variants like -s, -ed, -ing if possible, but mostly just the base word)
      let blanked = W.ex;
      if (W.ex) {
          const reg = new RegExp(W.word.substring(0, W.word.length-1) + "[a-z]*", "gi");
          blanked = W.ex.replace(reg, '_______');
      }
      el('q-word').textContent = blanked || "No example sentence available.";
      document.querySelector('.prompt').textContent = 'Recall the word';
      
      const posIpa = `<span style="font-family:var(--font-mono); color:var(--muted); font-size:0.75rem;">[${W.pos}] ${W.ipa || ''}</span>`;
      el('q-ex').innerHTML = `<strong>Word:</strong> ${W.word} ${posIpa}<br><br><strong>Context:</strong> ${esc(W.ex)}`;
  }
  
  el('q-def').textContent=W.def;
  const g=el('q-gre');
  if(W.gre){ g.style.display='block'; g.innerHTML='GRE TRAP: '+esc(W.gre); }
  else g.style.display='none';
  el('q-reveal').style.display='none';
  el('q-btns-front').style.display='grid';
  el('q-btns-back').style.display='none';
  el('q-flash').textContent='';'''

new_loadNext = '''  el('q-def').textContent=W.def;
  const g=el('q-gre');
  if(W.gre){ g.style.display='block'; g.innerHTML='GRE TRAP: '+esc(W.gre); }
  else g.style.display='none';
  el('q-reveal').style.display='none';
  el('q-flash').textContent='';
  
  el('q-mcq').innerHTML = '';
  el('q-mcq').style.display = 'none';
  el('q-btns-next').style.display = 'none';
  el('q-btns-front').style.display = 'none';
  el('q-btns-back').style.display = 'none';

  if(studyMode === 'word') {
      el('q-word').style.fontSize = '3.5rem';
      el('q-word').textContent = W.word;
      el('q-pos').textContent = W.pos;
      el('q-ipa').textContent = W.ipa || '';
      el('q-pos').style.display = 'inline-block';
      el('q-ipa').style.display = 'inline-block';
      document.querySelector('.prompt').textContent = 'Recall the meaning';
      el('q-ex').innerHTML = esc(W.ex);
      el('q-btns-front').style.display='grid';
  } else {
      el('q-word').style.fontSize = '1.35rem';
      el('q-pos').style.display = 'none';
      el('q-ipa').style.display = 'none';
      
      let blanked = W.ex;
      if (W.ex) {
          const reg = new RegExp(W.word.substring(0, W.word.length-1) + "[a-z]*", "gi");
          blanked = W.ex.replace(reg, '_______');
      }
      el('q-word').textContent = blanked || "No example sentence available.";
      document.querySelector('.prompt').textContent = 'Fill in the blank';
      
      const posIpa = `<span style="font-family:var(--font-mono); color:var(--muted); font-size:0.75rem;">[${W.pos}] ${W.ipa || ''}</span>`;
      el('q-ex').innerHTML = `<strong>Word:</strong> ${W.word} ${posIpa}<br><br><strong>Context:</strong> ${esc(W.ex)}`;
      
      // Generate MCQ Options
      let opts = [W.word];
      while(opts.length < 4) {
          let rand = WORDS[Math.floor(Math.random()*WORDS.length)].word;
          if(!opts.includes(rand)) opts.push(rand);
      }
      opts.sort(() => Math.random() - 0.5);
      
      let optsHtml = '<div class="mcq-opts">';
      opts.forEach(o => {
          optsHtml += `<button class="mcq-btn" onclick="mcqAnswer('${o}')">${o}</button>`;
      });
      optsHtml += '</div>';
      el('q-mcq').innerHTML = optsHtml;
      el('q-mcq').style.display = 'block';
  }'''
html = html.replace(old_loadNext, new_loadNext)


# 4. JS: Global mcqAnswer and btn-next binding
bindings_old = '''el('btn-show').onclick=showDef;'''
bindings_new = '''el('btn-show').onclick=showDef;

window.mcqAnswer = function(selectedWord) {
    if(shown) return;
    const W = WORDS[STATE.cur];
    const isCorrect = (selectedWord === W.word);
    
    document.querySelectorAll('.mcq-btn').forEach(btn => {
        if(btn.textContent === W.word) btn.classList.add('correct');
        else if(btn.textContent === selectedWord) btn.classList.add('wrong');
        btn.style.pointerEvents = 'none';
    });
    
    el('q-reveal').style.display='block';
    
    record(isCorrect ? 'correct' : 'miss');
    const s = st(STATE.cur);
    let f = '';
    if(isCorrect) f='LOGGED CORRECT — STREAK '+s.streak+'/5'+(s.mastered?' · MASTERED':'');
    else f='LOGGED MISSED — STREAK RESET';
    el('q-flash').textContent = f;
    
    shown = true;
    el('q-btns-next').style.display = 'grid';
};

if(el('btn-next')) {
  el('btn-next').onclick = () => {
      loadNext();
      el('q-flash').textContent='';
  };
}
'''
html = html.replace(bindings_old, bindings_new)

# 5. Fix end of file keyboard binding to support 1, 2, 3 only for word mode (or check if q-btns-back is visible)
# Currently it says: else if(shown && e.key==='1') answer('correct');
# This would trigger even in Context Mode!
# We should change `shown` checks.
key_bind_old = '''  if(e.code==='Space'){ if(!shown){ e.preventDefault(); showDef(); } }
  else if(shown && e.key==='1') answer('correct');
  else if(shown && e.key==='2') answer('miss');
  else if(shown && e.key==='3') answer('confused');'''
key_bind_new = '''  if(studyMode === 'word') {
      if(e.code==='Space'){ if(!shown){ e.preventDefault(); showDef(); } }
      else if(shown && e.key==='1') answer('correct');
      else if(shown && e.key==='2') answer('miss');
      else if(shown && e.key==='3') answer('confused');
  } else {
      if(shown && e.code==='Space'){ e.preventDefault(); loadNext(); }
  }'''
html = html.replace(key_bind_old, key_bind_new)

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied MCQ logic.")
